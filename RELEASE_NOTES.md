# HARNESS V2 0.1.6 Release Notes

GitHub source release notes for the current Codex-app-focused HARNESS V2 source.

## Changed

- Prepares the current source package metadata as `0.1.6`.
- Includes generated scaffold hardening for `AGENTS.md`, `RULES.md`, `CURRENT.md`, and `control\`.
- Keeps `harness-v2 init --root .` and `harness-v2 apply --root .` focused on project-root files, not a nested `harness-v2` folder.
- Includes executable 8-stage workflow checks, side-effect preflight checks, and the hook-equivalent `gate` command.
- Includes the local stdio MCP adapter for `status`, `verify`, `preflight`, `gate`, `init`, and `apply`.
- Keeps `doctor` as a read-only integration report that does not mutate project files.

## Runtime Requirements

- Node.js 18 or newer.
- Python 3.11 or newer on PATH.
- Supported npm wrapper platforms for this release: Windows and macOS.

## Verification

The release was verified with:

```text
python -m compileall harness_v2
python -m unittest discover tests
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .
node bin\harness-v2.js doctor --root .
python -m harness_v2 init --root <temporary project>
python -m harness_v2 verify <temporary project>\contracts\harness-task.json
npm pack --dry-run
```

Git tag push and GitHub release output close the source release transaction. npm publish is deferred.

## Publish Scope

Release target:

```text
GitHub source release v0.1.6
```

Release transaction state:

```text
GITHUB_SOURCE_RELEASE_PUBLISHED / NPM_PUBLISH_DEFERRED
```

Git tag and GitHub release target:

```text
v0.1.6
```

npm publish, repeat release tag creation, or GitHub release mutation requires a later exact transaction after this source release is closed.
