from __future__ import annotations

from dataclasses import dataclass

from voice_tts.application.dto import SynthesizeSpeechCommand, SynthesizeSpeechResultDto
from voice_tts.domain.ports import SpeechSynthesisEngine, WeightRepository


@dataclass(slots=True)
class SynthesizeSpeechUseCase:
    weight_repository: WeightRepository
    engine: SpeechSynthesisEngine

    def execute(self, command: SynthesizeSpeechCommand) -> SynthesizeSpeechResultDto:
        request = command.to_domain()
        weights = self.weight_repository.get_by_speaker_id(request.speaker_id)
        result = self.engine.synthesize(request, weights)
        return SynthesizeSpeechResultDto.from_domain(result)

