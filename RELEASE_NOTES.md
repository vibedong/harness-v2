# HARNESS V2 0.1.0 Release Notes

Initial public npm release candidate for HARNESS V2.

## Included

- Product-local HARNESS V2 control-plane documents for source, approval, permission, proof, lifecycle, routing, artifacts, regression, improvement, and release boundaries.
- Standard-library Python CLI with `status`, `verify`, and `doctor` commands.
- Executable verifier hardening for workflow/current pointer mismatch, side-effect conflicts, lifecycle known states, stale status surfaces, and author-local status command roots.
- Dependency-free Python editable install support through the local build backend included in the source and npm tarball.
- Dependency-free Windows/macOS npm CLI wrapper that delegates to the Python CLI.
- Unit tests and fixtures for the local verifier and npm wrapper, included in the source and npm tarball.

## Runtime Requirements

- Node.js 18 or newer.
- Python 3.11 or newer on PATH.
- Supported npm wrapper platforms for this release: Windows and macOS.

## Verification

The release candidate is expected to pass:

```text
python -m compileall harness_v2
python -m unittest discover tests
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
npm pack --dry-run
```

## Publish Scope

The intended npm publish target is:

```text
harness-v2@0.1.0
```

PyPI publish is not included in this release.

Release execution requires npm authentication, a git tag, a GitHub release, and post-publish fresh install verification.
