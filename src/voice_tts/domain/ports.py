from __future__ import annotations

from typing import Protocol

from pathlib import Path

from voice_tts.domain.entities import (
    AudioSourceMetadata,
    ModelProfile,
    ReferenceClipCandidate,
    SynthesisRequest,
    SynthesisResult,
)


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


class ReferenceAudioPreparationService(Protocol):
    def inspect(self, input_path: Path) -> AudioSourceMetadata:
        """Inspect a source audio file and return its metadata."""

    def suggest_segments(self, input_path: Path, metadata: AudioSourceMetadata) -> tuple[ReferenceClipCandidate, ...]:
        """Return ranked candidate reference segments for the given source audio."""

    def export_segment(
        self,
        input_path: Path,
        output_path: Path,
        segment: ReferenceClipCandidate,
    ) -> Path:
        """Export a single audio segment to a WAV file."""
