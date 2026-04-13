# voice-tts Mechanism (V2)

- Role: 현재 저장소의 작동 사실과 evidence 기록
- Source Type: As-Is / Mechanism
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 1 local-first bootstrap closed
- Update Trigger: 코드 사실, path, dependency, 테스트, limitation이 바뀔 때
- Excluded Content: 장기 roadmap, 구조 규범, 우선순위 결정

## 1. As-Is Snapshot

| Capability | Status | Current Fact | Evidence |
| --- | --- | --- | --- |
| Documentation Stack | `working` | `.voice-tts/` 아래 local six-doc stack이 실제 구현 상태에 맞게 갱신되었다 | `.voice-tts/*.md` |
| Project Packaging | `working` | `uv + pyproject` 기반 Python project가 존재한다 | `pyproject.toml`, `.python-version`, `README.md` |
| Local CLI | `working` | `voice-tts version`, `voice-tts doctor` command가 존재한다 | `src/voice_tts/cli.py` |
| Settings Loader | `working` | `.env` 기반 local settings loader와 validation이 있다 | `src/voice_tts/infrastructure/config.py`, `.env.example` |
| Bootstrap Container | `working` | settings 로드와 placeholder dependency assembly를 수행하는 container가 있다 | `src/voice_tts/bootstrap/container.py` |
| Doctor Diagnostics | `working` | Python version, device policy, workdir/temp, optional external path를 점검하는 doctor report가 있다 | `src/voice_tts/bootstrap/doctor.py` |
| Domain/Application Seams | `working` | `SpeechSynthesisEngine`, `WeightRepository`, `SynthesizeSpeechUseCase` seam이 존재한다 | `src/voice_tts/domain/ports.py`, `src/voice_tts/application/use_cases.py` |
| GPT-SoVITS Runtime | `placeholder` | engine/repository는 placeholder이며 real inference는 없다 | `src/voice_tts/infrastructure/engines.py`, `src/voice_tts/infrastructure/repositories.py` |
| Automated Tests | `working` | settings, CLI, architecture smoke test가 존재한다 | `tests/test_settings.py`, `tests/test_cli.py`, `tests/test_architecture.py` |
| Service Adapter | `absent` | FastAPI/router/HTTP API는 intentionally absent다 | current file tree |

## 2. Runtime Entry Points

### CLI

- `uv run voice-tts version`
- `uv run voice-tts doctor`

### Test Commands

- `uv run pytest`

### Bootstrap Command

- `uv sync --python 3.10`

## 3. Current Facts Worth Preserving

1. 현재 repo는 local-first CLI bootstrap 단계다.
2. `doctor`는 inference를 수행하지 않는다.
3. optional external path(`GPT_SOVITS_ROOT`, `WEIGHTS_ROOT`)가 unset이면 warning으로 남고, 잘못 설정된 path는 fail로 처리한다.
4. Python version policy는 runtime에서 3.10.x를 요구한다.

## 4. Current File Map

| Area | Primary Paths |
| --- | --- |
| package root | `src/voice_tts/__init__.py`, `src/voice_tts/__main__.py`, `src/voice_tts/cli.py` |
| bootstrap | `src/voice_tts/bootstrap/container.py`, `src/voice_tts/bootstrap/doctor.py` |
| domain | `src/voice_tts/domain/entities.py`, `src/voice_tts/domain/value_objects.py`, `src/voice_tts/domain/ports.py` |
| application | `src/voice_tts/application/dto.py`, `src/voice_tts/application/use_cases.py` |
| infrastructure | `src/voice_tts/infrastructure/config.py`, `src/voice_tts/infrastructure/logging.py`, `src/voice_tts/infrastructure/engines.py`, `src/voice_tts/infrastructure/repositories.py` |
| tests | `tests/test_cli.py`, `tests/test_settings.py`, `tests/test_architecture.py` |

## 5. Verification Baseline

Phase 1에서 유지해야 하는 verification baseline:

1. `uv sync --python 3.10`
2. `uv run voice-tts version`
3. `uv run voice-tts doctor`
4. `uv run pytest`

## 6. Current Repository Drift

| Drift | Evidence | Effect |
| --- | --- | --- |
| real synthesis path는 아직 없다 | placeholder engine/repository | local bootstrap은 되지만 user-visible TTS output은 아직 없다 |
| doctor path policy는 Phase 1용으로 느슨하다 | optional path warning | Phase 2에서 stricter required contract로 바뀔 수 있다 |
| model metadata contract가 없다 | no weight manifest file or schema | speaker/model resolution 구현이 다음 단계다 |
| web/API surface가 없다 | no FastAPI/router files | remote/service integration은 future optional phase다 |

## 7. Evidence Rules for V2

1. `working`은 실제 파일과 실행 경로가 repo에 있을 때만 쓴다.
2. `placeholder`는 구조는 있으나 기능 value가 없음을 뜻한다.
3. `absent`는 기대 surface가 아직 repo에 없음을 뜻한다.
4. 리서치 사실은 `ref/`와 `topology.md`, 구현 사실은 `mechanism.md`가 맡는다.
