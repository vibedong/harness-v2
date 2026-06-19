# HARNESS V2 Gate Manifest 템플릿

status: template / not_record / not_approval / not_permission / not_proof / not_lifecycle

## Gate

- work unit: `<work-unit>`
- target surface: `<target-surface>`
- current state: `<current-state>`
- requested next state: `<next-state>`

## Required Check

1. source freshness
2. exact approval scope
3. permission과 side-effect ceiling
4. proof obligation
5. lifecycle entry
6. release separation

이 템플릿은 approval, permission, proof, lifecycle transition, route permission, regression pass, package readiness, release readiness가 아닙니다.
