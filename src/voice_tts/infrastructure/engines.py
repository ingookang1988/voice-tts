from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import numpy as np
import soundfile as sf

from voice_tts.domain.entities import (
    SUPPORTED_MODEL_VERSION,
    ModelProfile,
    SynthesisRequest,
    SynthesisResult,
)
from voice_tts.exceptions import (
    VoiceTtsConfigurationError,
    VoiceTtsDependencyError,
    VoiceTtsSynthesisError,
    VoiceTtsUsageError,
)
from voice_tts.infrastructure.system import find_ffmpeg_executable


class GptSovitsV2SpeechSynthesisEngine:
    """Adapter that bridges the local use case to an external GPT-SoVITS checkout."""

    def __init__(
        self,
        gpt_sovits_root: Path | None,
        default_device: str,
        use_fp16: bool,
        temp_root: Path,
    ) -> None:
        self.gpt_sovits_root = gpt_sovits_root
        self.default_device = default_device
        self.use_fp16 = use_fp16
        self.temp_root = temp_root

    def synthesize(
        self,
        request: SynthesisRequest,
        model_profile: ModelProfile,
    ) -> SynthesisResult:
        if model_profile.version != SUPPORTED_MODEL_VERSION:
            raise VoiceTtsConfigurationError(
                f"unsupported model profile version: {model_profile.version}"
            )
        if not request.ref_audio_path.exists():
            raise VoiceTtsUsageError(
                f"reference audio was not found: {request.ref_audio_path}"
            )
        if not request.ref_audio_path.is_file():
            raise VoiceTtsUsageError(
                f"reference audio is not a file: {request.ref_audio_path}"
            )
        if not model_profile.tts_config_path.exists():
            raise VoiceTtsConfigurationError(
                f"tts config path was not found: {model_profile.tts_config_path}"
            )

        pipeline = self._build_pipeline(model_profile.tts_config_path)
        ref_audio_path = self._prepare_reference_audio(request)
        sample_rate, audio_data = self._run_pipeline(
            pipeline=pipeline,
            request=request,
            ref_audio_path=ref_audio_path,
        )

        request.output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            sf.write(
                file=str(request.output_path),
                data=np.asarray(audio_data),
                samplerate=int(sample_rate),
                format="WAV",
                subtype="PCM_16",
            )
        except Exception as exc:  # pragma: no cover - exercised in external smoke
            raise VoiceTtsSynthesisError(
                f"failed to write WAV output to {request.output_path}: {exc}"
            ) from exc

        return SynthesisResult(
            audio_path=request.output_path,
            sample_rate=int(sample_rate),
            metadata={
                "engine": SUPPORTED_MODEL_VERSION,
                "model_profile_id": model_profile.id,
                "ref_audio_path": str(ref_audio_path),
            },
        )

    def _build_pipeline(self, tts_config_path: Path):
        gpt_sovits_root = self._require_gpt_sovits_root()
        root_text = str(gpt_sovits_root)
        if root_text not in sys.path:
            sys.path.insert(0, root_text)
            importlib.invalidate_caches()

        try:
            from GPT_SoVITS.TTS_infer_pack.TTS import TTS, TTS_Config
        except Exception as exc:  # pragma: no cover - exercised in external smoke
            raise VoiceTtsDependencyError(
                f"failed to import GPT-SoVITS runtime from {gpt_sovits_root}: {exc}"
            ) from exc

        try:
            config = TTS_Config(str(tts_config_path))
            if self.default_device != "auto" and hasattr(config, "device"):
                config.device = self.default_device
            if hasattr(config, "is_half"):
                config.is_half = self.use_fp16
            return TTS(config)
        except Exception as exc:  # pragma: no cover - exercised in external smoke
            raise VoiceTtsDependencyError(
                f"failed to initialize GPT-SoVITS TTS runtime: {exc}"
            ) from exc

    def _prepare_reference_audio(self, request: SynthesisRequest) -> Path:
        if request.ref_start_sec is None and request.ref_end_sec is None:
            return request.ref_audio_path

        ffmpeg = find_ffmpeg_executable()
        if ffmpeg is None:
            raise VoiceTtsDependencyError(
                "ffmpeg was not found on PATH; install ffmpeg before using synthesize"
            )

        trim_root = self.temp_root / "ref-trims"
        trim_root.mkdir(parents=True, exist_ok=True)
        trimmed_audio_path = trim_root / f"{uuid4().hex}.wav"

        start_sec = request.ref_start_sec or 0.0
        command = [
            str(ffmpeg),
            "-y",
            "-i",
            str(request.ref_audio_path),
            "-ss",
            f"{start_sec:.3f}",
        ]
        if request.ref_end_sec is not None:
            duration = request.ref_end_sec - start_sec
            command.extend(["-t", f"{duration:.3f}"])
        command.extend(
            [
                "-vn",
                "-acodec",
                "pcm_s16le",
                str(trimmed_audio_path),
            ]
        )

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip() or "unknown ffmpeg error"
            raise VoiceTtsSynthesisError(f"ffmpeg failed to trim reference audio: {detail}")
        return trimmed_audio_path

    def _run_pipeline(self, pipeline, request: SynthesisRequest, ref_audio_path: Path):
        payload = {
            "text": request.text,
            "text_lang": request.text_lang.value,
            "ref_audio_path": str(ref_audio_path),
            "prompt_text": request.prompt_text,
            "prompt_lang": request.prompt_lang.value,
            "top_p": request.sampling_profile.top_p,
            "temperature": request.sampling_profile.temperature,
        }
        try:
            result = pipeline.run(payload)
            if isinstance(result, tuple) and len(result) == 2:
                sample_rate, audio_data = result
            else:
                sample_rate, audio_data = next(iter(result))
        except StopIteration as exc:  # pragma: no cover - exercised in external smoke
            raise VoiceTtsSynthesisError("GPT-SoVITS returned no audio frames") from exc
        except Exception as exc:  # pragma: no cover - exercised in external smoke
            raise VoiceTtsSynthesisError(f"GPT-SoVITS synthesis failed: {exc}") from exc
        return int(sample_rate), audio_data

    def _require_gpt_sovits_root(self) -> Path:
        if self.gpt_sovits_root is None:
            raise VoiceTtsConfigurationError(
                "VOICE_TTS_GPT_SOVITS_ROOT is required for synthesize"
            )
        if not self.gpt_sovits_root.exists():
            raise VoiceTtsConfigurationError(
                f"VOICE_TTS_GPT_SOVITS_ROOT does not exist: {self.gpt_sovits_root}"
            )
        if not self.gpt_sovits_root.is_dir():
            raise VoiceTtsConfigurationError(
                f"VOICE_TTS_GPT_SOVITS_ROOT is not a directory: {self.gpt_sovits_root}"
            )
        return self.gpt_sovits_root
