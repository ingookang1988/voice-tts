from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from voice_tts.infrastructure.config import Settings


@dataclass(frozen=True, slots=True)
class DoctorCheck:
    name: str
    status: str
    detail: str


@dataclass(frozen=True, slots=True)
class DoctorReport:
    settings: Settings
    checks: tuple[DoctorCheck, ...]

    @property
    def pass_count(self) -> int:
        return sum(1 for check in self.checks if check.status == "PASS")

    @property
    def warn_count(self) -> int:
        return sum(1 for check in self.checks if check.status == "WARN")

    @property
    def fail_count(self) -> int:
        return sum(1 for check in self.checks if check.status == "FAIL")

    @property
    def ok(self) -> bool:
        return self.fail_count == 0


def run_doctor(settings: Settings) -> DoctorReport:
    checks = (
        _python_version_check(),
        _device_policy_check(settings.default_device),
        _mutable_directory_check("workdir", settings.workdir),
        _mutable_directory_check("temp_root", settings.temp_root),
        _optional_external_path_check("gpt_sovits_root", settings.gpt_sovits_root),
        _optional_external_path_check("weights_root", settings.weights_root),
    )
    return DoctorReport(settings=settings, checks=checks)


def _python_version_check() -> DoctorCheck:
    major, minor = sys.version_info[:2]
    if (major, minor) == (3, 10):
        return DoctorCheck("python", "PASS", f"using supported Python {major}.{minor}")
    return DoctorCheck(
        "python",
        "FAIL",
        f"expected Python 3.10.x, got {major}.{minor}",
    )


def _device_policy_check(default_device: str) -> DoctorCheck:
    return DoctorCheck("device", "PASS", f"default device policy is '{default_device}'")


def _mutable_directory_check(name: str, path: Path) -> DoctorCheck:
    if path.exists() and path.is_dir():
        return DoctorCheck(name, "PASS", f"{path} exists")
    if _has_existing_ancestor(path):
        return DoctorCheck(
            name,
            "WARN",
            f"{path} is not created yet; an existing ancestor directory is available",
        )
    return DoctorCheck(name, "FAIL", f"{path} cannot be created because no ancestor path is available")


def _has_existing_ancestor(path: Path) -> bool:
    current = path if path.is_absolute() else Path(".").joinpath(path)
    for candidate in (current,) + tuple(current.parents):
        if candidate.exists():
            return True
    return False


def _optional_external_path_check(name: str, path: Path | None) -> DoctorCheck:
    if path is None:
        return DoctorCheck(name, "WARN", "not configured yet; optional during Phase 1")
    if not path.exists():
        return DoctorCheck(name, "FAIL", f"{path} does not exist")
    if not path.is_dir():
        return DoctorCheck(name, "FAIL", f"{path} is not a directory")
    return DoctorCheck(name, "PASS", f"{path} exists")
