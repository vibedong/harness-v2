# HARNESS V2 Approval Control

status: package_github_surface / remaining_completion_program / approval_control

This file separates approval request, user response, and bound approval scope.

## Current Bound Scope

Previous bound work unit:

```text
detail_step_20_docs_control_sync_slice
```

Current bound work unit:

```text
remaining_completion_program
```

Current active slice:

```text
hook_equivalent_gate_hardening
```

Current bound user packet:

```text
Approve HARNESS V2 remaining completion program:
work only under F:\Folder\harness-v2.

Purpose:
finish HARNESS V2 for Codex-app-focused use by completing generated scaffold hardening,
executable 8-stage workflow engine enforcement, side-effect preflight adapter design and
implementation if locally feasible, optional MCP feasibility/design only unless separately
approved for implementation, final quality audit, documentation sync, and GitHub push.

Allow modifying product files under F:\Folder\harness-v2 needed for those goals.

Allow creating new files only when directly required for workflow engine enforcement,
lifecycle ledger/read-set/preflight implementation, generated scaffold templates,
tests/fixtures, Hook or equivalent local preflight adapter, or documentation needed to
explain those implemented surfaces.

Allow local verification:
python -m compileall harness_v2
python -m unittest discover tests
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
node bin\harness-v2.js init --root <temporary project>
python -m harness_v2 status --root <repo root>
python -m harness_v2 verify tests\fixtures\valid-task.json
python -m harness_v2 init --root <temporary project>
python -m harness_v2 verify <temporary project>\contracts\harness-task.json
npm pack --dry-run

Allow temporary verification folders under TEMP.
Allow cleaning only generated verification artifacts:
temporary TEMP folders,
__pycache__,
*.egg-info,
npm pack dry-run output.

Allow read-only subagent review with vowline at each major slice.
Subagents may not edit files, mutate git/network, grant approval, produce proof, or declare lifecycle transition.

Allow git add/commit/push to vibedong/harness-v2 after each completed slice if verification and review pass.

Do not perform npm publish.
Do not perform Python package registry publish.
Do not create GitHub release or release tag.
Do not install dependencies from network.
Do not read secrets.
Do not perform destructive operations outside generated temporary verification artifacts.
Do not mutate files outside F:\Folder\harness-v2.
Do not claim final HARNESS completion until final audit, tests, readback, and fresh-project scaffold verification pass.
```

Current Goal G continuation approval:

```text
User approved proceeding with the MCP, hook, and integration-hardening plan, starting with Goal G.
Goal G may evaluate and implement a local MCP adapter when feasible, as a thin wrapper over existing HARNESS V2 CLI/core surfaces.
This supersedes the prior MCP design-only boundary only for local stdio MCP adapter implementation. Hook work, integration hardening, package registry publish, release, dependency, secret, external mutation, and destructive work remain outside this slice.
```

Current Goal H continuation approval:

```text
User approved Goal H: Hook / Hook-Equivalent hardening under the remaining completion program.
Local evidence did not expose a direct Codex app pre-command or pre-write hook surface for this repo.
Goal H therefore implements an executable hook-equivalent gate over status, verify, and optional preflight checks, without mutating Codex app configuration or claiming shell/editor automatic blocking.
```

## Bound Local Verification Commands

These commands are bound for the current remaining completion program. The direct preflight smoke commands are included because the current program explicitly includes the side-effect preflight adapter and the latest user response approved DEF continuation under the existing denied-operation ceiling.

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js preflight tests\fixtures\valid-task.json --side-effect "python -m compileall harness_v2"`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root . --side-effect "python -m compileall harness_v2"`
- `node bin\harness-v2.js mcp < JSON-RPC smoke input`
- `node bin\harness-v2.js init --root <temporary project>`
- `python -m harness_v2 status --root <repo root>`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 preflight tests\fixtures\valid-task.json --side-effect "python -m unittest discover tests"`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root . --side-effect "python -m unittest discover tests"`
- `python -m harness_v2 mcp < JSON-RPC smoke input`
- `python -m harness_v2 init --root <temporary project>`
- `python -m harness_v2 verify <temporary project>\contracts\harness-task.json`
- `npm pack --dry-run`

Operation type:

- local product implementation, documentation, control-plane, test, scaffold, and verification work under `F:\Folder\harness-v2`;
- completed targets are generated scaffold hardening, executable 8-stage workflow engine enforcement, and side-effect preflight adapter work;
- current target is hook-equivalent gate hardening, documentation sync, final quality audit, and GitHub push;
- no npm publish, Python package registry publish, GitHub release, release tag, dependency install, secret access, or destructive operation outside generated temporary verification artifacts.

Freshness anchors:

- exact remaining completion program user packet;
- `CURRENT.md` remaining completion pointer;
- `control\permission.md` exact side-effect ceiling;
- `control\proof.md` final quality audit proof obligation;
- `control\lifecycle.md` remaining completion lifecycle boundary.

Denied by the current approval scope:

- mutation outside `F:\Folder\harness-v2`;
- files or new surfaces not directly required by the remaining completion program;
- npm publish;
- Python package registry publish;
- GitHub release creation;
- release tag creation;
- dependency install from network;
- secret access;
- external network mutation outside allowed git push;
- remote MCP hosting;
- MCP client configuration mutation;
- Codex app configuration mutation or real hook installation;
- destructive operation outside generated temporary verification artifacts.

## Scope Fit

An action is inside approval scope only when it matches the work unit, target surface, operation type, exclusions, freshness anchors, and proof obligation.

If any part is wider, missing, or stale, approval does not fit and the workflow fails closed.

This file does not grant permission, produce proof, move lifecycle state, grant route permission, create regression pass, execute improvement, prepare release, or claim automatic enforcement completion.
