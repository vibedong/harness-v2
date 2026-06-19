# HARNESS V2 Release Transaction

status: package_github_surface / whole_plan_conformance_audit / release_transaction_boundary

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
- improvement intake;
- binding-surface classification.

No one of these surfaces can create release readiness by itself.

## Closed Release History

Closed release target:

```text
harness-v2@0.1.7 / v0.1.7
```

Closed status:

```text
NPM_PUBLISHED / GITHUB_RELEASE_PUBLISHED / RELEASE_EXECUTION_CLOSED
```

Historical notes:

- npm package `harness-v2@0.1.7` and Git tag/GitHub release `v0.1.7` are closed release history.
- That transaction authorized one npm publish, one Git tag, and one GitHub release for the exact 0.1.7 transaction only.
- The closed transaction does not authorize repeat npm publish, tag mutation, GitHub release mutation, Python package registry publish, dependency installation, secret access, external mutation, or destructive work.
- Local post-0.1.7 workflow engine completion, conformance audit, and `workflow_binding_engine` classification are not npm publish, GitHub release, release tag, deploy, or release readiness by themselves.

## Future Transaction Inputs

A future release transaction must name:

- source release record;
- npm, Python package, GitHub release, tag, deploy, or install artifact target;
- permission scope for package, publish, deploy, install, or external mutation;
- proof obligation and verifier;
- installed project or rollback evidence when applicable;
- lifecycle transition target;
- stale triggers and rollback path.

## Current Permission Ceiling

The current Goal 6 audit slice allows local verification, generated TEMP project verification through tests, read-only subagent review, and git add/commit/push only for the verified Goal 6 commit.

The current Goal 6 audit slice denies:

- npm publish;
- Python package registry publish or deploy work;
- GitHub release creation or mutation;
- release tag creation or mutation;
- dependency installation from network;
- secret access;
- external network mutation outside the approved Goal 6 git push;
- destructive action outside generated temporary verification artifacts;
- release readiness claims.

## Non-Authority Boundary

This file does not execute npm publish, Python package registry publish, deploy, GitHub release, tag creation, approval, permission, proof, lifecycle transition, automatic external enforcement, or implementation completion by itself.
