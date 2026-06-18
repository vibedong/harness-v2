# HARNESS V2 0.1.3 Release Notes

Project application release for HARNESS V2.

## Changed

- Added `harness-v2 init --root .` to apply HARNESS V2 scaffold files to a project.
- Added `harness-v2 apply --root .` as an alias for `init`.
- Added an initial valid task contract at `contracts\harness-task.json` in initialized projects.
- Added idempotent scaffold behavior: existing files are skipped unless `--force` is passed.
- Updated English and Korean README quick starts to use install, init, status, and verify.

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
harness-v2@0.1.3
```

GitHub release:

```text
https://github.com/vibedong/harness-v2/releases/tag/v0.1.3
```
