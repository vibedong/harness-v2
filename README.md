# HARNESS V2

HARNESS V2 is a local control tool for AI-assisted development work. It applies a project-local harness scaffold, then records the task scope, approval, permissions, proof obligations, and lifecycle state before an AI coding agent starts changing files.

Use it with tools such as Codex, Claude Code, Cursor, or Copilot when you want the agent to stay inside an explicit task contract and report verifiable evidence before claiming completion.

Korean documentation is available in [README.ko.md](README.ko.md).

## What It Is

HARNESS V2 is not an AI model and it does not write code for you. It is a workflow harness that makes the working boundary visible and checkable.

Current implementation status: HARNESS V2 is a project scaffold, task-contract validator, and CLI helper. It makes boundaries explicit and checkable, but it is not a complete automatic enforcement or completion layer.

Before a task starts, you describe:

- the current source and workflow pointer;
- the user approval packet;
- the paths approved for the task;
- the side effects that are allowed or denied;
- the proof obligations required before completion;
- the lifecycle state the task is allowed to occupy.

The CLI can apply the initial scaffold with `harness-v2 init --root .`, then check whether a task contract is structurally valid and whether it conflicts with the current local HARNESS V2 state.

## Current Enforcement Boundary

The executable surface currently covers:

- project-root scaffold generation with `init` / `apply`;
- current pointer readback with `status`;
- task contract validation with `verify`;
- stage-specific workflow checks through `workflow_stage`;
- side-effect and write-path preflight checks with `preflight`;
- hook-equivalent gate checks with `gate`;
- local MCP stdio tool access with `mcp`.

HARNESS V2 ships a hook-equivalent gate command: `harness-v2 gate <task.json> --root .`. It combines `status`, `verify`, and optional `preflight` checks into one explicit boundary check. From local evidence for this repo, no direct Codex app hook surface was found, so the gate does not install a real Codex app hook and does not automatically block your shell or editor.

HARNESS V2 ships a local stdio MCP adapter that exposes `status`, `verify`, `preflight`, `gate`, `init`, and `apply` as MCP tools. The MCP adapter is a thin wrapper over the existing HARNESS V2 core and does not replace `CURRENT.md`, task contracts, approval, permission, proof, lifecycle, or release boundaries.

HARNESS V2 does not currently ship an HTTP MCP server, real editor hook, shell-level blocker, or Codex app configuration installer.

## When To Use It

HARNESS V2 is useful when:

- an AI agent will edit more than one file;
- the task has clear approval boundaries;
- some side effects must stay denied;
- completion must depend on test or verification output;
- long-running agent work needs a current workflow pointer;
- release, package, or repository operations must stay behind an explicit transaction boundary.

For a tiny typo fix in one file, HARNESS V2 may be more ceremony than you need.

## Problems It Reduces

| problem | how HARNESS V2 helps |
| --- | --- |
| the agent forgets the current task | `CURRENT.md` keeps the visible workflow pointer |
| scope and approval get mixed | `approval.approved_paths` records the approved path surface |
| risky commands are treated as normal work | `permission.allowed_side_effects` and `permission.denied_side_effects` separate side effects |
| completion is claimed without evidence | `proof.obligations` names the required checks |
| progress notes become lifecycle state | `lifecycle.current_state` and `lifecycle.target_state` stay explicit |
| package or release work expands accidentally | release and package actions require exact current scope |

HARNESS V2 reduces these risks by making the contract explicit. It does not automatically stop every editor, shell, or external tool.

## Install

Install the public npm package:

```powershell
npm install -g harness-v2
```

Runtime prerequisites:

- Node.js 18 or newer.
- Python 3.11 or newer available on PATH.
- Windows or macOS for the npm wrapper in this release.

The npm command delegates to the Python CLI. HARNESS V2 is not rewritten in JavaScript.

## What's New In 0.1.5

