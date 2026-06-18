import json
import subprocess
import sys
import tempfile
import zipfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_TASK = ROOT / "tests" / "fixtures" / "valid-task.json"
INVALID_TASK = ROOT / "tests" / "fixtures" / "invalid-missing-approval.json"
APPROVED_SOURCE_FILES = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "RULES.md",
    "CURRENT.md",
    "README.md",
    "README.ko.md",
    "LICENSE",
    "RELEASE_NOTES.md",
    "package.json",
    "pyproject.toml",
    "_build_backend/harness_backend.py",
    "bin/harness-v2.js",
    "rules/workflows.md",
    "control/source.md",
    "control/approval.md",
    "control/permission.md",
    "control/proof.md",
    "control/lifecycle.md",
    "records/README.md",
    "routing/manifest.md",
    "artifacts/registry.md",
    "artifacts/log.md",
    "safety/regression.md",
    "safety/improvement.md",
    "release/transaction.md",
    "contracts/task.schema.json",
    "contracts/approval.schema.json",
    "contracts/permission.schema.json",
    "contracts/proof.schema.json",
    "contracts/lifecycle.schema.json",
    "contracts/artifact.schema.json",
    "templates/task.json",
    "templates/gate-manifest.md",
    "templates/approval-request.md",
    "templates/proof-report.md",
    "harness_v2/__init__.py",
    "harness_v2/__main__.py",
    "harness_v2/cli.py",
    "harness_v2/core.py",
    "harness_v2/verify.py",
    "harness_v2/doctor.py",
    "tests/test_harness_v2.py",
    "tests/fixtures/valid-task.json",
    "tests/fixtures/invalid-missing-approval.json",
}
ALLOWED_COMMANDS = {
    "python -m compileall harness_v2",
    "python -m unittest discover tests",
    "python -m venv <temporary smoke-test venv under TEMP>",
    "<temporary venv>\\Scripts\\python -m pip install --no-deps -e .",
    "<temporary venv>\\Scripts\\python -m harness_v2 status --root <repo root>",
    "<temporary venv>\\Scripts\\python -m harness_v2 verify tests\\fixtures\\valid-task.json",
    "python -m harness_v2 init --root <temporary project>",
    "python -m harness_v2 verify <temporary project>\\contracts\\harness-task.json",
    "node bin\\harness-v2.js status --root .",
    "node bin\\harness-v2.js verify tests\\fixtures\\valid-task.json",
    "node bin\\harness-v2.js init --root <temporary project>",
    "npm pack --dry-run",
    "npm view harness-v2@0.1.5 version dist.tarball",
}
PERMISSION_COMMANDS = {
    "python -m compileall harness_v2",
    "python -m unittest discover tests",
    "python -m venv <temporary smoke-test venv under TEMP>",
    "<temporary venv>\\Scripts\\python -m pip install --no-deps -e .",
    "<temporary venv>\\Scripts\\python -m harness_v2 status --root <repo root>",
    "<temporary venv>\\Scripts\\python -m harness_v2 verify tests\\fixtures\\valid-task.json",
    "python -m harness_v2 init --root <temporary project>",
    "python -m harness_v2 verify <temporary project>\\contracts\\harness-task.json",
    "node bin\\harness-v2.js status --root .",
    "node bin\\harness-v2.js verify tests\\fixtures\\valid-task.json",
    "node bin\\harness-v2.js init --root <temporary project>",
    "npm pack --dry-run",
    "npm view harness-v2@0.1.5 version dist.tarball",
}
ALLOWED_GIT_COMMANDS = {
    "git init",
    "git add <intended HARNESS V2 product files>",
    "git commit",
    "gh repo create vibedong/harness-v2 --public --source . --remote origin",
    "git push -u origin <branch>",
}
FORBIDDEN_SOURCE_FRAGMENT = "source" + ".fragment.json"
REMOVED_PACKAGE_REGISTRY_ACRONYM = "Py" + "PI"


