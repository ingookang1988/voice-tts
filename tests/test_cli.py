from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

from typer.testing import CliRunner

from voice_tts.application.dto import (
    PrepareReferenceAudioResultDto,
    ReferenceClipCandidateDto,
    SynthesizeSpeechResultDto,
)
from voice_tts.cli import app
from voice_tts.domain.entities import ModelProfile
from voice_tts.exceptions import ModelProfileNotFoundError


runner = CliRunner()


def _reset_fake_upstream_modules() -> None:
    for module_name in (
        "GPT_SoVITS",
        "GPT_SoVITS.TTS_infer_pack",
        "GPT_SoVITS.TTS_infer_pack.TTS",
    ):
        sys.modules.pop(module_name, None)


def _write_fake_checkout(root: Path, *, invalid_tts_module: bool = False) -> None:
    package_root = root / "GPT_SoVITS" / "TTS_infer_pack"
    package_root.mkdir(parents=True, exist_ok=True)
    (root / "GPT_SoVITS" / "__init__.py").write_text("", encoding="utf-8")
    (package_root / "__init__.py").write_text("", encoding="utf-8")
    module_body = "def broken(:\n" if invalid_tts_module else "\n".join(
        [
            "class TTS_Config:",
            "    def __init__(self, config_path: str) -> None:",
            "        self.config_path = config_path",
            "",
            "class TTS:",
            "    def __init__(self, config: TTS_Config) -> None:",
            "        self.config = config",
            "",
            "    def run(self, payload):",
            "        return iter([(24000, [0, 0, 0])])",
        ]
    )
    (package_root / "TTS.py").write_text(module_body, encoding="utf-8")
    _reset_fake_upstream_modules()


def _write_manifest(
    manifest_path: Path,
    tts_config_path: Path,
    *,
    legacy: bool = False,
    supported_devices: list[str] | None = None,
    required_checkout_files: list[str] | None = None,
) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    profile: dict[str, object] = {
        "id": "gsv2-default",
        "version": "gpt-sovits-v2",
        "tts_config_path": str(tts_config_path),
    }
    if not legacy:
        profile.update(
            {
                "display_name": "Korean Zero-Shot",
                "languages": ["ko", "en"],
                "speaker_tags": ["female"],
                "notes": "phase3 test profile",
                "compatibility": {
                    "required_checkout_files": required_checkout_files
                    or ["GPT_SoVITS/TTS_infer_pack/TTS.py"],
                    "supported_devices": supported_devices or ["auto", "cpu"],
                },
            }
        )
    manifest_path.write_text(json.dumps({"profiles": [profile]}), encoding="utf-8")


def _combined_output(result) -> str:
    return f"{result.stdout}{getattr(result, 'stderr', '')}"


class _FakeUseCase:
    def __init__(self, result: SynthesizeSpeechResultDto | None = None, error: Exception | None = None) -> None:
        self.result = result or SynthesizeSpeechResultDto(
            audio_path="D:/Project/voice-tts/.local/outputs/gsv2-default/sample.wav",
            sample_rate=32000,
            metadata={
                "engine": "gpt-sovits-v2",
                "model_profile_id": "gsv2-default",
                "profile_display_name": "Korean Zero-Shot",
                "resolved_tts_config_path": "D:/GPT-SoVITS/GPT_SoVITS/configs/tts_infer.yaml",
                "input_ref_audio_path": "D:/clips/sample.wav",
                "resolved_ref_audio_path": "D:/clips/sample.wav",
                "trim_applied": "false",
                "elapsed_ms": "1234",
                "device": "cpu",
                "use_fp16": "false",
            },
        )
        self.error = error
        self.commands = []

    def execute(self, command):
        self.commands.append(command)
        if self.error is not None:
            raise self.error
        return self.result


