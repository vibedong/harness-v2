# HARNESS V2 Workflow Rules

status: package_github_surface / remaining_completion_program / workflow_rules

Workflow rules specialize `RULES.md`. They cannot weaken root rules or create approval, permission, proof, lifecycle state, routing authority, artifact authority, regression pass, improvement execution, or release state.

## Executable Stage IDs

Task contracts use `workflow_stage` for stage-specific verifier rules. The allowed values are the canonical HARNESS V2 task flow:

- `spec`
- `spec_review`
- `plan`
- `plan_review`
- `plan_approval`
- `development`
- `development_review`
- `improvement`

`workflow` remains the current program pointer from `CURRENT.md`; `workflow_stage` is the task-local rule stage.

Artifact observation, routing, safety/regression, and release boundaries are control surfaces. They are not `workflow_stage` values.

## Spec Workflow

Spec work captures the task goal, scope, current truth, unknowns, and completion criteria.

Spec work may update task-local stage records only. It cannot approve implementation, run product writes, grant permission, claim proof, or move lifecycle state.

Executable predicate: `spec` paths stay in `records\current-task.md`, `records\stages\spec.md`, or `records\decisions.md`; non-record side effects are denied.

## Spec Review Workflow

Spec review checks whether the task goal, scope, assumptions, and completion criteria are coherent enough to plan.

Spec review produces findings. Findings are not approval, permission, proof result, lifecycle state, route permission, or release readiness.

Executable predicate: `spec_review` paths stay in `records\stages\spec-review.md` or `records\decisions.md`; non-record side effects and lifecycle movement are denied.

## Plan Workflow

Plan work designs the work order, proof plan, permission boundaries, rollback/stale conditions, and handoff shape.

Plan work may update task-local stage records only. It cannot start product writes unless a later plan approval, permission, proof obligation, and lifecycle entry all name the same target surface.

Executable predicate: `plan` paths stay in `records\stages\plan.md` or `records\decisions.md`; non-record side effects are denied.

## Plan Review Workflow

Plan review checks the plan, proof obligation, permission boundary, execution order, and stale/backtrack rule.

Review findings must be resolved, deferred, or rejected before approval. Review cannot approve implementation by itself.

Executable predicate: `plan_review` paths stay in `records\stages\plan-review.md` or `records\decisions.md`; non-record side effects and lifecycle movement are denied.

## Plan Approval Workflow

Plan approval work binds a user response to a named scope.

Broad approval is input only until it is matched to an exact work unit, target surface, exclusions, stale triggers, and proof obligation.

Approval binding does not grant side effects. Side effects must pass `control\permission.md`.

Executable predicate: `plan_approval` paths stay in `control\approval.md`, `records\stages\plan-approval.md`, or `records\decisions.md`; an exact approval packet and excluded side effects are required.

## Development Workflow

Development work may write only the target surface named in `CURRENT.md`, bound by `control\approval.md`, and accepted by `control\permission.md`.

Development work must keep package metadata, release artifacts, dependencies, git, secrets, external mutations, destructive operations, and paths outside the exact packet out of scope unless the current exact packet opens that work.

Executable predicate: `development` requires concrete approved paths and an explicit local write side effect, while release execution side effects remain denied.

## Development Review Workflow

Development review inspects source, target, scope, permission, proof obligation, lifecycle state, route guidance, artifact observability, regression safety, improvement classification, and release boundary.

Review work produces findings and proof readback. Findings are not approval, permission, lifecycle state, route permission, regression pass, improvement execution, or release readiness.

Executable predicate: `development_review` paths stay in `records\stages\development-review.md`, `records\proof.md`, or `records\decisions.md`; non-record side effects, lifecycle movement, and authority claims are denied.

## Improvement Workflow

Improvement captures lessons, rejected/deferred candidates, follow-up risks, and HARNESS improvement candidates after review.

Improvement may update task-local records and safety/improvement notes. It does not directly edit rules, routes, code, tests, release surfaces, or product behavior without a new scoped workflow.

Executable predicate: `improvement` paths stay in `records\stages\improvement.md`, `records\decisions.md`, `records\handoff.md`, `safety\regression.md`, or `safety\improvement.md`; product implementation paths, non-record side effects, and release execution are denied.

## Control Surfaces

`artifacts\registry.md`, `artifacts\log.md`, `routing\manifest.md`, `safety\regression.md`, `safety\improvement.md`, and `release\transaction.md` remain control and observability surfaces. They can inform stages, but they do not become stages, approval, permission, proof, lifecycle transition, or release readiness.

## Root Precedence

When this file conflicts with `RULES.md`, `RULES.md` wins and the workflow fails closed.
