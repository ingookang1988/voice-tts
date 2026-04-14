from __future__ import annotations

import json
from pathlib import Path

import pytest

from voice_tts.exceptions import ManifestError, ModelProfileNotFoundError
from voice_tts.infrastructure.repositories import JsonModelProfileRepository


def _modern_manifest_payload(tts_config_path: str) -> dict[str, object]:
    return {
        "profiles": [
            {
                "id": "gsv2-default",
                "display_name": "Korean Zero-Shot",
                "version": "gpt-sovits-v2",
                "tts_config_path": tts_config_path,
                "languages": ["ko", "en"],
                "speaker_tags": ["female", "studio"],
                "notes": "baseline profile",
                "compatibility": {
                    "required_checkout_files": ["GPT_SoVITS/TTS_infer_pack/TTS.py"],
                    "supported_devices": ["auto", "cpu"],
                },
            }
        ]
    }


def _legacy_manifest_payload(tts_config_path: str) -> dict[str, object]:
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
        json.dumps(_modern_manifest_payload("configs/tts_infer.yaml")),
        encoding="utf-8",
    )

    repository = JsonModelProfileRepository(manifest_path)
    profiles = repository.list_profiles()

    assert len(profiles) == 1
    profile = profiles[0]
    assert profile.id == "gsv2-default"
    assert profile.display_name == "Korean Zero-Shot"
    assert profile.tts_config_path == tts_config_path.resolve()
    assert profile.languages == ("ko", "en")
    assert profile.speaker_tags == ("female", "studio")
    assert profile.notes == "baseline profile"
    assert profile.compatibility.supported_devices == ("auto", "cpu")
    assert profile.normalization_warnings == ()


def test_repository_applies_legacy_defaults_with_warnings(tmp_path: Path) -> None:
    config_root = tmp_path / "configs"
    config_root.mkdir()
    tts_config_path = config_root / "tts_infer.yaml"
    tts_config_path.write_text("custom: {}\n", encoding="utf-8")
    manifest_path = tmp_path / "model-profiles.json"
    manifest_path.write_text(
        json.dumps(_legacy_manifest_payload(str(tts_config_path))),
        encoding="utf-8",
    )

    repository = JsonModelProfileRepository(manifest_path)
    profile = repository.list_profiles()[0]

    assert profile.display_name == "gsv2-default"
    assert profile.languages == ("auto",)
    assert profile.speaker_tags == ()
    assert profile.notes is None
    assert profile.compatibility.supported_devices == ("auto", "cpu", "cuda")
    assert "legacy defaults applied for display_name" in profile.normalization_warnings
    assert "legacy defaults applied for compatibility" in profile.normalization_warnings


def test_repository_raises_for_unknown_profile(tmp_path: Path) -> None:
    config_root = tmp_path / "configs"
    config_root.mkdir()
    tts_config_path = config_root / "tts_infer.yaml"
    tts_config_path.write_text("custom: {}\n", encoding="utf-8")
    manifest_path = tmp_path / "model-profiles.json"
    manifest_path.write_text(
        json.dumps(_modern_manifest_payload(str(tts_config_path))),
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


def test_repository_rejects_invalid_compatibility_shape(tmp_path: Path) -> None:
    manifest_path = tmp_path / "model-profiles.json"
    manifest_path.write_text(
        json.dumps(
            {
                "profiles": [
                    {
                        "id": "bad-profile",
                        "display_name": "Bad",
                        "version": "gpt-sovits-v2",
                        "tts_config_path": "tts_infer.yaml",
                        "languages": ["ko"],
                        "speaker_tags": [],
                        "compatibility": [],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    repository = JsonModelProfileRepository(manifest_path)
    with pytest.raises(ManifestError):
        repository.list_profiles()


def test_repository_rejects_invalid_supported_devices(tmp_path: Path) -> None:
    manifest_path = tmp_path / "model-profiles.json"
    manifest_path.write_text(
        json.dumps(
            {
                "profiles": [
                    {
                        "id": "bad-profile",
                        "display_name": "Bad",
                        "version": "gpt-sovits-v2",
                        "tts_config_path": "tts_infer.yaml",
                        "languages": ["ko"],
                        "speaker_tags": [],
                        "compatibility": {
                            "required_checkout_files": ["GPT_SoVITS/TTS_infer_pack/TTS.py"],
                            "supported_devices": ["cuda", "tpu"],
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

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
                        "display_name": "Bad",
                        "version": "gpt-sovits-v3",
                        "tts_config_path": "tts_infer.yaml",
                        "languages": ["ko"],
                        "speaker_tags": [],
                        "compatibility": {
                            "required_checkout_files": ["GPT_SoVITS/TTS_infer_pack/TTS.py"],
                            "supported_devices": ["auto", "cpu"],
                        },
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    repository = JsonModelProfileRepository(manifest_path)
    with pytest.raises(ManifestError):
        repository.list_profiles()
