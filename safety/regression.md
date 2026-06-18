# HARNESS V2 Regression Safety

status: package_github_surface / remaining_completion_program / regression_safety

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
| generated scaffold mistaken for automatic enforcement completion | require generated AGENTS/RULES/CURRENT to say scaffold + task-contract validator + CLI helper, not automatic enforcement sandbox or completion layer |
| workflow area documented but not executable | require `workflow_stage` enum, verifier stage predicates, valid examples for all stages, and representative rejection tests |
| preflight adapter mistaken for shell-level blocking | require README/control wording that preflight checks proposed actions but does not execute or automatically block external tools |
| MCP feasibility mistaken for MCP implementation | require README/routing/control wording that no MCP server, manifest, or runtime implementation is shipped in this slice |

## Guard Evidence

Valid evidence for this package, GitHub, npm wrapper, generated scaffold, and remaining completion program surface is readback, search, listing, unittest output, Node wrapper smoke output, fresh TEMP init/verify output, npm dry-run pack output, and surface-specific review against current local files.

Executable tests and fixtures inside `tests\` are part of the current proof material. Package metadata, Windows/macOS npm wrapper metadata, local Node wrapper smoke, npm dry-run pack verification, fresh scaffold verification, and git push are allowed only inside the current remaining completion approval and permission scope.

Npm publish, Python package registry publish, dependency installation from the network, secret access, unrelated external mutation, destructive operations outside generated verification artifacts, GitHub release creation, release tag creation, MCP implementation, and release execution remain outside the current permission ceiling.

## Non-Authority Boundary

This file does not create active regression tests, verification commands, proof, approval, permission, lifecycle transition, route permission, implementation completion, package readiness, or release readiness.
