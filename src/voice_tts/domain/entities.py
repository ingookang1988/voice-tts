from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from voice_tts.domain.value_objects import LanguageCode, SamplingProfile


@dataclass(frozen=True, slots=True)
class ModelWeights:
    speaker_id: str
    gpt_weights: Path | None = None
    sovits_weights: Path | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.speaker_id.strip():
            raise ValueError("speaker_id must not be blank")


@dataclass(frozen=True, slots=True)
class SynthesisRequest:
    text: str
    speaker_id: str
    language_code: LanguageCode = field(default_factory=LanguageCode)
    reference_text: str | None = None
    sampling_profile: SamplingProfile = field(default_factory=SamplingProfile)

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("text must not be blank")
        if not self.speaker_id.strip():
            raise ValueError("speaker_id must not be blank")


@dataclass(frozen=True, slots=True)
class SynthesisResult:
    audio_path: Path
    sample_rate: int
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be positive")

