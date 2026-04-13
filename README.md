# voice-tts

`voice-tts` is a local-first GPT-SoVITS bootstrap project for Windows RTX 4080 environments.

Phase 1 is intentionally small. It provides:

- a `uv`-managed Python project
- a `src/voice_tts` package with Clean Architecture seams
- a local CLI entrypoint
- a `doctor` self-check command
- tests for settings, CLI, and architecture boundaries

Phase 1 does **not** include real GPT-SoVITS inference, WAV generation, FastAPI, Docker, or a web API. Those are deferred to Phase 2 and beyond.

## Requirements

- Python `3.10.x`
- `uv`

## Quick Start

```powershell
uv sync --python 3.10
uv run voice-tts version
uv run voice-tts doctor
uv run pytest
```

## CLI

### `voice-tts version`

Prints the installed project version.

### `voice-tts doctor`

Runs a local bootstrap self-check:

- settings load
- Python version policy
- workdir / temp path status
- optional GPT-SoVITS and weights path status
- device policy status

`doctor` exits with:

- `0` when the bootstrap is healthy or only has Phase 1 warnings
- `1` when there is a blocking configuration problem

## Layout

```text
src/voice_tts/
  application/
  bootstrap/
  domain/
  infrastructure/
  cli.py
tests/
.voice-tts/
```

## Phase 2 Preview

Phase 2 will plug GPT-SoVITS into the existing seams:

- `SpeechSynthesisEngine`
- `WeightRepository`
- `SynthesizeSpeechUseCase`

and then add a real local synthesis command.

