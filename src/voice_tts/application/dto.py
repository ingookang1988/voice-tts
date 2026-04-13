from __future__ import annotations

from dataclasses import dataclass, field

from voice_tts.domain.entities import SynthesisRequest, SynthesisResult
from voice_tts.domain.value_objects import LanguageCode, SamplingProfile


@dataclass(frozen=True, slots=True)
class SynthesizeSpeechCommand:
    text: str
    speaker_id: str
    language_code: str = "auto"
    reference_text: str | None = None
    top_p: float = 1.0
    temperature: float = 1.0

    def to_domain(self) -> SynthesisRequest:
        return SynthesisRequest(
            text=self.text,
            speaker_id=self.speaker_id,
            language_code=LanguageCode(self.language_code),
            reference_text=self.reference_text,
            sampling_profile=SamplingProfile(
                top_p=self.top_p,
                temperature=self.temperature,
            ),
        )


@dataclass(frozen=True, slots=True)
class SynthesizeSpeechResultDto:
    audio_path: str
    sample_rate: int
    metadata: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_domain(cls, result: SynthesisResult) -> "SynthesizeSpeechResultDto":
        return cls(
            audio_path=str(result.audio_path),
            sample_rate=result.sample_rate,
            metadata=dict(result.metadata),
        )

