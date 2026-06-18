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
    "pyproject.toml",
    "_build_backend/harness_backend.py",
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
}
PERMISSION_COMMANDS = {
    "python -m compileall harness_v2",
    "python -m unittest discover tests",
    "python -m venv <temporary smoke-test venv under TEMP>",
    "<temporary venv>\\Scripts\\python -m pip install --no-deps -e .",
    "<temporary venv>\\Scripts\\python -m harness_v2 status --root F:\\Folder\\harness-v2",
    "<temporary venv>\\Scripts\\python -m harness_v2 verify tests\\fixtures\\valid-task.json",
}
ALLOWED_GIT_COMMANDS = {
    "git init",
    "git add <intended HARNESS V2 product files>",
    "git commit",
    "gh repo create vibedong/harness-v2 --public --source . --remote origin",
    "git push -u origin <branch>",
}
FORBIDDEN_SOURCE_FRAGMENT = "source" + ".fragment.json"


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
            self.assertIn("harness_v2-0.1.0.dist-info/METADATA", names)
            self.assertIn("harness_v2-0.1.0.dist-info/entry_points.txt", names)
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
            self.assertIn("harness_v2-0.1.0.dist-info/METADATA", names)
            self.assertIn("harness_v2-0.1.0.dist-info/entry_points.txt", names)
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
        current_commands = commands_under_heading(
            ROOT / "CURRENT.md",
            "## Current Allowed Local Verification Commands",
        )

        self.assertIn("--root .", readme)
        self.assertNotIn("--root F:\\Folder\\harness-v2", readme)
        self.assertIn("<temporary venv>\\Scripts\\python -m harness_v2 status --root <repo root>", current_commands)

    def test_docs_control_sync_surfaces_are_fourth_slice(self):
        synced_files = [
            ROOT / "AGENTS.md",
            ROOT / "RULES.md",
            ROOT / "routing" / "manifest.md",
            ROOT / "artifacts" / "registry.md",
            ROOT / "artifacts" / "log.md",
            ROOT / "safety" / "regression.md",
        ]

        for path in synced_files:
            content = path.read_text()
            self.assertIn("status: package_github_surface / fourth_slice", content)
            self.assertNotIn("status: executable_local_mvp_surface / third_slice", content)

        root_rules = (ROOT / "RULES.md").read_text()
        self.assertNotIn("Do not create package metadata", root_rules)
        self.assertIn("Package metadata, local editable install verification, and GitHub repository push", root_rules)

    def test_artifact_surfaces_include_package_github_scope(self):
        registry = (ROOT / "artifacts" / "registry.md").read_text()
        log = (ROOT / "artifacts" / "log.md").read_text()
        regression = (ROOT / "safety" / "regression.md").read_text()

        self.assertIn("package-metadata", registry)
        self.assertIn("package-backend", registry)
        self.assertIn("fourth-slice package and GitHub MVP", log)
        self.assertIn("docs/control sync", log)
        self.assertIn("author-local paths copied into GitHub-facing commands", regression)


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

    def test_status_reads_current_workflow_pointer(self):
        from harness_v2.core import read_current_status

        status = read_current_status(ROOT)

        self.assertEqual(status["workflow"], "package_publish_review")
        self.assertEqual(status["state"], "package_publish_review")
        self.assertIn("not_pypi", status["substate"])

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


if __name__ == "__main__":
    unittest.main()