class HarnessV2ExecutableMvpTests(unittest.TestCase):
    def test_approved_source_file_surface_is_exact(self):
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and ".git" not in path.parts
            and path.suffix != ".pyc"
            and ".egg-info" not in "".join(path.parts)
        }

        self.assertEqual(actual, APPROVED_SOURCE_FILES)

    def test_local_build_backend_builds_dependency_free_wheel(self):
        sys.path.insert(0, str(ROOT / "_build_backend"))
        try:
            import harness_backend

            with tempfile.TemporaryDirectory() as wheel_dir:
                wheel_name = harness_backend.build_wheel(wheel_dir)
                wheel_path = Path(wheel_dir) / wheel_name

                self.assertTrue(wheel_path.exists())
                with zipfile.ZipFile(wheel_path) as wheel:
                    names = set(wheel.namelist())

            self.assertIn("harness_v2/cli.py", names)
            self.assertIn("harness_v2/core.py", names)
            self.assertIn("harness_v2-0.1.5.dist-info/METADATA", names)
            self.assertIn("harness_v2-0.1.5.dist-info/entry_points.txt", names)
        finally:
            sys.path.remove(str(ROOT / "_build_backend"))

    def test_local_build_backend_builds_pep660_editable_wheel(self):
        sys.path.insert(0, str(ROOT / "_build_backend"))
        try:
            import harness_backend

            with tempfile.TemporaryDirectory() as wheel_dir:
                wheel_name = harness_backend.build_editable(wheel_dir)
                wheel_path = Path(wheel_dir) / wheel_name

                self.assertTrue(wheel_path.exists())
                self.assertIn("-0.editable-", wheel_name)
                with zipfile.ZipFile(wheel_path) as wheel:
                    names = set(wheel.namelist())
                    pth = wheel.read("harness_v2_editable.pth").decode("utf-8").strip()

            self.assertEqual(pth, str(ROOT))
            self.assertNotIn("harness_v2/cli.py", names)
            self.assertIn("harness_v2-0.1.5.dist-info/METADATA", names)
            self.assertIn("harness_v2-0.1.5.dist-info/entry_points.txt", names)
        finally:
            sys.path.remove(str(ROOT / "_build_backend"))

    def test_task_schema_uses_only_approved_local_schema_files(self):
        task_schema = json.loads((ROOT / "contracts" / "task.schema.json").read_text())
        referenced_schema_names = {
            Path(value).name
            for value in json.dumps(task_schema).split('"')
            if value.startswith("./")
        }

        self.assertLessEqual(
            referenced_schema_names,
            {
                "approval.schema.json",
                "permission.schema.json",
                "proof.schema.json",
                "lifecycle.schema.json",
                "artifact.schema.json",
            },
        )
        for source_file in APPROVED_SOURCE_FILES:
            content = (ROOT / source_file).read_text()
            self.assertNotIn(FORBIDDEN_SOURCE_FRAGMENT, content)

    def test_npm_wrapper_package_metadata_is_dependency_free(self):
        package_json = json.loads((ROOT / "package.json").read_text())

        self.assertEqual(package_json["name"], "harness-v2")
        self.assertEqual(package_json["version"], "0.1.5")
        self.assertEqual(package_json["license"], "MIT")
        self.assertEqual(package_json["bin"], {"harness-v2": "bin/harness-v2.js"})
        self.assertEqual(package_json["os"], ["win32", "darwin"])
        self.assertEqual(package_json["engines"], {"node": ">=18"})
        self.assertEqual(package_json["repository"], {"type": "git", "url": "git+https://github.com/vibedong/harness-v2.git"})
        self.assertEqual(package_json["homepage"], "https://github.com/vibedong/harness-v2#readme")
        self.assertEqual(package_json["bugs"], {"url": "https://github.com/vibedong/harness-v2/issues"})
        self.assertEqual(package_json["author"], "vibedong")
        self.assertIn("workflow", package_json["keywords"])
        self.assertIn("ai", package_json["keywords"])
        self.assertIn("harness", package_json["keywords"])
        self.assertNotIn("dependencies", package_json)
        self.assertNotIn("devDependencies", package_json)
        self.assertNotIn("optionalDependencies", package_json)

        self.assertEqual(
            set(package_json["files"]),
            {
                "AGENTS.md",
                "RULES.md",
                "CURRENT.md",
                "README.md",
                "README.ko.md",
                "LICENSE",
                "RELEASE_NOTES.md",
                "pyproject.toml",
                "_build_backend/*.py",
                "bin/harness-v2.js",
                "harness_v2/*.py",
                "tests/test_harness_v2.py",
                "tests/fixtures/*.json",
                "contracts/*.schema.json",
                "templates/*.json",
                "templates/*.md",
                "control/*.md",
                "rules/*.md",
                "records/README.md",
                "routing/manifest.md",
                "artifacts/*.md",
                "safety/*.md",
                "release/*.md",
            },
        )
        for entry in package_json["files"]:
            self.assertNotIn("__pycache__", entry)
            self.assertNotIn(".pyc", entry)

    def test_public_release_docs_are_present(self):
        license_text = (ROOT / "LICENSE").read_text()
        release_notes = (ROOT / "RELEASE_NOTES.md").read_text()
        readme = (ROOT / "README.md").read_text()
        korean_readme = (ROOT / "README.ko.md").read_text(encoding="utf-8")

        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 vibedong", license_text)
        self.assertIn("# HARNESS V2 0.1.5 Release Notes", release_notes)
        self.assertIn("npm install -g harness-v2", readme)
        self.assertIn("harness-v2 init --root .", readme)
        self.assertIn("harness-v2 apply --root .", readme)
        self.assertIn("README.ko.md", readme)
        self.assertIn("# HARNESS V2 사용설명서", korean_readme)
        self.assertIn("npm install -g harness-v2", korean_readme)
        self.assertIn("harness-v2 init --root .", korean_readme)
        self.assertIn("Python 3.11", readme)
        self.assertIn("Python 3.11", release_notes)
        self.assertIn("NPM_PUBLISHED", release_notes)
        self.assertNotIn(REMOVED_PACKAGE_REGISTRY_ACRONYM, readme)
        self.assertNotIn(REMOVED_PACKAGE_REGISTRY_ACRONYM, korean_readme)
        self.assertNotIn(REMOVED_PACKAGE_REGISTRY_ACRONYM, release_notes)

    def test_release_version_policy_is_consistent(self):
        import harness_v2

        package_json = json.loads((ROOT / "package.json").read_text())

        self.assertEqual(harness_v2.__version__, "0.1.5")
        self.assertEqual(package_json["version"], "0.1.5")
        self.assertIn("0.1.5", (ROOT / "RELEASE_NOTES.md").read_text())

    def test_node_wrapper_delegates_status_and_verify_to_python_cli(self):
        status = subprocess.run(
            ["node", "bin/harness-v2.js", "status", "--root", "."],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        verify = subprocess.run(
            ["node", "bin/harness-v2.js", "verify", "tests/fixtures/valid-task.json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertEqual(json.loads(status.stdout)["workflow"], "package_publish_review")
        self.assertEqual(verify.returncode, 0, verify.stderr)
        self.assertEqual(json.loads(verify.stdout)["task_id"], "harness-v2-valid-task")

    def test_node_wrapper_delegates_init_to_python_cli(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            init = subprocess.run(
                ["node", "bin/harness-v2.js", "init", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            verify = subprocess.run(
                ["node", "bin/harness-v2.js", "verify", str(root / "contracts" / "harness-task.json")],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(init.returncode, 0, init.stderr)
            self.assertIn("contracts\\harness-task.json", json.loads(init.stdout)["created"])
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertEqual(json.loads(verify.stdout)["task_id"], "harness-v2-initial-task")

    def test_npm_pack_dry_run_succeeds_without_publish(self):
        completed = subprocess.run(
            [npm_executable(), "pack", "--dry-run"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("harness-v2-0.1.5.tgz", completed.stdout)
        self.assertNotIn("__pycache__", completed.stdout)
        self.assertNotIn(".pyc", completed.stdout)

    def test_command_authority_lists_only_approved_verification_commands(self):
        self.assertEqual(
            commands_under_heading(ROOT / "CURRENT.md", "## Current Allowed Local Verification Commands"),
            ALLOWED_COMMANDS,
        )
        self.assertEqual(
            commands_under_heading(ROOT / "control" / "permission.md", "## Allowed Local Commands"),
            PERMISSION_COMMANDS,
        )
        self.assertEqual(
            commands_under_heading(ROOT / "control" / "permission.md", "## Allowed Git/GitHub Commands"),
            ALLOWED_GIT_COMMANDS,
        )

    def test_github_facing_commands_are_portable(self):
        readme = (ROOT / "README.md").read_text()
        approval = (ROOT / "control" / "approval.md").read_text()
        permission = (ROOT / "control" / "permission.md").read_text()
        current_commands = commands_under_heading(
            ROOT / "CURRENT.md",
            "## Current Allowed Local Verification Commands",
        )

        self.assertIn("--root .", readme)
        self.assertNotIn("--root F:\\Folder\\harness-v2", readme)
        self.assertNotIn("--root F:\\Folder\\harness-v2", approval)
        self.assertNotIn("--root F:\\Folder\\harness-v2", permission)
        self.assertIn("--root <repo root>", approval)
        self.assertIn("--root <repo root>", permission)
        self.assertIn("<temporary venv>\\Scripts\\python -m harness_v2 status --root <repo root>", current_commands)

    def test_docs_control_sync_surfaces_are_fourth_slice(self):
        synced_files = [
            ROOT / "AGENTS.md",
            ROOT / "RULES.md",
            ROOT / "control" / "source.md",
            ROOT / "control" / "approval.md",
            ROOT / "control" / "permission.md",
            ROOT / "rules" / "workflows.md",
            ROOT / "records" / "README.md",
            ROOT / "routing" / "manifest.md",
            ROOT / "artifacts" / "registry.md",
            ROOT / "artifacts" / "log.md",
            ROOT / "safety" / "regression.md",
            ROOT / "safety" / "improvement.md",
        ]

        for path in synced_files:
            content = path.read_text()
            self.assertIn("status: package_github_surface / fourth_slice", content)
            self.assertNotIn("status: executable_local_mvp_surface / third_slice", content)

        root_rules = (ROOT / "RULES.md").read_text()
        self.assertNotIn("Do not create package metadata", root_rules)
        self.assertIn("Windows/macOS npm wrapper metadata", root_rules)
        self.assertIn("Do not perform npm publish", root_rules)

    def test_task_fixtures_match_package_publish_review_state(self):
        valid = json.loads(VALID_TASK.read_text())
        invalid = json.loads(INVALID_TASK.read_text())

        self.assertEqual(valid["workflow"], "package_publish_review")
        self.assertEqual(valid["lifecycle"]["current_state"], "package_publish_review")
        self.assertEqual(valid["lifecycle"]["target_state"], "package_publish_review")
        self.assertEqual(invalid["workflow"], "package_publish_review")
        self.assertEqual(invalid["lifecycle"]["current_state"], "package_publish_review")
        self.assertEqual(invalid["lifecycle"]["target_state"], "package_publish_review")
        self.assertIn("pyproject.toml", valid["approval"]["approved_paths"])
        self.assertIn("_build_backend\\harness_backend.py", valid["approval"]["approved_paths"])
        self.assertIn("package.json", valid["approval"]["approved_paths"])
        self.assertIn("bin\\harness-v2.js", valid["approval"]["approved_paths"])
        self.assertIn("node bin\\harness-v2.js status --root .", valid["permission"]["allowed_side_effects"])
        self.assertIn("npm pack --dry-run", valid["permission"]["allowed_side_effects"])
        self.assertIn("npm view harness-v2@0.1.5 version dist.tarball", valid["permission"]["allowed_side_effects"])
        self.assertNotIn("npm publish", valid["permission"]["allowed_side_effects"])
        self.assertIn("npm publish", valid["permission"]["denied_side_effects"])
        self.assertIn("Python package registry publish", valid["permission"]["denied_side_effects"])

    def test_artifact_surfaces_include_package_github_scope(self):
        registry = (ROOT / "artifacts" / "registry.md").read_text()
        log = (ROOT / "artifacts" / "log.md").read_text()
        regression = (ROOT / "safety" / "regression.md").read_text()

        self.assertIn("package-metadata", registry)
        self.assertIn("package-backend", registry)
        self.assertIn("fourth-slice package and GitHub MVP", log)
        self.assertIn("docs/control sync", log)
        self.assertIn("author-local paths copied into GitHub-facing commands", regression)
        self.assertIn("npm wrapper MVP mistaken for npm release", regression)


    def test_valid_task_fixture_is_accepted_by_verifier(self):
        from harness_v2.core import validate_task_file

        result = validate_task_file(VALID_TASK)

        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.task_id, "harness-v2-valid-task")

    def test_invalid_task_missing_approval_is_rejected(self):
        from harness_v2.core import validate_task_file

        result = validate_task_file(INVALID_TASK)

        self.assertFalse(result.ok)
        self.assertIn("approval", "\n".join(result.errors))

    def test_verifier_rejects_workflow_mismatch_with_current_pointer(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["workflow"] = "executable_mvp_review"

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("workflow must match CURRENT.md workflow package_publish_review", "\n".join(result.errors))

    def test_verifier_rejects_allowed_and_denied_side_effect_conflict(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["permission"]["allowed_side_effects"].append("Python package registry publish")

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn(
            "permission side effect conflicts with denied side effect: Python package registry publish",
            "\n".join(result.errors),
        )

    def test_verifier_rejects_approval_excluded_side_effect_conflict(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["approval"]["excluded_side_effects"].append("external deployment")
        payload["permission"]["allowed_side_effects"].append("external deployment")

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("permission side effect conflicts with approval exclusion: external deployment", "\n".join(result.errors))

    def test_verifier_rejects_unknown_lifecycle_state(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["lifecycle"]["current_state"] = "unknown_future_state"

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("lifecycle.current_state is not a known state: unknown_future_state", "\n".join(result.errors))

    def test_verifier_rejects_author_local_status_command_root(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["permission"]["allowed_side_effects"].append(
            "<temporary venv>\\Scripts\\python -m harness_v2 status --root F:\\Folder\\harness-v2"
        )

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("status command must use --root <repo root> or --root .", "\n".join(result.errors))

    def test_verifier_rejects_stale_status_surface(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            (root / "CURRENT.md").write_text(
                "\n".join(
                    [
                        "workflow: `package_publish_review`",
                        "state: `package_publish_review`",
                        "substate: `test`",
                    ]
                ),
                encoding="utf-8",
            )
            control = root / "control"
            control.mkdir()
            (control / "source.md").write_text(
                "status: executable_local_mvp_surface / third_slice / source_control\n",
                encoding="utf-8",
            )

            result = validate_task(payload, root=root)

        self.assertFalse(result.ok)
        self.assertIn("stale status surface: control/source.md", "\n".join(result.errors))

    def test_status_reads_current_workflow_pointer(self):
        from harness_v2.core import read_current_status

        status = read_current_status(ROOT)

        self.assertEqual(status["workflow"], "package_publish_review")
        self.assertEqual(status["state"], "package_publish_review")
        self.assertIn("npm_only", status["substate"])

    def test_doctor_reports_next_action_without_mutation(self):
        from harness_v2.doctor import inspect_project

        report = inspect_project(ROOT)

        self.assertEqual(report["mutation"], "none")
        self.assertEqual(report["release_ready"], False)
        self.assertIn("next_action", report)

    def test_cli_status_outputs_json_without_external_dependency(self):
        completed = subprocess.run(
            [sys.executable, "-m", "harness_v2", "status", "--root", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["workflow"], "package_publish_review")

    def test_cli_verify_accepts_valid_and_rejects_invalid_fixture(self):
        accepted = subprocess.run(
            [sys.executable, "-m", "harness_v2", "verify", str(VALID_TASK)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        rejected = subprocess.run(
            [sys.executable, "-m", "harness_v2", "verify", str(INVALID_TASK)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("approval", rejected.stderr)

    def test_cli_init_applies_harness_to_empty_project(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            init = subprocess.run(
                [sys.executable, "-m", "harness_v2", "init", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(init.returncode, 0, init.stderr)
            payload = json.loads(init.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["initial_task"], "contracts\\harness-task.json")

            expected_paths = {
                "AGENTS.md",
                "RULES.md",
                "CURRENT.md",
                "control\\source.md",
                "control\\approval.md",
                "control\\permission.md",
                "control\\proof.md",
                "control\\lifecycle.md",
                "contracts\\harness-task.json",
                "templates\\task.json",
            }
            self.assertTrue(expected_paths.issubset(set(payload["created"])))
            for relative_path in expected_paths:
                self.assertTrue((root / relative_path).exists(), relative_path)

            status = subprocess.run(
                [sys.executable, "-m", "harness_v2", "status", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            verify = subprocess.run(
                [sys.executable, "-m", "harness_v2", "verify", str(root / "contracts" / "harness-task.json")],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertEqual(json.loads(status.stdout)["workflow"], "default")
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertEqual(json.loads(verify.stdout)["task_id"], "harness-v2-initial-task")

            agents = (root / "AGENTS.md").read_text(encoding="utf-8")
            rules = (root / "RULES.md").read_text(encoding="utf-8")
            current = (root / "CURRENT.md").read_text(encoding="utf-8")

            self.assertIn("AI agent entry point", agents)
            self.assertIn("README.md` and `README.ko.md` are user documentation", agents)
            self.assertIn("Installation alone does not approve arbitrary work", agents)
            self.assertIn("README files are user-facing documentation only", rules)
            self.assertIn("No one surface substitutes for another", rules)
            self.assertIn("does not authorize arbitrary feature work", current)

    def test_cli_apply_alias_is_idempotent_without_force(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            subprocess.run(
                [sys.executable, "-m", "harness_v2", "init", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            custom_agents = "# Custom AGENTS\n\nKeep this file.\n"
            (root / "AGENTS.md").write_text(custom_agents, encoding="utf-8")

            applied = subprocess.run(
                [sys.executable, "-m", "harness_v2", "apply", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(applied.returncode, 0, applied.stderr)
            payload = json.loads(applied.stdout)
            self.assertIn("AGENTS.md", payload["skipped"])
            self.assertEqual((root / "AGENTS.md").read_text(encoding="utf-8"), custom_agents)

    def test_cli_init_from_package_checkout_applies_to_parent_project(self):
        with tempfile.TemporaryDirectory() as temp_root:
            project = Path(temp_root)
            package_root = project / "harness-v2"
            (package_root / "harness_v2").mkdir(parents=True)
            (package_root / "bin").mkdir()
            (package_root / "package.json").write_text(
                json.dumps({"name": "harness-v2", "version": "0.0.0"}),
                encoding="utf-8",
            )
            (package_root / "harness_v2" / "core.py").write_text("# marker\n", encoding="utf-8")
            (package_root / "bin" / "harness-v2.js").write_text("// marker\n", encoding="utf-8")

            init = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    (
                        "import sys; "
                        f"sys.path.insert(0, {str(ROOT)!r}); "
                        "from harness_v2.cli import main; "
                        "raise SystemExit(main(['init', '--root', '.']))"
                    ),
                ],
                cwd=package_root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(init.returncode, 0, init.stderr)
            payload = json.loads(init.stdout)
            self.assertEqual(Path(payload["root"]), project.resolve())
            self.assertEqual(Path(payload["requested_root"]), package_root.resolve())
            self.assertTrue(payload["redirected_from_package_root"])
            self.assertTrue((project / "AGENTS.md").exists())
            self.assertTrue((project / "contracts" / "harness-task.json").exists())
            self.assertFalse((package_root / "AGENTS.md").exists())


def commands_under_heading(path: Path, heading: str) -> set[str]:
    lines = path.read_text().splitlines()
    inside = False
    commands = set()
    for line in lines:
        if line.startswith("## "):
            inside = line.strip() == heading
            continue
        if inside and line.strip().startswith("- `") and line.strip().endswith("`"):
            commands.add(line.strip()[3:-1])
    return commands


def valid_task_payload() -> dict:
    return json.loads(VALID_TASK.read_text())


def npm_executable() -> str:
    return "npm.cmd" if sys.platform == "win32" else "npm"


if __name__ == "__main__":
    unittest.main()
