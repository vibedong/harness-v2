# HARNESS V2 Workflow Rules

status: package_github_surface / fourth_slice / workflow_rules

Workflow rules specialize `RULES.md`. They cannot weaken root rules or create approval, permission, proof, lifecycle state, routing authority, artifact authority, regression pass, improvement execution, or release state.

## Planning Workflow

Planning work may read planning records and produce candidate documents.

Planning work must label drafts, candidates, deferred items, active decisions, and implementation boundaries separately.

Planning work cannot start product writes unless approval, permission, proof obligation, and lifecycle entry all name the same target surface.

## Approval Workflow

Approval work binds a user response to a named scope.

Broad approval is input only until it is matched to an exact work unit, target surface, exclusions, stale triggers, and proof obligation.

Approval binding does not grant side effects. Side effects must pass `control\permission.md`.

## Development Workflow

Development work may write only the target surface named in `CURRENT.md`, bound by `control\approval.md`, and accepted by `control\permission.md`.

Development work must keep package metadata, release artifacts, dependencies, git, secrets, external mutations, destructive operations, and paths outside the exact packet out of scope unless the current exact packet opens that work.

## Development Review Workflow

Review work may inspect source, target, scope, permission, proof obligation, lifecycle state, route guidance, artifact observability, regression safety, improvement classification, and release boundary.

Review work produces findings. Findings are not approval, permission, proof result, lifecycle state, route permission, regression pass, improvement execution, or release readiness.

## Artifact Observation Workflow

Artifact work may maintain lightweight rows and provenance notes for gate-relevant local markdown artifacts.

Artifact work must not turn registry rows, log entries, file existence, headings, summaries, or subagent reports into source authority or proof.

## Routing Workflow

Routing work may choose a suggested skill, agent role, or review lane based on operation mode and side-effect class.

Routing work must stop before any side effect that lacks approval and permission.

## Safety And Improvement Workflow

Safety work may map boundary risks, misuse scenarios, stale triggers, and regression guard candidates.

Improvement work may classify candidate changes and lessons. It does not directly edit rules, routes, code, tests, release surfaces, or product behavior without a new scoped workflow.

## Release Boundary Workflow

Release work is boundary analysis only in this package and GitHub MVP surface.

Python package registry publish, deploy, release readiness, rollback execution, and unrelated external mutation require a later release transaction scope.

## Root Precedence

When this file conflicts with `RULES.md`, `RULES.md` wins and the workflow fails closed.
