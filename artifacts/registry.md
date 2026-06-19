# HARNESS V2 Artifact Registry

status: package_github_surface / remaining_completion_program / artifact_registry

이 파일은 gate-relevant local markdown surface를 위한 lightweight artifact registry입니다. index일 뿐 source authority나 proof가 아닙니다.

## Registry 규칙

source/current truth, approval, permission, proof, lifecycle, route, safety, improvement, release boundary에 영향을 줄 수 있는 artifact만 등록합니다.

전체 transcript registry를 만들거나 모든 temporary note를 등록하지 않습니다.

## Local MVP Row

| artifact id | path | role | authority limit |
| --- | --- | --- | --- |
| root-entry | `AGENTS.md` | product-local entry router | detailed policy가 아님 |
| root-rules | `RULES.md` | common guard catalog | workflow-specific override가 아님 |
| current-pointer | `CURRENT.md` | visible current state와 active surface pointer | proof 또는 release state가 아님 |
| workflow-rules | `rules\workflows.md` | workflow-specific guard application | root rule을 약화할 수 없음 |
| source-control | `control\source.md` | source authority boundary | approval 또는 proof가 아님 |
| approval-control | `control\approval.md` | bound approval scope | side-effect permission이 아님 |
| permission-control | `control\permission.md` | side-effect ceiling | proof가 아님 |
| proof-control | `control\proof.md` | proof obligation과 artifact check boundary | approval 또는 lifecycle이 아님 |
| lifecycle-control | `control\lifecycle.md` | lifecycle state movement boundary | proof 또는 permission이 아님 |
| records-index | `records\README.md` | workflow record lane index | decision ledger가 아님 |
| routing-manifest | `routing\manifest.md` | route guidance | tool permission이 아님 |
| artifact-registry | `artifacts\registry.md` | lightweight index | source authority가 아님 |
| artifact-log | `artifacts\log.md` | concise provenance notes | proof가 아님 |
| regression-safety | `safety\regression.md` | boundary-risk and regression map | regression pass가 아님 |
| improvement-safety | `safety\improvement.md` | improvement candidate classifier | product change가 아님 |
| release-transaction | `release\transaction.md` | release boundary와 transaction gate | release readiness가 아님 |
| root-readme | `README.md` | GitHub-facing overview | source authority 또는 proof가 아님 |
| contracts | `contracts\*.schema.json` | minimal local contract descriptions | runtime proof가 아님 |
| templates | `templates\*` | reusable local templates | task record가 아님 |
| package-metadata | `pyproject.toml` | dependency-free local package metadata | Python package registry publish readiness가 아님 |
| package-backend | `_build_backend\harness_backend.py` | dependency-free local PEP 517 and PEP 660 backend | file existence만으로 proof가 아님 |
| executable-cli | `harness_v2\*.py` | local editable install에 포함되는 stdlib local CLI, verifier, doctor | file existence만으로 proof가 아님 |
| executable-tests | `tests\*` | unittest와 fixture proof material | file existence만으로 ProofReceipt가 아님 |
| side-effect-preflight | `harness_v2\preflight.py` | task contract 기준 local pre-execution side-effect and path check | shell-level blocking이 아님 |
| mcp-stdio-adapter | `harness_v2\mcp.py`, `harness_v2\cli.py`, `tests\test_harness_v2.py` | status, verify, preflight, init, apply를 노출하는 local stdio JSON-RPC adapter | source authority, shell-level blocking, remote MCP hosting이 아님 |
| hook-equivalent-gate | `harness_v2\gate.py`, `harness_v2\cli.py`, `harness_v2\mcp.py`, `tests\test_harness_v2.py` | CLI와 MCP `harness_gate`로 노출되는 status, verify, optional preflight 기반 explicit local gate | real Codex app hook, shell blocker, editor blocker, proof receipt가 아님 |
| integration-doctor | `harness_v2\doctor.py`, `harness_v2\cli.py`, `tests\test_harness_v2.py` | local surface와 closed release boundary를 위한 read-only integration report | release readiness, proof receipt, lifecycle transition이 아님 |
| transition-ledger | `contracts\transition.schema.json`, `templates\transition-log.md`, `harness_v2\lifecycle.py` | transition ledger parsing과 lifecycle transition evaluation | approval, permission, proof receipt, log line에 의한 automatic lifecycle movement가 아님 |
| freshness-map | `contracts\freshness.schema.json`, `templates\freshness-map.json`, `harness_v2\freshness.py` | stale reason과 backtrack target을 가진 optional hash-bound freshness anchors | source authority가 아니며 metadata-only stale clearing 또는 silent project overwrite가 아님 |

## Stale Trigger

registry row는 path, role, authority limit, target surface, proof obligation, owner boundary가 바뀌면 stale이 됩니다.

## 권한 없음 경계

registry row는 approval, permission, proof, lifecycle transition, route permission, regression pass, improvement execution, package readiness, release readiness를 부여하지 않습니다.
