# HARNESS V2

HARNESS V2는 AI 코딩 작업을 더 안전하고 일관되게 진행하기 위한 로컬 workflow binding 도구입니다.

AI 에이전트가 긴 작업을 하다 보면 승인 범위, 현재 단계, 검증 기준, 금지된 작업을 놓칠 수 있습니다. HARNESS V2는 프로젝트 안에 작업 기준선을 만들어서 에이전트가 무엇을 기준으로 움직여야 하는지 확인할 수 있게 합니다.

이 README는 사람을 위한 제품 설명서입니다. AI가 따라야 하는 세부 규칙은 프로젝트에 생성되는 `AGENTS.md`, `RULES.md`, `CURRENT.md`, `control\`, `contracts\`에 들어갑니다.

## 어떤 도움을 주나요?

HARNESS V2는 AI 에이전트가 다음을 놓치지 않도록 돕습니다.

- 지금 어떤 작업을 하는지
- 어떤 파일을 바꿔도 되는지
- 어떤 명령이나 부수 효과가 금지되어 있는지
- 완료 전에 어떤 검증이 필요한지
- 현재 작업 단계가 어디인지
- 오래된 승인, 계획, proof를 다시 쓰고 있지는 않은지
- release, publish, destructive action 같은 위험 작업이 별도 경계 안에 있는지

작은 오타 수정에는 필요 이상으로 무거울 수 있습니다. 여러 파일을 바꾸는 작업, 긴 세션, context 압축 후 이어가기, 배포 전 점검처럼 경계가 중요한 작업에서 특히 유용합니다.

## 현재 구현 상태

HARNESS V2의 현재 분류는 `workflow_binding_engine`입니다.

정확히 말하면 HARNESS V2는 `explicit CLI/MCP/task-contract surface` 위에서 작동합니다. 즉 task contract, CLI 명령, Python CLI로 위임되는 npm wrapper, local stdio MCP adapter, generated scaffold, test를 기준으로 작업 경계를 확인합니다.

HARNESS V2가 해주는 것:

- `init` / `apply`로 프로젝트 루트에 scaffold 생성
- `status`로 현재 workflow pointer 확인
- `verify`로 task contract 검증
- `gate`로 작업 전 hook-equivalent gate 확인
- `preflight`로 제안된 side effect와 write path 확인
- lifecycle transition, stale/backtrack, approval/permission/proof receipt 검사
- `doctor`로 local integration 상태 확인
- `mcp`로 local stdio MCP adapter 실행

HARNESS V2가 아닌 것:

- 보안 샌드박스
- 실제 shell/editor blocker
- Codex 앱 native hook installer
- 사용자의 판단이나 승인을 대체하는 자동 권한 시스템
- 모든 외부 도구를 자동으로 차단하는 시스템

현재 repo 기준으로 no direct Codex app hook surface was found. 따라서 `gate`는 실제 Codex app hook을 설치하지 않고, does not automatically block your shell or editor. 한국어로 말하면 shell이나 editor를 자동으로 차단하지 않습니다.

## 설치

프로젝트에 HARNESS V2를 적용할 때는 GitHub 저장소를 프로젝트 폴더에 clone하지 않습니다. GitHub clone은 HARNESS V2 자체를 개발하거나 기여할 때 쓰는 방식입니다.

아래처럼 실행하면 대상 프로젝트가 HARNESS V2 소스 저장소가 되어버리므로 적용 방식이 아닙니다.

```powershell
git clone https://github.com/vibedong/harness-v2.git .
```

일반 사용자는 npm으로 CLI를 설치한 뒤, 실제 프로젝트 루트에서 `init`을 실행합니다.

```powershell
npm install -g harness-v2
```

필수 조건:

- Node.js 18 이상
- PATH에서 실행 가능한 Python 3.11 이상
- 현재 npm wrapper는 Windows와 macOS를 대상으로 합니다.

npm 패키지는 JavaScript로 HARNESS V2를 다시 구현한 것이 아닙니다. `harness-v2` 명령은 내부적으로 Python CLI에 위임합니다.

## 프로젝트에 적용하기

프로젝트 폴더에서 실행합니다.

```powershell
harness-v2 init --root .
```

`apply`도 같은 적용 명령입니다.

```powershell
harness-v2 apply --root .
```

기본 동작은 기존 파일을 덮어쓰지 않습니다. 이미 프로젝트에 `AGENTS.md`, `RULES.md`, `CURRENT.md`, `control\` 파일이 있다면 보존합니다.

정상 적용 결과는 프로젝트 안에 `harness-v2` 하위 폴더가 생기는 형태가 아닙니다. 예를 들어 대상이 `F:\my-project`라면 파일은 바로 아래처럼 보여야 합니다.

```text
F:\my-project\AGENTS.md
F:\my-project\RULES.md
F:\my-project\CURRENT.md
F:\my-project\control\
F:\my-project\contracts\
F:\my-project\templates\
```

Do not create or leave a nested `harness-v2` folder inside the project.

만약 `package.json`, `harness_v2\`, `bin\`, `tests\`, `.git` remote가 `vibedong/harness-v2`인 상태가 프로젝트 루트에 보인다면, 그것은 하네스가 적용된 프로젝트가 아니라 HARNESS V2 소스 체크아웃입니다. 이 경우 `harness-v2 doctor --root .`가 source checkout 경고를 표시합니다.

## 5분 Quick Start

```powershell
npm install -g harness-v2
harness-v2 init --root .
harness-v2 status --root .
harness-v2 verify contracts\harness-task.json
harness-v2 gate contracts\harness-task.json --root .
```

정상 동작:

- `init`은 프로젝트 루트에 HARNESS 파일을 생성합니다.
- `status`는 `CURRENT.md`에서 현재 상태를 읽어 JSON으로 출력합니다.
- `verify`는 task contract가 현재 HARNESS 상태와 충돌하지 않는지 확인합니다.
- `gate`는 `status`, `verify`, 선택적 `preflight`를 한 번에 확인합니다.

## 자주 쓰는 명령

현재 상태 확인:

```powershell
harness-v2 status --root .
```

task contract 검증:

```powershell
harness-v2 verify contracts\harness-task.json
```

작업 전 gate 확인:

```powershell
harness-v2 gate contracts\harness-task.json --root .
```

제안된 명령이나 파일 변경을 사전 확인:

```powershell
harness-v2 preflight contracts\harness-task.json --root . --side-effect "python -m unittest discover tests"
```

local 상태 점검:

```powershell
harness-v2 doctor --root .
```

local stdio MCP adapter 실행:

```powershell
harness-v2 mcp --root .
```

MCP adapter는 `status`, `verify`, `preflight`, `gate`, `decision`, `init`, `apply`를 tool로 노출합니다. 노출되는 도구 이름은 `harness_status`, `harness_verify`, `harness_preflight`, `harness_gate`, `harness_decision`, `harness_init`, `harness_apply`입니다.

이 MCP adapter는 기존 HARNESS V2 core를 감싸는 wrapper입니다. It does not replace `CURRENT.md`, task contract, approval, permission, proof, lifecycle, or release boundaries.

## 작업 단계

HARNESS V2의 기본 workflow stage는 8개입니다.

```text
spec
spec_review
plan
plan_review
plan_approval
development
development_review
improvement
```

`workflow_stage`는 task contract에서 쓰는 현재 단계입니다. `current_gate`는 `workflow_stage`에서 파생되는 read-model 값입니다.

`artifact_observation`, `routing`, `safety_improvement`, `release_boundary`는 workflow stage가 아닙니다. 이들은 control 또는 관찰 표면으로 남습니다.

## task contract 예시

HARNESS V2는 작업 단위를 JSON contract로 묶습니다. 아래 예시는 README 수정 같은 문서 작업을 위한 contract입니다.

```json
{
  "task_id": "readme-docs-update",
  "title": "Update public README",
  "workflow": "remaining_completion_program",
  "contract_version": "0.1.8",
  "workflow_stage": "development",
  "current_gate": "development",
  "task_mode": "planned_change",
  "record_strength": "light",
  "risk_flags": ["docs_write_surface"],
  "proof_profile": "current",
  "capability_request": ["local_docs_update"],
  "classification_required": true,
  "record_density": {
    "generated_file_count": 0,
    "required_read_set_size": 3,
    "field_presence": "strict"
  },
  "source": {
    "basis": ["CURRENT.md", "control\\approval.md", "control\\permission.md"],
    "current_pointer": "CURRENT.md"
  },
  "approval": {
    "packet": "User approved README documentation update",
    "approved_paths": ["README.md"],
    "excluded_side_effects": [
      "package publish",
      "release execution",
      "dependency install from network",
      "secret access",
      "external network mutation",
      "destructive operation"
    ]
  },
  "permission": {
    "allowed_side_effects": ["local file writes to README.md"],
    "denied_side_effects": [
      "package publish",
      "release execution",
      "dependency install from network",
      "secret access",
      "external network mutation",
      "destructive operation"
    ]
  },
  "proof": {
    "obligations": ["python -m unittest discover tests"]
  },
  "lifecycle": {
    "current_state": "workflow_realignment_review",
    "target_state": "workflow_realignment_review"
  }
}
```

검증:

```powershell
harness-v2 verify <task.json>
```

## 업데이트 방법

CLI를 최신 버전으로 업데이트합니다.

```powershell
npm install -g harness-v2@latest
```

업데이트 후 프로젝트에서 확인합니다.

```powershell
harness-v2 status --root .
harness-v2 verify contracts\harness-task.json
harness-v2 gate contracts\harness-task.json --root .
```

전역 CLI 업데이트는 프로젝트-local scaffold를 자동으로 덮어쓰지 않습니다. 프로젝트 파일까지 최신 scaffold와 맞추려면 기존 상태를 보존하면서 비교 적용해야 합니다. 특히 `CURRENT.md`, approval, permission, proof, lifecycle 상태는 프로젝트별 현재 상태이므로 무작정 덮어쓰면 안 됩니다.

AI 코딩 도구에 맡길 때는 짧게 말해도 됩니다.

```text
하네스 업데이트해줘.
```

단, README 자체는 AI 지시문이 아닙니다. 실제 작업 규칙은 프로젝트-local HARNESS 파일이 담당합니다.

## 0.1.9 업데이트 내용

- `harness-v2@0.1.9` npm package로 설치/적용 혼동 방지 guard를 배포합니다.
- GitHub clone을 프로젝트 적용 방식으로 오해하지 않도록 README 설치 흐름을 강화했습니다.
- 임의 이름의 프로젝트 폴더에 HARNESS V2 소스가 직접 clone된 경우 `init/apply`가 실패하고 진단을 출력합니다.
- `doctor`가 HARNESS V2 source checkout과 applied project scaffold를 구분해서 보고합니다.
- GitHub/npm 메인 문서는 `README.md` 하나만 사용하고, 별도 `README.ko.md`는 제거했습니다.
- README를 사람을 위한 초보자용 제품 설명서로 정리했습니다.
- 적용 파일이 대상 프로젝트 루트에 바로 생성되도록 정리했습니다.
- `AGENTS.md`, `RULES.md`, `CURRENT.md`, `control\` scaffold를 강화했습니다.
- `status`, `verify`, 선택적 `preflight`를 묶는 hook-equivalent gate를 추가했습니다.
- `status`, `verify`, `preflight`, `gate`, `decision`, `init`, `apply`를 노출하는 local stdio MCP adapter를 포함합니다.
- `doctor`는 local surface와 release boundary를 읽는 read-only integration report로 유지됩니다.

## release와 publish 경계

현재 공개 패키지는 npm 기준입니다. Python package registry publish는 이 README의 사용 경로에 포함하지 않습니다.

release, tag, npm publish는 일반 작업과 별도 경계입니다. HARNESS V2는 release 작업이 일반 파일 수정에 섞이지 않도록 release transaction을 분리해서 다룹니다.

## 한 줄 요약

HARNESS V2는 AI가 작업을 잘하게 만드는 마법이 아니라, AI가 작업 중 기준을 잃지 않도록 프로젝트 안에 확인 가능한 작업 경계를 깔아주는 도구입니다.
