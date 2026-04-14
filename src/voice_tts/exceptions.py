from __future__ import annotations


VOICE_TTS_ERROR_STAGES = {
    "manifest",
    "preflight",
    "import",
    "trim",
    "synthesis",
    "output",
}


def with_stage(stage: str, detail: str) -> str:
    normalized_stage = stage.strip().lower()
    if normalized_stage not in VOICE_TTS_ERROR_STAGES:
        raise ValueError(f"unsupported voice-tts error stage: {stage}")
    return f"[{normalized_stage}] {detail}"


class VoiceTtsError(Exception):
    """Base exception for deterministic voice-tts failures."""


class VoiceTtsConfigurationError(VoiceTtsError):
    """Raised when runtime configuration is missing or invalid."""


class VoiceTtsUsageError(VoiceTtsError):
    """Raised when CLI inputs or user-supplied paths are invalid."""


class VoiceTtsDependencyError(VoiceTtsError):
    """Raised when an external runtime dependency is unavailable."""


class ManifestError(VoiceTtsConfigurationError):
    """Raised when the model profile manifest cannot be read or validated."""


class ModelProfileNotFoundError(VoiceTtsUsageError):
    """Raised when the requested model profile does not exist."""


class VoiceTtsSynthesisError(VoiceTtsError):
    """Raised when upstream synthesis or WAV serialization fails."""
