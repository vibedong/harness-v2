# HARNESS V2 Proof Control

status: package_github_surface / transition_ledger_lifecycle_guard / proof_control

workflow: `remaining_completion_program`

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the Goal 2 transition ledger slice, verify after authoring:

1. `contracts\transition.schema.json` and `templates\transition-log.md` define the required transition record fields;
2. `harness_v2\lifecycle.py` can parse, append, and evaluate transition records;
3. appending with a previous ledger hash rejects earlier ledger tampering;
4. lifecycle movement is an evaluated operation, not a log line;
5. the evaluator allows valid route edges and rejects invalid route edges;
6. transition refs are project-relative and, when a root is supplied, existing;
7. legacy aliases such as `approval` are rejected instead of silently mapped to runtime IDs;
8. same-task `improvement -> spec` is rejected and requires a new spec task;
9. `plan_approval -> development` requires active approval and permission references;
10. stale approval, permission, proof, or source evidence fails closed;
11. `development_review -> improvement` requires active approval, active permission, and current proof evidence;
12. the MCP surface remains a local stdio JSON-RPC adapter and not a source of truth;
13. the hook-equivalent gate remains an explicit command surface and does not become a real shell/editor hook;
14. local verification commands pass or blocked commands are reported as blocked;
15. no npm publish, GitHub release, release tag, Python package registry publish, dependency install, secret access, external mutation outside the approved Goal 2 git push, or destructive operation is performed.

## Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root .`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .`

## Artifact Checks

Readback, search, listing, diff output, transition fixture evaluation, and review findings are artifact checks for this slice. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Release Transaction Evidence

No release transaction evidence is required for this local slice because npm publish, GitHub release, release tag, and Python package registry publish are denied.

The previous `harness-v2@0.1.7` / `v0.1.7` release evidence remains closed history and does not authorize this slice to publish.

## Freshness

Proof evidence becomes stale when target files, write surface, approval scope, permission scope, proof obligation, lifecycle state, transition schema, transition log format, route guidance, npm target, release boundary, generated scaffold behavior, workflow stage enum, or automatic-enforcement wording changes.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, package registry publish state, release state, final completion, or future-slice authority.
