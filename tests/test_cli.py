from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from voice_tts.application.dto import SynthesizeSpeechResultDto
from voice_tts.cli import app
from voice_tts.exceptions import ModelProfileNotFoundError


runner = CliRunner()


def _write_manifest(manifest_path: Path, tts_config_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "profiles": [
                    {
                        "id": "gsv2-default",
                        "version": "gpt-sovits-v2",
                        "tts_config_path": str(tts_config_path),
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def _combined_output(result) -> str:
    return f"{result.stdout}{getattr(result, 'stderr', '')}"


class _FakeUseCase:
    def __init__(self, result: SynthesizeSpeechResultDto | None = None, error: Exception | None = None) -> None:
        self.result = result or SynthesizeSpeechResultDto(
            audio_path="D:/Project/voice-tts/.local/outputs/gsv2-default/sample.wav",
            sample_rate=32000,
        )
        self.error = error
        self.commands = []

    def execute(self, command):
        self.commands.append(command)
        if self.error is not None:
            raise self.error
        return self.result


def test_version_command_prints_project_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "voice-tts 0.2.0" in result.stdout


def test_doctor_passes_with_valid_phase2_configuration(monkeypatch, tmp_path: Path) -> None:
    workdir = tmp_path / "workdir"
    temp_root = tmp_path / "temp"
    output_root = tmp_path / "outputs"
    gpt_root = tmp_path / "gpt"
    config_root = tmp_path / "configs"
    manifest_path = tmp_path / "model-profiles.json"
    workdir.mkdir()
    temp_root.mkdir()
    output_root.mkdir()
    gpt_root.mkdir()
    config_root.mkdir()
    tts_config_path = config_root / "tts_infer.yaml"
    tts_config_path.write_text("custom: {}\n", encoding="utf-8")
    _write_manifest(manifest_path, tts_config_path)

    monkeypatch.setenv("VOICE_TTS_ENV", "local")
    monkeypatch.setenv("VOICE_TTS_LOG_LEVEL", "INFO")
    monkeypatch.setenv("VOICE_TTS_WORKDIR", str(workdir))
    monkeypatch.setenv("VOICE_TTS_TEMP_ROOT", str(temp_root))
    monkeypatch.setenv("VOICE_TTS_OUTPUT_ROOT", str(output_root))
    monkeypatch.setenv("VOICE_TTS_GPT_SOVITS_ROOT", str(gpt_root))
    monkeypatch.setenv("VOICE_TTS_MODEL_MANIFEST", str(manifest_path))
    monkeypatch.setenv("VOICE_TTS_DEFAULT_DEVICE", "auto")
    monkeypatch.setattr(
        "voice_tts.bootstrap.doctor.find_ffmpeg_executable",
        lambda: Path("C:/ffmpeg/bin/ffmpeg.exe"),
    )

    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "doctor passed" in result.stdout
    assert "[PASS] model_manifest" in result.stdout
    assert "[PASS] ffmpeg" in result.stdout


def test_doctor_fails_when_manifest_is_missing(monkeypatch, tmp_path: Path) -> None:
    workdir = tmp_path / "workdir"
    temp_root = tmp_path / "temp"
    output_root = tmp_path / "outputs"
    gpt_root = tmp_path / "gpt"
    workdir.mkdir()
    temp_root.mkdir()
    output_root.mkdir()
    gpt_root.mkdir()

    monkeypatch.setenv("VOICE_TTS_WORKDIR", str(workdir))
    monkeypatch.setenv("VOICE_TTS_TEMP_ROOT", str(temp_root))
    monkeypatch.setenv("VOICE_TTS_OUTPUT_ROOT", str(output_root))
    monkeypatch.setenv("VOICE_TTS_GPT_SOVITS_ROOT", str(gpt_root))
    monkeypatch.setenv("VOICE_TTS_MODEL_MANIFEST", str(tmp_path / "missing.json"))
    monkeypatch.setattr(
        "voice_tts.bootstrap.doctor.find_ffmpeg_executable",
        lambda: Path("C:/ffmpeg/bin/ffmpeg.exe"),
    )

    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 1
    assert "[FAIL] model_manifest" in result.stdout
    assert "doctor failed" in result.stdout


def test_synthesize_requires_named_flags() -> None:
    result = runner.invoke(app, ["synthesize"])
    assert result.exit_code != 0
    assert "Missing option '--model-profile'" in _combined_output(result)


def test_synthesize_prints_generated_output(monkeypatch, tmp_path: Path) -> None:
    fake_use_case = _FakeUseCase(
        result=SynthesizeSpeechResultDto(
            audio_path=str(tmp_path / "generated.wav"),
            sample_rate=32000,
        )
    )
    monkeypatch.setattr(
        "voice_tts.cli.build_container",
        lambda: SimpleNamespace(synthesize_speech=fake_use_case),
    )

    ref_audio = tmp_path / "ref.wav"
    ref_audio.write_bytes(b"RIFF")
    result = runner.invoke(
        app,
        [
            "synthesize",
            "--model-profile",
            "gsv2-default",
            "--text",
            "안녕하세요",
            "--text-lang",
            "ko",
            "--ref-audio",
            str(ref_audio),
            "--prompt-text",
            "안녕하세요, 반갑습니다.",
            "--prompt-lang",
            "ko",
        ],
    )
    assert result.exit_code == 0
    assert "generated wav:" in result.stdout
    assert "sample_rate: 32000" in result.stdout
    assert fake_use_case.commands[0].model_profile_id == "gsv2-default"


def test_synthesize_fails_for_invalid_trim_range(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        "voice_tts.cli.build_container",
        lambda: SimpleNamespace(synthesize_speech=_FakeUseCase()),
    )
    ref_audio = tmp_path / "ref.wav"
    ref_audio.write_bytes(b"RIFF")

    result = runner.invoke(
        app,
        [
            "synthesize",
            "--model-profile",
            "gsv2-default",
            "--text",
            "안녕하세요",
            "--text-lang",
            "ko",
            "--ref-audio",
            str(ref_audio),
            "--prompt-text",
            "안녕하세요, 반갑습니다.",
            "--prompt-lang",
            "ko",
            "--ref-start-sec",
            "4.0",
            "--ref-end-sec",
            "3.0",
        ],
    )
    assert result.exit_code == 1
    assert "ref_end_sec must be greater than ref_start_sec" in _combined_output(result)


def test_synthesize_fails_for_unknown_profile(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        "voice_tts.cli.build_container",
        lambda: SimpleNamespace(
            synthesize_speech=_FakeUseCase(
                error=ModelProfileNotFoundError("model profile 'missing' was not found")
            )
        ),
    )
    ref_audio = tmp_path / "ref.wav"
    ref_audio.write_bytes(b"RIFF")

    result = runner.invoke(
        app,
        [
            "synthesize",
            "--model-profile",
            "missing",
            "--text",
            "안녕하세요",
            "--text-lang",
            "ko",
            "--ref-audio",
            str(ref_audio),
            "--prompt-text",
            "안녕하세요, 반갑습니다.",
            "--prompt-lang",
            "ko",
        ],
    )
    assert result.exit_code == 1
    assert "model profile 'missing' was not found" in _combined_output(result)
