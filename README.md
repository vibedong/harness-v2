# HARNESS V2

HARNESS V2는 AI 코딩 작업을 더 안전하고 일관되게 진행하기 위한 로컬 workflow binding 도구입니다.

HARNESS V2는 Codex 앱에서 프로젝트 작업을 시작할 때 AI가 현재 작업 경계, 승인 범위, 증거, 진행 단계, 금지 작업을 놓치지 않게 해 주는 작업 하네스입니다.

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

정확히 말하면 HARNESS V2는 명시적인 CLI, MCP, task contract 표면 위에서 작동합니다. 즉 task contract, CLI 명령, Python CLI로 위임되는 npm wrapper, local stdio MCP adapter, 생성된 scaffold, test를 기준으로 작업 경계를 확인합니다.

HARNESS V2가 해주는 것:

- `init` / `apply`로 프로젝트 루트에 scaffold 생성
- `task start`로 사용자의 실제 작업 요청을 현재 task contract와 `CURRENT.md`에 등록
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

현재 저장소 기준으로 직접 연결되는 Codex app hook 표면은 없습니다. 따라서 `gate`는 실제 Codex app hook을 설치하지 않고, shell이나 editor를 자동으로 차단하지 않습니다.

현재 layout version은 `legacy-control-records-v1`입니다. `status`, `verify`, `doctor`는 이 값을 보고하며, 기존 프로젝트처럼 `layout_version`이 없는 task contract도 같은 legacy layout으로 호환 처리합니다. 알 수 없는 layout version은 migration 진단과 함께 실패합니다.

