# HARNESS V2 0.1.4 Release Notes

Project application polish release for HARNESS V2.

## Changed

- Detects a cloned `harness-v2` package checkout during `init` and applies the scaffold to the parent project folder.
- Reports both `requested_root` and final `root` in `init` / `apply` JSON output.
- Keeps existing `init` / `apply` behavior for ordinary project folders.
- Updated English and Korean troubleshooting for package-checkout versus project-root placement.

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
python -m harness_v2 init --root <temporary project>
python -m harness_v2 verify <temporary project>\contracts\harness-task.json
npm pack --dry-run
npm publish --dry-run
npm publish
```

## Publish Scope

Published npm package:

```text
harness-v2@0.1.4
```

GitHub release:

```text
https://github.com/vibedong/harness-v2/releases/tag/v0.1.4
```
