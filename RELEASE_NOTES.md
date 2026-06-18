# HARNESS V2 0.1.1 Release Notes

Documentation patch release for HARNESS V2.

## Changed

- Reworked `README.md` into a practical user manual.
- Added Korean documentation in `README.ko.md`.
- Replaced the package-registry acronym in user-facing and control-plane documentation with the clearer phrase `Python package registry publish`.
- Updated release notes and control surfaces to reflect that the public npm release is already published.

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
```

## Publish Scope

Published npm package:

```text
harness-v2@0.1.1
```

GitHub release:

```text
https://github.com/vibedong/harness-v2/releases/tag/v0.1.1
```
