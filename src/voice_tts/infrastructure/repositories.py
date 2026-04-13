from __future__ import annotations

from pathlib import Path

from voice_tts.domain.entities import ModelWeights


class PlaceholderWeightRepository:
    """Phase 1 placeholder for a future local weight repository."""

    def __init__(self, weights_root: Path | None) -> None:
        self.weights_root = weights_root

    def get_by_speaker_id(self, speaker_id: str) -> ModelWeights:
        raise NotImplementedError(
            "Phase 1 does not resolve speaker weights yet."
        )

