# voice-tts

`voice-tts` is a local-first GPT-SoVITS toolkit for Windows-oriented TTS work.

Phase 3 is now landed. The repo provides:

- a `uv`-managed Python project
- a `src/voice_tts` package with Clean Architecture seams
- a typed model profile catalog with Hybrid Warn manifest normalization
- a local CLI with `version`, `doctor`, and `synthesize`
- a GPT-SoVITS v2 adapter that imports an external checkout
- zero-shot reference-audio synthesis with optional manual trim
- richer diagnostics for profile compatibility and synthesis output
- tests for settings, CLI, repositories, use cases, architecture, and adapter smoke

This project is still local-first. It does **not** include FastAPI, Docker, automatic diarization, automatic ASR, automatic VAD, reference-audio assist automation, or GPT-SoVITS v3 support.

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
Copy-Item .env.example .env
```

Set at least these values in `.env`:

```dotenv
VOICE_TTS_GPT_SOVITS_ROOT=D:/GPT-SoVITS
VOICE_TTS_MODEL_MANIFEST=.local/model-profiles.json
VOICE_TTS_OUTPUT_ROOT=.local/outputs
```

Create a manifest based on [`config/model-profiles.example.json`](config/model-profiles.example.json):

```json
{
  "profiles": [
    {
      "id": "gsv2-default",
      "display_name": "Korean Zero-Shot",
      "version": "gpt-sovits-v2",
      "tts_config_path": "D:/GPT-SoVITS/GPT_SoVITS/configs/tts_infer.yaml",
      "languages": ["ko", "en"],
      "speaker_tags": ["female", "studio"],
      "notes": "Reference profile for zero-shot local synthesis on a GPT-SoVITS v2 checkout.",
      "compatibility": {
        "required_checkout_files": ["GPT_SoVITS/TTS_infer_pack/TTS.py"],
        "supported_devices": ["auto", "cpu", "cuda"]
      }
    }
  ]
}
```

Legacy Phase 2 manifests still load, but `voice-tts doctor` will mark them with `WARN` because default metadata had to be filled in.

Then check the local runtime:

```powershell
uv run voice-tts version
uv run voice-tts doctor
```

## CLI

### `voice-tts version`

Prints the installed project version.

### `voice-tts doctor`

Runs a Phase 3 compatibility preflight:

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

Phase 4 planning is now centered on:

- reference-audio assist beyond manual trim
- optional service adapter evaluation
- keeping the local CLI path as the canonical debugging surface
