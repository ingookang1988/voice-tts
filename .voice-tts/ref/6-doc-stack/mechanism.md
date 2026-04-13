# Odys Studio Mechanism (V4)

- Role: 현재 시스템의 작동 사실과 evidence 기록
- Source Type: As-Is / Mechanism
- Baseline Date: 2026-03-30 (KST)
- Current Phase: Phase A Closed / Phase B Find & Replace Perfection Active
- Update Trigger: 코드 사실, route, path, dependency, 테스트, limitation이 바뀔 때
- Excluded Content: 장기 roadmap, 구조 규범, 우선순위 결정

## 1. As-Is Snapshot

| Capability | Status | Current Fact | Evidence |
| --- | --- | --- | --- |
| Documentation Stack | `working` | `.odys/` 아래 6문서가 존재하고, current live product map은 `feature.md`, 구조 규범은 `topology.md`, runtime fact와 evidence는 `mechanism.md`, execution backlog는 `sprint.md`가 소유한다. `.plan/` 문서는 background reference로 남는다. | `.odys/odys.md`, `.odys/roadmap.md`, `.odys/feature.md`, `.odys/topology.md`, `.odys/mechanism.md`, `.odys/sprint.md` |
| Workspace Shell | `working` | editor route에서 6 workspace mode를 switch하며 AppHeader, WorkspaceModeNav, EditorLayout, ToolboxPanel, SerializationAssistantPanel을 조합한다. note mode는 dedicated panel과 `NOTE_TOOLS`를 사용하되 fullscreen/focus에서도 left panel과 toolbox shell을 유지해 brainstorming/serialization과 같은 editor grammar를 따른다. mobile/narrow-width에서는 compact mode-switcher sheet를 쓰고, workspace list drawer / toolbox overlay / mode switcher가 하나의 mobile overlay context에서 mutually exclusive하게 동작한다. | `frontend/src/app/editor/[id]/page.tsx`, `frontend/src/app/globals.css`, `frontend/tailwind.config.js`, `frontend/src/widgets/AppHeader/index.tsx`, `frontend/src/widgets/WorkspaceModeNav/index.tsx`, `frontend/src/widgets/EditorLayout/index.tsx`, `frontend/src/widgets/EditorLayout/mobile-chrome.tsx`, `frontend/src/widgets/ToolboxPanel/index.tsx`, `frontend/src/widgets/ToolboxPanel/tools.tsx`, `frontend/src/widgets/SerializationAssistantPanel/index.tsx` |
| Pure Note Workspace | `working` | note workspace는 `Folder > Note` tree, autosave-only authoring, compact note header, explicit `내보내기` handoff(`brainstorming` / `lore` / `serialization`), assistant/error tool 부재, compact-label full-width mobile move fallback을 제공한다. note API contract와 autosave/handoff logic은 `entities/features`로 이동했고, handoff는 single-call BFF endpoint를 사용한다. handoff status는 returned payload 기준 success/error tone으로 노출되고, 성공 후 export panel은 닫히며 같은 note selection/content는 유지된다. tree hydrate/select/move 뒤에는 선택 note를 다시 scroll into view하여 context를 유지한다. action chrome은 save `아이콘 + 텍스트`, edit/delete icon-only, folder expand chevron/title-only로 sharpen되었고 neutral icon + 한글화 polish도 유지된다. 남은 과제는 real-corpus/manual large-tree 및 handoff product-feel validation이다. | `frontend/src/widgets/WorkspaceNote/index.tsx`, `frontend/src/entities/note/api/notes.ts`, `frontend/src/features/note-content-save/model/useNoteAutoSave.ts`, `frontend/src/features/note-handoff/model.ts`, `src/backend/presentation/api/routers/notes.py`, `src/backend/application/notes/use_cases/`, `src/backend/domain/notes/entities.py`, `tests/backend/api/test_notes.py`, `tests/backend/test_note_service.py`, `tests/backend/architecture/test_notes_lore_slice_architecture.py`, `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/phase-a-mobile-390.spec.ts` |
| Entry Screens | `working` | login과 project list는 glass/landing 톤에서 editor-console 진입 화면으로 재구성되었고, project console은 create/open에 더해 inline title rename과 project-scoped delete를 제공한다. contract는 stable `data-testid`와 mock-backed Playwright smoke에 연결된다. | `frontend/src/widgets/Auth/ui/LoginScreen.tsx`, `frontend/src/widgets/ProjectList/ui/ProjectListScreen.tsx`, `frontend/src/shared/api/projects.ts`, `src/backend/presentation/api/routers/projects.py`, `tests/backend/api/test_projects_brainstorm.py`, `frontend/e2e/brainstorm-to-lore.spec.ts` |
| Plotboard Main Area | `working` | worldview cards는 explicit `worldview_promoted` + stored `summary`를 사용하는 projection으로 분리되었고, graph는 explicit relations를 렌더링하며 desktop/tablet direct-connect draft, clickable edge edit pill, inbound source-edit jump, lore wiki round-trip을 side sheet에서 지원한다. read path는 aggregate BFF `plotboard-view`를 사용하고, node position은 `plotboard-layout` write path로 서버에 저장되어 재진입 시 복원된다. 저장 좌표가 없는 문서는 category-clustered fallback layout으로 배치되고, graph viewport는 graph 첫 진입/문서 집합 변경 때만 refit되며 selected lore focus는 session-local viewport snapshot과 medium-zoom center path를 사용한다. `전체 보기` reset control, dense graph overlay-safe top gutter, selected-edge emphasis, narrow-width minimap hide도 유지된다. persisted mutation은 source lore의 `relations` save path를 통과하고, relation editor는 요약 -> 관계 목록 -> 편집 순서의 staged disclosure를 사용하며, narrow-width에서는 bottom-sheet/stacked authoring으로 내려간다. relation taxonomy preset, semantic legend/color, 정렬된 row hierarchy, free-text custom relation도 유지된다. | `frontend/src/widgets/WorkspacePlotboard/index.tsx`, `frontend/src/widgets/Workspaces/ui/LoreGraph.tsx`, `frontend/src/widgets/Workspaces/ui/loreRelationTaxonomy.ts`, `frontend/src/features/plotboard-graph/model.ts`, `frontend/src/entities/lore/api/lore.ts`, `src/backend/presentation/api/routers/lore.py`, `src/backend/application/lore/use_cases/`, `src/backend/alembic/versions/d1f2e3c4b5a6_add_plotboard_layout_to_lore_documents.py`, `tests/backend/api/test_lore.py` |
| Lore Wiki UX | `working` | lore wiki는 left sidebar `Lore Wiki Index` + article-first main canvas + explicit edit mode로 재구성되었고, summary/promotion/wiki metadata/body의 source surface가 되며 relation summary는 read-only이고 plotboard relation editor와 동일 문서 round-trip을 지원한다. lore wiki만 widened left panel width(`320px`)를 사용하고, sidebar는 `Promoted / Working / Library` grouped index, advanced disclosure, folded metadata/stat preview, long-list/no-results state를 제공한다. article view의 metadata rail도 secondary disclosure로 접힌 상태에서 시작한다. lore wiki 표현부는 `WorkspaceLoreWiki` 아래로 이동했고 shared lore presentation helper는 entity layer가 소유한다. | `frontend/src/widgets/WorkspaceLoreWiki/index.tsx`, `frontend/src/widgets/WorkspaceLoreWiki/ui/LoreWiki.tsx`, `frontend/src/entities/lore/model/presentation.ts`, `frontend/src/entities/lore/api/lore.ts`, `frontend/src/entities/novel/model/store.ts`, `src/backend/application/lore/use_cases/`, `src/backend/alembic/versions/c0f7e1b6a12d_add_lore_wiki_fields.py`, `frontend/e2e/lore-wiki-large-corpus.spec.ts` |
| Serialization QA Sync | `working` | lint detail source는 current chapter의 `trackChange` mark로 재배선되었고, editor mount 전에는 saved chapter HTML의 `data-suggestion` / `data-reason` fallback을 사용한다. serialization runtime composition은 dedicated widget으로 분리되었다. | `frontend/src/widgets/TiptapCanvas/model/track-change-errors.ts`, `frontend/src/widgets/TiptapCanvas/model/editor-store.ts`, `frontend/src/widgets/TiptapCanvas/ui/ErrorListPanel.tsx`, `frontend/src/widgets/TiptapCanvas/ui/core/components/editor.tsx`, `frontend/src/widgets/WorkspaceSerialization/index.tsx` |
| Serialization Structure Sidebar | `working` | serialization left panel은 chapter metadata에서 derived `Part > BK > Chapter` 트리를 만들고, 기본 상태에서는 현재 구조 summary와 single-select EP cross-filter를 보여준다. 선택 챕터의 `Part/BK/EP` 메타데이터는 explicit `구조 편집`을 열었을 때만 수정하며, structure draft는 synchronous ref를 source-of-truth로 사용해 save 시 stale batched state에 의존하지 않는다. save 후에는 same saved payload를 기준으로 summary, active chapter row, grouped tree가 함께 즉시 갱신되고, active chapter가 다른 `Part/BK`로 이동하면 목적지 branch를 자동으로 펼치며 active chapter를 계속 visible 상태로 유지한다. desktop에서는 drag handle + before/after/group drop indicator로 chapter reorder/group move를 수행하고, mobile에서는 compact-label full-width move fallback으로 같은 intent를 수행한다. 신규 챕터는 latest saved `Part/BK`를 상속하고 EP는 빈 태그 배열로 시작한다. 이 slice는 FE `entities/features/widgets` 분리와 BE pure-domain/application/repository 경계, dedicated chapter move endpoint로 재배선되었다. | `frontend/src/widgets/WorkspaceSerialization/index.tsx`, `frontend/src/entities/chapter/api/chapters.ts`, `frontend/src/entities/chapter/model/grouping.ts`, `frontend/src/features/chapter-organize/model.ts`, `frontend/src/features/chapter-metadata-edit/model.ts`, `src/backend/presentation/api/routers/chapters.py`, `src/backend/application/chapters/use_cases/`, `src/backend/domain/chapters/entities.py`, `src/backend/domain/chapters/repositories.py`, `src/backend/infrastructure/persistence/chapters_repository.py`, `src/backend/infrastructure/persistence/sqlmodel/chapters.py`, `src/backend/alembic/versions/a7b1c9d4e2f0_add_serialization_units_to_chapters.py`, `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/phase-a-mobile-390.spec.ts`, `tests/backend/api/test_chapters.py`, `tests/backend/test_chapter_service.py`, `tests/backend/architecture/test_chapter_slice_architecture.py` |
| Architecture DDD Slices | `partial` | chapter에 이어 notes/lore/brainstorm slice도 pure domain entity/value object/repository port, application service/DTO, infrastructure mapper/repository로 나뉘고 router는 HTTP mapping만 담당한다. assistant lore/brainstorm read도 application service를 통해 로드한다. legacy surface와 일부 cross-cutting leftover는 아직 남아 있다. | `src/backend/domain/chapters/entities.py`, `src/backend/domain/notes/entities.py`, `src/backend/domain/lore/entities.py`, `src/backend/domain/brainstorm/entities.py`, `src/backend/domain/chapters/value_objects.py`, `src/backend/domain/notes/value_objects.py`, `src/backend/domain/lore/value_objects.py`, `src/backend/application/chapters/use_cases/`, `src/backend/application/notes/use_cases/`, `src/backend/application/lore/use_cases/`, `src/backend/application/brainstorm/use_cases/`, `src/backend/infrastructure/persistence/chapters_repository.py`, `src/backend/infrastructure/persistence/notes_repository.py`, `src/backend/infrastructure/persistence/lore_repository.py`, `src/backend/infrastructure/persistence/brainstorm_repository.py`, `src/backend/presentation/api/routers/chapters.py`, `src/backend/presentation/api/routers/notes.py`, `src/backend/presentation/api/routers/lore.py`, `src/backend/presentation/api/routers/brainstorm.py`, `src/backend/presentation/api/routers/assistant.py`, `tests/backend/architecture/test_chapter_slice_architecture.py`, `tests/backend/architecture/test_notes_lore_slice_architecture.py`, `tests/backend/architecture/test_brainstorm_slice_architecture.py`, `tests/backend/test_chapter_service.py`, `tests/backend/test_note_service.py`, `tests/backend/test_lore_service.py`, `tests/backend/test_brainstorm_service.py` |
| Workspace FSD Slices | `partial` | serialization에 이어 note/lore/plotboard/brainstorm도 dedicated widget로 옮겨졌고 business contract/autosave/handoff/relation/promotion/extract logic이 `entities/features/widgets`로 이동했다. composition root는 onboarding까지 포함해 새 widget를 직접 참조하고, `widgets/Workspaces` barrel은 제거되었다. 남은 `widgets/Workspaces/ui/*`는 shared presentational surface다. | `frontend/src/app/editor/[id]/page.tsx`, `frontend/src/widgets/WorkspaceOnboarding/index.tsx`, `frontend/src/widgets/WorkspaceSerialization/index.tsx`, `frontend/src/widgets/WorkspaceNote/index.tsx`, `frontend/src/widgets/WorkspaceBrainstorm/index.tsx`, `frontend/src/widgets/WorkspacePlotboard/index.tsx`, `frontend/src/widgets/WorkspaceLoreWiki/index.tsx`, `frontend/src/widgets/WorkspaceLoreWiki/ui/LoreWiki.tsx`, `frontend/src/entities/lore/model/presentation.ts`, `frontend/src/entities/brainstorm/api/brainstorm.ts`, `frontend/src/entities/chapter/api/chapters.ts`, `frontend/src/entities/note/api/notes.ts`, `frontend/src/entities/lore/api/lore.ts`, `frontend/src/features/chapter-content-save/model/useChapterAutoSave.ts`, `frontend/src/features/note-content-save/model/useNoteAutoSave.ts`, `frontend/src/features/note-handoff/model.ts`, `frontend/src/features/lore-promotion/model.ts`, `frontend/src/features/lore-relation-edit/model.ts`, `frontend/src/features/lore-wiki-edit/model.ts`, `frontend/src/entities/chapter/model/grouping.test.ts`, `frontend/src/entities/note/model/tree.test.ts`, `frontend/src/features/note-handoff/model.test.ts`, `frontend/src/features/lore-promotion/model.test.ts`, `frontend/.eslintrc.json` |
| Workspace BFF Surface | `partial` | `/api/v1/projects`는 project console의 create/list/update/delete contract를 제공하고, `/api/v1/chapters`, `/api/v1/assistant`에 더해 notes handoff BFF(`note -> brainstorm/lore/serialization`), chapter move BFF(`POST /api/v1/chapters/{project_id}/move`), lore aggregate read/write BFF(`plotboard-view`, `plotboard-layout`), brainstorm CRUD/extract BFF가 frontend workflow에 맞춘 stable contract를 제공하면서 내부 domain/application/repository mapping 뒤로 persistence를 숨긴다. legacy `/api/chat`/`history`/`database`/`documents`는 기본값으로는 비활성화되고 `ENABLE_LEGACY_API_ROUTES=true`일 때만 노출되는 deprecated backend compatibility surface로 분리되었으며, frontend legacy compatibility consumer(`UploadTab`, `legacy-graphrag`)는 repo에서 제거되었다. | `src/backend/presentation/api/routers/projects.py`, `src/backend/presentation/api/routers/chapters.py`, `src/backend/presentation/api/routers/notes.py`, `src/backend/presentation/api/routers/lore.py`, `src/backend/presentation/api/routers/brainstorm.py`, `src/backend/presentation/api/routers/assistant.py`, `src/backend/presentation/api/dependencies/notes.py`, `src/backend/presentation/api/dependencies/lore.py`, `src/backend/presentation/api/dependencies/brainstorm.py`, `src/backend/application/chapters/use_cases/`, `src/backend/application/notes/use_cases/`, `src/backend/application/lore/use_cases/`, `src/backend/application/brainstorm/use_cases/`, `src/backend/application/agents/serialization_assistant.py`, `frontend/.eslintrc.json`, `tests/backend/test_app_factory.py`, `tests/backend/api/test_chapters.py`, `tests/backend/api/test_notes.py`, `tests/backend/api/test_lore.py`, `tests/backend/api/test_projects_brainstorm.py`, `tests/backend/api/test_assistant.py`, `tests/backend/test_brainstorm_service.py`, `tests/backend/architecture/test_brainstorm_slice_architecture.py` |
| Agent Pipeline | `working` | lore + pacing streaming analysis와 reviewable polish flow는 유지되며, assistant chat contract는 serialization/brainstorming 둘 다 지원하고 mode별 system prompt와 conservative completion budget을 사용한다. chat 최종 답변은 deterministic normalizer를 거쳐 기본적으로 `진단 1문장 + 실행 제안 최대 3개` 형식으로 정리되고, expanded 요청일 때만 더 길어진다. FE assistant panel은 markdown을 렌더링하고, empty state/quick prompt/input hierarchy도 minimal disclosure 기준으로 재정렬되었다. | `src/backend/application/agents/graph_orchestrator.py`, `src/backend/application/agents/serialization_assistant.py`, `src/backend/presentation/api/routers/assistant.py`, `frontend/src/widgets/SerializationAssistantPanel/index.tsx` |
| Automated Tests | `partial` | reopened Phase A slices를 보호하는 backend integration과 frontend Playwright spec은 존재한다. 2026-03-30 local rerun에서는 frontend `npx tsc --noEmit`, focused Jest pack(`plotboard-graph`, `brainstorm-extract-review`, `note tree`, `chapter grouping`), Playwright canonical pack(`lore-wiki-large-corpus`, `phase-a-hardening`, `phase-a-mobile-390`, `serialization-assistant`, `brainstorm-to-lore`, `hp1-canonical`, `hp1-mobile-390`)이 모두 green이었고 결과는 `19 pass / 0 fail`이다. 이번 세션에서는 `scripts/run-local-ci.ps1`가 `-PythonExecutable`을 받아 explicit supported Python `3.10`~`3.13` interpreter를 사용할 수 있게 되었고, `.\.tmp\manual-py312\Scripts\python.exe` 기준 backend `flake8` + deterministic pytest가 실제로 통과했다. supported interpreter로 `create_app(enable_startup_checks=True)`와 `/api/health/ready`도 동작하며, actual `Project #12` HP1 rerun은 brainstorm extract, note move/handoff, chapter save/move, lore relation round-trip, assistant chat/polish까지 수행되었다. 남은 제약은 full integration preflight가 여전히 Docker-backed test DB(`localhost:5433`) availability에 의존하고, local Neo4j persistence는 DNS resolution failure로 degraded라는 점이다. | `tests/backend/api/test_assistant.py`, `tests/backend/api/test_chapters.py`, `tests/backend/api/test_lore.py`, `tests/backend/api/test_notes.py`, `tests/backend/api/test_projects_brainstorm.py`, `tests/backend/test_chapter_service.py`, `tests/backend/test_note_service.py`, `tests/backend/test_lore_service.py`, `tests/backend/test_brainstorm_service.py`, `tests/backend/architecture/test_chapter_slice_architecture.py`, `tests/backend/architecture/test_notes_lore_slice_architecture.py`, `tests/backend/architecture/test_brainstorm_slice_architecture.py`, `frontend/src/features/plotboard-graph/model.test.ts`, `frontend/src/entities/chapter/model/grouping.test.ts`, `frontend/src/entities/note/model/tree.test.ts`, `frontend/src/features/brainstorm-extract-review/model.test.ts`, `frontend/src/features/note-handoff/model.test.ts`, `frontend/src/features/lore-promotion/model.test.ts`, `frontend/e2e/serialization-assistant.spec.ts`, `frontend/e2e/brainstorm-to-lore.spec.ts`, `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/phase-a-mobile-390.spec.ts`, `frontend/e2e/lore-wiki-large-corpus.spec.ts`, `frontend/e2e/hp1-canonical.spec.ts`, `frontend/e2e/hp1-mobile-390.spec.ts`, `frontend/e2e/support/ui-helpers.ts`, `frontend/e2e/support/odys-api-mocks.ts`, `frontend/src/widgets/ProjectList/ui/ProjectListScreen.tsx`, `frontend/src/features/chapter-content-save/model/useChapterAutoSave.ts`, `scripts/run-local-ci.ps1`, `scripts/run-local-e2e.ps1`, `frontend/playwright.config.ts`, `docs/REAL_CORPUS_VALIDATION_HP1.md` |
| Deployment Packaging | `working` | backend/frontend Dockerfile과 docker-compose orchestration은 유지되지만, backend web startup은 이제 Alembic migration을 직접 수행하지 않고 Postgres reachability + schema revision guardrail만 확인한다. Railway 운영선은 migration-first release flow와 proxy-first frontend(`/api/*`)를 기준으로 문서화되었다. | `Dockerfile.backend`, `Dockerfile.frontend`, `docker-compose.yml`, `Procfile`, `src/backend/main.py`, `src/backend/infrastructure/startup.py`, `src/backend/alembic/env.py`, `frontend/next.config.js`, `docs/RAILWAY_DEPLOYMENT.md` |

