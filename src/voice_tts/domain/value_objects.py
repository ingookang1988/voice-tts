from __future__ import annotations

from dataclasses import dataclass


_DEVICE_POLICIES = {"auto", "cpu", "cuda"}


@dataclass(frozen=True, slots=True)
class DevicePolicy:
    value: str = "auto"

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if normalized not in _DEVICE_POLICIES:
            raise ValueError(f"unsupported device policy: {self.value}")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class LanguageCode:
    value: str = "auto"

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not normalized:
            raise ValueError("language code must not be blank")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class SamplingProfile:
    top_p: float = 1.0
    temperature: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 < self.top_p <= 1.0:
            raise ValueError("top_p must be within (0.0, 1.0]")
        if self.temperature <= 0.0:
            raise ValueError("temperature must be positive")

