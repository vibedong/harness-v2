# HARNESS V2 Routing Manifest

status: package_github_surface / remaining_completion_program / routing_manifest

This file maps operation modes to suggested local routes. Routing is guidance, not permission.

## Route Principles

- Choose routes by operation mode and side-effect class, not by skill name alone.
- Check `RULES.md`, `CURRENT.md`, `control\approval.md`, and `control\permission.md` before any side effect.
- Require `vowline` discipline for main-agent and subagent work.
- Treat subagent reports as review material, not approval, permission, proof, lifecycle transition, or release readiness.
- Read depth is evidence-scaled: start with the current-task surfaces and expand only when stale/conflict, side effects, proof/completion claims, lifecycle movement, package/release work, or approval/permission boundary questions require current evidence.

## Operation Routes

| operation mode | suggested route | required boundary |
| --- | --- | --- |
| recovery | read `AGENTS.md`, `RULES.md`, `CURRENT.md`, then relevant surface | stop on stale or conflicting pointer |
| planning | planning records and workflow rules | planning output is not execution |
| approval analysis | `control\approval.md` plus current user packet | approval does not grant side effects |
| local markdown authoring | `CURRENT.md`, `control\permission.md`, `control\proof.md` | write only approved markdown paths |
| development review | source, approval, permission, proof, lifecycle, route, artifact, safety surfaces | findings are not proof |
| proof check | `control\proof.md` plus readback/search/listing | artifact checks must match obligation |
| side-effect preflight | `harness_v2` CLI with `preflight <task> --side-effect ...` or `--path ... --mode write` | preflight checks a proposed action; it does not execute or automatically block shell/editor actions |
| hook-equivalent gate | `harness_v2` CLI with `gate <task> --root .`, or MCP tool `harness_gate` | combines status, verify, and optional preflight; no direct Codex app hook surface was found and this does not automatically block shell/editor actions |
| executable local MVP | `harness_v2` CLI with `status`, `verify`, and `doctor` | only approved local commands and no external dependency |
| integration hardening | `harness_v2` CLI with `doctor --root .` plus status/verify/gate/preflight/MCP/package smoke checks | read-only integration report; does not create release readiness |
| MCP stdio adapter | `python -m harness_v2 mcp` or `node bin\harness-v2.js mcp` with JSON-RPC over stdio | local stdio only; tools wrap existing core behavior and do not replace source, approval, permission, proof, lifecycle, or release boundaries |
| remaining completion program | generated scaffold, workflow engine, preflight adapter, tests, docs/control, and audit surfaces named by current approval | no npm publish, Python package registry publish, release tag, GitHub release, dependency install, secrets, or destructive action outside generated verification artifacts |
| package, GitHub, and npm wrapper MVP | package metadata and wrapper surfaces named by an explicit package slice | package, npm dry-run, registry readback, or release work require current approval, permission, and proof |
| artifact observation | `artifacts\registry.md` and `artifacts\log.md` | registry/log are not source or proof |
| regression safety | `safety\regression.md` | mapping is not pass evidence |
| improvement intake | `safety\improvement.md` | candidate is not product change |
| release boundary | `release\transaction.md` | current npm source-push target is `harness-v2@0.1.13`; repeat npm publish, tag creation, GitHub release execution, Python package registry publish, and deploy require a future transaction |

## Specialist And Subagent Guardrail

Subagents may inspect and review within the prompt-scoped read surface. They must not edit files, grant approval, grant permission, produce ProofReceipt, move lifecycle state, run release work, or widen scope unless a later workflow explicitly gives that authority.

## Layout And Owner Compatibility

compatibility paths remain public targets: `AGENTS.md`, `RULES.md`, `CURRENT.md`, `control\`, `contracts\`, `templates\`, `records\`, `routing\`, `artifacts\`, `safety\`, and `release\`.

domain owner ids are not workflow stages. Workflow stages describe process state; domain owner ids describe responsibility areas.

folder existence, registry rows, log rows, route rows, release notes, and release transaction entries are not authority.

release notes do not create release readiness, publish authority, tag authority, or version authority.

release/package surfaces are not part of the layout task and do not create release readiness, publish authority, tag authority, or version authority.

No domain-centered folder rename or big-bang migration is implied by owner/domain analysis.

## Non-Authority Boundary

This manifest does not grant tool permission, file permission, external permission, approval, proof, lifecycle transition, regression pass, improvement execution, package readiness, or release readiness.