## 2. Capability Entries

### ARCH-PRE-01 [Frontend Workspace Shell]
- Status: `partial`
- Code Paths:
  - `frontend/src/app/editor/[id]/page.tsx`
  - `frontend/src/widgets/WorkspacePlotboard/index.tsx`
  - `frontend/src/widgets/WorkspaceNote/index.tsx`
  - `frontend/src/widgets/WorkspaceLoreWiki/index.tsx`
  - `frontend/src/widgets/AppHeader/index.tsx`
  - `frontend/src/widgets/WorkspaceModeNav/index.tsx`
  - `frontend/src/widgets/EditorLayout/index.tsx`
  - `frontend/src/widgets/ToolboxPanel/index.tsx`
  - `frontend/src/widgets/ToolboxPanel/tools.tsx`
  - `frontend/src/widgets/SerializationAssistantPanel/index.tsx`
  - `frontend/src/features/note-content-save/model/useNoteAutoSave.ts`
  - `frontend/src/app/globals.css`
  - `frontend/tailwind.config.js`
- Routes and Surfaces:
  - editor surface: `/editor/[id]`
  - workspace modes: onboarding, note, brainstorming, plotboard, serialization, lore-wiki
- Dependencies:
  - Next.js App Router
  - Zustand
  - Tiptap
  - Tailwind CSS
  - `@xyflow/react`
