# HARNESS V2 Proof Control

status: package_github_surface / remaining_completion_program / proof_control

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the MCP stdio adapter implementation slice, verify after authoring:

1. generated scaffold hardening remains documented and covered by tests;
2. executable 8-stage workflow enforcement remains documented and covered by tests;
3. side-effect preflight remains documented as a pre-execution contract check, not automatic shell-level blocking;
4. MCP is implemented only as a local stdio JSON-RPC adapter over existing HARNESS V2 core functions;
5. MCP tools expose status, verify, preflight, init, and apply without making MCP the source of truth;
6. README and README.ko describe status, verify, init/apply, preflight, MCP, update behavior, and current non-automatic-enforcement limits;
7. control, routing, artifact, safety, improvement, and release surfaces agree on current approval, permission, proof, lifecycle, MCP, and release boundaries;
8. read-only subagent review findings are reflected or explicitly rejected before git push;
9. the approved local verification commands pass or blocked commands are reported as blocked;
10. git status and push output show the final intended product state is current on `vibedong/harness-v2`.

## Verification Commands

- `python -m compileall harness_v2`
- `python -m unittest discover tests`
- `node bin\harness-v2.js status --root .`
- `node bin\harness-v2.js verify tests\fixtures\valid-task.json`
- `node bin\harness-v2.js preflight tests\fixtures\valid-task.json --side-effect "python -m compileall harness_v2"`
- `node bin\harness-v2.js mcp < JSON-RPC smoke input`
- `node bin\harness-v2.js init --root <temporary project>`
- `python -m harness_v2 status --root <repo root>`
- `python -m harness_v2 verify tests\fixtures\valid-task.json`
- `python -m harness_v2 preflight tests\fixtures\valid-task.json --side-effect "python -m unittest discover tests"`
- `python -m harness_v2 mcp < JSON-RPC smoke input`
- `python -m harness_v2 init --root <temporary project>`
- `python -m harness_v2 verify <temporary project>\contracts\harness-task.json`
- `npm pack --dry-run`

## Artifact Checks

Readback, search, listing, diff output, temporary fresh-project verification, subagent findings, git status, and git push output are artifact checks for this slice. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Freshness

Proof evidence becomes stale when target files, write surface, approval scope, permission scope, proof obligation, lifecycle state, route guidance, GitHub target, npm target, release boundary, generated scaffold behavior, or automatic-enforcement wording changes.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, package registry publish state, release state, final completion, or future-slice authority.
