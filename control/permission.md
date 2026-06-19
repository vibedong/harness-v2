# HARNESS V2 Permission Control

status: package_github_surface / stale_backtrack_engine / permission_control

workflow: `remaining_completion_program`

This file separates approved intent from allowed side effects.

## Side Effect Classes

| class | current stale/backtrack decision |
| --- | --- |
| local read | allowed under `F:\Folder\harness-v2` and generated TEMP verification folders |
| local file write | allowed under `F:\Folder\harness-v2` only for the exact Goal 3 stale/backtrack surface |
| new files | allowed only for Goal 3 freshness schema, freshness template, freshness module, and stale fixtures |
| local command execution | allowed only for the commands listed below |
| local MCP stdio adapter | allowed only as a dependency-free stdio JSON-RPC adapter over existing HARNESS V2 core functions |
| hook-equivalent gate | allowed only as an explicit local command that combines `status`, `verify`, and optional `preflight`; it is not a real shell/editor hook |
| temporary verification folders | allowed under TEMP |
| cleanup | allowed only for generated TEMP folders, `__pycache__`, and `*.egg-info` |
| read-only subagent review | allowed with `vowline`; subagents may not edit, mutate git/network, grant approval, produce proof, or declare lifecycle transition |
| git push | allowed only for the verified Goal 3 commit |
| npm publish | denied for this local slice |
| GitHub release or release tag | denied for this local slice |
| Python package registry publish | denied |
| dependency install from network, secret read, destructive action outside generated verification artifacts | denied |

## Exact Write Surface

Allowed write paths are product files under `F:\Folder\harness-v2` needed for Goal 3:

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

Any mutation outside `F:\Folder\harness-v2` fails closed except generated TEMP verification artifacts and their cleanup.

## Allowed Local Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .`

## Allowed Git/GitHub Commands

- `git add <intended Goal 3 product files>`
- `git commit`
- `git push`

## Permission Boundaries

Permission cannot widen approval scope and cannot produce proof, lifecycle state, route permission, regression pass, improvement execution, package registry publish readiness, release readiness, real hook installation, or automatic enforcement completion.

## Structured PermissionDecision Records

Goal 5 adds executable PermissionDecision records.

A PermissionDecision must reference active approval when side effects exist, classify the side-effect class, stay within the approval ceiling, and include preflight status for file, git, network, release, package, secret, or destructive side effects.

PermissionDecision records cannot approve side effects excluded by approval, cannot exceed the approval ceiling, cannot produce proof, and cannot move lifecycle state.

This permission surface allows git push only for the verified Goal 3 commit. It denies npm publish, Git tag creation, GitHub release creation, Python package registry publish, dependency installation from network, secret access, external network mutation outside the approved Goal 3 git push, remote MCP hosting, MCP client configuration mutation, Codex app configuration mutation, real shell/editor hook installation, and destructive action outside generated verification artifacts for the current stale/backtrack slice.
