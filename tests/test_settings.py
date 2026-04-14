from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from voice_tts.infrastructure.config import Settings


def test_settings_load_defaults(monkeypatch) -> None:
    monkeypatch.delenv("VOICE_TTS_ENV", raising=False)
    monkeypatch.delenv("VOICE_TTS_LOG_LEVEL", raising=False)
    monkeypatch.delenv("VOICE_TTS_WORKDIR", raising=False)
    monkeypatch.delenv("VOICE_TTS_GPT_SOVITS_ROOT", raising=False)
    monkeypatch.delenv("VOICE_TTS_MODEL_MANIFEST", raising=False)
    monkeypatch.delenv("VOICE_TTS_TEMP_ROOT", raising=False)
    monkeypatch.delenv("VOICE_TTS_OUTPUT_ROOT", raising=False)
    monkeypatch.delenv("VOICE_TTS_DEFAULT_DEVICE", raising=False)
    monkeypatch.delenv("VOICE_TTS_USE_FP16", raising=False)

    settings = Settings()
    assert settings.env == "local"
    assert settings.log_level == "INFO"
    assert settings.default_device == "auto"
    assert settings.gpt_sovits_root is None
    assert settings.model_manifest == Path(".local/model-profiles.json")
    assert settings.output_root == Path(".local/outputs")
    assert settings.use_fp16 is True


def test_settings_allow_env_override(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("VOICE_TTS_ENV", "test")
    monkeypatch.setenv("VOICE_TTS_LOG_LEVEL", "debug")
    monkeypatch.setenv("VOICE_TTS_WORKDIR", str(tmp_path / "work"))
    monkeypatch.setenv("VOICE_TTS_MODEL_MANIFEST", str(tmp_path / "manifest.json"))
    monkeypatch.setenv("VOICE_TTS_TEMP_ROOT", str(tmp_path / "tmp"))
    monkeypatch.setenv("VOICE_TTS_OUTPUT_ROOT", str(tmp_path / "outputs"))
    monkeypatch.setenv("VOICE_TTS_DEFAULT_DEVICE", "CUDA")
    monkeypatch.setenv("VOICE_TTS_USE_FP16", "false")

    settings = Settings()
    assert settings.env == "test"
    assert settings.log_level == "DEBUG"
    assert settings.model_manifest == tmp_path / "manifest.json"
    assert settings.output_root == tmp_path / "outputs"
    assert settings.default_device == "cuda"
    assert settings.use_fp16 is False


def test_settings_reject_invalid_device(monkeypatch) -> None:
    monkeypatch.setenv("VOICE_TTS_DEFAULT_DEVICE", "tpu")
    with pytest.raises(ValidationError):
        Settings()