- Proof:
  - route shell이 `workspaceMode`에 따라 mode-specific shell을 렌더링한다.
  - note workspace는 dedicated panel을 사용하고 `NOTE_TOOLS`만 노출하며, assistant/error tool은 implicit default로 열리지 않는다.
  - brainstorming toolbox에는 assistant가 연결되고, serialization toolbox에는 assistant와 오류 목록이 연결된다.
  - lore wiki는 left sidebar `Lore Wiki Index`와 article-first main canvas를 사용하고, plotboard main area는 worldview/graph/timeline split을 제공한다.
  - plotboard/lore-wiki toolbox는 placeholder tool을 제거하고 실제 capability만 노출한다.
  - lore wiki <-> plotboard는 focused lore doc state를 공유하여 같은 문서로 왕복 이동한다.
  - note workspace는 `Folder > Note` tree, compact note header, explicit `내보내기` handoff CTA, mobile move fallback을 제공한다.
  - plotboard graph는 desktop/tablet에서 source handle -> target handle direct-connect draft를 열고, persisted relation save는 동일 side sheet form 경로를 재사용한다.
  - graph edge label은 clickable edit pill로 노출되고, inbound row는 source lore 기준 relation edit state로 점프할 수 있다.
  - 기본 left panel width는 `272px`, toolbox panel width는 `360px`이며 lore wiki만 `320px` left panel을 사용해 index 가독성을 높인다.
  - narrow-width에서는 left panel drawer, toolbox overlay, mode-switcher sheet가 single mobile overlay context에서 번갈아 열리며 동시에 겹치지 않는다.
  - graph view에서 lore side sheet가 열리면 desktop에서는 main surface가 right gutter를 남겨 graph와 editor를 함께 유지하고, narrow-width에서는 stacked/bottom-sheet authoring으로 내려가 한 손 동선을 유지한다.
  - shared shape token(`panel/card/control/chip`)과 sharper surface rule이 AppHeader, WorkspaceModeNav, ToolboxPanel, assistant panel, workspace banner 전반에 적용되어 편집 툴 톤을 맞춘다.
- Limits:
  - narrow access blocker는 닫혔지만 real-corpus lore scale/perf validation과 repeated manual validation은 더 필요하다.
  - pure note workspace baseline과 automated closeout evidence는 live지만, real-corpus/manual large-tree validation과 export/handoff product-feel validation은 더 필요하다.

### ARCH-EDT-01 [Editor State and Sync]
- Status: `working`
- Code Paths:
  - `frontend/src/entities/novel/model/store.ts`
  - `frontend/src/widgets/TiptapCanvas/model/editor-store.ts`
  - `frontend/src/widgets/TiptapCanvas/model/track-change-errors.ts`
  - `frontend/src/widgets/TiptapCanvas/model/extensions/TrackChanges.ts`
  - `frontend/src/widgets/TiptapCanvas/ui/TiptapCanvas.tsx`
  - `frontend/src/widgets/TiptapCanvas/ui/core/components/editor.tsx`
  - `frontend/src/features/chapter-content-save/model/useChapterAutoSave.ts`
  - `frontend/src/widgets/WorkspaceSerialization/index.tsx`
- Routes and Surfaces:
  - brainstorming content와 serialization content를 store level에서 분리
  - chapter/mode 전환 시 `pendingContent` bridge로 editor content를 주입
  - serialization lint detail은 editor doc 또는 saved chapter HTML fallback에서 복구
- Dependencies:
  - Zustand
  - Tiptap
  - custom TrackChanges extension
  - browser `DOMParser`
- Proof:
  - `TrackChanges` mark는 `data-suggestion`, `data-reason`, `data-severity`를 유지한다.
  - `extractTrackChangeErrorsFromDoc()`와 `extractTrackChangeErrorsFromHtml()`가 canonical lint detail을 계산한다.
  - `ErrorListPanel`은 `loreResult.logical_errors` 직독 대신 `canonicalLogicalErrors`를 읽는다.
  - chapter list와 상단 banner의 `logic_error_count`는 same canonical source에서 reconcile된다.
- Limits:
  - analyze result를 text span에 매핑하는 로직은 여전히 substring 기반이다.
  - DB에는 lint detail이 별도 structured field로 저장되지 않고 chapter HTML/trackChange markup에서 재구성된다.

### ARCH-APP-01 [Backend Application and Routing]
- Status: `partial`
- Code Paths:
  - `src/backend/main.py`
  - `src/backend/presentation/api/routers/assistant.py`
  - `src/backend/presentation/api/routers/brainstorm.py`
  - `src/backend/presentation/api/routers/lore.py`
  - `src/backend/presentation/api/routers/notes.py`
  - `src/backend/presentation/api/routers/chapters.py`
  - `src/backend/presentation/api/routers/projects.py`
- Routes and Surfaces:
  - Odys v1 surface: `/api/v1/projects`, `/api/v1/brainstorm`, `/api/v1/lore`, `/api/v1/notes`, `/api/v1/chapters`, `/api/v1/assistant`
  - legacy compatibility surface (deprecated + setting-gated, default disabled): `/api/chat`, `/api/database`, `/api/documents`, `/api/history`
  - health surface: `/api/health`
- Dependencies:
  - FastAPI
  - SQLModel
  - Pydantic
  - Loguru
  - Neo4j driver
- Proof:
  - `main.py`는 Odys v1 route와 legacy compatibility route를 별도 helper로 등록하고, legacy helper는 deprecated tag와 setting gate를 사용한다. 기본 app/OpenAPI는 legacy route를 등록하지 않고, opt-in 시 startup warning을 남긴다.
  - projects router는 create/list에 더해 `PATCH /api/v1/projects/{project_id}`, `DELETE /api/v1/projects/{project_id}`를 노출해 project console rename/delete를 지원한다.
  - assistant router는 `workspace_mode: "serialization" | "brainstorming"`를 허용한다.
  - brainstorming assistant는 `chapter_id` 없이 동작하며 recent dumps + lore summary를 context로 load한다.
  - lore router는 response/update contract에서 `summary`, `worldview_promoted`, `wiki_metadata`, `relations`, `updated_at`를 노출한다.
  - notes router는 folder + note tree payload와 explicit metadata/content update path를 노출한다.
  - chapters router는 DB session/ORM model을 직접 다루지 않고 application `ChapterService`와 DI dependency를 통해 request/response mapping만 수행한다.
- Limits:
  - application layer는 아직 hybrid product surface다.
  - legacy routes는 deprecated + setting-gated compatibility surface로 fenced 되었고 기본값은 비활성화다. 남은 과제는 opt-in caller audit와 eventual removal timing 정리다.

### ARCH-PER-01 [Persistence Boundary]
- Status: `partial`
- Code Paths:
  - `src/backend/domain/brainstorm/entities.py`
  - `src/backend/domain/chapters/entities.py`
  - `src/backend/application/brainstorm/use_cases/`
  - `src/backend/application/chapters/use_cases/`
  - `src/backend/infrastructure/persistence/sqlmodel/brainstorm.py`
  - `src/backend/infrastructure/persistence/sqlmodel/chapters.py`
  - `src/backend/infrastructure/persistence/brainstorm_repository.py`
  - `src/backend/infrastructure/persistence/chapters_repository.py`
  - `src/backend/alembic/versions/cb09a2d4eefc_add_ltee_multimode_tables.py`
  - `src/backend/alembic/versions/c0f7e1b6a12d_add_lore_wiki_fields.py`
  - `src/backend/infrastructure/database/neo4j_repository.py`
  - `src/backend/presentation/api/routers/brainstorm.py`
  - `src/backend/presentation/api/routers/lore.py`
  - `src/backend/presentation/api/routers/notes.py`
  - `src/backend/presentation/api/routers/chapters.py`
- Storage Roles:
  - Postgres: project, chapter, lore document, brainstorm dump, note folder, project note
  - Neo4j: lore extraction result의 event/worldview graph
- Dependencies:
  - SQLModel
  - Alembic
  - PostgreSQL
  - Neo4j
- Proof:
  - `NoteFolder`와 `ProjectNote`는 project-scoped folder / note tree와 autosave content를 저장한다.
  - chapter persistence는 infrastructure `ChapterRecord` + repository mapper가 담당하고, pure `Chapter` domain entity는 framework import 없이 `part_title`, `book_title`, `episode_tags` 규칙을 소유한다.
  - alembic revision `a7b1c9d4e2f0_add_serialization_units_to_chapters.py`가 chapter structural metadata를 backfill한다.
  - `LoreDocument`는 `summary`, `worldview_promoted`, `wiki_metadata`, `relations`, `plotboard_layout`, `updated_at`를 가진다.
  - alembic revision `c0f7e1b6a12d_add_lore_wiki_fields.py`가 lore wiki/promotion 필드와 initial backfill을 추가한다.
  - alembic revision `d1f2e3c4b5a6_add_plotboard_layout_to_lore_documents.py`가 lore document layout persistence 필드를 추가한다.
  - notes router는 project note의 folder move / reorder / content autosave와 non-empty folder delete guard를 제공한다.
  - `LoreDocument.relations` JSONB가 lore API response/update에 그대로 노출된다.
  - relation canonical shape는 `relations.edges[]`로 관리된다.
  - lore router는 `target_id` 존재 여부를 검증하고 self-edge를 거부하며 같은 `target_id + type` 중복을 제거한다.
  - lore router는 `worldview_promoted=true`일 때 non-history, canonical, non-empty summary를 강제하고 category-specific `wiki_metadata`만 허용한다.
  - chapters router는 `logic_error_count`를 derived cache처럼 유지한다.
  - projects router delete path는 note/chapter/lore/brainstorm의 project-scoped Postgres rows를 먼저 정리한 뒤 project row를 제거한다.
  - integration suite는 `TEST_POSTGRES_URI=postgresql://odys:odys@localhost:5433/odys_test` 계약을 사용한다.
