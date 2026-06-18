# HARNESS V2 Regression Safety

status: package_github_surface / fourth_slice / regression_safety

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
| package/GitHub MVP mistaken for Python package registry release | require separate Python package registry or release transaction approval |
| npm wrapper MVP mistaken for npm release | require a separate release transaction and exact npm target approval |
| author-local paths copied into GitHub-facing commands | require `<repo root>` or current-directory examples for portable docs |

## Guard Evidence

Valid evidence for this package, GitHub, npm wrapper, and public npm release surface is readback, search, listing, unittest output, editable install smoke output, Node wrapper smoke output, npm dry-run pack output, npm publish dry-run output, fresh-client clone verification when separately approved, and surface-specific review against current local files.

Executable tests and fixtures inside `tests\` are part of the current proof material. Package metadata, editable install smoke verification, Windows/macOS npm wrapper metadata, local Node wrapper smoke, npm dry-run pack verification, npm publish dry-run verification, exact npm publish for `harness-v2@0.1.1`, git initialization, GitHub repository creation, tag, release, and push are allowed only inside the current release transaction scope.

Python package registry publish, dependency installation from the network, secret access, unrelated external mutation, destructive operations outside generated verification artifacts, and release work outside `harness-v2@0.1.1` remain outside the current permission ceiling.

## Non-Authority Boundary

This file does not create active regression tests, verification commands, proof, approval, permission, lifecycle transition, route permission, implementation completion, package readiness, or release readiness.
