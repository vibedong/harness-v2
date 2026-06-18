# HARNESS V2 Proof Control

status: package_github_surface / detail_step_20_docs_control_sync / proof_control

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the detail step 20 docs/control sync slice, verify after authoring:

1. all changed files are inside the eleven-file approved docs/control surface;
2. no code, tests, schemas, fixtures, package metadata, hook, MCP, release artifact, dependency, secret, or destructive surface changed;
3. no current release boundary says exact npm publish is for `harness-v2@0.1.4`;
4. `0.1.5` wording is consistent with the already-published npm package state and does not imply repeat npm publish authority;
5. current proof obligations do not require `npm publish --dry-run` when current permission denies package and publish work;
6. product docs say HARNESS V2 is currently a scaffold, task-contract validator, and CLI helper, not automatic enforcement completion;
7. Codex app guidance uses evidence-scaled readback rather than minimal reading at all costs;
8. local readback/search output supports the changed wording;
9. read-only subagent review findings are reflected or explicitly rejected before git push.

## Artifact Checks

Readback, search, listing, diff output, subagent findings, git status, and git push output are artifact checks for this slice. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Freshness

Proof evidence becomes stale when target files, write surface, approval scope, permission scope, proof obligation, lifecycle state, route guidance, GitHub target, npm target, release boundary, or automatic-enforcement wording changes.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, Python package registry publish state, release state, or future-slice authority.
