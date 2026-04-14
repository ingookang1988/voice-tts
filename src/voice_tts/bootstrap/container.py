from __future__ import annotations

from dataclasses import dataclass

from voice_tts.application.use_cases import SynthesizeSpeechUseCase
from voice_tts.infrastructure.config import Settings
from voice_tts.infrastructure.engines import GptSovitsV2SpeechSynthesisEngine
from voice_tts.infrastructure.logging import configure_logging
from voice_tts.infrastructure.repositories import JsonModelProfileRepository


@dataclass(slots=True)
class ApplicationContainer:
    settings: Settings
    model_profile_repository: JsonModelProfileRepository
    synthesis_engine: GptSovitsV2SpeechSynthesisEngine
    synthesize_speech: SynthesizeSpeechUseCase


def build_container(settings: Settings | None = None) -> ApplicationContainer:
    resolved_settings = settings or Settings()
    configure_logging(resolved_settings.log_level)

    model_profile_repository = JsonModelProfileRepository(resolved_settings.model_manifest)
    synthesis_engine = GptSovitsV2SpeechSynthesisEngine(
        gpt_sovits_root=resolved_settings.gpt_sovits_root,
        default_device=resolved_settings.default_device,
        use_fp16=resolved_settings.use_fp16,
        temp_root=resolved_settings.temp_root,
    )
    synthesize_speech = SynthesizeSpeechUseCase(
        model_profile_repository=model_profile_repository,
        engine=synthesis_engine,
        output_root=resolved_settings.output_root,
    )
    return ApplicationContainer(
        settings=resolved_settings,
        model_profile_repository=model_profile_repository,
        synthesis_engine=synthesis_engine,
        synthesize_speech=synthesize_speech,
    )
