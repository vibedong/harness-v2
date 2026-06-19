# HARNESS V2 Lifecycle Control

status: package_github_surface / workflow_stage_realignment / lifecycle_control

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
- `public_release_candidate`
- `public_release_published`
- `package_candidate_ready`
- `npm_published`
- `blocked`
- `deferred`

## Current Entry

The current local lifecycle entry is:

```text
public_release_published -> workflow_realignment_review
```

Active slice:

```text
canonical_8_stage_realign / unreleased_local / release_closed
```

Scope:

- product writes only under `F:\Folder\harness-v2`;
- published `harness-v2@0.1.7` / `v0.1.7` is closed release history;
- executable `workflow_stage` now follows the canonical task flow from the brainstorming/stage-plan records;
- `artifact_observation`, `routing`, `safety_improvement`, and `release_boundary` are no longer lifecycle workflow stages;
- artifact, routing, safety/regression, and release transaction remain control surfaces;
- generated downstream project scaffold now includes task-local stage records under `records\`;
- generated `records\gate-state.json`, when present, is a validated read-model derived from a source task `workflow_stage` and source hash;
- the hook-equivalent gate remains an explicit status/verify/preflight command, not a real shell/editor hook;
- local verification commands are named in `control\permission.md`;
- no npm publish, Python package registry publish, GitHub release or tag mutation, git push, dependency install, secret access, external mutation, or destructive operation is part of this lifecycle entry.

This entry is not a public release, repeat npm publish, Python package registry publish, future release authority, shell-level automatic enforcement, real hook installation, remote MCP hosting, MCP client installation, MCP client configuration, ApprovalDecision, PermissionDecision, ProofReceipt, or LifecycleTransition.

## Transition Requirements

A later state movement must name:

- source state
- target state
- approval basis
- permission scope
- proof obligation or proof result dependency
- target surface
- stale triggers
- rollback or backtrack target

## Backtrack Rule

Backtrack to `workflow_realignment_authoring`, `package_publish_review`, or `public_release_published` if approval scope, permission scope, source basis, proof obligation, lifecycle target, route surface, artifact surface, safety boundary, improvement classification, release boundary, package surface, npm wrapper surface, generated scaffold behavior, workflow stage enum, or target surface becomes stale or conflicting.

This file does not produce proof, approval, npm publish state, Python package registry publish state, release state, route permission, regression pass, improvement execution, or permission for future slices.
