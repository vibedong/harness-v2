# HARNESS V2 Root Rules

status: package_github_surface / detail_step_20_docs_control_sync / root_rules

These are the product-local root rules for the HARNESS V2 package, GitHub, and npm wrapper MVP surface. Workflow rules in `rules\workflows.md` may specialize these rules but cannot weaken them.

Current HARNESS V2 is a scaffold, task-contract validator, and CLI helper. It makes boundaries visible and checkable, but it is not an automatic editor/shell/network sandbox and it does not complete approval, permission, proof, lifecycle, package, or release work by installation alone.

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

## Evidence-Scaled Readback

Routine current-task work may start with `AGENTS.md`, this file, `CURRENT.md`, and the active task contract or current control surface named by the request.

Expand the readback when the task involves approval, permission, proof, lifecycle movement, stale state, product implementation, package/release work, external mutation, destructive action, secrets, git publishing, or any conflicting pointer. Extra reading must produce better evidence for the decision; it is not a substitute for approval, permission, proof, or lifecycle authority.

## Product Write Boundary

The current package, GitHub, and npm wrapper MVP surface contains the files named in `CURRENT.md` and `control\permission.md`.

Local writing is allowed only when the requested work unit is inside the bound approval scope, inside the permission side-effect ceiling, and tied to a current proof obligation and lifecycle entry.

Package metadata, local editable install verification, Windows/macOS npm wrapper metadata, npm dry-run pack verification, npm publish dry-run verification, npm registry readback, and GitHub repository push are allowed only when the current approval and permission surfaces explicitly name them. The current docs/control sync slice does not authorize package build, npm publish, release execution, dependency installation, hook work, or MCP work.

Do not perform npm publish, Python package registry publish, dependency installation from the network, secret access, release tag creation, GitHub release execution, unrelated external mutation, or destructive action outside generated verification artifacts unless a separate active release transaction, approval surface, permission surface, and proof obligation all name that exact target.

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
