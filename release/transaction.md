# HARNESS V2 Release Transaction

status: package_github_surface / fourth_slice / release_transaction_boundary

This file defines the local markdown boundary for future install and release transactions. It does not execute or prepare a PyPI or product release.

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
- package or install artifact target;
- permission scope for package, publish, deploy, install, or external mutation;
- proof obligation and verifier;
- installed project or rollback evidence when applicable;
- lifecycle transition target;
- stale triggers and rollback path.

## Current Denials

The current package and GitHub publish scope allows local package smoke verification and GitHub repository push, but denies:

- dependency changes;
- PyPI publish or deploy work;
- release execution;
- unrelated external network mutation;
- secret access;
- destructive action outside generated verification artifacts;
- release readiness claims.

## Non-Authority Boundary

This file does not execute, approve, prepare, or validate PyPI publish, deploy, release, approval, permission, proof, lifecycle transition, implementation completion, or release readiness.
