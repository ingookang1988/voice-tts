from __future__ import annotations

import subprocess
from pathlib import Path

from voice_tts.domain.entities import AudioSourceMetadata
from voice_tts.infrastructure.reference_audio import (
    FfmpegReferenceAudioPreparationService,
    derive_non_silent_spans,
    export_audio_clip,
    merge_reference_spans,
    rank_reference_spans,
)


def test_derive_non_silent_spans_from_ffmpeg_silence_output() -> None:
    silence_output = "\n".join(
        [
            "[silencedetect] silence_start: 0.0",
            "[silencedetect] silence_end: 0.8 | silence_duration: 0.8",
            "[silencedetect] silence_start: 6.5",
            "[silencedetect] silence_end: 7.0 | silence_duration: 0.5",
            "[silencedetect] silence_start: 13.2",
        ]
    )

    spans = derive_non_silent_spans(silence_output, total_duration_sec=18.0)

    assert spans == ((0.8, 6.5), (7.0, 13.2))


def test_merge_reference_spans_merges_small_gaps() -> None:
    merged = merge_reference_spans(((0.0, 4.0), (4.1, 6.0), (7.0, 10.0)))

    assert merged == ((0.0, 6.0), (7.0, 10.0))


def test_rank_reference_spans_filters_and_orders_by_target_duration() -> None:
    ranked = rank_reference_spans(((0.0, 2.0), (2.0, 8.2), (9.0, 15.0), (16.0, 27.5)))

    assert ranked == ((9.0, 15.0), (2.0, 8.2))


def test_reference_audio_service_inspects_metadata(monkeypatch, tmp_path: Path) -> None:
    source_audio = tmp_path / "source.wav"
    source_audio.write_bytes(b"RIFF")
    service = FfmpegReferenceAudioPreparationService()

    monkeypatch.setattr(
        "voice_tts.infrastructure.reference_audio.find_ffprobe_executable",
        lambda: Path("C:/ffmpeg/bin/ffprobe.exe"),
    )
    monkeypatch.setattr(
        "voice_tts.infrastructure.reference_audio.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout=(
                '{"streams":[{"codec_type":"audio","codec_name":"pcm_s16le","sample_rate":"48000","channels":1,'
                '"duration":"12.5"}],"format":{"format_name":"wav","duration":"12.5"}}'
            ),
            stderr="",
        ),
    )

    metadata = service.inspect(source_audio)

    assert metadata == AudioSourceMetadata(
        duration_sec=12.5,
        sample_rate=48000,
        channels=1,
        format_name="pcm_s16le",
        container_name="wav",
    )


def test_reference_audio_service_suggests_top_three_ranked_candidates(monkeypatch, tmp_path: Path) -> None:
    source_audio = tmp_path / "source.wav"
    source_audio.write_bytes(b"RIFF")
    service = FfmpegReferenceAudioPreparationService()

    monkeypatch.setattr(
        "voice_tts.infrastructure.reference_audio.find_ffmpeg_executable",
        lambda: Path("C:/ffmpeg/bin/ffmpeg.exe"),
    )
    monkeypatch.setattr(
        "voice_tts.infrastructure.reference_audio.subprocess.run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args=args,
            returncode=0,
            stdout="",
            stderr="\n".join(
                [
                    "[silencedetect] silence_start: 0.0",
                    "[silencedetect] silence_end: 0.5 | silence_duration: 0.5",
                    "[silencedetect] silence_start: 6.4",
                    "[silencedetect] silence_end: 7.0 | silence_duration: 0.6",
                    "[silencedetect] silence_start: 13.4",
                    "[silencedetect] silence_end: 14.0 | silence_duration: 0.6",
                ]
            ),
        ),
    )

    candidates = service.suggest_segments(
        source_audio,
        AudioSourceMetadata(
            duration_sec=20.0,
            sample_rate=48000,
            channels=1,
            format_name="pcm_s16le",
            container_name="wav",
        ),
    )

    assert len(candidates) == 3
    assert candidates[0].start_sec == 14.0
    assert candidates[0].end_sec == 20.0
    assert candidates[1].start_sec == 0.5
    assert candidates[2].start_sec == 7.0


def test_export_audio_clip_runs_ffmpeg(monkeypatch, tmp_path: Path) -> None:
    source_audio = tmp_path / "source.wav"
    source_audio.write_bytes(b"RIFF")
    output_path = tmp_path / "clip.wav"
    calls: list[list[str]] = []

    monkeypatch.setattr(
        "voice_tts.infrastructure.reference_audio.find_ffmpeg_executable",
        lambda: Path("C:/ffmpeg/bin/ffmpeg.exe"),
    )

    def _fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(args=command, returncode=0, stdout="", stderr="")

    monkeypatch.setattr("voice_tts.infrastructure.reference_audio.subprocess.run", _fake_run)

    exported = export_audio_clip(source_audio, output_path, start_sec=1.0, end_sec=7.0)

    assert exported == output_path
    assert "-ss" in calls[0]
    assert "-t" in calls[0]
