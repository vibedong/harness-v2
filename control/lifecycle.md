# HARNESS V2 Lifecycle Control

status: package_github_surface / whole_plan_conformance_audit / lifecycle_control

workflow: `remaining_completion_program`

이 파일은 current pointer, progress note, lifecycle state movement를 분리합니다.

## State Model

알려진 local state:

- `scaffold_only`
- `planning_artifact_complete`
- `product_markdown_mvp_authoring`
- `product_markdown_mvp_review`
- `executable_mvp_authoring`
- `executable_mvp_review`
- `package_publish_authoring`
- `package_publish_review`
- `npm_wrapper_authoring`
- `npm_wrapper_review`
- `workflow_realignment_authoring`
- `workflow_realignment_review`
- `transition_ledger_authoring`
- `transition_ledger_review`
- `stale_backtrack_authoring`
- `stale_backtrack_review`
- `record_density_authoring`
- `record_density_review`
- `decision_receipt_authoring`
- `decision_receipt_review`
- `whole_plan_conformance_authoring`
- `whole_plan_conformance_review`
- `workflow_binding_engine_classified`
- `public_release_candidate`
- `public_release_published`
- `package_candidate_ready`
- `npm_published`
- `blocked`
- `deferred`

## 현재 Entry

현재 local lifecycle entry:

```text
decision_receipt_review -> whole_plan_conformance_review
```

Active slice:

```text
whole_plan_conformance_audit / unreleased_local / release_closed
```

scope:

- product write는 `F:\Folder\harness-v2` 안에서만 수행합니다.
- published `harness-v2@0.1.7` / `v0.1.7`은 closed release history입니다.
- executable `workflow_stage`는 brainstorming/stage-plan record에서 나온 canonical task flow를 따릅니다: `spec`, `spec_review`, `plan`, `plan_review`, `plan_approval`, `development`, `development_review`, `improvement`.
- later explicit migration이 ownership을 바꾸기 전까지 `workflow_stage`는 writable compatibility owner이고 `current_gate`는 derived/read-model입니다.
- `artifact_observation`, `routing`, `safety_improvement`, `release_boundary`는 lifecycle workflow stage가 아닙니다.
- artifact, routing, safety/regression, improvement, release transaction surface는 control 또는 observability surface로 남습니다.
- generated downstream project scaffold는 `records\` 아래 task-local stage record를 포함합니다.
- generated `records\gate-state.json`이 있으면 source task `workflow_stage`와 source hash에서 파생된 validated read-model입니다.
- `contracts\transition.schema.json`, `templates\transition-log.md`, `harness_v2\lifecycle.py`는 transition ledger surface를 정의합니다.
- transition log record는 append-only evidence이며 그 자체로 lifecycle state를 이동하지 않습니다.
- transition record append는 이전 transition ledger hash로 guard될 수 있으므로 앞선 block edit 또는 delete는 append 전에 fail합니다.
- lifecycle movement는 evaluated operation이며 log line이 아닙니다.
- transition evaluation은 route edge, task source gate, project-relative source refs, approval reference, permission reference, proof reference, freshness refs, stale check를 확인한 뒤 movement를 수락합니다.
- legacy stage alias와 same-task `improvement -> spec` movement는 fail closed합니다.
- `contracts\freshness.schema.json`, `templates\freshness-map.json`, `harness_v2\freshness.py`는 freshness/backtrack surface를 정의합니다.
- freshness map이 없으면 compatibility diagnostic을 만들며 기존 프로젝트를 조용히 overwrite하지 않습니다.
- stale freshness anchor는 explicit `backtrack_target`과 `reason` 값을 냅니다.
- stale approval, permission, proof, artifact, source, transition evidence는 조용히 재사용할 수 없습니다.
- ApprovalDecision, PermissionDecision, ProofReceipt record는 evidence record일 뿐입니다. 어떤 record도 lifecycle movement를 선언하거나 수행할 수 없습니다.
- task-mode와 record-strength evaluation은 approval, permission, proof, lifecycle, stale, route, capability, regression, release check를 약화하지 않으면서 record density를 제어합니다.
- hook-equivalent gate는 explicit status/verify/preflight command이며 real shell/editor hook이 아닙니다.
- local verification command는 `control\permission.md`에 명시됩니다.
- npm publish, Python package registry publish, GitHub release or tag mutation, dependency install, secret access, approved Goal 6 git push 밖의 external mutation, destructive operation은 이 lifecycle entry에 포함되지 않습니다.

이 entry는 현재 explicit CLI/MCP/task-contract surface를 `workflow_binding_engine`으로 분류하는 데 사용됩니다. public release, repeat npm publish, Python package registry publish, future release authority, shell-level automatic enforcement, real hook installation, remote MCP hosting, MCP client installation, MCP client configuration, ApprovalDecision, PermissionDecision, ProofReceipt, automatic LifecycleTransition이 아닙니다.

## Transition 요구사항

lifecycle state movement는 transition record에서 평가되어야 합니다. lifecycle movement는 evaluated operation이지 log line이 아닙니다.

transition record는 아래를 명시해야 합니다.

- `from_gate`
- `to_gate`
- `reason`
- `source_refs`
- `approval_ref`
- `permission_ref`
- `proof_ref`
- `freshness_refs`
- `stale_check`
- `actor`

evaluator는 아래를 거부해야 합니다.

- unknown 또는 legacy gate name
- canonical same-task route graph 밖의 route edge
- task contract `workflow_stage`와 맞지 않는 `from_gate`
- missing, absolute, escaping, non-existent source 또는 freshness reference
- stale approval, permission, proof, source evidence
- active approval과 permission reference가 없는 `plan_approval -> development`
- active approval, active permission, current proof evidence가 없는 `development_review -> improvement`
- same-task `improvement -> spec`

## Backtrack 규칙

freshness anchor의 backtrack target:

- spec source stale -> `spec`
- spec review source stale -> changed source에 따라 `spec_review` 또는 `spec`
- plan source stale -> `plan`
- plan review stale -> changed source에 따라 `plan_review` 또는 `plan`
- plan approval scope stale -> `plan_approval`
- permission side-effect scope stale -> development 시작 여부에 따라 `plan_approval` 또는 `development`
- proof obligation stale -> changed source에 따라 `development_review` 또는 `development`
- transition ledger stale -> last verified lifecycle gate
- release boundary stale -> improvement 또는 blocked release audit

approval scope, permission scope, source basis, proof obligation, lifecycle target, route surface, artifact surface, safety boundary, improvement classification, release boundary, package surface, npm wrapper surface, generated scaffold behavior, workflow stage enum, freshness map, binding-surface classification, target surface가 stale 또는 conflicting이 되면 `whole_plan_conformance_review`, `decision_receipt_review`, `stale_backtrack_authoring`, `transition_ledger_review`, `workflow_realignment_authoring`, `package_publish_review`, `public_release_published` 중 필요한 지점으로 backtrack합니다.

이 파일은 proof, approval, npm publish state, Python package registry publish state, release state, route permission, regression pass, improvement execution, future slice permission을 만들지 않습니다.
