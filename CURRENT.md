# HARNESS V2 현재 상태

status: package_github_surface / whole_plan_conformance_audit / current_pointer

이 파일은 local HARNESS V2 product surface의 visible current pointer입니다.

## 현재 Workflow

workflow: `remaining_completion_program`

state: `workflow_realignment_review`

substate: `workflow_binding_engine_classified / unreleased_local / release_closed`

source basis:

- Stage 00~05 confirmed planning artifacts.
- whole-plan과 stage-plan records. 이 기록들은 canonical task flow를 `spec`, `spec_review`, `plan`, `plan_review`, `plan_approval`, `development`, `development_review`, `improvement`로 정의합니다.
- published npm/GitHub state `harness-v2@0.1.7` / `v0.1.7`. 이제 closed release history로 취급합니다.
- workflow stage는 brainstorming/stage-plan flow를 따라야 하며, control surface를 `workflow_stage`에 섞으면 안 된다는 사용자 correction.
- package가 현재 주로 owner에게 사용되므로 recommended clean-break direction을 사용한다는 사용자 direction.

## 현재 Program

local worktree는 post-0.1.7 workflow engine completion and conformance audit slice 상태입니다.

완료된 release history:

- generated scaffold hardening
- side-effect preflight adapter
- MCP stdio adapter implementation
- hook-equivalent gate hardening
- closed `harness-v2@0.1.7` npm package history reference
- closed `v0.1.7` GitHub release history reference

현재 active slice:

- executable `workflow_stage`가 canonical task flow와 맞는지 audit하고 보존합니다.
  - `spec`
  - `spec_review`
  - `plan`
  - `plan_review`
  - `plan_approval`
  - `development`
  - `development_review`
  - `improvement`
