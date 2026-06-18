# HARNESS V2 Workflow Records

status: package_github_surface / fourth_slice / records_index

This file is the local lane index for future HARNESS V2 workflow records. It is an index and placement guide, not a decision ledger by itself.

## Lane Index

| lane | purpose | authority limit |
| --- | --- | --- |
| source | records source basis, freshness anchors, and conflicts | does not override `control\source.md` |
| spec | records spec request and spec review material | does not approve implementation |
| plan | records plan artifact and plan review material | does not execute work |
| approval | records approval requests and bound scopes | does not grant side effects |
| permission | records side-effect preflight material | does not prove completion |
| proof | records proof obligations and artifact check material | does not become proof without evaluation |
| lifecycle | records lifecycle entry candidates and transition material | does not move state by log presence |
| route | records routing review material | does not grant route permission |
| artifact | records gate-relevant artifact observations | does not become source authority |
| safety | records regression, misuse, and boundary-risk observations | does not create regression pass |
| improvement | records improvement candidates and lessons | does not apply product changes |
| release | records release transaction candidates | does not create release readiness |

## Placement Rule

Record payloads are created only when a later scoped workflow names their target file, format, owner, proof need, and write permission.

Until then, this README provides lane names and boundaries only.

## Non-Authority Boundary

This file does not create active state, approval, permission, proof, lifecycle transition, route permission, regression pass, improvement execution, implementation completion, PyPI publish readiness, or release readiness.
