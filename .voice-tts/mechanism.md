# voice-tts Mechanism (V2)

- Role: 현재 저장소의 작동 사실과 evidence 기록
- Source Type: As-Is / Mechanism
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 4a reference-audio assist and local CLI UX landed
- Update Trigger: 코드 사실, path, dependency, 테스트, limitation이 바뀔 때
- Excluded Content: 장기 roadmap, 구조 규범, 우선순위 결정

## 1. As-Is Snapshot

| Capability | Status | Current Fact | Evidence |
| --- | --- | --- | --- |
| Documentation Stack | `working` | `.voice-tts/` 아래 local six-doc stack이 실제 구현 상태에 맞게 갱신되었다 | `.voice-tts/*.md` |
| Project Packaging | `working` | `uv + pyproject` 기반 Python project가 존재하며 현재 버전은 `0.4.0`이다 | `pyproject.toml`, `uv.lock`, `README.md` |
| Local CLI | `working` | `voice-tts version`, `voice-tts init`, `voice-tts doctor`, `voice-tts profiles`, `voice-tts prepare-ref`, `voice-tts synthesize` command가 존재한다 | `src/voice_tts/cli.py` |
| Settings Loader | `working` | `.env` 기반 local settings loader가 `GPT_SOVITS_ROOT`, `MODEL_MANIFEST`, `OUTPUT_ROOT`를 다룬다 | `src/voice_tts/infrastructure/config.py`, `.env.example` |
| Typed Model Profile Catalog | `working` | JSON manifest에서 `display_name`, `languages`, `speaker_tags`, `notes`, `compatibility`까지 포함한 profile을 읽고 legacy fallback은 warning으로 남긴다 | `src/voice_tts/domain/entities.py`, `src/voice_tts/infrastructure/repositories.py`, `config/model-profiles.example.json` |
| Workspace Scaffolding | `working` | `init`가 `.env`와 seeded manifest를 생성하고 `.local/tmp`, `.local/outputs`를 만든다 | `src/voice_tts/infrastructure/workspace.py`, `src/voice_tts/cli.py` |
| GPT-SoVITS Runtime Adapter | `working` | external checkout을 `sys.path`에 붙여 GPT-SoVITS v2 inference 클래스를 import한다 | `src/voice_tts/infrastructure/gpt_sovits.py`, `src/voice_tts/infrastructure/engines.py` |
| Reference Audio Trim | `working` | optional `--ref-start-sec`, `--ref-end-sec`는 ffmpeg CLI를 통해 trim된다 | `src/voice_tts/infrastructure/engines.py` |
| Reference Audio Assist | `working` | `prepare-ref`가 ffprobe metadata inspect, ffmpeg silence-based candidate ranking, WAV export를 수행한다 | `src/voice_tts/infrastructure/reference_audio.py`, `src/voice_tts/application/use_cases.py`, `src/voice_tts/cli.py` |
| Doctor Diagnostics | `working` | Python version, device policy, workdir/temp/output, GPT root, ffmpeg, manifest profile count, per-profile metadata/config/device/checkout/import 상태를 점검한다 | `src/voice_tts/bootstrap/doctor.py` |
| Synthesis Diagnostics | `working` | synthesize 성공 시 profile/config/ref/trim/elapsed/device/fp16 metadata를 출력하고 실패는 stage prefix로 구분된다 | `src/voice_tts/application/dto.py`, `src/voice_tts/cli.py`, `src/voice_tts/exceptions.py`, `src/voice_tts/infrastructure/engines.py` |
| Automated Tests | `working` | settings, CLI, repository, use case, workspace scaffolding, reference-audio parsing, architecture, adapter smoke test가 존재한다 | `tests/` |
| External Smoke | `working` | opt-in external synthesis smoke marker가 존재한다 | `tests/test_external_synthesis.py` |
| Service Adapter | `absent` | FastAPI/router/HTTP API는 intentionally absent다 | current file tree |

## 2. Runtime Entry Points

### CLI

