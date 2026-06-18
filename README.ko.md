# HARNESS V2 사용설명서

HARNESS V2는 AI와 함께 소프트웨어 작업을 할 때 사용하는 로컬 워크플로우 하네스입니다. 목표, 승인, 권한, 증거, 진행 상태, 라우팅, 산출물, 회귀 위험, 개선 후보, 릴리스 경계를 문서와 실행 검증으로 묶어 줍니다.

영문 문서는 [README.md](README.md)에 있습니다.

## 현재 상태

현재 공개 릴리스는 npm의 `harness-v2@0.1.1`입니다.

이 저장소에는 다음이 들어 있습니다.

- 작업 경계를 기록하는 product-local markdown control 문서
- JSON contract와 task template
- 표준 라이브러리만 사용하는 Python CLI
- 외부 의존성 없는 로컬 package metadata와 build backend
- Python CLI에 위임하는 Windows/macOS용 npm CLI wrapper
- task 검증을 위한 unittest와 fixture

## 설치

npm에서 설치합니다.

```powershell
npm install -g harness-v2
```

필수 런타임:

- Node.js 18 이상
- PATH에서 실행 가능한 Python 3.11 이상
- 이번 릴리스의 npm wrapper는 Windows와 macOS를 지원

설치 확인:

```powershell
harness-v2 status --root .
```

## CLI 사용법

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

npm 명령은 내부적으로 Python CLI를 실행합니다. HARNESS V2를 JavaScript로 다시 구현한 것이 아닙니다.

## 하네스 사용 흐름

HARNESS V2는 작업 단위마다 명시적인 task contract가 있을 때 가장 잘 작동합니다.

1. 현재 source와 workflow pointer를 정합니다.
2. 사용자가 승인한 범위를 기록합니다.
3. 허용된 side effect와 금지된 side effect를 분리합니다.
4. 완료를 말하기 전에 필요한 proof obligation을 정합니다.
5. 진행 메모와 lifecycle 전환을 분리합니다.
6. `harness-v2 verify`로 task contract를 검증합니다.

기본 fixture는 작은 예시입니다.

```powershell
harness-v2 verify tests\fixtures\valid-task.json
```

승인, 권한, 증거, lifecycle state, workflow pointer가 충돌하면 verifier는 fail closed로 실패합니다.

## 로컬 개발 검증

저장소 루트에서 실행합니다.

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
| `contracts\` | JSON contract 파일 |
| `templates\` | task, gate, approval, proof template |
| `harness_v2\` | Python CLI와 helper |
| `_build_backend\` | 외부 의존성 없는 로컬 PEP 517 build backend |
| `tests\` | unittest와 fixture |
| `records\`, `routing\`, `artifacts\`, `safety\`, `release\` | 경계와 관찰 기록 표면 |

## 경계 규칙

README는 설명 문서입니다. README 자체는 source authority, approval, permission, proof, lifecycle transition, route permission, regression pass, package readiness, release readiness, product completion을 만들지 않습니다.
