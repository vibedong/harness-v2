# HARNESS V2 Approval Control

status: package_github_surface / stale_backtrack_engine / approval_control

workflow: `remaining_completion_program`

This file separates approval request, user response, and bound approval scope.

## Current Bound Scope

Current bound work unit:

```text
goal_3_stale_backtrack_engine
```

Current active slice:

```text
stale_backtrack_engine / unreleased_local / no_release_transaction
```

Approval basis:

```text
User approved continuing the remaining work from F:\Folder\writingplans.md in Goal mode.
Goal 0, Goal 1, and Goal 2 are complete.
The active Goal is Goal 3: Stale / Backtrack Engine.
```

Purpose:

- detect stale source, approval, permission, proof, artifact, and transition evidence;
- emit explicit backtrack targets and reasons;
- add optional freshness map support without silently overwriting existing 0.1.7 projects;
- expose freshness status through verify and MCP verify output;
- keep stale evidence from being cleared by metadata-only edits;
- sync approval, permission, proof, lifecycle, artifact, and regression surfaces.

Allowed product write surface:

- `contracts\freshness.schema.json`
- `templates\freshness-map.json`
- `harness_v2\core.py`
- `harness_v2\cli.py`
- `harness_v2\freshness.py`
- `harness_v2\mcp.py`
- `tests\test_harness_v2.py`
- `tests\fixtures\invalid-stale-approval.json`
- `tests\fixtures\invalid-stale-proof.json`
- `control\approval.md`
- `control\permission.md`
- `control\proof.md`
- `control\lifecycle.md`
- `artifacts\registry.md`
- `artifacts\log.md`
- `safety\regression.md`

## Bound Local Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .`

## Bound Git/GitHub Commands

- `git add <intended Goal 3 product files>`
- `git commit`
- `git push`

Denied by the current approval scope:

- mutation outside `F:\Folder\harness-v2`;
- npm publish;
- Python package registry publish;
- GitHub release creation;
- release tag creation;
- git push outside the verified Goal 3 commit;
- dependency install from network;
- secret access;
- external network mutation outside the approved Goal 3 git push;
- remote MCP hosting;
- MCP client configuration mutation;
- Codex app configuration mutation or real hook installation;
- destructive operation outside generated temporary verification artifacts.

## Scope Fit

An action is inside approval scope only when it matches the work unit, target surface, operation type, exclusions, freshness anchors, and proof obligation.

If any part is wider, missing, or stale, approval does not fit and the workflow fails closed.

This file does not grant permission, produce proof, move lifecycle state, grant route permission, create regression pass, execute improvement, prepare release, or claim automatic enforcement completion.
