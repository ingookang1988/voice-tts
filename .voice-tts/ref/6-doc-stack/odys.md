# Odys Studio Documentation Control Tower (V4)

- Role: `.odys/` 문서 체계의 최상위 진입점
- Source Type: Control Tower / Canonical Entry
- Baseline Date: 2026-03-30 (KST)
- Current Phase: Phase A closure validation active / Phase B visual engine integration blocked-next
- Update Trigger: 상위 기준선, active focus, 문서 소유권, phase 요약이 바뀔 때
- Excluded Content: 상세 런타임 증적, 장기 설계 해설, 세부 WO 로그

## 1. Purpose
이 문서는 Odys Studio 문서 체계의 control tower다. V4의 목적은 Odys 목표 아키텍처를 SSOT로 유지하되, 현재 리포지토리가 아직 일부 legacy naming과 compatibility surface를 품은 전환기 상태라는 사실을 숨기지 않는 것이다.

V4 문서 체계는 아래 원칙을 따른다.

1. `roadmap.md`는 phase와 promotion gate만 기록한다.
2. `feature.md`는 current live feature, hierarchy, actor-outcome, E2E flow, intentional hold만 기록한다.
3. `topology.md`는 목표 규범만 기록한다.
4. `mechanism.md`는 현재 코드와 검증 가능한 사실만 기록한다.
5. `sprint.md`는 실행 보드와 backlog만 기록한다.
6. `odys.md`는 위 다섯 문서의 진입점과 기준선만 기록한다.

`.plan/` 아래 PRD와 user journey 문서는 background/historical reference로 남고, current live product의 SSOT는 `.odys/feature.md`를 포함한 `.odys/` six-doc stack이 맡는다.

## 2. Current Baseline

| Item | Current Baseline |
| --- | --- |
| Product Identity | 이 리포지토리는 **Odys 목표를 가진 전환기 레포**다. editor/workspace/assistant 흐름과 repo-facing 문서는 Odys 기준선으로 올라왔지만, 일부 package/container identifier와 legacy API surface는 아직 transition 상태다. |
| Canonical Doc Root | `.odys/` |
| Current Live Product Map | current live feature snapshot, actor-outcome, primary entry, E2E flow, intentional hold의 owner는 `.odys/feature.md`다. `.plan/*.md`는 background reference로 남는다. |
| Current Focus | 현재 기준선은 **Phase A closure validation**이다. 2026-03-30 기준 loop 5 blocker closeout, plotboard graph feel / viewport polish, HP1 mock canonical mini-pack까지 local baseline에 landed 되었고 frontend regression pack은 `bern` + `hp1` corpus family 기준 Playwright canonical `19 / 19` green을 유지한다. 2026-04-12 세션에서는 legacy route 코드 완전 제거 사실 확인, orphan legacy service/schema cleanup(`application/use_cases/`, `presentation/schemas/models.py`, `widgets/Workspaces/note.tsx` 삭제), projects/users domain entity의 DDD dataclass 전환이 수행되었다. 다만 full backend integration preflight는 여전히 Docker-backed test DB availability에 의존하고 local Neo4j persistence는 DNS resolution failure로 degraded이므로 gate는 `Yellow`이며, 현재 중심은 closure review와 Docker-backed backend verification rerun 정리다. |
| Architecture Program | Phase A에서는 architecture hardening을 별도 축으로 추적한다. `topology.md`는 Clean Architecture + DDD/FSD/BFF canon을, `mechanism.md`는 chapter/notes/lore/plotboard/brainstorm proof와 current drift를, `sprint.md`는 DDD/FSD/BFF rollout WO를 소유한다. |
| Implemented Highlights | 6-workspace shell, frontend legacy compatibility consumer 제거, repo-facing branding cleanup, backend legacy compatibility route default-off + explicit opt-in retain, compatibility rollout note, pure note closeout slice(full-path mobile move labels, selected-note scroll recovery, payload-based handoff feedback, same-note stationary export), mobile shell mode-switcher sheet + overlay mutex baseline, 브레인스토밍 덤프 저장/추출/수락 + worldview/history mixed review materialization, lore wiki left sidebar index + article read/edit mode + advanced disclosure + folded metadata preview, `summary/worldview_promoted/wiki_metadata` 기반 worldview promotion baseline, explicit relation graph + outbound CRUD + inbound reference baseline, relation taxonomy preset + semantic legend/color baseline, graph direct-connect draft authoring + clickable edge edit pill + inbound source-edit jump + server-persisted node layout + category-clustered fallback layout + focus-safe viewport/reset-view + narrow bottom-sheet authoring, chapter autosave/trackChange-based QA sync baseline, serialization summary-first structure rail + saved-state regrouping/branch auto-open/new chapter inheritance + desktop DnD/group move + mobile move fallback + dedicated move endpoint, serialization/brainstorming assistant baseline, deterministic compact assistant reply normalization + expanded-on-demand baseline, assistant markdown render + minimal quick prompt disclosure, global shape token + sharper shell surface baseline, login/project list editor-console reframe + project rename/delete baseline, lore-only wider wiki panel, lore wiki grouped large-corpus index, stable FE regression baseline, deployed runtime baseline. |
| Baseline Retained | local verification path와 regression path(`bern` + `hp1` mock canonical 포함), serialization-first polish flow, deployed rollout 증거는 유지되지만 더 이상 Phase A closeout 단독 근거로 쓰지 않는다. |
| Open Follow-up | Docker-backed backend integration rerun, Phase A closure review, pure note workspace의 real-corpus/manual product-feel validation 반복 증적, serialization의 real-corpus large chapter-count/manual validation, lore wiki real-corpus scale/perf validation, plotboard real-corpus graph feel / viewport polish manual validation 반복 증적, assistant real-user product-fit tuning과 BubbleMenu quality hardening, package/container/historical identifier rename 여부 판단. |

