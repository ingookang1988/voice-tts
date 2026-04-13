from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from voice_tts.cli import app


runner = CliRunner()


def test_version_command_prints_project_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "voice-tts 0.1.0" in result.stdout


def test_doctor_passes_with_valid_local_configuration(monkeypatch, tmp_path: Path) -> None:
    workdir = tmp_path / "workdir"
    temp_root = tmp_path / "temp"
    gpt_root = tmp_path / "gpt"
    weights_root = tmp_path / "weights"
    workdir.mkdir()
    temp_root.mkdir()
    gpt_root.mkdir()
    weights_root.mkdir()

    monkeypatch.setenv("VOICE_TTS_ENV", "local")
    monkeypatch.setenv("VOICE_TTS_LOG_LEVEL", "INFO")
    monkeypatch.setenv("VOICE_TTS_WORKDIR", str(workdir))
    monkeypatch.setenv("VOICE_TTS_TEMP_ROOT", str(temp_root))
    monkeypatch.setenv("VOICE_TTS_GPT_SOVITS_ROOT", str(gpt_root))
    monkeypatch.setenv("VOICE_TTS_WEIGHTS_ROOT", str(weights_root))
    monkeypatch.setenv("VOICE_TTS_DEFAULT_DEVICE", "auto")

    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "doctor passed" in result.stdout
    assert "[PASS] weights_root" in result.stdout


def test_doctor_fails_when_configured_weights_root_is_missing(
    monkeypatch,
    tmp_path: Path,
) -> None:
    workdir = tmp_path / "workdir"
    temp_root = tmp_path / "temp"
    gpt_root = tmp_path / "gpt"
    workdir.mkdir()
    temp_root.mkdir()
    gpt_root.mkdir()

    monkeypatch.setenv("VOICE_TTS_WORKDIR", str(workdir))
    monkeypatch.setenv("VOICE_TTS_TEMP_ROOT", str(temp_root))
    monkeypatch.setenv("VOICE_TTS_GPT_SOVITS_ROOT", str(gpt_root))
    monkeypatch.setenv("VOICE_TTS_WEIGHTS_ROOT", str(tmp_path / "missing-weights"))

    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 1
    assert "[FAIL] weights_root" in result.stdout
    assert "doctor failed" in result.stdout

