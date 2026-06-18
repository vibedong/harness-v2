# HARNESS V2 0.1.2 Release Notes

Documentation patch release for the public npm package README.

## Changed

- Expanded `README.md` into a user-first onboarding guide with install, quick start, AI-agent prompt, troubleshooting, and actual task-contract vocabulary.
- Expanded `README.ko.md` into a Korean user manual with the same practical flow.
- Kept examples aligned with the shipped schema fields: `approval.approved_paths`, `permission.allowed_side_effects`, `permission.denied_side_effects`, and `proof.obligations`.
- Kept the npm package as a Windows/macOS wrapper that delegates to the Python CLI.

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
npm pack --dry-run
npm publish --dry-run
npm publish
```

## Publish Scope

Published npm package:

```text
harness-v2@0.1.2
```

GitHub release:

```text
https://github.com/vibedong/harness-v2/releases/tag/v0.1.2
```
