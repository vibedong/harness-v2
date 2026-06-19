# HARNESS V2 Release Transaction

status: package_github_surface / npm_0.1.9_release / release_transaction_boundary

이 파일은 install/release transaction을 위한 local markdown boundary를 정의합니다. release readiness input을 기록하지만, 자체로 npm, Python package registry publish, GitHub release, release tag, deploy, product release work를 실행하지 않습니다.

## Release 분리

release work는 아래 표면과 분리됩니다.

- source authority
- approval scope
- permission preflight
- proof obligation
- lifecycle state
- route guidance
- artifact registry/log entry
- regression mapping
- improvement intake
- binding-surface classification

이 표면 중 어떤 것도 자체로 release readiness를 만들 수 없습니다.

## 현재 Release Transaction

release target:

```text
harness-v2@0.1.9
```

release scope:

- current GitHub source state를 npm package `harness-v2@0.1.9`로 publish합니다.
- direct source checkout에 대한 install/apply confusion guard를 포함합니다.
- single Korean public `README.md`를 유지합니다.
- 제거된 `README.ko.md` package surface는 제외 상태로 유지합니다.
- Python package registry publish는 denied 상태로 유지합니다.
- 별도 approval이 없으면 GitHub release/tag creation은 이 npm-only transaction 밖에 둡니다.

required verification:

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

publish 성공 후 이 transaction은 `harness-v2@0.1.9`에 대해 closed 상태입니다.

## 닫힌 Release History

closed release target:

```text
harness-v2@0.1.8 / harness-v2@0.1.7 / v0.1.7
```

closed status:

```text
NPM_PUBLISHED / GITHUB_RELEASE_PUBLISHED / RELEASE_EXECUTION_CLOSED
```

historical notes:

- npm package `harness-v2@0.1.8`은 closed npm release history입니다.
- npm package `harness-v2@0.1.7`과 Git tag/GitHub release `v0.1.7`은 closed release history입니다.
- 해당 transaction은 exact 0.1.7 transaction에 대해서만 npm publish 1회, Git tag 1회, GitHub release 1회를 승인했습니다.
- closed transaction은 repeat npm publish, tag mutation, GitHub release mutation, Python package registry publish, dependency installation, secret access, external mutation, destructive work를 승인하지 않습니다.
- local post-0.1.7 workflow engine completion, conformance audit, `workflow_binding_engine` classification은 자체로 npm publish, GitHub release, release tag, deploy, release readiness가 아닙니다.

## Future Transaction Input

future release transaction은 아래를 명시해야 합니다.

- source release record
- npm, Python package, GitHub release, tag, deploy, install artifact target
- package, publish, deploy, install, external mutation의 permission scope
- proof obligation과 verifier
- 해당되는 경우 installed project 또는 rollback evidence
- lifecycle transition target
- stale trigger와 rollback path

## 현재 Permission Ceiling

현재 npm 0.1.9 release transaction은 local verification, verified release commit을 위한 git add/commit/push, `harness-v2@0.1.9` npm publish 1회를 허용합니다.

현재 npm 0.1.9 release transaction은 아래를 denied로 둡니다.

- Python package registry publish 또는 deploy work
- GitHub release creation 또는 mutation
- release tag creation 또는 mutation
- network dependency installation
- secret access
- approved git push와 npm publish 밖의 external network mutation
- generated temporary verification artifact 밖의 destructive action
- named npm package target 밖의 release readiness claim

## 권한 없음 경계

이 파일은 자체로 npm publish, Python package registry publish, deploy, GitHub release, tag creation, approval, permission, proof, lifecycle transition, automatic external enforcement, implementation completion을 실행하지 않습니다.