- Limits:
  - worldview는 별도 table 없이 lore document의 explicit promotion metadata와 summary field를 사용한다.
  - relation taxonomy는 free-text이며 preset schema가 없다.
  - brainstorm/lore extract graph save path는 DNS-resolvable `NEO4J_URI`에 의존하며, Neo4j Aura host를 해석하지 못하면 SSE에 `Neo4j Save Error`를 남기고 Postgres-backed flow만 계속 진행한다.
  - deployment workflow/provider definition은 repo 밖에 있을 수 있다.

### ARCH-DOM-01 [Backend Domain DDD Boundary]
- Status: `partial`
- Code Paths:
  - `src/backend/domain/chapters/entities.py`
  - `src/backend/domain/notes/entities.py`
  - `src/backend/domain/lore/entities.py`
  - `src/backend/domain/chapters/value_objects.py`
  - `src/backend/domain/notes/value_objects.py`
  - `src/backend/domain/lore/value_objects.py`
  - `src/backend/domain/chapters/repositories.py`
  - `src/backend/domain/notes/repositories.py`
  - `src/backend/domain/lore/repositories.py`
  - `src/backend/application/chapters/dto.py`
  - `src/backend/application/notes/dto.py`
  - `src/backend/application/lore/dto.py`
  - `src/backend/application/chapters/use_cases/`
  - `src/backend/application/notes/use_cases/`
  - `src/backend/application/lore/use_cases/`
  - `src/backend/infrastructure/persistence/sqlmodel/chapters.py`
  - `src/backend/infrastructure/persistence/sqlmodel/notes.py`
  - `src/backend/infrastructure/persistence/sqlmodel/lore.py`
  - `src/backend/infrastructure/persistence/chapters_repository.py`
  - `src/backend/infrastructure/persistence/notes_repository.py`
  - `src/backend/infrastructure/persistence/lore_repository.py`
  - `src/backend/presentation/api/routers/chapters.py`
  - `src/backend/presentation/api/routers/notes.py`
  - `src/backend/presentation/api/routers/lore.py`
  - `tests/backend/architecture/test_chapter_slice_architecture.py`
  - `tests/backend/architecture/test_notes_lore_slice_architecture.py`
  - `tests/backend/test_chapter_service.py`
  - `tests/backend/test_note_service.py`
  - `tests/backend/test_lore_service.py`
- Routes and Surfaces:
  - chapter CRUD/stat/content/metadata/move surface: `POST/GET/PATCH/DELETE /api/v1/chapters/*`, `POST /api/v1/chapters/{project_id}/move`
  - note tree CRUD + handoff BFF surface: `GET/POST/PATCH/DELETE /api/v1/notes/*`, `POST /api/v1/notes/{project_id}/{note_id}/handoff/*`
  - lore CRUD + plotboard aggregate surface: `GET/POST/PATCH/DELETE /api/v1/lore/*`, `GET /api/v1/lore/{project_id}/plotboard-view`, `PUT /api/v1/lore/{project_id}/plotboard-layout`
  - assistant serialization context load path
- Dependencies:
  - dataclass-based domain models
  - application command DTO
  - repository port + SQLModel mapper adapter
- Proof:
  - chapter/notes/lore domain package는 framework-free entity/value object/repository port만 가진다.
  - chapter/notes/lore router는 DB session/ORM import 대신 application service를 사용한다.
  - chapter metadata patch semantics와 note/lore invariant는 application layer에서 보존된다.
  - assistant router의 lore/chapter context도 application service를 통해 읽는다.
- Limits:
  - legacy surface와 일부 cross-cutting leftover는 아직 같은 수준으로 정리되지 않았다.
  - repo-wide domain purity는 chapter + notes + lore + brainstorm proof 이후 leftover cleanup 단계다.

### ARCH-STR-02 [Frontend FSD Slice Ownership]
- Status: `partial`
- Code Paths:
  - `frontend/src/app/editor/[id]/page.tsx`
  - `frontend/src/widgets/WorkspaceSerialization/index.tsx`
  - `frontend/src/widgets/WorkspaceNote/index.tsx`
  - `frontend/src/widgets/WorkspacePlotboard/index.tsx`
  - `frontend/src/widgets/WorkspaceLoreWiki/index.tsx`
  - `frontend/src/entities/chapter/api/chapters.ts`
  - `frontend/src/entities/note/api/notes.ts`
  - `frontend/src/entities/lore/api/lore.ts`
  - `frontend/src/entities/chapter/model/grouping.ts`
  - `frontend/src/entities/chapter/model/normalize.ts`
  - `frontend/src/features/chapter-organize/model.ts`
  - `frontend/src/features/chapter-metadata-edit/model.ts`
  - `frontend/src/features/chapter-content-save/model/useChapterAutoSave.ts`
  - `frontend/src/features/note-content-save/model/useNoteAutoSave.ts`
  - `frontend/src/features/note-handoff/model.ts`
  - `frontend/src/features/lore-promotion/model.ts`
  - `frontend/src/features/lore-relation-edit/model.ts`
  - `frontend/src/features/lore-wiki-edit/model.ts`
  - `frontend/src/entities/chapter/model/grouping.test.ts`
  - `frontend/src/entities/note/model/tree.test.ts`
  - `frontend/src/features/note-handoff/model.test.ts`
  - `frontend/src/features/lore-promotion/model.test.ts`
- Routes and Surfaces:
  - editor serialization / note / plotboard / lore-wiki tabs
  - chapter metadata/grouping/autosave, note autosave/handoff, lore promotion/relation/wiki edit interaction
- Dependencies:
  - Next.js App Router
  - React
  - Zustand
  - entity-owned API client
- Proof:
  - editor composition root는 serialization/note/plotboard/lore 전용 widget를 직접 import한다.
  - chapter/note/lore API contract는 더 이상 `shared/api/*`가 아니라 entity layer가 소유한다.
  - note/chapter autosave와 note handoff, lore promotion/relation helper도 feature ownership으로 이동했다.
  - grouping/normalization/tree/promotion helper는 entity/model or feature layer에 있고 focused unit test가 추가되었다.
- Limits:
  - legacy `Workspaces` barrel은 제거되었지만 shared cross-workspace UI와 일부 shared/legacy cleanup은 아직 남아 있다.
  - boundaries lint config는 동작하지만 legacy selector warning이 남아 있다.

### ARCH-BFF-01 [Workspace BFF Surface]
- Status: `partial`
- Code Paths:
  - `src/backend/presentation/api/routers/chapters.py`
  - `src/backend/presentation/api/routers/notes.py`
  - `src/backend/presentation/api/routers/lore.py`
  - `src/backend/presentation/api/routers/assistant.py`
  - `src/backend/presentation/api/dependencies/notes.py`
  - `src/backend/presentation/api/dependencies/lore.py`
  - `src/backend/application/chapters/use_cases/`
  - `src/backend/application/notes/use_cases/`
  - `src/backend/application/lore/use_cases/`
  - `src/backend/application/agents/serialization_assistant.py`
  - `src/backend/infrastructure/persistence/chapters_repository.py`
  - `src/backend/infrastructure/persistence/notes_repository.py`
  - `src/backend/infrastructure/persistence/lore_repository.py`
  - `tests/backend/api/test_chapters.py`
  - `tests/backend/api/test_notes.py`
  - `tests/backend/api/test_lore.py`
  - `tests/backend/api/test_assistant.py`
- Routes and Surfaces:
  - `/api/v1/projects/*`
  - `/api/v1/chapters/*`
  - `/api/v1/chapters/{project_id}/move`
  - `/api/v1/notes/{project_id}/{note_id}/handoff/*`
  - `/api/v1/lore/{project_id}/plotboard-view`
  - `/api/v1/lore/{project_id}/plotboard-layout`
  - `/api/v1/assistant/chat`
  - `/api/v1/assistant/polish`
- Dependencies:
  - FastAPI transport models
  - application services and agent orchestration
  - dependency-injected repository adapter
- Proof:
  - projects router는 project console create/list/update/delete를 stable FE-facing contract로 노출한다.
  - chapter router는 stable FE-facing response shape를 유지하면서 내부 mapping을 application/service 뒤로 숨기고, dedicated move endpoint로 structure intent를 분리한다.
  - notes router는 tree CRUD와 note->brainstorm/lore/serialization handoff를 single-call BFF로 노출한다.
  - lore router는 plotboard aggregate read/write를 stable FE-facing payload로 노출하고 CRUD mutation은 lore service 뒤로 숨긴다.
  - assistant router는 workspace mode와 chapter context를 frontend workflow 기준으로 조합한다.
  - presentation layer는 migrated chapter/notes/lore slice에서 persistence adapter를 직접 노출하지 않는다.
- Limits:
  - legacy `/api/chat`, `/api/history`, `/api/database`, `/api/documents` surface는 `ENABLE_LEGACY_API_ROUTES=true`일 때만 등록되는 deprecated compatibility surface로 계속 공존한다.

### ARCH-AI-01 [Lore and Creative Assistance]
- Status: `partial`
- Code Paths:
  - `src/backend/application/agents/graph_orchestrator.py`
  - `src/backend/application/agents/lore_agent.py`
  - `src/backend/application/agents/pacing_agent.py`
  - `src/backend/application/agents/serialization_assistant.py`
  - `src/backend/presentation/api/routers/assistant.py`
  - `frontend/src/widgets/SerializationAssistantPanel/index.tsx`
  - `frontend/src/shared/store/assistant-store.ts`
  - `frontend/src/widgets/TiptapCanvas/ui/core/components/menus/text-menu/text-menu.tsx`
- Routes and Surfaces:
  - stream analysis: `POST /api/v1/lore/extract`
  - dump extraction: `POST /api/v1/brainstorm/{project_id}/{dump_id}/extract`
  - workspace assistant chat: `POST /api/v1/assistant/chat`
  - serialization text polish: `POST /api/v1/assistant/polish`
- Dependencies:
  - LangGraph
  - LangChain OpenAI
  - Pydantic
  - Tiptap
