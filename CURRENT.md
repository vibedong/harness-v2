# HARNESS V2 Current State

status: package_github_surface / remaining_completion_program / current_pointer

This file is the visible current pointer for the local HARNESS V2 product surface.

## Current Workflow

workflow: `remaining_completion_program`

state: `package_publish_review`

substate: `side_effect_preflight_adapter / not_final_completion`

source basis:

- Stage 00~05 confirmed planning artifacts.
- Product Implementation Entry Gate package/GitHub/npm-wrapper history.
- Published npm package state for `harness-v2@0.1.5`.
- User correction that `F:\Folder\harness-v2` is the completed product repository, not the user's downstream working project.
- User requirement that Codex-app users should install/apply HARNESS V2 into their project root, with README as user documentation and AI-facing rules in generated project-root files.
- Exact remaining completion program approval for generated scaffold hardening, executable workflow enforcement, side-effect preflight adapter work if locally feasible, MCP feasibility/design only unless separately approved, final audit, documentation sync, and GitHub push.

## Current Program

The remaining completion program is active but not complete.

Completed slices:

- generated scaffold hardening
- executable 8-stage workflow engine enforcement

Current active slice:

- side-effect preflight adapter

Future slices in this program:

- MCP feasibility/design only unless separately approved for implementation
- final quality audit, documentation sync, and GitHub push

## Current Surface

Active package, GitHub, npm wrapper, scaffold, workflow, preflight, and audit files may include:

- `.gitattributes`
- `.gitignore`
- `AGENTS.md`
- `RULES.md`
- `CURRENT.md`
- `README.md`
- `README.ko.md`
- `LICENSE`
- `RELEASE_NOTES.md`
- `package.json`
- `pyproject.toml`
- `_build_backend\harness_backend.py`
- `bin\harness-v2.js`
- `rules\workflows.md`
- `control\source.md`
- `control\approval.md`
- `control\permission.md`
- `control\proof.md`
- `control\lifecycle.md`
- `records\README.md`
- `routing\manifest.md`
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

New files are allowed only when directly required for workflow engine enforcement, lifecycle ledger/read-set/preflight implementation, generated scaffold templates, tests/fixtures, hook or equivalent local preflight adapter, or documentation needed to explain implemented surfaces.

## Current Allowed Local Verification Commands

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

## Current Allowed Git/GitHub Commands

- `git add <intended HARNESS V2 product files>`
- `git commit`
- `git push`

## Stop Conditions

Stop if a requested action needs files outside `F:\Folder\harness-v2`.

Stop if a requested action needs files or new surfaces not directly required by the active remaining completion program.

Stop if a pointer, source, approval, permission, proof obligation, lifecycle requirement, route, registry/log row, safety boundary, improvement classification, or release boundary is missing, stale, or conflicting.

Stop before npm publish, Python package registry publish, GitHub release creation, release tag creation, dependency installation from network, secret access, external network mutation outside allowed git push, or destructive operation outside generated temporary verification artifacts.

This file is a current pointer. It does not claim automatic enforcement completion, final HARNESS completion, public stable release readiness, Python package registry publish state, release execution, release tag state, or GitHub release state.
