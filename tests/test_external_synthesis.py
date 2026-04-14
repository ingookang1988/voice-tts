from __future__ import annotations

import os
from pathlib import Path

import pytest
import soundfile as sf
from typer.testing import CliRunner

from voice_tts.cli import app


runner = CliRunner()


@pytest.mark.external
def test_external_synthesize_smoke(tmp_path: Path) -> None:
    required_env = {
        "VOICE_TTS_GPT_SOVITS_ROOT": os.getenv("VOICE_TTS_GPT_SOVITS_ROOT"),
        "VOICE_TTS_MODEL_MANIFEST": os.getenv("VOICE_TTS_MODEL_MANIFEST"),
        "VOICE_TTS_EXTERNAL_REF_AUDIO": os.getenv("VOICE_TTS_EXTERNAL_REF_AUDIO"),
    }
    missing = [name for name, value in required_env.items() if not value]
    if missing:
        pytest.skip(f"external smoke is not configured: missing {', '.join(missing)}")

    model_profile = os.getenv("VOICE_TTS_EXTERNAL_MODEL_PROFILE", "gsv2-default")
    text = os.getenv("VOICE_TTS_EXTERNAL_TEXT", "안녕하세요")
    text_lang = os.getenv("VOICE_TTS_EXTERNAL_TEXT_LANG", "ko")
    prompt_text = os.getenv("VOICE_TTS_EXTERNAL_PROMPT_TEXT", "안녕하세요, 반갑습니다.")
    prompt_lang = os.getenv("VOICE_TTS_EXTERNAL_PROMPT_LANG", "ko")
    output_path = tmp_path / "external-smoke.wav"

    result = runner.invoke(
        app,
        [
            "synthesize",
            "--model-profile",
            model_profile,
            "--text",
            text,
            "--text-lang",
            text_lang,
            "--ref-audio",
            required_env["VOICE_TTS_EXTERNAL_REF_AUDIO"],
            "--prompt-text",
            prompt_text,
            "--prompt-lang",
            prompt_lang,
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert output_path.exists()
    audio_data, sample_rate = sf.read(str(output_path))
    assert sample_rate > 0
    assert len(audio_data) > 0
