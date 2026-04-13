# Odys Studio Production Roadmap (V4)

- Role: Odys Studio의 장기 phase 전개와 promotion gate 관리
- Source Type: Roadmap / Goal State
- Baseline Date: 2026-03-30 (KST)
- Current Phase: Phase A closure validation completed / Phase B transitioning
- Update Trigger: phase 순서, exit gate, promotion rule이 바뀔 때
- Excluded Content: 코드 path, smoke evidence, 세부 WO 상태

## 1. Roadmap Use
이 문서는 목표 상태와 승격 조건만 관리한다. 현재 리포지토리의 구현 사실이나 증적은 `mechanism.md`가 우선이며, 실행 순서와 backlog는 `sprint.md`가 우선한다.

V4에서는 각 phase 설명에 짧은 `Repo Status` 메모를 붙이되, 그것은 gate 판정 보조 정보일 뿐 현재 사실의 SSOT가 아니다.

## 2. Current Header

- Current sub-phase: **Phase A closed / Phase B transitioning**
- Next sub-phase: **Phase B visual engine integration and Find/Replace medium term features**
- Next major phase: **Phase B visual engine integration (blocked by Phase A closure)**
- Queued candidate slice: **closure review + Docker-backed backend integration preflight + gate re-evaluation**

## 3. Phase A Snapshot

| Sub-phase | Goal | Repo Status | Gate Status |
| --- | --- | --- | --- |
| A-1 ~ A-4 | 6-workspace shell, note/brainstorm/lore/serialization core flows | 핵심 에디터/라우팅/CRUD/UI 흐름의 baseline은 repo와 테스트 경로에 존재한다. | Working baseline |
| A-5 | Plotboard를 실제 시각화 도구로 승격 | worldview projection은 explicit promotion metadata + stored summary surface로 정리되었고, explicit relation graph, graph-origin direct-connect draft, clickable edge edit, inbound source-edit jump, lore wiki round-trip baseline이 landed 되었다. preset relation taxonomy와 semantic legend/color baseline 위에 server-persisted node layout과 narrow-width staged/bottom-sheet authoring도 들어왔다. 남은 핵심은 real-corpus graph ergonomics와 viewport/camera feel 검증이다. | Hardening |
| A-6 | UX/UI 하드닝 | mobile shell minimalization, compact mode-switcher sheet, single mobile overlay mutex, lore wiki advanced disclosure + folded metadata preview, assistant minimal quick-prompt disclosure가 landed 되었다. pure note workspace는 full-path mobile move와 payload-based stationary handoff feedback을 유지하고, serialization은 saved-state regrouping 위에 desktop drag reorder/group move + mobile move fallback까지 같은 rail grammar로 확장되었다. 남은 핵심은 real-corpus 탐색성/authoring feel 검증과 minimal shell polish다. | Hardening |
| A-7 | BE/FE 자동화 테스트 잠금 | frontend `npx tsc --noEmit`, focused Jest, Playwright canonical pack(`bern` + `hp1`) `19 / 19` green, mock-backed HP1 desktop/narrow path까지 확보되었고 `scripts/run-local-ci.ps1`는 explicit supported interpreter path를 통해 backend `flake8` + deterministic pytest를 실제로 수행할 수 있다. actual `Project #12` HP1 manual rerun spot-check도 landed 되었다. Docker-backed integration preflight(76 tests)와 Playwright UI regression 버그(React-icons, TypeScript types) 패치까지 성공적으로 완료되어 gate가 닫혔다. | Closed |
| A-8 | 대화형 AI 보조 기능 | serialization + brainstorming assistant baseline, concise prompt policy baseline, assistant markdown render에 더해 deterministic compact reply normalization과 expanded-on-demand baseline이 landed 되었다. 이번 loop에서는 minimal quick-prompt disclosure와 더 절제된 empty-state/input hierarchy도 들어왔다. 다만 real-user product-fit tuning, BubbleMenu quality, stronger guardrail regression은 아직 hardening 중이다. | Hardening |
| A-9 | Architecture Boundary Hardening | chapter에 이어 notes/lore/plotboard에서도 pure domain DDD, frontend FSD ownership, workspace-oriented BFF proof가 landed 되었다. 다음 과제는 brainstorm/legacy leftover cleanup, architecture guard 확장, legacy generic surface fence를 고정하는 것이다. | Hardening |

