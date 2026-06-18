# HARNESS V2 Proof Control

status: package_github_surface / fourth_slice / proof_control

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the fourth-slice package, GitHub publish, npm wrapper surface, and current `0.1.5` npm publish slice, verify after authoring:

1. all product source changes are under `F:\Folder\harness-v2`;
2. package metadata and build backend install in editable mode without dependency installation;
3. no non-source generated package artifacts remain under `F:\Folder\harness-v2` after cleanup;
4. `python -m compileall harness_v2` exits 0;
5. `python -m unittest discover tests` exits 0;
6. local package smoke install accepts the source package with `--no-deps -e .`;
7. installed package smoke can run `harness_v2 status`;
8. installed package smoke can verify `tests\fixtures\valid-task.json`;
9. `node bin\harness-v2.js status --root .` exits 0;
10. `node bin\harness-v2.js verify tests\fixtures\valid-task.json` exits 0;
11. `python -m harness_v2 init --root <temporary project>` exits 0;
12. `python -m harness_v2 verify <temporary project>\contracts\harness-task.json` exits 0;
13. `node bin\harness-v2.js init --root <temporary project>` exits 0;
14. `npm pack --dry-run` exits 0 without publishing;
15. `npm publish --dry-run` exits 0;
16. `LICENSE`, `RELEASE_NOTES.md`, and public npm metadata are present;
17. npm registry readback reports `harness-v2@0.1.5`;
19. the unittest suite proves init-generated AI-facing scaffold text separates README documentation from AI authority;
20. the unittest suite proves CLI status can run without external dependency;
21. the unittest suite proves the verifier rejects `tests\fixtures\invalid-missing-approval.json`;
22. the unittest suite proves the verifier accepts `tests\fixtures\valid-task.json`;
23. the unittest suite proves doctor reports next action without mutating files;
24. GitHub publish proof names repository URL, branch, and pushed commit;
25. product-local markdown boundaries still deny npm publish, Python package registry publish, dependency install, secret access, release tag creation, GitHub release execution, unrelated external network mutation, and destructive operation outside generated verification artifacts.

## Artifact Checks

Readback, search, listing, compile output, unittest output, package smoke output, Node wrapper output, npm dry-run output, CLI output, verifier output, doctor output, git output, and GitHub output are artifact checks. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Freshness

Proof evidence becomes stale when target files, write surface, approval scope, permission scope, verifier command, package metadata, npm wrapper metadata, package backend, lifecycle state, route guidance, artifact registry/log contents, safety boundary, improvement classification, GitHub target, npm target, or release boundary changes.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, Python package registry publish state, release state, or future-slice authority.
