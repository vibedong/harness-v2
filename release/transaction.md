# HARNESS V2 Release Transaction

status: package_github_surface / npm_0.1.9_release / release_transaction_boundary

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

## Current Release Transaction

Release target:

```text
harness-v2@0.1.9
```

Release scope:

- publish the current GitHub source state as npm package `harness-v2@0.1.9`;
- include install/apply confusion guards for direct source checkouts;
- keep the single Korean public `README.md`;
- keep the removed `README.ko.md` package surface excluded;
- keep Python package registry publish denied;
- keep GitHub release/tag creation out of this npm-only transaction unless separately approved.

Required verification:

```text
python -m compileall harness_v2
python -m unittest discover tests
python -m harness_v2 status --root .
python -m harness_v2 verify tests\fixtures\valid-task.json
python -m harness_v2 gate tests\fixtures\valid-task.json --root .
python -m harness_v2 doctor --root .
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .
node bin\harness-v2.js doctor --root .
npm pack --dry-run
npm publish
```

After successful publish, this transaction is closed for `harness-v2@0.1.9`.

## Closed Release History

Closed release target:

```text
harness-v2@0.1.8 / harness-v2@0.1.7 / v0.1.7
```

Closed status:

```text
NPM_PUBLISHED / GITHUB_RELEASE_PUBLISHED / RELEASE_EXECUTION_CLOSED
```

Historical notes:

- npm package `harness-v2@0.1.8` is closed npm release history.
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

The current npm 0.1.9 release transaction allows local verification, git add/commit/push for the verified release commit, and one npm publish for `harness-v2@0.1.9`.

The current npm 0.1.9 release transaction denies:

- Python package registry publish or deploy work;
- GitHub release creation or mutation;
- release tag creation or mutation;
- dependency installation from network;
- secret access;
- external network mutation outside the approved git push and npm publish;
- destructive action outside generated temporary verification artifacts;
- release readiness claims outside the named npm package target.

## Non-Authority Boundary

This file does not execute npm publish, Python package registry publish, deploy, GitHub release, tag creation, approval, permission, proof, lifecycle transition, automatic external enforcement, or implementation completion by itself.
