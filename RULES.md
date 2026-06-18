# HARNESS V2 Root Rules

status: package_github_surface / fourth_slice / root_rules

These are the product-local root rules for the HARNESS V2 package, GitHub, and npm wrapper MVP surface. Workflow rules in `rules\workflows.md` may specialize these rules but cannot weaken them.

## Authority Separation

- `control\source.md` decides what can be trusted as source.
- `CURRENT.md` owns the visible current workflow pointer and active surface pointer.
- `control\approval.md` separates approval request, user response, and bound approval scope.
- `control\permission.md` separates approved intent from allowed side effects.
- `control\proof.md` separates proof obligation, artifact check, and proof result.
- `control\lifecycle.md` separates progress notes from workflow state movement.
- `routing\manifest.md` provides route guidance only.
- `artifacts\registry.md` and `artifacts\log.md` provide lightweight observability only.
- `safety\regression.md` and `safety\improvement.md` provide boundary risk controls only.
- `release\transaction.md` keeps release and install work behind a separate transaction boundary.

No surface substitutes for another.

## Fail Closed

Fail closed when any required source, current pointer, approval scope, permission scope, proof obligation, lifecycle state, route, artifact status, safety boundary, improvement classification, or release boundary is missing, stale, conflicting, or outside scope.

Fail closed when a task asks for paths, commands, package metadata, npm wrapper metadata, release artifacts, dependency changes, git operations, secrets, external mutations, destructive actions, new files, or new folders outside the current exact approval and permission scope.

## Product Write Boundary

The current package, GitHub, and npm wrapper MVP surface contains the files named in `CURRENT.md` and `control\permission.md`.

Local writing is allowed only when the requested work unit is inside the bound approval scope, inside the permission side-effect ceiling, and tied to a current proof obligation and lifecycle entry.

Package metadata, local editable install verification, Windows/macOS npm wrapper metadata, npm dry-run pack verification, and GitHub repository push are allowed only when the current approval and permission surfaces explicitly name them.

Do not perform Python package registry publish, dependency installation from the network, secret access, unrelated external mutation, or destructive action outside generated verification artifacts. npm publish is allowed only for `harness-v2@0.1.0` when an active release transaction, approval surface, permission surface, and proof obligation all name that exact target and npm authentication is present.

## Guard Catalog

| guard | meaning |
| --- | --- |
| source guard | current source must name the target surface and be fresh for that scope |
| approval guard | exact user approval must match work unit, target surface, exclusions, and stale triggers |
| permission guard | side effects must stay inside the approved local ceiling |
| proof guard | artifact checks are evidence material until evaluated against a proof obligation |
| lifecycle guard | progress notes and current pointers do not become lifecycle movement by themselves |
| route guard | route guidance never grants tool, file, network, package, git, or release permission |
| artifact guard | registry rows and log entries are indexes, not source authority or proof |
| regression guard | mappings and scenarios do not equal passing regression evidence |
| improvement guard | improvement candidates do not directly change product rules |
| release guard | install, package, npm publish, Python package registry publish, deploy, and release readiness require a separate transaction |

## Current State

Use `CURRENT.md` for the active workflow pointer and next local action. If it conflicts with this file or any specialized surface, stop and reconcile before acting.
