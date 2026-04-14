from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError

from voice_tts import __version__
from voice_tts.application.dto import PrepareReferenceAudioCommand, SynthesizeSpeechCommand
from voice_tts.bootstrap.container import build_container
from voice_tts.bootstrap.doctor import DoctorReport, run_doctor
from voice_tts.exceptions import VoiceTtsError
from voice_tts.infrastructure.workspace import initialize_workspace

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
def init(
    gpt_sovits_root: Path = typer.Option(..., "--gpt-sovits-root", help="Path to the external GPT-SoVITS checkout."),
    manifest: Path = typer.Option(Path(".local/model-profiles.json"), "--manifest", help="Manifest path to create."),
    output_root: Path = typer.Option(Path(".local/outputs"), "--output-root", help="Default output root for generated WAV files."),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing .env or manifest."),
) -> None:
    """Scaffold the local .env and model manifest for a first run."""

    try:
        result = initialize_workspace(
            gpt_sovits_root=gpt_sovits_root,
            manifest_path=manifest,
            output_root=output_root,
            force=force,
        )
    except VoiceTtsError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    typer.echo("voice-tts init")
    typer.echo(f"env_path: {result.env_path}")
    typer.echo(f"manifest_path: {result.manifest_path}")
    typer.echo(f"output_root: {result.output_root}")
    typer.echo(f"seeded_profile: {result.profile_id}")
    typer.echo("next_step: run `uv run voice-tts doctor`")


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
def profiles() -> None:
    """List manifest-backed model profiles for local discovery."""

    try:
        container = build_container()
        profiles = container.model_profile_repository.list_profiles()
    except ValidationError as exc:
        typer.secho("Configuration validation failed.", fg=typer.colors.RED, err=True)
        for error in exc.errors():
            location = ".".join(str(part) for part in error["loc"])
            typer.echo(f"- {location}: {error['msg']}", err=True)
        raise typer.Exit(code=1)
    except VoiceTtsError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    typer.echo("voice-tts profiles")
    for profile in profiles:
        config_status = "present" if profile.tts_config_path.exists() and profile.tts_config_path.is_file() else "missing"
        typer.echo(f"- {profile.id}: {profile.display_name}")
        typer.echo(f"  languages: {', '.join(profile.languages)}")
        typer.echo(f"  speaker_tags: {', '.join(profile.speaker_tags) if profile.speaker_tags else '(none)'}")
        typer.echo(f"  supported_devices: {', '.join(profile.compatibility.supported_devices)}")
        typer.echo(f"  config_path: {profile.tts_config_path} ({config_status})")
        typer.echo(
            "  normalization_warnings: "
            + (", ".join(profile.normalization_warnings) if profile.normalization_warnings else "(none)")
        )


@app.command("prepare-ref")
def prepare_ref(
    input: Path = typer.Option(..., "--input", help="Input audio file to inspect and optionally export."),
    start_sec: float | None = typer.Option(None, "--start-sec", help="Explicit trim start in seconds."),
    end_sec: float | None = typer.Option(None, "--end-sec", help="Explicit trim end in seconds."),
    pick: int | None = typer.Option(None, "--pick", help="1-based ranked candidate to export."),
    output: Path | None = typer.Option(None, "--output", help="Optional prepared WAV output path."),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing exported clip."),
) -> None:
    """Inspect, rank, and optionally export a reference-audio clip."""

    try:
        container = build_container()
        command = PrepareReferenceAudioCommand(
            input_path=input,
            start_sec=start_sec,
            end_sec=end_sec,
            pick=pick,
            output_path=output,
            force=force,
        )
        result = container.prepare_reference_audio.execute(command)
    except ValidationError as exc:
        typer.secho("Configuration validation failed.", fg=typer.colors.RED, err=True)
        for error in exc.errors():
            location = ".".join(str(part) for part in error["loc"])
            typer.echo(f"- {location}: {error['msg']}", err=True)
        raise typer.Exit(code=1)
    except VoiceTtsError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    _print_prepare_reference_result(result)


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

    _print_synthesis_result(result)


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


def _print_synthesis_result(result) -> None:
    typer.secho(f"generated wav: {result.audio_path}", fg=typer.colors.GREEN)
    typer.echo(f"sample_rate: {result.sample_rate}")

    profile_label = result.metadata.get(
        "profile_display_name",
        result.metadata.get("model_profile_id", "(unknown)"),
    )
    profile_id = result.metadata.get("model_profile_id", "(unknown)")
    typer.echo(f"profile: {profile_id} ({profile_label})")
    typer.echo("config_path: " + result.metadata.get("resolved_tts_config_path", "(unknown)"))
    typer.echo("resolved_ref_audio: " + result.metadata.get("resolved_ref_audio_path", "(unknown)"))
    typer.echo("trim_applied: " + result.metadata.get("trim_applied", "(unknown)"))
    typer.echo("elapsed_ms: " + result.metadata.get("elapsed_ms", "(unknown)"))
    typer.echo("device: " + result.metadata.get("device", "(unknown)"))
    typer.echo("use_fp16: " + result.metadata.get("use_fp16", "(unknown)"))


def _print_prepare_reference_result(result) -> None:
    typer.echo("voice-tts prepare-ref")
    typer.echo(f"source_audio: {result.source_path}")
    typer.echo(f"duration_sec: {_format_seconds(result.duration_sec)}")
    typer.echo(f"sample_rate: {result.sample_rate if result.sample_rate is not None else '(unknown)'}")
    typer.echo(f"channels: {result.channels if result.channels is not None else '(unknown)'}")
    typer.echo(f"format: {result.format_name or '(unknown)'}")
    typer.echo(f"container: {result.container_name or '(unknown)'}")

    if result.candidates:
        typer.echo("candidate_segments:")
        for candidate in result.candidates:
            typer.echo(
                f"  {candidate.index}. {_format_seconds(candidate.start_sec)} -> {_format_seconds(candidate.end_sec)} "
                f"({_format_seconds(candidate.duration_sec)}s)"
            )
    else:
        typer.echo("candidate_segments: none found")

    if result.exported_clip_path is not None:
        typer.secho(f"prepared_ref_audio: {result.exported_clip_path}", fg=typer.colors.GREEN)
        if result.selected_candidate is not None:
            typer.echo(
                "selected_range: "
                f"{_format_seconds(result.selected_candidate.start_sec)} -> {_format_seconds(result.selected_candidate.end_sec)} "
                f"({_format_seconds(result.selected_candidate.duration_sec)}s)"
            )


def _format_seconds(value: float) -> str:
    return f"{value:.3f}"
