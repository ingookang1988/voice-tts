from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from voice_tts.application.dto import (
    PrepareReferenceAudioCommand,
    PrepareReferenceAudioResultDto,
    SynthesizeSpeechCommand,
    SynthesizeSpeechResultDto,
)
from voice_tts.domain.entities import ReferenceAudioPreparationResult, ReferenceClipCandidate
from voice_tts.domain.ports import (
    ModelProfileRepository,
    ReferenceAudioPreparationService,
    SpeechSynthesisEngine,
)
from voice_tts.exceptions import VoiceTtsUsageError, with_stage


@dataclass(slots=True)
class SynthesizeSpeechUseCase:
    model_profile_repository: ModelProfileRepository
    engine: SpeechSynthesisEngine
    output_root: Path

    def execute(self, command: SynthesizeSpeechCommand) -> SynthesizeSpeechResultDto:
        output_path = command.resolve_output_path(self.output_root)
        request = command.to_domain(output_path)
        model_profile = self.model_profile_repository.get_by_id(request.model_profile_id)
        result = self.engine.synthesize(request, model_profile)
        return SynthesizeSpeechResultDto.from_domain(result)


@dataclass(slots=True)
class PrepareReferenceAudioUseCase:
    reference_audio_service: ReferenceAudioPreparationService
    temp_root: Path

    def execute(self, command: PrepareReferenceAudioCommand) -> PrepareReferenceAudioResultDto:
        metadata = self.reference_audio_service.inspect(command.input_path)
        candidates = (
            self.reference_audio_service.suggest_segments(command.input_path, metadata)
            if not command.has_explicit_range
            else ()
        )

        exported_clip_path: Path | None = None
        selected_candidate: ReferenceClipCandidate | None = None

        if command.has_explicit_range:
            selected_candidate = ReferenceClipCandidate(
                start_sec=command.start_sec or 0.0,
                end_sec=command.end_sec or 0.0,
            )
            output_path = command.resolve_output_path(self.temp_root, selected_candidate)
            exported_clip_path = self.reference_audio_service.export_segment(
                input_path=command.input_path,
                output_path=output_path,
                segment=selected_candidate,
            )
        elif command.pick is not None:
            if not candidates:
                raise VoiceTtsUsageError(
                    with_stage("preflight", "no ranked candidate segments are available to export")
                )
            candidate_index = command.pick - 1
            if candidate_index < 0 or candidate_index >= len(candidates):
                raise VoiceTtsUsageError(
                    with_stage(
                        "preflight",
                        f"pick must be between 1 and {len(candidates)} for the current analysis result",
                    )
                )
            selected_candidate = candidates[candidate_index]
            output_path = command.resolve_output_path(self.temp_root, selected_candidate)
            exported_clip_path = self.reference_audio_service.export_segment(
                input_path=command.input_path,
                output_path=output_path,
                segment=selected_candidate,
            )

        return PrepareReferenceAudioResultDto.from_domain(
            ReferenceAudioPreparationResult(
                source_path=command.input_path,
                source_metadata=metadata,
                candidates=candidates,
                exported_clip_path=exported_clip_path,
                selected_candidate=selected_candidate,
            )
        )
