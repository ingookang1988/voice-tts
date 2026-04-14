from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError

from voice_tts import __version__
from voice_tts.application.dto import SynthesizeSpeechCommand
from voice_tts.bootstrap.container import build_container
from voice_tts.bootstrap.doctor import DoctorReport, run_doctor
from voice_tts.exceptions import VoiceTtsError

app = typer.Typer(
    add_completion=False,
    help="Local-first CLI for the voice-tts GPT-SoVITS toolkit.",
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


@app.command()
def synthesize(
    model_profile: str = typer.Option(..., "--model-profile", help="Model profile id from the manifest."),
    text: str = typer.Option(..., "--text", help="Target text to synthesize."),
    text_lang: str = typer.Option(..., "--text-lang", help="Language code for the target text."),
    ref_audio: Path = typer.Option(..., "--ref-audio", help="Reference audio path for zero-shot voice cloning."),
    prompt_text: str = typer.Option(..., "--prompt-text", help="Prompt transcript that matches the reference audio."),
    prompt_lang: str = typer.Option(..., "--prompt-lang", help="Language code for the prompt transcript."),
    ref_start_sec: float | None = typer.Option(None, "--ref-start-sec", help="Optional trim start in seconds."),
    ref_end_sec: float | None = typer.Option(None, "--ref-end-sec", help="Optional trim end in seconds."),
    output: Path | None = typer.Option(None, "--output", help="Optional output WAV path."),
    top_p: float = typer.Option(1.0, "--top-p", help="Sampling top_p passed to GPT-SoVITS."),
    temperature: float = typer.Option(1.0, "--temperature", help="Sampling temperature passed to GPT-SoVITS."),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing explicit output file."),
) -> None:
    """Run local GPT-SoVITS synthesis and emit a WAV file."""

    try:
        container = build_container()
        command = SynthesizeSpeechCommand(
            model_profile_id=model_profile,
            text=text,
            text_lang=text_lang,
            ref_audio_path=ref_audio,
            ref_start_sec=ref_start_sec,
            ref_end_sec=ref_end_sec,
            prompt_text=prompt_text,
            prompt_lang=prompt_lang,
            output_path=output,
            top_p=top_p,
            temperature=temperature,
            force=force,
        )
        result = container.synthesize_speech.execute(command)
    except ValidationError as exc:
        typer.secho("Configuration validation failed.", fg=typer.colors.RED, err=True)
        for error in exc.errors():
            location = ".".join(str(part) for part in error["loc"])
            typer.echo(f"- {location}: {error['msg']}", err=True)
        raise typer.Exit(code=1)
    except VoiceTtsError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    typer.secho(f"generated wav: {result.audio_path}", fg=typer.colors.GREEN)
    typer.echo(f"sample_rate: {result.sample_rate}")


def _print_doctor_report(report: DoctorReport) -> None:
    typer.echo("voice-tts doctor")
    typer.echo(f"  environment: {report.settings.env}")
    typer.echo(f"  device: {report.settings.default_device}")
    typer.echo(f"  workdir: {_format_path(report.settings.workdir)}")
    typer.echo(f"  temp_root: {_format_path(report.settings.temp_root)}")
    typer.echo(f"  output_root: {_format_path(report.settings.output_root)}")
    typer.echo(f"  model_manifest: {_format_path(report.settings.model_manifest)}")
    typer.echo(f"  gpt_sovits_root: {_format_path(report.settings.gpt_sovits_root)}")

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
