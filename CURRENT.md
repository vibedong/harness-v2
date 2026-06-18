# HARNESS V2 Current State

status: package_github_surface / remaining_completion_program / current_pointer

This file is the visible current pointer for the local HARNESS V2 product surface.

## Current Workflow

workflow: `remaining_completion_program`

state: `public_release_published`

substate: `github_source_release_v0.1.6 / npm_publish_deferred / release_closed`

source basis:

- Stage 00~05 confirmed planning artifacts.
- Product Implementation Entry Gate package/GitHub/npm-wrapper history.
- Prior published npm package state for `harness-v2@0.1.5`.
- Current GitHub source release target `v0.1.6`; npm publish is deferred.
- User correction that `F:\Folder\harness-v2` is the completed product repository, not the user's downstream working project.
- User requirement that Codex-app users should install/apply HARNESS V2 into their project root, with README as user documentation and AI-facing rules in generated project-root files.
- Exact remaining completion program approval for generated scaffold hardening, executable workflow enforcement, side-effect preflight adapter work if locally feasible, MCP feasibility/design only unless separately approved, final audit, documentation sync, and GitHub push.
- User approval to proceed with Goal G after the three-step MCP, hook, and integration hardening plan.
- Goal G approval supersedes the prior MCP design-only boundary only for local stdio MCP adapter implementation; hook work, integration hardening, package registry publish, release, dependency, secret, external mutation, and destructive work remain outside this slice.
- User approval to proceed with Goal H hook / hook-equivalent hardening under the remaining completion program.
- Local evidence did not expose a direct Codex app pre-command or pre-write hook surface for this repo, so Goal H implements an executable hook-equivalent gate instead of mutating Codex app configuration.
- User request to proceed with Goal I after Goal H, bound to integration hardening and release preparation without npm publish, Python registry publish, GitHub release, or release tag execution.
- User-approved public release and npm publish slice for `harness-v2@0.1.6`, including npm publish, Git tag `v0.1.6`, GitHub release creation, release docs/control sync, and the `pyproject.toml` version-consistency amendment.
- User cancellation of npm publish for this release path; `npm publish` is no longer part of the active transaction.

## Current Program

The remaining completion program is complete for the 0.1.6 GitHub source release transaction with npm publish deferred.

Completed slices:

- generated scaffold hardening
- executable 8-stage workflow engine enforcement
- side-effect preflight adapter
- MCP feasibility/design and final quality audit/docs-control sync
- MCP stdio adapter implementation
- hook-equivalent gate hardening
- integration hardening and release preparation
- GitHub source release `v0.1.6`

Current active slice:

- no active implementation slice; GitHub source release `v0.1.6` is closed after tag/release proof

Future slices in this program:

- npm publish, a later GitHub release/tag change, dependency installation, secret access, or destructive work require a later exact approval packet and release transaction after closeout

## Current Surface

Active package, GitHub, npm wrapper, scaffold, workflow, preflight, local MCP stdio adapter, and audit files may include:

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

New files are allowed only when directly required for workflow engine enforcement, lifecycle ledger/read-set/preflight implementation, generated scaffold templates, tests/fixtures, hook or equivalent local preflight adapter, local MCP stdio adapter implementation, or documentation needed to explain implemented surfaces.

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

## Current Allowed Git/GitHub Commands

- `git add <intended HARNESS V2 product files>`
- `git commit`
- `git push`
- `git push --tags`
- `gh release create v0.1.6 --repo vibedong/harness-v2 --title "HARNESS V2 0.1.6" --notes-file RELEASE_NOTES.md`

## Stop Conditions

Stop if a requested action needs files outside `F:\Folder\harness-v2`.

Stop if a requested action needs files or new surfaces not directly required by the active remaining completion program.

Stop if a pointer, source, approval, permission, proof obligation, lifecycle requirement, route, registry/log row, safety boundary, improvement classification, or release boundary is missing, stale, or conflicting.

Stop before npm publish, Python package registry publish, GitHub release or tag mutation outside the approved `v0.1.6` source release transaction, dependency installation from network, secret access, external network mutation outside allowed git push and the approved GitHub release transaction, or destructive operation outside generated temporary verification artifacts.

This file is a current pointer. It does not claim shell-level automatic enforcement, Python package registry publish state, future release authority, real Codex app hook installation, remote MCP hosting, MCP client installation, or MCP client configuration state.
