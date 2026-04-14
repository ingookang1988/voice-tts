from __future__ import annotations

from typing import Protocol

from voice_tts.domain.entities import ModelProfile, SynthesisRequest, SynthesisResult


class SpeechSynthesisEngine(Protocol):
    def synthesize(
        self,
        request: SynthesisRequest,
        model_profile: ModelProfile,
    ) -> SynthesisResult:
        """Run speech synthesis with the resolved model profile."""


class ModelProfileRepository(Protocol):
    def get_by_id(self, model_profile_id: str) -> ModelProfile:
        """Resolve a synthesis model profile by identifier."""

    def list_profiles(self) -> tuple[ModelProfile, ...]:
        """Return all manifest-backed model profiles."""
