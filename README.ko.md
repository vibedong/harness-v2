# HARNESS V2 사용설명서

HARNESS V2는 AI에게 개발 작업을 맡길 때 작업 범위, 승인, 권한, 검증 의무, 진행 상태를 먼저 기록하고 확인하는 로컬 작업 통제 도구입니다.

Codex, Claude Code, Cursor, Copilot 같은 AI 코딩 도구가 정해진 범위를 잊거나, 검증 없이 완료를 말하거나, 승인되지 않은 부수 효과를 실행하는 위험을 줄이기 위해 사용합니다.

영문 문서는 [README.md](README.md)에 있습니다.

## 무엇인가요?

HARNESS V2는 AI 모델이 아니고, 코드를 대신 작성하는 도구도 아닙니다. AI가 작업하기 전에 기준을 고정하고, 그 기준과 충돌하는 task contract를 fail-closed로 거절하는 하네스입니다.

작업 전에 다음을 적습니다.

- 현재 source와 workflow pointer
- 사용자가 승인한 approval packet
- 이번 작업에서 승인된 경로
- 허용된 side effect와 금지된 side effect
- 완료 전에 필요한 proof obligation
- 현재 lifecycle state와 target state

CLI는 task contract의 구조가 맞는지, 그리고 현재 HARNESS V2 상태와 충돌하지 않는지 확인합니다.

## 언제 사용하나요?

HARNESS V2는 이런 상황에서 유용합니다.

- AI가 여러 파일을 수정해야 할 때
- 사용자가 승인한 작업 범위를 명확히 남기고 싶을 때
- 실행하면 안 되는 명령이나 부수 효과가 있을 때
- 완료 판단을 테스트나 검증 결과에 묶고 싶을 때
- 긴 AI 작업에서 현재 workflow pointer를 잃지 않고 싶을 때
- 패키지, 릴리스, 저장소 작업을 별도 transaction 경계 뒤에 두고 싶을 때

작은 오타 수정이나 단일 파일 수정에는 필요 이상으로 무거울 수 있습니다.

## 어떤 문제를 줄여주나요?

| 문제 | HARNESS V2가 돕는 방식 |
| --- | --- |
| AI가 현재 작업을 잊음 | `CURRENT.md`가 visible workflow pointer를 유지 |
| 승인 범위와 실제 수정 범위가 섞임 | `approval.approved_paths`가 승인된 경로를 기록 |
| 위험한 명령이 일반 작업처럼 섞임 | `permission.allowed_side_effects`와 `permission.denied_side_effects`로 분리 |
| 검증 없이 완료를 말함 | `proof.obligations`가 완료 전 검증을 명시 |
| 진행 메모가 lifecycle state처럼 취급됨 | `lifecycle.current_state`와 `lifecycle.target_state`를 분리 |
| 패키지나 릴리스 작업이 커짐 | 정확한 현재 scope 없이는 release/package 작업을 허용하지 않음 |

HARNESS V2는 위험을 줄이는 도구입니다. 모든 에디터, 셸, 외부 도구를 자동으로 막는 보안 샌드박스는 아닙니다.

## 설치

npm 공개 패키지로 설치합니다.

```powershell
npm install -g harness-v2
```

필수 런타임:

- Node.js 18 이상
- PATH에서 실행 가능한 Python 3.11 이상
- 이번 릴리스의 npm wrapper는 Windows와 macOS 지원

npm 명령은 내부적으로 Python CLI에 위임합니다. HARNESS V2를 JavaScript로 다시 구현한 것이 아닙니다.

## 5분 Quick Start

가장 빠른 첫 성공은 이미 HARNESS V2 control file과 fixture가 들어 있는 이 저장소에서 CLI를 실행해 보는 것입니다.

```powershell
git clone https://github.com/vibedong/harness-v2.git
cd harness-v2
npm install -g harness-v2
harness-v2 status --root .
harness-v2 verify tests\fixtures\valid-task.json
```

정상 동작:

- `status`는 `CURRENT.md`에서 읽은 JSON을 출력합니다.
- `verify`는 valid fixture를 통과시키고 `{"ok": true, ...}`를 출력합니다.

새 task contract를 만들 때는 `templates\task.json`을 형식 참고용으로 사용하고, 현재 `CURRENT.md`와 맞는 값으로 채웁니다.

