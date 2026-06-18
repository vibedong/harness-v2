# HARNESS V2 Lifecycle Control

status: package_github_surface / detail_step_20_docs_control_sync / lifecycle_control

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

The current detail step 20 entry is:

```text
package_publish_review -> package_publish_review
```

Scope:

- eleven docs/control files named in `control\approval.md` only;
- local readback/search verification named in `control\permission.md`;
- read-only subagent review with `vowline`;
- git add, commit, and push only for this docs/control sync slice after review passes;
- no package build, npm publish dry-run, repeat npm publish, Python package registry publish, dependency install, secret access, release tag creation, GitHub release execution, hook work, MCP work, unrelated external network mutation, or destructive operation.

This entry records docs/control sync review while preserving the `package_publish_review` state. It is not repeat npm publish, Python package registry publish, release readiness, automatic enforcement completion, product completion, or a future-slice transition.

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

Backtrack to `package_publish_review`, `package_publish_authoring`, `npm_wrapper_authoring`, or `public_release_candidate` if approval scope, permission scope, source basis, proof obligation, lifecycle target, route surface, artifact surface, safety boundary, improvement classification, release boundary, package surface, npm wrapper surface, GitHub target, npm target, automatic-enforcement wording, or target surface becomes stale or conflicting.

This file does not produce proof, approval, npm publish state, Python package registry publish state, release state, route permission, regression pass, improvement execution, or permission for future slices.