- `harness-v2 init --root .` now generates stronger AI-facing project files.
- Generated `AGENTS.md` says README files are user documentation, not AI operating authority.
- Generated `RULES.md`, `CURRENT.md`, and `control\` make source, approval, permission, proof, and lifecycle separation more explicit.
- Installed project files should appear directly in the target project root, not inside a nested `harness-v2` folder.
- Current GitHub source adds a hook-equivalent gate command for Codex-app-focused use without claiming real shell/editor blocking.

## Updating HARNESS V2

For the simplest path, ask your AI coding agent:

```text
하네스 업데이트해줘.
```

The agent should treat that request as:

1. Check the current project root and existing HARNESS files.
2. Update the global CLI with `npm install -g harness-v2@latest`.
3. Create a temporary fresh scaffold with the latest CLI and compare it with the project.
4. Update only HARNESS-managed surfaces that are safe to refresh, preserving project-specific `CURRENT.md`, approval, permission, proof, lifecycle, and active task state unless the user explicitly asks to reset them.
5. Do not create or leave a nested `harness-v2` folder inside the project.
6. Run `harness-v2 status --root .`, `harness-v2 verify contracts\harness-task.json`, and `harness-v2 gate contracts\harness-task.json --root .`.

Manual CLI update:

```powershell
npm install -g harness-v2@latest
harness-v2 status --root .
harness-v2 verify contracts\harness-task.json
harness-v2 gate contracts\harness-task.json --root .
```

This updates the global CLI only. It does not refresh project-local scaffold files or overwrite `CURRENT.md` / control state.

If a project needs the latest generated scaffold templates, have an AI agent compare the current project files against a fresh temporary scaffold before overwriting anything. Blind `--force` can replace project-local state.

Apply HARNESS V2 to a project:

```powershell
harness-v2 init --root .
```

`harness-v2 apply --root .` is an alias for the same operation. Existing files are not overwritten unless you pass `--force`.

HARNESS V2 applies files directly to the target project root. A normal project install should not leave a nested `harness-v2` folder inside the project. If the target is `F:\my-project`, the resulting files should be `F:\my-project\AGENTS.md`, `F:\my-project\RULES.md`, `F:\my-project\CURRENT.md`, `F:\my-project\control\`, `F:\my-project\contracts\`, and `F:\my-project\templates\`.

## 5-Minute Quick Start

The fastest first success is to apply HARNESS V2 to the current project and verify the initial task contract.

```powershell
npm install -g harness-v2
harness-v2 init --root .
harness-v2 status --root .
harness-v2 verify contracts\harness-task.json
harness-v2 gate contracts\harness-task.json --root .
```

Expected behavior:

- `init` creates `AGENTS.md`, `RULES.md`, `CURRENT.md`, `control\`, `contracts\harness-task.json`, and `templates\task.json`.
- `status` prints JSON from `CURRENT.md`.
- `verify` accepts the initial task contract and prints `{"ok": true, ...}`.
- `gate` accepts the initial task contract and prints a combined status/verify result.

The target folder itself receives the harness files. If a `harness-v2` child folder appears in your project, that folder is not the applied harness surface; run `harness-v2 init --root <project>` against the parent folder you actually want to use.

To start a new task contract, copy or adapt `templates\task.json` and fill in values that match your current `CURRENT.md`.

```json
{
  "task_id": "readme-docs-update",
  "title": "Update public README",
  "workflow": "package_publish_review",
  "source": {
    "basis": ["CURRENT.md", "control\\approval.md", "control\\permission.md"],
    "current_pointer": "CURRENT.md"
  },
  "approval": {
    "packet": "User approved README documentation update",
    "approved_paths": ["README.md", "README.ko.md"],
    "excluded_side_effects": ["package publish", "release execution"]
  },
  "permission": {
    "allowed_side_effects": ["local file writes to README.md and README.ko.md"],
    "denied_side_effects": ["package publish", "release execution", "dependency install from network"]
  },
  "proof": {
    "obligations": ["python -m unittest discover tests"]
  },
  "lifecycle": {
    "current_state": "package_publish_review",
    "target_state": "package_publish_review"
  }
}
```

Then verify the task file:

```powershell
harness-v2 verify <task.json>
```

The task `workflow` and `lifecycle.current_state` must match the current pointer in `CURRENT.md`.

## Basic Workflow

1. Choose the task goal and current source basis.
2. Record the exact user approval packet.
3. Put approved paths in `approval.approved_paths`.
4. Put allowed and denied side effects in `permission`.
5. Put required checks in `proof.obligations`.
6. Keep lifecycle movement separate from progress notes.
7. Run `harness-v2 verify <task.json>`.
8. Run `harness-v2 gate <task.json> --root .` before file changes or side-effectful commands.
9. Give the verified contract to your AI coding agent.
10. Before completion, check that the proof obligations were actually run and reported.

## Core Concepts

| term | meaning |
| --- | --- |
| task contract | JSON object that binds one work unit |
| `source.basis` | files or records the agent should treat as task basis |
| `source.current_pointer` | pointer to the current workflow state, normally `CURRENT.md` |
| `approval.packet` | exact approval text or approval reference |
| `approval.approved_paths` | paths approved for this task |
| `approval.excluded_side_effects` | actions excluded even if the task otherwise looks related |
| `permission.allowed_side_effects` | commands or effects the task may perform |
| `permission.denied_side_effects` | commands or effects the task must not perform |
| `proof.obligations` | checks required before completion is claimed |
| `lifecycle.current_state` | current lifecycle state expected by the task |
| `lifecycle.target_state` | lifecycle state the task is allowed to target |

The current executable contract vocabulary is defined by `contracts\*.schema.json` and `templates\task.json`.

## Common Commands

Show the current workflow pointer:

```powershell
harness-v2 status --root .
```

Apply HARNESS V2 to a project:

```powershell
harness-v2 init --root .
harness-v2 apply --root .
```

Verify a task contract:

```powershell
harness-v2 verify contracts\harness-task.json
```

Run the hook-equivalent gate before work:

```powershell
harness-v2 gate contracts\harness-task.json --root .
harness-v2 gate contracts\harness-task.json --root . --side-effect "python -m unittest discover tests"
```

`gate` does not execute the proposed command. It reads `CURRENT.md`, verifies the task contract, and runs optional `preflight` checks for proposed side effects or write paths. It is a hook-equivalent gate, not a real Codex app hook, shell blocker, or editor blocker.

Check a proposed side effect or write path before running it:

```powershell
harness-v2 preflight contracts\harness-task.json --side-effect "python -m unittest discover tests"
harness-v2 preflight contracts\harness-task.json --path README.md --mode write
```

`preflight` does not execute the command and does not automatically block your shell or editor. It checks the proposal against the task contract before you act.

Run the local MCP stdio adapter:

```powershell
harness-v2 mcp
```

The MCP adapter speaks newline-delimited JSON-RPC over stdio. It is meant to be launched by an MCP-capable client, not used as an interactive shell command. Exposed tools are `harness_status`, `harness_verify`, `harness_preflight`, `harness_gate`, `harness_init`, and `harness_apply`.

Inspect project shape without mutating files:

```powershell
python -m harness_v2 doctor --root .
```

For package verification, run the Node wrapper directly from the package source directory:

```powershell
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
```

## Prompt For AI Coding Agents

Use a prompt like this after you have a task contract:

```text
Work under HARNESS V2.

