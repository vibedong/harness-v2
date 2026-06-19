# HARNESS V2 루트 규칙

status: package_github_surface / remaining_completion_program / root_rules

이 파일은 HARNESS V2 package, GitHub, npm wrapper MVP surface의 product-local root rules입니다. `rules\workflows.md`의 workflow rules는 이 규칙을 특화할 수 있지만 약화할 수 없습니다.

현재 HARNESS V2는 scaffold, task-contract validator, CLI helper입니다. 경계를 보이게 만들고 확인 가능하게 만들지만, 자동 enforcement sandbox, completion layer, approval engine, proof generator, lifecycle transition engine, editor, shell, network, release sandbox가 아닙니다.

hook-equivalent gate는 명시적인 local command입니다: `harness-v2 gate <task.json> --root .`. 이 명령은 status, verify, 선택적 preflight를 함께 확인합니다. 실제 Codex app hook을 설치하지 않고, shell이나 editor를 차단하지 않으며, approval을 부여하거나 permission을 넓히거나 proof를 생성하거나 lifecycle state를 이동하지 않습니다.

integration doctor는 명시적인 read-only command입니다: `harness-v2 doctor --root .`. local surface composition과 닫힌 release boundary를 보고합니다. release readiness, approval, permission, proof, lifecycle state를 만들지 않습니다.

## 권한 분리

- `control\source.md`는 무엇을 source로 신뢰할 수 있는지 결정합니다.
- `CURRENT.md`는 visible current workflow pointer와 active surface pointer를 소유합니다.
- `control\approval.md`는 approval request, user response, bound approval scope를 분리합니다.
- `control\permission.md`는 approved intent와 allowed side effect를 분리합니다.
- `control\proof.md`는 proof obligation, artifact check, proof result를 분리합니다.
- `control\lifecycle.md`는 progress note와 workflow state movement를 분리합니다.
- `routing\manifest.md`는 route guidance만 제공합니다.
- `artifacts\registry.md`와 `artifacts\log.md`는 lightweight observability만 제공합니다.
- `safety\regression.md`와 `safety\improvement.md`는 boundary risk control만 제공합니다.
- `release\transaction.md`는 release와 install 작업을 별도 transaction boundary 뒤에 둡니다.

어떤 surface도 다른 surface를 대신하지 않습니다.

## Fail Closed

필요한 source, current pointer, approval scope, permission scope, proof obligation, lifecycle state, route, artifact status, safety boundary, improvement classification, release boundary가 없거나 stale이거나 충돌하거나 scope 밖이면 fail closed합니다.

작업이 현재 exact approval과 permission scope 밖의 path, command, package metadata, npm wrapper metadata, release artifact, dependency change, git operation, secret, external mutation, destructive action, new file, new folder를 요구하면 fail closed합니다.

## 증거 수준에 맞춘 읽기

일반적인 current-task 작업은 `AGENTS.md`, 이 파일, `CURRENT.md`, active task contract 또는 요청이 명시한 current control surface에서 시작할 수 있습니다.

approval, permission, proof, lifecycle movement, stale state, product implementation, package/release work, external mutation, destructive action, secret, git publishing, conflicting pointer가 있으면 readback을 확장합니다. 추가 읽기는 현재 판단에 더 좋은 evidence를 제공해야 하며 approval, permission, proof, lifecycle authority를 대신하지 않습니다.

## Product Write Boundary

현재 package, GitHub, npm wrapper MVP surface는 `CURRENT.md`와 `control\permission.md`에 명시된 파일을 포함합니다.

local writing은 요청된 work unit이 bound approval scope 안에 있고, permission side-effect ceiling 안에 있으며, current proof obligation과 lifecycle entry에 연결된 경우에만 허용됩니다.

package metadata, local verification, Windows/macOS npm wrapper metadata, npm dry-run pack verification, generated scaffold verification, workflow enforcement work, side-effect preflight adapter work, GitHub repository push는 current approval과 permission surface가 명시할 때만 허용됩니다. 현재 remaining completion program은 여전히 npm publish, Python package registry publish, GitHub release creation, release tag creation, network dependency installation, secret access, generated verification artifact 밖의 destructive action을 승인하지 않습니다.

별도의 active release transaction, approval surface, permission surface, proof obligation이 정확한 target을 모두 명시하지 않는 한 npm publish, Python package registry publish, network dependency installation, secret access, release tag creation, GitHub release execution, unrelated external mutation, generated verification artifact 밖의 destructive action을 수행하지 않습니다.

## Guard Catalog

| guard | 의미 |
| --- | --- |
| source guard | 현재 source가 target surface를 명시하고 해당 scope에서 fresh해야 합니다 |
| approval guard | 정확한 user approval이 work unit, target surface, exclusion, stale trigger와 맞아야 합니다 |
| permission guard | side effect는 approved local ceiling 안에 있어야 합니다 |
| proof guard | artifact check는 proof obligation에 대해 평가되기 전까지 evidence material입니다 |
| lifecycle guard | progress note와 current pointer는 그 자체로 lifecycle movement가 되지 않습니다 |
| route guard | route guidance는 tool, file, network, package, git, release permission을 부여하지 않습니다 |
| artifact guard | registry row와 log entry는 index일 뿐 source authority나 proof가 아닙니다 |
| regression guard | mapping과 scenario는 regression pass가 아닙니다 |
| improvement guard | improvement candidate는 직접 product rule을 변경하지 않습니다 |
| release guard | install, package, npm publish, Python package registry publish, deploy, release readiness는 별도 transaction이 필요합니다 |

## 현재 상태

active workflow pointer와 다음 local action은 `CURRENT.md`를 사용합니다. 이 파일 또는 specialized surface와 충돌하면 행동 전에 멈추고 조정합니다.
