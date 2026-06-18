# HARNESS V2 Proof Control

status: package_github_surface / remaining_completion_program / proof_control

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the side-effect preflight adapter slice, verify after authoring:

1. the CLI exposes `preflight`;
2. preflight validates the task contract before evaluating the proposed side effect or path;
3. explicitly allowed side effects pass;
4. denied, excluded, or unlisted side effects fail;
5. write-mode path checks require an exact `approval.approved_paths` match;
6. Node wrapper delegates `preflight` to the Python CLI;
7. README and README.ko explain preflight as a pre-execution contract check, not automatic shell-level blocking;
8. read-only subagent review findings are reflected or explicitly rejected before git push;
9. the approved local verification commands pass or blocked commands are reported as blocked.

## Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js preflight tests\fixtures\valid-task.json --side-effect "python -m compileall harness_v2"`
- `node bin\harness-v2.js init --root <temporary project>`
- `python -m harness_v2 status --root <repo root>`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 preflight tests\fixtures\valid-task.json --side-effect "python -m unittest discover tests"`
- `python -m harness_v2 init --root <temporary project>`
- `python -m harness_v2 verify <temporary project>\contracts\harness-task.json`
- `npm pack --dry-run`

## Artifact Checks

Readback, search, listing, diff output, temporary fresh-project verification, subagent findings, git status, and git push output are artifact checks for this slice. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Freshness

Proof evidence becomes stale when target files, write surface, approval scope, permission scope, proof obligation, lifecycle state, route guidance, GitHub target, npm target, release boundary, generated scaffold behavior, or automatic-enforcement wording changes.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, package registry publish state, release state, final completion, or future-slice authority.
