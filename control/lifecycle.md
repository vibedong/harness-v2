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
package_publish_review -> public_release_published
```

Active slice:

```text
github_source_release_v0.1.6 / npm_publish_deferred / release_closed
```

Scope:

- product writes only under `F:\Folder\harness-v2`;
- generated scaffold hardening is complete;
- executable 8-stage workflow enforcement is complete;
- side-effect preflight adapter work is complete;
- MCP feasibility/design and final quality audit/docs-control sync is complete;
- local MCP stdio adapter implementation, final quality audit, documentation sync, and GitHub push are complete for Goal G;
- hook-equivalent gate hardening is complete for Goal H;
- the gate is an explicit executable check over status, verify, and optional preflight, not a real Codex app hook, shell blocker, or editor blocker;
- integration hardening and release preparation are complete for Goal I;
- the current release path defers npm publish and authorizes Git tag `v0.1.6`, GitHub release creation, release docs/control sync, and the `pyproject.toml` version-consistency amendment;
- `doctor` reports integrated local surfaces and keeps the repeat-release boundary closed;
- no remote MCP hosting, MCP client configuration mutation, Python package registry publish, dependency install, secret access, or destructive operation is part of this lifecycle entry;
- local verification commands named in `control\permission.md`;
- read-only subagent review with `vowline`;
- git add, commit, and push after completed slices pass verification and review;
- no npm publish, Python package registry publish, GitHub release or tag mutation outside the approved `v0.1.6` source release transaction, dependency install from network, secret access, external network mutation outside allowed git/GitHub release operations, or destructive operation outside generated temporary verification artifacts.

This entry moves from `package_publish_review` to `public_release_published` for the exact GitHub source release `v0.1.6`. It is not npm publish, Python package registry publish, future release authority, shell-level automatic enforcement, real hook installation, remote MCP hosting, MCP client installation, or MCP client configuration.

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
