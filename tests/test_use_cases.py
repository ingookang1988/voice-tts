from __future__ import annotations

from pathlib import Path

import pytest

from voice_tts.application.dto import PrepareReferenceAudioCommand, SynthesizeSpeechCommand
from voice_tts.application.use_cases import PrepareReferenceAudioUseCase, SynthesizeSpeechUseCase
from voice_tts.domain.entities import AudioSourceMetadata, ModelProfile, ReferenceClipCandidate, SynthesisResult
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


class _FakeReferenceAudioService:
    def __init__(self) -> None:
        self.inspect_calls: list[Path] = []
        self.suggest_calls: list[Path] = []
        self.export_calls: list[tuple[Path, Path, ReferenceClipCandidate]] = []
        self.metadata = AudioSourceMetadata(
            duration_sec=18.0,
            sample_rate=44100,
            channels=1,
            format_name="pcm_s16le",
            container_name="wav",
        )
        self.candidates = (
            ReferenceClipCandidate(start_sec=0.5, end_sec=6.2),
            ReferenceClipCandidate(start_sec=7.0, end_sec=13.1),
        )

    def inspect(self, input_path: Path) -> AudioSourceMetadata:
        self.inspect_calls.append(input_path)
        return self.metadata

    def suggest_segments(self, input_path: Path, metadata: AudioSourceMetadata) -> tuple[ReferenceClipCandidate, ...]:
        self.suggest_calls.append(input_path)
        return self.candidates

    def export_segment(
        self,
        input_path: Path,
        output_path: Path,
        segment: ReferenceClipCandidate,
    ) -> Path:
        self.export_calls.append((input_path, output_path, segment))
        return output_path


def _make_profile(tmp_path: Path) -> ModelProfile:
    config_path = tmp_path / "tts_infer.yaml"
    config_path.write_text("custom: {}\n", encoding="utf-8")
    return ModelProfile(
        id="gsv2-default",
        display_name="Korean Zero-Shot",
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

    with pytest.raises(VoiceTtsUsageError, match="\\[preflight\\] output file already exists"):
        command.resolve_output_path(tmp_path / "outputs")


def test_command_allows_existing_output_with_force(tmp_path: Path) -> None:
    existing_output = tmp_path / "outputs" / "existing.wav"
    existing_output.parent.mkdir(parents=True)
    existing_output.write_bytes(b"stub")
    command = _make_command(tmp_path, output_path=existing_output, force=True)

    assert command.resolve_output_path(tmp_path / "outputs") == existing_output


def test_command_rejects_invalid_trim_range(tmp_path: Path) -> None:
    with pytest.raises(VoiceTtsUsageError, match="\\[preflight\\] ref_end_sec must be greater than ref_start_sec"):
        _make_command(tmp_path, ref_start_sec=3.0, ref_end_sec=2.0)


def test_prepare_reference_use_case_generates_default_output_path(tmp_path: Path) -> None:
    service = _FakeReferenceAudioService()
    use_case = PrepareReferenceAudioUseCase(
        reference_audio_service=service,
        temp_root=tmp_path / "tmp",
    )
    source_audio = tmp_path / "source.wav"
    source_audio.write_bytes(b"RIFF")

    result = use_case.execute(
        PrepareReferenceAudioCommand(
            input_path=source_audio,
            pick=1,
        )
    )

    assert service.inspect_calls == [source_audio]
    assert service.suggest_calls == [source_audio]
    assert len(service.export_calls) == 1
    _, output_path, segment = service.export_calls[0]
    assert output_path.parent == tmp_path / "tmp" / "ref-clips"
    assert output_path.suffix == ".wav"
    assert segment.start_sec == 0.5
    assert result.exported_clip_path == str(output_path)


def test_prepare_reference_command_rejects_invalid_pick() -> None:
    with pytest.raises(VoiceTtsUsageError, match="\\[preflight\\] pick must be a positive 1-based index"):
        PrepareReferenceAudioCommand(input_path=Path("source.wav"), pick=0)


def test_prepare_reference_command_rejects_partial_trim_range() -> None:
    with pytest.raises(VoiceTtsUsageError, match="\\[preflight\\] start_sec and end_sec must be provided together"):
        PrepareReferenceAudioCommand(input_path=Path("source.wav"), start_sec=1.0)


def test_prepare_reference_use_case_rejects_out_of_range_pick(tmp_path: Path) -> None:
    service = _FakeReferenceAudioService()
    use_case = PrepareReferenceAudioUseCase(
        reference_audio_service=service,
        temp_root=tmp_path / "tmp",
    )
    source_audio = tmp_path / "source.wav"
    source_audio.write_bytes(b"RIFF")

    with pytest.raises(
        VoiceTtsUsageError,
        match="\\[preflight\\] pick must be between 1 and 2 for the current analysis result",
    ):
        use_case.execute(
            PrepareReferenceAudioCommand(
                input_path=source_audio,
                pick=3,
            )
        )
