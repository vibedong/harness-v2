# HARNESS V2 Release Transaction

status: package_github_surface / remaining_completion_program / release_transaction_boundary

This file defines the local markdown boundary for install and release transactions. It records release readiness inputs but does not execute npm, Python package registry publish, GitHub release, release tag, deploy, or product release work by itself.

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
- npm, Python package, GitHub release, tag, deploy, or install artifact target;
- permission scope for package, publish, deploy, install, or external mutation;
- proof obligation and verifier;
- installed project or rollback evidence when applicable;
- lifecycle transition target;
- stale triggers and rollback path.

## Current Release Transaction Status

Target:

```text
harness-v2@0.1.5
```

Status:

```text
NPM_PUBLISHED_HISTORICAL / RELEASE_EXECUTION_CLOSED
```

Reason:

- npm package `harness-v2@0.1.5` is already published.
- The current remaining completion program may verify package shape with `npm pack --dry-run`, but does not authorize repeat npm publish.
- Generated scaffold hardening improves the files created by `harness-v2 init --root .` and `harness-v2 apply --root .` for future package updates.
- Git tag creation and GitHub release execution are not permitted by the current transaction.
- Python package registry publish is not permitted by the current transaction.

## Current Permission Ceiling

The current remaining completion program allows local verification, generated TEMP project verification, read-only subagent review, `npm pack --dry-run`, and git push after completed slices pass verification and review.

The current transaction denies:

- npm publish;
- Python package registry publish or deploy work;
- GitHub release creation;
- release tag creation;
- dependency installation from network;
- secret access;
- external network mutation outside allowed git push;
- destructive action outside generated temporary verification artifacts;
- release readiness claims.

## Non-Authority Boundary

This file does not execute npm publish, Python package registry publish, deploy, GitHub release, tag creation, approval, permission, proof, lifecycle transition, automatic enforcement completion, or implementation completion by itself.
