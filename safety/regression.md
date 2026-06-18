# HARNESS V2 Regression Safety

status: executable_local_mvp_surface / third_slice / regression_safety

This file maps HARNESS V2 boundary risks to regression guard candidates. It does not define executable tests or passing evidence.

## Boundary Risk Map

| risk | guard |
| --- | --- |
| broad approval treated as implementation permission | require exact work unit, target surface, exclusions, proof obligation, and permission preflight |
| permission treated as proof | require artifact checks against `control\proof.md` |
| proof material treated as lifecycle state | require lifecycle requirements in `control\lifecycle.md` |
| route suggestion treated as tool permission | check `routing\manifest.md` against `control\permission.md` |
| registry/log treated as source authority | check `artifacts\registry.md`, `artifacts\log.md`, and `control\source.md` |
| regression mapping treated as pass evidence | require explicit proof obligation and current artifact check |
| improvement candidate applied directly | route through `safety\improvement.md` and a new scoped workflow |
| release boundary treated as release readiness | require a separate release transaction scope |
| legacy V1 or `F:\Folder\harnessresearch\` reused as source | fail closed unless a later explicit source policy changes this |

## Guard Evidence

Valid evidence for this markdown MVP is readback, search, listing, and surface-specific review against current local markdown files.

Executable tests and fixtures inside `tests\` are part of the current proof material. Packages, dependency changes, git, external mutation, destructive operations, and release checks remain outside the current permission ceiling.

## Non-Authority Boundary

This file does not create active regression tests, verification commands, proof, approval, permission, lifecycle transition, route permission, implementation completion, package readiness, or release readiness.
