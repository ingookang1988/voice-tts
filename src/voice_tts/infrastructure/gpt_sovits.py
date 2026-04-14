from __future__ import annotations

import importlib
import sys
from pathlib import Path


GPT_SOVITS_TTS_MODULE = "GPT_SoVITS.TTS_infer_pack.TTS"
YAML_SUFFIXES = {".yaml", ".yml"}


def ensure_gpt_sovits_on_sys_path(gpt_sovits_root: Path) -> None:
    root_text = str(gpt_sovits_root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    importlib.invalidate_caches()


def shallow_import_tts_module(gpt_sovits_root: Path):
    ensure_gpt_sovits_on_sys_path(gpt_sovits_root)
    return importlib.import_module(GPT_SOVITS_TTS_MODULE)


def is_yaml_like_path(path: Path) -> bool:
    return path.suffix.lower() in YAML_SUFFIXES