## 3. Phase Snapshot

| Phase Slice | Current Judgment | Notes |
| --- | --- | --- |
| Phase A-1 ~ A-4 | Working baseline | 6-mode shell, note/brainstorm flow, lore/wiki CRUD baseline, serialization autosave/stats baseline은 repo와 테스트 경로에 존재한다. |
| Phase A-5 | Hardening loop active | worldview cards는 explicit `worldview_promoted` metadata와 stored `summary`를 사용하는 projection surface로 정리되었고, graph는 explicit relations + graph-origin draft authoring + clickable edge edit + inbound source-edit jump + server-persisted layout을 사용한다. unsaved 문서에는 category-clustered fallback layout이 적용되고, selection/focus는 전체 refit 대신 focus-safe viewport와 session-local `전체 보기` reset으로 정리되었다. persisted mutation은 여전히 plotboard side sheet save 경로를 거치며, narrow-width에서는 minimap hide + bottom-sheet/staged authoring baseline이 landed 되었다. 남은 과제는 real-corpus graph feel/manual validation closeout이다. |
| Phase A-6 | Hardening loop active | serialization lint canonical sync는 유지되고, lore wiki는 left sidebar index, article read/edit mode, foldable metadata preview, advanced disclosure, promoted-only navigation에 더해 `Promoted / Working / Library` grouped sidebar와 sharper editor-tool shell baseline까지 landed 되었다. pure note workspace의 payload-based handoff feedback과 same-note stationary export, serialization의 saved-state regrouping과 desktop DnD/group move는 여전히 유효하며, loop 5에서 reopened 되었던 HP1 `390` note/serialization mobile move affordance blocker는 closeout 되었다. 남은 과제는 real-corpus scale/perf validation, note/serialization manual authoring feel closeout, plotboard/assistant product-fit 검증이다. |
| Phase A-7 | Closure validation active | frontend `npx tsc --noEmit`, focused Jest(`plotboard-graph` 포함), Playwright canonical selection(`bern` + `hp1`)은 `19 / 19` green이고 loop 5 reopened FE blockers는 닫혔다. `scripts/run-local-ci.ps1`는 explicit `-PythonExecutable` path를 지원하며 supported Python `3.12` 기준 backend startup checks, readiness, backend `flake8`, deterministic pytest도 확인되었다. actual `Project #12` HP1 manual rerun spot-check도 landed 되었지만, full backend integration preflight는 local Docker-backed test DB availability가 필요하고 Neo4j persistence는 optional degraded 상태라 gate는 아직 `Yellow`다. |
| Phase A-8 | Hardening loop active | serialization + brainstorming assistant surface, concise prompt baseline, FE markdown render에 더해 deterministic compact reply normalization과 expanded-on-demand baseline이 landed 되었고 quick prompt/copy도 더 절제된 disclosure로 정리되었다. 다만 real-user product-fit tuning, BubbleMenu quality hardening, stronger long-tail guardrail regression은 더 필요하다. |
| Phase B | Blocked-next | visual engine integration은 다음 major focus이지만, 현재는 Phase A hardening closure가 선행 조건이다. |

