# HARNESS V2 Workflow 기록

status: package_github_surface / workflow_stage_realignment / records_index

이 파일은 HARNESS V2 workflow 기록의 local lane index입니다. 자체로 decision ledger가 아니라 index와 배치 안내입니다.

## Canonical Stage 기록

생성된 downstream project는 official workflow stage별 task-local record를 `records\stages\` 아래에 받습니다.

| stage | generated record | authority limit |
| --- | --- | --- |
| `spec` | `records\stages\spec.md` | task goal/scope를 기록합니다. planning이나 implementation을 승인하지 않습니다. |
| `spec_review` | `records\stages\spec-review.md` | review finding을 기록합니다. approval을 부여하지 않습니다. |
| `planning` | `records\stages\planning.md` | work order와 proof plan을 기록합니다. work를 실행하지 않습니다. |
| `plan_review` | `records\stages\plan-review.md` | plan review를 기록합니다. implementation을 승인하지 않습니다. |
| `approval` | `records\stages\approval.md` | approval context를 반영합니다. 자체로 side effect를 부여하지 않습니다. |
| `development` | `records\stages\development.md` | implementation note를 기록합니다. approved path를 넓히지 않습니다. |
| `development_review` | `records\stages\development-review.md` | review/proof readback을 기록합니다. 자체로 proof를 만들지 않습니다. |
| `improvement` | `records\stages\improvement.md` | lesson과 next candidate를 기록합니다. product behavior를 바꾸지 않습니다. |

## Supporting 기록

| record | purpose | authority limit |
| --- | --- | --- |
| `records\current-task.md` | 사람이 읽는 current task note | 충돌하면 task contract와 `CURRENT.md`가 우선합니다. |
| `records\decisions.md` | task-local decision과 deferred item | implementation 전 source/approval/proof가 필요합니다. |
| `records\proof.md` | proof command/readback note | `proof.obligations`와 맞지 않으면 proof가 아닙니다. |
| `records\handoff.md` | 다음 session을 위한 continuity note | approval, permission, proof, lifecycle이 아닙니다. |

## Control Surface 분리

`routing\manifest.md`, `artifacts\registry.md`, `artifacts\log.md`, `safety\regression.md`, `safety\improvement.md`, `release\transaction.md`는 control/observability surface로 남습니다. 이 파일들은 `workflow_stage` 값이 아니며 route permission, source authority, proof, regression pass, improvement execution, release readiness를 부여하지 않습니다.

## 배치 규칙

record payload는 이후 scoped workflow가 target file, format, owner, proof need, write permission을 명시할 때만 만들거나 수정합니다.

## 권한 없음 경계

이 파일은 active state, approval, permission, proof, lifecycle transition, route permission, regression pass, improvement execution, implementation completion, Python package registry publish readiness, release readiness를 만들지 않습니다.
