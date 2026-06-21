# HARNESS V2 Improvement 안전 경계

status: package_github_surface / remaining_completion_program / improvement_safety

이 파일은 improvement observation을 분류합니다. product rule을 직접 바꾸지는 않습니다.

`domain:improvement`는 improvement domain owner입니다. workflow stage `improvement`와 구분하며, domain owner는 workflow stage가 아닙니다.

## Improvement 분류

| class | meaning | next handling |
| --- | --- | --- |
| observation | 발견된 friction, risk, unclear boundary | action 전 evidence를 모읍니다. |
| candidate | 근거가 있는 improvement idea | scoped workflow로 route합니다. |
| rejected | current rule이나 goal과 충돌하는 검토된 idea | rationale을 짧게 남깁니다. |
| deferred | current permission 또는 lifecycle state 밖의 유용한 idea | future scope를 기다립니다. |
| unknown | evidence가 부족한 ambiguous signal | 결정 전 source를 모읍니다. |

## Intake 요구사항

improvement candidate는 아래를 명시해야 합니다.

- 관찰된 issue 또는 opportunity
- source evidence
- affected surface
- touched boundary
- expected benefit
- stale 또는 rollback trigger
- 실제 변경에 필요한 approval과 permission

## 현재 Deferred Candidate

| candidate | class | current handling |
| --- | --- | --- |
| MCP adapter around `status`, `verify`, `preflight`, `gate`, `decision`, `init/apply` | observation | local stdio adapter로 구현되었습니다. future work는 별도 scope에서 Codex app configuration guidance 또는 hook-equivalent integration을 추가할 수 있습니다. |
| hook-equivalent gate over `status`, `verify`, optional `preflight` | observation | direct Codex app hook surface가 없음을 확인한 뒤 explicit local CLI/MCP gate로 구현되었습니다. real hook 연동은 별도 scope에서만 다룹니다. |
| read-only integration doctor for release preparation | observation | integrated surface와 closed release boundary에 대한 local report로 구현되었습니다. future release execution은 여전히 별도 transaction이 필요합니다. |
| record-density mode engine | observation | task-mode / record-strength evaluation으로 구현되었습니다. future work는 측정된 project data로 source-volume과 evidence-binding threshold를 조정할 수 있습니다. |

## Direct-Change Guard

improvement record는 `AGENTS.md`, `RULES.md`, workflow rule, control file, routing, artifact, safety file, release file, code, test, schema, fixture, runner, package, dependency, git, secret, external system, destructive target을 직접 수정하지 않습니다.

## 권한 없음 경계

이 파일은 backlog authority, approval, permission, proof, lifecycle transition, route permission, regression pass, implementation completion, package readiness, release readiness를 만들지 않습니다.
