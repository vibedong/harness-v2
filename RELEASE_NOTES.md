# HARNESS V2 릴리스 노트

## HARNESS V2 0.1.9 릴리스 노트

install/apply 혼동 방지 release를 위한 npm release note입니다.

## 변경 사항

- current source package metadata를 `0.1.9`로 publish합니다.
- `git clone https://github.com/vibedong/harness-v2.git .`가 project-application path가 아님을 명확히 합니다.
- target root가 임의 project name을 가진 direct HARNESS V2 source checkout이면 `init` / `apply`가 fail closed하도록 합니다.
- package-root redirect는 nested `harness-v2` package folder에만 유지합니다.
- HARNESS V2 source checkout과 applied project scaffold를 구분하는 `doctor` diagnostic을 추가합니다.
- README는 AI operating authority가 아니라 user-facing product documentation으로 유지합니다.

## Runtime 요구사항

- Node.js 18 이상
- PATH에 등록된 Python 3.11 이상
- 이번 release의 npm wrapper 지원 platform: Windows, macOS

## 검증

release는 아래 명령으로 검증했습니다.

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

## Publish 범위

release target:

```text
harness-v2@0.1.9
```

이 version에 대한 repeat npm publish는 불가능합니다. 이후 package update에는 새 version이 필요합니다.

## HARNESS V2 0.1.8 릴리스 노트

Korean public README release를 위한 npm release note입니다.

## 변경 사항

- current source package metadata를 `0.1.8`로 publish합니다.
- GitHub와 npm user를 위해 single Korean `README.md`를 사용합니다.
- 별도 `README.ko.md` package surface를 제거합니다.
- README는 AI operating authority가 아니라 user-facing product documentation으로 유지합니다.
- `workflow_binding_engine` classification과 explicit CLI/MCP/task-contract boundary wording을 보존합니다.
- canonical workflow stage `spec`, `spec_review`, `plan`, `plan_review`, `plan_approval`, `development`, `development_review`, `improvement`를 보존합니다.
- `harness-v2 init --root .`와 `harness-v2 apply --root .`는 nested `harness-v2` folder가 아니라 project-root file에 집중합니다.
- hook-equivalent `gate` command, local stdio MCP adapter, `harness_decision`, read-only `doctor` report를 유지합니다.

## Runtime 요구사항

- Node.js 18 이상
- PATH에 등록된 Python 3.11 이상
- 이번 release의 npm wrapper 지원 platform: Windows, macOS

## 검증

release는 아래 명령으로 검증했습니다.

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

## Publish 범위

release target:

```text
harness-v2@0.1.8
```

publish 후 release transaction state:

```text
NPM_PUBLISHED / GITHUB_SOURCE_PUSHED / RELEASE_EXECUTION_CLOSED
```

이 version에 대한 repeat npm publish는 불가능합니다. 이후 package update에는 새 version이 필요합니다.

## HARNESS V2 0.1.7 릴리스 노트

이전 Codex-app-focused HARNESS V2 source를 위한 npm/GitHub release note입니다.

## 0.1.7 변경 사항

- source package metadata를 `0.1.7`로 publish합니다.
- `AGENTS.md`, `RULES.md`, `CURRENT.md`, `control\`에 대한 generated scaffold hardening을 포함합니다.
- `harness-v2 init --root .`와 `harness-v2 apply --root .`는 nested `harness-v2` folder가 아니라 project-root file에 집중합니다.
- executable 8-stage workflow check, side-effect preflight check, hook-equivalent `gate` command를 포함합니다.
- `status`, `verify`, `preflight`, `gate`, `init`, `apply`를 위한 local stdio MCP adapter를 포함합니다.
- `doctor`는 project file을 mutate하지 않는 read-only integration report로 유지합니다.