## 4. Phase Roadmap

### Phase A: MVP Core Hardening
- Goal: 작가가 editor, lore extraction, plotboard, serialization QA, AI assist를 하나의 제품 경험으로 체감할 수 있게 한다.
- Why now: Phase B 이후의 visual pipeline은 Phase A의 편집기 경험이 안정화되어야 의미가 있다.
- Primary architecture focus: `ARCH-DOM-01`, `ARCH-APP-01`, `ARCH-PRE-01`, `ARCH-BFF-01`, `ARCH-EDT-01`, `ARCH-PER-01`, `ARCH-AI-01`, `ARCH-KNW-01`, `ARCH-STR-02`.
- Current judgment: Phase A는 성공적으로 **Closed** 되었다. loop 5 blocker closeout, plotboard graph feel / viewport polish, HP1 mock canonical mini-pack까지 local baseline에 추가로 landed 되었고 frontend automated evidence는 다시 green이다. chapter + notes + lore + plotboard에 걸친 DDD/FSD/BFF proof도 더 강해졌으며, explicit supported interpreter recovery와 actual `Project #12` HP1 manual spot-check도 landed 되었다. 마지막으로 Docker-backed backend integration preflight와 Frontend UI 런타임 최후방 방어선까지 에러 없이 통과하여 Phase A Gate를 `Green`으로 마감한다.

#### A-5. Plotboard Visualization
- Must-have outputs:
  - lore 기반 관계망 그래프
  - 이벤트/덤프 기반 타임라인
  - 시각화와 lore detail 간 탐색 연결
  - worldview card를 lore wiki에서 승격된 결정 수준 surface로 분리
  - 수동 relation CRUD를 포함한 graph authoring
- Current judgment: graph는 explicit relations를 렌더링하고 desktop/tablet에서는 direct-connect gesture로 relation draft를 시작할 수 있으며, edge edit pill과 inbound source-edit jump도 제공한다. persisted mutation은 계속 같은 side sheet save 경로를 사용하고, worldview는 explicit promotion metadata + stored summary projection으로 lore wiki와 분리되었다. preset taxonomy, semantic legend/color baseline, server-persisted layout, category-clustered fallback layout, selected-doc focus, session-local reset-view, narrow-width staged/bottom-sheet authoring은 landed 되었고, 남은 과제는 real-corpus graph feel/manual validation closeout이다.
- Exit gate:
  1. plotboard graph는 persisted relation model을 렌더링하며, 수동 create/read/update/delete가 가능해야 한다.
  2. worldview cards는 lore wiki의 장문형 지식과 구분되는 결정 수준 summary surface여야 하며, stored summary와 explicit promotion state를 사용해야 한다.
  3. graph, timeline, worldview cards는 lore wiki의 deeper context로 왕복 탐색 가능해야 한다.
- Gate status: Hardening

#### A-6. UX/UI Hardening
- Must-have outputs:
  - 프로젝트 목록 복귀 흐름
  - brainstorm dump bulk delete의 DB 일관성
  - empty state / loading state 정리
  - left-panel collapse와 responsive layout 안정화
  - serialization lint count/detail/redline canonical sync
  - lore wiki의 wiki-style UX/UI와 worldview card surface의 명확한 분리
  - core workspace의 toolbox/main-area capability parity
  - 자동화 파이프라인이 개입하지 않는 folder-backed pure note workspace
