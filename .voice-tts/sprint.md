# voice-tts Sprint (V2)

- Role: 현재 기준선에서 다음 구현 순서를 추적하는 실행 문서
- Source Type: Execution / Backlog
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 4 reference-audio assist + optional service adapter evaluation active-next
- Update Trigger: WO 상태, next action, drift follow-up, baseline evidence가 바뀔 때
- Excluded Content: 구조 규범, 장기 roadmap, 장문의 리서치 본문

## 1. Program Snapshot

- Current focus: reference-audio assist의 최소 범위를 정하고 local CLI debugging canon을 유지하는 것
- Next focus: optional service adapter가 필요한지 domain/application seam 기준으로 평가하는 것
- Current reality: Phase 3 diagnostics/model lifecycle hardening은 닫혔고, 이제 higher-level assist와 adapter decision 단계로 넘어갈 시점이다

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
| TTS | `WO-TTS-001` synthesize command MVP | `completed` | CLI는 `version/doctor`만 있었다 | `voice-tts synthesize` command와 local WAV output policy가 들어왔다 | `src/voice_tts/cli.py`, `src/voice_tts/application/use_cases.py` |
| TTS | `WO-TTS-002` GPT-SoVITS adapter integration | `completed` | placeholder engine만 있었다 | external GPT-SoVITS v2 adapter가 들어왔다 | `src/voice_tts/infrastructure/engines.py` |
| TTS | `WO-TTS-003` model profile repository bootstrap | `completed` | placeholder repository만 있었다 | manifest-backed `ModelProfileRepository`가 들어왔다 | `src/voice_tts/infrastructure/repositories.py`, `config/model-profiles.example.json` |
| Runtime | `WO-ENV-001` richer doctor diagnostics | `completed` | doctor는 bootstrap 진단만 했다 | gpt root, ffmpeg, manifest profile count를 진단한다 | `src/voice_tts/bootstrap/doctor.py` |
| Runtime | `WO-RUNTIME-002` compatibility preflight | `completed` | manifest는 parse만 하고 compatibility는 얕았다 | profile version/config/runtime mismatch를 더 일찍 드러낸다 | `src/voice_tts/bootstrap/doctor.py`, `src/voice_tts/infrastructure/repositories.py` |
| Model | `WO-MODEL-001` richer profile metadata | `completed` | manifest는 최소 필드만 가졌다 | language/speaker tags, notes, compatibility metadata를 확장했다 | `config/`, `src/voice_tts/domain/entities.py` |
| Runtime | `WO-RUNTIME-003` synthesis diagnostics | `completed` | synthesize 성공/실패 정보가 최소였다 | output metadata, timing, richer error context를 추가했다 | `src/voice_tts/application`, `src/voice_tts/infrastructure`, `src/voice_tts/cli.py` |
| TTS | `WO-TTS-004` reference-audio assist | `active` | manual trim flags만 있다 | ref clip prep 보조 흐름의 최소 범위를 정의하고 첫 local-first assist를 설계한다 | `src/voice_tts/infrastructure`, `src/voice_tts/cli.py` |
| Adapter | `WO-API-001` optional service adapter evaluation | `queued` | no web/API surface | local-first가 충분히 단단해진 뒤 FastAPI adapter 여부를 결정한다 | future only |

## 4. Capability Summary

| Capability | Current Judgment | Source of Truth |
| --- | --- | --- |
| Documentation Governance | working | `.voice-tts/voice-tts.md` |
| Local CLI Runtime | working | `.voice-tts/feature.md`, `.voice-tts/mechanism.md` |
| Settings and Manifest Bootstrap | working | `.voice-tts/mechanism.md` |
| Typed Model Profile Catalog | working | `.voice-tts/feature.md`, `.voice-tts/mechanism.md` |
| Profile-aware Diagnostics | working | `.voice-tts/feature.md`, `.voice-tts/mechanism.md` |
| Real GPT-SoVITS Integration | working | `.voice-tts/mechanism.md` |
| Local WAV Output | working | `.voice-tts/feature.md`, `.voice-tts/mechanism.md` |
| Optional Service Adapter | intentionally absent | `.voice-tts/topology.md` |

## 5. Current Drift Follow-up

| Drift | Owner Track | Immediate Next Action |
| --- | --- | --- |
| reference-audio prep가 수동이다 | TTS | assist 범위를 trim-presets, validation helper, clip suggestion 중 어디까지 열지 결정한다 |
| service adapter need가 아직 판단되지 않았다 | Adapter | local CLI 충분성, failure modes, future remote usage를 기준으로 평가한다 |
| profile browsing UX가 아직 CLI에 없다 | Model | 필요 시 read-only listing surface를 별도 phase로 분리할지 판단한다 |
