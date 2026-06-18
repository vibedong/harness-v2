# HARNESS V2 Current State

status: package_github_surface / fourth_slice / current_pointer

This file is the visible current pointer for the local HARNESS V2 product surface.

## Current Workflow

workflow: `package_publish_review`

state: `package_publish_review`

substate: `fourth_slice_package_github_surface_authored / npm_wrapper_authored / public_patch_release_published / npm_published / github_release_created / npm_only / next_package_candidate`

source basis:

- Stage 00~05 confirmed planning artifacts.
- Product Implementation Entry Gate section 21 second-slice local markdown MVP result.
- Product Implementation Entry Gate section 22 third-slice executable MVP packet candidate.
- Product Implementation Entry Gate section 25 blocked threshold record superseded by the user's exact third-slice packet.
- Exact third-slice approval packet for the paths listed in `control\approval.md`.
- User request to package and publish to GitHub, constrained to `F:\Folder\harness-v2` only.
- Exact npm wrapper package slice approval for Windows/macOS Node wrapper packaging without npm publish.
- Historical public npm release workflow for `harness-v2@0.1.4`, now superseded for the current `0.1.5` package-candidate slice.
- User request that installing HARNESS V2 should lead directly to project application through `harness-v2 init --root .` / `harness-v2 apply --root .`.
- User request to strengthen the init-generated AI-facing scaffold and prepare everything up to, but not including, the next npm package publish.

## Current Surface

Active package, GitHub, and npm wrapper MVP files include:

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
- `contracts\task.schema.json`
- `contracts\approval.schema.json`
- `contracts\permission.schema.json`
- `contracts\proof.schema.json`
- `contracts\lifecycle.schema.json`
- `contracts\artifact.schema.json`
- `templates\task.json`
- `templates\gate-manifest.md`
- `templates\approval-request.md`
- `templates\proof-report.md`
- `harness_v2\__init__.py`
- `harness_v2\__main__.py`
- `harness_v2\cli.py`
- `harness_v2\core.py`
- `harness_v2\verify.py`
- `harness_v2\doctor.py`
- `tests\test_harness_v2.py`
- `tests\fixtures\valid-task.json`
- `tests\fixtures\invalid-missing-approval.json`

## Current Allowed Local Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m venv <temporary smoke-test venv under TEMP>`
- `<temporary venv>\Scripts\python -m pip install --no-deps -e .`
- `<temporary venv>\Scripts\python -m harness_v2 status --root <repo root>`
- `<temporary venv>\Scripts\python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 init --root <temporary project>`
- `python -m harness_v2 verify <temporary project>\contracts\harness-task.json`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js init --root <temporary project>`
- `npm pack --dry-run`
- `npm publish --dry-run`

These commands are proof material only for the current `0.1.5` package candidate. The temporary smoke-test venv is a generated verification artifact and is not part of the product source surface. `npm publish`, tag creation, and GitHub release execution require a separate release transaction. These checks do not create Python package registry publish readiness.

## Stop Conditions

Stop if the requested action needs a file outside the active executable local MVP file list.

Stop if a pointer, source, approval, permission, proof obligation, lifecycle requirement, route, registry/log row, safety boundary, improvement classification, or release boundary is missing, stale, or conflicting.

Stop if the task asks for npm publish, Python package registry publish, dependency installation, secret access, external network mutation outside the exact GitHub push command, release tag creation, GitHub release execution, or destructive operation outside generated local verification artifacts.

This file is a current pointer. The current pointer does not claim Python package registry publish, dogfood proof, or final product completion.
