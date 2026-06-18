# HARNESS V2 Proof Control

status: package_github_surface / remaining_completion_program / proof_control

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the generated scaffold hardening slice, verify after authoring:

1. generated `AGENTS.md`, `RULES.md`, and `CURRENT.md` say HARNESS V2 is a scaffold, task-contract validator, and CLI helper, not automatic enforcement completion;
2. generated project-root files keep README as user documentation only, not source authority, approval, permission, proof, lifecycle, or release authority;
3. generated read order is evidence-scaled and expands to exact control text for approval, permission, proof, lifecycle, stale/conflict, release, external mutation, destructive action, or product implementation risk;
4. generated `contracts\harness-task.json` verifies in a fresh temporary project;
5. the generated scaffold is applied to the selected project root and not nested inside the installed package checkout when package-root redirection applies;
6. current fixtures match the active remaining completion program workflow and denial boundaries;
7. read-only subagent review findings are reflected or explicitly rejected before git push;
8. the approved local verification commands pass or blocked commands are reported as blocked.

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
