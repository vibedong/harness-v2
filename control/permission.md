# HARNESS V2 Permission Control

status: package_github_surface / fourth_slice / permission_control

This file separates approved intent from allowed side effects.

## Side Effect Classes

| class | fourth-slice local decision |
| --- | --- |
| local read | allowed for HARNESS V2 product files and planning context needed for this scope |
| local file write | allowed only under `F:\Folder\harness-v2` |
| local command execution | allowed for verification, editable package smoke, Node wrapper smoke, npm dry-run pack, npm registry readback, and git push commands below |
| package metadata, package build, local editable smoke install | allowed only for this product |
| npm wrapper metadata, dry-run pack, and npm registry readback | allowed only for `harness-v2@0.1.5` |
| GitHub repository creation and push | allowed only for this product folder |
| npm publish, Python package registry publish, dependency install | denied |
| secret access, unrelated external network mutation, destructive action | denied |

## Exact Write Surface

Allowed write paths are under `F:\Folder\harness-v2` only.

Any write outside that folder fails closed, except generated package smoke artifacts under the OS temporary directory.

## Allowed Local Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m venv <temporary smoke-test venv under TEMP>`
- `<temporary venv>\Scripts\python -m pip install --no-deps -e .`
- `<temporary venv>\Scripts\python -m harness_v2 status --root <repo root>`
- `<temporary venv>\Scripts\python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 init --root <temporary project>`
- `python -m harness_v2 verify <temporary project>\contracts\harness-task.json`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js init --root <temporary project>`
- `npm pack --dry-run`
- `npm view harness-v2@0.1.5 version dist.tarball`

The temporary smoke-test venv, generated `harness_v2.egg-info`, generated `__pycache__` directories under `F:\Folder\harness-v2`, and npm dry-run generated output may be removed after verification because they are generated proof material, not product source.

## Allowed Git/GitHub Commands

- `git init`
- `git add <intended HARNESS V2 product files>`
- `git commit`
- `gh repo create vibedong/harness-v2 --public --source . --remote origin`
- `git push -u origin <branch>`

## Permission Boundaries

Permission cannot widen approval scope and cannot produce proof, lifecycle state, route permission, regression pass, improvement execution, or Python package registry publish readiness.

The release transaction file may describe release boundaries, but this permission surface still denies npm publish, Python package registry publish, dependency install, secret access, release tag creation, GitHub release execution, unrelated external network mutation, and destructive actions outside generated verification artifacts.
