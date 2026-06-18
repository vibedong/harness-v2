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
    "harness_v2/preflight.py",
    "harness_v2/mcp.py",
    "tests/test_harness_v2.py",
    "tests/fixtures/valid-task.json",
    "tests/fixtures/invalid-missing-approval.json",
}
ALLOWED_COMMANDS = {
    "python -m compileall harness_v2",
    "python -m unittest discover tests",
    "node bin\\harness-v2.js status --root .",
    "node bin\\harness-v2.js verify tests\\fixtures\\valid-task.json",
    "node bin\\harness-v2.js preflight tests\\fixtures\\valid-task.json --side-effect \"python -m compileall harness_v2\"",
    "node bin\\harness-v2.js mcp < JSON-RPC smoke input",
    "node bin\\harness-v2.js init --root <temporary project>",
    "python -m harness_v2 status --root <repo root>",
    "python -m harness_v2 verify tests\\fixtures\\valid-task.json",
    "python -m harness_v2 preflight tests\\fixtures\\valid-task.json --side-effect \"python -m unittest discover tests\"",
    "python -m harness_v2 mcp < JSON-RPC smoke input",
    "python -m harness_v2 init --root <temporary project>",
    "python -m harness_v2 verify <temporary project>\\contracts\\harness-task.json",
    "npm pack --dry-run",
}
PERMISSION_COMMANDS = {
    "python -m compileall harness_v2",
    "python -m unittest discover tests",
    "node bin\\harness-v2.js status --root .",
    "node bin\\harness-v2.js verify tests\\fixtures\\valid-task.json",
    "node bin\\harness-v2.js preflight tests\\fixtures\\valid-task.json --side-effect \"python -m compileall harness_v2\"",
    "node bin\\harness-v2.js mcp < JSON-RPC smoke input",
    "node bin\\harness-v2.js init --root <temporary project>",
    "python -m harness_v2 status --root <repo root>",
    "python -m harness_v2 verify tests\\fixtures\\valid-task.json",
    "python -m harness_v2 preflight tests\\fixtures\\valid-task.json --side-effect \"python -m unittest discover tests\"",
    "python -m harness_v2 mcp < JSON-RPC smoke input",
    "python -m harness_v2 init --root <temporary project>",
    "python -m harness_v2 verify <temporary project>\\contracts\\harness-task.json",
    "npm pack --dry-run",
}
ALLOWED_GIT_COMMANDS = {
    "git add <intended HARNESS V2 product files>",
    "git commit",
    "git push",
}
EXPECTED_SCAFFOLD_CREATED = {
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
EXPECTED_SCAFFOLD_FILES = {path.replace("\\", "/") for path in EXPECTED_SCAFFOLD_CREATED}
INITIAL_APPROVED_PATHS = {
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
INITIAL_ALLOWED_SIDE_EFFECTS = {
    "local file writes to initial HARNESS V2 scaffold files",
    "local readback of generated HARNESS V2 scaffold files",
    "harness-v2 status --root .",
    "harness-v2 verify contracts\\harness-task.json",
}
INITIAL_DENIED_SIDE_EFFECTS = {
    "dependency install from network",
    "package publish",
    "release execution",
    "secret access",
    "external network mutation",
    "destructive operation",
}
INITIAL_PROOF_OBLIGATIONS = {
    "generated AGENTS/RULES/CURRENT bind AI agents without relying on README authority",
    "harness-v2 status --root .",
    "harness-v2 verify contracts\\harness-task.json",
}
WORKFLOW_STAGES = {
    "planning",
    "approval",
    "development",
    "development_review",
    "artifact_observation",
    "routing",
    "safety_improvement",
    "release_boundary",
}
COMMON_DENIED_SIDE_EFFECTS = [
    "npm publish",
    "Python package registry publish",
    "GitHub release creation",
    "release tag creation",
    "dependency install from network",
    "secret access",
    "external network mutation outside allowed git push",
    "remote MCP hosting",
    "MCP client configuration mutation",
    "destructive operation outside generated verification artifacts",
]
FORBIDDEN_SOURCE_FRAGMENT = "source" + ".fragment.json"
REMOVED_PACKAGE_REGISTRY_ACRONYM = "Py" + "PI"


def generated_file_set(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


def assert_fresh_scaffold_shape(
    case: unittest.TestCase,
    root: Path,
    payload: dict,
    requested_root: Path,
    *,
    redirected: bool = False,
) -> None:
    case.assertEqual(Path(payload["root"]), root.resolve())
    case.assertEqual(Path(payload["requested_root"]), requested_root.resolve())
    case.assertEqual(payload["redirected_from_package_root"], redirected)
    case.assertEqual(set(payload["created"]), EXPECTED_SCAFFOLD_CREATED)
    case.assertEqual(payload["skipped"], [])
    case.assertEqual(payload["overwritten"], [])
    case.assertEqual(generated_file_set(root), EXPECTED_SCAFFOLD_FILES)
    case.assertEqual({path.name for path in root.iterdir() if path.is_dir()}, {"control", "contracts", "templates"})
    for forbidden in ("harness-v2", "harness_v2", "bin", "package.json"):
        case.assertFalse((root / forbidden).exists(), forbidden)


def stage_payload(
    stage: str,
    approved_paths: list[str],
    *,
    allowed_side_effects: list[str] | None = None,
    denied_side_effects: list[str] | None = None,
    source_basis: list[str] | None = None,
    proof_obligations: list[str] | None = None,
    excluded_side_effects: list[str] | None = None,
    target_state: str = "package_publish_review",
) -> dict:
    payload = valid_task_payload()
    payload["task_id"] = f"harness-v2-{stage}-task"
    payload["title"] = f"Validate {stage} workflow stage"
    payload["workflow_stage"] = stage
    payload["source"]["basis"] = source_basis or ["CURRENT.md"]
    payload["approval"]["packet"] = f"Approve exact {stage} workflow stage task"
    payload["approval"]["approved_paths"] = approved_paths
    payload["approval"]["excluded_side_effects"] = excluded_side_effects or list(COMMON_DENIED_SIDE_EFFECTS)
    payload["permission"]["allowed_side_effects"] = allowed_side_effects or ["local readback/search only"]
    payload["permission"]["denied_side_effects"] = denied_side_effects or list(COMMON_DENIED_SIDE_EFFECTS)
    payload["proof"]["obligations"] = proof_obligations or [f"{stage} workflow stage verified"]
    payload["lifecycle"]["target_state"] = target_state
    return payload


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
        self.assertIn("workflow_stage", task_schema["required"])
        self.assertEqual(set(task_schema["properties"]["workflow_stage"]["enum"]), WORKFLOW_STAGES)
        for source_file in APPROVED_SOURCE_FILES:
            content = (ROOT / source_file).read_text()
            self.assertNotIn(FORBIDDEN_SOURCE_FRAGMENT, content)

    def test_workflow_stage_registry_is_exact_eight_stage_contract(self):
        task_schema = json.loads((ROOT / "contracts" / "task.schema.json").read_text())
        workflow_rules = (ROOT / "rules" / "workflows.md").read_text()
        template = (ROOT / "templates" / "task.json").read_text()

        self.assertEqual(set(task_schema["properties"]["workflow_stage"]["enum"]), WORKFLOW_STAGES)
        self.assertIn("<planning|approval|development|development_review|artifact_observation|routing|safety_improvement|release_boundary>", template)
        for heading in (
            "## Planning Workflow",
            "## Approval Workflow",
            "## Development Workflow",
            "## Development Review Workflow",
            "## Artifact Observation Workflow",
            "## Routing Workflow",
            "## Safety And Improvement Workflow",
            "## Release Boundary Workflow",
        ):
            self.assertIn(heading, workflow_rules)

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
        self.assertIn("npm install -g harness-v2@latest", readme)
        self.assertIn("harness-v2 init --root .", readme)
        self.assertIn("harness-v2 apply --root .", readme)
        self.assertIn("What's New In 0.1.5", readme)
        self.assertIn("하네스 업데이트해줘.", readme)
        self.assertIn("Do not create or leave a nested `harness-v2` folder", readme)
        self.assertIn("ships a local stdio MCP adapter", readme)
        self.assertIn("harness-v2 mcp", readme)
        self.assertIn("README.ko.md", readme)
        self.assertIn("# HARNESS V2 사용설명서", korean_readme)
        self.assertIn("npm install -g harness-v2", korean_readme)
        self.assertIn("npm install -g harness-v2@latest", korean_readme)
        self.assertIn("harness-v2 init --root .", korean_readme)
        self.assertIn("0.1.5 업데이트 내용", korean_readme)
        self.assertIn("하네스 업데이트해줘.", korean_readme)
        self.assertIn("프로젝트 안에 `harness-v2` 하위 폴더를 만들거나 남기지 않습니다", korean_readme)
        self.assertIn("local stdio MCP adapter", korean_readme)
        self.assertIn("harness-v2 mcp", korean_readme)
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
        self.assertEqual(json.loads(status.stdout)["workflow"], "remaining_completion_program")
        self.assertEqual(verify.returncode, 0, verify.stderr)
        self.assertEqual(json.loads(verify.stdout)["task_id"], "harness-v2-valid-task")

    def test_cli_preflight_allows_explicit_side_effect_and_write_path(self):
        side_effect = subprocess.run(
            [
                sys.executable,
                "-m",
                "harness_v2",
                "preflight",
                str(VALID_TASK),
                "--side-effect",
                "python -m unittest discover tests",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        write_path = subprocess.run(
            [
                sys.executable,
                "-m",
                "harness_v2",
                "preflight",
                str(VALID_TASK),
                "--path",
                "harness_v2\\preflight.py",
                "--mode",
                "write",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(side_effect.returncode, 0, side_effect.stderr)
        self.assertTrue(json.loads(side_effect.stdout)["ok"])
        self.assertEqual(write_path.returncode, 0, write_path.stderr)
        self.assertTrue(json.loads(write_path.stdout)["ok"])

    def test_cli_preflight_rejects_denied_or_unlisted_side_effects_and_unapproved_path(self):
        denied = subprocess.run(
            [
                sys.executable,
                "-m",
                "harness_v2",
                "preflight",
                str(VALID_TASK),
                "--side-effect",
                "npm publish",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        unlisted = subprocess.run(
            [
                sys.executable,
                "-m",
                "harness_v2",
                "preflight",
                str(VALID_TASK),
                "--side-effect",
                "python -m pip install requests",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        unapproved_path = subprocess.run(
            [
                sys.executable,
                "-m",
                "harness_v2",
                "preflight",
                str(VALID_TASK),
                "--path",
                "outside.md",
                "--mode",
                "write",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(denied.returncode, 1)
        self.assertIn("permission.denied_side_effects", "\n".join(json.loads(denied.stdout)["errors"]))
        self.assertEqual(unlisted.returncode, 1)
        self.assertIn("side effect is not explicitly allowed", "\n".join(json.loads(unlisted.stdout)["errors"]))
        self.assertEqual(unapproved_path.returncode, 1)
        self.assertIn("write path is not approved: outside.md", "\n".join(json.loads(unapproved_path.stdout)["errors"]))

    def test_node_wrapper_delegates_preflight_to_python_cli(self):
        completed = subprocess.run(
            [
                "node",
                "bin/harness-v2.js",
                "preflight",
                "tests/fixtures/valid-task.json",
                "--side-effect",
                "python -m compileall harness_v2",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(json.loads(completed.stdout)["ok"])

    def test_python_mcp_adapter_lists_and_calls_core_tools(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            completed = subprocess.run(
                [sys.executable, "-m", "harness_v2", "mcp"],
                cwd=ROOT,
                input=mcp_input(
                    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}}},
                    {"jsonrpc": "2.0", "method": "notifications/initialized"},
                    {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
                    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "harness_status", "arguments": {"root": "."}}},
                    {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "harness_verify", "arguments": {"task": "tests\\fixtures\\valid-task.json"}}},
                    {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "harness_preflight", "arguments": {"task": "tests\\fixtures\\valid-task.json", "side_effect": "python -m unittest discover tests"}}},
                    {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "harness_init", "arguments": {"root": str(root)}}},
                ),
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stderr, "")
            responses = [json.loads(line) for line in completed.stdout.splitlines()]
            self.assertEqual([response["id"] for response in responses], [1, 2, 3, 4, 5, 6])
            self.assertEqual(responses[0]["result"]["capabilities"], {"tools": {"listChanged": False}})

            tool_names = {tool["name"] for tool in responses[1]["result"]["tools"]}
            self.assertEqual(tool_names, {"harness_status", "harness_verify", "harness_preflight", "harness_init", "harness_apply"})

            status_payload = responses[2]["result"]["structuredContent"]
            verify_payload = responses[3]["result"]["structuredContent"]
            preflight_payload = responses[4]["result"]["structuredContent"]
            init_payload = responses[5]["result"]["structuredContent"]

            self.assertEqual(status_payload["status"]["workflow"], "remaining_completion_program")
            self.assertTrue(verify_payload["ok"])
            self.assertTrue(preflight_payload["ok"])
            assert_fresh_scaffold_shape(self, root, init_payload, root)

    def test_node_wrapper_delegates_mcp_to_python_cli(self):
        completed = subprocess.run(
            ["node", "bin/harness-v2.js", "mcp"],
            cwd=ROOT,
            input=mcp_input(
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}}},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            ),
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        responses = [json.loads(line) for line in completed.stdout.splitlines()]
        self.assertEqual(responses[0]["result"]["serverInfo"]["name"], "harness-v2")
        self.assertIn("harness_preflight", {tool["name"] for tool in responses[1]["result"]["tools"]})

    def test_mcp_adapter_reports_protocol_errors_as_json_rpc(self):
        from harness_v2.mcp import handle_message

        parse_error = handle_message("{")
        unknown_tool = handle_message(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": "missing_tool", "arguments": {}},
                }
            )
        )

        self.assertEqual(parse_error["error"]["code"], -32700)
        self.assertEqual(unknown_tool["error"]["code"], -32602)
        self.assertIn("Unknown tool", unknown_tool["error"]["message"])

    def test_preflight_rejects_invalid_task_contract_before_side_effect(self):
        from harness_v2.preflight import evaluate_preflight

        result = evaluate_preflight(INVALID_TASK, side_effect="local read")

        self.assertFalse(result.ok)
        self.assertIn("task: approval must be an object", "\n".join(result.errors))

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
            payload = json.loads(init.stdout)
            assert_fresh_scaffold_shape(self, root, payload, root)
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
            commands_under_heading(ROOT / "control" / "approval.md", "## Bound Local Verification Commands"),
            ALLOWED_COMMANDS,
        )
        self.assertEqual(
            commands_under_heading(ROOT / "control" / "proof.md", "## Verification Commands"),
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
        self.assertIn("python -m harness_v2 status --root <repo root>", current_commands)

    def test_current_program_surfaces_are_not_stale_third_slice(self):
        current_program_files = [
            ROOT / "AGENTS.md",
            ROOT / "RULES.md",
            ROOT / "CURRENT.md",
            ROOT / "control" / "source.md",
            ROOT / "control" / "approval.md",
            ROOT / "control" / "permission.md",
            ROOT / "control" / "proof.md",
            ROOT / "control" / "lifecycle.md",
            ROOT / "rules" / "workflows.md",
            ROOT / "records" / "README.md",
            ROOT / "routing" / "manifest.md",
            ROOT / "artifacts" / "registry.md",
            ROOT / "artifacts" / "log.md",
            ROOT / "safety" / "regression.md",
            ROOT / "safety" / "improvement.md",
        ]

        for path in current_program_files:
            content = path.read_text()
            self.assertNotIn("status: executable_local_mvp_surface / third_slice", content)
            self.assertNotIn("status: package_github_surface / fourth_slice", content)
        for path in (
            ROOT / "CURRENT.md",
            ROOT / "control" / "approval.md",
            ROOT / "control" / "permission.md",
            ROOT / "control" / "proof.md",
            ROOT / "control" / "lifecycle.md",
            ROOT / "routing" / "manifest.md",
        ):
            self.assertIn("remaining_completion_program", path.read_text())

        root_rules = (ROOT / "RULES.md").read_text()
        self.assertNotIn("Do not create package metadata", root_rules)
        self.assertIn("Windows/macOS npm wrapper metadata", root_rules)
        self.assertIn("Do not perform npm publish", root_rules)

    def test_task_fixtures_match_remaining_completion_program_state(self):
        valid = json.loads(VALID_TASK.read_text())
        invalid = json.loads(INVALID_TASK.read_text())

        self.assertEqual(valid["workflow"], "remaining_completion_program")
        self.assertEqual(valid["workflow_stage"], "development")
        self.assertEqual(valid["lifecycle"]["current_state"], "package_publish_review")
        self.assertEqual(valid["lifecycle"]["target_state"], "package_publish_review")
        self.assertEqual(invalid["workflow"], "remaining_completion_program")
        self.assertEqual(invalid["workflow_stage"], "development")
        self.assertEqual(invalid["lifecycle"]["current_state"], "package_publish_review")
        self.assertEqual(invalid["lifecycle"]["target_state"], "package_publish_review")
        self.assertIn("pyproject.toml", valid["approval"]["approved_paths"])
        self.assertIn("_build_backend\\harness_backend.py", valid["approval"]["approved_paths"])
        self.assertIn("package.json", valid["approval"]["approved_paths"])
        self.assertIn("bin\\harness-v2.js", valid["approval"]["approved_paths"])
        self.assertIn("harness_v2\\mcp.py", valid["approval"]["approved_paths"])
        self.assertIn("node bin\\harness-v2.js status --root .", valid["permission"]["allowed_side_effects"])
        self.assertIn("node bin\\harness-v2.js mcp < JSON-RPC smoke input", valid["permission"]["allowed_side_effects"])
        self.assertIn("python -m harness_v2 mcp < JSON-RPC smoke input", valid["permission"]["allowed_side_effects"])
        self.assertIn("npm pack --dry-run", valid["permission"]["allowed_side_effects"])
        self.assertNotIn("npm publish", valid["permission"]["allowed_side_effects"])
        self.assertIn("npm publish", valid["permission"]["denied_side_effects"])
        self.assertIn("Python package registry publish", valid["permission"]["denied_side_effects"])
        self.assertIn("remote MCP hosting", valid["permission"]["denied_side_effects"])
        self.assertIn("MCP client configuration mutation", valid["permission"]["denied_side_effects"])

    def test_artifact_surfaces_include_package_github_scope(self):
        registry = (ROOT / "artifacts" / "registry.md").read_text()
        log = (ROOT / "artifacts" / "log.md").read_text()
        regression = (ROOT / "safety" / "regression.md").read_text()

        self.assertIn("package-metadata", registry)
        self.assertIn("package-backend", registry)
        self.assertIn("fourth-slice package and GitHub MVP", log)
        self.assertIn("docs/control sync", log)
        self.assertIn("MCP stdio adapter implementation", log)
        self.assertIn("author-local paths copied into GitHub-facing commands", regression)
        self.assertIn("npm wrapper MVP mistaken for npm release", regression)
        self.assertIn("MCP stdio adapter mistaken for source of truth", regression)


    def test_mcp_adapter_is_stdio_wrapper_not_source_of_truth(self):
        readme = (ROOT / "README.md").read_text()
        routing = (ROOT / "routing" / "manifest.md").read_text()
        proof = (ROOT / "control" / "proof.md").read_text()
        improvement = (ROOT / "safety" / "improvement.md").read_text()

        self.assertIn("local stdio MCP adapter", readme)
        self.assertIn("does not replace `CURRENT.md`", readme)
        self.assertIn("MCP stdio adapter", routing)
        self.assertIn("local stdio only", routing)
        self.assertIn("local stdio JSON-RPC adapter", proof)
        self.assertIn("MCP adapter around `status`, `verify`, `preflight`, and `init/apply`", improvement)


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
        self.assertIn("workflow must match CURRENT.md workflow remaining_completion_program", "\n".join(result.errors))

    def test_verifier_rejects_bad_source_pointer_or_missing_current_basis(self):
        from harness_v2.core import validate_task

        bad_pointer = valid_task_payload()
        bad_pointer["source"]["current_pointer"] = "README.md"
        missing_current = valid_task_payload()
        missing_current["source"]["basis"] = ["control\\approval.md"]

        bad_pointer_result = validate_task(bad_pointer, root=ROOT)
        missing_current_result = validate_task(missing_current, root=ROOT)

        self.assertFalse(bad_pointer_result.ok)
        self.assertIn("source.current_pointer must be CURRENT.md", "\n".join(bad_pointer_result.errors))
        self.assertFalse(missing_current_result.ok)
        self.assertIn("source.basis must include CURRENT.md", "\n".join(missing_current_result.errors))

    def test_verifier_rejects_missing_core_denied_side_effects(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["permission"]["denied_side_effects"] = ["npm publish"]

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("permission.denied_side_effects must include denial for: dependency install", "\n".join(result.errors))

    def test_verifier_rejects_missing_or_unknown_workflow_stage(self):
        from harness_v2.core import validate_task

        missing = valid_task_payload()
        del missing["workflow_stage"]
        unknown = valid_task_payload()
        unknown["workflow_stage"] = "unknown_stage"

        missing_result = validate_task(missing, root=ROOT)
        unknown_result = validate_task(unknown, root=ROOT)

        self.assertFalse(missing_result.ok)
        self.assertIn("workflow_stage must be a non-empty string", "\n".join(missing_result.errors))
        self.assertFalse(unknown_result.ok)
        self.assertIn("workflow_stage is not a known stage: unknown_stage", "\n".join(unknown_result.errors))

    def test_verifier_accepts_all_known_workflow_stages(self):
        from harness_v2.core import validate_task

        examples = {
            "planning": stage_payload("planning", ["stage-plans\\candidate.md"]),
            "approval": stage_payload("approval", ["control\\approval.md"]),
            "development": stage_payload(
                "development",
                ["AGENTS.md"],
                allowed_side_effects=["local file writes under F:\\Folder\\harness-v2"],
            ),
            "development_review": stage_payload("development_review", ["records\\README.md"]),
            "artifact_observation": stage_payload(
                "artifact_observation",
                ["artifacts\\registry.md", "artifacts\\log.md"],
            ),
            "routing": stage_payload("routing", ["routing\\manifest.md"]),
            "safety_improvement": stage_payload(
                "safety_improvement",
                ["safety\\regression.md", "safety\\improvement.md"],
            ),
            "release_boundary": stage_payload("release_boundary", ["release\\transaction.md"]),
        }

        for stage, payload in examples.items():
            with self.subTest(stage=stage):
                result = validate_task(payload, root=ROOT)
                self.assertTrue(result.ok, result.errors)

    def test_workflow_stage_engine_rejects_stage_rule_violations(self):
        from harness_v2.core import validate_task

        cases = [
            (
                "planning_product_path",
                stage_payload("planning", ["harness_v2\\core.py"]),
                "planning stage approved path is outside allowed prefixes: harness_v2\\core.py",
            ),
            (
                "planning_mutation",
                stage_payload("planning", ["stage-plans\\candidate.md"], allowed_side_effects=["local file writes"]),
                "planning stage cannot allow mutating side effect: local file writes",
            ),
            (
                "approval_broad_packet",
                {**stage_payload("approval", ["control\\approval.md"]), "approval": {
                    **stage_payload("approval", ["control\\approval.md"])["approval"],
                    "packet": "go ahead",
                    "excluded_side_effects": []
                }},
                "approval stage requires an exact approval packet, not a broad approval phrase",
            ),
            (
                "development_broad_path",
                stage_payload(
                    "development",
                    ["*"],
                    allowed_side_effects=["local file writes under F:\\Folder\\harness-v2"],
                ),
                "approval.approved_paths contains broad path: *",
            ),
            (
                "development_release_execution",
                stage_payload(
                    "development",
                    ["AGENTS.md"],
                    allowed_side_effects=["local file writes under F:\\Folder\\harness-v2", "npm publish"],
                ),
                "development stage cannot allow release execution side effect: npm publish",
            ),
            (
                "development_missing_write",
                stage_payload("development", ["AGENTS.md"], allowed_side_effects=["local readback/search only"]),
                "development stage requires an explicit local write side effect",
            ),
            (
                "development_review_mutation",
                stage_payload("development_review", ["records\\README.md"], allowed_side_effects=["local file writes"]),
                "development_review stage cannot allow mutating side effect: local file writes",
            ),
            (
                "development_review_lifecycle",
                stage_payload("development_review", ["records\\README.md"], target_state="public_release_candidate"),
                "development_review stage cannot move lifecycle state",
            ),
            (
                "development_review_authority_claim",
                stage_payload(
                    "development_review",
                    ["records\\README.md"],
                    proof_obligations=["review findings produce proof result"],
                ),
                "development_review stage cannot claim authority from review/route/artifact material: review findings produce proof result",
            ),
            (
                "artifact_non_artifact_path",
                stage_payload("artifact_observation", ["CURRENT.md"]),
                "artifact_observation stage approved path is outside allowed surface: CURRENT.md",
            ),
            (
                "artifact_source_authority",
                stage_payload(
                    "artifact_observation",
                    ["artifacts\\registry.md"],
                    source_basis=["artifacts\\registry.md"],
                ),
                "artifact_observation stage cannot use artifact registry/log as source authority",
            ),
            (
                "artifact_proof_claim",
                stage_payload(
                    "artifact_observation",
                    ["artifacts\\registry.md"],
                    proof_obligations=["artifact is proof"],
                ),
                "artifact_observation stage cannot claim authority from review/route/artifact material: artifact is proof",
            ),
            (
                "routing_non_routing_path",
                stage_payload("routing", ["CURRENT.md"]),
                "routing stage approved path is outside allowed surface: CURRENT.md",
            ),
            (
                "routing_side_effect",
                stage_payload("routing", ["routing\\manifest.md"], allowed_side_effects=["git push"]),
                "routing stage cannot allow mutating side effect: git push",
            ),
            (
                "routing_permission_claim",
                stage_payload(
                    "routing",
                    ["routing\\manifest.md"],
                    proof_obligations=["route permission granted"],
                ),
                "routing stage cannot claim authority from review/route/artifact material: route permission granted",
            ),
            (
                "safety_product_path",
                stage_payload("safety_improvement", ["harness_v2\\core.py"]),
                "safety_improvement stage approved path is outside allowed surface: harness_v2\\core.py",
            ),
            (
                "safety_mutation",
                stage_payload(
                    "safety_improvement",
                    ["safety\\regression.md"],
                    allowed_side_effects=["local file writes"],
                ),
                "safety_improvement stage cannot allow mutating side effect: local file writes",
            ),
            (
                "release_non_release_path",
                stage_payload("release_boundary", ["CURRENT.md"]),
                "release_boundary stage approved path is outside allowed surface: CURRENT.md",
            ),
            (
                "release_execution",
                stage_payload("release_boundary", ["release\\transaction.md"], allowed_side_effects=["npm publish"]),
                "release_boundary stage cannot allow release execution side effect: npm publish",
            ),
            (
                "release_missing_denial",
                stage_payload(
                    "release_boundary",
                    ["release\\transaction.md"],
                    denied_side_effects=["dependency install from network"],
                ),
                "release_boundary stage requires denied side effect: npm publish",
            ),
        ]

        for name, payload, expected_error in cases:
            with self.subTest(name=name):
                result = validate_task(payload, root=ROOT)
                self.assertFalse(result.ok)
                self.assertIn(expected_error, "\n".join(result.errors))

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
                        "workflow: `remaining_completion_program`",
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

        self.assertEqual(status["workflow"], "remaining_completion_program")
        self.assertEqual(status["state"], "package_publish_review")
        self.assertIn("mcp_stdio_adapter_implementation", status["substate"])
        self.assertIn("goal_g_complete", status["substate"])

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
        self.assertEqual(payload["workflow"], "remaining_completion_program")

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
            assert_fresh_scaffold_shape(self, root, payload, root)

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
            approval = (root / "control" / "approval.md").read_text(encoding="utf-8")
            permission = (root / "control" / "permission.md").read_text(encoding="utf-8")
            proof = (root / "control" / "proof.md").read_text(encoding="utf-8")
            initial_task = json.loads((root / "contracts" / "harness-task.json").read_text(encoding="utf-8"))

            self.assertIn("AI agent entry point", agents)
            self.assertIn("README.md` and `README.ko.md` are user documentation", agents)
            self.assertIn("task-contract validator", agents)
            self.assertIn("CLI helper", agents)
            self.assertIn("not an automatic enforcement sandbox", agents)
            self.assertIn("completion layer", agents)
            self.assertIn("Evidence-Scaled Read Order", agents)
            self.assertIn("Installation, `init`, `apply`, and CLI availability do not approve", agents)
            self.assertIn("active task contract", agents)
            self.assertIn("README files are user-facing documentation only", rules)
            self.assertIn("task-contract validator", rules)
            self.assertIn("not an automatic enforcement sandbox", rules)
            self.assertIn("completion layer", rules)
            self.assertIn("Evidence-Scaled Readback", rules)
            self.assertIn("No one surface substitutes for another", rules)
            self.assertIn("not an automatic enforcement sandbox", current)
            self.assertIn("not_automatic_enforcement_completion", current)
            self.assertIn("does not authorize arbitrary feature work", current)
            self.assertIn("init/apply success", approval)
            self.assertIn("do not grant permission for the next task", permission)
            self.assertIn("installation/init/apply success", proof)

            self.assertEqual(initial_task["source"]["basis"], ["AGENTS.md", "RULES.md", "CURRENT.md"])
            self.assertEqual(set(initial_task["approval"]["approved_paths"]), INITIAL_APPROVED_PATHS)
            self.assertEqual(set(initial_task["approval"]["excluded_side_effects"]), INITIAL_DENIED_SIDE_EFFECTS)
            self.assertEqual(set(initial_task["permission"]["allowed_side_effects"]), INITIAL_ALLOWED_SIDE_EFFECTS)
            self.assertEqual(set(initial_task["permission"]["denied_side_effects"]), INITIAL_DENIED_SIDE_EFFECTS)
            self.assertEqual(set(initial_task["proof"]["obligations"]), INITIAL_PROOF_OBLIGATIONS)
            self.assertEqual(initial_task["workflow_stage"], "development")
            self.assertEqual(initial_task["lifecycle"], {"current_state": "ready", "target_state": "ready"})

            from harness_v2.core import validate_task

            for denied in INITIAL_DENIED_SIDE_EFFECTS:
                mutated = json.loads(json.dumps(initial_task))
                mutated["permission"]["allowed_side_effects"].append(denied)
                result = validate_task(mutated, root=root)
                self.assertFalse(result.ok, denied)
                self.assertIn(f"permission side effect conflicts with denied side effect: {denied}", "\n".join(result.errors))

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
            self.assertEqual(set(payload["created"]), EXPECTED_SCAFFOLD_CREATED)
            self.assertEqual(payload["skipped"], [])
            self.assertEqual(payload["overwritten"], [])
            for relative_path in EXPECTED_SCAFFOLD_CREATED:
                self.assertTrue((project / relative_path).exists(), relative_path)
                self.assertFalse((package_root / relative_path).exists(), relative_path)
            for forbidden_scaffold_dir in ("control", "contracts", "templates"):
                self.assertFalse((package_root / forbidden_scaffold_dir).exists(), forbidden_scaffold_dir)

            status = subprocess.run(
                [sys.executable, "-m", "harness_v2", "status", "--root", str(project)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            verify = subprocess.run(
                [sys.executable, "-m", "harness_v2", "verify", str(project / "contracts" / "harness-task.json")],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertEqual(json.loads(status.stdout)["workflow"], "default")
            self.assertEqual(verify.returncode, 0, verify.stderr)


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


def mcp_input(*messages: dict) -> str:
    return "\n".join(json.dumps(message, separators=(",", ":")) for message in messages) + "\n"


def valid_task_payload() -> dict:
    return json.loads(VALID_TASK.read_text())


def npm_executable() -> str:
    return "npm.cmd" if sys.platform == "win32" else "npm"


if __name__ == "__main__":
    unittest.main()
