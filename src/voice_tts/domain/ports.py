from __future__ import annotations

from typing import Protocol

from voice_tts.domain.entities import ModelWeights, SynthesisRequest, SynthesisResult


class SpeechSynthesisEngine(Protocol):
    def synthesize(
        self,
        request: SynthesisRequest,
        weights: ModelWeights,
    ) -> SynthesisResult:
        """Run speech synthesis with the resolved model weights."""


class WeightRepository(Protocol):
    def get_by_speaker_id(self, speaker_id: str) -> ModelWeights:
        """Resolve model weights for a speaker identifier."""

