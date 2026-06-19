# HARNESS V2 Permission Control

status: package_github_surface / whole_plan_conformance_audit / permission_control

workflow: `remaining_completion_program`

This file separates approved intent from allowed side effects.

## Side Effect Classes

| class | current Goal 6 decision |
| --- | --- |
| local read | allowed under `F:\Folder\harness-v2` and generated TEMP verification folders |
| local file write | allowed under `F:\Folder\harness-v2` only for the exact Goal 6 docs/control/test audit surface |
| new files | denied for this slice |
| local command execution | allowed only for the commands listed below |
| local MCP stdio adapter | readback only through existing CLI/MCP surfaces; no remote hosting or client configuration mutation |
| hook-equivalent gate | allowed only as an explicit local command that combines `status`, `verify`, and optional `preflight`; it is not a real shell/editor hook |
| temporary verification folders | allowed under TEMP only when created by approved verification commands or tests |
| cleanup | allowed only for generated TEMP folders, `__pycache__`, and `*.egg-info` |
| read-only subagent review | allowed with `vowline`; subagents may not edit, mutate git/network, grant approval, produce proof, or declare lifecycle transition |
| git push | allowed only for the verified Goal 6 commit |
| npm publish | denied for this local slice |
| GitHub release or release tag | denied for this local slice |
| Python package registry publish | denied |
| dependency install from network, secret read, destructive action outside generated verification artifacts | denied |

## Exact Write Surface

Allowed write paths are product files under `F:\Folder\harness-v2` needed for Goal 6:

- `README.md`
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

Any mutation outside `F:\Folder\harness-v2` fails closed except generated TEMP verification artifacts and their cleanup.

## Allowed Local Commands

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

## Allowed Git/GitHub Commands

- `git add <intended Goal 6 product files>`
- `git commit`
- `git push`

## Permission Boundaries

Permission cannot widen approval scope and cannot produce proof, lifecycle state, route permission, regression pass, improvement execution, package registry publish readiness, release readiness, real hook installation, or automatic external enforcement.

## Structured PermissionDecision Records

PermissionDecision records must reference active approval when side effects exist, classify the side-effect class, stay within the approval ceiling, and include preflight status for file, git, network, release, package, secret, or destructive side effects.

PermissionDecision records cannot approve side effects excluded by approval, cannot exceed the approval ceiling, cannot produce proof, and cannot move lifecycle state.

This permission surface allows git push only for the verified Goal 6 commit. It denies npm publish, Git tag creation, GitHub release creation, Python package registry publish, dependency installation from network, secret access, external network mutation outside the approved Goal 6 git push, remote MCP hosting, MCP client configuration mutation, Codex app configuration mutation, real shell/editor hook installation, and destructive action outside generated verification artifacts for the current audit slice.
