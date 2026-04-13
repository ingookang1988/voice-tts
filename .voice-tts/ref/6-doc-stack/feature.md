# Odys Studio Feature Map (V4)

- Role: current live feature, hierarchy, actor-outcome, E2E flow, intentional hold를 product language로 기록하는 canonical feature SSOT
- Source Type: Feature / Current Product Map
- Baseline Date: 2026-03-30 (KST)
- Current Phase: Phase A closure validation active / Phase B visual engine integration blocked-next
- Update Trigger: current live feature surface, actor outcome, primary entry, E2E flow, intentional hold가 바뀔 때
- Excluded Content: phase 판단, topology 규범, WO 실행 상태 표, release 증적 소유권, latest SHA

## 1. Document Role

이 문서는 Odys Studio의 **현재 live product**를 product language로 설명하는 canonical feature SSOT다. `feature.md`는 workspace-first 기준의 live feature snapshot, actor/outcome, primary entry point, E2E flow, intentional hold만 소유한다.

Boundary는 아래와 같다.

1. phase sequencing과 promotion rule은 `roadmap.md`가 소유한다.
2. architecture norm과 sanctioned structure는 `topology.md`가 소유한다.
3. runtime fact, path evidence, test entry는 `mechanism.md`가 소유한다.
4. active WO, next action, closeout tracking은 `sprint.md`가 소유한다.
5. 문서 시스템 baseline과 reading order는 `odys.md`가 소유한다.

`.plan/` 아래 PRD, user journey, action plan 문서는 historical/background reference로 남고, current live product의 owner는 아니다.

## 2. Current Product Feature Snapshot

| Feature ID | Feature | Current Status | Summary |
| --- | --- | --- | --- |
| `FEAT-ENTRY-01` | Entry and Project Console | `live` | login과 project console에서 생성/열기/이름 수정/삭제 후 editor shell로 진입한다. |
| `FEAT-NOTE-01` | Pure Note Workspace | `live` | zero-intervention scratchpad에서 폴더/노트 트리, autosave, compact-label mobile move fallback, stationary compact export handoff를 제공한다. |
| `FEAT-BRAIN-01` | Brainstorming Workspace | `live` | 자유 덤프와 review-gated extract-to-lore 흐름(worldview + event-derived history candidate)을 제공한다. |
| `FEAT-PLOT-01` | Plotboard Workspace | `live` | worldview, persisted relation graph, timeline, lore round-trip을 제공한다. |
| `FEAT-SERIAL-01` | Serialization Workspace | `live` | manuscript authoring, structure rail DnD/group move, lint, reviewable AI를 결합한다. |
| `FEAT-LORE-01` | Lore Wiki Workspace | `live` | article-first knowledge base와 advanced disclosure 기반 metadata/promotion 편집을 제공한다. |
| `FEAT-AI-01` | Workspace-Aware AI Assistance | `live` | brainstorming/serialization assistant와 reviewable BubbleMenu polish, minimal quick prompts를 제공한다. |

## 3. Feature Hierarchy

