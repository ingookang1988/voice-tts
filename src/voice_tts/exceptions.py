from __future__ import annotations


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
