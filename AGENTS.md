# HARNESS V2 제품 진입점

status: package_github_surface / remaining_completion_program / entry_router

이 파일은 HARNESS V2의 product-local entry router입니다. 짧게 유지하고, 현재 authority surface를 찾는 용도로만 사용합니다.

현재 HARNESS V2는 project scaffold, task-contract validator, CLI helper입니다. 자동 enforcement sandbox, completion layer, approval engine, proof generator, lifecycle transition engine이 아닙니다.

Goal H는 명시적인 hook-equivalent gate 명령을 추가했습니다. 작업 전 `harness-v2 gate <task.json> --root .`로 status, verify, 선택적 preflight를 함께 확인하되, 이것을 실제 shell/editor blocker나 Codex app hook installation으로 취급하지 않습니다.

Goal I는 `harness-v2 doctor --root .`를 통한 read-only integration hardening을 추가했습니다. 이 출력은 local integration report일 뿐이며 release readiness, proof 자체, lifecycle movement가 아닙니다.

## 읽기 순서

1. `RULES.md`
2. `CURRENT.md`
3. 요청된 작업이 workflow를 명시하면 `rules\workflows.md`
4. 요청된 작업과 관련된 `control\`, `records\`, `routing\`, `artifacts\`, `safety\`, `release\` 하위 파일

나중에 정확한 approval packet, permission preflight, proof obligation, lifecycle entry가 더 넓은 작업을 명시하기 전까지 현재 package와 GitHub MVP surface 밖으로 확장하지 않습니다.

증거 수준에 맞춰 읽습니다. 일반적인 current-task 작업은 짧은 읽기 순서에서 시작할 수 있지만, approval, permission, proof, lifecycle, stale state, release, external mutation, destructive action, product implementation risk가 있으면 행동 전에 더 깊은 source/control readback이 필요합니다.

## 복구 규칙

context compression, resume, handoff, goal continuation 이후:

1. 이 파일을 읽습니다.
2. `RULES.md`를 읽습니다.
3. `CURRENT.md`를 읽습니다.
4. 요청된 작업에 필요한 workflow와 surface 파일만 읽습니다.
5. source, approval, permission, proof, lifecycle, route, artifact, safety, improvement, release state가 없거나 stale이거나 충돌하거나 scope 밖이면 멈춥니다.

## 현재 중지 규칙

작업이 product write를 요청하면, 먼저 요청 대상이 `CURRENT.md`의 current write surface, `control\approval.md`의 bound approval scope, `control\permission.md`의 side-effect ceiling 안에 있는지 확인합니다.

작업이 proof 또는 completion을 요청하면, 먼저 `control\proof.md`의 proof obligation을 확인합니다.

작업이 workflow state 이동을 요청하면, 먼저 `control\lifecycle.md`의 transition requirement를 확인합니다.

작업이 routing, artifact indexing, regression safety, improvement intake, release work를 요청하면 해당 local surface를 읽고 non-authority boundary를 유지합니다.

## 현재 금지 사항

- approval text를 permission으로 취급하지 않습니다.
- permission을 proof로 취급하지 않습니다.
- proof material을 lifecycle state로 취급하지 않습니다.
- route guidance를 side-effect permission으로 취급하지 않습니다.
- registry row나 log entry를 source authority 또는 proof로 취급하지 않습니다.
- regression mapping을 regression pass로 취급하지 않습니다.
- improvement candidate를 product change로 취급하지 않습니다.
- release transaction boundary를 release readiness로 취급하지 않습니다.
- install, init/apply, CLI availability를 automatic enforcement completion으로 취급하지 않습니다.
- 현재 bound approval과 permission scope 밖의 file, code, test, schema, fixture, runner, package, release artifact, dependency, git operation, secret, external mutation, destructive action을 추가하지 않습니다.
