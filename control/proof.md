# HARNESS V2 Proof Control

status: package_github_surface / whole_plan_conformance_audit / proof_control

workflow: `remaining_completion_program`

이 파일은 proof obligation, artifact check, proof result를 분리합니다.

## Authority Negative Boundary

이 proof surface는 evidence carrier, not authority generator입니다.

폴더 존재, registry row, log row, review note, route row, release note, package metadata, test pass, agent claim은 proof material이 될 수 있지만, current ProofReceipt나 proof obligation 평가 없이 proof result를 만들지 않습니다.

## 현재 Proof Obligation

Goal 6 whole-plan conformance와 binding surface audit slice에서는 authoring 후 아래를 검증합니다.

1. canonical stage identifier가 `RULES.md`와 `writingplans.md`에 맞는지 확인합니다.
2. `workflow_stage`가 writable owner로 남고 `current_gate`가 derived/read-model value로 남는지 확인합니다.
3. transition evaluator가 존재하고 log-only movement를 거부하는지 확인합니다.
4. stale/backtrack engine이 stale approval, permission, proof, source, artifact, transition reuse를 거부하는지 확인합니다.
5. `effective_record_strength`가 `classification_required`를 포함하는지 확인합니다.
6. `development`가 risk escalation 전에는 `light`로 default되고, risk가 요구하면 `strict`로 올라가는지 확인합니다.
7. ApprovalDecision, PermissionDecision, ProofReceipt evaluator가 broad scope, missing source binding, stale refs, lifecycle-transition claim에서 fail closed하는지 확인합니다.
8. 노출된 status, verify, gate, doctor surface에서 CLI behavior, npm wrapper behavior, MCP wrapper behavior, hook-equivalent gate behavior가 정렬되어 있는지 확인합니다.
9. fresh-project scaffold verification과 existing-project preservation이 현재 local test로 덮이는지 확인합니다.
10. docs/control/release surface가 지원되지 않는 automatic external enforcement, npm publish, GitHub release, Python package registry publish, release readiness, proof completion, lifecycle completion을 주장하지 않는지 확인합니다.
11. local verification command가 통과하거나 blocked command가 blocked로 보고되는지 확인합니다.

## Verification Commands

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

## Artifact Check

readback, search, listing, diff output, test output, CLI output, Node wrapper output, npm dry-run output, review finding은 이 slice의 artifact check입니다. proof obligation에 대해 평가되기 전까지는 evidence material일 뿐입니다.

subagent report와 review finding은 defect를 찾는 데 도움을 줄 수 있지만 그 자체로 proof result가 아닙니다.

## Release Transaction Evidence

이 local slice에서는 npm publish, GitHub release, release tag, Python package registry publish가 denied이므로 release transaction evidence가 필요하지 않습니다.

이전 `harness-v2@0.1.7` / `v0.1.7` release evidence는 closed history이며, 이 slice의 publish를 승인하지 않습니다.

## Freshness

target file, source hash, approval scope, permission scope, proof obligation, lifecycle state, transition schema, transition log format, freshness map, artifact registry, route guidance, npm target, release boundary, generated scaffold behavior, workflow stage enum, binding-surface classification, automatic-enforcement wording이 바뀌면 proof evidence는 stale이 됩니다.

## Structured ProofReceipt Records

ProofReceipt record는 proof obligation을 verifier command 또는 readback method, verifier result, current source hash, proof predicate와 묶습니다. test pass, review pass, metadata value, agent claim은 current ProofReceipt에 잡히지 않으면 proof가 아닙니다.

task가 proof receipt를 required로 선언하면 ProofReceipt가 없거나 참조한 source hash가 stale인 경우 verification은 fail closed합니다.

ProofReceipt record는 approval을 부여하거나, permission을 부여하거나, lifecycle state를 이동하거나, release readiness를 만들 수 없습니다.

이 파일은 approval, permission, lifecycle state, route permission, regression pass, improvement execution, package registry publish state, release state, final completion, future-slice authority를 부여하지 않습니다.