```json
{
  "task_id": "readme-docs-update",
  "title": "Update public README",
  "workflow": "package_publish_review",
  "source": {
    "basis": ["CURRENT.md", "control\\approval.md", "control\\permission.md"],
    "current_pointer": "CURRENT.md"
  },
  "approval": {
    "packet": "User approved README documentation update",
    "approved_paths": ["README.md", "README.ko.md"],
    "excluded_side_effects": ["package publish", "release execution"]
  },
  "permission": {
    "allowed_side_effects": ["local file writes to README.md and README.ko.md"],
    "denied_side_effects": ["package publish", "release execution", "dependency install from network"]
  },
  "proof": {
    "obligations": ["python -m unittest discover tests"]
  },
  "lifecycle": {
    "current_state": "package_publish_review",
    "target_state": "package_publish_review"
  }
}
```

작성한 task 파일을 검증합니다.

```powershell
harness-v2 verify <task.json>
```

`workflow`와 `lifecycle.current_state`는 `CURRENT.md`의 현재 pointer와 맞아야 합니다.

## 기본 사용 흐름

1. 작업 목표와 source basis를 정합니다.
2. 사용자의 정확한 approval packet을 기록합니다.
3. 승인된 경로를 `approval.approved_paths`에 둡니다.
4. 허용/금지 side effect를 `permission`에 나눕니다.
5. 완료 전 검증을 `proof.obligations`에 둡니다.
6. 진행 메모와 lifecycle 이동을 분리합니다.
7. `harness-v2 verify <task.json>`를 실행합니다.
8. 검증된 contract를 AI 코딩 도구에 줍니다.
9. 완료 전 proof obligation이 실제로 실행되고 보고됐는지 확인합니다.

## 핵심 개념

| 용어 | 뜻 |
| --- | --- |
| task contract | 하나의 작업 단위를 묶는 JSON object |
| `source.basis` | AI가 작업 기준으로 봐야 하는 파일 또는 기록 |
| `source.current_pointer` | 현재 workflow 상태를 가리키는 포인터. 보통 `CURRENT.md` |
| `approval.packet` | 사용자의 정확한 승인 문장 또는 승인 참조 |
| `approval.approved_paths` | 이번 작업에서 승인된 경로 |
| `approval.excluded_side_effects` | 관련 있어 보여도 제외된 행동 |
| `permission.allowed_side_effects` | 이번 작업에서 실행 가능한 명령 또는 효과 |
| `permission.denied_side_effects` | 이번 작업에서 실행하면 안 되는 명령 또는 효과 |
| `proof.obligations` | 완료 전에 확인해야 하는 검증 항목 |
| `lifecycle.current_state` | task가 기대하는 현재 lifecycle state |
| `lifecycle.target_state` | task가 목표로 삼을 수 있는 lifecycle state |

현재 실행 가능한 contract vocabulary는 `contracts\*.schema.json`과 `templates\task.json`에 정의되어 있습니다.

## 자주 쓰는 명령어

현재 workflow pointer를 확인합니다.

```powershell
harness-v2 status --root .
```

task contract를 검증합니다.

```powershell
harness-v2 verify tests\fixtures\valid-task.json
```

파일을 바꾸지 않고 project shape를 점검합니다.

```powershell
python -m harness_v2 doctor --root .
```

로컬 체크아웃에서 Node wrapper를 직접 실행합니다.

```powershell
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
```

## AI에게 작업시킬 때 사용할 프롬프트

task contract를 만든 뒤 AI 코딩 도구에 아래처럼 지시할 수 있습니다.

```text
HARNESS V2 기준으로 작업해줘.

먼저 다음 파일을 읽어.
- CURRENT.md
- AGENTS.md
- RULES.md
- <task.json>

규칙:
- approval.approved_paths를 승인된 수정 표면으로 취급해.
- approval.excluded_side_effects는 실행하지 마.
- permission.denied_side_effects는 실행하지 마.
- 필요한 변경이 범위 밖이면 멈추고 보고해.
- 완료라고 말하기 전에 proof.obligations의 모든 항목을 실행하거나 결과를 보고해.
- 최종 보고에는 변경 파일, 검증 명령, 성공/실패 결과를 포함해.
```

이 프롬프트는 AI에게 주는 작업 지침입니다. 실제 검증 기준은 현재 task contract와 로컬 control file입니다.

## 문제 해결

### `harness-v2 status --root .`가 실패합니다

지정한 root에 `CURRENT.md`가 있는지 확인하세요. `status` 명령은 그 파일에서 현재 pointer를 읽습니다.

