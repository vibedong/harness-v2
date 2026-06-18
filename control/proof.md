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
11. `python -m harness_v2 init --root <temporary project>` exits 0;
12. `python -m harness_v2 verify <temporary project>\contracts\harness-task.json` exits 0;
13. `node bin\harness-v2.js init --root <temporary project>` exits 0;
14. `npm pack --dry-run` exits 0 without publishing;
15. `npm publish --dry-run` exits 0;
16. `LICENSE`, `RELEASE_NOTES.md`, and public npm metadata are present;
17. `npm publish` exits 0 for `harness-v2@0.1.3`;
18. `git tag v0.1.3` and `git push origin v0.1.3` succeed;
19. `gh release create v0.1.3 --title "HARNESS V2 0.1.3" --notes-file RELEASE_NOTES.md` succeeds;
20. post-publish fresh install verification succeeds from npm;
21. the unittest suite proves CLI status can run without external dependency;
22. the unittest suite proves the verifier rejects `tests\fixtures\invalid-missing-approval.json`;
23. the unittest suite proves the verifier accepts `tests\fixtures\valid-task.json`;
24. the unittest suite proves doctor reports next action without mutating files;
25. GitHub publish proof names repository URL, branch, and pushed commit;
26. product-local markdown boundaries still deny Python package registry publish, dependency install, secret access, unrelated external network mutation, and destructive operation outside generated verification artifacts.

## Artifact Checks

Readback, search, listing, compile output, unittest output, package smoke output, Node wrapper output, npm dry-run output, CLI output, verifier output, doctor output, git output, and GitHub output are artifact checks. They are evidence material only until evaluated against this proof obligation.

Subagent reports and review findings can help find defects, but they are not proof results by themselves.

## Freshness

Proof evidence becomes stale when target files, write surface, approval scope, permission scope, verifier command, package metadata, npm wrapper metadata, package backend, lifecycle state, route guidance, artifact registry/log contents, safety boundary, improvement classification, GitHub target, npm target, or release boundary changes.

This file does not grant approval, permission, lifecycle state, route permission, regression pass, improvement execution, Python package registry publish state, release state, or future-slice authority.