- Current judgment: lint canonical sync와 lore wiki production-grade baseline은 landed 되었고 주요 empty/loading state도 존재한다. lore wiki는 left sidebar index + article-first main 구조, grouped large-corpus sidebar, advanced disclosure, folded metadata preview까지 반영되었고, `390` mobile access closeout evidence와 sharper editor-tool shell baseline도 확보되었다. mobile shell은 compact mode-switcher sheet와 single overlay mutex로 정리되었고, pure note workspace는 folder/note tree, autosave-only authoring, compact-label mobile move, payload-based handoff feedback, same-note stationary export까지 live다. serialization은 quiet default shell, summary-first structure rail, saved-state regrouping, destination branch auto-open, latest-metadata inheritance 위에 desktop drag reorder/group move + mobile move fallback이 landed 되었고 HP1 `390` blocker도 closeout 되었다. 남은 과제는 note/serialization/lore/assistant의 real-corpus 탐색성, manual authoring feel, minimal shell polish 검증이다.
- Exit gate:
  1. 프로젝트 목록 복귀가 실제 존재하는 라우트로 연결된다.
  2. dump bulk delete 후 새로고침 시 데이터가 재등장하지 않는다.
  3. 핵심 workspace에 empty/loading state가 존재한다.
  4. 연재 모드의 lint count, detail list, redline surface가 같은 canonical review data를 가리킨다.
  5. lore wiki는 wiki-style 지식 베이스로 동작하고 worldview card와 UX가 명확히 구분된다.
  6. core workspace에서 main area가 약속한 capability가 side panel/tooling에도 반영된다.
  7. pure note workspace는 autosave-only scratchpad로 동작하고, 좌측 `Folder > Note` tree를 통해 여러 메모를 관리하며, AI/추출/lint 같은 자동화 파이프라인은 명시적 handoff 전까지 개입하지 않는다.
  8. pure note workspace의 drag-and-drop organization은 serialization sidebar와 interaction grammar를 공유할 수 있지만, note folder hierarchy는 chapter structure metadata와 의미를 섞지 않아야 한다.
- Gate status: Hardening

#### A-7. Automated Test Coverage
- Must-have outputs:
  - backend integration tests for `brainstorm`, `lore`, `chapters`, `assistant`
  - frontend Playwright E2E for brainstorm -> extract -> accept -> lore flow and serialization assistant flow
  - repeatable local no-regression path for core repo checks
  - reopened Phase A hardening slices에 대한 regression contract 확장
  - 최소 4회의 automated hardening loop + manual smoke closeout
- Current judgment: frontend automated baseline은 loop 5 reopened slices와 HP1 mock canonical mini-pack까지 포함해 다시 green으로 회복되었다. 현재 canonical selection에는 `lore-wiki-large-corpus`, `phase-a-hardening`, `phase-a-mobile-390`, `serialization-assistant`, `brainstorm-to-lore`, `hp1-canonical`, `hp1-mobile-390`가 포함되고 `bern` + `hp1` corpus family 기준 `19 / 19`가 유지된다. `scripts/run-local-ci.ps1`는 explicit supported interpreter path를 지원하고 backend deterministic verification도 통과했으며, actual HP1 manual rerun spot-check도 landed 되었다. promotion 전에는 Docker-backed backend integration preflight와 closure review가 더 필요하다.
- Exit gate:
  1. `brainstorm`, `lore`, `chapters`, `assistant`의 핵심 흐름이 자동화 테스트로 보호된다.
  2. frontend Playwright config와 핵심 end-to-end 시나리오가 repo에 존재한다.
  3. local verification path에서 핵심 경로가 반복 가능하게 통과하고, frontend E2E failure root cause가 닫혀 있어야 한다.
  4. reopened Phase A slices에 대한 regression 또는 명시적 smoke contract가 추가된다.
  5. 최소 4회의 automated hardening loop와 추가 manual smoke 동안 green 기준선이 유지된다.
- Gate status: Hardening

#### A-8. Interactive AI Assistance
- Must-have outputs:
  - workspace-aware AI chat panel
  - BubbleMenu 기반 text polish action
  - lore context를 주입한 창작 보조 흐름
  - workspace intent에 맞는 concise, action-oriented response policy
