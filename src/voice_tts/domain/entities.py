from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from voice_tts.domain.value_objects import DevicePolicy, LanguageCode, SamplingProfile

SUPPORTED_MODEL_VERSION = "gpt-sovits-v2"
DEFAULT_REQUIRED_CHECKOUT_FILES = (Path("GPT_SoVITS/TTS_infer_pack/TTS.py"),)
DEFAULT_SUPPORTED_DEVICES = ("auto", "cpu", "cuda")


@dataclass(frozen=True, slots=True)
class ModelCompatibility:
    required_checkout_files: tuple[Path, ...] = field(
        default_factory=lambda: DEFAULT_REQUIRED_CHECKOUT_FILES
    )
    supported_devices: tuple[str, ...] = field(
        default_factory=lambda: DEFAULT_SUPPORTED_DEVICES
    )

    def __post_init__(self) -> None:
        normalized_paths: list[Path] = []
        for raw_path in self.required_checkout_files:
            candidate = Path(raw_path)
            if not str(candidate).strip():
                raise ValueError("required_checkout_files entries must not be blank")
            if candidate.is_absolute():
                raise ValueError("required_checkout_files entries must be relative paths")
            normalized_paths.append(candidate)
        if not normalized_paths:
            raise ValueError("required_checkout_files must not be empty")
        object.__setattr__(self, "required_checkout_files", tuple(normalized_paths))

        normalized_devices: list[str] = []
        for raw_device in self.supported_devices:
            normalized_devices.append(DevicePolicy(raw_device).value)
        if not normalized_devices:
            raise ValueError("supported_devices must not be empty")
        object.__setattr__(self, "supported_devices", tuple(dict.fromkeys(normalized_devices)))


@dataclass(frozen=True, slots=True)
class ModelProfile:
    id: str
    display_name: str
    version: str
    tts_config_path: Path
    languages: tuple[str, ...] = field(default_factory=lambda: ("auto",))
    speaker_tags: tuple[str, ...] = field(default_factory=tuple)
    notes: str | None = None
    compatibility: ModelCompatibility = field(default_factory=ModelCompatibility)
    normalization_warnings: tuple[str, ...] = field(default_factory=tuple, repr=False)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("id must not be blank")
        if not self.display_name.strip():
            raise ValueError("display_name must not be blank")
        if self.version.strip().lower() != SUPPORTED_MODEL_VERSION:
            raise ValueError(f"version must be '{SUPPORTED_MODEL_VERSION}'")
        if not str(self.tts_config_path).strip():
            raise ValueError("tts_config_path must not be blank")

        normalized_languages = tuple(LanguageCode(language).value for language in self.languages)
        if not normalized_languages:
            raise ValueError("languages must not be empty")
        object.__setattr__(self, "languages", tuple(dict.fromkeys(normalized_languages)))

        normalized_speaker_tags = tuple(
            tag.strip()
            for tag in self.speaker_tags
            if str(tag).strip()
        )
        object.__setattr__(
            self,
            "speaker_tags",
            tuple(dict.fromkeys(normalized_speaker_tags)),
        )

        normalized_notes = self.notes.strip() if isinstance(self.notes, str) else self.notes
        object.__setattr__(self, "notes", normalized_notes or None)

        normalized_warnings = tuple(
            warning.strip()
            for warning in self.normalization_warnings
            if str(warning).strip()
        )
        object.__setattr__(
            self,
            "normalization_warnings",
            tuple(dict.fromkeys(normalized_warnings)),
        )


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
