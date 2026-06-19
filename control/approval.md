# HARNESS V2 Approval Control

status: package_github_surface / transition_ledger_lifecycle_guard / approval_control

workflow: `remaining_completion_program`

This file separates approval request, user response, and bound approval scope.

## Current Bound Scope

Current bound work unit:

```text
goal_2_transition_ledger_lifecycle_guard
```

Current active slice:

```text
transition_ledger_lifecycle_guard / unreleased_local / no_release_transaction
```

Approval basis:

```text
User approved continuing the remaining work from F:\Folder\writingplans.md in Goal mode.
Goal 0 and Goal 1 are complete.
The active Goal is Goal 2: Transition Ledger And Lifecycle Guard.
```

Purpose:

- implement transition ledger parsing and lifecycle transition evaluation;
- make lifecycle movement an evaluated operation, not a log line;
- keep `workflow_stage` as the compatibility owner and `current_gate` / `records\gate-state.json` as derived read-models;
- require transition records to bind `from_gate`, `to_gate`, source refs, freshness refs, approval, permission, proof, stale check, reason, and actor;
- require `plan_approval -> development` to have active approval and permission references;
- require `development_review -> improvement` to have proof evidence;
- reject legacy stage aliases, stale transition evidence, invalid route edges, and same-task `improvement -> spec`;
- sync lifecycle, approval, permission, proof, workflow, and routing control surfaces;
- verify locally.

Allowed product write surface:

- `contracts\transition.schema.json`
- `templates\transition-log.md`
- `harness_v2\core.py`
- `harness_v2\cli.py`
- `harness_v2\lifecycle.py`
- `harness_v2\mcp.py`
- `tests\test_harness_v2.py`
- `tests\fixtures\valid-transition-log.md`
- `tests\fixtures\invalid-transition-stale-approval.md`
- `control\lifecycle.md`
- `control\approval.md`
- `control\permission.md`
- `control\proof.md`
- `rules\workflows.md`
- `routing\manifest.md`

## Bound Local Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root .`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .`

## Bound Git/GitHub Commands

- `git add <intended Goal 2 product files>`
- `git commit`
- `git push`

Denied by the current approval scope:

- mutation outside `F:\Folder\harness-v2`;
- npm publish;
- Python package registry publish;
- GitHub release creation;
- release tag creation;
- git push outside the verified Goal 2 commit;
- dependency install from network;
- secret access;
- external network mutation outside the approved Goal 2 git push;
- remote MCP hosting;
- MCP client configuration mutation;
- Codex app configuration mutation or real hook installation;
- destructive operation outside generated temporary verification artifacts.

## Scope Fit

An action is inside approval scope only when it matches the work unit, target surface, operation type, exclusions, freshness anchors, and proof obligation.

If any part is wider, missing, or stale, approval does not fit and the workflow fails closed.

This file does not grant permission, produce proof, move lifecycle state, grant route permission, create regression pass, execute improvement, prepare release, or claim automatic enforcement completion.
