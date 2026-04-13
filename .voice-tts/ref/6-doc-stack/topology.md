# Odys Studio Topology (V4)

- Role: Odys Studio 목표 아키텍처의 규범 SSOT
- Source Type: Normative / Topology
- Baseline Date: 2026-03-30 (KST)
- Current Phase: Phase A closure validation active / Phase B visual engine integration blocked-next
- Update Trigger: layer 경계, dependency canon, state sync canon, `ARCH-*` ownership이 바뀔 때
- Excluded Content: completion 판정, smoke 결과, short-term backlog, bug log

## 1. Interpretation Rules

1. 이 문서는 **규범만** 기록한다. 현재 리포지토리의 구현 사실은 `mechanism.md`가 기록한다.
2. 목표와 현재 구현이 어긋나면, 규범을 낮추지 않는다. 대신 `Current Repository Drift`에 informational note를 남긴다.
3. 모든 구조 단위는 `ARCH-*` ID로 추적한다.
4. Odys의 목표 제품선은 B2B 창작 editor이며, legacy compatibility surface는 목표 제품 정의가 아니다.

## 2. Cross-Cutting Rules

1. 프론트엔드는 Next.js App Router와 FSD dependency direction 및 ownership canon을 유지한다.
2. 백엔드는 Clean Architecture, DDD, port/adapter 경계를 함께 유지한다.
3. AI의 텍스트 개입은 reviewable editing flow를 통과해야 한다.
4. 배포/CI의 성공 여부는 구조 규범 자체를 바꾸지 않는다. 운영 상태는 `mechanism.md`와 `sprint.md`에서 관리한다.
5. 규범 문서는 구현 완료를 선언하지 않는다.
6. 동일한 narrative artifact의 원본과 파생 surface는 source/derived 관계가 분명해야 하며, 서로 구분되지 않는 중복 편집 surface로 수렴해서는 안 된다.
7. QA 요약 수치와 상세 목록은 서로 다른 임시 캐시가 아니라 동일한 canonical review data에서 파생되어야 한다.
8. 같은 capability가 main area와 toolbox/tool surface 양쪽에 나타나더라도, 데이터 계약은 단일 source에서 파생되어야 한다.
9. workspace마다 자동화 개입 수준은 명시적으로 구분되어야 하며, zero-intervention scratchpad는 다른 pipeline-triggering surface와 의미가 섞이면 안 된다.
10. Odys v1의 사용자-facing API는 workspace-first BFF surface를 지향하며, persistence model이나 내부 adapter shape를 직접 노출해서는 안 된다.
11. compact/mobile shell에서 좌측 rail, toolbox, mode switcher 같은 transient overlay는 동시에 둘 이상 열리지 않아야 하며, 현재 작업 맥락을 가리는 chrome density를 늘리는 방향으로 조합되면 안 된다.

## 3. Layer Canon

| Architecture ID | Layer | Responsibility | Normative Canon | Open / Closed |
| --- | --- | --- | --- | --- |
| `ARCH-DOM-01` | Domain | 순수 도메인 모델과 규칙, ubiquitous language | Clean Architecture domain은 DDD를 따른다. entity, value object, aggregate, domain service, repository port만 둘 수 있으며 SQLModel/SQLAlchemy/FastAPI/transport Pydantic에 의존하지 않는다 | Closed |
| `ARCH-APP-01` | Application | use case, query service, agent orchestration, BFF-facing DTO | 도메인 모델을 이용해 editor workflow를 조율하며, presentation/persistence 세부사항을 직접 노출하지 않는다. 외부 surface에 필요한 command/query DTO는 application이 소유한다 | Open |
| `ARCH-PRE-01` | Presentation | workspace shell, panels, navigation, view composition | 프론트는 App Router + FSD composition root를 유지하고, 백엔드 presentation은 BFF surface로서 request/response mapping과 transport concern만 소유한다 | Open |
| `ARCH-BFF-01` | BFF Surface | workspace-first frontend contract | `/api/v1/*` surface는 frontend workflow를 위한 BFF다. stable editor contract를 제공하되 persistence model, ORM record, DB session, 내부 agent/raw adapter shape를 직접 노출하지 않는다 | Open |
| `ARCH-EDT-01` | Editor State and Sync | editor 상태, workspace content routing, 외부 content 주입 | **Zustand 기반 상태 관리**를 기본 canon으로 하며, Tiptap 경계에서만 imperative content bridge를 허용한다 | Open |
| `ARCH-PER-01` | Persistence | 텍스트/업무 데이터와 narrative graph의 역할 분리 | Postgres는 프로젝트/챕터/로어/브레인스토밍의 기록 저장소, Neo4j는 narrative graph 저장소 역할을 맡는다 | Open |
| `ARCH-INF-01` | Infrastructure | 외부 시스템 adapter, 운영 packaging, future engine integration | LLM, DB driver, 배포/관측성, 향후 visual engine adapter를 인프라 경계에 격리한다 | Open |

