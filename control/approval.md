# HARNESS V2 Approval Control

status: package_github_surface / whole_plan_conformance_audit / approval_control

workflow: `remaining_completion_program`

이 파일은 approval request, user response, bound approval scope를 분리합니다.

## Authority Negative Boundary

이 approval surface는 evidence carrier, not authority generator입니다.

폴더 존재, registry row, log row, review note, route row, release note, package metadata, test pass, agent claim은 approval request와 user response를 보조하거나 기록할 수 있지만, 그 자체로 approval을 만들거나 approval scope를 넓히지 않습니다.

## 현재 Bound Scope

현재 bound work unit:

```text
goal_6_whole_plan_conformance_and_binding_surface_audit
```

현재 active slice:

```text
whole_plan_conformance_audit / unreleased_local / no_release_transaction
```

approval basis:

```text
사용자가 F:\Folder\writingplans.md의 remaining work를 Goal mode로 계속 진행하도록 승인했습니다.
Goal 0부터 Goal 5까지는 완료되었습니다.
현재 active Goal은 Goal 6: Whole-plan Conformance And Binding Surface Audit입니다.
```

목적:

- 구현된 HARNESS V2를 whole-plan과 stage-plan source record에 맞춰 audit합니다.
- canonical stage identifier와 current gate ownership을 검증합니다.
- CLI, npm wrapper, generated scaffold, MCP wrapper behavior alignment를 검증합니다.
- compatibility와 fresh-project scaffold behavior를 현재 local test와 command readback으로 검증합니다.
- product를 `workflow_binding_engine`, `advisory_cli_validator`, `blocked` 중 하나로 정직하게 분류합니다.
- release, npm publish, Python package registry publish, tag, GitHub release, dependency, secret, external mutation, destructive boundary를 denied 상태로 유지합니다.

허용된 product write surface:

- `README.md`
- `CURRENT.md`
- `RELEASE_NOTES.md`
- `tests\test_harness_v2.py`
- `safety\regression.md`
- `safety\improvement.md`
- `release\transaction.md`
- `routing\manifest.md`
- `control\source.md`
- `control\approval.md`
- `control\permission.md`
- `control\proof.md`
- `control\lifecycle.md`

## Bound Local Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m harness_v2 status --root .`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root .`
- `python -m harness_v2 doctor --root .`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .`
- `node bin\harness-v2.js doctor --root .`
- `npm pack --dry-run`

## Bound Git/GitHub Commands

- `git add <intended Goal 6 product files>`
- `git commit`
- `git push`

현재 approval scope에서 denied:

- `F:\Folder\harness-v2` 밖의 mutation
- npm publish
- Python package registry publish
- GitHub release creation
- release tag creation
- verified Goal 6 commit 밖의 git push
- network dependency install
- secret access
- approved Goal 6 git push 밖의 external network mutation
- remote MCP hosting
- MCP client configuration mutation
- Codex app configuration mutation 또는 real hook installation
- generated temporary verification artifact 밖의 destructive operation

## Scope 적합성

action은 work unit, target surface, operation type, exclusion, audit check, proof obligation과 맞을 때만 approval scope 안에 있습니다.

일부라도 더 넓거나 누락되었거나 stale이면 approval은 맞지 않으며 workflow는 fail closed합니다.

## Structured ApprovalDecision Records

ApprovalDecision record는 approval request, exact user response, exact edit paths, commands, side effects, git scope, release scope, exclusions, current source refs를 묶습니다.

broad chat response, review pass, metadata, package state, test success, agent claim은 ApprovalDecision record가 아닙니다.

ApprovalDecision은 approval scope를 묶을 수 있지만 permission을 부여하거나, proof를 만들거나, lifecycle state를 이동하거나, active task approval ceiling 밖으로 확장할 수 없습니다.

이 파일은 permission을 부여하지 않고, proof를 만들지 않고, lifecycle state를 이동하지 않고, route permission을 부여하지 않고, regression pass를 만들지 않고, improvement를 실행하지 않고, release를 준비하지 않고, package를 publish하지 않고, GitHub release를 만들지 않고, automatic external enforcement를 주장하지 않습니다.
