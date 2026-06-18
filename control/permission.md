# HARNESS V2 Permission Control

status: package_github_surface / detail_step_20_docs_control_sync / permission_control

This file separates approved intent from allowed side effects.

## Side Effect Classes

| class | detail step 20 local decision |
| --- | --- |
| local read | allowed for HARNESS V2 product files and planning context needed for this docs/control sync |
| local file write | allowed only for the eleven files named in `control\approval.md` |
| local command execution | allowed only for local readback/search verification and the git commands below |
| package metadata, package build, local editable smoke install | denied for this slice |
| npm wrapper metadata, dry-run pack, npm registry readback | denied for this slice |
| GitHub repository push | allowed only for this docs/control sync slice after review passes |
| npm publish, npm publish dry-run, Python package registry publish, dependency install | denied |
| secret access, unrelated external network mutation, destructive action | denied |

## Exact Write Surface

Allowed write paths are:

- `AGENTS.md`
- `RULES.md`
- `CURRENT.md`
- `README.md`
- `README.ko.md`
- `routing\manifest.md`
- `control\approval.md`
- `control\permission.md`
- `control\proof.md`
- `control\lifecycle.md`
- `release\transaction.md`

Any write outside those files fails closed.

## Allowed Local Commands

- local file readback, listing, and search commands scoped to this repository;
- `git status --short`
- `git diff -- <intended docs/control files>`

No package build, npm pack, npm publish dry-run, npm registry readback, Python package smoke install, dependency install, hook work, or MCP work is allowed by this slice.

## Allowed Git/GitHub Commands

- `git add <intended HARNESS V2 product files>`
- `git commit`
- `git push`

## Permission Boundaries

Permission cannot widen approval scope and cannot produce proof, lifecycle state, route permission, regression pass, improvement execution, or Python package registry publish readiness.

The release transaction file may describe release boundaries, but this permission surface still denies npm publish, npm publish dry-run, Python package registry publish, package build, dependency install, secret access, release tag creation, GitHub release execution, unrelated external network mutation outside the allowed git push, and destructive actions.
