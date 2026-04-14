from __future__ import annotations

import json
from pathlib import Path

from voice_tts.domain.entities import ModelProfile
from voice_tts.exceptions import ManifestError, ModelProfileNotFoundError


class JsonModelProfileRepository:
    """Manifest-backed repository for local synthesis model profiles."""

    def __init__(self, manifest_path: Path) -> None:
        self.manifest_path = manifest_path

    def get_by_id(self, model_profile_id: str) -> ModelProfile:
        for profile in self.list_profiles():
            if profile.id == model_profile_id:
                return profile
        raise ModelProfileNotFoundError(
            f"model profile '{model_profile_id}' was not found in {self.manifest_path}"
        )

    def list_profiles(self) -> tuple[ModelProfile, ...]:
        payload = self._load_manifest()
        raw_profiles = payload.get("profiles")
        if not isinstance(raw_profiles, list):
            raise ManifestError("model manifest must contain a 'profiles' list")

        profiles: list[ModelProfile] = []
        for index, item in enumerate(raw_profiles):
            if not isinstance(item, dict):
                raise ManifestError(f"profile entry at index {index} must be an object")
            try:
                metadata = item.get("metadata", {})
                if not isinstance(metadata, dict):
                    raise ManifestError("profile metadata must be an object")
                profiles.append(
                    ModelProfile(
                        id=str(item["id"]),
                        version=str(item["version"]),
                        tts_config_path=self._resolve_path(item["tts_config_path"]),
                        metadata={str(key): str(value) for key, value in metadata.items()},
                    )
                )
            except KeyError as exc:
                raise ManifestError(
                    f"profile entry at index {index} is missing '{exc.args[0]}'"
                ) from exc
            except ValueError as exc:
                raise ManifestError(f"invalid profile entry at index {index}: {exc}") from exc
        return tuple(profiles)

    def _load_manifest(self) -> dict[str, object]:
        if not self.manifest_path.exists():
            raise ManifestError(f"model manifest not found: {self.manifest_path}")
        if not self.manifest_path.is_file():
            raise ManifestError(f"model manifest is not a file: {self.manifest_path}")
        try:
            payload = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise ManifestError(
                f"failed to read model manifest {self.manifest_path}: {exc}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise ManifestError(
                f"failed to parse model manifest {self.manifest_path}: {exc.msg}"
            ) from exc
        if not isinstance(payload, dict):
            raise ManifestError("model manifest root must be a JSON object")
        return payload

    def _resolve_path(self, raw_path: object) -> Path:
        path_value = Path(str(raw_path))
        if path_value.is_absolute():
            return path_value
        return (self.manifest_path.parent / path_value).resolve()
