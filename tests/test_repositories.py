from __future__ import annotations

import json
from pathlib import Path

import pytest

from voice_tts.exceptions import ManifestError, ModelProfileNotFoundError
from voice_tts.infrastructure.repositories import JsonModelProfileRepository


def _manifest_payload(tts_config_path: str) -> dict[str, object]:
    return {
        "profiles": [
            {
                "id": "gsv2-default",
                "version": "gpt-sovits-v2",
                "tts_config_path": tts_config_path,
            }
        ]
    }


def test_repository_loads_profiles_and_resolves_relative_paths(tmp_path: Path) -> None:
    config_root = tmp_path / "configs"
    config_root.mkdir()
    tts_config_path = config_root / "tts_infer.yaml"
    tts_config_path.write_text("custom: {}\n", encoding="utf-8")
    manifest_path = tmp_path / "model-profiles.json"
    manifest_path.write_text(
        json.dumps(_manifest_payload("configs/tts_infer.yaml")),
        encoding="utf-8",
    )

    repository = JsonModelProfileRepository(manifest_path)
    profiles = repository.list_profiles()

    assert len(profiles) == 1
    assert profiles[0].id == "gsv2-default"
    assert profiles[0].tts_config_path == tts_config_path.resolve()


def test_repository_raises_for_unknown_profile(tmp_path: Path) -> None:
    config_root = tmp_path / "configs"
    config_root.mkdir()
    tts_config_path = config_root / "tts_infer.yaml"
    tts_config_path.write_text("custom: {}\n", encoding="utf-8")
    manifest_path = tmp_path / "model-profiles.json"
    manifest_path.write_text(
        json.dumps(_manifest_payload(str(tts_config_path))),
        encoding="utf-8",
    )

    repository = JsonModelProfileRepository(manifest_path)
    with pytest.raises(ModelProfileNotFoundError):
        repository.get_by_id("missing")


def test_repository_rejects_invalid_manifest_json(tmp_path: Path) -> None:
    manifest_path = tmp_path / "model-profiles.json"
    manifest_path.write_text("{not-json}", encoding="utf-8")

    repository = JsonModelProfileRepository(manifest_path)
    with pytest.raises(ManifestError):
        repository.list_profiles()


def test_repository_rejects_unsupported_profile_version(tmp_path: Path) -> None:
    manifest_path = tmp_path / "model-profiles.json"
    manifest_path.write_text(
        json.dumps(
            {
                "profiles": [
                    {
                        "id": "bad-profile",
                        "version": "gpt-sovits-v3",
                        "tts_config_path": "tts_infer.yaml",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    repository = JsonModelProfileRepository(manifest_path)
    with pytest.raises(ManifestError):
        repository.list_profiles()
