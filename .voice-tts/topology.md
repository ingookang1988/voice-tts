# voice-tts Topology (V2)

- Role: voice-tts 목표 아키텍처의 규범 SSOT
- Source Type: Normative / Topology
- Baseline Date: 2026-04-14 (KST)
- Current Phase: Phase 2 local synthesis MVP closed
- Update Trigger: layer 경계, dependency canon, package canon, runtime surface ownership이 바뀔 때
- Excluded Content: 완료 판정, smoke 결과, 세부 backlog, 구현 로그

## 1. Interpretation Rules

1. 이 문서는 **규범만** 기록한다. 현재 저장소의 구현 사실은 `mechanism.md`가 기록한다.
2. 목표와 현재 구현이 어긋나면 규범을 낮추지 않는다. 대신 drift를 `voice-tts.md`와 `mechanism.md`에 남긴다.
3. 구조 단위는 `ARCH-*` ID로 추적한다.
4. 현재 제품선은 **local-first CLI synthesis core**이며, web/API는 optional future adapter다.

## 2. Cross-Cutting Rules

1. backend/core compile-time dependency는 `Bootstrap/CLI -> Application -> Domain`만 허용한다.
2. adapter dependency는 `Infrastructure -> Application -> Domain`만 허용한다.
3. domain은 GPT-SoVITS, PyTorch, FastAPI, Pydantic, Typer 구현 세부사항을 모르면 된다.
4. application은 use case와 DTO만 소유하고 infrastructure/CLI를 직접 import하지 않는다.
5. CLI는 public runtime surface지만 orchestration은 application에 위임해야 한다.
6. GPT-SoVITS upstream 코드는 인프라 adapter 뒤에 격리되어야 하며, 여러 레이어에 흩뿌려지면 안 된다.
7. local-first가 현재 canon이지만, 미래의 web adapter가 들어와도 domain/application seam은 그대로 유지해야 한다.

## 3. Layer Canon

| Architecture ID | Layer | Responsibility | Normative Canon | Open / Closed |
| --- | --- | --- | --- | --- |
| `ARCH-DOM-01` | Domain | 순수 도메인 모델과 규칙, ubiquitous language | entity, value object, aggregate, repository/engine port만 둘 수 있으며 framework import를 피한다 | Closed |
| `ARCH-APP-01` | Application | use case, command/result DTO | synthesis workflow를 조율하며 CLI/infrastructure 세부사항을 직접 소유하지 않는다 | Closed |
| `ARCH-INF-01` | Infrastructure | 외부 시스템 adapter, runtime integration | GPT-SoVITS, filesystem, manifest parsing, ffmpeg trim, config loader, logging을 격리한다 | Open |
| `ARCH-CLI-01` | Local Runtime Surface | local command entry and UX | `voice-tts` 명령은 version/doctor/synthesize surface를 소유할 수 있다 | Closed |
| `ARCH-OBS-01` | Diagnostics | bootstrap/runtime validation | `doctor`와 후속 diagnostics는 local troubleshooting canonical path가 된다 | Open |

## 4. Package Structure Canon

현재 canonical package layout은 아래와 같다.

```text
src/
  voice_tts/
    application/
    bootstrap/
    domain/
    infrastructure/
    cli.py
```

규범:

1. `src/voice_tts/domain`은 순수 모델과 port만 소유한다.
2. `src/voice_tts/application`은 DTO와 use case만 소유한다.
3. `src/voice_tts/infrastructure`는 settings, logging, repository adapter, engine adapter, external command helper를 소유한다.
4. `src/voice_tts/bootstrap`은 settings 로드와 의존성 조립을 소유한다.
5. `src/voice_tts/cli.py`는 public command surface를 소유한다.

## 5. Runtime Surface Canon

현재 허용되는 public runtime surface:

- `voice-tts version`
- `voice-tts doctor`
- `voice-tts synthesize`

현재 intentionally absent:

- FastAPI / HTTP API
- background worker
- Docker runtime

규범:

1. 새 public command는 domain/application seam을 우회하지 않는다.
2. `doctor`는 inference를 수행하지 않고 bootstrap/diagnostic concern만 가진다.
3. `synthesize`는 CLI에서 직접 GPT-SoVITS 세부사항을 다루지 않고 use case와 infrastructure adapter를 통한다.

## 6. Integration Canon

핵심 port/interface:

- `SpeechSynthesisEngine`
- `ModelProfileRepository`
- `SynthesizeSpeechUseCase`

규범:

1. real GPT-SoVITS adapter는 `SpeechSynthesisEngine` 구현체로만 들어간다.
2. local manifest/profile lookup은 `ModelProfileRepository` 구현체로만 들어간다.
3. command surface는 use case 호출까지만 알고, model path 해석과 inference는 인프라가 담당한다.
4. external GPT-SoVITS checkout은 `VOICE_TTS_GPT_SOVITS_ROOT`로 주입한다.
5. reference audio trim은 ffmpeg CLI를 통해 인프라에서 수행한다.
6. output artifact policy는 application/use case boundary에서 고정하고, 실제 WAV write는 engine adapter가 수행한다.

## 7. Current Repository Drift

| Drift | Why It Matters |
| --- | --- |
| manifest metadata는 아직 최소 수준이다 | richer compatibility와 browsing UX는 Phase 3 과제다 |
| doctor는 현재 preflight 위주다 | runtime health/weight inventory 진단은 더 넓어질 수 있다 |
| service adapter가 아직 없다 | local-first에는 충분하지만 remote usage는 아직 논외다 |
