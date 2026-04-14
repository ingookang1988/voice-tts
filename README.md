# voice-tts

`voice-tts` is a local-first GPT-SoVITS toolkit for Windows-oriented TTS work.

Phase 4a is now landed. The repo provides:

- a `uv`-managed Python project
- a `src/voice_tts` package with Clean Architecture seams
- a typed model profile catalog with Hybrid Warn manifest normalization
- a local CLI with `version`, `init`, `doctor`, `profiles`, `prepare-ref`, and `synthesize`
- first-run workspace scaffolding for `.env` and a seeded manifest
- a GPT-SoVITS v2 adapter that imports an external checkout
- silence-based reference-audio inspection, ranking, and WAV export
- zero-shot reference-audio synthesis with optional manual trim
- richer diagnostics for profile compatibility and synthesis output
- tests for settings, CLI, repositories, use cases, workspace scaffolding, reference-audio parsing, architecture, and adapter smoke

This project is still local-first. It does **not** include FastAPI, Docker, automatic diarization, automatic ASR, automatic VAD, or GPT-SoVITS v3 support.

## Requirements

- Python `3.10.x`
- `uv`
- `ffmpeg` on `PATH`
- an external GPT-SoVITS checkout
- the external GPT-SoVITS runtime requirements installed into the same `.venv`

`voice-tts` does not vendor the full GPT-SoVITS dependency set. Our `.venv` must satisfy both this repo and the referenced GPT-SoVITS checkout.

## Quick Start

```powershell
uv sync --python 3.10
uv run voice-tts init --gpt-sovits-root D:\GPT-SoVITS
```

`init` creates:

- `.env` from `.env.example`
- `.local/model-profiles.json` with a seeded `gsv2-default` profile
- `.local/tmp` and `.local/outputs`

Then check the local runtime and discover the seeded profile:

```powershell
uv run voice-tts version
uv run voice-tts doctor
uv run voice-tts profiles
```

Prepare a reference clip:

```powershell
uv run voice-tts prepare-ref --input D:\clips\session.wav
uv run voice-tts prepare-ref --input D:\clips\session.wav --pick 1
```

Then synthesize:

```powershell
uv run voice-tts synthesize `
  --model-profile gsv2-default `
  --text "안녕하세요" `
  --text-lang ko `
  --ref-audio .local\tmp\ref-clips\session-0p500-6p200.wav `
  --prompt-text "안녕하세요, 반갑습니다." `
  --prompt-lang ko
```

## CLI

### `voice-tts version`

Prints the installed project version.

### `voice-tts init`

Scaffolds `.env`, a seeded manifest, and the default local temp/output directories.

Rules:

- `--gpt-sovits-root` is required
- `--manifest` defaults to `.local/model-profiles.json`
- `--output-root` defaults to `.local/outputs`
- if `.env` or the target manifest already exists, pass `--force` to overwrite it

### `voice-tts doctor`

Runs a compatibility preflight:

- settings load
- Python version policy
- workdir / temp / output path status
- required GPT-SoVITS root status
- `ffmpeg` availability
- model manifest parse and profile count
- profile metadata completeness
- config path existence and YAML shape
- required checkout files under `VOICE_TTS_GPT_SOVITS_ROOT`
- default device compatibility
- shallow upstream import of `GPT_SoVITS.TTS_infer_pack.TTS`

`doctor` exits with:

- `0` when the runtime is healthy or only has warnings
- `1` when there is a blocking compatibility problem

### `voice-tts profiles`

Prints manifest-backed profile metadata for discovery:

- profile id and display name
- languages
- speaker tags
- supported devices
- config path status
- manifest normalization warnings

### `voice-tts prepare-ref`

Inspects source audio, prints metadata, ranks up to 3 candidate speech clips, and can export one as WAV.

```powershell
uv run voice-tts prepare-ref --input D:\clips\session.wav
uv run voice-tts prepare-ref --input D:\clips\session.wav --pick 1
uv run voice-tts prepare-ref --input D:\clips\session.wav --start-sec 1.2 --end-sec 6.8
```

Rules:

- source metadata always includes duration, sample rate, channels, format, and container
- if no explicit range is provided, silence-based analysis ranks up to 3 candidates
- `--pick` chooses a ranked candidate and exports it to WAV
- `--start-sec` and `--end-sec` export that exact range and cannot be combined with `--pick`
- default export path is `.local/tmp/ref-clips/<source-stem>-<start>-<end>.wav`
- if the output file already exists, pass `--force` to overwrite it

### `voice-tts synthesize`

Runs local GPT-SoVITS v2 zero-shot synthesis and writes a WAV file.

```powershell
uv run voice-tts synthesize `
  --model-profile gsv2-default `
  --text "안녕하세요" `
  --text-lang ko `
  --ref-audio D:\clips\sample.wav `
  --ref-start-sec 1.2 `
  --ref-end-sec 6.8 `
  --prompt-text "안녕하세요, 반갑습니다." `
  --prompt-lang ko
```

Rules:

- `--model-profile`, `--text`, `--text-lang`, `--ref-audio`, `--prompt-text`, `--prompt-lang` are required
- `--ref-start-sec` and `--ref-end-sec` are optional manual trim controls
- output is always WAV
- if `--output` is omitted, the file is written under `.local/outputs/<model-profile>/...wav`
- if `--output` already exists, pass `--force` to overwrite it

Success output always includes:

- generated wav path
- sample rate
- resolved profile id and display name
- resolved config path
- resolved reference audio path
- trim applied 여부
- elapsed time
- selected device
- fp16 usage

Deterministic failures use stage prefixes:

- `[manifest]`
- `[preflight]`
- `[import]`
- `[trim]`
- `[synthesis]`
- `[output]`

## Tests

Default tests stay green without external model assets:

```powershell
uv run pytest
```

Opt-in external smoke is available when a real GPT-SoVITS checkout and reference audio are configured:

```powershell
uv run pytest -m external
```

## Layout

```text
config/
src/voice_tts/
  application/
  bootstrap/
  domain/
  infrastructure/
  cli.py
tests/
.voice-tts/
```

## Next Focus

Phase 4b planning is now centered on:

- optional service adapter evaluation
- richer runtime observability
- keeping the local CLI path as the canonical debugging surface