- Proof:
  - serialization/brainstorming assistant는 동일 SSE contract를 사용한다.
  - brainstorming assistant session key는 `projectId:brainstorming`이고 serialization은 chapter-scoped다.
  - backend prompt는 workspace mode별 규칙을 분리하고, 기본 응답 형식을 "짧은 진단 1문장 + 실행 가능한 제안 최대 3개"로 유도한다.
  - backend completion budget은 기본 응답에서 보수적으로 제한되고, explicit long-form 요청일 때만 확장된다.
  - assistant router는 `done.message`와 non-stream `message`에 deterministic compact normalizer를 적용해 decorated heading이나 과도한 bullet을 canonical compact output으로 정리한다.
  - FE assistant panel의 quick prompt와 helper copy는 compact reply policy를 직접 설명하고, serialization/brainstorming의 prompt 묶음을 분리한다.
  - BubbleMenu polish는 reviewable TrackChange flow를 유지하고, preset(`교정`/`확장`/`요약`)과 custom prompt composer가 같은 `POST /api/v1/assistant/polish` contract를 통해 TrackChange suggestion을 생성한다.
  - FE assistant panel은 `react-markdown` + `remark-gfm`으로 assistant markdown을 렌더링한다.
- Limits:
  - concise policy는 prompt + deterministic normalizer baseline이지만 schema-level structured contract는 아니다.
  - assistant history browser나 long-running conversation tooling은 없다.
  - analyze result mark mapping은 robust offset mapping이 아니다.

## 3. Core Dependency Map

### Frontend Runtime
| Dependency | Where It Matters | Current Role |
| --- | --- | --- |
| Next.js 14 App Router | `frontend/src/app/editor/[id]/page.tsx` | editor shell과 workspace route composition |
| React 18 | 전체 `frontend/src` | workspace UI, panel composition, transitions |
| Zustand | `frontend/src/entities/novel/model/store.ts`, `frontend/src/widgets/TiptapCanvas/model/editor-store.ts`, `frontend/src/shared/store/assistant-store.ts` | workspace content, editor UI state, assistant session state |
| Tiptap 3 | `frontend/src/widgets/TiptapCanvas/**` | editor, reviewable AI mark, serialization QA source |
| `@xyflow/react` | `frontend/src/widgets/Workspaces/ui/LoreGraph.tsx` | explicit relation graph rendering |
| Tailwind CSS | `frontend/src/**/*` | workspace UI styling |
| Playwright | `frontend/e2e/**` | mocked end-to-end regression |

### Backend Runtime
| Dependency | Where It Matters | Current Role |
| --- | --- | --- |
| FastAPI | `src/backend/main.py`, `src/backend/presentation/api/routers/*.py` | API surface composition |
| SQLModel | `src/backend/infrastructure/persistence/sqlmodel/brainstorm.py`, `src/backend/infrastructure/persistence/sqlmodel/chapters.py` | Postgres persistence and query layer |
| Alembic | `src/backend/alembic/versions/*.py` | schema evolution |
| PostgreSQL | chapters/lore/brainstorm tests and runtime | project/chapter/lore/dump record store |
| Neo4j | lore/brainstorm extract save path | narrative graph persistence |
| LangGraph / LangChain OpenAI | `src/backend/application/agents/*.py` | lore analysis, pacing analysis, assistant chat |
| pytest | `tests/backend/**` | backend regression |

## 4. Canonical Test and Verification Entry Points

### Local Bootstrap
1. backend integration DB:
   - `docker compose up -d postgres-test`
2. frontend dependencies:
   - `cd frontend && npm ci`
3. backend venv entry:
   - `.\venv\Scripts\python.exe`

### Frontend Checks
- Type check:
  - `cd frontend`
  - `.\node_modules\.bin\tsc.cmd --noEmit -p .\tsconfig.json`
- Lint:
  - `cd frontend`
  - `npm run lint`
- Targeted E2E:
  - `cd frontend`
  - `.\node_modules\.bin\playwright.cmd test --workers=1 serialization-assistant.spec.ts brainstorm-to-lore.spec.ts phase-a-hardening.spec.ts phase-a-mobile-390.spec.ts lore-wiki-large-corpus.spec.ts`

### Next Session Local Verification Entry
1. local orchestration scripts:
   - `scripts/run-local-ci.ps1`
   - `scripts/run-local-e2e.ps1`
2. Playwright runtime config:
   - `frontend/playwright.config.ts`
3. mocked backend contract:
   - `frontend/e2e/support/odys-api-mocks.ts`
4. reopened Phase A scenario:
   - `frontend/e2e/phase-a-hardening.spec.ts`
5. lore scale regression scenario:
   - `frontend/e2e/lore-wiki-large-corpus.spec.ts`
6. local reproduction command:
   - `powershell -ExecutionPolicy Bypass -File .\scripts\run-local-e2e.ps1`
7. supported backend verification command:
   - `powershell -ExecutionPolicy Bypass -File .\scripts\run-local-ci.ps1 -SkipFrontend -SkipIntegration -PythonExecutable .\.tmp\manual-py312\Scripts\python.exe`

### 2026-03-30 Phase A Loop 5 Blocker Closeout Note
1. local verification:
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npx jest src/features/brainstorm-extract-review/model.test.ts src/entities/note/model/tree.test.ts src/entities/chapter/model/grouping.test.ts --runInBand`
   - `cd frontend && npx playwright test e2e/lore-wiki-large-corpus.spec.ts e2e/phase-a-hardening.spec.ts e2e/phase-a-mobile-390.spec.ts e2e/serialization-assistant.spec.ts e2e/brainstorm-to-lore.spec.ts --workers=1`
2. surfaced implementation:
   - brainstorm extract review는 `worldview_updates`뿐 아니라 `events`를 `history` lore candidate로 materialize하고, accept 시 lore wiki focus로 이어진다.
   - note mobile move와 serialization mobile move는 우측 좁은 column 대신 카드 하단 full-width action row를 사용하고, select option은 compact label 기준으로 축약된다.
   - serialization structure save는 synchronous draft ref를 기준으로 저장되어 save 직후 summary, active chapter metadata, destination `Part/BK` auto-open, active chapter visibility가 함께 맞춰진다.
   - Playwright mock contract는 event-only extraction payload와 long-label note/chapter dataset을 포함해 `390` affordance를 직접 검증한다.
3. remaining gap:
   - local backend targeted pytest는 Python `3.14` + SQLAlchemy PostgreSQL dialect version-probe 문제로 여전히 blocked다.
   - HP1 real-corpus manual rerun은 blocker closeout 코드 반영 이후 follow-up pending 상태다.

### 2026-03-30 Phase A Closure Validation Note
1. local verification:
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npx jest src/features/plotboard-graph/model.test.ts src/features/brainstorm-extract-review/model.test.ts src/entities/note/model/tree.test.ts src/entities/chapter/model/grouping.test.ts --runInBand`
   - `cd frontend && npx playwright test e2e/lore-wiki-large-corpus.spec.ts e2e/phase-a-hardening.spec.ts e2e/phase-a-mobile-390.spec.ts e2e/serialization-assistant.spec.ts e2e/brainstorm-to-lore.spec.ts --workers=1`
   - `powershell -ExecutionPolicy Bypass -File .\scripts\run-local-ci.ps1 -SkipFrontend`
2. surfaced implementation:
   - plotboard graph는 저장 좌표가 없는 lore 문서에 category-clustered fallback layout을 적용하고, relation degree와 `worldview_promoted` 우선순위를 기준으로 cluster 중심 배치를 고정한다.
   - graph viewport는 graph 첫 진입 또는 문서 집합 변경 때만 `fitView`를 수행하고, 이후 selection/lore wiki round-trip/relation save/layout persistence에서는 session-local viewport snapshot과 selected-doc medium-zoom focus를 사용해 jump를 줄인다.
   - dense corpus용 `전체 보기` reset control, overlay-safe top gutter, selected-edge emphasis, narrow-width minimap hide가 lore wiki <-> plotboard same-doc round-trip 및 `390` smoke와 함께 회귀 기준으로 추가되었다.
   - local backend verification path는 `scripts/run-local-ci.ps1` preflight에서 Python `3.10`~`3.13` supported matrix만 허용하도록 명시되었고, ad-hoc Python `3.12` startup은 Windows `ProactorEventLoop` + psycopg async PostgreSQL connectivity check에서 계속 막힌다.
3. remaining gap:
   - HP1 real-corpus manual rerun은 supported backend startup path가 아직 막혀 있어 재실행하지 못했다.
   - Phase A gate는 local canonical automation green 상태지만 real-corpus rerun evidence가 없어 `Yellow`를 유지한다.

### 2026-03-30 Supported Interpreter Recovery and HP1 Manual Validation Note
1. local verification:
   - `powershell -ExecutionPolicy Bypass -File .\scripts\run-local-ci.ps1 -SkipFrontend`
   - `powershell -ExecutionPolicy Bypass -File .\scripts\run-local-ci.ps1 -SkipFrontend -SkipIntegration -PythonExecutable .\.tmp\manual-py312\Scripts\python.exe`
   - `.\.tmp\manual-py312\Scripts\python.exe -m pytest tests/backend/test_app_factory.py tests/backend/test_startup_graph.py tests/backend/test_runtime.py -q`
   - `create_app(enable_startup_checks=True)` + `GET /api/health/ready`
2. surfaced implementation:
   - `scripts/run-local-ci.ps1`는 explicit `-PythonExecutable` path를 우선 사용하고, repo venv가 unsupported matrix에 걸릴 때는 supported interpreter 예시를 포함해 fail-fast 한다.
   - supported Python `3.12` 환경에서는 backend startup checks와 readiness path가 실제로 동작하며 `postgres/schema=healthy`, `graph=degraded`로 응답한다.
   - actual `Project #12` rerun에서는 HP1 dump extract가 `extracted`로 닫혔고, note move/handoff, chapter save/move, lore relation save/update + `plotboard-view` round-trip, assistant compact reply, reviewable polish suggestion까지 모두 확인되었다.
3. remaining gap:
   - full backend integration preflight는 여전히 `localhost:5433` test DB availability와 Docker Desktop에 의존한다.
   - local Neo4j persistence는 DNS resolution failure로 degraded이며 extract stream에는 `Neo4j Save Error`가 surfaced될 수 있다.