First read:
- CURRENT.md
- AGENTS.md
- RULES.md
- <task.json>

Rules:
- Scale read depth to the evidence needed, not to minimal reading at all costs. Read enough of the named source/control surfaces to bind scope, approval, permission, proof, and lifecycle; use targeted structural reads first, but read exact source text when authority, conflict, or stale-state decisions depend on wording.
- Treat approval.approved_paths as the approved write surface.
- Do not execute approval.excluded_side_effects.
- Do not execute permission.denied_side_effects.
- If the needed change is outside scope, stop and report it.
- Before claiming completion, run or report every proof.obligations item.
- In the final report, list changed files, verification commands, and pass/fail results.
```

This prompt is guidance for the agent. The current task contract and local control files remain the source for verification.

## Troubleshooting

### `harness-v2 status --root .` fails

Check that the root contains `CURRENT.md`. The `status` command reads the current pointer from that file.

If the project has not been initialized yet, run:

```powershell
harness-v2 init --root .
```

### The files appeared in the wrong place

Run `harness-v2 status --root <project>` against the folder you expected to receive the harness. The project root should contain `AGENTS.md`, `RULES.md`, `CURRENT.md`, `control\`, `contracts\`, and `templates\` directly. It should not require opening a nested `harness-v2` folder.

If the files are not directly under the intended project root, pass the target explicitly:

```powershell
harness-v2 init --root F:\path\to\your-project
```

### `harness-v2 verify <task.json>` fails

Common causes:

- a required object is missing: `source`, `approval`, `permission`, `proof`, or `lifecycle`;
- `workflow` does not match the workflow in `CURRENT.md`;
- `lifecycle.current_state` does not match the state in `CURRENT.md`;
- an allowed side effect conflicts with a denied side effect;
- a lifecycle state is not known in `control\lifecycle.md`;
- a control surface still contains a stale status marker.

### The agent needs a file outside `approval.approved_paths`

Stop the work and ask for a new approval packet or a narrower follow-up task. Do not silently widen the contract.

### A proof command fails

Report the failing command and separate existing failures from failures introduced by the task. Do not claim completion from a failed proof obligation.

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
| `contracts\harness-task.json` | initial project task contract created by `init` |
| `templates\task.json` | reusable task contract template created by `init` |
| `harness_v2\` | standard-library Python CLI and helpers |
| `_build_backend\` | dependency-free local PEP 517 build backend |
| `tests\` | unittest coverage and fixtures |
| `records\`, `routing\`, `artifacts\`, `safety\`, `release\` | local boundary and observability surfaces |

The npm package also ships its own schema and test fixtures for development, but a newly initialized user project starts with the smaller scaffold above.

## What HARNESS V2 Does Not Do

HARNESS V2 does not:

- write code by itself;
- decide requirements for the user;
- automatically block every external tool;
- turn install, init/apply, or CLI availability into automatic enforcement completion;
- run proof commands automatically;
- fix failing tests automatically;
- silently modify an arbitrary directory during `npm install -g`;
- publish packages or create releases without an exact, separate transaction scope;
- make README text into approval, permission, proof, lifecycle state, or release readiness.

## Recommended Practice

- Start with a small task contract.
- Keep `approval.approved_paths` narrow.
- Use evidence-scaled read depth: routine work can begin from `AGENTS.md`, `RULES.md`, `CURRENT.md`, and the active task contract; approval, permission, proof, lifecycle, stale state, release, external mutation, destructive action, or product implementation risk requires deeper source/control readback.
- Treat package metadata, dependency changes, secrets, deployment, and release actions as separate work.
- Keep proof obligations short enough to run, but strong enough to prove the task.
- Preserve failing proof output instead of rewriting it into a pass.
- Split documentation, code, package, and release work into separate task contracts when the side effects differ.

## Developer Verification

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

## Status

Install the current public package with `npm install -g harness-v2`. Use `npm view harness-v2 version` if you need to inspect the latest published npm version.

## Boundary Rule

README content is documentation only. It is not source authority, approval, permission, proof, lifecycle transition, route permission, regression pass, package readiness, release readiness, or product completion by itself.

## License

MIT. See [LICENSE](LICENSE).
