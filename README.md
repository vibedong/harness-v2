# HARNESS V2

HARNESS V2 is a local workflow harness for AI-assisted software work. It keeps source, approval, permission, proof, lifecycle, routing, artifact, regression, improvement, and release boundaries visible and checkable.

Korean documentation is available in [README.ko.md](README.ko.md).

## Status

The current public release is `harness-v2@0.1.1` on npm.

This repository provides:

- product-local markdown controls for workflow boundaries;
- JSON contracts and reusable task templates;
- a standard-library Python CLI;
- dependency-free local package metadata and build backend;
- a Windows/macOS npm CLI wrapper that delegates to the Python CLI;
- fixture-backed unit tests for local task verification.

## Install

Install from npm:

```powershell
npm install -g harness-v2
```

Runtime prerequisites:

- Node.js 18 or newer.
- Python 3.11 or newer available on PATH.
- Windows or macOS for the npm wrapper in this release.

Confirm the installed CLI:

```powershell
harness-v2 status --root .
```

## CLI Usage

Show the current workflow pointer:

```powershell
harness-v2 status --root .
```

Verify a task contract:

```powershell
harness-v2 verify tests\fixtures\valid-task.json
```

Inspect project shape without mutating files:

```powershell
python -m harness_v2 doctor --root .
```

The npm command delegates to the Python CLI. It does not rewrite HARNESS V2 in JavaScript.

## How To Use The Harness

HARNESS V2 works best when each work unit has an explicit task contract:

1. Choose the current source and workflow pointer.
2. Record what the user approved.
3. Separate allowed side effects from denied side effects.
4. Name the proof obligations before claiming completion.
5. Keep lifecycle movement separate from progress notes.
6. Verify the task contract with `harness-v2 verify`.

The default fixture is a compact example:

```powershell
harness-v2 verify tests\fixtures\valid-task.json
```

If approval, permission, proof, lifecycle state, or workflow pointer conflicts, the verifier fails closed.

## Local Development Checks

From this repository:

```powershell
python -m compileall harness_v2
python -m unittest discover tests
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
npm pack --dry-run
```

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

## Repository Layout

| path | role |
| --- | --- |
| `AGENTS.md` | product-local agent entry router |
| `RULES.md` | product-local root rules |
| `CURRENT.md` | visible current workflow pointer |
| `README.ko.md` | Korean user manual |
| `LICENSE` | MIT license |
| `RELEASE_NOTES.md` | release notes |
| `package.json` | npm wrapper package manifest |
| `bin\harness-v2.js` | Windows/macOS Node CLI wrapper for the Python CLI |
| `control\` | source, approval, permission, proof, and lifecycle boundaries |
| `contracts\` | JSON contract files |
| `templates\` | task, gate, approval, and proof templates |
| `harness_v2\` | standard-library Python CLI and helpers |
| `_build_backend\` | dependency-free local PEP 517 build backend |
| `tests\` | unittest coverage and fixtures |
| `records\`, `routing\`, `artifacts\`, `safety\`, `release\` | local boundary and observability surfaces |

## Boundary Rule

README content is documentation only. It is not source authority, approval, permission, proof, lifecycle transition, route permission, regression pass, package readiness, release readiness, or product completion by itself.
