# HARNESS V2 Release Transaction

status: package_github_surface / fourth_slice / release_transaction_boundary

This file defines the local markdown boundary for install and release transactions. It records release readiness inputs but does not execute npm, Python package registry publish, or product release work by itself.

## Release Separation

Release work is separate from:

- source authority;
- approval scope;
- permission preflight;
- proof obligation;
- lifecycle state;
- route guidance;
- artifact registry/log entries;
- regression mapping;
- improvement intake.

No one of these surfaces can create release readiness by itself.

## Future Transaction Inputs

A future release transaction must name:

- source release record;
- npm, Python package, or install artifact target;
- permission scope for package, publish, deploy, install, or external mutation;
- proof obligation and verifier;
- installed project or rollback evidence when applicable;
- lifecycle transition target;
- stale triggers and rollback path.

## Current Release Readiness Audit

Target:

```text
harness-v2@0.1.3
```

Status:

```text
RELEASE_PUBLISHED
```

Reason:

- npm package `harness-v2` already exists, and `0.1.3` is the next project application version for the same package.
- GitHub CLI is authenticated for `vibedong/harness-v2`.
- npm CLI now authenticates successfully with `npm.cmd whoami`.
- The `0.1.3` transaction adds project scaffold application through `harness-v2 init --root .` and `harness-v2 apply --root .`.
- npm registry reports `harness-v2@0.1.3` with tarball `https://registry.npmjs.org/harness-v2/-/harness-v2-0.1.3.tgz`.
- Git tag `v0.1.3` was pushed to `vibedong/harness-v2`.
- GitHub release `v0.1.3` was created at `https://github.com/vibedong/harness-v2/releases/tag/v0.1.3`.
- Post-publish npm install verification succeeded from a temporary npm prefix, including installed `README.ko.md` presence.
- Local verification, init/apply scaffold verification, Node wrapper verification, and npm pack dry-run are the required pre-publish proof commands.
- Exact release execution commands are permitted only for `harness-v2@0.1.3`, `v0.1.3`, and the GitHub repository `vibedong/harness-v2`.

## Current Permission Ceiling

The current package, GitHub publish, npm wrapper, and npm release scope allows local editable package smoke verification, local Node wrapper proof, npm dry-run pack proof, exact npm publish for `harness-v2@0.1.3`, exact Git tag `v0.1.3`, exact GitHub release `v0.1.3`, and GitHub repository push, but denies:

- dependency changes;
- Python package registry publish or deploy work;
- release execution outside `harness-v2@0.1.3` / `v0.1.3`;
- unrelated external network mutation;
- secret access;
- destructive action outside generated verification artifacts;
- release readiness claims.

## Non-Authority Boundary

This file does not execute npm publish, Python package registry publish, deploy, approval, permission, proof, lifecycle transition, or implementation completion by itself.