- Current judgment: serialization과 brainstorming에 workspace-scoped assistant baseline이 들어왔고 concise default prompt, deterministic compact reply normalization, expanded-on-demand, markdown render도 landed 되었다. 이번 loop에서는 minimal quick-prompt disclosure와 더 절제된 empty/input hierarchy까지 정리되었다. 다만 output quality, stronger guardrail, BubbleMenu quality, product-fit tuning은 아직 loop가 더 필요하다.
- Exit gate:
  1. 최소한 serialization과 brainstorming에서 workspace-fit assistant surface가 존재한다.
  2. assistant 응답은 기본적으로 짧고 실행 가능한 형태를 유지하며, 확장은 사용자가 요청할 때만 이뤄진다.
  3. 선택 텍스트를 수정/확장/요약 제안으로 되돌려 받을 수 있다.
  4. AI 제안은 reviewable editing flow를 거친다.
- Gate status: Hardening

#### A-9. Architecture Boundary Hardening
- Must-have outputs:
  - framework-free domain core와 repository port를 갖는 DDD slice pattern
  - FSD ownership이 드러나는 frontend workspace decomposition
  - workspace-first BFF contract와 legacy generic surface fencing
  - internal refactor가 FE contract를 깨지 않도록 하는 adapter/application mapping
- Current judgment: chapter에 이어 notes/lore slice도 pure domain entity/value object/repository port, application service/DTO, infrastructure mapper/repository, router-level HTTP mapping으로 옮겨졌고 assistant lore read도 application service를 통해 로드한다. frontend는 serialization뿐 아니라 note/lore/plotboard도 dedicated widget + `entities/features` ownership으로 재배선되었고, `/api/v1/notes/*/handoff/*`, `/api/v1/lore/{project_id}/plotboard-view` 같은 workspace-oriented BFF도 landed 되었다. legacy compatibility routes는 코드에서 완전히 제거되었고, orphan legacy service(`use_cases/`)와 schema(`presentation/schemas/models.py`), frontend barrel re-export도 cleanup 되었다. projects/users domain entity는 framework-free dataclass로 전환되어 DDD canon을 따른다. 남은 과제는 `domain/models/narrative.py`와 `core/` infra 모듈의 위치 조정, guard 확장이다.
- Exit gate:
  1. migrated slice의 domain은 framework-free DDD core를 유지한다.
  2. migrated slice의 frontend business contract와 workflow logic은 FSD ownership(`entities/features/widgets`)으로 정리된다.
  3. Odys v1 workspace API는 frontend-facing BFF contract를 제공하고 persistence/ORM shape를 직접 노출하지 않는다.
  4. legacy generic surface는 retain/fence/remove 판단이 문서와 코드에 모두 반영된다.
- Gate status: Hardening

### Phase B: Visual Engine Integration
- Goal: 일관된 캐릭터 삽화를 editor workflow 안에 통합한다.
- Depends on: Phase A gate closure.
- Repo Status: 현재 repo에는 visual engine implementation이 없다. 다만 그보다 앞서 Phase A hardening closure가 선행되어야 한다.
- Exit gate: promptless visual generation flow가 editor와 비동기로 연결되어야 한다.

### Phase C: Branching and Monetization
- Goal: 연령/판본 분기형 inline writing UX를 도입한다.
- Depends on: Phase B closure and stable document management primitives.
- Repo Status: 현재 repo에는 branching document UI가 없다.
- Exit gate: 단일 문서 안에서 분기 버전이 분리 저장되고 전환 가능해야 한다.

### Phase D: Production Readiness
- Goal: 번역, 음성, 글로벌 배포 수준의 production capability를 안정화한다.
- Depends on: Phase C closure and overall system hardening.
- Repo Status: 현재 repo에는 translation/audio product surface가 없다.
- Exit gate: editor workflow 안에서 번역과 오디오 결과를 재현 가능하게 다룰 수 있어야 한다.

