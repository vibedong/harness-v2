# HARNESS V2 Product Entry

status: package_github_surface / detail_step_20_docs_control_sync / entry_router

This file is the product-local entry router for HARNESS V2. Keep it short and use it only to find the current authority surface.

Current HARNESS V2 is a project scaffold, task-contract validator, and CLI helper. It is not an automatic enforcement sandbox and it does not complete workflow transitions by itself.

## Read Order

1. `RULES.md`
2. `CURRENT.md`
3. `rules\workflows.md` when the requested action names a workflow.
4. The relevant file under `control\`, `records\`, `routing\`, `artifacts\`, `safety\`, or `release\`.

Do not expand beyond the current package and GitHub MVP surface unless a later exact approval packet, permission preflight, proof obligation, and lifecycle entry name that wider work.

Use evidence-scaled readback. Routine current-task work can start from the short read order, but approval, permission, proof, lifecycle, stale state, release, external mutation, destructive action, or product implementation risk requires deeper source/control readback before acting.

## Recovery Rule

After context compression, resume, handoff, or goal continuation:

1. Read this file.
2. Read `RULES.md`.
3. Read `CURRENT.md`.
4. Read only the workflow and surface files required by the requested action.
5. Stop if source, approval, permission, proof, lifecycle, route, artifact, safety, improvement, or release state is missing, stale, conflicting, or outside scope.

## Current Stop Rule

If the task asks for product writes, first verify the requested target is inside the current write surface in `CURRENT.md`, the bound approval scope in `control\approval.md`, and the side-effect ceiling in `control\permission.md`.

If the task asks for proof or completion, first verify the proof obligation in `control\proof.md`.

If the task asks to move workflow state, first verify transition requirements in `control\lifecycle.md`.

If the task asks for routing, artifact indexing, regression safety, improvement intake, or release work, read the matching local surface and keep its non-authority boundary intact.

## Forbidden Now

- Do not treat approval text as permission.
- Do not treat permission as proof.
- Do not treat proof material as lifecycle state.
- Do not treat route guidance as side-effect permission.
- Do not treat registry rows or log entries as source authority or proof.
- Do not treat regression mapping as a regression pass.
- Do not treat improvement candidates as product changes.
- Do not treat release transaction boundaries as release readiness.
- Do not treat install, init/apply, or CLI availability as automatic enforcement completion.
- Do not add files, code, tests, schemas, fixtures, runners, packages, release artifacts, dependencies, git operations, secrets, external mutations, or destructive actions beyond the currently bound approval and permission scope.
