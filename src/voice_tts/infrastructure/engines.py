from __future__ import annotations

from pathlib import Path

from voice_tts.domain.entities import ModelWeights, SynthesisRequest, SynthesisResult


class PlaceholderSpeechSynthesisEngine:
    """Phase 1 placeholder for a future GPT-SoVITS adapter."""

    def __init__(
        self,
        gpt_sovits_root: Path | None,
        default_device: str,
        use_fp16: bool,
    ) -> None:
        self.gpt_sovits_root = gpt_sovits_root
        self.default_device = default_device
        self.use_fp16 = use_fp16

    def synthesize(
        self,
        request: SynthesisRequest,
        weights: ModelWeights,
    ) -> SynthesisResult:
        raise NotImplementedError(
            "Phase 1 does not implement real GPT-SoVITS inference yet."
        )

