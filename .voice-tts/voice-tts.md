# voice-tts Documentation Control Tower (V2)

- Role: `.voice-tts/` 문서 체계의 최상위 진입점
- Source Type: Control Tower / Canonical Entry
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 2 local synthesis MVP closed / Phase 3 diagnostics and model lifecycle active-next
- Update Trigger: 상위 기준선, active focus, 문서 소유권, phase 요약이 바뀔 때
- Excluded Content: 상세 구현 로그, 장기 설계 해설, 세부 WO 이력

## 1. Purpose

이 문서는 `voice-tts` 프로젝트 문서 체계의 control tower다. 현재 기준선은 **local-first CLI 위에서 GPT-SoVITS v2 zero-shot synthesis가 열려 있는 상태**다.

문서 체계의 소유권은 아래와 같다.

1. `roadmap.md`는 phase와 promotion gate만 기록한다.
2. `feature.md`는 현재 live 상태의 개발자-facing feature와 flow만 기록한다.
3. `topology.md`는 목표 아키텍처 규범만 기록한다.
4. `mechanism.md`는 현재 저장소에 실제로 존재하는 사실만 기록한다.
5. `sprint.md`는 다음 구현 순서와 backlog만 기록한다.
6. `voice-tts.md`는 위 다섯 문서의 진입점과 기준선만 기록한다.

`ref/` 아래 문서는 background/reference이고, 현재 프로젝트의 SSOT는 `.voice-tts/` 루트의 six-doc stack이 맡는다.

## 2. Current Baseline

| Item | Current Baseline |
| --- | --- |
| Product Identity | 이 저장소는 **로컬 전용 GPT-SoVITS TTS toolkit**이다. 현재는 CLI에서 실제 zero-shot WAV 합성 경로가 열려 있다. |
| Canonical Doc Root | `.voice-tts/` |
| Current Live Product Map | 현재 live 상태의 개발자-facing feature owner는 `.voice-tts/feature.md`다. |
| Current Focus | 현재 기준선은 **Phase 3 diagnostics and model lifecycle** 준비다. Phase 2에서 `voice-tts synthesize`, manifest-backed profile resolution, external checkout adapter, manual ref trim, output policy가 들어왔다. |
| Architecture Program | `topology.md`는 local-first package canon과 Clean Architecture + DDD + port/adapter 원칙을, `mechanism.md`는 실제 파일/명령/테스트 사실을, `sprint.md`는 Phase 3의 diagnostics/model metadata 후속 작업을 소유한다. |
| Implemented Highlights | `voice-tts version`, `voice-tts doctor`, `voice-tts synthesize`, `JsonModelProfileRepository`, `GptSovitsV2SpeechSynthesisEngine`, `config/model-profiles.example.json`, adapter smoke test, external opt-in smoke |
| Open Follow-up | richer doctor diagnostics, profile metadata 확장, compatibility preflight, auto reference-audio assist, optional web/API adapter |

## 3. Phase Snapshot

| Phase Slice | Current Judgment | Notes |
| --- | --- | --- |
| Phase 0 Research and Harness | Closed baseline | 리서치 리포트와 local six-doc stack이 유지된다. |
| Phase 1 Local-first Bootstrap | Closed | `uv` project, `src/voice_tts`, CLI, doctor, settings, tests가 들어왔다. |
| Phase 2 Core Synthesis MVP | Closed | local synthesize command, manifest-backed profile resolution, external GPT-SoVITS adapter, WAV output path가 landed 되었다. |
| Phase 3 Model Lifecycle and Diagnostics | Active-next | richer profile metadata, diagnostics, runtime validation을 붙이는 단계다. |
| Phase 4 Optional Service Adapters | Queued | 필요 시 FastAPI, background worker, streaming surface를 추가하는 단계다. |

## 4. Canonical Six-Doc Stack

| Document | Owns | Read When | Must Not Contain |
| --- | --- | --- | --- |
| `voice-tts.md` | 기준선, 문서 소유권, active focus | 새 세션 시작, 문서 읽기 순서 판단 | 상세 증적, 세부 실행 로그 |
| `roadmap.md` | 장기 phase, exit gate, promotion rules | 현재 phase와 다음 승격 조건을 확인할 때 | 현재 코드 사실, file path evidence |
| `feature.md` | current live feature, actor-outcome, flow, intentional hold | 지금 어떤 로컬 surface가 실제로 열려 있는지 볼 때 | 구조 규범, 장기 phase 판정 |
| `topology.md` | 목표 아키텍처 규범, dependency canon | 구조 변경 허용 여부를 판단할 때 | 완료 판정, 실행 로그 |
| `mechanism.md` | 현재 저장소 사실, evidence, gap | 지금 repo에 실제로 무엇이 있는지 확인할 때 | 장기 roadmap, 우선순위 결정 |
| `sprint.md` | active WO, backlog, drift follow-up | 바로 다음 구현 작업을 정할 때 | 구조 규범, 장문의 리서치 설명 |

## 5. Current Repository Drift

| Drift | Current Evidence | Impact | Tracking |
| --- | --- | --- | --- |
| external GPT-SoVITS checkout은 여전히 repo 밖 자산이다 | `VOICE_TTS_GPT_SOVITS_ROOT`와 manifest가 필요하다 | setup이 끝나지 않으면 `doctor`와 `synthesize`가 fail한다 | `mechanism.md`, `sprint.md` |
| profile metadata는 아직 최소 계약만 있다 | manifest는 `id/version/tts_config_path` 중심이다 | compatibility preflight와 richer catalog는 Phase 3 과제다 | `roadmap.md`, `sprint.md` |
| ref audio 정리는 수동 구간 지정에 머물러 있다 | `--ref-start-sec`, `--ref-end-sec`만 제공된다 | diarization/VAD/ASR assist는 아직 없다 | `feature.md`, `roadmap.md` |
| web/API surface는 아직 intentionally absent다 | FastAPI/router가 없다 | local-first 흐름은 단순하지만 remote/service integration은 아직 논외다 | `topology.md`, `roadmap.md` |

## 6. Reading Order

1. `voice-tts.md`: 현재 기준선과 문서 역할을 먼저 확인한다.
2. `roadmap.md`: phase와 exit gate를 확인한다.
3. `feature.md`: 현재 live 상태의 로컬 surface를 확인한다.
4. `topology.md`: 이번 변경이 구조적으로 허용되는지 확인한다.
5. `mechanism.md`: 현재 repo에 실제로 무엇이 있는지 확인한다.
6. `sprint.md`: 바로 다음 WO를 확인한다.

## 7. Session Start Checklist

1. `voice-tts.md`에서 current phase와 drift를 읽는다.
2. `roadmap.md`에서 이번 작업이 어느 phase를 움직이는지 확인한다.
3. `feature.md`에서 어떤 로컬 실행 표면이 live인지 확인한다.
4. `topology.md`에서 구조 규범을 확인한다.
5. `mechanism.md`에서 실제 파일, 명령, 테스트를 확인한다.
6. `sprint.md`에서 active WO를 확인한다.
