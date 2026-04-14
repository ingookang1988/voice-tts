from __future__ import annotations

import sys
from pathlib import Path

import soundfile as sf

from voice_tts.domain.entities import ModelProfile, SynthesisRequest
from voice_tts.domain.value_objects import LanguageCode, SamplingProfile
from voice_tts.infrastructure.engines import GptSovitsV2SpeechSynthesisEngine


def _write_fake_checkout(root: Path) -> None:
    package_root = root / "GPT_SoVITS" / "TTS_infer_pack"
    package_root.mkdir(parents=True)
    (root / "GPT_SoVITS" / "__init__.py").write_text("", encoding="utf-8")
    (package_root / "__init__.py").write_text("", encoding="utf-8")
    (package_root / "TTS.py").write_text(
        "\n".join(
            [
                "from __future__ import annotations",
                "",
                "import numpy as np",
                "",
                "",
                "class TTS_Config:",
                "    def __init__(self, config_path: str) -> None:",
                "        self.config_path = config_path",
                "        self.device = 'cpu'",
                "        self.is_half = False",
                "",
                "",
                "class TTS:",
                "    def __init__(self, config: TTS_Config) -> None:",
                "        self.config = config",
                "",
                "    def run(self, req):",
                "        audio = np.zeros(2400, dtype=np.int16)",
                "        return iter([(24000, audio)])",
            ]
        ),
        encoding="utf-8",
    )


def test_engine_generates_wav_with_fake_gpt_sovits_checkout(tmp_path: Path) -> None:
    checkout_root = tmp_path / "fake-gpt-sovits"
    _write_fake_checkout(checkout_root)

    config_path = tmp_path / "tts_infer.yaml"
    config_path.write_text("custom: {}\n", encoding="utf-8")
    ref_audio = tmp_path / "reference.wav"
    ref_audio.write_bytes(b"RIFF")
    output_path = tmp_path / "generated.wav"

    for module_name in (
        "GPT_SoVITS",
        "GPT_SoVITS.TTS_infer_pack",
        "GPT_SoVITS.TTS_infer_pack.TTS",
    ):
        sys.modules.pop(module_name, None)

    engine = GptSovitsV2SpeechSynthesisEngine(
        gpt_sovits_root=checkout_root,
        default_device="cpu",
        use_fp16=False,
        temp_root=tmp_path / "tmp",
    )
    profile = ModelProfile(
        id="gsv2-default",
        version="gpt-sovits-v2",
        tts_config_path=config_path,
    )
    request = SynthesisRequest(
        model_profile_id="gsv2-default",
        text="안녕하세요",
        text_lang=LanguageCode("ko"),
        ref_audio_path=ref_audio,
        prompt_text="안녕하세요, 반갑습니다.",
        prompt_lang=LanguageCode("ko"),
        output_path=output_path,
        sampling_profile=SamplingProfile(top_p=1.0, temperature=1.0),
    )

    result = engine.synthesize(request, profile)

    assert result.audio_path == output_path
    assert output_path.exists()
    audio_data, sample_rate = sf.read(str(output_path))
    assert sample_rate == 24000
    assert len(audio_data) == 2400
