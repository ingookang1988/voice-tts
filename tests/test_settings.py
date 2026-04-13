from __future__ import annotations

import pytest
from pydantic import ValidationError

from voice_tts.infrastructure.config import Settings


def test_settings_load_defaults(monkeypatch) -> None:
    monkeypatch.delenv("VOICE_TTS_ENV", raising=False)
    monkeypatch.delenv("VOICE_TTS_LOG_LEVEL", raising=False)
    monkeypatch.delenv("VOICE_TTS_WORKDIR", raising=False)
    monkeypatch.delenv("VOICE_TTS_GPT_SOVITS_ROOT", raising=False)
    monkeypatch.delenv("VOICE_TTS_WEIGHTS_ROOT", raising=False)
    monkeypatch.delenv("VOICE_TTS_TEMP_ROOT", raising=False)
    monkeypatch.delenv("VOICE_TTS_DEFAULT_DEVICE", raising=False)
    monkeypatch.delenv("VOICE_TTS_USE_FP16", raising=False)

    settings = Settings()
    assert settings.env == "local"
    assert settings.log_level == "INFO"
    assert settings.default_device == "auto"
    assert settings.gpt_sovits_root is None
    assert settings.weights_root is None
    assert settings.use_fp16 is True


def test_settings_allow_env_override(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("VOICE_TTS_ENV", "test")
    monkeypatch.setenv("VOICE_TTS_LOG_LEVEL", "debug")
    monkeypatch.setenv("VOICE_TTS_WORKDIR", str(tmp_path / "work"))
    monkeypatch.setenv("VOICE_TTS_TEMP_ROOT", str(tmp_path / "tmp"))
    monkeypatch.setenv("VOICE_TTS_DEFAULT_DEVICE", "CUDA")
    monkeypatch.setenv("VOICE_TTS_USE_FP16", "false")

    settings = Settings()
    assert settings.env == "test"
    assert settings.log_level == "DEBUG"
    assert settings.default_device == "cuda"
    assert settings.use_fp16 is False


def test_settings_reject_invalid_device(monkeypatch) -> None:
    monkeypatch.setenv("VOICE_TTS_DEFAULT_DEVICE", "tpu")
    with pytest.raises(ValidationError):
        Settings()

