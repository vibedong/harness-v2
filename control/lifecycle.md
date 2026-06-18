# HARNESS V2 Lifecycle Control

status: package_github_surface / fourth_slice / lifecycle_control

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
- `blocked`
- `deferred`

## Current Entry

The current fourth-slice entry is:

```text
executable_mvp_review -> package_publish_review
```

Scope:

- `F:\Folder\harness-v2` folder only;
- local verification commands named in `control\permission.md`;
- package metadata, local package smoke verification, git initialization, GitHub repository creation, and push;
- no PyPI publish, release execution, dependency install, secret access, unrelated external network mutation, or destructive operation outside generated verification artifacts.

This entry records that the local package and GitHub publication surface has moved into review after authoring. It is not PyPI publish, release execution, product completion, or future-slice transition.

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

Backtrack to `executable_mvp_review` or `package_publish_authoring` if approval scope, permission scope, source basis, proof obligation, lifecycle target, route surface, artifact surface, safety boundary, improvement classification, release boundary, package surface, GitHub target, or target surface becomes stale or conflicting.

This file does not produce proof, approval, PyPI publish state, release state, route permission, regression pass, improvement execution, or permission for future slices.