현재 release에서는 domain layout이 활성화되어 있지 않고, domain layout candidate도 생성하지 않습니다. 현재 runtime lookup과 generated scaffold path는 기존 `control\`, `records\`, `contracts\` 구조를 유지합니다.

`doctor`는 domain layout migration report를 read-only로 보여줍니다. 이 report는 현재 generated scaffold path, package source surface, runtime lookup path를 비교용으로 보여줄 뿐이며, 새 domain folder를 만들거나 기존 프로젝트 파일을 이동하지 않습니다.

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

AI 코딩 도구에게 맡길 때는 길게 설명하지 않아도 됩니다.

```text
이 프로젝트에 HARNESS V2 적용해줘.
```

어떤 하네스를 말하는지 명확히 하고 싶다면 아래처럼 말하면 됩니다.

```text
vibedong/harness-v2 기준으로 이 프로젝트에 HARNESS V2 적용해줘.
```

일상적인 표현으로는 아래처럼 말해도 됩니다.

```text
이 프로젝트에 하네스 설치해줘.
```

HARNESS V2 링크를 같이 주고 싶다면 아래처럼 말해도 됩니다.

```text
https://github.com/vibedong/harness-v2 이 프로젝트에 하네스 설치해줘.
```

이 경우 링크는 어떤 하네스를 설치할지 알려주는 식별자입니다. GitHub 저장소를 현재 프로젝트 폴더에 clone하라는 뜻이 아닙니다.

이 말은 아래 작업을 뜻합니다.

1. npm 최신 패키지로 `harness-v2` CLI를 설치하거나 업데이트합니다.
2. GitHub clone하지 말고 현재 프로젝트 루트에 scaffold만 적용합니다.
3. `harness-v2 init --root .`를 실행합니다.
4. `status`, `verify`, `gate`, `doctor` 결과를 확인합니다.
5. 프로젝트 안에 `harness-v2` 하위 폴더나 HARNESS V2 소스 체크아웃이 생기지 않았는지 확인합니다.

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

프로젝트 안에 중첩된 `harness-v2` 폴더를 만들거나 남겨두지 마세요.

만약 `package.json`, `harness_v2\`, `bin\`, `tests\`, `.git` remote가 `vibedong/harness-v2`인 상태가 프로젝트 루트에 보인다면, 그것은 하네스가 적용된 프로젝트가 아니라 HARNESS V2 소스 체크아웃입니다. 이 경우 `harness-v2 doctor --root .`가 source checkout 경고를 표시합니다.

## 새 프로젝트 scaffold 검증

새 프로젝트 scaffold 검증은 HARNESS V2가 대상 프로젝트 루트 바로 아래에 필요한 파일만 펼치는지 확인하는 audit입니다.

정상 적용 증거:

- 대상 프로젝트 루트 바로 아래 `AGENTS.md`, `RULES.md`, `CURRENT.md`가 생성됩니다.
- 대상 프로젝트 루트 바로 아래 `contracts\harness-task.json`, `control\`, `records\`, `templates\`가 생성됩니다.
- `harness-v2 status --root .`, `harness-v2 verify contracts\harness-task.json`, `harness-v2 gate contracts\harness-task.json --root .`가 통과합니다.
- 중첩된 `harness-v2` 소스 폴더, `harness_v2\`, `bin\`, `package.json`이 생기지 않습니다.

이 검증은 프로젝트에 HARNESS V2 source checkout을 clone하는 것이 아니라, 현재 프로젝트 루트에 scaffold만 적용한다는 경계를 확인합니다.

## 5분 Quick Start

```powershell
npm install -g harness-v2
harness-v2 init --root .
harness-v2 task start --root . --title "현재 작업" --summary "사용자가 요청한 작업을 짧게 요약"
harness-v2 status --root .
harness-v2 verify contracts\harness-task.json
harness-v2 gate contracts\harness-task.json --root .
```

정상 동작:

- `init`은 프로젝트 루트에 HARNESS 파일을 생성합니다.
- `task start`는 사용자의 실제 작업 요청을 `CURRENT.md`와 `contracts\harness-task.json`에 현재 작업으로 등록합니다.
- `status`는 `CURRENT.md`에서 현재 상태를 읽어 JSON으로 출력합니다.
- `verify`는 task contract가 현재 HARNESS 상태와 충돌하지 않는지 확인합니다.
- `gate`는 `status`, `verify`, 선택적 `preflight`를 한 번에 확인합니다.

## 실제 작업 요청 등록

`init` 직후의 `contracts\harness-task.json`은 “하네스가 적용됐다”는 초기 scaffold 증명용입니다. 사용자가 실제 작업을 요청하면, 에이전트는 본격적인 분석이나 파일 변경 전에 그 요청을 현재 작업으로 등록해야 합니다.

```powershell
harness-v2 task start --root . --title "나라장터 실시설계 크롤링 판단" --summary "전체 추출 후 통과/검토필요/제외 판정 흐름을 설계한다."
```

이 명령은 다음을 갱신합니다.

- `CURRENT.md`
- `contracts\harness-task.json`
- `records\current-task.md`

기본 등록 상태는 `spec` 단계의 `scope_pending`입니다. 즉 “이 작업을 하겠다”는 현재 포인터는 생기지만, 코드 수정, 크롤링 실행, dependency install, release, publish, secret, destructive action 같은 권한이 자동으로 열리지는 않습니다. 그런 작업은 별도 승인과 amended task contract가 필요합니다.

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

사용자 요청을 현재 작업으로 등록:

```powershell
harness-v2 task start --root . --title "<짧은 작업명>" --summary "<요청 요약>"
```

local stdio MCP adapter 실행:

```powershell
harness-v2 mcp --root .
```

MCP adapter는 `status`, `verify`, `preflight`, `gate`, `decision`, `init`, `apply`를 tool로 노출합니다. 노출되는 도구 이름은 `harness_status`, `harness_verify`, `harness_preflight`, `harness_gate`, `harness_decision`, `harness_init`, `harness_apply`입니다.

이 MCP adapter는 기존 HARNESS V2 core를 감싸는 wrapper입니다. `CURRENT.md`, task contract, approval, permission, proof, lifecycle, release boundary를 대체하지 않습니다.

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

## README 업데이트 기록 유지 원칙

HARNESS V2의 사용자가 체감하는 변경은 README의 업데이트 내용에 함께 남깁니다.

- release, npm package, scaffold, workflow, CLI, MCP, contract, install/apply 동작이 바뀌면 README의 해당 버전 또는 `local unreleased` 업데이트 섹션을 갱신합니다.
- README 업데이트 내용 없이 release, package, scaffold, workflow 변경을 완료로 말하지 않습니다.
- 자세한 내부 기록은 `RELEASE_NOTES.md`, `CURRENT.md`, control/record surface에 둘 수 있지만, 사용자가 보는 변경 요약은 README에 남깁니다.

이 원칙은 README가 AI 지시문이라는 뜻이 아니라, 공개 사용자 문서가 현재 제품 상태와 어긋나지 않게 하는 documentation/release rule입니다.

## 0.1.12 업데이트 내용

- `harness-v2@0.1.12` npm package로 README 업데이트 기록 유지 원칙을 배포합니다.
- 사용자가 체감하는 release, package, scaffold, workflow, CLI, MCP, contract, install/apply 변경은 README 업데이트 섹션에 함께 남기도록 문서화했습니다.
- README 업데이트 내용 없이 release, package, scaffold, workflow 변경을 완료로 말하지 않도록 테스트를 추가했습니다.
- `0.1.11`의 한국어 `CURRENT.md` heading 정리와 `0.1.10`의 한국어 scaffold/task start 흐름은 그대로 유지합니다.

## local unreleased task binding 업데이트

- `task start`가 `records\current-task.md`뿐 아니라 `records\stages\spec.md`도 현재 사용자 요청으로 갱신하도록 강화했습니다.
- generated `AGENTS.md`와 `RULES.md`는 실제 작업 요청이 들어왔을 때 `records\current-task.md`와 `records\stages\spec.md`가 그 요청을 가리키지 않으면 대화 답변만으로 진행하지 말라고 명시합니다.
- 이 변경은 “하네스 적용만 되고 실제 작업 산출물이 안 보이는” 상태를 줄이기 위한 local unreleased 개선입니다.

## 0.1.11 업데이트 내용

- `harness-v2@0.1.11` npm package로 generated `CURRENT.md`의 남은 영어 heading을 한국어로 정리합니다.
- 새로 적용되는 `CURRENT.md`는 `## 현재 작업`, `## 중지 조건` heading을 사용합니다.
- `0.1.10`의 한국어 scaffold 설명문과 `task start` 흐름은 그대로 유지합니다.