| Feature ID | Parent Feature | Actors | Primary Outcome | Primary Entry Point | Current Status | Linked ARCH | Linked WO | Linked Tests / Evidence | Hold Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `FEAT-ENTRY-01` | `none` | 신규/복귀 작가 | 로그인 후 프로젝트를 생성/정리하고 현재 프로젝트를 다시 연다 | `/` -> project list -> `/editor/[id]` | `live` | `ARCH-PRE-01`, `ARCH-APP-01` | `WO-PRE-CORE-001`, `WO-UX-007`, `WO-UX-014`, `WO-UX-015` | `frontend/e2e/brainstorm-to-lore.spec.ts` | `none` |
| `FEAT-NOTE-01` | `none` | 자유 메모형 작가 | 자동 개입 없이 메모를 쌓고 필요할 때만 다른 workspace로 복제한다 | editor `노트` tab | `live` | `ARCH-PRE-01`, `ARCH-EDT-01`, `ARCH-APP-01`, `ARCH-PER-01` | `WO-PRE-CORE-003` | `tests/backend/api/test_notes.py`, `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/phase-a-mobile-390.spec.ts`, `frontend/e2e/hp1-mobile-390.spec.ts` | automated closeout은 landed 되었고, real-corpus/manual large-tree 및 handoff feel validation이 남아 있다 |
| `FEAT-BRAIN-01` | `none` | 정원사형 작가 | 자유 덤프를 쌓고 lore extraction으로 구조화한다 | editor `브레인스토밍` tab | `live` | `ARCH-PRE-01`, `ARCH-APP-01`, `ARCH-AI-01` | `WO-PRE-CORE-002`, `WO-AI-005`, `WO-UX-016` | `frontend/e2e/brainstorm-to-lore.spec.ts`, `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/hp1-canonical.spec.ts` | 백그라운드 덤프 추출 전역 상태화가 완료되어 워크스페이스 간 이동 중에도 유지된다 |
| `FEAT-PLOT-01` | `none` | 건축가형 작가 | worldview, relation, timeline을 시각적으로 조정하고 lore와 왕복한다 | editor `플롯보드` tab | `live` | `ARCH-PRE-01`, `ARCH-KNW-01`, `ARCH-PER-01` | `WO-VIZ-001`, `WO-VIZ-002`, `WO-IA-001` | `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/phase-a-mobile-390.spec.ts`, `frontend/e2e/hp1-canonical.spec.ts`, `frontend/e2e/hp1-mobile-390.spec.ts`, `tests/backend/api/test_lore.py` | persisted layout, category-clustered fallback, same-doc focus, reset-view, staged narrow authoring은 live이고, real-corpus graph feel/manual validation이 남아 있다 |
| `FEAT-SERIAL-01` | `none` | 연재 작가 | manuscript를 쓰면서 lint, structure metadata, reviewable polish를 함께 다룬다 | editor `작품 연재` tab | `live` | `ARCH-PRE-01`, `ARCH-EDT-01`, `ARCH-AI-01`, `ARCH-PER-01` | `WO-PRE-CORE-002`, `WO-UX-012`, `WO-IA-002`, `WO-AI-004`, `WO-UX-016` | `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/serialization-assistant.spec.ts`, `frontend/e2e/hp1-mobile-390.spec.ts`, `tests/backend/api/test_chapters.py`, `tests/backend/test_chapter_service.py`, `tests/backend/api/test_assistant.py` | 서사 분석 전역화 및 LoreEntity 하이라이트가 추가되었으며, 타자기 스크롤, 일괄 바꾸기, 일괄 수락/거절 기능 등 핵심 에디터 도구가 추가되어 안정되었다 |
| `FEAT-LORE-01` | `none` | 설정 큐레이터 | article-first wiki에서 metadata, promotion, relation reference를 관리한다 | editor `로어 백과` tab | `live` | `ARCH-PRE-01`, `ARCH-KNW-01`, `ARCH-PER-01` | `WO-PRE-CORE-002`, `WO-IA-001` | `frontend/e2e/lore-wiki-large-corpus.spec.ts`, `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/hp1-canonical.spec.ts`, `tests/backend/api/test_lore.py` | advanced disclosure와 folded metadata preview는 live이고, real-corpus scale/perf/manual validation이 남아 있다 |
| `FEAT-AI-01` | `FEAT-BRAIN-01`, `FEAT-SERIAL-01` | 연재 작가, 정원사형 작가 | workspace intent에 맞는 짧은 보조 응답과 reviewable text polish를 받는다 | `AI 보조` panel, BubbleMenu polish actions | `live` | `ARCH-AI-01`, `ARCH-PRE-01`, `ARCH-STR-03` | `WO-AI-003`, `WO-AI-004`, `WO-AI-005`, `WO-AI-006` | `frontend/e2e/serialization-assistant.spec.ts`, `frontend/e2e/phase-a-hardening.spec.ts`, `tests/backend/api/test_assistant.py` | minimal quick prompts는 live이고, product-fit tuning, BubbleMenu quality, stronger guardrail regression이 남아 있다 |

## 4. Actor / Outcome Model

| Actor | Current Outcome |
| --- | --- |
| 신규/복귀 작가 | login과 project console을 통해 프로젝트를 생성/정리하고 editor shell로 복귀한다. |
| 자유 메모형 작가 | note workspace에서 자동 개입 없이 메모를 쌓고 필요할 때만 brainstorming/lore/serialization으로 복제한다. |
| 정원사형 작가 | brainstorming workspace에서 자유 덤프를 쌓고 review queue를 거쳐 lore로 구조화한다. |
| 건축가형 작가 | plotboard와 lore wiki를 왕복하며 relation과 worldview surface를 조정한다. |
| 연재 작가 | serialization workspace에서 lint, structure metadata, reviewable AI를 함께 사용한다. |
| 설정 큐레이터 | lore wiki에서 article, metadata, promotion state를 관리하고 plotboard로 이동한다. |

## 5. E2E Flows

### `FLOW-ENTRY-01` Project Open to Workspace Shell

