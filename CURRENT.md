# HARNESS V2 Current State

status: package_github_surface / fourth_slice / current_pointer

This file is the visible current pointer for the local HARNESS V2 product surface.

## Current Workflow

workflow: `package_publish_review`

state: `package_publish_review`

substate: `fourth_slice_package_github_surface_authored / local_package_smoke_required / not_pypi`

source basis:

- Stage 00~05 confirmed planning artifacts.
- Product Implementation Entry Gate section 21 second-slice local markdown MVP result.
- Product Implementation Entry Gate section 22 third-slice executable MVP packet candidate.
- Product Implementation Entry Gate section 25 blocked threshold record superseded by the user's exact third-slice packet.
- Exact third-slice approval packet for the paths listed in `control\approval.md`.
- User request to package and publish to GitHub, constrained to `F:\Folder\harness-v2` only.

## Current Surface

Active executable local MVP files include:

- `.gitignore`
- `AGENTS.md`
- `RULES.md`
- `CURRENT.md`
- `README.md`
- `pyproject.toml`
- `_build_backend\harness_backend.py`
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
- `<temporary venv>\Scripts\python -m harness_v2 status --root F:\Folder\harness-v2`
- `<temporary venv>\Scripts\python -m harness_v2 verify tests\fixtures\valid-task.json`

These commands are local proof material only. The temporary smoke-test venv is a generated verification artifact and is not part of the product source surface. These checks do not create PyPI publish readiness or release execution.

## Stop Conditions

Stop if the requested action needs a file outside the active executable local MVP file list.

Stop if a pointer, source, approval, permission, proof obligation, lifecycle requirement, route, registry/log row, safety boundary, improvement classification, or release boundary is missing, stale, or conflicting.

Stop if the task asks for PyPI publish, release execution, dependency installation, secret access, external network mutation outside GitHub repository creation/push, or destructive operation outside generated local verification artifacts.

This file is a current pointer. The current pointer does not claim PyPI publish, release execution, dogfood proof, or final product completion.
