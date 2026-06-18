# HARNESS V2 Proof Control

status: package_github_surface / remaining_completion_program / proof_control

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the executable 8-stage workflow engine enforcement slice, verify after authoring:

1. task contracts require `workflow_stage`;
2. `workflow_stage` is limited to the eight executable stages in `rules\workflows.md`;
3. verifier rejects missing or unknown stages;
4. verifier accepts one coherent minimal contract for each stage;
5. verifier rejects representative stage rule violations for planning, approval, development, development review, artifact observation, routing, safety/improvement, and release boundary work;
6. generated initial task contracts declare a valid `workflow_stage` and still verify in a fresh temporary project;
7. current fixtures match the active remaining completion program workflow, stage, and denial boundaries;
8. read-only subagent review findings are reflected or explicitly rejected before git push;
9. the approved local verification commands pass or blocked commands are reported as blocked.

## Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js init --root <temporary project>`
- `python -m harness_v2 status --root <repo root>`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 init --root <temporary project>`
- `python -m harness_v2 verify <temporary project>\contracts\harness-task.json`
- `npm pack --dry-run`

## Artifact Checks

Readback, search, listing, diff output, temporary fresh-project verification, subagent findings, git status, and git push output are artifact checks for this slice. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Freshness

Proof evidence becomes stale when target files, write surface, approval scope, permission scope, proof obligation, lifecycle state, route guidance, GitHub target, npm target, release boundary, generated scaffold behavior, or automatic-enforcement wording changes.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, package registry publish state, release state, final completion, or future-slice authority.