- later explicit migration이 ownership을 바꾸기 전까지 `workflow_stage`를 writable compatibility owner로 유지하고 `current_gate`는 여기서 파생합니다.
- 기존 `0.1.7` task contract가 `current_gate`, `task_mode`, `record_strength`를 생략해도 compatible하게 유지합니다. `current_gate`를 파생하고, missing `task_mode`는 `planned_change`, missing `record_strength`는 `minimal`로 default하며, stage와 task-mode rule에서 `effective_record_strength`를 계산합니다.
- required Goal 0 field가 없는 strict contract는 migration diagnostic과 함께 fail합니다.
- `artifact_observation`, `routing`, `safety_improvement`, `release_boundary`를 workflow stage에서 제거합니다.
- artifact, routing, safety/regression, release transaction은 control surface로 유지합니다.
- generated task-local records scaffold를 `records\` 아래에 추가합니다.
- npm publish, GitHub release, release tag, dependency install, secret access, destructive work 없이 local verification을 수행합니다.
- 이 local Goal 6 audit slice를 새 npm publish, GitHub release, release tag로 취급하지 않습니다.
- 현재 explicit CLI/MCP/task-contract surface를 `advisory_cli_validator`나 `blocked`가 아니라 `workflow_binding_engine`으로 분류합니다. 다만 HARNESS V2가 automatic shell/editor blocker 또는 Codex app hook installer가 아니라는 경계는 유지합니다.
- current layout version은 `legacy-control-records-v1`로 보고합니다.
- `status`, `verify`, `doctor`는 `layout_version`, `current_layout_paths_active`, `domain_layout_enabled`, `domain_layout_candidate`를 노출합니다.
- `layout_version`이 없는 기존 task contract는 current legacy layout으로 호환 처리합니다.
- unknown layout version은 migration diagnostic과 함께 fail closed합니다.
- domain layout은 아직 enabled 또는 candidate가 아니며, runtime lookup path와 generated scaffold path는 기존 `control\`, `records\`, `contracts\` 구조를 유지합니다.
- 새 프로젝트 scaffold 검증은 `init`이 대상 프로젝트 루트 바로 아래에 `AGENTS.md`, `RULES.md`, `CURRENT.md`, `contracts\harness-task.json`, `control\`, `records\`, `templates\`를 만들고, 중첩 source checkout 폴더를 만들지 않는지 확인합니다.
- README 업데이트 기록 유지: 사용자가 체감하는 release, package, scaffold, workflow, CLI, MCP, contract, install/apply 변경은 README 업데이트 섹션에 함께 남겨야 합니다. README 업데이트 내용 없이는 해당 변경을 완료로 말하지 않습니다.

## Codex 앱 적용 안내

HARNESS V2는 Codex 앱에서 프로젝트 작업을 시작할 때 AI가 현재 작업 경계, 승인 범위, 증거, 진행 단계, 금지 작업을 놓치지 않게 해 주는 작업 하네스입니다.

사용자는 보통 아래처럼 말하면 됩니다.

```text
이 프로젝트에 HARNESS V2 적용해줘.
```

어떤 하네스를 적용할지 명확히 해야 하면 아래처럼 말합니다.

```text
vibedong/harness-v2 기준으로 이 프로젝트에 HARNESS V2 적용해줘.
```

HARNESS V2는 설치만으로 Codex 앱을 자동 차단하는 샌드박스가 아닙니다. 에이전트는 `AGENTS.md`, `RULES.md`, `CURRENT.md`, active task contract, `status`, `verify`, `gate`, `doctor` 결과를 기준으로 행동해야 합니다.

미래 release path:

- npm publish, GitHub release/tag mutation, Python package registry publish, dependency installation, secret access, destructive work, external mutation은 나중에 정확한 approval packet과 release transaction이 있어야 합니다.

## 현재 Surface

active package, npm wrapper, scaffold, workflow, preflight, local MCP stdio adapter, audit file은 아래를 포함할 수 있습니다.

- `.gitattributes`
- `.gitignore`
- `AGENTS.md`
- `RULES.md`
- `CURRENT.md`
- `README.md`
- `LICENSE`
- `RELEASE_NOTES.md`
- `package.json`
- `pyproject.toml`
- `_build_backend\harness_backend.py`
- `bin\harness-v2.js`
- `rules\workflows.md`
- `control\source.md`
- `control\approval.md`
- `control\permission.md`
- `control\proof.md`
- `control\lifecycle.md`
- `records\README.md`
- `routing\manifest.md`
- `artifacts\registry.md`
- `artifacts\log.md`
- `safety\regression.md`
- `safety\improvement.md`
- `release\transaction.md`
- `contracts\*.schema.json`
- `templates\*.json`
- `templates\*.md`
- `harness_v2\*.py`
- `tests\*.py`
- `tests\fixtures\*.json`

generated downstream project scaffold는 `records\current-task.md`, `records\stages\*.md`, `records\decisions.md`, `records\proof.md`, `records\handoff.md`를 포함할 수 있습니다.

## 현재 허용된 Local Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js preflight tests\fixtures\valid-task.json --side-effect "python -m compileall harness_v2"`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root . --side-effect "python -m compileall harness_v2"`
- `node bin\harness-v2.js doctor --root .`
- `node bin\harness-v2.js mcp < JSON-RPC smoke input`
- `node bin\harness-v2.js init --root <temporary project>`
- `python -m harness_v2 status --root <repo root>`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 preflight tests\fixtures\valid-task.json --side-effect "python -m unittest discover tests"`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root . --side-effect "python -m unittest discover tests"`
- `python -m harness_v2 doctor --root <repo root>`
- `python -m harness_v2 mcp < JSON-RPC smoke input`
- `python -m harness_v2 init --root <temporary project>`
- `python -m harness_v2 verify <temporary project>\contracts\harness-task.json`
- `npm pack --dry-run`

## 중지 조건

요청된 action이 `F:\Folder\harness-v2` 밖의 파일을 필요로 하면 멈춥니다.

요청된 action이 npm publish, Python package registry publish, GitHub release or tag mutation, git push, dependency installation from network, secret access, external network mutation, generated temporary verification artifact 밖의 destructive operation을 필요로 하면 멈춥니다.

pointer, source, approval, permission, proof obligation, lifecycle requirement, route, registry/log row, safety boundary, improvement classification, release boundary가 없거나 stale이거나 충돌하면 멈춥니다.

이 파일은 current pointer입니다. shell-level automatic enforcement, future release authority, real Codex app hook installation, remote MCP hosting, MCP client installation, MCP client configuration state를 주장하지 않습니다.
