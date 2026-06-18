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
- `npm_wrapper_authoring`
- `npm_wrapper_review`
- `public_release_candidate`
- `public_release_published`
- `package_candidate_ready`
- `npm_published`
- `blocked`
- `deferred`

## Current Entry

The current fourth-slice entry is:

```text
package_publish_review -> package_publish_review
```

Scope:

- `F:\Folder\harness-v2` folder only;
- local verification commands named in `control\permission.md`;
- package metadata, local editable package smoke verification, Windows/macOS npm wrapper metadata, local Node wrapper proof, npm dry-run pack proof, npm publish dry-run proof, npm registry readback for `harness-v2@0.1.5`, git initialization, and GitHub repository push;
- no repeat npm publish, Python package registry publish, dependency install, secret access, release tag creation, GitHub release execution, unrelated external network mutation, or destructive operation outside generated verification artifacts.

This entry records that the local package, GitHub publication, npm wrapper surface, and npm published surface remain in review until proof is complete. It is not repeat npm publish, Python package registry publish, product completion, or future-slice transition.

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

Backtrack to `package_publish_review`, `package_publish_authoring`, `npm_wrapper_authoring`, or `public_release_candidate` if approval scope, permission scope, source basis, proof obligation, lifecycle target, route surface, artifact surface, safety boundary, improvement classification, release boundary, package surface, npm wrapper surface, GitHub target, npm target, or target surface becomes stale or conflicting.

This file does not produce proof, approval, npm publish state, Python package registry publish state, release state, route permission, regression pass, improvement execution, or permission for future slices.