- `Entry`: `/` login screen + project console
- `Path`: 로그인 -> project create/rename/delete/open -> `/editor/[id]` 진입 -> AppHeader / WorkspaceModeNav / EditorLayout / ToolboxPanel이 로드된다
- `Current Surface`: LoginScreen, ProjectListScreen(create/open/rename/delete), AppHeader, WorkspaceModeNav, EditorLayout
- `Linked ARCH`: `ARCH-PRE-01`, `ARCH-APP-01`
- `Current Hold Boundary`: 외부 branding/copy alignment는 이 flow owner가 아니라 hygiene slice가 다룬다

### `FLOW-BRAIN-01` Brainstorm Dump to Lore Extraction

- `Entry`: editor `브레인스토밍` tab
- `Path`: 자유 덤프 작성 -> dump save/list -> extract 실행 -> worldview/history-event review candidate 생성 -> accept 시 lore document materialize + lore wiki focus -> lore/plotboard surface에서 후속 탐색
- `Current Surface`: brainstorming canvas, dump list, extract CTA, mixed review queue, lore wiki, plotboard
- `Linked ARCH`: `ARCH-PRE-01`, `ARCH-APP-01`, `ARCH-AI-01`, `ARCH-KNW-01`
- `Current Hold Boundary`: mixed review와 mock canonical evidence는 존재하지만, real-corpus ideation/manual product-feel validation은 아직 out of closeout 상태다

### `FLOW-NOTE-01` Note Capture and Explicit Handoff

- `Entry`: editor `노트` tab
- `Path`: `Folder > Note` tree 로드 -> note 작성/autosave -> assistant/lint 없이 scratchpad 유지 -> 명시적 CTA로 brainstorming/lore/serialization에 복제 -> payload-based status를 확인하고 같은 note에 머문다
- `Current Surface`: note tree, compact note header, export panel, success/error handoff status, note canvas, autosave status, compact-label mobile move fallback
- `Linked ARCH`: `ARCH-PRE-01`, `ARCH-EDT-01`, `ARCH-APP-01`, `ARCH-PER-01`
- `Current Hold Boundary`: real-corpus/manual large-tree validation과 cross-workspace handoff feel validation은 아직 남아 있다

### `FLOW-SERIAL-01` Serialization Writing and Reviewable AI

- `Entry`: editor `작품 연재` tab
- `Path`: chapter 선택/작성 -> structure save 시 saved-state regrouping/branch auto-open -> desktop drag reorder/group move 또는 mobile move fallback -> canonical lint count/detail/redline sync -> BubbleMenu polish 또는 assistant 요청 -> reviewable apply/reject
- `Current Surface`: writing-first serialization canvas, summary-first chapter structure sidebar, drag handle/drop indicator/group move, mobile move fallback, error list, assistant panel, BubbleMenu
- `Linked ARCH`: `ARCH-PRE-01`, `ARCH-EDT-01`, `ARCH-AI-01`, `ARCH-PER-01`
- `Current Hold Boundary`: real-corpus large chapter-count/manual authoring feel, rename/bulk organization semantics validation, BubbleMenu/narrow product-feel closeout은 아직 남아 있다

### `FLOW-LORE-PLOT-01` Lore Wiki and Plotboard Round-Trip

- `Entry`: editor `로어 백과` tab 또는 `플롯보드` tab
- `Path`: lore wiki index/article 탐색 -> advanced disclosure로 metadata/promotion 확인 -> plotboard relation editor 또는 worldview/graph/timeline로 이동 -> persisted graph layout과 staged relation editor를 거쳐 focused lore document state로 다시 복귀
- `Current Surface`: Lore Wiki Index, article canvas, folded metadata rail, plotboard worldview surface, persisted relation graph, same-doc focus, reset-view control, timeline, staged relation editor
- `Linked ARCH`: `ARCH-PRE-01`, `ARCH-KNW-01`, `ARCH-PER-01`
- `Current Hold Boundary`: lore/wiki real-corpus validation과 plotboard graph feel/manual validation closeout은 아직 남아 있다

## 6. Coverage Mapping

