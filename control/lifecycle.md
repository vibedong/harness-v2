# HARNESS V2 Lifecycle Control

status: package_github_surface / stale_backtrack_engine / lifecycle_control

workflow: `remaining_completion_program`

This file separates current pointer, progress note, and lifecycle state movement.

## State Model

Known local states:

- `scaffold_only`
- `planning_artifact_complete`
- `product_markdown_mvp_authoring`
- `product_markdown_mvp_review`
- `executable_mvp_authoring`
- `executable_mvp_review`
- `package_publish_authoring`
- `package_publish_review`
- `npm_wrapper_authoring`
- `npm_wrapper_review`
- `workflow_realignment_authoring`
- `workflow_realignment_review`
- `transition_ledger_authoring`
- `transition_ledger_review`
- `stale_backtrack_authoring`
- `stale_backtrack_review`
- `public_release_candidate`
- `public_release_published`
- `package_candidate_ready`
- `npm_published`
- `blocked`
- `deferred`

## Current Entry

The current local lifecycle entry is:

```text
transition_ledger_review -> stale_backtrack_review
```

Active slice:

```text
stale_backtrack_engine / unreleased_local / release_closed
```

Scope:

- product writes only under `F:\Folder\harness-v2`;
- published `harness-v2@0.1.7` / `v0.1.7` is closed release history;
- executable `workflow_stage` now follows the canonical task flow from the brainstorming/stage-plan records;
- `artifact_observation`, `routing`, `safety_improvement`, and `release_boundary` are no longer lifecycle workflow stages;
- artifact, routing, safety/regression, and release transaction remain control surfaces;
- generated downstream project scaffold now includes task-local stage records under `records\`;
- generated `records\gate-state.json`, when present, is a validated read-model derived from a source task `workflow_stage` and source hash;
- `contracts\transition.schema.json`, `templates\transition-log.md`, and `harness_v2\lifecycle.py` define the Goal 2 transition ledger surface;
- transition log records are append-only evidence and do not move lifecycle state by themselves;
- appending a transition record may be guarded by the previous transition ledger hash so earlier block edits or deletions fail before append;
- lifecycle movement is an evaluated operation, not a log line;
- transition evaluation checks route edge, task source gate, project-relative source refs, approval reference, permission reference, proof reference, freshness refs, and stale check before accepting movement;
- legacy stage aliases and same-task `improvement -> spec` movement fail closed;
- `contracts\freshness.schema.json`, `templates\freshness-map.json`, and `harness_v2\freshness.py` define the Goal 3 freshness/backtrack surface;
- absent freshness maps produce compatibility diagnostics and do not silently overwrite existing projects;
- stale freshness anchors emit explicit `backtrack_target` and `reason` values;
- stale approval, permission, proof, artifact, source, or transition evidence cannot be reused silently;
- the hook-equivalent gate remains an explicit status/verify/preflight command, not a real shell/editor hook;
- local verification commands are named in `control\permission.md`;
- no npm publish, Python package registry publish, GitHub release or tag mutation, dependency install, secret access, external mutation outside the approved Goal 3 git push, or destructive operation is part of this lifecycle entry.

This entry is not a public release, repeat npm publish, Python package registry publish, future release authority, shell-level automatic enforcement, real hook installation, remote MCP hosting, MCP client installation, MCP client configuration, ApprovalDecision, PermissionDecision, ProofReceipt, or an automatic LifecycleTransition.

Goal 5 decision/receipt records are evidence records only. ApprovalDecision, PermissionDecision, and ProofReceipt can satisfy inputs to later lifecycle evaluation, but none of them can declare or perform lifecycle movement by itself.

## Transition Requirements

A lifecycle state movement must be evaluated from a transition record. Lifecycle movement is an evaluated operation, not a log line.

A transition record must name:

- `from_gate`
- `to_gate`
- `reason`
- `source_refs`
- `approval_ref`
- `permission_ref`
- `proof_ref`
- `freshness_refs`
- `stale_check`
- `actor`

The evaluator must reject:

- unknown or legacy gate names;
- route edges outside the canonical same-task route graph;
- `from_gate` that does not match the task contract `workflow_stage`;
- missing, absolute, escaping, or non-existent source or freshness references;
- stale approval, permission, proof, or source evidence;
- `plan_approval -> development` without active approval and permission references;
- `development_review -> improvement` without active approval, active permission, and current proof evidence;
- same-task `improvement -> spec`.

## Backtrack Rule

Backtrack targets for freshness anchors:

- spec source stale -> `spec`
- spec review source stale -> `spec_review` or `spec` depending changed source
- plan source stale -> `plan`
- plan review stale -> `plan_review` or `plan` depending changed source
- plan approval scope stale -> `plan_approval`
- permission side-effect scope stale -> `plan_approval` or `development` depending whether development started
- proof obligation stale -> `development_review` or `development` depending changed source
- transition ledger stale -> last verified lifecycle gate
- release boundary stale -> improvement or blocked release audit

Backtrack to `stale_backtrack_authoring`, `transition_ledger_review`, `workflow_realignment_authoring`, `package_publish_review`, or `public_release_published` if approval scope, permission scope, source basis, proof obligation, lifecycle target, route surface, artifact surface, safety boundary, improvement classification, release boundary, package surface, npm wrapper surface, generated scaffold behavior, workflow stage enum, freshness map, or target surface becomes stale or conflicting.

This file does not produce proof, approval, npm publish state, Python package registry publish state, release state, route permission, regression pass, improvement execution, or permission for future slices.
