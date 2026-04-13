from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError

from voice_tts import __version__
from voice_tts.bootstrap.container import build_container
from voice_tts.bootstrap.doctor import DoctorReport, run_doctor

app = typer.Typer(
    add_completion=False,
    help="Local-first CLI for the voice-tts bootstrap project.",
)


def _report_color(status: str) -> str:
    if status == "PASS":
        return typer.colors.GREEN
    if status == "WARN":
        return typer.colors.YELLOW
    return typer.colors.RED


def _format_path(path: Path | None) -> str:
    if path is None:
        return "(unset)"
    return str(path)


@app.command()
def version() -> None:
    """Print the installed project version."""

    typer.echo(f"voice-tts {__version__}")


@app.command()
def doctor() -> None:
    """Run a local bootstrap self-check."""

    try:
        container = build_container()
    except ValidationError as exc:
        typer.secho("Configuration validation failed.", fg=typer.colors.RED, err=True)
        for error in exc.errors():
            location = ".".join(str(part) for part in error["loc"])
            typer.echo(f"- {location}: {error['msg']}", err=True)
        raise typer.Exit(code=1)

    report = run_doctor(container.settings)
    _print_doctor_report(report)
    raise typer.Exit(code=0 if report.ok else 1)


def _print_doctor_report(report: DoctorReport) -> None:
    typer.echo("voice-tts doctor")
    typer.echo(f"  environment: {report.settings.env}")
    typer.echo(f"  device: {report.settings.default_device}")
    typer.echo(f"  workdir: {_format_path(report.settings.workdir)}")
    typer.echo(f"  temp_root: {_format_path(report.settings.temp_root)}")

    for check in report.checks:
        typer.secho(
            f"[{check.status}] {check.name}: {check.detail}",
            fg=_report_color(check.status),
        )

    summary = (
        f"doctor passed: {report.pass_count} pass, {report.warn_count} warn, {report.fail_count} fail"
        if report.ok
        else f"doctor failed: {report.pass_count} pass, {report.warn_count} warn, {report.fail_count} fail"
    )
    typer.secho(summary, fg=typer.colors.GREEN if report.ok else typer.colors.RED)
