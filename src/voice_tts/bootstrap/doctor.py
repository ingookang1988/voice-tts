from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from voice_tts.exceptions import ManifestError
from voice_tts.infrastructure.config import Settings
from voice_tts.infrastructure.gpt_sovits import is_yaml_like_path, shallow_import_tts_module
from voice_tts.infrastructure.repositories import JsonModelProfileRepository
from voice_tts.infrastructure.system import find_ffmpeg_executable


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
    repository = JsonModelProfileRepository(settings.model_manifest)
    checks: list[DoctorCheck] = [
        _python_version_check(),
        _device_policy_check(settings.default_device),
        _mutable_directory_check("workdir", settings.workdir),
        _mutable_directory_check("temp_root", settings.temp_root),
        _mutable_directory_check("output_root", settings.output_root),
        _required_external_path_check("gpt_sovits_root", settings.gpt_sovits_root),
        _ffmpeg_check(),
    ]

    manifest_check, profiles = _manifest_check(repository)
    checks.append(manifest_check)
    checks.extend(_profile_checks(settings, profiles))
    return DoctorReport(settings=settings, checks=tuple(checks))


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


def _required_external_path_check(name: str, path: Path | None) -> DoctorCheck:
    if path is None:
        return DoctorCheck(name, "FAIL", "required for Phase 3 synthesize but not configured")
    if not path.exists():
        return DoctorCheck(name, "FAIL", f"{path} does not exist")
    if not path.is_dir():
        return DoctorCheck(name, "FAIL", f"{path} is not a directory")
    return DoctorCheck(name, "PASS", f"{path} exists")


def _ffmpeg_check() -> DoctorCheck:
    ffmpeg = find_ffmpeg_executable()
    if ffmpeg is None:
        return DoctorCheck(
            "ffmpeg",
            "FAIL",
            "ffmpeg was not found on PATH; install it before running synthesize",
        )
    return DoctorCheck("ffmpeg", "PASS", f"{ffmpeg} is available")


def _manifest_check(
    repository: JsonModelProfileRepository,
) -> tuple[DoctorCheck, tuple]:
    try:
        profiles = repository.list_profiles()
    except ManifestError as exc:
        return DoctorCheck("model_manifest", "FAIL", str(exc)), ()

    return DoctorCheck(
        "model_manifest",
        "PASS",
        f"{len(profiles)} profile(s) loaded from {repository.manifest_path}",
    ), profiles


def _profile_checks(settings: Settings, profiles: tuple) -> tuple[DoctorCheck, ...]:
    if not profiles:
        return ()

    import_ok = False
    import_detail = "upstream import skipped because checkout root is unavailable"
    if settings.gpt_sovits_root is not None and settings.gpt_sovits_root.exists() and settings.gpt_sovits_root.is_dir():
        try:
            shallow_import_tts_module(settings.gpt_sovits_root)
            import_ok = True
            import_detail = "upstream TTS module import succeeded"
        except Exception as exc:
            import_detail = f"upstream import failed: {exc}"

    checks: list[DoctorCheck] = []
    for profile in profiles:
        fail_reasons: list[str] = []
        warn_reasons: list[str] = list(profile.normalization_warnings)

        if not profile.tts_config_path.exists():
            fail_reasons.append(f"config path is missing: {profile.tts_config_path}")
        elif not profile.tts_config_path.is_file():
            fail_reasons.append(f"config path is not a file: {profile.tts_config_path}")
        elif not is_yaml_like_path(profile.tts_config_path):
            fail_reasons.append(f"config path is not a YAML file: {profile.tts_config_path}")

        if settings.default_device not in profile.compatibility.supported_devices:
            fail_reasons.append(
                f"default device '{settings.default_device}' is not supported by this profile"
            )

        if settings.gpt_sovits_root is None or not settings.gpt_sovits_root.exists() or not settings.gpt_sovits_root.is_dir():
            fail_reasons.append("checkout root is unavailable")
        else:
            missing_checkout_files = [
                str(settings.gpt_sovits_root / relative_path)
                for relative_path in profile.compatibility.required_checkout_files
                if not (settings.gpt_sovits_root / relative_path).exists()
            ]
            if missing_checkout_files:
                fail_reasons.append("missing checkout files: " + ", ".join(missing_checkout_files))

        if not import_ok:
            fail_reasons.append(import_detail)

        detail_prefix = (
            f"display='{profile.display_name}', languages={','.join(profile.languages)}, "
            f"devices={','.join(profile.compatibility.supported_devices)}"
        )
        if fail_reasons:
            checks.append(
                DoctorCheck(
                    name=f"profile:{profile.id}",
                    status="FAIL",
                    detail=detail_prefix + "; " + "; ".join(fail_reasons),
                )
            )
            continue

        if warn_reasons:
            checks.append(
                DoctorCheck(
                    name=f"profile:{profile.id}",
                    status="WARN",
                    detail=detail_prefix + "; " + "; ".join(warn_reasons),
                )
            )
            continue

        checks.append(
            DoctorCheck(
                name=f"profile:{profile.id}",
                status="PASS",
                detail=detail_prefix + "; " + import_detail,
            )
        )
    return tuple(checks)
