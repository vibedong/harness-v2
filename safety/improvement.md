# HARNESS V2 Improvement Safety

status: package_github_surface / fourth_slice / improvement_safety

This file classifies improvement observations without directly changing product rules.

## Improvement Classes

| class | meaning | next handling |
| --- | --- | --- |
| observation | a noticed friction, risk, or unclear boundary | collect evidence before action |
| candidate | a supported improvement idea | route to a scoped workflow |
| rejected | a considered idea that conflicts with current rules or goals | keep rationale concise |
| deferred | a useful idea outside current permission or lifecycle state | wait for future scope |
| unknown | an ambiguous signal with insufficient evidence | gather source before deciding |

## Intake Requirements

An improvement candidate must name:

- observed issue or opportunity;
- source evidence;
- affected surface;
- boundary touched;
- expected benefit;
- stale or rollback trigger;
- required approval and permission for any actual change.

## Direct-Change Guard

Improvement records do not directly edit `AGENTS.md`, `RULES.md`, workflow rules, control files, routing, artifacts, safety files, release files, code, tests, schemas, fixtures, runners, packages, dependencies, git, secrets, external systems, or destructive targets.

## Non-Authority Boundary

This file does not create backlog authority, approval, permission, proof, lifecycle transition, route permission, regression pass, implementation completion, package readiness, or release readiness.
