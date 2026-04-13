# voice-tts Sprint (V2)

- Role: 현재 기준선에서 다음 구현 순서를 추적하는 실행 문서
- Source Type: Execution / Backlog
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 2 core synthesis MVP active-next
- Update Trigger: WO 상태, next action, drift follow-up, baseline evidence가 바뀔 때
- Excluded Content: 구조 규범, 장기 roadmap, 장문의 리서치 본문

## 1. Program Snapshot

- Current focus: GPT-SoVITS를 local-first seam에 실제로 연결하고 synthesize command를 여는 것
- Next focus: local weight repository와 output audio happy path 추가
- Current reality: Phase 1 bootstrap은 닫혔고, 이제 placeholder adapter를 real inference path로 교체할 시점이다

## 2. Execution Rules

1. `completed`는 실제 file path evidence와 동작 근거가 있을 때만 사용한다.
2. `active`는 지금 바로 손대야 하는 항목이다.
3. `queued`는 다음 순서로 등록된 항목이다.
4. `drift`는 코드와 목표 사이에 명시적 불일치가 남아 있는 상태다.

## 3. Active Work Order Board

| Track | Work Order | Status | Current As-Is | Target | Proof / Next Action |
| --- | --- | --- | --- | --- | --- |
| Docs | `WO-DOC-001` local six-doc stack bootstrap | `completed` | local docs stack이 필요했다 | `.voice-tts/` six-doc stack과 implementation sync를 맞췄다 | `.voice-tts/*.md` |
| Bootstrap | `WO-BOOT-001` local-first skeleton | `completed` | docs-only repo였다 | `uv`, `src/voice_tts`, CLI, settings, tests가 들어왔다 | `pyproject.toml`, `src/voice_tts`, `tests` |
| TTS | `WO-TTS-001` synthesize command MVP | `active` | CLI는 `version/doctor`만 있다 | `voice-tts synthesize` command를 추가하고 local output happy path를 연다 | `src/voice_tts/cli.py`, `src/voice_tts/application/use_cases.py` |
| TTS | `WO-TTS-002` GPT-SoVITS adapter integration | `active` | placeholder engine만 있다 | real GPT-SoVITS adapter로 `SpeechSynthesisEngine`를 구현한다 | `src/voice_tts/infrastructure/engines.py` |
| TTS | `WO-TTS-003` weight repository bootstrap | `queued` | placeholder repository만 있다 | local file-backed `WeightRepository`와 metadata contract를 만든다 | `src/voice_tts/infrastructure/repositories.py` |
| Runtime | `WO-ENV-001` richer doctor diagnostics | `queued` | doctor는 bootstrap 진단만 한다 | model path, weight manifest, optional CUDA/GPU readiness까지 진단 범위를 넓힌다 | `src/voice_tts/bootstrap/doctor.py` |
| Test | `WO-TEST-001` synthesis smoke | `queued` | bootstrap test만 있다 | synthesize happy path와 failure path smoke를 추가한다 | `tests/` |
| Adapter | `WO-API-001` optional web adapter | `queued` | no web/API surface | local-first가 안정화되면 FastAPI adapter 여부를 결정한다 | future only |

## 4. Capability Summary

| Capability | Current Judgment | Source of Truth |
| --- | --- | --- |
| Documentation Governance | working | `.voice-tts/voice-tts.md` |
| Local CLI Bootstrap | working | `.voice-tts/feature.md`, `.voice-tts/mechanism.md` |
| Settings and Validation | working | `.voice-tts/mechanism.md` |
| Clean Architecture Seams | working | `.voice-tts/topology.md`, `.voice-tts/mechanism.md` |
| Real GPT-SoVITS Integration | not started | `.voice-tts/mechanism.md`, `.voice-tts/roadmap.md` |
| Local Audio Output | not started | `.voice-tts/roadmap.md` |
| Optional Service Adapter | intentionally absent | `.voice-tts/topology.md` |

## 5. Current Drift Follow-up

| Drift | Owner Track | Immediate Next Action |
| --- | --- | --- |
| placeholder engine | TTS | GPT-SoVITS adapter spike를 실제 import/wrapper 방향으로 교체한다 |
| placeholder repository | TTS | local speaker/model weight metadata contract를 만든다 |
| no synthesize command | TTS | CLI public surface를 Phase 2 범위로 확장한다 |
| doctor is bootstrap-only | Runtime | model/runtime diagnostics를 추가한다 |
| no output artifact policy | TTS | output audio path, naming, overwrite policy를 고정한다 |