## 4. Canonical Six-Doc Stack

| Document | Owns | Read When | Must Not Contain |
| --- | --- | --- | --- |
| `odys.md` | 기준선, 문서 소유권, active focus | 새 세션 시작, 문서 읽기 순서 판단 | 상세 증적, 세부 구현 로그 |
| `roadmap.md` | 장기 phase, exit gate, promotion rules | 현재 phase와 다음 승격 조건을 확인할 때 | 현재 코드 사실, file path evidence |
| `feature.md` | current live feature, hierarchy, actor-outcome, primary entry, E2E flow, intentional hold | 지금 제품이 사용자에게 어떻게 보이는지 빠르게 읽을 때 | phase 판단, topology 규범, active WO, release evidence owner |
| `topology.md` | 목표 아키텍처 규범, dependency canon | 구조 변경 허용 여부를 판단할 때 | 완료 판정, smoke 결과, 버그 로그 |
| `mechanism.md` | 현재 코드 사실, evidence, dependency/test entry | 무엇이 실제로 구현되어 있는지, 다음 세션에 어디서 시작할지 확인할 때 | 장기 roadmap, 우선순위 결정 |
| `sprint.md` | active WO, backlog, drift follow-up | 바로 다음 구현 작업과 정리 순서를 확인할 때 | 구조 규범, 장문의 runtime 설명 |

## 5. Current Repository Drift

| Drift | Current Evidence | Impact | Tracking |
| --- | --- | --- | --- |
| Repo-facing branding은 정렬됐지만 package/container identifier는 아직 유지된다 | `frontend/package.json`, `docker-compose.yml`, `docs/SETUP_V2.md` | 현재 사용자/기여자 진입 표면은 Odys 기준선으로 맞춰졌지만, repo-wide identifier rename은 별도 판단이 필요하다. | `mechanism.md`, `sprint.md`, `roadmap.md` |
| Legacy API surface는 제거 완료 | `main.py`에는 Odys v1 라우터만 남아 있고 legacy chat/history/database/document 라우터 코드는 완전히 제거되었다. orphan legacy service(`use_cases/`)와 schema(`presentation/schemas/models.py`)도 cleanup 되었다 | legacy surface drift는 닫혔다. | `topology.md`, `mechanism.md`, `sprint.md` |
| DDD/FSD/BFF rollout은 chapter를 넘어 notes/lore/plotboard/brainstorm/projects까지 확장되었다 | architecture proof는 chapter + notes + lore + plotboard + brainstorm + projects에 걸쳐 landed 되었고, orphan legacy code cleanup도 완료되었다. `domain/models/narrative.py`와 `core/` infra 모듈은 active하지만 위치 조정은 별도 판단이 필요하다. | `topology.md`, `mechanism.md`, `sprint.md`, `roadmap.md` |
| Worldview promotion rollout verification이 아직 부족 | `summary`, `worldview_promoted`, `wiki_metadata`와 backfill migration은 repo에 landed 되었지만, manual smoke와 운영 환경 검증은 더 필요하다. | source wiki와 promoted summary 분리는 구현됐지만 closure evidence는 아직 부족하다. | `mechanism.md`, `sprint.md` |
| Plotboard relation UX는 graph-first authoring으로 크게 전진했지만 아직 closeout은 아니다 | graph는 explicit relation, preset taxonomy, semantic legend/color, direct-connect draft, edge edit pill, inbound source-edit jump, server-persisted layout, category-clustered fallback layout, focus-safe viewport, session-local reset-view, narrow bottom-sheet authoring을 제공하고 save는 side sheet에서 확정된다 | authoring parity blocker는 크게 줄었지만 real-corpus graph feel과 manual validation closeout이 더 필요하다. | `mechanism.md`, `sprint.md`, `roadmap.md` |
| Assistant concise policy가 structured schema는 아님 | backend prompt와 deterministic normalizer가 짧은 진단 + 최대 3개 제안을 canonical output으로 정리하지만 schema-level contract는 아니다 | 품질 회귀와 real-user product-fit tuning을 테스트와 loop로 계속 잡아야 한다. | `mechanism.md`, `sprint.md`, `roadmap.md` |
| Pure note workspace closure evidence가 아직 부족하다 | note workspace baseline은 live이고 folder-backed tree, autosave-only authoring, compact export handoff, mobile move fallback도 존재한다. 다만 large-tree/manual validation과 export/handoff real-user validation은 아직 남아 있다. | zero-intervention scratchpad semantics는 제품선에 들어왔지만, closeout evidence는 이제 주로 validation 쪽을 더 고정해야 한다. | `feature.md`, `topology.md`, `mechanism.md`, `sprint.md`, `roadmap.md` |
| Large-corpus / manual smoke validation이 아직 부족 | lore wiki / plotboard / serialization / assistant surface | mock-backed canonical evidence는 `lore-wiki-large-corpus`에 더해 `bern` + `hp1` corpus family Playwright pack까지 확장되었지만, HP1 real-corpus manual rerun과 체감 UX validation은 아직 남아 있다. | `mechanism.md`, `sprint.md` |
| Backend local verification path는 explicit supported interpreter에서 runnable하다 | `scripts/run-local-ci.ps1`, HP1 validation note | repo venv `3.14`는 여전히 fail-fast 대상이지만 `-PythonExecutable`로 supported Python `3.12`를 지정하면 backend startup/readiness와 deterministic verification은 실제로 동작한다. 남은 제약은 full integration preflight가 local Docker-backed test DB availability에 의존한다는 점이다. | `mechanism.md`, `sprint.md`, `roadmap.md` |
| Deployment workflow execution remains repo-external | repo에는 local verification scripts, container packaging, Railway deployment note가 있으나 provider-side workflow execution 자체는 repo 밖일 수 있다. | 운영 재현성과 온보딩 설명은 좋아졌지만 provider/runtime truth를 완전히 repo 안으로 끌어오진 못했다. | `mechanism.md`, `sprint.md` |

