# HARNESS V2 Current State

status: package_github_surface / detail_step_20_docs_control_sync / current_pointer

This file is the visible current pointer for the local HARNESS V2 product surface.

## Current Workflow

workflow: `package_publish_review`

state: `package_publish_review`

substate: `npm_0_1_5_published / detail_step_20_docs_control_sync / not_automatic_enforcement_completion`

source basis:

- Stage 00~05 confirmed planning artifacts.
- Product Implementation Entry Gate section 21 second-slice local markdown MVP result.
- Product Implementation Entry Gate section 22 third-slice executable MVP packet candidate.
- Product Implementation Entry Gate section 25 blocked threshold record superseded by the user's exact third-slice packet.
- Exact third-slice approval packet for the paths listed in `control\approval.md`.
- User request to package and publish to GitHub, constrained to `F:\Folder\harness-v2` only.
- Exact npm wrapper package slice approval for Windows/macOS Node wrapper packaging without npm publish.
- Historical public npm release workflow for `harness-v2@0.1.4`, now superseded by the published `harness-v2@0.1.5` npm state.
- User request that installing HARNESS V2 should lead directly to project application through `harness-v2 init --root .` / `harness-v2 apply --root .`.
- User request to strengthen the init-generated AI-facing scaffold before the `0.1.5` package publish.
- User request to proceed with npm publish for `harness-v2@0.1.5`, now completed historically.
- Exact detail step 20 docs/control sync approval for stale wording, proof/permission dry-run mismatch, automatic-enforcement wording, and evidence-scaled readback guidance.

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

## Current Allowed Verification And Git Commands

For the detail step 20 docs/control sync slice:

- local file readback, listing, and search commands scoped to this repository;
- `git status --short`;
- `git diff -- <intended docs/control files>`;
- read-only subagent review with `vowline`;
- `git add`, `git commit`, and `git push` only for this docs/control sync slice after review passes.

Historical package, npm wrapper, npm publish dry-run, and npm registry readback commands are evidence material for prior package slices. They are not current permission for package build, npm publish dry-run, repeat npm publish, release execution, dependency installation, hook work, or MCP work.

## Stop Conditions

Stop if the requested action needs a file outside the detail step 20 approved docs/control sync file list.

Stop if a pointer, source, approval, permission, proof obligation, lifecycle requirement, route, registry/log row, safety boundary, improvement classification, or release boundary is missing, stale, or conflicting.

Stop if the task asks for package build, npm publish dry-run, npm publish, Python package registry publish, dependency installation, secret access, external network mutation outside the allowed git push, release tag creation, GitHub release execution, hook work, MCP work, or destructive operation.

This file is a current pointer. The current pointer does not claim automatic enforcement completion, Python package registry publish, dogfood proof, release readiness, or final product completion.
