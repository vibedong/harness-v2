# HARNESS V2 Workflow 규칙

status: package_github_surface / whole_plan_conformance_audit / workflow_rules

workflow rule은 `RULES.md`를 특화합니다. root rule을 약화하거나 approval, permission, proof, lifecycle state, routing authority, artifact authority, regression pass, improvement execution, release state를 만들 수 없습니다.

## Canonical Workflow Stage

task contract는 stage-specific verifier rule을 위해 `workflow_stage`를 사용합니다. 허용 값은 아래 canonical HARNESS V2 task flow입니다.

```text
spec
spec_review
plan
plan_review
plan_approval
development
development_review
improvement
```

`artifact_observation`, `routing`, `safety_improvement`, `release_boundary`는 workflow stage가 아닙니다. 각각 artifact, route, safety/improvement, release transaction surface로 남습니다.

## Stage와 Owner 분리

`workflow_stage`, `current_gate`, `derived_current_gate`, transition `from_gate` / `to_gate`, freshness `backtrack_target`은 workflow stage만 받습니다.

아래 responsibility owner 또는 domain owner는 workflow stage가 아닙니다.

```text
task
source
workflow
approval
permission
proof
lifecycle
route
artifact
inventory
regression
domain:improvement
release
contract
```

`domain:improvement`는 improvement domain owner를 가리키는 이름입니다. workflow stage `improvement`와 같은 값으로 쓰지 않습니다.

## Record Density Mode 규칙

task contract는 아래 mode field를 사용합니다.

- `task_mode`
- `record_strength`
- `risk_flags`
- `proof_profile`
- `capability_request`
- `classification_required`
- `record_density`

mode engine은 아래 입력의 최댓값으로 `effective_record_strength`를 계산합니다.

- stage minimum
- task mode default
- requested record strength
- risk flags
- proof profile
- capability request
- classification requirement
- write surface
- proof obligations
- lifecycle movement
- stale status
- source volume

`development`는 risk escalation 전에는 `light`에서 시작합니다. approval, permission-sensitive side effect, product write, current proof, stale-risk work, lifecycle movement, release/package/external/secret/destructive capability, ambiguity, `classification_required: true`가 있으면 effective result는 `strict`로 올라갑니다.

record density는 stage order를 바꾸지 않고 approval, permission, proof, lifecycle, stale, route, capability, regression, release check를 약화할 수 없습니다.

실행 검증 조건: strict task contract는 `task_mode`, `record_strength`, `risk_flags`, `proof_profile`, `capability_request`, `classification_required`, `record_density`를 요구합니다. `read_only_analysis`는 mutating side effect를 허용할 수 없습니다. `record_density`는 generated file count, required read-set size, field presence를 computed effective strength와 비교합니다.

## Lifecycle Transition Edge

lifecycle movement는 evaluated operation이며 log line이 아닙니다.

transition evaluator는 같은 task 안에서 아래 route edge만 수락합니다.

```text
spec -> spec_review
spec_review -> spec
spec_review -> plan
plan -> plan_review
plan_review -> plan
plan_review -> plan_approval
plan_approval -> plan
plan_approval -> development
development -> development_review
development_review -> development
development_review -> improvement
improvement -> development
```

same-task `improvement -> spec`은 denied입니다. 새 spec은 separate task가 필요합니다.

## Spec Workflow

목적: 문제와 source를 묶고, output shape와 risk를 기록합니다.

spec work는 task-local stage record만 갱신할 수 있습니다. implementation approval을 만들거나, product write를 실행하거나, permission을 부여하거나, proof를 주장하거나, lifecycle state를 이동할 수 없습니다.

실행 검증 조건: `spec` path는 `records\current-task.md`, `records\stages\spec.md`, `records\decisions.md` 안에 있어야 하며 non-record side effect는 denied입니다.

## Spec Review Workflow

목적: spec이 충분한지 확인하고, missing source와 ambiguity를 찾습니다.

실행 검증 조건: `spec_review` path는 `records\stages\spec-review.md` 또는 `records\decisions.md` 안에 있어야 하며 non-record side effect와 lifecycle movement는 denied입니다.

## Plan Workflow

목적: 구현 계획, 검증 방법, allowed surface를 설계합니다.

plan work는 task-local stage record만 갱신할 수 있습니다. later plan approval, permission, proof obligation, lifecycle entry가 같은 target surface를 모두 명시하기 전에는 product write를 시작할 수 없습니다.

실행 검증 조건: `plan` path는 `records\stages\plan.md` 또는 `records\decisions.md` 안에 있어야 하며 non-record side effect는 denied입니다.

## Plan Review Workflow

목적: 계획의 gap, risk, missing proof를 확인합니다.

review finding은 approval 전에 resolved, deferred, rejected 중 하나로 처리되어야 합니다. review 자체는 implementation을 승인하지 않습니다.

실행 검증 조건: `plan_review` path는 `records\stages\plan-review.md` 또는 `records\decisions.md` 안에 있어야 하며 non-record side effect와 lifecycle movement는 denied입니다.

## Plan Approval Workflow

목적: user approval을 exact edit paths, command, exclusion, proof obligation으로 묶습니다.

approval binding은 side effect를 부여하지 않습니다. side effect는 `control\permission.md`를 통과해야 합니다.

실행 검증 조건: `plan_approval` path는 `control\approval.md`, `records\stages\plan-approval.md`, `records\decisions.md` 안에 있어야 합니다. broad approval phrase는 denied이며 `approval.excluded_side_effects`가 필요합니다.

## Development Workflow

목적: 승인된 surface 안에서 구현합니다.

development work는 현재 exact packet이 열지 않는 한 package metadata, release artifact, dependency, git, secret, external mutation, destructive operation, exact packet 밖의 path를 scope 밖에 둡니다.

실행 검증 조건: `development`는 concrete approved path와 explicit local write side effect를 요구하며 release execution side effect는 denied 상태로 유지됩니다.

## Development Review Workflow

목적: 구현 결과와 proof readiness를 검토합니다.

실행 검증 조건: `development_review` path는 `records\stages\development-review.md`, `records\proof.md`, `records\decisions.md` 안에 있어야 하며 non-record side effect, lifecycle movement, authority claim은 denied입니다.

## Improvement Workflow

목적: regression, follow-up, future-slice 후보를 분류합니다.

improvement는 task-local record와 safety/improvement note를 갱신할 수 있습니다. 새 scoped workflow 없이는 rule, route, code, test, release surface, product behavior를 직접 수정하지 않습니다.

실행 검증 조건: `improvement` path는 `records\stages\improvement.md`, `records\decisions.md`, `records\handoff.md`, `safety\regression.md`, `safety\improvement.md` 안에 있어야 합니다. product implementation path, non-record side effect, release execution은 denied입니다.
