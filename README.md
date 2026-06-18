# HARNESS V2

HARNESS V2 is a local workflow harness for AI-assisted software work. It keeps source, approval, permission, proof, lifecycle, routing, artifact, regression, improvement, and release boundaries visible and checkable.

## Status

Current build stage: package and GitHub publish MVP.

This repository currently provides:

- product-local markdown controls;
- minimal JSON contracts and templates;
- a standard-library Python CLI;
- dependency-free local package metadata and build backend;
- fixture-backed unit tests for local task verification.

PyPI publish, release transaction execution, dependency installation, secret access, and destructive operations outside generated local verification artifacts are not part of this slice.

## Quick Start

From this directory:

```powershell
python -m compileall harness_v2
python -m unittest discover tests
```

The unittest suite covers the local CLI `status`, `verify`, and `doctor` behavior for this slice.

Editable package smoke test without dependency installation:

```powershell
$venv = Join-Path $env:TEMP "harness-v2-smoke-venv"
Remove-Item -Recurse -Force $venv -ErrorAction SilentlyContinue
python -m venv $venv
& (Join-Path $venv "Scripts\python.exe") -m pip install --no-deps -e .
& (Join-Path $venv "Scripts\python.exe") -m harness_v2 status --root .
& (Join-Path $venv "Scripts\python.exe") -m harness_v2 verify tests\fixtures\valid-task.json
Remove-Item -Recurse -Force $venv -ErrorAction SilentlyContinue
```

The package smoke test proves that the local package metadata can be consumed by pip in editable mode without dependency installation.

## Repository Layout

| path | role |
| --- | --- |
| `AGENTS.md` | product-local agent entry router |
| `RULES.md` | product-local root rules |
| `CURRENT.md` | visible current workflow pointer |
| `control\` | source, approval, permission, proof, and lifecycle boundaries |
| `contracts\` | minimal JSON contract files |
| `templates\` | task, gate, approval, and proof templates |
| `harness_v2\` | local standard-library Python CLI and helpers |
| `_build_backend\` | dependency-free local PEP 517 build backend |
| `tests\` | unittest coverage and fixtures |
| `records\`, `routing\`, `artifacts\`, `safety\`, `release\` | local boundary and observability surfaces |

## Boundary Rule

README content is documentation only. It is not source authority, approval, permission, proof, lifecycle transition, route permission, regression pass, package readiness, release readiness, or product completion by itself.
