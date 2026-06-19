# HARNESS V2 Release Notes

## HARNESS V2 0.1.8 Release Notes

npm release notes for the Korean public README release.

## Changed

- Publishes the current source package metadata as `0.1.8`.
- Uses a single Korean `README.md` for GitHub and npm users.
- Removes the separate `README.ko.md` package surface.
- Keeps README as user-facing product documentation, not AI operating authority.
- Preserves the `workflow_binding_engine` classification and explicit CLI/MCP/task-contract boundary wording.
- Preserves the canonical workflow stages: `spec`, `spec_review`, `plan`, `plan_review`, `plan_approval`, `development`, `development_review`, `improvement`.
- Keeps `harness-v2 init --root .` and `harness-v2 apply --root .` focused on project-root files, not a nested `harness-v2` folder.
- Keeps the hook-equivalent `gate` command, local stdio MCP adapter, `harness_decision`, and read-only `doctor` report.

## Runtime Requirements

- Node.js 18 or newer.
- Python 3.11 or newer on PATH.
- Supported npm wrapper platforms for this release: Windows and macOS.

## Verification

The release was verified with:

```text
python -m compileall harness_v2
python -m unittest discover tests
python -m harness_v2 status --root .
python -m harness_v2 verify tests\fixtures\valid-task.json
python -m harness_v2 gate tests\fixtures\valid-task.json --root .
python -m harness_v2 doctor --root .
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .
node bin\harness-v2.js doctor --root .
npm pack --dry-run
npm publish
```

## Publish Scope

Release target:

```text
harness-v2@0.1.8
```

Release transaction state after publish:

```text
NPM_PUBLISHED / GITHUB_SOURCE_PUSHED / RELEASE_EXECUTION_CLOSED
```

Repeat npm publish for this version is not possible. A later package update requires a new version.

## HARNESS V2 0.1.7 Release Notes

npm and GitHub release notes for the previous Codex-app-focused HARNESS V2 source.

## Changed In 0.1.7

- Publishes the source package metadata as `0.1.7`.
- Includes generated scaffold hardening for `AGENTS.md`, `RULES.md`, `CURRENT.md`, and `control\`.
- Keeps `harness-v2 init --root .` and `harness-v2 apply --root .` focused on project-root files, not a nested `harness-v2` folder.
- Includes executable 8-stage workflow checks, side-effect preflight checks, and the hook-equivalent `gate` command.
- Includes the local stdio MCP adapter for `status`, `verify`, `preflight`, `gate`, `init`, and `apply`.
- Keeps `doctor` as a read-only integration report that does not mutate project files.
