# voice-tts Feature Map (V2)

- Role: 현재 live 상태의 개발자-facing feature, hierarchy, actor-outcome, 작업 흐름, intentional hold를 기록하는 canonical feature SSOT
- Source Type: Feature / Current Project Map
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 3 diagnostics and model lifecycle closed
- Update Trigger: current live feature surface, actor outcome, primary entry, flow, intentional hold가 바뀔 때
- Excluded Content: phase 판단, 구조 규범, active WO, 상세 구현 증적

## 1. Document Role

이 문서는 `voice-tts` 프로젝트의 **현재 live 상태**를 개발자 관점의 product language로 설명한다. 현재 repo는 service product보다 **local CLI synthesis tool**이 먼저 존재한다.

## 2. Current Project Feature Snapshot

| Feature ID | Feature | Current Status | Summary |
| --- | --- | --- | --- |
| `FEAT-DOC-01` | Documentation Control Tower | `live` | `.voice-tts/voice-tts.md`를 기준으로 현재 phase, 읽기 순서, 문서 ownership을 확인할 수 있다. |
| `FEAT-CLI-01` | Local CLI Surface | `live` | `voice-tts version`, `voice-tts doctor`, `voice-tts synthesize`를 통해 버전 조회, compatibility preflight, 로컬 WAV 합성을 실행할 수 있다. |
| `FEAT-CFG-01` | Settings and Model Catalog | `live` | `.env.example`, typed model profile manifest, `pydantic-settings` 기반으로 local config와 profile catalog를 로드할 수 있다. |
| `FEAT-DIAG-01` | Profile-aware Diagnostics | `live` | `doctor`가 profile metadata completeness, config/YAML shape, checkout files, supported devices, shallow upstream import를 검사한다. |
| `FEAT-TTS-01` | Zero-shot Local Synthesis | `live` | external GPT-SoVITS v2 checkout을 adapter로 연결해 ref audio + prompt 기반 WAV 합성을 수행하고 richer metadata를 출력한다. |
| `FEAT-ARCH-01` | Clean Architecture Seams | `live` | `SpeechSynthesisEngine`, `ModelProfileRepository`, `SynthesizeSpeechUseCase` seam이 유지된다. |

## 3. Feature Hierarchy

| Feature ID | Parent Feature | Actors | Primary Outcome | Primary Entry Point | Current Status | Hold Note |
| --- | --- | --- | --- | --- | --- | --- |
| `FEAT-DOC-01` | `none` | 개발자 | 현재 기준선과 문서 읽기 순서를 파악한다 | `.voice-tts/voice-tts.md` | `live` | governance surface다 |
| `FEAT-CLI-01` | `none` | 개발자 | 로컬 상태 점검과 합성을 실행한다 | `uv run voice-tts doctor`, `uv run voice-tts synthesize` | `live` | external checkout setup이 prerequisite다 |
| `FEAT-CFG-01` | `FEAT-CLI-01` | 개발자 | env + manifest로 typed profile catalog와 path policy를 로드한다 | `.env.example`, `config/model-profiles.example.json`, `voice_tts.infrastructure.config.Settings` | `live` | legacy manifest도 읽지만 warning 대상이다 |
| `FEAT-DIAG-01` | `FEAT-CLI-01` | 개발자 | profile별 compatibility 문제를 synthesize 전에 좁힌다 | `voice_tts.bootstrap.doctor.run_doctor` | `live` | shallow import까지만 수행하고 heavy model load는 하지 않는다 |
| `FEAT-TTS-01` | `FEAT-CLI-01` | 개발자 | zero-shot ref audio 합성으로 WAV를 만들고 runtime metadata를 받는다 | `voice_tts.infrastructure.engines.GptSovitsV2SpeechSynthesisEngine` | `live` | GPT-SoVITS v2 단일 버전만 지원한다 |
| `FEAT-ARCH-01` | `none` | 개발자 | Phase 4 이후에도 domain/application seam을 재사용한다 | `src/voice_tts/domain`, `src/voice_tts/application` | `live` | service adapter는 아직 없다 |

## 4. Actor / Outcome Model

| Actor | Current Outcome |
| --- | --- |
| 구현을 이어갈 개발자 | 문서와 CLI를 읽고 local synthesis path를 바로 실행하거나 확장할 수 있다. |
| 환경을 점검하려는 개발자 | `voice-tts doctor`로 GPT-SoVITS root, manifest metadata, checkout files, device compatibility, shallow import 상태를 확인한다. |
| 음성 합성을 수행하려는 개발자 | `voice-tts synthesize`로 zero-shot reference-audio WAV를 생성하고 runtime diagnostics를 함께 확인한다. |
| 아키텍처 결정을 유지하려는 개발자 | domain/application seam을 보며 GPT-SoVITS integration 위치를 명확히 유지한다. |

## 5. E2E Flows

### `FLOW-CLI-01` Local Compatibility Preflight

- `Entry`: `uv run voice-tts doctor`
- `Path`: settings 로드 -> Python version 확인 -> workdir/temp/output 상태 확인 -> GPT-SoVITS root 확인 -> ffmpeg 확인 -> manifest parse/profile count 확인 -> profile metadata/config/device/check files 확인 -> shallow import 확인 -> PASS/WARN/FAIL 요약 출력
- `Current Surface`: CLI, settings loader, doctor report
- `Current Hold Boundary`: actual model instantiation는 하지 않지만 synthesize prerequisites는 강하게 검사한다

### `FLOW-CLI-02` Version Verification

- `Entry`: `uv run voice-tts version`
- `Path`: installed package version 출력
- `Current Surface`: CLI
- `Current Hold Boundary`: provider inventory는 아직 포함하지 않는다

### `FLOW-CLI-03` Local Zero-shot Synthesis

- `Entry`: `uv run voice-tts synthesize`
- `Path`: CLI flags -> command validation -> manifest profile resolution -> optional ffmpeg ref trim -> external GPT-SoVITS import -> synthesis -> WAV write -> diagnostics-rich result 출력
- `Current Surface`: CLI, application/use case, model profile repository, GPT-SoVITS adapter
- `Current Hold Boundary`: zero-shot 단일 경로만 지원하며 diarization/ASR/VAD와 reference-audio assist는 없다

## 6. Intentional Hold Inventory

| Hold Item | Why It Is Not A Current Live Feature |
| --- | --- |
| automatic diarization / VAD / ASR | 현재는 수동 구간 지정 기반의 단일 화자 전제만 지원한다 |
| reference-audio assist | ref audio prep는 아직 사람이 직접 구간을 잡아야 한다 |
| GPT-SoVITS v3 support | 현재 adapter는 v2 단일 버전만 지원한다 |
| FastAPI/web adapter | local-first 범위를 지키기 위해 의도적으로 제외했다 |
| Docker/runtime packaging | 현재는 local CLI 개발 루프가 우선이다 |
