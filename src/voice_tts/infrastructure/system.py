from __future__ import annotations

import shutil
from pathlib import Path


def find_ffmpeg_executable() -> Path | None:
    executable = shutil.which("ffmpeg")
    if executable is None:
        return None
    return Path(executable)


def find_ffprobe_executable() -> Path | None:
    executable = shutil.which("ffprobe")
    if executable is not None:
        return Path(executable)

    ffmpeg = find_ffmpeg_executable()
    if ffmpeg is None:
        return None

    suffix = ffmpeg.suffix
    sibling = ffmpeg.with_name(f"ffprobe{suffix}")
    if sibling.exists():
        return sibling
    return None
