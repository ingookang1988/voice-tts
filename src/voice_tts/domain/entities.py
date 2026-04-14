from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from voice_tts.domain.value_objects import LanguageCode, SamplingProfile

SUPPORTED_MODEL_VERSION = "gpt-sovits-v2"


@dataclass(frozen=True, slots=True)
class ModelProfile:
    id: str
    version: str
    tts_config_path: Path
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("id must not be blank")
        if self.version.strip().lower() != SUPPORTED_MODEL_VERSION:
            raise ValueError(f"version must be '{SUPPORTED_MODEL_VERSION}'")
        if not str(self.tts_config_path).strip():
            raise ValueError("tts_config_path must not be blank")


@dataclass(frozen=True, slots=True)
class SynthesisRequest:
    model_profile_id: str
    text: str
    text_lang: LanguageCode = field(default_factory=LanguageCode)
    ref_audio_path: Path = field(default_factory=Path)
    ref_start_sec: float | None = None
    ref_end_sec: float | None = None
    prompt_text: str = ""
    prompt_lang: LanguageCode = field(default_factory=LanguageCode)
    output_path: Path = field(default_factory=Path)
    sampling_profile: SamplingProfile = field(default_factory=SamplingProfile)

    def __post_init__(self) -> None:
        if not self.model_profile_id.strip():
            raise ValueError("model_profile_id must not be blank")
        if not self.text.strip():
            raise ValueError("text must not be blank")
        if not self.prompt_text.strip():
            raise ValueError("prompt_text must not be blank")
        if not str(self.ref_audio_path).strip():
            raise ValueError("ref_audio_path must not be blank")
        if self.ref_start_sec is not None and self.ref_start_sec < 0.0:
            raise ValueError("ref_start_sec must be >= 0.0")
        effective_start = self.ref_start_sec or 0.0
        if self.ref_end_sec is not None and self.ref_end_sec <= effective_start:
            raise ValueError("ref_end_sec must be greater than ref_start_sec")
        if self.output_path.suffix.lower() != ".wav":
            raise ValueError("output_path must end with .wav")


@dataclass(frozen=True, slots=True)
class SynthesisResult:
    audio_path: Path
    sample_rate: int
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if self.audio_path.suffix.lower() != ".wav":
            raise ValueError("audio_path must end with .wav")
