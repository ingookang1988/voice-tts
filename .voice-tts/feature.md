# voice-tts Feature Map (V2)

- Role: 현재 live 상태의 개발자-facing feature, hierarchy, actor-outcome, 작업 흐름, intentional hold를 기록하는 canonical feature SSOT
- Source Type: Feature / Current Project Map
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 1 local-first bootstrap closed
- Update Trigger: current live feature surface, actor outcome, primary entry, flow, intentional hold가 바뀔 때
- Excluded Content: phase 판단, 구조 규범, active WO, 상세 구현 증적

## 1. Document Role

이 문서는 `voice-tts` 프로젝트의 **현재 live 상태**를 개발자 관점의 product language로 설명한다. 현재 repo는 service product보다 **local CLI bootstrap tool**이 먼저 존재한다.

## 2. Current Project Feature Snapshot

| Feature ID | Feature | Current Status | Summary |
| --- | --- | --- | --- |
| `FEAT-DOC-01` | Documentation Control Tower | `live` | `.voice-tts/voice-tts.md`를 기준으로 현재 phase, 읽기 순서, 문서 ownership을 확인할 수 있다. |
| `FEAT-CLI-01` | Local CLI Surface | `live` | `voice-tts version`, `voice-tts doctor`를 통해 버전 조회와 bootstrap self-check를 실행할 수 있다. |
| `FEAT-CFG-01` | Settings Bootstrap | `live` | `.env.example`와 `pydantic-settings` 기반으로 local config를 로드할 수 있다. |
| `FEAT-ARCH-01` | Clean Architecture Seams | `live` | `SpeechSynthesisEngine`, `WeightRepository`, `SynthesizeSpeechUseCase` seam이 Phase 2 integration용으로 고정되어 있다. |

## 3. Feature Hierarchy

| Feature ID | Parent Feature | Actors | Primary Outcome | Primary Entry Point | Current Status | Hold Note |
| --- | --- | --- | --- | --- | --- | --- |
| `FEAT-DOC-01` | `none` | 개발자 | 현재 기준선과 문서 읽기 순서를 파악한다 | `.voice-tts/voice-tts.md` | `live` | governance surface다 |
| `FEAT-CLI-01` | `none` | 개발자 | 로컬 bootstrap 상태를 확인한다 | `uv run voice-tts doctor` | `live` | synthesize command는 아직 없다 |
| `FEAT-CFG-01` | `none` | 개발자 | local env와 path policy를 로드하고 검증한다 | `.env.example`, `voice_tts.infrastructure.config.Settings` | `live` | real model path validation은 아직 얕다 |
| `FEAT-ARCH-01` | `none` | 개발자 | Phase 2에서 GPT-SoVITS를 꽂을 seam을 재사용한다 | `src/voice_tts/domain`, `src/voice_tts/application` | `live` | placeholder implementation만 있다 |

## 4. Actor / Outcome Model

| Actor | Current Outcome |
| --- | --- |
| 구현을 이어갈 개발자 | CLI와 문서를 읽고 Phase 2 진입점을 빠르게 찾는다. |
| 환경을 점검하려는 개발자 | `voice-tts doctor`로 현재 local bootstrap 상태를 확인한다. |
| 아키텍처 결정을 유지하려는 개발자 | domain/application seam을 보며 GPT-SoVITS integration 위치를 명확히 잡는다. |

## 5. E2E Flows

### `FLOW-CLI-01` Local Bootstrap Check

- `Entry`: `uv run voice-tts doctor`
- `Path`: settings 로드 -> Python version 확인 -> workdir/temp path 상태 확인 -> optional GPT-SoVITS/weights path 상태 확인 -> PASS/WARN/FAIL 요약 출력
- `Current Surface`: CLI, settings loader, doctor report
- `Current Hold Boundary`: 실제 model import나 inference는 아직 수행하지 않는다

### `FLOW-CLI-02` Version Verification

- `Entry`: `uv run voice-tts version`
- `Path`: installed package version 출력
- `Current Surface`: CLI
- `Current Hold Boundary`: runtime/provider info는 아직 포함하지 않는다

### `FLOW-ARCH-01` Phase 2 Integration Start

- `Entry`: `src/voice_tts/application/use_cases.py`
- `Path`: command -> domain request -> `WeightRepository` -> `SpeechSynthesisEngine`
- `Current Surface`: application/dto/use_case, domain ports
- `Current Hold Boundary`: infrastructure는 placeholder이고 real adapter는 아직 없다

## 6. Intentional Hold Inventory

| Hold Item | Why It Is Not A Current Live Feature |
| --- | --- |
| `voice-tts synthesize` | real GPT-SoVITS integration이 아직 없다 |
| WAV/audio output | Phase 2의 happy-path deliverable이다 |
| model weight resolution | placeholder repository만 있고 local metadata contract는 아직 없다 |
| FastAPI/web adapter | local-first 범위를 지키기 위해 의도적으로 제외했다 |
| Docker/runtime packaging | 현재는 local CLI 개발 루프가 우선이다 |