## 4. Extension Canon

| Architecture ID | Extension | Responsibility | Normative Canon | Open / Closed |
| --- | --- | --- | --- | --- |
| `ARCH-AI-01` | Lore and Creative Assist Agents | lore extraction, pacing analysis, creative assistance | editor workflow에 필요한 분석/제안을 application 계층에서 orchestration하며, assistant 기본 응답은 workspace intent에 맞는 짧고 실행 가능한 형태를 지향한다 | Open |
| `ARCH-KNW-01` | Knowledge Surfaces | lore wiki, worldview cards, relation authoring | lore wiki는 left sidebar index와 article-first main을 갖는 장문형 배경 지식의 source surface, worldview cards는 승격된 결정 수준 summary surface이며, plotboard relation은 graph gesture와 form editor를 모두 활용하더라도 explicit save를 거치는 manual CRUD를 지원해야 한다 | Open |
| `ARCH-SSE-01` | Streaming UX | AI analysis와 제안의 점진적 전달 | stream은 UI responsiveness를 위해 허용하되, 편집 반영은 reviewable flow를 유지해야 한다 | Open |
| `ARCH-STR-01` | L.T.E.E Narrative Modeling | LoreNode/EventNode 중심 narrative schema | 시간, 장소, 참여자, 행동이 빠지지 않는 event modeling을 유지한다 | Open |
| `ARCH-STR-02` | Frontend FSD | 프론트엔드 계층 의존성 통제와 ownership 분리 | `app -> widgets -> features -> entities -> shared` 방향만 허용한다. `app`은 composition root, `widgets`는 screen/workspace assembly, `features`는 user interaction, `entities`는 business contract/model, `shared`는 generic infra/ui만 소유한다 | Closed |
| `ARCH-STR-03` | Reviewable AI Suggestions | AI 제안의 편집 반영 방식 | 사용자의 검토 없이 본문을 확정 덮어쓰지 않는다 | Closed |

## 5. Editor Sync Canon

`ARCH-EDT-01`의 세부 규범은 아래와 같다.

1. workspace와 editor UI 상태의 주 저장소는 Zustand store다.
2. 서로 다른 workspace content는 store level에서 분리한다.
3. Tiptap content prop이 완전한 reactive sync point가 아니므로, 외부에서 chapter 전환이나 mode 전환 시 **imperative bridge**를 사용할 수 있다.
4. 그 bridge는 editor boundary에 한정되며, 전역 state 관리의 기본 패턴이 되어서는 안 된다.
5. `useSyncExternalStore`는 현재 canon이 아니다. 향후 도입하려면 구조적 이유와 migration plan이 함께 문서화되어야 한다.
6. 연재 QA에서 lint count, detailed error list, reviewable redline은 현재 chapter의 동일한 canonical review data를 바라봐야 한다.
7. editor mount 이전의 초기 상태에서는 저장된 chapter artifact를 읽어 임시 fallback을 구성할 수 있지만, editor doc가 올라오면 editor-derived canonical state가 우선한다.

## 6. Dependency Direction Canon

### Backend
Compile-time dependency direction:
`Presentation -> Application -> Domain`

Adapter dependency direction:
`Infrastructure -> Application -> Domain`

- presentation은 BFF surface로서 request/response mapping, auth, transport validation을 담당하고, migrated slice에서 ORM record나 DB session을 직접 import하지 않는다.
- application은 use case/query/agent orchestration과 BFF-facing DTO를 소유하며, presentation이나 infrastructure 세부사항을 import하지 않는다.
- domain은 DDD core이며 상위 레이어와 프레임워크를 참조하지 않는다.
- infrastructure는 repository, database, LLM, external adapter를 제공하고 application/domain으로 매핑한다.

### Frontend
`app -> widgets -> features -> entities -> shared`