### 2026-03-30 Phase A Loop 6 HP1 Mock Canonical Note
1. local verification:
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npx playwright test e2e/lore-wiki-large-corpus.spec.ts e2e/phase-a-hardening.spec.ts e2e/phase-a-mobile-390.spec.ts e2e/serialization-assistant.spec.ts e2e/brainstorm-to-lore.spec.ts e2e/hp1-canonical.spec.ts e2e/hp1-mobile-390.spec.ts --workers=1`
2. surfaced implementation:
   - Playwright mock layer는 `corpusFamily: 'bern' | 'hp1'`를 지원하며, 기존 Bern fixture는 유지한 채 HP1 project/lore/brainstorm/chapter/note dataset을 별도 family로 추가했다.
   - `hp1-canonical`은 brainstorming extract -> lore accept -> lore wiki article -> plotboard focus -> relation add/edit의 desktop golden path를 Harry Potter 시나리오로 잠근다.
   - `hp1-mobile-390`은 lore wiki -> plotboard graph 조작, note mobile move fallback, serialization mobile move fallback과 long-label summary를 HP1 narrow-width 시나리오로 잠근다.
3. remaining gap:
   - HP1 mock canonical evidence는 local regression strength를 높였지만 real-corpus manual rerun을 대체하지 않는다.
   - Phase A gate는 여전히 supported backend startup path + actual `Project #12` rerun evidence가 있어야만 `Green`으로 올라간다.

### 2026-03-31 Phase A Loop 8 Setting Mode & Mobile Layout Hotfix
1. local verification:
   - `cd frontend && npx tsc --noEmit`
2. surfaced implementation:
   - 프로젝트의 개별 설정을 전역으로 관리하고 변경할 수 있도록 `WorkspaceMode`에 `setting` 모드를 추가하고, `WorkspaceModeNav` (데스크톱) 및 `AppHeader` (모바일)에 라우팅을 연동했다.
   - 단일 프로젝트 정보 조회를 위한 백엔드 `GET /api/v1/projects/{project_id}` 엔드포인트를 추가하고, 프론트엔드 모델 `ProjectSummary`, `ProjectUpdatePayload`를 맵핑했다.
   - 프로젝트 엔티티의 JSONB 타입 특권 필드인 `configs`를 활용하여 "1화 분량 목표 글자수(`targetWordCount`)" 등의 확장 설정값(meta values)을 안전하게 병합(`PATCH`)하는 로직을 백엔드에 추가했다.
   - 모바일 환경에서의 `EditorLayout` 좌측 패널 가로 너비(`leftPanelWidth`)를 기존 `min(92vw, 340px)`에서 `min(85vw, 320px)`로 축소 조정하여 좁은 화면(iPhone SE 등)에서 목록이 넓어져 우측으로 잘리는 UI 오버플로우를 완화했다.
3. remaining gap:
   - Project List (대시보드) 화면에서 프로젝트 설정으로 바로 진입하는 경로는 없고, 우선 작업실 내부(EditorPage)로 진입한 후에만 설정 모드로 접근할 수 있는 상태다.

### 2026-03-31 Phase A Loop 7 UX Fix Note
1. local verification:
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npx playwright test e2e/phase-a-mobile-390.spec.ts e2e/phase-a-hardening.spec.ts --workers=1`
2. surfaced implementation:
   - mobile workspace footer는 line-clamp와 min-height 제약으로 narrow viewport에서 contents-shift 없이 layout을 유지한다. (lore wiki `text-[11px]` 설명도 line-clamp-1 적용)
   - workspace nav panel은 note/chapter 선택 시 mobile overlay auto-close 되어 UX depth 이탈을 바로 반영한다.
   - `MobileWorkspaceRailToggle`의 최소 크기를 `44x44`로 주어 mobile tap target HIG 기준을 충족시켰다.
   - `AppHeader` 모드 스위처 시트의 `0.5rem` 여백을 `2px`로 줄여, 모바일 서브헤더 하단에 빈틈없이 붙도록 개선했다.
   - `EditorLayout`의 phone viewport에서 `leftPanel` 너비를 `min(92vw, 340px)` 및 `min-width: 280px`로 상향하여 리스트 항목이 지나치게 잘리는 현상을 완화했다.
   - editor rendering flicker는 `selectedNoteId` / `chapterId` transition 이전에 `pendingContent`를 set하여 Zustand store 갱신이 먼저 일어나도록 순서를 변경, content 주입 gap을 닫았다. (Fix-1 적용)
   - `editor.isEmpty` 빈 오버레이 노출도 `pendingContent === null` 조건으로 가드를 추가해 주입 중 깜빡임을 방지한다. (Fix-2 적용)
3. remaining gap:
   - Editor transition 과정에 pending opacity skeleton을 추가하는 polish 단계는 pending으로 남겨두었다.

### 2026-03-26 Verification Note
1. current closeout SHA:
   - `5560058`
2. local verification:
   - `cd frontend && npm run lint`
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npm run build`
   - `cd frontend && npm run test:e2e:local -- phase-a-hardening.spec.ts`
   - `cd frontend && npm run test:e2e:local -- brainstorm-to-lore.spec.ts`
   - `cd frontend && npm run test:e2e:local -- phase-a-mobile-390.spec.ts`
   - current-SHA rerun은 local-only single-worker 경로로 수행했고 모두 green이다.
3. traced root cause:
   - 앱 회귀보다 Playwright spec drift가 원인이었고, Lore Wiki / Plotboard / assistant UI 변경으로 placeholder, exact accessible name, markdown list rendering, worldview-vs-graph expectation, hidden mobile infobox DOM이 어긋나 있었다.
4. hosted verification:
   - GitHub-hosted `frontend-ci` run `23577979005`
   - run URL: `https://github.com/ingookang1988/odys-studio/actions/runs/23577979005`
   - `head_sha`: `e5928b30b8643de8ba88287430537d133c9a54b9`
   - run attempt: `1`
   - workflow duration: 약 `2m 36s`
   - job result: `build` success, `e2e` success
5. mock-backed manual smoke:
   - `1440`: 8-test smoke green. project open/back, brainstorm dump -> lore accept, plotboard relation CRUD, lore wiki edit/promotion, serialization lint sync, assistant session scoping까지 통과했다.
   - `1024`: 8-test smoke green. desktop과 동일 시나리오가 통과했다.
   - `390`: brainstorming dump -> extract, serialization toolbox, lore wiki drawer/article, plotboard drawer/view toggle, side sheet round-trip이 green이고 left drawer/toolbox overlay conflict와 CTA overflow blocker는 닫혔다.

### 2026-03-28 Note and Serialization Closeout Note
1. local verification:
   - `cd frontend && npm run lint`
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npx jest src/entities/note/model/tree.test.ts src/features/note-handoff/model.test.ts --runInBand`
   - `cd frontend && npx jest src/entities/chapter/model/grouping.test.ts --runInBand`
   - `cd frontend && npx playwright test phase-a-hardening.spec.ts phase-a-mobile-390.spec.ts --workers=1`
2. surfaced implementation:
   - pure note workspace는 mobile move selector에서 compact folder label을 사용하고, hydrate/select/move 뒤 선택 note를 다시 scroll into view한다.
   - note handoff는 returned payload 기준 success/error tone으로 상태를 보여주며, 성공 후 export panel을 닫되 같은 note selection/content를 유지하고 lore/serialization draft는 note-derived default로 reset한다.
   - serialization structure save는 summary, active chapter row, grouped tree를 같은 saved payload로 즉시 동기화하고, 목적지 `Part/BK` branch를 자동으로 펼친다.
   - new chapter inheritance는 latest saved `Part/BK`를 기준으로 고정되고 `EP`는 빈 배열로 시작한다.
3. regression note:
   - serialization regrouping과 mobile re-entry는 초기 spec expectation과 어긋나는 flaky 구간이 있었고, widget state sync와 `ui-helpers` contract를 함께 조정해 desktop/mobile canonical spec이 다시 같이 green이 되도록 닫았다.

### 2026-03-27 UI Sharpening and Lore Scale Validation Note
1. current closeout SHA:
   - `b342431`
2. local verification:
   - `cd frontend && npm run lint`
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npm run build`
   - `cd frontend && npm run test:e2e:local -- phase-a-hardening.spec.ts`
   - `cd frontend && npm run test:e2e:local -- brainstorm-to-lore.spec.ts`
   - `cd frontend && npm run test:e2e:local -- phase-a-mobile-390.spec.ts`
   - `cd frontend && npm run test:e2e:local -- lore-wiki-large-corpus.spec.ts`
3. surfaced implementation:
   - 전역 `panel/card/control/chip` radius token과 얕은 surface 규칙이 shell과 entry screen에 적용되었다.
   - login/project list는 editor-console 톤으로 재구성되었고, create/open flow smoke가 유지된다.
   - lore wiki sidebar는 `Promoted / Working / Library` grouped index를 사용하며 large-corpus mock data에서도 selection, search, plotboard round-trip을 유지한다.
   - plotboard relation authoring은 preset taxonomy, semantic legend/color, free-text custom fallback을 함께 사용한다.
4. regression note:
   - 초기 `lore-wiki-large-corpus` spec에서는 이미 열린 plotboard side sheet가 `세라` 클릭을 가로채는 false-negative가 있었고, 기존 문서 시트를 먼저 닫는 경로를 추가해 closeout했다.

### 2026-03-27 Assistant Policy Hardening Note
1. current closeout SHA:
   - `4f451ab`