## 6. Reading Order

1. `odys.md`: 현재 기준선과 문서 역할을 먼저 확인한다.
2. `roadmap.md`: phase와 exit gate를 확인한다.
3. `feature.md`: current live feature, actor-outcome, E2E flow, intentional hold를 확인한다.
4. `topology.md`: 이번 변경이 구조적으로 허용되는지 확인한다.
5. `mechanism.md`: 현재 구현 사실, 핵심 의존성, 테스트 경로, 다음 세션 점프 포인트를 확인한다.
6. `sprint.md`: 바로 다음 구현 작업과 drift follow-up을 확인한다.

## 7. Update Rules

| If this changed | Update this doc first | Then sync |
| --- | --- | --- |
| current live feature surface, hierarchy, actor-outcome, primary entry, E2E flow, intentional hold | `feature.md` | `odys.md`, `mechanism.md`, `sprint.md` |
| 구조 경계, 의존성 규칙, state canon | `topology.md` | `odys.md`, `sprint.md` |
| 실제 구현 사실, route, path, dependency/test entry | `mechanism.md` | `odys.md`, `sprint.md` |
| active WO, backlog, drift status | `sprint.md` | `odys.md` |
| phase 순서, exit gate, promotion 기준 | `roadmap.md` | `odys.md`, `sprint.md` |
| 상위 기준선, active focus, 문서 역할 | `odys.md` | 필요 시 하위 문서 |

## 8. Session Start Checklist

1. `odys.md`에서 current phase와 drift를 읽는다.
2. `roadmap.md`에서 이번 작업이 어떤 phase를 움직이는지 확인한다.
3. `feature.md`에서 current live feature, actor-outcome, E2E flow, intentional hold를 확인한다.
4. `topology.md`에서 구조 규범을 확인한다.
5. `mechanism.md`에서 실제 구현 사실, 핵심 파일, 테스트 명령, 남은 limitation을 확인한다.
6. `sprint.md`에서 active WO와 backlog를 확인한다.

## 9. Session Close Checklist

1. 구조 규범이 바뀌었으면 `topology.md`를 갱신한다.
2. current live feature, actor-outcome, primary entry, E2E flow, intentional hold가 바뀌었으면 `feature.md`를 갱신한다.
3. 구현 사실, dependency, evidence, test entry가 바뀌었으면 `mechanism.md`를 갱신한다.
4. WO 상태나 drift 상태가 바뀌었으면 `sprint.md`를 갱신한다.
5. phase gate가 바뀌었으면 `roadmap.md`를 갱신한다.
6. 상위 기준선이나 active focus가 바뀌었으면 `odys.md`를 갱신한다.