- `app`은 route-level composition root만 맡고 business logic를 소유하지 않는다.
- `widgets`는 workspace/main-area/tool surface 조합을 맡되, 장기적으로 cross-domain business logic의 영구 거주지가 되어서는 안 된다.
- `features`는 user action과 local workflow를 캡슐화하고, `entities`는 domain contract/model/api를 소유한다.
- `shared`는 generic infra, UI primitive, utility만 허용되며 도메인별 API contract나 business helper의 영구 소유자가 되어서는 안 된다.
- 동일 계층 교차 참조는 필요한 범위에서만 허용한다.
- 역방향 참조는 허용하지 않는다.
- legacy surface를 감싼다고 해서 FSD 방향을 깨면 안 된다.

### BFF
- frontend와 backend의 기본 통합 경로는 workspace-first BFF surface다.
- BFF는 frontend editor workflow에 맞춘 read/write contract를 제공하기 위해 여러 use case, query service, agent response를 조합할 수 있다.
- 내부 persistence refactor, repository 교체, domain 재구성은 BFF contract 뒤로 숨겨져야 한다.
- legacy generic surface는 BFF와 구분되어 fenced 상태로 남겨야 하며, 새 capability의 기본 진입점이 되어서는 안 된다.

## 7. Middle Gate Canon

1. 각 workspace는 editor 직행만이 아니라, 결과물을 조망하는 중간 층을 가질 수 있어야 한다.
2. 다만 Middle Gate의 구현 형태는 workspace별로 달라질 수 있다. 카드, 리스트, 그래프, 타임라인, 사이드바 모두 허용된다.
3. Middle Gate는 presentation concern이며, persistence나 agent orchestration 규칙을 침범하지 않는다.

## 8. Workspace Mode Canon

1. brainstorming workspace는 아이디어를 dump하고 필요 시 extraction/assistant를 호출하는 assistive ideation surface여야 한다.
2. pure note workspace는 자유 메모와 임시 초안을 위한 zero-intervention scratchpad여야 하며, AI/추출/lint/구조화 pipeline이 background나 implicit flow로 개입해서는 안 된다.
3. pure note workspace의 외부 연결은 explicit user handoff로만 허용한다. note -> brainstorming, note -> lore, note -> serialization 같은 승격/복제/내보내기 action은 명시적 CTA를 통해서만 일어나야 한다.
4. pure note workspace의 기본 navigation surface는 좌측 `Folder > Note` tree여야 하며, 폴더는 정리 단위일 뿐 chapter/status/pipeline state를 의미해서는 안 된다.
5. pure note workspace의 note tree는 drag handle, before/after(or group) drop indicator, mobile move fallback 같은 interaction grammar를 serialization sidebar와 공유할 수 있지만, note folder hierarchy와 serialization metadata contract는 별도 규칙으로 유지해야 한다.
6. serialization workspace는 production manuscript surface로서 lint, reviewable AI, chapter structure metadata 같은 강한 authoring semantics를 유지해야 하며, metadata control은 본문 몰입을 해치지 않도록 compact summary와 explicit edit toggle 뒤로 물러날 수 있다.
7. lore wiki와 plotboard는 source/projection knowledge surface semantics를 유지해야 하며, note workspace가 이 역할을 대체해서는 안 된다.
8. 여러 workspace가 같은 editor 기술(Tiptap 등)을 공유할 수는 있지만, 자동화 개입 수준과 데이터 ownership 규칙은 각 mode별로 분리되어야 한다.

## 9. Knowledge Surface Canon

1. Lore Wiki는 plotboard에 등장하지 않는 배경까지 자유롭게 기술할 수 있는 장문형 knowledge base이며, `title`, `summary`, `content`, `validation_status`, `wiki_metadata`, `worldview_promoted`의 source surface다.
2. Lore Wiki의 기본 navigation surface는 left sidebar index이고, main canvas는 article-first 읽기/편집 경험을 우선해야 한다.
3. Worldview cards는 lore wiki에서 explicit promotion된 결정 수준 summary surface다.
4. 모든 lore entry가 worldview card가 될 필요는 없으며, cards는 deeper lore context로 연결될 수 있어야 한다.
5. lore wiki와 plotboard는 focused lore document state를 공유해 같은 문서로 왕복 이동할 수 있어야 한다.
6. Plotboard relation graph는 manual create/read/update/delete를 지원해야 하며, relation authoring surface는 plotboard가 소유한다.
7. 그래프 drag-connect나 edge click은 relation draft/edit 진입점이 될 수 있지만, persisted mutation은 explicit relation type 선택과 save를 거쳐야 한다.
8. Lore Wiki의 relation summary/backlinks는 read-only reference surface여야 하며, relation 편집 CTA는 plotboard로 연결되어야 한다.
9. 텍스트 기반 또는 그래프 기반 relation inference는 assistive suggestion일 수 있지만, 유일한 authoring 경로가 되어서는 안 된다.
10. knowledge surface가 같은 `LoreDocument` 저장소를 공유하더라도, 어떤 surface가 source이고 어떤 surface가 projection인지 규칙이 명시되어야 한다.
11. worldview projection은 stored summary와 explicit promotion state를 기준으로 동작해야 한다.
12. plotboard graph layout은 BFF를 통해 persist될 수 있으며, narrow-width relation authoring은 bottom-sheet/staged disclosure를 사용하더라도 explicit save path와 source/projection 구분을 유지해야 한다.

