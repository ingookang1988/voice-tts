from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from voice_tts.domain.entities import AudioSourceMetadata, ReferenceClipCandidate
from voice_tts.exceptions import (
    VoiceTtsDependencyError,
    VoiceTtsSynthesisError,
    VoiceTtsUsageError,
    with_stage,
)
from voice_tts.infrastructure.system import find_ffmpeg_executable, find_ffprobe_executable


SILENCE_START_PATTERN = re.compile(r"silence_start:\s*([0-9]+(?:\.[0-9]+)?)")
SILENCE_END_PATTERN = re.compile(r"silence_end:\s*([0-9]+(?:\.[0-9]+)?)")
SILENCE_GAP_THRESHOLD_SEC = 0.25
MIN_REFERENCE_DURATION_SEC = 3.0
MAX_REFERENCE_DURATION_SEC = 10.0
TARGET_REFERENCE_DURATION_SEC = 6.0
MAX_REFERENCE_CANDIDATES = 3


class FfmpegReferenceAudioPreparationService:
    """Inspect, analyze, and export local reference-audio clips using ffmpeg/ffprobe."""

    def inspect(self, input_path: Path) -> AudioSourceMetadata:
        _validate_source_audio_path(input_path)
        ffprobe = find_ffprobe_executable()
        if ffprobe is None:
            raise VoiceTtsDependencyError(
                with_stage("preflight", "ffprobe was not found on PATH; install ffmpeg before using prepare-ref")
            )

        command = [
            str(ffprobe),
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(input_path),
        ]
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip() or "unknown ffprobe error"
            raise VoiceTtsSynthesisError(
                with_stage("trim", f"ffprobe failed to inspect source audio: {detail}")
            )

        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise VoiceTtsSynthesisError(
                with_stage("trim", f"ffprobe returned invalid JSON: {exc.msg}")
            ) from exc

        streams = payload.get("streams")
        if not isinstance(streams, list):
            raise VoiceTtsSynthesisError(with_stage("trim", "ffprobe did not return stream metadata"))
        audio_stream = next(
            (stream for stream in streams if isinstance(stream, dict) and stream.get("codec_type") == "audio"),
            None,
        )
        if audio_stream is None:
            raise VoiceTtsUsageError(with_stage("preflight", f"input audio has no audio stream: {input_path}"))

        format_payload = payload.get("format") if isinstance(payload.get("format"), dict) else {}
        duration_sec = _parse_positive_float(
            audio_stream.get("duration", format_payload.get("duration")),
            field_name="duration",
        )
        sample_rate = _parse_optional_positive_int(audio_stream.get("sample_rate"))
        channels = _parse_optional_positive_int(audio_stream.get("channels"))
        format_name = _normalize_optional_text(audio_stream.get("codec_name"))
        container_name = _normalize_optional_text(format_payload.get("format_name"))

        return AudioSourceMetadata(
            duration_sec=duration_sec,
            sample_rate=sample_rate,
            channels=channels,
            format_name=format_name,
            container_name=container_name,
        )

    def suggest_segments(
        self,
        input_path: Path,
        metadata: AudioSourceMetadata,
    ) -> tuple[ReferenceClipCandidate, ...]:
        _validate_source_audio_path(input_path)
        ffmpeg = find_ffmpeg_executable()
        if ffmpeg is None:
            raise VoiceTtsDependencyError(
                with_stage("preflight", "ffmpeg was not found on PATH; install it before using prepare-ref")
            )

        command = [
            str(ffmpeg),
            "-hide_banner",
            "-i",
            str(input_path),
            "-af",
            "silencedetect=noise=-35dB:d=0.2",
            "-f",
            "null",
            "-",
        ]
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip() or "unknown ffmpeg error"
            raise VoiceTtsSynthesisError(
                with_stage("trim", f"ffmpeg failed to analyze source audio: {detail}")
            )

        spans = derive_non_silent_spans(completed.stderr, metadata.duration_sec)
        merged_spans = merge_reference_spans(spans)
        ranked = rank_reference_spans(merged_spans)
        return tuple(
            ReferenceClipCandidate(start_sec=start_sec, end_sec=end_sec)
            for start_sec, end_sec in ranked[:MAX_REFERENCE_CANDIDATES]
        )

    def export_segment(
        self,
        input_path: Path,
        output_path: Path,
        segment: ReferenceClipCandidate,
    ) -> Path:
        return export_audio_clip(
            input_path=input_path,
            output_path=output_path,
            start_sec=segment.start_sec,
            end_sec=segment.end_sec,
        )


