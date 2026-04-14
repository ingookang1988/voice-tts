from __future__ import annotations

import shutil
from pathlib import Path


def find_ffmpeg_executable() -> Path | None:
    executable = shutil.which("ffmpeg")
    if executable is None:
        return None
    return Path(executable)