## local unreleased layout 업데이트

- `layout_version` 보고를 추가했습니다. 현재 값은 `legacy-control-records-v1`입니다.
- `status`, `verify`, `doctor`가 현재 layout report를 노출합니다.
- `layout_version`이 없는 기존 task contract는 현재 legacy layout으로 호환됩니다.
- 알 수 없는 layout version은 migration 진단과 함께 fail closed합니다.
- domain layout은 아직 enabled/candidate 상태가 아니며, 현재 scaffold/runtime path는 변경하지 않습니다.
- `doctor`는 `domain_layout_migration` 섹션에서 `current_layout_version`, `generated_scaffold_paths`, `source_package_surfaces`, `runtime_lookup_paths`, `domain_layout_candidate`, `migration_required`, `migration_blockers`를 read-only로 보고합니다.
- 현재 값은 `domain_layout_candidate: false`, `migration_required: false`, `migration_blockers: []`입니다. 이 report 자체는 파일 생성, 이동, 삭제를 수행하지 않습니다.

## 0.1.10 업데이트 내용

- `harness-v2@0.1.10` npm package로 한국어 scaffold 설명문과 `task start` 흐름을 배포합니다.
- 새로 적용되는 `AGENTS.md`, `RULES.md`, `CURRENT.md`, `control\`, `records\`, `templates\` 설명문을 한국어 중심으로 정리했습니다.
- `harness-v2 task start --root .`로 실제 작업 요청을 current task contract에 등록할 수 있습니다.
- task start 결과는 `CURRENT.md`, `contracts\harness-task.json`, `records\current-task.md`에 반영되며, 기존 initial scaffold 상태를 임의 작업 승인으로 오해하지 않도록 `scope_pending` 경계를 둡니다.
- 기존 npm `0.1.9`처럼 설치/적용 혼동 방지 guard와 source checkout 진단은 유지합니다.

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