2. local verification:
   - `docker compose up -d postgres-test`
   - `.\venv\Scripts\python.exe -m pytest tests/backend/api/test_assistant.py`
   - `cd frontend && npm run lint`
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npm run test:e2e:local -- serialization-assistant.spec.ts`
   - `cd frontend && npm run test:e2e:local -- phase-a-hardening.spec.ts`
   - `cd frontend && npm run test:e2e:local -- phase-a-mobile-390.spec.ts`
3. surfaced implementation:
   - backend chat final answer는 deterministic normalizer를 거쳐 기본적으로 `진단 1문장 + 번호형 제안 최대 3개`로 canonicalize된다.
   - explicit expanded 요청은 더 긴 제안을 허용하지만 compact 구조는 유지한다.
   - FE assistant panel의 quick prompt, helper copy, mock contract는 compact reply baseline에 맞춰 재정렬되었다.
4. regression note:
   - 최초 local backend rerun은 `postgres-test` 컨테이너가 떠 있지 않아 hang처럼 보일 수 있었고, canonical local path인 `docker compose up -d postgres-test` 후 정상 통과를 확인했다.

### 2026-03-27 Custom BubbleMenu Polish Note
1. local verification:
   - `.\venv\Scripts\python.exe -m pytest tests/backend/api/test_assistant.py`
   - `cd frontend && npm run lint`
   - `cd frontend && .\node_modules\.bin\tsc.cmd --noEmit -p .\tsconfig.json`
   - `cd frontend && .\node_modules\.bin\playwright.cmd test serialization-assistant.spec.ts --workers=1`
2. surfaced implementation:
   - `AssistantPolishRequest` / `AssistantPolishInstruction`는 `custom`과 `custom_prompt`를 지원하고, invalid custom request는 stable `422` validation으로 반환된다.
   - serialization BubbleMenu는 기존 preset shortcut을 유지하면서 같은 surface 안에 직접 지시 composer를 열고, selection snapshot(`from/to/selectedText`)을 고정한 뒤 TrackChange suggestion을 반영한다.
   - polish prompt는 `instruction=custom`일 때만 `[사용자 지시]` 블록을 추가하고, 응답 contract는 계속 single replacement + reason JSON으로 유지된다.
3. regression note:
   - 초기 validator는 plain `ValueError`를 사용해 global validation handler에서 JSON serialization issue를 드러냈고, `PydanticCustomError`로 교체해 closeout했다.

### 2026-03-27 Serialization Unit Folder System Note
1. local verification:
   - `.\venv\Scripts\python.exe -m pytest tests/backend/api/test_chapters.py tests/backend/api/test_assistant.py`
   - `cd frontend && npm run lint`
   - `cd frontend && .\node_modules\.bin\tsc.cmd --noEmit -p .\tsconfig.json`
   - `cd frontend && .\node_modules\.bin\playwright.cmd test e2e/phase-a-hardening.spec.ts e2e/serialization-assistant.spec.ts e2e/phase-a-mobile-390.spec.ts --workers=1`
2. surfaced implementation:
   - chapter API/model은 `part_title`, `book_title`, `episode_tags`를 public contract로 노출하고 `PATCH /api/v1/chapters/{project_id}/{chapter_id}/metadata`로 구조 메타데이터를 저장한다.
   - serialization left panel은 flat chapter list 대신 `Part > BK > Chapter` derived tree를 렌더링하고, 선택 챕터 기준 현재 구조 summary를 먼저 보여준 뒤 explicit `구조 편집` panel에서만 `Part/BK/EP`를 수정한다.
   - EP는 folder가 아니라 chapter-level cross tag로 유지되며, single-select filter가 켜지면 matching `Part/BK` 그룹을 자동으로 펼쳐 결과 visibility를 보장한다.
   - 새 챕터 생성은 active chapter의 `Part/BK`를 상속하고 `EP`는 빈 배열로 시작한다.
3. regression note:
   - hierarchy와 EP chip이 추가되면서 기존 Playwright selector가 strict-mode 충돌을 일으켰고, structure status/save button에 stable `data-testid`를 추가해 closeout했다.

### 2026-03-27 Plotboard Direct Connect UX Note
1. local verification:
   - `cd frontend && npm run lint`
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npx playwright test phase-a-hardening.spec.ts phase-a-mobile-390.spec.ts --workers=1`
2. surfaced implementation:
   - `LoreGraph`는 custom lore node와 explicit source/target handle을 사용하고, desktop/tablet direct-connect가 relation draft를 연다.
   - persisted edge는 clickable edit pill을 노출하고, same side sheet relation form이 create/edit 둘 다의 canonical save path로 유지된다.
   - inbound reference row는 source lore 기준 relation edit state로 jump하며, node position은 세션 로컬로 유지된다.
   - narrow-width에서는 broken drag affordance 대신 tap-to-edit help copy를 노출한다.
3. regression note:
   - 초기 E2E는 SVG edge click hit-area와 open side sheet overlay 때문에 flaky했으며, stable edge edit pill contract와 desktop graph gutter reservation으로 closeout했다.

### Backend Checks
- Targeted integration:
  - `.\venv\Scripts\python.exe -m pytest tests/backend/api/test_assistant.py tests/backend/api/test_lore.py`
- Full integration family:
  - `.\venv\Scripts\python.exe -m pytest -m "integration and not external" tests/backend/api`

### 2026-03-26 Lore Wiki UX/UI Reframe Note
1. UI actions:
   - `SSOT Guide` 전용 패널을 접고, left panel 자체를 canonical `Lore Wiki Index`로 승격했다.
   - 검색, 카테고리, 정렬, promoted-only, 결과 count, 문서 list를 모두 sidebar로 이동했다.
   - main 영역은 별도 index 컬럼을 제거하고 article-first 단일 읽기 canvas로 재구성했다.
   - lore wiki만 `leftPanelWidth=320`을 사용하고, mobile drawer도 같은 sidebar를 재사용한다.
2. component boundary:
   - lore wiki 표현부는 `frontend/src/widgets/WorkspaceLoreWiki/ui/LoreWiki.tsx`가 소유하고, shared lore presentation helper는 `frontend/src/entities/lore/model/presentation.ts`에 정리되어 `LoreWikiSidebar`, `LoreWikiDocCard`, `LoreWikiArticleHeader`와 plotboard query/relation formatter가 같은 canonical source를 사용한다.
3. local validation:
   - `cd frontend && npx tsc --noEmit`
   - `cd frontend && npm run lint`
   - clean dev-server restart 후 `cd frontend && npm run test:e2e -- phase-a-hardening.spec.ts --workers=1`
   - clean dev-server restart 후 `cd frontend && npm run test:e2e -- brainstorm-to-lore.spec.ts --workers=1`
4. operator note:
   - stale local Next dev server를 재사용하면 `_next/static` chunk `404`로 false-negative Playwright failure가 날 수 있으므로 local rerun 전 clean restart가 더 안전하다.

### 2026-03-26 Backend Recovery Note
1. traced hosted crash cause:
   - startup migration path가 `src/backend/alembic/env.py`의 local `asyncio` shadowing 때문에 Linux에서 `UnboundLocalError`로 죽을 수 있었다.
2. recovery actions:
   - production Postgres schema를 Alembic head `c0f7e1b6a12d`까지 올렸다.
   - startup migration regression을 수정했고, Procfile도 `--no-access-log` 기준으로 Docker path와 맞췄다.
3. local Linux validation:
   - Docker image로 startup checks 통과
   - `GET /` `200`
   - `GET /api/health` `200` with `llm_provider: "openai"`
   - `OPTIONS /api/v1/projects/` returns frontend ACAO header
   - `GET /api/v1/projects/` `200`
   - `POST /api/v1/projects/` `201`
   - `GET /api/v1/lore/1` `200`
   - `POST /api/v1/assistant/chat` `200`
4. public Railway validation:
   - Railway public backend가 다시 healthy replica를 제공한다.
   - production `GET /`, `GET /api/health`, `OPTIONS /api/v1/projects/`, `GET /api/v1/projects/`, `POST /api/v1/projects/`, `GET /api/v1/lore/1`, `POST /api/v1/assistant/chat`가 모두 green이다.
   - Playwright browser smoke에서 project create와 lore wiki load가 다시 동작했고, console error는 favicon `404`만 남았다.

### Local Verification Scripts
- Full local verification:
  - `scripts/run-local-ci.ps1`
- Frontend local E2E:
  - `scripts/run-local-e2e.ps1`

## 5. Next Session Reference Map

