# HARNESS V2 Approval Control

status: package_github_surface / remaining_completion_program / approval_control

This file separates approval request, user response, and bound approval scope.

## Current Bound Scope

Previous bound work unit:

```text
detail_step_20_docs_control_sync_slice
```

Current bound work unit:

```text
remaining_completion_program
```

Current active slice:

```text
side_effect_preflight_adapter
```

Current bound user packet:

```text
Approve HARNESS V2 remaining completion program:
work only under F:\Folder\harness-v2.

Purpose:
finish HARNESS V2 for Codex-app-focused use by completing generated scaffold hardening,
executable 8-stage workflow engine enforcement, side-effect preflight adapter design and
implementation if locally feasible, optional MCP feasibility/design only unless separately
approved for implementation, final quality audit, documentation sync, and GitHub push.

Allow modifying product files under F:\Folder\harness-v2 needed for those goals.

Allow creating new files only when directly required for workflow engine enforcement,
lifecycle ledger/read-set/preflight implementation, generated scaffold templates,
tests/fixtures, Hook or equivalent local preflight adapter, or documentation needed to
explain those implemented surfaces.

Allow local verification:
python -m compileall harness_v2
python -m unittest discover tests
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
node bin\harness-v2.js init --root <temporary project>
python -m harness_v2 status --root <repo root>
python -m harness_v2 verify tests\fixtures\valid-task.json
python -m harness_v2 init --root <temporary project>
python -m harness_v2 verify <temporary project>\contracts\harness-task.json
npm pack --dry-run

Allow temporary verification folders under TEMP.
Allow cleaning only generated verification artifacts:
temporary TEMP folders,
__pycache__,
*.egg-info,
npm pack dry-run output.

Allow read-only subagent review with vowline at each major slice.
Subagents may not edit files, mutate git/network, grant approval, produce proof, or declare lifecycle transition.

Allow git add/commit/push to vibedong/harness-v2 after each completed slice if verification and review pass.

Do not perform npm publish.
Do not perform Python package registry publish.
Do not create GitHub release or release tag.
Do not install dependencies from network.
Do not read secrets.
Do not perform destructive operations outside generated temporary verification artifacts.
Do not mutate files outside F:\Folder\harness-v2.
Do not claim final HARNESS completion until final audit, tests, readback, and fresh-project scaffold verification pass.
```

Operation type:

- local product implementation, documentation, control-plane, test, scaffold, and verification work under `F:\Folder\harness-v2`;
- first active target is generated scaffold hardening;
- later targets are executable 8-stage workflow engine enforcement, side-effect preflight adapter work if locally feasible, MCP feasibility/design only unless separately approved, final quality audit, documentation sync, and GitHub push;
- no npm publish, Python package registry publish, GitHub release, release tag, dependency install, secret access, or destructive operation outside generated temporary verification artifacts.

Freshness anchors:

- exact remaining completion program user packet;
- `CURRENT.md` remaining completion pointer;
- `control\permission.md` exact side-effect ceiling;
- `control\proof.md` generated scaffold hardening proof obligation;
- `control\lifecycle.md` remaining completion lifecycle boundary.

Denied by the current approval scope:

- mutation outside `F:\Folder\harness-v2`;
- files or new surfaces not directly required by the remaining completion program;
- npm publish;
- Python package registry publish;
- GitHub release creation;
- release tag creation;
- dependency install from network;
- secret access;
- external network mutation outside allowed git push;
- destructive operation outside generated temporary verification artifacts.

## Scope Fit

An action is inside approval scope only when it matches the work unit, target surface, operation type, exclusions, freshness anchors, and proof obligation.

If any part is wider, missing, or stale, approval does not fit and the workflow fails closed.

This file does not grant permission, produce proof, move lifecycle state, grant route permission, create regression pass, execute improvement, prepare release, or claim automatic enforcement completion.