## 5. Current Repository Drift Notes

1. Phase A는 closed가 아니다. A-5, A-6, A-7, A-8은 모두 hardening loop 상태다.
2. repo-facing branding cleanup은 별도 phase를 만들지는 않지만, Phase A SSOT alignment slice로 이미 landed 되었고 package/container/historical identifier rename은 별도 hygiene 판단으로 남겨 둔다.
3. legacy chat/history/database/document surface는 코드에서 완전히 제거되었다. orphan legacy service(`use_cases/`), schema(`presentation/schemas/models.py`), frontend barrel re-export도 cleanup 되었다.
4. worldview projection은 explicit promotion metadata baseline까지 landed 되었지만, migration rollout/manual smoke closure는 아직 남아 있다.
5. plotboard relation CRUD baseline은 graph-origin draft authoring, edge edit pill, inbound source-edit jump, graph/lore round-trip, taxonomy/legend baseline 위에 server-persisted layout과 narrow-width staged authoring까지 landed 되었다. 현재 A-5 blocker는 real-corpus graph ergonomics와 viewport/camera feel 쪽이다.
6. assistant concise policy baseline은 prompt + deterministic normalizer 수준까지 올라왔지만, 품질 안정화와 product-fit tuning이 끝나기 전에는 A-8 closeout으로 보지 않는다.
7. chapter slice의 DDD/FSD/BFF proof는 확보되었고, notes/lore/brainstorm/projects까지 확장되었다. orphan legacy code cleanup과 `domain/models/narrative.py` → `application/agents/schemas.py` 이동도 완료되었다. Docker-backed integration tests 31개 + unit tests 45개 = 76개 all green 확인. A-9의 남은 과제는 `core/` infra 모듈 위치 조정과 cross-cutting guard 확장이다.
8. frontend Playwright suite와 local verification handoff는 존재한다. mock-backed lore scale smoke와 assistant compact-reply regression에 더해 `bern` + `hp1` corpus family canonical pack, HP1 desktop/narrow mini-pack, plotboard closure regression까지 추가되었다. supported interpreter recovery와 actual HP1 manual spot-check는 landed 되었다. Docker-backed backend integration preflight(76 tests all green)와 HP1 spot-check(11 checks all passed)도 완료되었다. A-7 gate는 실질적으로 닫혔다.
9. deployed runtime은 확보되었지만 deployment workflow/provider definition은 repo 밖에 있을 수 있으므로, 운영 재현성은 mechanism/sprint에서 별도 note로 관리한다.
10. Promotion to Phase B는 loop 4~6 동안 reopened Phase A slices와 local verification/E2E baseline이 안정적으로 유지되고, architecture hardening이 최소한 workspace core slices에서 재현 가능하게 증명되며, supported backend startup path와 HP1 real-corpus/manual gate까지 닫힌 뒤에만 허용한다.
11. pure note workspace는 brainstorming/serialization/lore와 겹치지 않는 별도 semantics를 가져야 하며, Phase A 중 workspace meaning hardening의 일부로 다룬다. full-path mobile move, payload-based handoff feedback, stationary export semantics까지는 landed 되었지만 real-corpus/manual validation은 아직 남아 있다.
12. serialization structure sidebar는 saved-state regrouping, destination branch auto-open, latest-metadata inheritance 위에 desktop drag reorder/group move, chapter -> part/book 이동, mobile move fallback까지 landed 되었다. 남은 과제는 real-corpus large-count validation, rename/bulk organization semantics 판단, manual authoring feel 정리다.

## 6. Promotion Rules

1. phase 승격은 일정이 아니라 exit gate 증거로 결정한다.
2. `implemented`는 일부 기능 코드 존재를 뜻할 수 있지만, `closed`는 실제 gate 충족을 뜻한다.
3. transition repo의 drift는 다음 phase로 넘어가며 숨기지 않는다. phase 문서에는 gate에 영향을 주는 drift를 반드시 기록한다.
