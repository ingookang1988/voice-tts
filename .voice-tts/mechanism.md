# voice-tts Mechanism (V2)

- Role: 현재 저장소의 작동 사실과 evidence 기록
- Source Type: As-Is / Mechanism
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 3 diagnostics and model lifecycle closed
- Update Trigger: 코드 사실, path, dependency, 테스트, limitation이 바뀔 때
- Excluded Content: 장기 roadmap, 구조 규범, 우선순위 결정

## 1. As-Is Snapshot

| Capability | Status | Current Fact | Evidence |
| --- | --- | --- | --- |
| Documentation Stack | `working` | `.voice-tts/` 아래 local six-doc stack이 실제 구현 상태에 맞게 갱신되었다 | `.voice-tts/*.md` |
| Project Packaging | `working` | `uv + pyproject` 기반 Python project가 존재하며 Phase 3 기준 버전은 `0.3.0`이다 | `pyproject.toml`, `uv.lock`, `README.md` |
| Local CLI | `working` | `voice-tts version`, `voice-tts doctor`, `voice-tts synthesize` command가 존재한다 | `src/voice_tts/cli.py` |
| Settings Loader | `working` | `.env` 기반 local settings loader가 `GPT_SOVITS_ROOT`, `MODEL_MANIFEST`, `OUTPUT_ROOT`를 다룬다 | `src/voice_tts/infrastructure/config.py`, `.env.example` |
| Typed Model Profile Catalog | `working` | JSON manifest에서 `display_name`, `languages`, `speaker_tags`, `notes`, `compatibility`까지 포함한 profile을 읽고 legacy fallback은 warning으로 남긴다 | `src/voice_tts/domain/entities.py`, `src/voice_tts/infrastructure/repositories.py`, `config/model-profiles.example.json` |
| GPT-SoVITS Runtime Adapter | `working` | external checkout을 `sys.path`에 붙여 GPT-SoVITS v2 inference 클래스를 import한다 | `src/voice_tts/infrastructure/gpt_sovits.py`, `src/voice_tts/infrastructure/engines.py` |
| Reference Audio Trim | `working` | optional `--ref-start-sec`, `--ref-end-sec`는 ffmpeg CLI를 통해 trim된다 | `src/voice_tts/infrastructure/engines.py` |
| Doctor Diagnostics | `working` | Python version, device policy, workdir/temp/output, GPT root, ffmpeg, manifest profile count, per-profile metadata/config/device/checkout/import 상태를 점검한다 | `src/voice_tts/bootstrap/doctor.py` |
| Synthesis Diagnostics | `working` | synthesize 성공 시 profile/config/ref/trim/elapsed/device/fp16 metadata를 출력하고 실패는 stage prefix로 구분된다 | `src/voice_tts/application/dto.py`, `src/voice_tts/cli.py`, `src/voice_tts/exceptions.py`, `src/voice_tts/infrastructure/engines.py` |
| Automated Tests | `working` | settings, CLI, repository, use case, architecture, adapter smoke test가 존재한다 | `tests/` |
| External Smoke | `working` | opt-in external synthesis smoke marker가 존재한다 | `tests/test_external_synthesis.py` |
| Service Adapter | `absent` | FastAPI/router/HTTP API는 intentionally absent다 | current file tree |

## 2. Runtime Entry Points

### CLI

- `uv run voice-tts version`
- `uv run voice-tts doctor`
- `uv run voice-tts synthesize --model-profile ... --text ... --text-lang ... --ref-audio ... --prompt-text ... --prompt-lang ...`

### Test Commands

- `uv run pytest`
- `uv run pytest -m external`

### Bootstrap Command

- `uv sync --python 3.10`

## 3. Current Facts Worth Preserving

1. 현재 repo는 local-first CLI synthesis + diagnostics 단계다.
2. `doctor`는 heavy model load 없이 profile-aware compatibility preflight를 수행한다.
3. `synthesize`는 GPT-SoVITS code를 vendoring 하지 않고 외부 checkout을 adapter로 참조한다.
4. output format은 WAV 고정이고 auto output path는 `.local/outputs/<profile>/...wav`다.
5. deterministic failure surface는 `[manifest]`, `[preflight]`, `[import]`, `[trim]`, `[synthesis]`, `[output]` stage prefix를 사용한다.
6. real upstream execution은 local environment에 external GPT-SoVITS checkout과 compatible dependencies가 준비되어야 한다.

## 4. Current File Map

| Area | Primary Paths |
| --- | --- |
| package root | `src/voice_tts/__init__.py`, `src/voice_tts/__main__.py`, `src/voice_tts/cli.py`, `src/voice_tts/exceptions.py` |
| bootstrap | `src/voice_tts/bootstrap/container.py`, `src/voice_tts/bootstrap/doctor.py` |
| domain | `src/voice_tts/domain/entities.py`, `src/voice_tts/domain/value_objects.py`, `src/voice_tts/domain/ports.py` |
| application | `src/voice_tts/application/dto.py`, `src/voice_tts/application/use_cases.py` |
| infrastructure | `src/voice_tts/infrastructure/config.py`, `src/voice_tts/infrastructure/logging.py`, `src/voice_tts/infrastructure/repositories.py`, `src/voice_tts/infrastructure/engines.py`, `src/voice_tts/infrastructure/gpt_sovits.py`, `src/voice_tts/infrastructure/system.py` |
| config examples | `config/model-profiles.example.json` |
| tests | `tests/test_cli.py`, `tests/test_settings.py`, `tests/test_repositories.py`, `tests/test_use_cases.py`, `tests/test_engines.py`, `tests/test_external_synthesis.py`, `tests/test_architecture.py` |

## 5. Verification Baseline

Phase 3에서 유지해야 하는 verification baseline:

1. `uv sync --python 3.10`
2. `uv run voice-tts version`
3. `uv run voice-tts doctor`
4. `uv run pytest`
5. `uv run pytest -m external` when external assets are ready

## 6. Current Repository Drift

| Drift | Evidence | Effect |
| --- | --- | --- |
| external GPT-SoVITS root/manifest가 default workspace에는 없다 | default `doctor`가 fail한다 | repo 코드는 준비됐지만 local asset setup 없이는 바로 synthesize 할 수 없다 |
| reference-audio cleanup assist가 없다 | manual trim flags only | multi-speaker audio prep는 여전히 사람이 직접 해야 한다 |
| web/API surface가 없다 | no FastAPI/router files | remote/service integration은 future optional phase다 |

## 7. Evidence Rules for V2

1. `working`은 실제 파일과 실행 경로가 repo에 있을 때만 쓴다.
2. `placeholder`는 구조는 있으나 기능 value가 없음을 뜻한다.
3. `absent`는 기대 surface가 아직 repo에 없음을 뜻한다.
4. 리서치 사실은 `ref/`와 `topology.md`, 구현 사실은 `mechanism.md`가 맡는다.
