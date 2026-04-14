from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from voice_tts.domain.entities import SynthesisRequest, SynthesisResult
from voice_tts.domain.value_objects import LanguageCode, SamplingProfile
from voice_tts.exceptions import VoiceTtsUsageError, with_stage


@dataclass(frozen=True, slots=True)
class SynthesizeSpeechCommand:
    model_profile_id: str
    text: str
    text_lang: str
    ref_audio_path: Path
    ref_start_sec: float | None = None
    ref_end_sec: float | None = None
    prompt_text: str = ""
    prompt_lang: str = "auto"
    output_path: Path | None = None
    top_p: float = 1.0
    temperature: float = 1.0
    force: bool = False

    def __post_init__(self) -> None:
        if not self.model_profile_id.strip():
            raise VoiceTtsUsageError(with_stage("preflight", "model_profile_id must not be blank"))
        if not self.text.strip():
            raise VoiceTtsUsageError(with_stage("preflight", "text must not be blank"))
        if not self.prompt_text.strip():
            raise VoiceTtsUsageError(with_stage("preflight", "prompt_text must not be blank"))
        if not str(self.ref_audio_path).strip():
            raise VoiceTtsUsageError(with_stage("preflight", "ref_audio_path must not be blank"))
        if self.ref_start_sec is not None and self.ref_start_sec < 0.0:
            raise VoiceTtsUsageError(with_stage("preflight", "ref_start_sec must be >= 0.0"))
        effective_start = self.ref_start_sec or 0.0
        if self.ref_end_sec is not None and self.ref_end_sec <= effective_start:
            raise VoiceTtsUsageError(
                with_stage("preflight", "ref_end_sec must be greater than ref_start_sec")
            )
        if self.output_path is not None and self.output_path.suffix.lower() != ".wav":
            raise VoiceTtsUsageError(with_stage("preflight", "output_path must end with .wav"))

    def resolve_output_path(self, output_root: Path) -> Path:
        resolved_path = self.output_path or (
            output_root
            / self.model_profile_id
            / f"{datetime.now():%Y%m%d-%H%M%S-%f}.wav"
        )
        if resolved_path.suffix.lower() != ".wav":
            raise VoiceTtsUsageError(with_stage("preflight", "output_path must end with .wav"))
        if resolved_path.exists() and resolved_path.is_dir():
            raise VoiceTtsUsageError(
                with_stage("preflight", f"output path points to a directory: {resolved_path}")
            )
        if resolved_path.exists() and not self.force:
            raise VoiceTtsUsageError(
                with_stage(
                    "preflight",
                    f"output file already exists: {resolved_path}; pass --force to overwrite",
                )
            )
        resolved_path.parent.mkdir(parents=True, exist_ok=True)
        return resolved_path

    def to_domain(self, output_path: Path) -> SynthesisRequest:
        try:
            return SynthesisRequest(
                model_profile_id=self.model_profile_id,
                text=self.text,
                text_lang=LanguageCode(self.text_lang),
                ref_audio_path=self.ref_audio_path,
                ref_start_sec=self.ref_start_sec,
                ref_end_sec=self.ref_end_sec,
                prompt_text=self.prompt_text,
                prompt_lang=LanguageCode(self.prompt_lang),
                output_path=output_path,
                sampling_profile=SamplingProfile(
                    top_p=self.top_p,
                    temperature=self.temperature,
                ),
            )
        except ValueError as exc:
            raise VoiceTtsUsageError(with_stage("preflight", str(exc))) from exc


@dataclass(frozen=True, slots=True)
class SynthesizeSpeechResultDto:
    audio_path: str
    sample_rate: int
    metadata: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_domain(cls, result: SynthesisResult) -> "SynthesizeSpeechResultDto":
        return cls(
            audio_path=str(result.audio_path),
            sample_rate=result.sample_rate,
            metadata=dict(result.metadata),
        )
