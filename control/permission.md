# HARNESS V2 Permission Control

status: package_github_surface / remaining_completion_program / permission_control

This file separates approved intent from allowed side effects.

## Side Effect Classes

| class | remaining completion program decision |
| --- | --- |
| local read | allowed under `F:\Folder\harness-v2` and generated TEMP verification folders |
| local file write | allowed under `F:\Folder\harness-v2` only when directly required by the active remaining completion program |
| new files | allowed only for workflow engine enforcement, lifecycle ledger/read-set/preflight implementation, generated scaffold templates, tests/fixtures, hook or equivalent local preflight adapter, local MCP stdio adapter implementation, or documentation needed to explain implemented surfaces |
| local command execution | allowed only for the commands listed below |
| local MCP stdio adapter | allowed only as a dependency-free stdio JSON-RPC adapter over existing HARNESS V2 core functions |
| hook-equivalent gate | allowed only as an explicit local command that combines `status`, `verify`, and optional `preflight`; it is not a real shell/editor hook |
| integration doctor | allowed only as a read-only local report over current status, project shape, integrated surfaces, and closed release boundary |
| temporary verification folders | allowed under TEMP |
| cleanup | allowed only for generated TEMP folders, `__pycache__`, `*.egg-info`, and npm pack dry-run output |
| read-only subagent review | allowed with `vowline`; subagents may not edit, mutate git/network, grant approval, produce proof, or declare lifecycle transition |
| GitHub repository push | allowed after a completed slice passes verification and review |
| npm publish | allowed only for the exact `harness-v2@0.1.7` npm release transaction |
| GitHub release and release tag | allowed only for `vibedong/harness-v2` `v0.1.7` after release verification passes |
| Python package registry publish | denied |
| dependency install from network, secret read, destructive action outside generated verification artifacts | denied |

## Exact Write Surface

Allowed write paths are product files under `F:\Folder\harness-v2` needed for the remaining completion program, including:

- `AGENTS.md`
- `RULES.md`
- `CURRENT.md`
- `README.md`
- `README.ko.md`
- `routing\manifest.md`
- `control\source.md`
- `control\approval.md`
- `control\permission.md`
- `control\proof.md`
- `control\lifecycle.md`
- `rules\workflows.md`
- `records\README.md`
- `artifacts\registry.md`
- `artifacts\log.md`
- `safety\regression.md`
- `safety\improvement.md`
- `release\transaction.md`
- `contracts\*.schema.json`
- `templates\*.json`
- `templates\*.md`
- `harness_v2\*.py`
- `tests\*.py`
- `tests\fixtures\*.json`
- `package.json`
- `bin\harness-v2.js`
- `pyproject.toml`
- `_build_backend\harness_backend.py`
- `LICENSE`
- `RELEASE_NOTES.md`
- `.gitignore`
- `.gitattributes`

Any mutation outside `F:\Folder\harness-v2` fails closed except generated TEMP verification artifacts and their cleanup.

## Allowed Local Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js preflight tests\fixtures\valid-task.json --side-effect "python -m compileall harness_v2"`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root . --side-effect "python -m compileall harness_v2"`
- `node bin\harness-v2.js doctor --root .`
- `node bin\harness-v2.js mcp < JSON-RPC smoke input`
- `node bin\harness-v2.js init --root <temporary project>`
- `python -m harness_v2 status --root <repo root>`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 preflight tests\fixtures\valid-task.json --side-effect "python -m unittest discover tests"`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root . --side-effect "python -m unittest discover tests"`
- `python -m harness_v2 doctor --root <repo root>`
- `python -m harness_v2 mcp < JSON-RPC smoke input`
- `python -m harness_v2 init --root <temporary project>`
- `python -m harness_v2 verify <temporary project>\contracts\harness-task.json`
- `npm pack --dry-run`

## Allowed Git/GitHub Commands

- `git add <intended HARNESS V2 product files>`
- `git commit`
- `git push`
- `git push --tags`
- `gh release create v0.1.7 --repo vibedong/harness-v2 --title "HARNESS V2 0.1.7" --notes-file RELEASE_NOTES.md`

## Permission Boundaries

Permission cannot widen approval scope and cannot produce proof, lifecycle state, route permission, regression pass, improvement execution, package registry publish readiness, release readiness, real hook installation, or automatic enforcement completion.

This permission surface allows npm publish, Git tag creation, GitHub release creation, and external network mutation only for the exact approved `harness-v2@0.1.7` and `vibedong/harness-v2` `v0.1.7` release transaction. It denies repeat npm publish, Python package registry publish, additional GitHub release mutation, additional release tag mutation, dependency installation from network, secret access, external network mutation outside allowed git/GitHub release operations, remote MCP hosting, MCP client configuration mutation, Codex app configuration mutation, real shell/editor hook installation, and destructive action outside generated verification artifacts.
