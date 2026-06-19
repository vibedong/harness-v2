# HARNESS V2 Proof Control

status: package_github_surface / stale_backtrack_engine / proof_control

workflow: `remaining_completion_program`

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the Goal 3 stale/backtrack slice, verify after authoring:

1. `contracts\freshness.schema.json` and `templates\freshness-map.json` define freshness anchors;
2. `harness_v2\freshness.py` computes source hashes, detects stale anchors, and emits backtrack targets;
3. absent freshness maps produce compatibility diagnostics, not silent overwrites or hard failures;
4. changing a plan source invalidates plan review and plan approval anchors;
5. changing approval scope invalidates permission and development transition anchors;
6. changing proof predicates or tests used as proof invalidates ProofReceipt anchors;
7. changing artifact registry invalidates dependent freshness refs;
8. stale state cannot be cleared by metadata-only freshness map edits;
9. `verify` and MCP verify expose freshness status without turning MCP into source of truth;
10. the local stdio JSON-RPC adapter remains a wrapper over core behavior;
11. the hook-equivalent gate remains an explicit command surface and does not become a real shell/editor hook;
12. local verification commands pass or blocked commands are reported as blocked;
13. no npm publish, GitHub release, release tag, Python package registry publish, dependency install, secret access, external mutation outside the approved Goal 3 git push, or destructive operation is performed.

## Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .`

## Artifact Checks

Readback, search, listing, diff output, freshness fixture evaluation, and review findings are artifact checks for this slice. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Release Transaction Evidence

No release transaction evidence is required for this local slice because npm publish, GitHub release, release tag, and Python package registry publish are denied.

The previous `harness-v2@0.1.7` / `v0.1.7` release evidence remains closed history and does not authorize this slice to publish.

## Freshness

Proof evidence becomes stale when target files, source hashes, approval scope, permission scope, proof obligation, lifecycle state, transition schema, transition log format, freshness map, artifact registry, route guidance, npm target, release boundary, generated scaffold behavior, workflow stage enum, or automatic-enforcement wording changes.

## Structured ProofReceipt Records

Goal 5 adds executable ProofReceipt records.

A ProofReceipt must bind a proof obligation to a verifier command or readback method, verifier result, current source hashes, and proof predicates. A test pass, review pass, metadata value, or agent claim is not proof unless it is captured in a current ProofReceipt.

When a task declares that a proof receipt is required, verification fails closed if no ProofReceipt is supplied or if any referenced source hash is stale.

ProofReceipt records cannot grant approval, grant permission, move lifecycle state, or create release readiness.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, package registry publish state, release state, final completion, or future-slice authority.
