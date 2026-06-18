# HARNESS V2 Approval Control

status: package_github_surface / fourth_slice / approval_control

This file separates approval request, user response, and bound approval scope.

## Current Bound Scope

Previous bound work unit:

```text
package_metadata_install_smoke_and_github_publish_slice
```

Current bound work unit:

```text
generated_agent_binding_package_candidate_slice
```

Previous bound user packet:

```text
Approve third HARNESS V2 executable local MVP slice:
create or modify only these paths under F:\Folder\harness-v2:
AGENTS.md, RULES.md, CURRENT.md,
README.md,
rules\workflows.md,
control\source.md, control\approval.md, control\permission.md,
control\proof.md, control\lifecycle.md,
records\README.md, routing\manifest.md,
artifacts\registry.md, artifacts\log.md,
safety\regression.md, safety\improvement.md,
release\transaction.md,
contracts\task.schema.json,
contracts\approval.schema.json,
contracts\permission.schema.json,
contracts\proof.schema.json,
contracts\lifecycle.schema.json,
contracts\artifact.schema.json,
templates\task.json,
templates\gate-manifest.md,
templates\approval-request.md,
templates\proof-report.md,
harness_v2\__init__.py,
harness_v2\__main__.py,
harness_v2\cli.py,
harness_v2\core.py,
harness_v2\verify.py,
harness_v2\doctor.py,
tests\test_harness_v2.py,
tests\fixtures\valid-task.json,
tests\fixtures\invalid-missing-approval.json.
Allowed local commands for verification only:
python -m compileall harness_v2
python -m unittest discover tests
No package metadata, package build, install, publish, deploy, release, git, dependency install,
secret access, external network mutation, or destructive operation.
```

Current bound user request:

```text
git hub 배포, 패키지 까지 하자
그 하네스폴더만 해
그것도하자
설치하면 바로 하네스 적용되는걸로가야대
그래 고고
README는 사용자문서고, AI가 보는게 아님.
그래 그것도 손봐라. goal npm패키지 전까지 다해놔
```

Current bound amendment:

```text
Approve fourth-slice amendment:
also allow keeping and modifying these existing files under F:\Folder\harness-v2:
.gitattributes,
_build_backend\harness_backend.py.

Allow implementing PEP 660 editable install support in _build_backend\harness_backend.py.

Allow rerunning:
python -m compileall harness_v2
python -m unittest discover tests
python -m venv <temporary smoke-test venv under TEMP>
<temporary venv>\Scripts\python -m pip install --no-deps -e .
<temporary venv>\Scripts\python -m harness_v2 status --root <repo root>
<temporary venv>\Scripts\python -m harness_v2 verify tests\fixtures\valid-task.json

Allow cleaning generated verification artifacts:
temporary smoke-test venv under TEMP,
harness_v2.egg-info if generated,
__pycache__ directories generated under F:\Folder\harness-v2.

Allow git add/commit/push only for this amendment to vibedong/harness-v2.

No Python package registry publish.
No secrets read.
No dependency install from network.
No destructive operation outside the named generated verification artifacts.
```

Current bound npm wrapper packet:

```text
Approve HARNESS V2 npm wrapper package slice:
work only under F:\Folder\harness-v2.

Allow creating/modifying only:
package.json,
bin\harness-v2.js,
README.md,
CURRENT.md,
control\approval.md,
control\permission.md,
control\proof.md,
control\lifecycle.md,
release\transaction.md,
tests\test_harness_v2.py.

Purpose:
add a Windows/macOS npm CLI wrapper package for HARNESS V2 that delegates to the existing Python CLI,
without rewriting HARNESS V2 in JavaScript and without publishing to npm yet.

Supported platforms:
Windows and macOS only for this slice.
Python 3 is an explicit runtime prerequisite.

Allow local verification:
python -m compileall harness_v2
python -m unittest discover tests
node bin\harness-v2.js status --root .
node bin\harness-v2.js verify tests\fixtures\valid-task.json
npm pack --dry-run
npm publish --dry-run

No Python package registry publish.
No npm publish.
No dependency install from network.
No secret read.
No destructive operation outside generated verification artifacts.
```

Operation type:

- local file creation or modification only under `F:\Folder\harness-v2`;
- local package metadata and dependency-free build backend creation;
- PEP 660 editable install support in `_build_backend\harness_backend.py`;
- local editable package smoke verification with generated artifacts limited to temporary paths or ignored build metadata;
- dependency-free npm wrapper metadata and Windows/macOS Node CLI wrapper creation;
- local Node wrapper smoke verification and `npm pack --dry-run`;
- npm publish dry-run verification for the `harness-v2@0.1.5` package candidate;
- no npm publish, release tag creation, or GitHub release execution in the current package-candidate slice;
- project application release that adds `harness-v2 init --root .` and `harness-v2 apply --root .`;
- git initialization, commit, GitHub repository creation, and push for the `F:\Folder\harness-v2` folder only;
- no npm publish, Python package registry publish, dependency install, secret access, release tag creation, GitHub release execution, or destructive operation outside generated local verification artifacts.

Freshness anchors:

- exact third-slice user packet;
- `CURRENT.md` package, GitHub, and npm wrapper pointer;
- `control\permission.md` exact write and command surface;
- `control\proof.md` fourth-slice proof obligation;
- `control\lifecycle.md` package, GitHub, and npm wrapper lifecycle entry.
- fourth-slice user request constrained to the HARNESS folder only.
- fourth-slice amendment for `.gitattributes`, `_build_backend\harness_backend.py`, editable install proof, generated artifact cleanup, and amendment git push.
- historical npm wrapper package slice approval for `package.json`, `bin\harness-v2.js`, local Node wrapper proof, and npm dry-run proof.
- historical public release preparation approval for `LICENSE`, `RELEASE_NOTES.md`, npm public package metadata, npm publish dry-run, tag/release planning, and npm publish execution.
- historical npm init/apply release request for `harness-v2@0.1.4`, superseded by the current `0.1.5` package-candidate slice.
- user request to strengthen generated agent-facing scaffold and prepare the next npm package candidate before any npm publish.

Denied by the current approval scope:

- paths outside `F:\Folder\harness-v2`;
- npm publish;
- Python package registry publish;
- dependency install outside already available local tooling;
- secret access;
- external network mutation outside GitHub repository push;
- release tag creation or GitHub release execution;
- destructive operation outside generated local verification artifacts.

## Scope Fit

An action is inside approval scope only when it matches the work unit, target surface, operation type, exclusions, freshness anchors, and proof obligation.

If any part is wider, missing, or stale, approval does not fit and the workflow fails closed.

This file does not grant permission, produce proof, move lifecycle state, grant route permission, create regression pass, execute improvement, or prepare release.
