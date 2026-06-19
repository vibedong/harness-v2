# HARNESS V2 Approval Control

status: package_github_surface / whole_plan_conformance_audit / approval_control

workflow: `remaining_completion_program`

This file separates approval request, user response, and bound approval scope.

## Current Bound Scope

Current bound work unit:

```text
goal_6_whole_plan_conformance_and_binding_surface_audit
```

Current active slice:

```text
whole_plan_conformance_audit / unreleased_local / no_release_transaction
```

Approval basis:

```text
User approved continuing the remaining work from F:\Folder\writingplans.md in Goal mode.
Goals 0 through 5 are complete.
The active Goal is Goal 6: Whole-plan Conformance And Binding Surface Audit.
```

Purpose:

- audit implemented HARNESS V2 against whole-plan and stage-plan source records;
- verify canonical stage identifiers and current gate ownership;
- verify CLI, npm wrapper, generated scaffold, and MCP wrapper behavior alignment;
- verify compatibility and fresh-project scaffold behavior through current local tests and command readback;
- classify the product honestly as `workflow_binding_engine`, `advisory_cli_validator`, or `blocked`;
- keep release, npm publish, Python package registry publish, tag, GitHub release, dependency, secret, external mutation, and destructive boundaries denied.

Allowed product write surface:

- `README.md`
- `README.ko.md`
- `CURRENT.md`
- `RELEASE_NOTES.md`
- `tests\test_harness_v2.py`
- `safety\regression.md`
- `safety\improvement.md`
- `release\transaction.md`
- `routing\manifest.md`
- `control\source.md`
- `control\approval.md`
- `control\permission.md`
- `control\proof.md`
- `control\lifecycle.md`

## Bound Local Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m harness_v2 status --root .`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root .`
- `python -m harness_v2 doctor --root .`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .`
- `node bin\harness-v2.js doctor --root .`
- `npm pack --dry-run`

## Bound Git/GitHub Commands

- `git add <intended Goal 6 product files>`
- `git commit`
- `git push`

Denied by the current approval scope:

- mutation outside `F:\Folder\harness-v2`;
- npm publish;
- Python package registry publish;
- GitHub release creation;
- release tag creation;
- git push outside the verified Goal 6 commit;
- dependency install from network;
- secret access;
- external network mutation outside the approved Goal 6 git push;
- remote MCP hosting;
- MCP client configuration mutation;
- Codex app configuration mutation or real hook installation;
- destructive operation outside generated temporary verification artifacts.

## Scope Fit

An action is inside approval scope only when it matches the work unit, target surface, operation type, exclusions, audit checks, and proof obligation.

If any part is wider, missing, or stale, approval does not fit and the workflow fails closed.

## Structured ApprovalDecision Records

ApprovalDecision records bind approval request, exact user response, exact edit paths, commands, side effects, git scope, release scope, exclusions, and current source refs.

Broad chat responses, review passes, metadata, package state, test success, and agent claims are not ApprovalDecision records.

An ApprovalDecision can bind approval scope, but it cannot grant permission, produce proof, move lifecycle state, or expand beyond the active task approval ceiling.

This file does not grant permission, produce proof, move lifecycle state, grant route permission, create regression pass, execute improvement, prepare release, publish a package, create a GitHub release, or claim automatic external enforcement.