| Task Area | First Files to Open | Why |
| --- | --- | --- |
| DDD/FSD/BFF expansion | `src/backend/domain/notes/entities.py`, `src/backend/domain/lore/entities.py`, `src/backend/application/notes/use_cases/`, `src/backend/application/lore/use_cases/`, `src/backend/presentation/api/routers/notes.py`, `src/backend/presentation/api/routers/lore.py`, `frontend/src/widgets/WorkspaceNote/index.tsx`, `frontend/src/widgets/WorkspacePlotboard/index.tsx`, `frontend/src/widgets/WorkspaceLoreWiki/index.tsx`, `frontend/src/entities/note/api/notes.ts`, `frontend/src/entities/lore/api/lore.ts`, `tests/backend/architecture/test_notes_lore_slice_architecture.py` | architecture proof가 chapter를 넘어 notes/lore/plotboard까지 landed 되었으므로, 다음 세션에서는 leftover/guard/fence 작업을 여기서 이어 보는 게 가장 빠르다. |
| Serialization lint sync | `frontend/src/widgets/TiptapCanvas/model/track-change-errors.ts`, `frontend/src/widgets/TiptapCanvas/model/editor-store.ts`, `frontend/src/widgets/TiptapCanvas/ui/ErrorListPanel.tsx`, `frontend/src/widgets/WorkspaceSerialization/index.tsx` | canonical review data 계산과 banner/list/chapter sync가 여기서 만난다. |
| TrackChange behavior | `frontend/src/widgets/TiptapCanvas/model/extensions/TrackChanges.ts`, `frontend/src/widgets/TiptapCanvas/ui/core/components/controls/analyze-button.tsx`, `frontend/src/widgets/TiptapCanvas/ui/core/components/editor.tsx` | mark 저장 형식과 editor 반영 방식이 여기 있다. |
| Assistant chat | `frontend/src/widgets/SerializationAssistantPanel/index.tsx`, `frontend/src/shared/store/assistant-store.ts`, `frontend/src/shared/types/assistant.ts`, `src/backend/presentation/api/routers/assistant.py`, `src/backend/application/agents/serialization_assistant.py`, `frontend/e2e/serialization-assistant.spec.ts` | workspace mode, session key, compact reply policy, SSE contract, expanded request regression을 같이 봐야 한다. |
| Pure note workspace | `frontend/src/widgets/WorkspaceNote/index.tsx`, `frontend/src/entities/note/api/notes.ts`, `frontend/src/features/note-content-save/model/useNoteAutoSave.ts`, `frontend/src/features/note-handoff/model.ts`, `frontend/src/entities/novel/model/store.ts`, `src/backend/presentation/api/routers/notes.py`, `src/backend/application/notes/use_cases/`, `tests/backend/api/test_notes.py`, `tests/backend/test_note_service.py`, `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/phase-a-mobile-390.spec.ts` | `Folder > Note` tree, note persistence boundary, autosave, explicit handoff CTA, single-call BFF export path, mobile move fallback, zero-intervention regression anchor를 여기서 먼저 본다. |
| Serialization units | `frontend/src/widgets/WorkspaceSerialization/index.tsx`, `frontend/src/entities/chapter/api/chapters.ts`, `frontend/src/entities/chapter/model/grouping.ts`, `frontend/src/features/chapter-organize/model.ts`, `frontend/src/features/chapter-metadata-edit/model.ts`, `src/backend/presentation/api/routers/chapters.py`, `src/backend/application/chapters/use_cases/`, `src/backend/domain/chapters/entities.py`, `src/backend/domain/chapters/repositories.py`, `src/backend/infrastructure/persistence/chapters_repository.py`, `src/backend/infrastructure/persistence/sqlmodel/chapters.py`, `src/backend/alembic/versions/a7b1c9d4e2f0_add_serialization_units_to_chapters.py`, `tests/backend/api/test_chapters.py`, `tests/backend/test_chapter_service.py`, `tests/backend/architecture/test_chapter_slice_architecture.py`, `frontend/e2e/phase-a-hardening.spec.ts` | Part/BK/EP metadata contract, drag reorder/group move UX, dedicated move endpoint, structure save path, EP filter behavior와 DDD/FSD chapter slice 경계를 같이 본다. |
| Lore relations | `frontend/src/entities/lore/api/lore.ts`, `frontend/src/features/lore-relation-edit/model.ts`, `src/backend/presentation/api/routers/lore.py`, `src/backend/application/lore/use_cases/`, `src/backend/domain/lore/entities.py` | relation JSON shape와 FE/BE contract, plotboard aggregate read, relation validation 규칙의 중심점이다. |
| Plotboard | `frontend/src/widgets/WorkspacePlotboard/index.tsx`, `frontend/src/widgets/Workspaces/ui/LoreGraph.tsx`, `frontend/src/widgets/Workspaces/ui/loreRelationTaxonomy.ts`, `frontend/src/features/plotboard-graph/model.ts`, `frontend/src/entities/lore/api/lore.ts`, `src/backend/presentation/api/routers/lore.py`, `tests/backend/api/test_lore.py`, `frontend/e2e/support/ui-helpers.ts` | worldview projection, category-clustered fallback layout, session-local viewport focus/reset, graph direct-connect draft, edge edit pill, persisted layout write path, staged relation editor, taxonomy color/legend, E2E drag helper가 여기 있다. |
| Lore wiki | `frontend/src/widgets/WorkspaceLoreWiki/index.tsx`, `frontend/src/widgets/WorkspaceLoreWiki/ui/LoreWiki.tsx`, `frontend/src/entities/lore/model/presentation.ts`, `frontend/src/entities/lore/api/lore.ts`, `frontend/e2e/lore-wiki-large-corpus.spec.ts` | grouped sidebar index, advanced disclosure, folded metadata rail, relation summary read-only surface와 scale smoke가 여기 있다. |
| Entry / Project Console | `frontend/src/widgets/Auth/ui/LoginScreen.tsx`, `frontend/src/widgets/ProjectList/ui/ProjectListScreen.tsx`, `frontend/e2e/brainstorm-to-lore.spec.ts` | editor 진입 전 로그인/프로젝트 create-open surface와 smoke contract가 여기 있다. |
| Frontend local E2E handoff | `scripts/run-local-e2e.ps1`, `frontend/playwright.config.ts`, `frontend/e2e/support/odys-api-mocks.ts`, `frontend/e2e/phase-a-hardening.spec.ts` | local-only Playwright 실행 경로를 script, runtime config, mocked contract, reopened regression scenario 순서로 좁힐 수 있다. |
| E2E mocks | `frontend/e2e/support/odys-api-mocks.ts` | frontend regression에서 server truth를 흉내내는 기준점이다. |
| Backend regression | `tests/backend/test_chapter_service.py`, `tests/backend/api/test_chapters.py`, `tests/backend/api/test_assistant.py`, `tests/backend/api/test_lore.py`, `tests/backend/conftest.py` | chapter move + lore plotboard layout contract와 assistant/lore integration fixture를 같이 확인해야 한다. |
| Frontend regression | `frontend/e2e/serialization-assistant.spec.ts`, `frontend/e2e/brainstorm-to-lore.spec.ts`, `frontend/e2e/phase-a-hardening.spec.ts`, `frontend/e2e/phase-a-mobile-390.spec.ts`, `frontend/e2e/lore-wiki-large-corpus.spec.ts`, `frontend/e2e/support/ui-helpers.ts` | reopened Phase A slices를 보호하는 UI contract와 responsive helper, canonical narrow/scale smoke가 여기 있다. |

## 6. Current Repository Drift

| Drift | Evidence | Effect |
| --- | --- | --- |
| Repo-facing branding cleanup landed but package/container identifiers remain out of scope | `README.md`, `frontend/README.md`, `frontend/package.json`, `config/settings.py`, `Dockerfile.backend`, `docker-compose.yml` | 현재 진입 문서와 설명문은 Odys 기준으로 정렬되었지만 repo-wide identifier rename 여부는 별도 hygiene 판단이 필요하다. |
| Legacy API surface fully removed | `src/backend/main.py` includes only Odys v1 routers; legacy chat/database/documents/history routers, orphan `application/use_cases/`, `presentation/schemas/models.py` have been deleted | legacy surface drift는 닫혔다. |
| DDD rollout expanded to projects — narrative schema relocated | `src/backend/domain/chapters/**`, `src/backend/domain/notes/**`, `src/backend/domain/lore/**`, `src/backend/domain/brainstorm/**`, `src/backend/domain/projects/entities.py` (framework-free dataclass), `src/backend/application/projects/use_cases/`, `src/backend/application/agents/schemas.py` (narrative output, relocated from `domain/models/`), `src/backend/application/notes/**`, `src/backend/application/lore/**`, `src/backend/application/brainstorm/**` | chapter/notes/lore/brainstorm/projects는 pure-domain proof를 가진다. narrative output schema는 application/agents 계층으로 이동 완료. 남은 과제는 `core/` infra 모듈의 위치 조정이다. |
| FSD rollout is broader but not fully cleaned up | `frontend/src/widgets/WorkspaceOnboarding/index.tsx`, `frontend/src/widgets/WorkspaceSerialization/index.tsx`, `frontend/src/widgets/WorkspaceNote/index.tsx`, `frontend/src/widgets/WorkspaceBrainstorm/index.tsx`, `frontend/src/widgets/WorkspacePlotboard/index.tsx`, `frontend/src/widgets/WorkspaceLoreWiki/index.tsx`, `frontend/src/widgets/WorkspaceLoreWiki/ui/LoreWiki.tsx`, `frontend/src/entities/brainstorm/**`, `frontend/src/entities/note/**`, `frontend/src/entities/lore/**`, `frontend/src/features/note-*/**`, `frontend/src/features/lore-*/**` | serialization, note, lore, plotboard, brainstorm는 FSD ownership으로 이동했고 legacy Workspaces barrel은 제거되었지만 shared UI ownership과 일부 shared/legacy cleanup은 더 필요하다. |
| Workspace BFF normalization is mostly complete | `src/backend/presentation/api/routers/chapters.py`, `src/backend/presentation/api/routers/assistant.py`, `src/backend/presentation/api/routers/lore.py`, `src/backend/presentation/api/routers/notes.py`, `src/backend/presentation/api/routers/brainstorm.py`, `src/backend/presentation/api/routers/projects.py`, `src/backend/main.py`, `frontend/.eslintrc.json`, `tests/backend/test_app_factory.py` | chapters/assistant에 더해 notes handoff, chapter move, plotboard aggregate read/write, brainstorm CRUD/extract, projects CRUD도 BFF 방향으로 정렬됐고 frontend legacy consumer cleanup과 orphan code cleanup은 완료되었다. |
| Worldview promotion rollout evidence is still incomplete | `src/backend/alembic/versions/c0f7e1b6a12d_add_lore_wiki_fields.py`, `frontend/src/widgets/WorkspacePlotboard/index.tsx`, `frontend/src/widgets/WorkspaceLoreWiki/index.tsx` | explicit promotion baseline은 landed 되었지만 migration/manual smoke closure는 더 필요하다. |
| Pure note workspace closeout evidence is still incomplete | `frontend/src/widgets/WorkspaceNote/index.tsx`, `src/backend/presentation/api/routers/notes.py`, `tests/backend/api/test_notes.py` | compact-label full-width mobile move fallback, selected-note scroll recovery, payload-based success/error handoff, stationary export reset, desktop/mobile regression closeout까지 automated baseline은 landed 되었지만, real-corpus/manual large-tree와 cross-workspace handoff product-feel validation은 더 필요하다. |
| Serialization organization closeout evidence is still incomplete | `frontend/src/widgets/WorkspaceSerialization/index.tsx`, `frontend/src/features/chapter-organize/model.ts`, `frontend/src/entities/chapter/model/grouping.ts`, `tests/backend/api/test_chapters.py` | saved-payload regrouping, destination branch auto-open, active chapter visibility, latest saved metadata inheritance 위에 desktop/mobile DnD-group move regression closeout은 landed 되었지만, real-corpus large chapter-count/manual authoring feel과 rename/bulk organization semantics는 더 필요하다. |
| Plotboard relation UX is graph-first on desktop/tablet but not fully parity-complete | `frontend/src/widgets/WorkspacePlotboard/index.tsx`, `frontend/src/widgets/Workspaces/ui/LoreGraph.tsx`, `frontend/src/widgets/Workspaces/ui/loreRelationTaxonomy.ts`, `frontend/src/features/plotboard-graph/model.ts` | category-clustered fallback layout, session-local viewport focus/reset, dense graph readability polish, narrow-width minimap hide까지 local baseline은 landed 되었지만 HP1 real-corpus/manual rerun evidence는 아직 없다. |
| Assistant concise policy is not schema-level | `src/backend/application/agents/serialization_assistant.py`, `src/backend/presentation/api/routers/assistant.py` | prompt + deterministic normalizer baseline은 landed 되었지만 structured contract와 real-user product-fit tuning은 더 가능하다. |
| Mock-backed scale proof above real-corpus validation gap remains | lore wiki / plotboard / assistant surface | `lore-wiki-large-corpus`에 더해 HP1 mock canonical desktop/narrow pack까지 확보되었지만 real-corpus/perf/manual validation은 더 필요하다. |
| Deployment workflow is outside repo | repo에는 `scripts/run-local-ci.ps1`, `scripts/run-local-e2e.ps1`, `Dockerfile.*`, `docker-compose.yml`은 있으나 deployment workflow definition은 보이지 않는다. | 운영 재현성과 온보딩 설명에 별도 note가 필요하다. |

## 7. Evidence Rules for V4

1. `working` 또는 `completed` 성격의 판단은 최소 1개의 실제 code path, route, test 중 하나를 근거로 남긴다.
2. path는 실제 repo 경로를 그대로 사용한다. frontend 경로는 `frontend/src/...` prefix를 생략하지 않는다.
3. limitation은 roadmap가 아니라 현재 코드의 한계만 적는다.
4. repo 밖에서 확인된 운영 사실은 `operator-confirmed` 성격으로 구분해 적고, repo 내부 증거와 혼동하지 않는다.
5. 다음 세션 jump-start를 돕는 dependency/test/path 정보는 `mechanism.md`에 넣고, phase 판단은 `roadmap.md`에 넣는다.
