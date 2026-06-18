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
github_source_release_v0.1.6 / npm_publish_deferred
```

Remaining completion program base packet:

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

Current Goal I continuation approval:

```text
User approved Goal I after Goal H.
Goal I is bound to integration hardening and release preparation under the remaining completion program.
It may harden read-only integration reporting and synchronize docs/control surfaces, but it does not authorize npm publish, Python registry publish, GitHub release, release tag creation, dependency installation, secret access, Codex app configuration mutation, real hook installation, or destructive work outside generated verification artifacts.

This Goal I boundary is superseded only by the later exact public release approval for `harness-v2@0.1.6`.
```

Current public release approval:

```text
Approve HARNESS V2 public release and npm publish slice:
work only under F:\Folder\harness-v2.

Purpose:
publish the current Goal H/I GitHub source state as a new public npm release,
including release readiness audit, version bump from 0.1.5 to 0.1.6 if needed,
release notes/update docs/control/release transaction sync, Git commit, Git tag,
GitHub release, and npm publish.

Allow modifying only release/package/control/doc/test files needed for this release:
package.json,
harness_v2\__init__.py,
README.md,
README.ko.md,
RELEASE_NOTES.md,
CURRENT.md,
control\approval.md,
control\permission.md,
control\proof.md,
control\lifecycle.md,
release\transaction.md,
tests\test_harness_v2.py,
tests\fixtures\valid-task.json.

Allow verification:
python -m compileall harness_v2
python -m unittest discover tests
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .
node bin\harness-v2.js doctor --root .
npm pack --dry-run
npm publish

Allow git/GitHub release operations:
git add/commit
git tag for v0.1.6
git push
git push --tags
GitHub release creation for vibedong/harness-v2 v0.1.6.
```

Current release amendment:

```text
Approve release slice amendment:
also allow modifying pyproject.toml under F:\Folder\harness-v2
for version consistency with package.json and harness_v2\__init__.py during the 0.1.6 npm/GitHub release.
```

Current npm publish cancellation:

```text
User cancelled npm publish for the current release path.
The active transaction keeps Git tag `v0.1.6`, GitHub release creation, release docs/control sync, and GitHub push.
`npm publish` is deferred and requires a later exact approval packet.
```

## Bound Local Verification Commands

These commands are bound for the current remaining completion program. The direct preflight smoke commands are included because the current program explicitly includes the side-effect preflight adapter and the latest user response approved DEF continuation under the existing denied-operation ceiling.

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

Operation type:

- local product implementation, documentation, control-plane, test, scaffold, and verification work under `F:\Folder\harness-v2`;
- completed targets are generated scaffold hardening, executable 8-stage workflow engine enforcement, and side-effect preflight adapter work;
- current target is the 0.1.6 GitHub source release transaction;
- Git tag `v0.1.6`, GitHub release creation, and git push are allowed only for this exact transaction;
- npm publish is deferred;
- no Python package registry publish, dependency install, secret access, or destructive operation outside generated temporary verification artifacts.

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
- additional GitHub release mutation after `v0.1.6` is created;
- additional release tag mutation after `v0.1.6` is created;
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
