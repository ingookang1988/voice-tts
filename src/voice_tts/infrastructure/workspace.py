from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from voice_tts.domain.entities import DEFAULT_REQUIRED_CHECKOUT_FILES, DEFAULT_SUPPORTED_DEVICES
from voice_tts.exceptions import VoiceTtsConfigurationError, VoiceTtsSynthesisError, VoiceTtsUsageError, with_stage


DEFAULT_PROFILE_ID = "gsv2-default"
DEFAULT_PROFILE_DISPLAY_NAME = "Korean Zero-Shot"
DEFAULT_PROFILE_NOTES = "Reference profile for zero-shot local synthesis on a GPT-SoVITS v2 checkout."
ENV_FILE_PATH = Path(".env")
ENV_TEMPLATE_PATH = Path(".env.example")
WORKDIR_PATH = Path(".local")
TEMP_ROOT_PATH = Path(".local/tmp")


@dataclass(frozen=True, slots=True)
class WorkspaceInitializationResult:
    env_path: Path
    manifest_path: Path
    output_root: Path
    profile_id: str


def initialize_workspace(
    *,
    gpt_sovits_root: Path,
    manifest_path: Path,
    output_root: Path,
    force: bool,
) -> WorkspaceInitializationResult:
    if not gpt_sovits_root.exists():
        raise VoiceTtsUsageError(
            with_stage("preflight", f"gpt_sovits_root was not found: {gpt_sovits_root}")
        )
    if not gpt_sovits_root.is_dir():
        raise VoiceTtsUsageError(
            with_stage("preflight", f"gpt_sovits_root is not a directory: {gpt_sovits_root}")
        )
    if not ENV_TEMPLATE_PATH.exists():
        raise VoiceTtsConfigurationError(
            with_stage("preflight", f".env template was not found: {ENV_TEMPLATE_PATH}")
        )

    if ENV_FILE_PATH.exists() and not force:
        raise VoiceTtsUsageError(
            with_stage("preflight", f"{ENV_FILE_PATH} already exists; pass --force to overwrite")
        )
    if manifest_path.exists() and not force:
        raise VoiceTtsUsageError(
            with_stage("preflight", f"{manifest_path} already exists; pass --force to overwrite")
        )

    WORKDIR_PATH.mkdir(parents=True, exist_ok=True)
    TEMP_ROOT_PATH.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)

    env_content = render_env_file(
        template=ENV_TEMPLATE_PATH.read_text(encoding="utf-8"),
        gpt_sovits_root=gpt_sovits_root,
        manifest_path=manifest_path,
        output_root=output_root,
    )
    manifest_payload = build_seed_manifest_payload(gpt_sovits_root)

    try:
        ENV_FILE_PATH.write_text(env_content, encoding="utf-8")
        manifest_path.write_text(
            json.dumps(manifest_payload, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise VoiceTtsSynthesisError(
            with_stage("output", f"failed to write workspace scaffolding: {exc}")
        ) from exc

    return WorkspaceInitializationResult(
        env_path=ENV_FILE_PATH,
        manifest_path=manifest_path,
        output_root=output_root,
        profile_id=DEFAULT_PROFILE_ID,
    )


def build_seed_manifest_payload(gpt_sovits_root: Path) -> dict[str, object]:
    config_path = (gpt_sovits_root / "GPT_SoVITS" / "configs" / "tts_infer.yaml").resolve()
    return {
        "profiles": [
            {
                "id": DEFAULT_PROFILE_ID,
                "display_name": DEFAULT_PROFILE_DISPLAY_NAME,
                "version": "gpt-sovits-v2",
                "tts_config_path": str(config_path),
                "languages": ["ko", "en"],
                "speaker_tags": ["female", "studio"],
                "notes": DEFAULT_PROFILE_NOTES,
                "compatibility": {
                    "required_checkout_files": [str(path) for path in DEFAULT_REQUIRED_CHECKOUT_FILES],
                    "supported_devices": list(DEFAULT_SUPPORTED_DEVICES),
                },
            }
        ]
    }


def render_env_file(
    *,
    template: str,
    gpt_sovits_root: Path,
    manifest_path: Path,
    output_root: Path,
) -> str:
    replacements = {
        "VOICE_TTS_ENV": "local",
        "VOICE_TTS_LOG_LEVEL": "INFO",
        "VOICE_TTS_WORKDIR": str(WORKDIR_PATH),
        "VOICE_TTS_GPT_SOVITS_ROOT": str(gpt_sovits_root),
        "VOICE_TTS_MODEL_MANIFEST": str(manifest_path),
        "VOICE_TTS_TEMP_ROOT": str(TEMP_ROOT_PATH),
        "VOICE_TTS_OUTPUT_ROOT": str(output_root),
        "VOICE_TTS_DEFAULT_DEVICE": "auto",
        "VOICE_TTS_USE_FP16": "true",
    }

    rendered_lines: list[str] = []
    seen_keys: set[str] = set()
    for raw_line in template.splitlines():
        key, separator, _ = raw_line.partition("=")
        if separator and key in replacements:
            rendered_lines.append(f"{key}={replacements[key]}")
            seen_keys.add(key)
        else:
            rendered_lines.append(raw_line)

    for key, value in replacements.items():
        if key not in seen_keys:
            rendered_lines.append(f"{key}={value}")

    return "\n".join(rendered_lines) + "\n"
