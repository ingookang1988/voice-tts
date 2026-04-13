from __future__ import annotations

from dataclasses import dataclass

from voice_tts.application.use_cases import SynthesizeSpeechUseCase
from voice_tts.infrastructure.config import Settings
from voice_tts.infrastructure.engines import PlaceholderSpeechSynthesisEngine
from voice_tts.infrastructure.logging import configure_logging
from voice_tts.infrastructure.repositories import PlaceholderWeightRepository


@dataclass(slots=True)
class ApplicationContainer:
    settings: Settings
    weight_repository: PlaceholderWeightRepository
    synthesis_engine: PlaceholderSpeechSynthesisEngine
    synthesize_speech: SynthesizeSpeechUseCase


def build_container(settings: Settings | None = None) -> ApplicationContainer:
    resolved_settings = settings or Settings()
    configure_logging(resolved_settings.log_level)

    weight_repository = PlaceholderWeightRepository(resolved_settings.weights_root)
    synthesis_engine = PlaceholderSpeechSynthesisEngine(
        gpt_sovits_root=resolved_settings.gpt_sovits_root,
        default_device=resolved_settings.default_device,
        use_fp16=resolved_settings.use_fp16,
    )
    synthesize_speech = SynthesizeSpeechUseCase(
        weight_repository=weight_repository,
        engine=synthesis_engine,
    )
    return ApplicationContainer(
        settings=resolved_settings,
        weight_repository=weight_repository,
        synthesis_engine=synthesis_engine,
        synthesize_speech=synthesize_speech,
    )

