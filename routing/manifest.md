# HARNESS V2 Routing Manifest

status: package_github_surface / remaining_completion_program / routing_manifest

이 파일은 operation mode를 suggested local route에 매핑합니다. routing은 guidance이며 permission이 아닙니다.

## Route 원칙

- skill name만 보지 말고 operation mode와 side-effect class로 route를 선택합니다.
- side effect 전에 `RULES.md`, `CURRENT.md`, `control\approval.md`, `control\permission.md`를 확인합니다.
- main agent와 subagent 모두 `vowline` discipline을 적용합니다.
- subagent report는 review material일 뿐이며 approval, permission, proof, lifecycle transition, release readiness가 아닙니다.
- read depth는 evidence-scaled입니다. current-task surface에서 시작하고, stale/conflict, side effect, proof/completion claim, lifecycle movement, package/release work, approval/permission boundary question이 현재 evidence를 요구할 때만 확장합니다.

## Operation Route

| operation mode | suggested route | required boundary |
| --- | --- | --- |
| recovery | `AGENTS.md`, `RULES.md`, `CURRENT.md`를 읽은 뒤 관련 surface | stale 또는 conflicting pointer면 중지 |
| plan | plan records와 workflow rules | plan output은 execution이 아님 |
| plan approval analysis | `control\approval.md`와 current user packet | approval은 side effect를 부여하지 않음 |
| local markdown authoring | `CURRENT.md`, `control\permission.md`, `control\proof.md` | 승인된 markdown path만 write |
| development review | source, approval, permission, proof, lifecycle, route, artifact, safety surfaces | finding은 proof가 아님 |
| proof check | `control\proof.md`와 readback/search/listing | artifact check는 obligation과 맞아야 함 |
| current gate read-model | task contract `workflow_stage`와 optional `records\gate-state.json` | gate-state는 generated/hash-bound이며 approval, permission, proof, lifecycle transition, release readiness가 아님 |
| lifecycle transition evaluation | `contracts\transition.schema.json`, `templates\transition-log.md`, `harness_v2.lifecycle` | transition record는 evidence이며 lifecycle movement는 log line이 아니라 evaluated operation |
| side-effect preflight | `harness_v2` CLI의 `preflight <task> --side-effect ...` 또는 `--path ... --mode write` | preflight는 proposed action을 확인하며 실행하거나 shell/editor action을 자동 차단하지 않음 |
| hook-equivalent gate | `harness_v2` CLI의 `gate <task> --root .` 또는 MCP tool `harness_gate` | status, verify, optional preflight를 결합함. direct Codex app hook surface는 없고 shell/editor action을 자동 차단하지 않음 |
| executable local MVP | `status`, `verify`, `doctor`를 가진 `harness_v2` CLI | 승인된 local command만, external dependency 없음 |
| integration hardening | `doctor --root .`와 status/verify/gate/preflight/MCP/package smoke check | read-only integration report이며 release readiness를 만들지 않음 |
| MCP stdio adapter | `python -m harness_v2 mcp` 또는 `node bin\harness-v2.js mcp`의 JSON-RPC over stdio | local stdio only. tool은 existing status, verify, preflight, gate, decision, init, apply behavior를 감쌀 뿐 source, approval, permission, proof, lifecycle, release boundary를 대체하지 않음 |
| remaining completion program | current approval이 명시한 generated scaffold, workflow engine, preflight adapter, tests, docs/control, audit surfaces | npm publish, Python package registry publish, release tag, GitHub release, dependency install, secrets, generated verification artifact 밖 destructive action 없음 |
| package, GitHub, and npm wrapper MVP | explicit package slice가 명시한 package metadata와 wrapper surfaces | package, npm dry-run, registry readback, release work는 current approval, permission, proof 필요 |
| artifact observation | `artifacts\registry.md`, `artifacts\log.md` | registry/log는 source나 proof가 아님 |
| regression safety | `safety\regression.md` | mapping은 pass evidence가 아님 |
| improvement intake | `safety\improvement.md` | candidate는 product change가 아님 |
| release boundary | `release\transaction.md` | 마지막 recorded package version reference는 `harness-v2@0.1.7`; npm publish, tag creation, GitHub release execution, Python package registry publish, deploy는 future transaction 필요 |

## Specialist/Subagent Guardrail

subagent는 prompt-scoped read surface 안에서 inspect와 review를 할 수 있습니다. later workflow가 명시적으로 권한을 주기 전에는 file edit, approval grant, permission grant, ProofReceipt production, lifecycle state movement, release work, scope widening을 할 수 없습니다.

## 권한 없음 경계

이 manifest는 tool permission, file permission, external permission, approval, proof, lifecycle transition, regression pass, improvement execution, package readiness, release readiness를 부여하지 않습니다.
