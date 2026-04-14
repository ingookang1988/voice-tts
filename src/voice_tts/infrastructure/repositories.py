from __future__ import annotations

import json
from pathlib import Path

from voice_tts.domain.entities import (
    DEFAULT_REQUIRED_CHECKOUT_FILES,
    DEFAULT_SUPPORTED_DEVICES,
    ModelCompatibility,
    ModelProfile,
)
from voice_tts.exceptions import ManifestError, ModelProfileNotFoundError, with_stage


class JsonModelProfileRepository:
    """Manifest-backed repository for local synthesis model profiles."""

    def __init__(self, manifest_path: Path) -> None:
        self.manifest_path = manifest_path

    def get_by_id(self, model_profile_id: str) -> ModelProfile:
        for profile in self.list_profiles():
            if profile.id == model_profile_id:
                return profile
        raise ModelProfileNotFoundError(
            with_stage(
                "manifest",
                f"model profile '{model_profile_id}' was not found in {self.manifest_path}",
            )
        )

    def list_profiles(self) -> tuple[ModelProfile, ...]:
        payload = self._load_manifest()
        raw_profiles = payload.get("profiles")
        if not isinstance(raw_profiles, list):
            raise ManifestError(
                with_stage("manifest", "model manifest must contain a 'profiles' list")
            )

        profiles: list[ModelProfile] = []
        for index, item in enumerate(raw_profiles):
            if not isinstance(item, dict):
                raise ManifestError(
                    with_stage("manifest", f"profile entry at index {index} must be an object")
                )
            try:
                profiles.append(self._build_profile(item))
            except KeyError as exc:
                raise ManifestError(
                    with_stage(
                        "manifest",
                        f"profile entry at index {index} is missing '{exc.args[0]}'",
                    )
                ) from exc
            except ValueError as exc:
                raise ManifestError(
                    with_stage("manifest", f"invalid profile entry at index {index}: {exc}")
                ) from exc

        if not profiles:
            raise ManifestError(with_stage("manifest", "model manifest must define at least one profile"))
        return tuple(profiles)

    def _load_manifest(self) -> dict[str, object]:
        if not self.manifest_path.exists():
            raise ManifestError(
                with_stage("manifest", f"model manifest not found: {self.manifest_path}")
            )
        if not self.manifest_path.is_file():
            raise ManifestError(
                with_stage("manifest", f"model manifest is not a file: {self.manifest_path}")
            )
        try:
            payload = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise ManifestError(
                with_stage("manifest", f"failed to read model manifest {self.manifest_path}: {exc}")
            ) from exc
        except json.JSONDecodeError as exc:
            raise ManifestError(
                with_stage("manifest", f"failed to parse model manifest {self.manifest_path}: {exc.msg}")
            ) from exc
        if not isinstance(payload, dict):
            raise ManifestError(
                with_stage("manifest", "model manifest root must be a JSON object")
            )
        return payload

    def _resolve_path(self, raw_path: object) -> Path:
        path_value = Path(str(raw_path))
        if path_value.is_absolute():
            return path_value
        return (self.manifest_path.parent / path_value).resolve()

    def _build_profile(self, payload: dict[str, object]) -> ModelProfile:
        profile_id = str(payload["id"])
        warnings: list[str] = []

        display_name_raw = payload.get("display_name")
        if display_name_raw is None:
            warnings.append("display_name")
            display_name = profile_id
        elif not isinstance(display_name_raw, str) or not display_name_raw.strip():
            raise ValueError("display_name must be a non-blank string")
        else:
            display_name = display_name_raw

        languages = self._resolve_string_list(
            payload=payload,
            field_name="languages",
            default=("auto",),
            warnings=warnings,
            allow_empty=False,
        )
        speaker_tags = self._resolve_string_list(
            payload=payload,
            field_name="speaker_tags",
            default=(),
            warnings=warnings,
            allow_empty=True,
        )
        notes = self._resolve_optional_string(payload=payload, field_name="notes", warnings=warnings)
        compatibility = self._resolve_compatibility(payload=payload, warnings=warnings)

        return ModelProfile(
            id=profile_id,
            display_name=display_name,
            version=str(payload["version"]),
            tts_config_path=self._resolve_path(payload["tts_config_path"]),
            languages=languages,
            speaker_tags=speaker_tags,
            notes=notes,
            compatibility=compatibility,
            normalization_warnings=tuple(
                f"legacy defaults applied for {field_name}"
                for field_name in warnings
            ),
        )

    def _resolve_string_list(
        self,
        payload: dict[str, object],
        field_name: str,
        default: tuple[str, ...],
        warnings: list[str],
        allow_empty: bool,
    ) -> tuple[str, ...]:
        raw_value = payload.get(field_name)
        if raw_value is None:
            warnings.append(field_name)
            return default
        if not isinstance(raw_value, list):
            raise ValueError(f"{field_name} must be a list of strings")

        values: list[str] = []
        for item in raw_value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"{field_name} entries must be non-blank strings")
            values.append(item.strip())
        if not values and not allow_empty:
            raise ValueError(f"{field_name} must not be empty")
        return tuple(values)

    def _resolve_optional_string(
        self,
        payload: dict[str, object],
        field_name: str,
        warnings: list[str],
    ) -> str | None:
        raw_value = payload.get(field_name)
        if raw_value is None:
            warnings.append(field_name)
            return None
        if not isinstance(raw_value, str):
            raise ValueError(f"{field_name} must be a string or null")
        stripped = raw_value.strip()
        return stripped or None

    def _resolve_compatibility(
        self,
        payload: dict[str, object],
        warnings: list[str],
    ) -> ModelCompatibility:
        raw_value = payload.get("compatibility")
        if raw_value is None:
            warnings.append("compatibility")
            return ModelCompatibility()
        if not isinstance(raw_value, dict):
            raise ValueError("compatibility must be an object")

        required_checkout_files_raw = raw_value.get("required_checkout_files")
        if required_checkout_files_raw is None:
            warnings.append("compatibility.required_checkout_files")
            required_checkout_files = DEFAULT_REQUIRED_CHECKOUT_FILES
        else:
            if not isinstance(required_checkout_files_raw, list):
                raise ValueError("compatibility.required_checkout_files must be a list")
            required_checkout_files = tuple(Path(str(item)) for item in required_checkout_files_raw)

        supported_devices_raw = raw_value.get("supported_devices")
        if supported_devices_raw is None:
            warnings.append("compatibility.supported_devices")
            supported_devices = DEFAULT_SUPPORTED_DEVICES
        else:
            if not isinstance(supported_devices_raw, list):
                raise ValueError("compatibility.supported_devices must be a list")
            supported_devices = tuple(str(item) for item in supported_devices_raw)

        return ModelCompatibility(
            required_checkout_files=required_checkout_files,
            supported_devices=supported_devices,
        )
