# HARNESS V2 Current State

status: package_github_surface / whole_plan_conformance_audit / current_pointer

This file is the visible current pointer for the local HARNESS V2 product surface.

## Current Workflow

workflow: `remaining_completion_program`

state: `workflow_realignment_review`

substate: `workflow_binding_engine_classified / unreleased_local / release_closed`

source basis:

- Stage 00~05 confirmed planning artifacts.
- Whole-plan and stage-plan records that define the canonical task flow as spec, spec review, plan, plan review, plan approval, development, development review, and improvement.
- Published npm/GitHub state `harness-v2@0.1.7` / `v0.1.7`, now treated as closed release history.
- User correction that workflow stages must follow the brainstorming/stage-plan flow and must not mix control surfaces into `workflow_stage`.
- User direction to use the recommended clean-break direction because the package is currently used mainly by the owner.

## Current Program

The local worktree is in a post-0.1.7 workflow engine completion and conformance audit slice.

Completed release history:

- generated scaffold hardening
- side-effect preflight adapter
- MCP stdio adapter implementation
- hook-equivalent gate hardening
- closed `harness-v2@0.1.7` npm package history reference
- closed `v0.1.7` GitHub release history reference

Current active slice:

- audit and preserve executable `workflow_stage` alignment to the canonical task flow:
  - `spec`
  - `spec_review`
  - `plan`
  - `plan_review`
  - `plan_approval`
  - `development`
  - `development_review`
  - `improvement`
- keep `workflow_stage` as the writable compatibility owner and derive `current_gate` from it unless a later explicit migration changes ownership;
- keep existing `0.1.7` task contracts compatible when they omit `current_gate`, `task_mode`, or `record_strength`, deriving `current_gate`, defaulting missing `task_mode` to `planned_change`, defaulting missing `record_strength` to `minimal`, and computing `effective_record_strength` from stage and task-mode rules;
- keep strict contracts failing with migration diagnostics if required Goal 0 fields are absent;
- remove `artifact_observation`, `routing`, `safety_improvement`, and `release_boundary` as workflow stages;
- keep artifact, routing, safety/regression, and release transaction as control surfaces;
- add generated task-local records scaffold under `records\`;
- verify locally without npm publish, GitHub release, release tag, dependency install, secret access, or destructive work.
- do not treat this local Goal 6 audit slice as a new npm publish, GitHub release, or release tag.
- classify the current explicit CLI/MCP/task-contract surface as `workflow_binding_engine`, not `advisory_cli_validator` or `blocked`, while preserving the boundary that HARNESS V2 is not an automatic shell/editor blocker or Codex app hook installer.

Future release path:

- npm publish, GitHub release/tag mutation, Python package registry publish, dependency installation, secret access, destructive work, or external mutation require a later exact approval packet and release transaction.

## Current Surface

Active package, npm wrapper, scaffold, workflow, preflight, local MCP stdio adapter, and audit files may include:

- `.gitattributes`
- `.gitignore`
- `AGENTS.md`
- `RULES.md`
- `CURRENT.md`
- `README.md`
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

Generated downstream project scaffold may include `records\current-task.md`, `records\stages\*.md`, `records\decisions.md`, `records\proof.md`, and `records\handoff.md`.

## Current Allowed Local Verification Commands

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

## Stop Conditions

Stop if a requested action needs files outside `F:\Folder\harness-v2`.

Stop if a requested action needs npm publish, Python package registry publish, GitHub release or tag mutation, git push, dependency installation from network, secret access, external network mutation, or destructive operation outside generated temporary verification artifacts.

Stop if a pointer, source, approval, permission, proof obligation, lifecycle requirement, route, registry/log row, safety boundary, improvement classification, or release boundary is missing, stale, or conflicting.

This file is a current pointer. It does not claim shell-level automatic enforcement, future release authority, real Codex app hook installation, remote MCP hosting, MCP client installation, or MCP client configuration state.
