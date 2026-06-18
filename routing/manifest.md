# HARNESS V2 Routing Manifest

status: package_github_surface / fourth_slice / routing_manifest

This file maps operation modes to suggested local routes. Routing is guidance, not permission.

## Route Principles

- Choose routes by operation mode and side-effect class, not by skill name alone.
- Check `RULES.md`, `CURRENT.md`, `control\approval.md`, and `control\permission.md` before any side effect.
- Require `vowline` discipline for main-agent and subagent work.
- Treat subagent reports as review material, not approval, permission, proof, lifecycle transition, or release readiness.

## Operation Routes

| operation mode | suggested route | required boundary |
| --- | --- | --- |
| recovery | read `AGENTS.md`, `RULES.md`, `CURRENT.md`, then relevant surface | stop on stale or conflicting pointer |
| planning | planning records and workflow rules | planning output is not execution |
| approval analysis | `control\approval.md` plus current user packet | approval does not grant side effects |
| local markdown authoring | `CURRENT.md`, `control\permission.md`, `control\proof.md` | write only approved markdown paths |
| development review | source, approval, permission, proof, lifecycle, route, artifact, safety surfaces | findings are not proof |
| proof check | `control\proof.md` plus readback/search/listing | artifact checks must match obligation |
| executable local MVP | `harness_v2` CLI with `status`, `verify`, and `doctor` | only approved local commands and no external dependency |
| package, GitHub, and npm wrapper MVP | `pyproject.toml`, `_build_backend`, `package.json`, `bin\harness-v2.js`, editable install smoke, Node wrapper smoke, npm dry-run pack, npm publish dry-run, and GitHub `main` branch | no Python package registry publish, dependency install, secret access, or unrelated external mutation |
| artifact observation | `artifacts\registry.md` and `artifacts\log.md` | registry/log are not source or proof |
| regression safety | `safety\regression.md` | mapping is not pass evidence |
| improvement intake | `safety\improvement.md` | candidate is not product change |
| release boundary | `release\transaction.md` | exact npm publish only for `harness-v2@0.1.0` after npm auth; no Python package registry publish or deploy |

## Specialist And Subagent Guardrail

Subagents may inspect and review within the prompt-scoped read surface. They must not edit files, grant approval, grant permission, produce ProofReceipt, move lifecycle state, run release work, or widen scope unless a later workflow explicitly gives that authority.

## Non-Authority Boundary

This manifest does not grant tool permission, file permission, external permission, approval, proof, lifecycle transition, regression pass, improvement execution, package readiness, or release readiness.