### `harness-v2 verify <task.json>`가 실패합니다

자주 발생하는 원인:

- 필수 object가 없음: `source`, `approval`, `permission`, `proof`, `lifecycle`
- `workflow`가 `CURRENT.md`의 workflow와 다름
- `lifecycle.current_state`가 `CURRENT.md`의 state와 다름
- allowed side effect와 denied side effect가 충돌함
- lifecycle state가 `control\lifecycle.md`의 known state에 없음
- control surface에 stale status marker가 남아 있음

### AI가 `approval.approved_paths` 밖의 파일이 필요하다고 합니다

작업을 멈추고 새 approval packet을 받거나, 더 작은 후속 task로 분리하세요. contract를 조용히 넓히지 않는 것이 핵심입니다.

### proof command가 실패합니다

실패한 명령과 결과를 그대로 보고하세요. 기존 실패인지 이번 작업이 만든 실패인지 구분하고, 실패한 proof obligation으로 완료를 주장하지 않습니다.

## 폴더 구조

| 경로 | 역할 |
| --- | --- |
| `AGENTS.md` | 제품-local agent 진입 라우터 |
| `RULES.md` | 제품-local root rules |
| `CURRENT.md` | 현재 workflow pointer |
| `README.md` | 영문 사용설명서 |
| `LICENSE` | MIT license |
| `RELEASE_NOTES.md` | 릴리스 노트 |
| `package.json` | npm wrapper package manifest |
| `bin\harness-v2.js` | Python CLI를 실행하는 Windows/macOS Node wrapper |
| `control\` | source, approval, permission, proof, lifecycle 경계 |
| `contracts\` | JSON schema contract 파일 |
| `templates\` | task, gate, approval, proof template |
| `harness_v2\` | Python CLI와 helper |
| `_build_backend\` | 외부 의존성 없는 로컬 PEP 517 build backend |
| `tests\` | unittest와 fixture |
| `records\`, `routing\`, `artifacts\`, `safety\`, `release\` | 경계와 관찰 기록 표면 |

이 저장소는 schema와 template을 제공합니다. 현재 사용자 task 파일용 `contracts\tasks\` 폴더를 따로 예약하지는 않습니다.

## HARNESS V2가 하지 않는 일

HARNESS V2는 다음을 자동으로 하지 않습니다.

- 코드 작성
- 요구사항 결정
- 모든 외부 도구 자동 차단
- proof command 자동 실행
- 실패한 테스트 자동 수정
- 정확한 별도 transaction scope 없는 패키지 publish나 release 생성
- README 문장을 approval, permission, proof, lifecycle state, release readiness로 바꾸기

## 권장 사용법

- 작은 task contract로 시작합니다.
- `approval.approved_paths`는 좁게 유지합니다.
- package metadata, dependency 변경, secret, deploy, release 작업은 별도 작업으로 분리합니다.
- proof obligation은 실제로 실행 가능할 만큼 짧고, 작업을 증명할 만큼 충분해야 합니다.
- 실패한 proof output은 통과한 것처럼 바꾸지 말고 그대로 남깁니다.
- 문서, 코드, 패키지, 릴리스 작업은 side effect가 다르면 서로 다른 task contract로 나누는 것이 좋습니다.

## 개발자용 검증

이 저장소 루트에서 실행합니다.

```powershell
python -m compileall harness_v2
python -m unittest discover tests
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
npm pack --dry-run
```

외부 의존성 설치 없이 editable package smoke test를 실행합니다.

```powershell
$venv = Join-Path $env:TEMP "harness-v2-smoke-venv"
Remove-Item -Recurse -Force $venv -ErrorAction SilentlyContinue
python -m venv $venv
& (Join-Path $venv "Scripts\python.exe") -m pip install --no-deps -e .
& (Join-Path $venv "Scripts\python.exe") -m harness_v2 status --root .
& (Join-Path $venv "Scripts\python.exe") -m harness_v2 verify tests\fixtures\valid-task.json
Remove-Item -Recurse -Force $venv -ErrorAction SilentlyContinue
```

## 현재 상태

현재 공개 릴리스는 npm의 `harness-v2@0.1.1`입니다.

## 경계 규칙

README는 설명 문서입니다. README 자체는 source authority, approval, permission, proof, lifecycle transition, route permission, regression pass, package readiness, release readiness, product completion을 만들지 않습니다.

## 라이선스

MIT. [LICENSE](LICENSE)를 참고하세요.