## 10. Assistant Surface Canon

1. assistant chat contract는 workspace mode를 공유해도 되지만, context loading과 session scope는 workspace별로 분리되어야 한다.
2. serialization assistant는 현재 chapter와 lore를 우선 근거로 삼아야 한다.
3. brainstorming assistant는 현재 brainstorm content, recent dump, lore summary를 우선 근거로 삼아야 한다.
4. concise default answer policy는 workspace intent에 맞는 짧고 실행 가능한 응답을 기본값으로 둔다.
5. polish/expand/summarize 같은 direct text action은 reviewable editing flow를 유지한다.
6. pure note workspace가 도입되더라도 assistant나 자동 분석은 implicit default가 되어서는 안 되며, 명시적 export/handoff 전까지는 note content를 pipeline context로 소비하지 않는다.

## 11. Current Repository Drift

아래 항목은 규범이 아니라, 현재 리포지토리가 목표 구조와 어긋나는 지점을 설명하기 위한 informational note다.

| Drift | Why It Matters |
| --- | --- |
| repo-facing branding은 정렬되었지만 package/container identifier는 아직 out-of-scope다 | 현재 사용자/기여자 진입 표면은 Odys 기준선으로 읽히지만 repo-wide identifier rename은 별도 판단이 필요하다. |
| legacy chat/history/database/document surface와 Odys v1 surface가 함께 존재 | 목표 제품선과 현재 repo shape를 분리해서 설명해야 한다. |
| DDD boundary proof는 chapter를 넘어 notes/lore까지 확장되었지만 아직 repo 전체는 아니다 | core 인프라 및 앱 모듈 이전이 완료되어 계층 분리가 완료되었다. |
| FSD ownership proof는 serialization을 넘어 note/lore/plotboard까지 확장되었지만 compatibility shim이 남아 있다 | `app/widgets/features/entities/shared` 분해는 serialization, note, lore, plotboard에서 보이기 시작했지만 legacy re-export와 남은 shared/mega-file cleanup은 아직 더 필요하다. |
| BFF canon이 아직 부분 정렬 상태다 | chapters/assistant에 더해 notes handoff, chapter move, plotboard aggregate read/write, brainstorm CRUD/extract도 BFF 방향으로 이동했다. 남은 불일치는 default-off compatibility surface의 rollout 확인과 eventual removal timing 정리 쪽이다. |
| pure note workspace closeout이 아직 full gate는 아니다 | zero-intervention semantics, folder-backed multi-note organization, full-path mobile move fallback, payload-based stationary handoff feedback, regression coverage는 landed 되었지만 real-corpus/manual validation은 아직 더 필요하다. |
| serialization organization closeout이 아직 full gate는 아니다 | saved-state regrouping, destination branch auto-open, latest-metadata inheritance 위에 desktop drag reorder/group move와 mobile move fallback이 landed 되었지만 real-corpus large-count validation과 rename/bulk organization semantics 판단은 아직 더 필요하다. |
| plotboard relation authoring은 desktop/tablet graph-first draft와 side-sheet save의 혼합형이다 | direct-connect draft, edge edit, persisted layout, narrow-width staged/bottom-sheet authoring은 landed 되었지만 real-corpus graph feel과 viewport/camera polish는 아직 더 필요하다. |
| assistant concise policy는 prompt-governed baseline이다 | workspace-intent AI canon은 반영되었지만 quality를 더 강하게 고정할 수 있다. |
| mock-backed regression 대비 real-corpus/manual validation 증거가 얇다 | 구조 proof는 강해졌지만 실제 corpus와 장시간 authoring 체감은 아직 product-level evidence가 더 필요하다. |
| deployment workflow/provider definition이 repo 안에 보이지 않는다 | 운영 재현성 설명이 infra packaging과 별도 관리되어야 한다. |