class _FakePrepareReferenceUseCase:
    def __init__(
        self,
        result: PrepareReferenceAudioResultDto | None = None,
        error: Exception | None = None,
    ) -> None:
        self.result = result or PrepareReferenceAudioResultDto(
            source_path="D:/clips/source.wav",
            duration_sec=12.5,
            sample_rate=48000,
            channels=1,
            format_name="pcm_s16le",
            container_name="wav",
            candidates=(),
            exported_clip_path=None,
            selected_candidate=None,
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
    assert "voice-tts 0.4.0" in result.stdout


def test_init_creates_env_and_seed_manifest(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env.example").write_text(
        "\n".join(
            [
                "VOICE_TTS_ENV=local",
                "VOICE_TTS_LOG_LEVEL=INFO",
                "VOICE_TTS_WORKDIR=.local",
                "VOICE_TTS_GPT_SOVITS_ROOT=",
                "VOICE_TTS_MODEL_MANIFEST=.local/model-profiles.json",
                "VOICE_TTS_TEMP_ROOT=.local/tmp",
                "VOICE_TTS_OUTPUT_ROOT=.local/outputs",
                "VOICE_TTS_DEFAULT_DEVICE=auto",
                "VOICE_TTS_USE_FP16=true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    gpt_root = tmp_path / "fake-gpt"
    gpt_root.mkdir()

    result = runner.invoke(app, ["init", "--gpt-sovits-root", str(gpt_root)])

    assert result.exit_code == 0
    assert "voice-tts init" in result.stdout
    assert "seeded_profile: gsv2-default" in result.stdout
    assert (tmp_path / ".env").exists()
    manifest_path = tmp_path / ".local" / "model-profiles.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert payload["profiles"][0]["id"] == "gsv2-default"
    assert payload["profiles"][0]["tts_config_path"] == str(
        (gpt_root / "GPT_SoVITS" / "configs" / "tts_infer.yaml").resolve()
    )


def test_init_fails_without_force_when_env_exists(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env.example").write_text("VOICE_TTS_GPT_SOVITS_ROOT=\n", encoding="utf-8")
    (tmp_path / ".env").write_text("VOICE_TTS_ENV=local\n", encoding="utf-8")
    gpt_root = tmp_path / "fake-gpt"
    gpt_root.mkdir()

    result = runner.invoke(app, ["init", "--gpt-sovits-root", str(gpt_root)])

    assert result.exit_code == 1
    assert ".env already exists; pass --force to overwrite" in _combined_output(result)


def test_doctor_passes_with_valid_phase3_configuration(monkeypatch, tmp_path: Path) -> None:
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
    _write_fake_checkout(gpt_root)
    _write_manifest(manifest_path, tts_config_path)

    monkeypatch.setenv("VOICE_TTS_ENV", "local")
    monkeypatch.setenv("VOICE_TTS_LOG_LEVEL", "INFO")
    monkeypatch.setenv("VOICE_TTS_WORKDIR", str(workdir))
    monkeypatch.setenv("VOICE_TTS_TEMP_ROOT", str(temp_root))
    monkeypatch.setenv("VOICE_TTS_OUTPUT_ROOT", str(output_root))
    monkeypatch.setenv("VOICE_TTS_GPT_SOVITS_ROOT", str(gpt_root))
    monkeypatch.setenv("VOICE_TTS_MODEL_MANIFEST", str(manifest_path))
    monkeypatch.setenv("VOICE_TTS_DEFAULT_DEVICE", "cpu")
    monkeypatch.setattr(
        "voice_tts.bootstrap.doctor.find_ffmpeg_executable",
        lambda: Path("C:/ffmpeg/bin/ffmpeg.exe"),
    )

    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "doctor passed" in result.stdout
    assert "[PASS] model_manifest" in result.stdout
    assert "[PASS] profile:gsv2-default" in result.stdout


def test_doctor_warns_for_legacy_manifest_defaults(monkeypatch, tmp_path: Path) -> None:
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
    _write_fake_checkout(gpt_root)
    _write_manifest(manifest_path, tts_config_path, legacy=True)

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
    assert "[WARN] profile:gsv2-default" in result.stdout
    assert "legacy defaults applied for display_name" in result.stdout


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


def test_doctor_fails_when_required_checkout_file_is_missing(monkeypatch, tmp_path: Path) -> None:
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
    _write_fake_checkout(gpt_root)
    _write_manifest(
        manifest_path,
        tts_config_path,
        required_checkout_files=["GPT_SoVITS/TTS_infer_pack/Missing.py"],
    )

    monkeypatch.setenv("VOICE_TTS_WORKDIR", str(workdir))
    monkeypatch.setenv("VOICE_TTS_TEMP_ROOT", str(temp_root))
    monkeypatch.setenv("VOICE_TTS_OUTPUT_ROOT", str(output_root))
    monkeypatch.setenv("VOICE_TTS_GPT_SOVITS_ROOT", str(gpt_root))
    monkeypatch.setenv("VOICE_TTS_MODEL_MANIFEST", str(manifest_path))
    monkeypatch.setenv("VOICE_TTS_DEFAULT_DEVICE", "cpu")
    monkeypatch.setattr(
        "voice_tts.bootstrap.doctor.find_ffmpeg_executable",
        lambda: Path("C:/ffmpeg/bin/ffmpeg.exe"),
    )

    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 1
    assert "[FAIL] profile:gsv2-default" in result.stdout
    assert "missing checkout files:" in result.stdout


def test_doctor_fails_when_upstream_import_breaks(monkeypatch, tmp_path: Path) -> None:
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
    _write_fake_checkout(gpt_root, invalid_tts_module=True)
    _write_manifest(manifest_path, tts_config_path)

    monkeypatch.setenv("VOICE_TTS_WORKDIR", str(workdir))
    monkeypatch.setenv("VOICE_TTS_TEMP_ROOT", str(temp_root))
    monkeypatch.setenv("VOICE_TTS_OUTPUT_ROOT", str(output_root))
    monkeypatch.setenv("VOICE_TTS_GPT_SOVITS_ROOT", str(gpt_root))
    monkeypatch.setenv("VOICE_TTS_MODEL_MANIFEST", str(manifest_path))
    monkeypatch.setenv("VOICE_TTS_DEFAULT_DEVICE", "cpu")
    monkeypatch.setattr(
        "voice_tts.bootstrap.doctor.find_ffmpeg_executable",
        lambda: Path("C:/ffmpeg/bin/ffmpeg.exe"),
    )

    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 1
    assert "[FAIL] profile:gsv2-default" in result.stdout
    assert "upstream import failed:" in result.stdout


def test_profiles_prints_profile_discovery_details(monkeypatch, tmp_path: Path) -> None:
    config_path = tmp_path / "tts_infer.yaml"
    config_path.write_text("custom: {}\n", encoding="utf-8")
    profile = ModelProfile(
        id="gsv2-default",
        display_name="Korean Zero-Shot",
        version="gpt-sovits-v2",
        tts_config_path=config_path,
        languages=("ko", "en"),
        speaker_tags=("female", "studio"),
        normalization_warnings=("legacy defaults applied for notes",),
    )
    fake_repository = SimpleNamespace(list_profiles=lambda: (profile,))
    monkeypatch.setattr(
        "voice_tts.cli.build_container",
        lambda: SimpleNamespace(model_profile_repository=fake_repository),
    )

    result = runner.invoke(app, ["profiles"])

    assert result.exit_code == 0
    assert "voice-tts profiles" in result.stdout
    assert "- gsv2-default: Korean Zero-Shot" in result.stdout
    assert "languages: ko, en" in result.stdout
    assert "speaker_tags: female, studio" in result.stdout
    assert "supported_devices: auto, cpu, cuda" in result.stdout
    assert f"config_path: {config_path} (present)" in result.stdout
    assert "legacy defaults applied for notes" in result.stdout


def test_prepare_ref_prints_ranked_candidates(monkeypatch, tmp_path: Path) -> None:
    fake_use_case = _FakePrepareReferenceUseCase(
        result=PrepareReferenceAudioResultDto(
            source_path=str(tmp_path / "source.wav"),
            duration_sec=18.2,
            sample_rate=44100,
            channels=1,
            format_name="pcm_s16le",
            container_name="wav",
            candidates=(
                ReferenceClipCandidateDto(index=1, start_sec=0.5, end_sec=6.2, duration_sec=5.7),
                ReferenceClipCandidateDto(index=2, start_sec=7.0, end_sec=13.1, duration_sec=6.1),
            ),
            exported_clip_path=None,
            selected_candidate=None,
        )
    )
    monkeypatch.setattr(
        "voice_tts.cli.build_container",
        lambda: SimpleNamespace(prepare_reference_audio=fake_use_case),
    )
    source_audio = tmp_path / "source.wav"
    source_audio.write_bytes(b"RIFF")

    result = runner.invoke(app, ["prepare-ref", "--input", str(source_audio)])

    assert result.exit_code == 0
    assert "voice-tts prepare-ref" in result.stdout
    assert "duration_sec: 18.200" in result.stdout
    assert "candidate_segments:" in result.stdout
    assert "1. 0.500 -> 6.200 (5.700s)" in result.stdout
    assert fake_use_case.commands[0].input_path == source_audio


def test_prepare_ref_prints_exported_clip(monkeypatch, tmp_path: Path) -> None:
    fake_use_case = _FakePrepareReferenceUseCase(
        result=PrepareReferenceAudioResultDto(
            source_path=str(tmp_path / "source.wav"),
            duration_sec=10.0,
            sample_rate=48000,
            channels=2,
            format_name="pcm_s16le",
            container_name="wav",
            candidates=(
                ReferenceClipCandidateDto(index=1, start_sec=1.0, end_sec=7.0, duration_sec=6.0),
            ),
            exported_clip_path=str(tmp_path / "prepared.wav"),
            selected_candidate=ReferenceClipCandidateDto(index=1, start_sec=1.0, end_sec=7.0, duration_sec=6.0),
        )
    )
    monkeypatch.setattr(
        "voice_tts.cli.build_container",
        lambda: SimpleNamespace(prepare_reference_audio=fake_use_case),
    )
    source_audio = tmp_path / "source.wav"
    source_audio.write_bytes(b"RIFF")

    result = runner.invoke(
        app,
        ["prepare-ref", "--input", str(source_audio), "--pick", "1"],
    )

    assert result.exit_code == 0
    assert f"prepared_ref_audio: {tmp_path / 'prepared.wav'}" in result.stdout
    assert "selected_range: 1.000 -> 7.000 (6.000s)" in result.stdout


def test_synthesize_requires_named_flags() -> None:
    result = runner.invoke(app, ["synthesize"])
    assert result.exit_code != 0
    assert "Missing option '--model-profile'" in _combined_output(result)


def test_synthesize_prints_generated_output(monkeypatch, tmp_path: Path) -> None:
    fake_use_case = _FakeUseCase(
        result=SynthesizeSpeechResultDto(
            audio_path=str(tmp_path / "generated.wav"),
            sample_rate=32000,
            metadata={
                "engine": "gpt-sovits-v2",
                "model_profile_id": "gsv2-default",
                "profile_display_name": "Korean Zero-Shot",
                "resolved_tts_config_path": "D:/GPT-SoVITS/GPT_SoVITS/configs/tts_infer.yaml",
                "input_ref_audio_path": str(tmp_path / "ref.wav"),
                "resolved_ref_audio_path": str(tmp_path / "ref-trim.wav"),
                "trim_applied": "true",
                "elapsed_ms": "987",
                "device": "cpu",
                "use_fp16": "false",
            },
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
    assert "profile: gsv2-default (Korean Zero-Shot)" in result.stdout
    assert "config_path: D:/GPT-SoVITS/GPT_SoVITS/configs/tts_infer.yaml" in result.stdout
    assert "resolved_ref_audio:" in result.stdout
    assert "trim_applied: true" in result.stdout
    assert "elapsed_ms: 987" in result.stdout
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
    assert "[preflight] ref_end_sec must be greater than ref_start_sec" in _combined_output(result)


def test_synthesize_fails_for_unknown_profile(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        "voice_tts.cli.build_container",
        lambda: SimpleNamespace(
            synthesize_speech=_FakeUseCase(
                error=ModelProfileNotFoundError(
                    "[manifest] model profile 'missing' was not found in D:/Project/voice-tts/.local/model-profiles.json"
                )
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
    assert "[manifest] model profile 'missing' was not found" in _combined_output(result)
