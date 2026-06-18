# HARNESS V2 Lifecycle Control

status: package_github_surface / remaining_completion_program / lifecycle_control

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
- `public_release_candidate`
- `public_release_published`
- `package_candidate_ready`
- `npm_published`
- `blocked`
- `deferred`

## Current Entry

The current remaining completion program entry is:

```text
package_publish_review -> package_publish_review
```

Active slice:

```text
generated_scaffold_hardening
```

Scope:

- product writes only under `F:\Folder\harness-v2`;
- generated scaffold hardening first;
- later slices may cover executable 8-stage workflow enforcement, side-effect preflight adapter work if locally feasible, MCP feasibility/design only unless separately approved, final quality audit, documentation sync, and GitHub push;
- local verification commands named in `control\permission.md`;
- read-only subagent review with `vowline`;
- git add, commit, and push after completed slices pass verification and review;
- no npm publish, Python package registry publish, GitHub release, release tag, dependency install from network, secret access, external network mutation outside allowed git push, or destructive operation outside generated temporary verification artifacts.

This entry preserves `package_publish_review` while completing missing local behavior and documentation needed for Codex-app-focused use. It is not repeat npm publish, Python package registry publish, public stable release readiness, release execution, automatic enforcement completion, or final product completion.

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

Backtrack to `package_publish_review`, `package_publish_authoring`, `npm_wrapper_authoring`, or `public_release_candidate` if approval scope, permission scope, source basis, proof obligation, lifecycle target, route surface, artifact surface, safety boundary, improvement classification, release boundary, package surface, npm wrapper surface, GitHub target, npm target, generated scaffold behavior, automatic-enforcement wording, or target surface becomes stale or conflicting.

This file does not produce proof, approval, npm publish state, Python package registry publish state, release state, route permission, regression pass, improvement execution, or permission for future slices.