def export_audio_clip(
    input_path: Path,
    output_path: Path,
    start_sec: float,
    end_sec: float | None,
) -> Path:
    _validate_source_audio_path(input_path)
    if start_sec < 0.0:
        raise VoiceTtsUsageError(with_stage("preflight", "start_sec must be >= 0.0"))
    if end_sec is not None and end_sec <= start_sec:
        raise VoiceTtsUsageError(with_stage("preflight", "end_sec must be greater than start_sec"))

    ffmpeg = find_ffmpeg_executable()
    if ffmpeg is None:
        raise VoiceTtsDependencyError(
            with_stage("trim", "ffmpeg was not found on PATH; install ffmpeg before exporting audio clips")
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(ffmpeg),
        "-y",
        "-i",
        str(input_path),
        "-ss",
        f"{start_sec:.3f}",
    ]
    if end_sec is not None:
        duration_sec = end_sec - start_sec
        command.extend(["-t", f"{duration_sec:.3f}"])
    command.extend(
        [
            "-vn",
            "-acodec",
            "pcm_s16le",
            str(output_path),
        ]
    )
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "unknown ffmpeg error"
        raise VoiceTtsSynthesisError(
            with_stage("trim", f"ffmpeg failed to trim reference audio: {detail}")
        )
    return output_path


def derive_non_silent_spans(silence_output: str, total_duration_sec: float) -> tuple[tuple[float, float], ...]:
    silence_events: list[tuple[str, float]] = []
    for line in silence_output.splitlines():
        silence_start_match = SILENCE_START_PATTERN.search(line)
        if silence_start_match is not None:
            silence_events.append(("start", float(silence_start_match.group(1))))
        silence_end_match = SILENCE_END_PATTERN.search(line)
        if silence_end_match is not None:
            silence_events.append(("end", float(silence_end_match.group(1))))

    spans: list[tuple[float, float]] = []
    current_start = 0.0
    in_silence = False
    for event_type, timestamp in silence_events:
        clamped_timestamp = min(max(timestamp, 0.0), total_duration_sec)
        if event_type == "start":
            if not in_silence and clamped_timestamp > current_start:
                spans.append((current_start, clamped_timestamp))
            in_silence = True
        else:
            current_start = clamped_timestamp
            in_silence = False

    if not in_silence and total_duration_sec > current_start:
        spans.append((current_start, total_duration_sec))
    return tuple(
        (start_sec, end_sec)
        for start_sec, end_sec in spans
        if end_sec > start_sec
    )


def merge_reference_spans(spans: tuple[tuple[float, float], ...]) -> tuple[tuple[float, float], ...]:
    if not spans:
        return ()

    merged: list[list[float]] = [[spans[0][0], spans[0][1]]]
    for start_sec, end_sec in spans[1:]:
        previous_start, previous_end = merged[-1]
        if start_sec - previous_end < SILENCE_GAP_THRESHOLD_SEC:
            merged[-1][1] = max(previous_end, end_sec)
        else:
            merged.append([start_sec, end_sec])

    return tuple((start_sec, end_sec) for start_sec, end_sec in merged)


def rank_reference_spans(spans: tuple[tuple[float, float], ...]) -> tuple[tuple[float, float], ...]:
    filtered = [
        (start_sec, end_sec)
        for start_sec, end_sec in spans
        if MIN_REFERENCE_DURATION_SEC <= (end_sec - start_sec) <= MAX_REFERENCE_DURATION_SEC
    ]
    filtered.sort(
        key=lambda span: (
            abs((span[1] - span[0]) - TARGET_REFERENCE_DURATION_SEC),
            span[0],
        )
    )
    return tuple(filtered)


def _validate_source_audio_path(input_path: Path) -> None:
    if not input_path.exists():
        raise VoiceTtsUsageError(with_stage("preflight", f"input audio was not found: {input_path}"))
    if not input_path.is_file():
        raise VoiceTtsUsageError(with_stage("preflight", f"input audio is not a file: {input_path}"))


def _parse_positive_float(raw_value: object, *, field_name: str) -> float:
    try:
        value = float(str(raw_value))
    except (TypeError, ValueError) as exc:
        raise VoiceTtsSynthesisError(
            with_stage("trim", f"ffprobe returned an invalid {field_name} value")
        ) from exc
    if value <= 0.0:
        raise VoiceTtsSynthesisError(with_stage("trim", f"ffprobe returned a non-positive {field_name} value"))
    return value


def _parse_optional_positive_int(raw_value: object) -> int | None:
    if raw_value in (None, ""):
        return None
    try:
        value = int(str(raw_value))
    except (TypeError, ValueError) as exc:
        raise VoiceTtsSynthesisError(
            with_stage("trim", "ffprobe returned an invalid integer metadata value")
        ) from exc
    return value if value > 0 else None


def _normalize_optional_text(raw_value: object) -> str | None:
    if raw_value is None:
        return None
    normalized = str(raw_value).strip()
    return normalized or None
