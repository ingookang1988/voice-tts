from __future__ import annotations

import json
from pathlib import Path

import pytest

from voice_tts.exceptions import VoiceTtsUsageError
from voice_tts.infrastructure.workspace import (
    build_seed_manifest_payload,
    initialize_workspace,
    render_env_file,
)


def test_build_seed_manifest_payload_uses_checkout_root(tmp_path: Path) -> None:
    gpt_root = tmp_path / "gpt"
    gpt_root.mkdir()

    payload = build_seed_manifest_payload(gpt_root)

    profile = payload["profiles"][0]
    assert profile["id"] == "gsv2-default"
    assert profile["tts_config_path"] == str((gpt_root / "GPT_SoVITS" / "configs" / "tts_infer.yaml").resolve())


def test_render_env_file_injects_runtime_paths(tmp_path: Path) -> None:
    rendered = render_env_file(
        template="VOICE_TTS_GPT_SOVITS_ROOT=\nVOICE_TTS_MODEL_MANIFEST=\nVOICE_TTS_OUTPUT_ROOT=\n",
        gpt_sovits_root=tmp_path / "gpt",
        manifest_path=tmp_path / "manifest.json",
        output_root=tmp_path / "outputs",
    )

    assert f"VOICE_TTS_GPT_SOVITS_ROOT={tmp_path / 'gpt'}" in rendered
    assert f"VOICE_TTS_MODEL_MANIFEST={tmp_path / 'manifest.json'}" in rendered
    assert f"VOICE_TTS_OUTPUT_ROOT={tmp_path / 'outputs'}" in rendered


def test_initialize_workspace_writes_scaffolding(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env.example").write_text(
        "VOICE_TTS_GPT_SOVITS_ROOT=\nVOICE_TTS_MODEL_MANIFEST=\nVOICE_TTS_OUTPUT_ROOT=\n",
        encoding="utf-8",
    )
    gpt_root = tmp_path / "gpt"
    gpt_root.mkdir()

    result = initialize_workspace(
        gpt_sovits_root=gpt_root,
        manifest_path=tmp_path / ".local" / "model-profiles.json",
        output_root=tmp_path / ".local" / "outputs",
        force=False,
    )

    assert result.env_path == Path(".env")
    assert Path(".env").exists()
    manifest_payload = json.loads((tmp_path / ".local" / "model-profiles.json").read_text(encoding="utf-8"))
    assert manifest_payload["profiles"][0]["id"] == "gsv2-default"
    assert (tmp_path / ".local" / "tmp").exists()


def test_initialize_workspace_rejects_existing_manifest_without_force(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env.example").write_text("VOICE_TTS_GPT_SOVITS_ROOT=\n", encoding="utf-8")
    gpt_root = tmp_path / "gpt"
    gpt_root.mkdir()
    manifest_path = tmp_path / ".local" / "model-profiles.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text("{}", encoding="utf-8")

    with pytest.raises(VoiceTtsUsageError, match="\\[preflight\\].*already exists; pass --force to overwrite"):
        initialize_workspace(
            gpt_sovits_root=gpt_root,
            manifest_path=manifest_path,
            output_root=tmp_path / ".local" / "outputs",
            force=False,
        )
