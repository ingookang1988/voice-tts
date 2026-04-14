# voice-tts Roadmap (V2)

- Role: voice-tts의 장기 phase 전개와 promotion gate 관리
- Source Type: Roadmap / Goal State
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 2 local synthesis MVP closed / Phase 3 diagnostics and model lifecycle active-next
- Update Trigger: phase 순서, exit gate, promotion rule이 바뀔 때
- Excluded Content: 현재 코드 사실, file path evidence, 상세 실행 로그

## 1. Roadmap Use

이 문서는 목표 상태와 승격 조건만 관리한다. 현재 저장소의 구현 사실은 `mechanism.md`, 실제 실행 순서는 `sprint.md`가 우선이다.

## 2. Current Header

- Current sub-phase: **Phase 3 diagnostics and model lifecycle preparation**
- Next sub-phase: **profile metadata hardening + doctor preflight expansion**
- Next major phase: **Phase 4 optional service adapters**
- Queued candidate slice: **reference-audio assist와 runtime observability**

## 3. Phase Snapshot

| Phase | Goal | Current Status | Gate Status |
| --- | --- | --- | --- |
| Phase 0 | Research and documentation harness | 리서치 보고서와 local six-doc stack이 유지된다 | Closed baseline |
| Phase 1 | Local-first bootstrap and CLI runtime | `uv`, `src/voice_tts`, CLI, doctor, settings, tests가 repo에 landed 되었다 | Closed |
| Phase 2 | Core local synthesis MVP | local synthesize command, model profile manifest, external checkout adapter, WAV output이 들어왔다 | Closed |
| Phase 3 | Model lifecycle and diagnostics | richer profile metadata, compatibility preflight, richer runtime validation은 아직 없다 | Active-next |
| Phase 4 | Optional service adapters | FastAPI/web/service adapter는 아직 intentionally absent다 | Queued |

## 4. Phase Roadmap

### Phase 0: Research and Harness

- Goal: 리서치 자산과 문서 하네스를 정리해 구현 전 기준선을 확보한다.
- Current judgment: reference research와 local six-doc stack이 유지되고 있으므로 baseline은 닫혔다.
- Exit gate:
1. 핵심 리서치 문서가 repo에 존재한다.
2. 문서 하네스 6종이 `.voice-tts/` 루트에 존재한다.
3. 문서별 ownership이 서로 충돌하지 않는다.
- Gate status: Closed baseline

### Phase 1: Local-first Bootstrap

- Goal: 웹/API 없이 로컬에서 시작 가능한 패키지, CLI, 설정, 테스트 부트스트랩을 만든다.
- Current judgment: `uv` manifest, `src/voice_tts`, `voice-tts version`, `voice-tts doctor`, 내부 seam, pytest baseline이 들어왔으므로 목표 범위는 닫혔다.
- Exit gate:
1. `uv sync`가 성공한다.
2. `voice-tts version`과 `voice-tts doctor`가 동작한다.
3. settings와 architecture smoke test가 존재한다.
4. GPT-SoVITS를 꽂을 내부 seam이 고정된다.
- Gate status: Closed

### Phase 2: Core Local Synthesis MVP

- Goal: GPT-SoVITS를 실제로 adapter seam에 연결하고 로컬 synthesize happy path를 연다.
- Current judgment: `voice-tts synthesize`, `JsonModelProfileRepository`, `GptSovitsV2SpeechSynthesisEngine`, auto output policy, opt-in external smoke contract가 들어왔으므로 MVP 목표 범위는 닫혔다.
- Depends on: Phase 1 closure.
- Must-have outputs:
  - `SpeechSynthesisEngine`의 real adapter implementation
  - manifest-backed `ModelProfileRepository`
  - local `voice-tts synthesize` command
  - ref audio + prompt + profile input -> local WAV output happy path
- Exit gate:
1. local command로 WAV 파일을 생성할 수 있다.
2. application은 여전히 GPT-SoVITS 내부 세부사항을 직접 모른다.
3. missing model/config/root failure가 deterministic error로 반환된다.
4. 기본 smoke와 opt-in external smoke가 존재한다.
- Gate status: Closed

### Phase 3: Model Lifecycle and Diagnostics

- Goal: profile metadata, doctor diagnostics, compatibility validation, output metadata를 정리한다.
- Depends on: Phase 2 closure.
- Must-have outputs:
  - richer model profile metadata contract
  - compatibility/version preflight validation
  - richer `doctor` output
  - runtime diagnostics/logging
- Exit gate:
1. profile selection이 richer metadata 기반으로 동작한다.
2. invalid path/version mismatch를 사전에 더 넓게 검출한다.
3. bootstrap/diagnostic output이 local troubleshooting에 충분하다.
- Gate status: Active-next

### Phase 4: Optional Service Adapters

- Goal: 필요 시 FastAPI 또는 다른 service adapter를 붙인다.
- Depends on: Phase 2 or 3 closure.
- Repo Status: 현재 repo에는 intentionally no web/API surface 상태다.
- Exit gate:
1. local core가 service adapter 뒤에서도 같은 seam을 유지한다.
2. adapter 추가가 domain/application canon을 깨지 않는다.
3. local-first command path는 계속 canonical debug path로 유지된다.
- Gate status: Queued

## 5. Promotion Rules

1. phase 승격은 일정이 아니라 exit gate 증거로 결정한다.
2. synthesize command가 있어도 deterministic failure와 basic smoke가 없으면 Phase 2는 닫히지 않는다.
3. web adapter는 로컬 코어와 diagnostics가 흔들리는 상태에서 먼저 열지 않는다.
4. 문서와 runtime truth가 어긋나면 phase를 낮추기보다 `mechanism.md`와 `sprint.md`에 drift를 남긴다.