| Feature ID | Canonical Docs | Primary ARCH | Primary WO | Test / Evidence Anchor |
| --- | --- | --- | --- | --- |
| `FEAT-ENTRY-01` | `feature.md`, `mechanism.md`, `sprint.md` | `ARCH-PRE-01`, `ARCH-APP-01` | `WO-PRE-CORE-001`, `WO-UX-007`, `WO-UX-014`, `WO-UX-015` | `frontend/e2e/brainstorm-to-lore.spec.ts` |
| `FEAT-NOTE-01` | `feature.md`, `topology.md`, `mechanism.md`, `sprint.md`, `roadmap.md` | `ARCH-PRE-01`, `ARCH-EDT-01`, `ARCH-APP-01`, `ARCH-PER-01` | `WO-PRE-CORE-003` | `tests/backend/api/test_notes.py`, `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/phase-a-mobile-390.spec.ts` |
| `FEAT-BRAIN-01` | `feature.md`, `mechanism.md`, `sprint.md`, `roadmap.md` | `ARCH-PRE-01`, `ARCH-AI-01`, `ARCH-APP-01` | `WO-PRE-CORE-002`, `WO-AI-005` | `frontend/e2e/brainstorm-to-lore.spec.ts`, `frontend/e2e/phase-a-hardening.spec.ts` |
| `FEAT-PLOT-01` | `feature.md`, `mechanism.md`, `sprint.md`, `roadmap.md` | `ARCH-PRE-01`, `ARCH-KNW-01`, `ARCH-PER-01` | `WO-VIZ-001`, `WO-VIZ-002`, `WO-IA-001` | `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/phase-a-mobile-390.spec.ts`, `tests/backend/api/test_lore.py` |
| `FEAT-SERIAL-01` | `feature.md`, `mechanism.md`, `sprint.md`, `roadmap.md` | `ARCH-PRE-01`, `ARCH-EDT-01`, `ARCH-AI-01`, `ARCH-PER-01` | `WO-PRE-CORE-002`, `WO-UX-012`, `WO-IA-002`, `WO-AI-004` | `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/serialization-assistant.spec.ts`, `tests/backend/api/test_chapters.py` |
| `FEAT-LORE-01` | `feature.md`, `topology.md`, `mechanism.md`, `sprint.md`, `roadmap.md` | `ARCH-KNW-01`, `ARCH-PRE-01`, `ARCH-PER-01` | `WO-PRE-CORE-002`, `WO-IA-001` | `frontend/e2e/lore-wiki-large-corpus.spec.ts`, `tests/backend/api/test_lore.py` |
| `FEAT-AI-01` | `feature.md`, `topology.md`, `mechanism.md`, `sprint.md`, `roadmap.md` | `ARCH-AI-01`, `ARCH-PRE-01`, `ARCH-STR-03` | `WO-AI-003`, `WO-AI-004`, `WO-AI-005`, `WO-AI-006` | `frontend/e2e/serialization-assistant.spec.ts`, `tests/backend/api/test_assistant.py` |

## 7. Intentional Hold Inventory

| Hold Item | Why It Is Not A Current Core Blocker | Owning Canonical Docs |
| --- | --- | --- |
| pure note workspace real-corpus/manual validation | note tree, autosave, compact-label mobile move fallback, selected-note context recovery baseline은 live라서 current product use는 가능하다 | `feature.md`, `roadmap.md`, `sprint.md`, `mechanism.md` |
| pure note real-corpus handoff feel validation | payload-based success copy, success/error tone split, draft reset, same-note stationary handoff semantics은 live지만 real-user wording 검증은 더 다듬을 수 있다 | `feature.md`, `roadmap.md`, `sprint.md` |
| plotboard real-corpus graph feel / viewport polish | persisted layout, category-clustered fallback, same-doc focus, reset-view, narrow staged authoring이 live라 현재 접근성 blocker는 닫혔고, 남은 과제는 실제 corpus에서의 그래프 체감과 manual validation closeout이다 | `feature.md`, `roadmap.md`, `sprint.md`, `mechanism.md` |
| lore wiki real-corpus scale/perf validation | grouped index와 large-corpus mock smoke는 확보되어 기본 UX는 live다 | `feature.md`, `roadmap.md`, `sprint.md`, `mechanism.md` |
| serialization large-count organization polish | Part/BK/EP baseline, summary-first left rail, saved-state regrouping, desktop drag reorder/group move, mobile move fallback, dedicated move endpoint는 live라서 production writing flow는 이미 열린 상태다 | `feature.md`, `roadmap.md`, `sprint.md`, `mechanism.md` |
| assistant real-user product-fit tuning | compact reply baseline, minimal quick prompts, reviewable polish flow는 live라서 feature 자체는 사용 가능하다 | `feature.md`, `roadmap.md`, `sprint.md`, `mechanism.md` |
| BubbleMenu quality hardening on narrow/long-tail cases | preset/custom polish와 validation contract는 live라서 core editing loop는 이미 동작한다 | `feature.md`, `roadmap.md`, `sprint.md` |
