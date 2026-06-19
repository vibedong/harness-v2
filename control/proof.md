# HARNESS V2 Proof Control

status: package_github_surface / whole_plan_conformance_audit / proof_control

workflow: `remaining_completion_program`

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the Goal 6 whole-plan conformance and binding surface audit slice, verify after authoring:

1. canonical stage identifiers match `RULES.md` and `writingplans.md`;
2. `workflow_stage` remains the writable owner and `current_gate` remains a derived/read-model value;
3. transition evaluator exists and denies log-only movement;
4. stale/backtrack engine denies stale approval, permission, proof, source, artifact, and transition reuse;
5. `effective_record_strength` includes `classification_required`;
6. `development` defaults to `light` before risk escalation and raises to `strict` when risk requires it;
7. ApprovalDecision, PermissionDecision, and ProofReceipt evaluators fail closed on broad scope, missing source binding, stale refs, or lifecycle-transition claims;
8. CLI behavior, npm wrapper behavior, MCP wrapper behavior, and hook-equivalent gate behavior remain aligned for exposed status, verify, gate, and doctor surfaces;
9. fresh-project scaffold verification and existing-project preservation are covered by current local tests;
10. docs/control/release surfaces do not claim unsupported automatic external enforcement, npm publish, GitHub release, Python package registry publish, release readiness, proof completion, or lifecycle completion;
11. local verification commands pass or blocked commands are reported as blocked.

## Verification Commands

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

## Artifact Checks

Readback, search, listing, diff output, test output, CLI output, Node wrapper output, npm dry-run output, and review findings are artifact checks for this slice. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Release Transaction Evidence

No release transaction evidence is required for this local slice because npm publish, GitHub release, release tag, and Python package registry publish are denied.

The previous `harness-v2@0.1.7` / `v0.1.7` release evidence remains closed history and does not authorize this slice to publish.

## Freshness

Proof evidence becomes stale when target files, source hashes, approval scope, permission scope, proof obligation, lifecycle state, transition schema, transition log format, freshness map, artifact registry, route guidance, npm target, release boundary, generated scaffold behavior, workflow stage enum, binding-surface classification, or automatic-enforcement wording changes.

## Structured ProofReceipt Records

ProofReceipt records bind a proof obligation to a verifier command or readback method, verifier result, current source hashes, and proof predicates. A test pass, review pass, metadata value, or agent claim is not proof unless it is captured in a current ProofReceipt.

When a task declares that a proof receipt is required, verification fails closed if no ProofReceipt is supplied or if any referenced source hash is stale.

ProofReceipt records cannot grant approval, grant permission, move lifecycle state, or create release readiness.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, package registry publish state, release state, final completion, or future-slice authority.
