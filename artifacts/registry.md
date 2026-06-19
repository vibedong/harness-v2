# HARNESS V2 Artifact Registry

status: package_github_surface / remaining_completion_program / artifact_registry

This file is the lightweight artifact registry for gate-relevant local markdown surfaces. It is an index, not source authority or proof.

## Registry Rule

Register only artifacts that can affect source/current truth, approval, permission, proof, lifecycle, route, safety, improvement, or release boundaries.

Do not build a full transcript registry or register every temporary note.

## Local MVP Rows

| artifact id | path | role | authority limit |
| --- | --- | --- | --- |
| root-entry | `AGENTS.md` | product-local entry router | not detailed policy |
| root-rules | `RULES.md` | common guard catalog | not workflow-specific override |
| current-pointer | `CURRENT.md` | visible current state and active surface pointer | not proof or release state |
| workflow-rules | `rules\workflows.md` | workflow-specific guard application | cannot weaken root rules |
| source-control | `control\source.md` | source authority boundary | not approval or proof |
| approval-control | `control\approval.md` | bound approval scope | not side-effect permission |
| permission-control | `control\permission.md` | side-effect ceiling | not proof |
| proof-control | `control\proof.md` | proof obligation and artifact check boundary | not approval or lifecycle |
| lifecycle-control | `control\lifecycle.md` | lifecycle state movement boundary | not proof or permission |
| records-index | `records\README.md` | workflow record lane index | not decision ledger |
| routing-manifest | `routing\manifest.md` | route guidance | not tool permission |
| artifact-registry | `artifacts\registry.md` | lightweight index | not source authority |
| artifact-log | `artifacts\log.md` | concise provenance notes | not proof |
| regression-safety | `safety\regression.md` | boundary-risk and regression map | not regression pass |
| improvement-safety | `safety\improvement.md` | improvement candidate classifier | not product change |
| release-transaction | `release\transaction.md` | release boundary and transaction gate | not release readiness |
| root-readme | `README.md` | GitHub-facing overview | not source authority or proof |
| contracts | `contracts\*.schema.json` | minimal local contract descriptions | not runtime proof |
| templates | `templates\*` | reusable local templates | not task records |
| package-metadata | `pyproject.toml` | dependency-free local package metadata | not Python package registry publish readiness |
| package-backend | `_build_backend\harness_backend.py` | dependency-free local PEP 517 and PEP 660 backend | not proof by file existence |
| executable-cli | `harness_v2\*.py` | stdlib local CLI, verifier, and doctor packaged for local editable install | not proof by file existence |
| executable-tests | `tests\*` | unittest and fixture proof material | not ProofReceipt by file existence |
| side-effect-preflight | `harness_v2\preflight.py` | local pre-execution side-effect and path check against a task contract | not shell-level blocking |
| mcp-stdio-adapter | `harness_v2\mcp.py`, `harness_v2\cli.py`, `tests\test_harness_v2.py` | local stdio JSON-RPC adapter exposing status, verify, preflight, init, and apply | not source authority, shell-level blocking, or remote MCP hosting |
| hook-equivalent-gate | `harness_v2\gate.py`, `harness_v2\cli.py`, `harness_v2\mcp.py`, `tests\test_harness_v2.py` | explicit local gate over status, verify, and optional preflight exposed through CLI and MCP `harness_gate` | not a real Codex app hook, shell blocker, editor blocker, or proof receipt |
| integration-doctor | `harness_v2\doctor.py`, `harness_v2\cli.py`, `tests\test_harness_v2.py` | read-only integration report for local surfaces and closed release boundary | not release readiness, proof receipt, or lifecycle transition |
| transition-ledger | `contracts\transition.schema.json`, `templates\transition-log.md`, `harness_v2\lifecycle.py` | transition ledger parsing and lifecycle transition evaluation | not approval, permission, proof receipt, or automatic lifecycle movement by log line |
| freshness-map | `contracts\freshness.schema.json`, `templates\freshness-map.json`, `harness_v2\freshness.py` | optional hash-bound freshness anchors with stale reasons and backtrack targets | not source authority, not metadata-only stale clearing, and not silent project overwrite |

## Stale Triggers

A registry row is stale when its path, role, authority limit, target surface, proof obligation, or owner boundary changes.

## Non-Authority Boundary

Registry rows do not grant approval, permission, proof, lifecycle transition, route permission, regression pass, improvement execution, package readiness, or release readiness.
