"""Domain models and ports for voice-tts."""

from voice_tts.domain.entities import (
    AudioSourceMetadata,
    DEFAULT_REQUIRED_CHECKOUT_FILES,
    DEFAULT_SUPPORTED_DEVICES,
    ReferenceAudioPreparationResult,
    ReferenceClipCandidate,
    SUPPORTED_MODEL_VERSION,
    ModelCompatibility,
    ModelProfile,
    SynthesisRequest,
    SynthesisResult,
)
from voice_tts.domain.ports import (
    ModelProfileRepository,
    ReferenceAudioPreparationService,
    SpeechSynthesisEngine,
)
from voice_tts.domain.value_objects import DevicePolicy, LanguageCode, SamplingProfile

__all__ = [
    "DevicePolicy",
    "DEFAULT_REQUIRED_CHECKOUT_FILES",
    "DEFAULT_SUPPORTED_DEVICES",
    "LanguageCode",
    "ModelCompatibility",
    "ModelProfile",
    "ModelProfileRepository",
    "AudioSourceMetadata",
    "ReferenceAudioPreparationResult",
    "ReferenceAudioPreparationService",
    "ReferenceClipCandidate",
    "SamplingProfile",
    "SpeechSynthesisEngine",
    "SUPPORTED_MODEL_VERSION",
    "SynthesisRequest",
    "SynthesisResult",
]
