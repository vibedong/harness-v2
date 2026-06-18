# HARNESS V2

HARNESS V2 is a local workflow harness for AI-assisted software work. It keeps source, approval, permission, proof, lifecycle, routing, artifact, regression, improvement, and release boundaries visible and checkable.

## Status

Current build stage: public npm release candidate.

This repository currently provides:

- product-local markdown controls;
- minimal JSON contracts and templates;
- a standard-library Python CLI;
- dependency-free local package metadata and build backend;
- a dependency-free Windows/macOS npm CLI wrapper that delegates to the Python CLI;
- fixture-backed unit tests for local task verification.

The public npm release target is `harness-v2@0.1.0`. PyPI publish is not part of this release.

## Quick Start

Install from npm after publication:

```powershell
npm install -g harness-v2
harness-v2 status --root .
```

Runtime prerequisites:

- Node.js 18 or newer.
- Python 3.11 or newer available on PATH.
- Windows or macOS for the npm wrapper in this release.

From this repository:

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

Local npm wrapper smoke test before publication:

```powershell
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
npm pack --dry-run
```

The npm wrapper supports Windows and macOS for this release. It requires Node.js and Python 3.11 or newer on PATH, then delegates to the existing Python CLI without rewriting HARNESS V2 in JavaScript. The dry-run pack check does not publish to npm.

## Repository Layout

| path | role |
| --- | --- |
| `AGENTS.md` | product-local agent entry router |
| `RULES.md` | product-local root rules |
| `CURRENT.md` | visible current workflow pointer |
| `LICENSE` | MIT license |
| `RELEASE_NOTES.md` | public release notes |
| `package.json` | npm wrapper package manifest |
| `bin\harness-v2.js` | Windows/macOS Node CLI wrapper for the Python CLI |
| `control\` | source, approval, permission, proof, and lifecycle boundaries |
| `contracts\` | minimal JSON contract files |
| `templates\` | task, gate, approval, and proof templates |
| `harness_v2\` | local standard-library Python CLI and helpers |
| `_build_backend\` | dependency-free local PEP 517 build backend |
| `tests\` | unittest coverage and fixtures |
| `records\`, `routing\`, `artifacts\`, `safety\`, `release\` | local boundary and observability surfaces |

## Boundary Rule

README content is documentation only. It is not source authority, approval, permission, proof, lifecycle transition, route permission, regression pass, package readiness, release readiness, or product completion by itself.
