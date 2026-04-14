from __future__ import annotations

from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "local"
    log_level: str = "INFO"
    workdir: Path = Path(".local")
    gpt_sovits_root: Path | None = None
    model_manifest: Path = Path(".local/model-profiles.json")
    temp_root: Path = Path(".local/tmp")
    output_root: Path = Path(".local/outputs")
    default_device: str = "auto"
    use_fp16: bool = True

    model_config = SettingsConfigDict(
        env_prefix="VOICE_TTS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("env")
    @classmethod
    def _normalize_env(cls, value: str) -> str:
        normalized = value.strip().lower()
        allowed = {"local", "test", "ci", "prod"}
        if normalized not in allowed:
            raise ValueError(f"env must be one of {sorted(allowed)}")
        return normalized

    @field_validator("log_level")
    @classmethod
    def _normalize_log_level(cls, value: str) -> str:
        normalized = value.strip().upper()
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if normalized not in allowed:
            raise ValueError(f"log_level must be one of {sorted(allowed)}")
        return normalized

    @field_validator("gpt_sovits_root", mode="before")
    @classmethod
    def _blank_path_to_none(cls, value: object) -> object:
        if value is None:
            return None
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @field_validator("default_device")
    @classmethod
    def _normalize_device(cls, value: str) -> str:
        normalized = value.strip().lower()
        allowed = {"auto", "cpu", "cuda"}
        if normalized not in allowed:
            raise ValueError(f"default_device must be one of {sorted(allowed)}")
        return normalized
