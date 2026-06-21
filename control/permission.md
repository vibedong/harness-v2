# HARNESS V2 Permission Control

status: package_github_surface / whole_plan_conformance_audit / permission_control

workflow: `remaining_completion_program`

이 파일은 approved intent와 allowed side effect를 분리합니다.

## Authority Negative Boundary

이 permission surface는 evidence carrier, not authority generator입니다.

폴더 존재, registry row, log row, review note, route row, release note, package metadata, test pass, agent claim은 side-effect 판단을 보조하거나 기록할 수 있지만, approval에서 제외한 side effect를 허용하거나 permission ceiling을 넓히지 않습니다.

## Side Effect 분류

| class | 현재 Goal 6 decision |
| --- | --- |
| local read | `F:\Folder\harness-v2`와 generated TEMP verification folder 안에서 허용 |
| local file write | exact Goal 6 docs/control/test audit surface에 필요한 경우 `F:\Folder\harness-v2` 안에서만 허용 |
| new files | 이 slice에서는 denied |
| local command execution | 아래 명령 목록에 있는 경우만 허용 |
| local MCP stdio adapter | 기존 CLI/MCP surface를 통한 readback만 허용. remote hosting 또는 client configuration mutation 없음 |
| hook-equivalent gate | `status`, `verify`, 선택적 `preflight`를 묶는 explicit local command로만 허용. real shell/editor hook이 아님 |
| temporary verification folders | approved verification command 또는 test가 만든 TEMP 하위 폴더만 허용 |
| cleanup | generated TEMP folder, `__pycache__`, `*.egg-info`에 한해 허용 |
| read-only subagent review | `vowline` 적용 조건으로 허용. subagent는 edit, git/network mutation, approval grant, proof production, lifecycle transition declaration 금지 |
| git push | verified Goal 6 commit에 한해 허용 |
| npm publish | 이 local slice에서는 denied |
| GitHub release or release tag | 이 local slice에서는 denied |
| Python package registry publish | denied |
| dependency install from network, secret read, generated verification artifact 밖의 destructive action | denied |

## Exact Write Surface

허용된 write path는 Goal 6에 필요한 `F:\Folder\harness-v2` 하위 product file입니다.

- `README.md`
- `CURRENT.md`
- `RELEASE_NOTES.md`
- `tests\test_harness_v2.py`
- `safety\regression.md`
- `safety\improvement.md`
- `release\transaction.md`
- `routing\manifest.md`
- `control\source.md`
- `control\approval.md`
- `control\permission.md`
- `control\proof.md`
- `control\lifecycle.md`

generated TEMP verification artifact와 그 cleanup을 제외하면 `F:\Folder\harness-v2` 밖의 mutation은 fail closed합니다.

## 허용된 Local Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `python -m harness_v2 status --root .`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 gate tests\fixtures\valid-task.json --root .`
- `python -m harness_v2 doctor --root .`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js gate tests\fixtures\valid-task.json --root .`
- `node bin\harness-v2.js doctor --root .`
- `npm pack --dry-run`

## 허용된 Git/GitHub Commands

- `git add <intended Goal 6 product files>`
- `git commit`
- `git push`

## Permission 경계

permission은 approval scope를 넓힐 수 없고 proof, lifecycle state, route permission, regression pass, improvement execution, package registry publish readiness, release readiness, real hook installation, automatic external enforcement를 만들 수 없습니다.

## Structured PermissionDecision Records

PermissionDecision record는 side effect가 있을 때 active approval을 참조해야 하며, side-effect class를 분류하고, approval ceiling 안에 머물며, file, git, network, release, package, secret, destructive side effect에 대한 preflight status를 포함해야 합니다.

PermissionDecision record는 approval에서 제외한 side effect를 승인할 수 없고, approval ceiling을 넘을 수 없고, proof를 만들 수 없고, lifecycle state를 이동할 수 없습니다.

이 permission surface는 verified Goal 6 commit에 한해서만 git push를 허용합니다. 현재 audit slice에서는 npm publish, Git tag creation, GitHub release creation, Python package registry publish, network dependency installation, secret access, approved Goal 6 git push 밖의 external network mutation, remote MCP hosting, MCP client configuration mutation, Codex app configuration mutation, real shell/editor hook installation, generated verification artifact 밖의 destructive action을 denied합니다.
