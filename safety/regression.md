# HARNESS V2 Regression Safety

status: package_github_surface / remaining_completion_program / regression_safety

이 파일은 HARNESS V2 boundary risk를 regression guard candidate에 매핑합니다. executable test나 passing evidence를 정의하지 않습니다.

## Boundary Risk Map

| risk | guard |
| --- | --- |
| broad approval treated as implementation permission | exact work unit, target surface, exclusion, proof obligation, permission preflight 요구 |
| permission treated as proof | `control\proof.md` 기준 artifact check 요구 |
| proof material treated as lifecycle state | `control\lifecycle.md`의 lifecycle requirement 요구 |
| route suggestion treated as tool permission | `routing\manifest.md`를 `control\permission.md`와 대조 |
| registry/log treated as source authority | `artifacts\registry.md`, `artifacts\log.md`, `control\source.md` 확인 |
| regression mapping treated as pass evidence | explicit proof obligation과 current artifact check 요구 |
| improvement candidate applied directly | `safety\improvement.md`와 new scoped workflow로 route |
| release boundary treated as release readiness | separate release transaction scope 요구 |
| legacy V1 or `F:\Folder\harnessresearch\` reused as source | later explicit source policy가 바뀌기 전까지 fail closed |
| package/GitHub MVP mistaken for Python package registry release | separate Python package registry 또는 release transaction approval 요구 |
| npm wrapper MVP mistaken for npm release | separate release transaction과 exact npm target approval 요구 |
| author-local paths copied into GitHub-facing commands | portable docs를 위해 `<repo root>` 또는 current-directory example 요구 |
| generated scaffold mistaken for automatic enforcement completion | generated AGENTS/RULES/CURRENT가 scaffold + task-contract validator + CLI helper이며 automatic enforcement sandbox 또는 completion layer가 아니라고 명시 |
| workflow area documented but not executable | `workflow_stage` enum, verifier stage predicate, all-stage valid example, representative rejection test 요구 |
| control surface mixed into workflow stage | `artifact_observation`, `routing`, `safety_improvement`, `release_boundary`를 `workflow_stage`로 거부하고 control/observability surface로 유지 |
| spec-stage work disappears from records | init/apply 중 `records\stages\spec.md`와 companion stage record file 생성 |
| preflight adapter mistaken for shell-level blocking | preflight가 proposed action을 확인할 뿐 실행하거나 external tool을 자동 차단하지 않는다는 README/control wording 요구 |
| MCP stdio adapter mistaken for source of truth | MCP가 existing HARNESS V2 core behavior를 감싸며 source, approval, permission, proof, lifecycle, release boundary를 대체하지 않는다는 README/routing/control wording 요구 |
| MCP stdio adapter mistaken for remote MCP hosting or shell-level blocking | local stdio only이며 hook, HTTP server, editor blocker, shell blocker가 아니라는 README/routing/control wording 요구 |
| hook-equivalent gate mistaken for a real shell/editor blocker | CLI/MCP test와 `gate`가 explicit이고 external tool을 자동 차단하지 않는다는 README/routing/control wording 요구 |
| integration doctor mistaken for release readiness | doctor output과 release/control wording에서 release boundary가 closed임을 요구 |
| transition log treated as lifecycle movement by itself | lifecycle evaluator test와 lifecycle movement가 log line이 아니라 evaluated operation이라는 wording 요구 |
| stale approval, permission, proof, source, artifact, or transition evidence reused silently | source hash, stale reason, explicit backtrack target을 가진 freshness anchor 요구 |
| metadata-only freshness map edit treated as stale clearance | reason/status text만이 아니라 source file hash 비교 요구 |
| absent freshness map breaks existing projects | compatibility diagnostic과 no silent overwrite 요구 |

## Guard Evidence

이 package, GitHub, npm wrapper, generated scaffold, remaining completion program surface의 valid evidence는 readback, search, listing, unittest output, Node wrapper smoke output, fresh TEMP init/verify output, npm dry-run pack output, current local file에 대한 surface-specific review입니다.

`tests\` 안의 executable test와 fixture는 current proof material의 일부입니다. package metadata, Windows/macOS npm wrapper metadata, local Node wrapper smoke, npm dry-run pack verification, fresh scaffold verification, git push는 current remaining completion approval과 permission scope 안에서만 허용됩니다.

npm publish, Python package registry publish, network dependency installation, secret access, unrelated external mutation, generated verification artifact 밖의 destructive operation, GitHub release creation, release tag creation, remote MCP hosting, MCP client configuration mutation, release execution은 current permission ceiling 밖에 있습니다.

## Non-Authority Boundary

이 파일은 active regression test, verification command, proof, approval, permission, lifecycle transition, route permission, implementation completion, package readiness, release readiness를 만들지 않습니다.
