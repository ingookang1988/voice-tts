from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from voice_tts.application.dto import SynthesizeSpeechCommand, SynthesizeSpeechResultDto
from voice_tts.domain.ports import ModelProfileRepository, SpeechSynthesisEngine


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
