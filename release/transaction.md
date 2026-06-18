# HARNESS V2 Release Transaction

status: package_github_surface / fourth_slice / release_transaction_boundary

This file defines the local markdown boundary for install and release transactions. It records release readiness inputs but does not execute npm, PyPI, or product release work by itself.

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
harness-v2@0.1.0
```

Status:

```text
RELEASE_READY_NPM_AUTH_PRESENT
```

Reason:

- npm package name `harness-v2` returned registry 404 during readiness check, so the name appears available.
- GitHub CLI is authenticated for `vibedong/harness-v2`.
- npm CLI now authenticates successfully with `npm.cmd whoami`.
- Git tag `v0.1.0` and GitHub release `v0.1.0` must not be created until npm publish succeeds.
- Local verification, Node wrapper verification, and npm pack dry-run are the required pre-publish proof commands.
- Exact release execution commands are permitted only for `harness-v2@0.1.0`, `v0.1.0`, and the GitHub repository `vibedong/harness-v2`.

## Current Permission Ceiling

The current package, GitHub publish, npm wrapper, and npm release scope allows local editable package smoke verification, local Node wrapper proof, npm dry-run pack proof, exact npm publish for `harness-v2@0.1.0`, exact Git tag `v0.1.0`, exact GitHub release `v0.1.0`, and GitHub repository push, but denies:

- dependency changes;
- PyPI publish or deploy work;
- release execution outside `harness-v2@0.1.0` / `v0.1.0`;
- unrelated external network mutation;
- secret access;
- destructive action outside generated verification artifacts;
- release readiness claims.

## Non-Authority Boundary

This file does not execute npm publish, PyPI publish, deploy, approval, permission, proof, lifecycle transition, or implementation completion by itself.
