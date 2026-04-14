from __future__ import annotations

from pathlib import Path

import pytest

from voice_tts.application.dto import SynthesizeSpeechCommand
from voice_tts.application.use_cases import SynthesizeSpeechUseCase
from voice_tts.domain.entities import ModelProfile, SynthesisResult
from voice_tts.exceptions import VoiceTtsUsageError


class _FakeRepository:
    def __init__(self, profile: ModelProfile) -> None:
        self.profile = profile
        self.requested_ids: list[str] = []

    def get_by_id(self, model_profile_id: str) -> ModelProfile:
        self.requested_ids.append(model_profile_id)
        return self.profile

    def list_profiles(self) -> tuple[ModelProfile, ...]:
        return (self.profile,)


class _FakeEngine:
    def __init__(self) -> None:
        self.requests = []
        self.model_profiles = []

    def synthesize(self, request, model_profile) -> SynthesisResult:
        self.requests.append(request)
        self.model_profiles.append(model_profile)
        return SynthesisResult(
            audio_path=request.output_path,
            sample_rate=32000,
            metadata={"engine": "fake"},
        )


def _make_profile(tmp_path: Path) -> ModelProfile:
    config_path = tmp_path / "tts_infer.yaml"
    config_path.write_text("custom: {}\n", encoding="utf-8")
    return ModelProfile(
        id="gsv2-default",
        version="gpt-sovits-v2",
        tts_config_path=config_path,
    )


def _make_command(tmp_path: Path, **overrides) -> SynthesizeSpeechCommand:
    ref_audio = tmp_path / "reference.wav"
    ref_audio.write_bytes(b"RIFF")
    payload = {
        "model_profile_id": "gsv2-default",
        "text": "안녕하세요",
        "text_lang": "ko",
        "ref_audio_path": ref_audio,
        "prompt_text": "안녕하세요, 반갑습니다.",
        "prompt_lang": "ko",
    }
    payload.update(overrides)
    return SynthesizeSpeechCommand(**payload)


def test_use_case_generates_auto_output_path_under_output_root(tmp_path: Path) -> None:
    profile = _make_profile(tmp_path)
    repository = _FakeRepository(profile)
    engine = _FakeEngine()
    use_case = SynthesizeSpeechUseCase(
        model_profile_repository=repository,
        engine=engine,
        output_root=tmp_path / "outputs",
    )

    result = use_case.execute(_make_command(tmp_path))

    assert repository.requested_ids == ["gsv2-default"]
    assert engine.requests[0].output_path.parent.parent == tmp_path / "outputs"
    assert Path(result.audio_path).suffix == ".wav"
    assert result.sample_rate == 32000


def test_command_rejects_existing_output_without_force(tmp_path: Path) -> None:
    existing_output = tmp_path / "outputs" / "existing.wav"
    existing_output.parent.mkdir(parents=True)
    existing_output.write_bytes(b"stub")
    command = _make_command(tmp_path, output_path=existing_output)

    with pytest.raises(VoiceTtsUsageError):
        command.resolve_output_path(tmp_path / "outputs")


def test_command_allows_existing_output_with_force(tmp_path: Path) -> None:
    existing_output = tmp_path / "outputs" / "existing.wav"
    existing_output.parent.mkdir(parents=True)
    existing_output.write_bytes(b"stub")
    command = _make_command(tmp_path, output_path=existing_output, force=True)

    assert command.resolve_output_path(tmp_path / "outputs") == existing_output


def test_command_rejects_invalid_trim_range(tmp_path: Path) -> None:
    with pytest.raises(VoiceTtsUsageError):
        _make_command(tmp_path, ref_start_sec=3.0, ref_end_sec=2.0)