- `uv run voice-tts version`
- `uv run voice-tts init --gpt-sovits-root ...`
- `uv run voice-tts doctor`
- `uv run voice-tts profiles`
- `uv run voice-tts prepare-ref --input ...`
- `uv run voice-tts synthesize --model-profile ... --text ... --text-lang ... --ref-audio ... --prompt-text ... --prompt-lang ...`

### Test Commands

- `uv run pytest`
- `uv run pytest -m external`

### Bootstrap Command

- `uv sync --python 3.10`

## 3. Current Facts Worth Preserving

1. 현재 repo는 local-first CLI setup + synthesis + diagnostics 단계다.
2. `doctor`는 heavy model load 없이 profile-aware compatibility preflight를 수행한다.
3. `prepare-ref`는 ffprobe로 source metadata를 보고 ffmpeg silencedetect 로그에서 non-silent span을 추출해 ranked candidate를 만든다.
4. `synthesize`는 GPT-SoVITS code를 vendoring 하지 않고 외부 checkout을 adapter로 참조한다.
5. output format은 WAV 고정이고 auto output path는 synthesize 기준 `.local/outputs/<profile>/...wav`, prepare-ref 기준 `.local/tmp/ref-clips/...wav`다.
6. deterministic failure surface는 `[manifest]`, `[preflight]`, `[import]`, `[trim]`, `[synthesis]`, `[output]` stage prefix를 사용한다.
7. real upstream execution은 local environment에 external GPT-SoVITS checkout과 compatible dependencies가 준비되어야 한다.

## 4. Current File Map

| Area | Primary Paths |
| --- | --- |
| package root | `src/voice_tts/__init__.py`, `src/voice_tts/__main__.py`, `src/voice_tts/cli.py`, `src/voice_tts/exceptions.py` |
| bootstrap | `src/voice_tts/bootstrap/container.py`, `src/voice_tts/bootstrap/doctor.py` |
| domain | `src/voice_tts/domain/entities.py`, `src/voice_tts/domain/value_objects.py`, `src/voice_tts/domain/ports.py` |
| application | `src/voice_tts/application/dto.py`, `src/voice_tts/application/use_cases.py` |
| infrastructure | `src/voice_tts/infrastructure/config.py`, `src/voice_tts/infrastructure/logging.py`, `src/voice_tts/infrastructure/repositories.py`, `src/voice_tts/infrastructure/engines.py`, `src/voice_tts/infrastructure/gpt_sovits.py`, `src/voice_tts/infrastructure/reference_audio.py`, `src/voice_tts/infrastructure/system.py`, `src/voice_tts/infrastructure/workspace.py` |
| config examples | `config/model-profiles.example.json` |
| tests | `tests/test_cli.py`, `tests/test_settings.py`, `tests/test_repositories.py`, `tests/test_use_cases.py`, `tests/test_reference_audio.py`, `tests/test_workspace.py`, `tests/test_engines.py`, `tests/test_external_synthesis.py`, `tests/test_architecture.py` |

## 5. Verification Baseline

Phase 4a에서 유지해야 하는 verification baseline:

1. `uv sync --python 3.10`
2. `uv run voice-tts version`
3. `uv run voice-tts init --gpt-sovits-root ...`
4. `uv run voice-tts doctor`
5. `uv run voice-tts profiles`
6. `uv run voice-tts prepare-ref --input ...`
7. `uv run pytest`
8. `uv run pytest -m external` when external assets are ready

## 6. Current Repository Drift

| Drift | Evidence | Effect |
| --- | --- | --- |
| external GPT-SoVITS root/manifest가 default workspace에는 없다 | default `doctor`가 fail한다 | repo 코드는 준비됐지만 local asset setup 없이는 바로 synthesize 할 수 없다 |
| web/API surface가 없다 | no FastAPI/router files | remote/service integration은 future optional phase다 |

## 7. Evidence Rules for V2

1. `working`은 실제 파일과 실행 경로가 repo에 있을 때만 쓴다.
2. `placeholder`는 구조는 있으나 기능 value가 없음을 뜻한다.
3. `absent`는 기대 surface가 아직 repo에 없음을 뜻한다.
4. 리서치 사실은 `ref/`와 `topology.md`, 구현 사실은 `mechanism.md`가 맡는다.
