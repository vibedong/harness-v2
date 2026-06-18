# HARNESS V2 Proof Control

status: package_github_surface / fourth_slice / proof_control

This file separates proof obligation, artifact check, and proof result.

## Current Proof Obligation

For the fourth-slice package, GitHub publish, and npm wrapper surface, verify after authoring:

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
11. `npm pack --dry-run` exits 0 without publishing;
12. the unittest suite proves CLI status can run without external dependency;
13. the unittest suite proves the verifier rejects `tests\fixtures\invalid-missing-approval.json`;
14. the unittest suite proves the verifier accepts `tests\fixtures\valid-task.json`;
15. the unittest suite proves doctor reports next action without mutating files;
16. GitHub publish proof names repository URL, branch, and pushed commit;
17. product-local markdown boundaries still deny npm publish, PyPI publish, release execution, dependency install, secret access, unrelated external network mutation, and destructive operation outside generated verification artifacts.

## Artifact Checks

Readback, search, listing, compile output, unittest output, package smoke output, Node wrapper output, npm dry-run output, CLI output, verifier output, doctor output, git output, and GitHub output are artifact checks. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Freshness

Proof evidence becomes stale when target files, write surface, approval scope, permission scope, verifier command, package metadata, npm wrapper metadata, package backend, lifecycle state, route guidance, artifact registry/log contents, safety boundary, improvement classification, GitHub target, npm target, or release boundary changes.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, PyPI publish state, release state, or future-slice authority.
