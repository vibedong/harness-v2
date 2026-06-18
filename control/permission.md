# HARNESS V2 Permission Control

status: package_github_surface / fourth_slice / permission_control

This file separates approved intent from allowed side effects.

## Side Effect Classes

| class | fourth-slice local decision |
| --- | --- |
| local read | allowed for HARNESS V2 product files and planning context needed for this scope |
| local file write | allowed only under `F:\Folder\harness-v2` |
| local command execution | allowed for verification, package smoke, and git/GitHub publish commands below |
| package metadata, package build, local smoke install | allowed only for this product |
| GitHub repository creation and push | allowed only for this product folder |
| PyPI publish, release execution, dependency install | denied |
| secret access, unrelated external network mutation, destructive action | denied |

## Exact Write Surface

Allowed write paths are under `F:\Folder\harness-v2` only.

Any write outside that folder fails closed, except generated package smoke artifacts under the OS temporary directory.

## Allowed Local Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m pip install --target <TEMP>\harness-v2-smoke-target --no-deps --no-build-isolation .`
- `python -m harness_v2 status --root .`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`

The package smoke target may be removed after verification because it is generated proof material, not product source.

## Allowed Git/GitHub Commands

- `git init`
- `git add <intended HARNESS V2 product files>`
- `git commit`
- `gh repo create vibedong/harness-v2 --public --source . --remote origin`
- `git push -u origin <branch>`

## Permission Boundaries

Permission cannot widen approval scope and cannot produce proof, lifecycle state, route permission, regression pass, improvement execution, PyPI publish readiness, or release readiness.

The release transaction file may describe release boundaries, but this permission surface still denies PyPI publish, release execution, dependency install, secret access, unrelated external network mutation, and destructive actions outside generated verification artifacts.
