import json
import hashlib
import subprocess
import sys
import tempfile
import zipfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_TASK = ROOT / "tests" / "fixtures" / "valid-task.json"
INVALID_TASK = ROOT / "tests" / "fixtures" / "invalid-missing-approval.json"
INVALID_GATE_MISMATCH = ROOT / "tests" / "fixtures" / "invalid-gate-mismatch.json"
INVALID_RECORD_STRENGTH = ROOT / "tests" / "fixtures" / "invalid-record-strength.json"
VALID_APPROVAL_DECISION = ROOT / "tests" / "fixtures" / "valid-approval-decision.json"
INVALID_BROAD_APPROVAL = ROOT / "tests" / "fixtures" / "invalid-broad-approval.json"
VALID_PROOF_RECEIPT = ROOT / "tests" / "fixtures" / "valid-proof-receipt.json"
INVALID_STALE_PROOF_RECEIPT = ROOT / "tests" / "fixtures" / "invalid-stale-proof-receipt.json"
APPROVED_SOURCE_FILES = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "RULES.md",
    "CURRENT.md",
    "README.md",
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
    "contracts/gate-state.schema.json",
    "contracts/transition.schema.json",
    "contracts/freshness.schema.json",
    "contracts/approval-decision.schema.json",
    "contracts/permission-decision.schema.json",
    "contracts/proof-receipt.schema.json",
    "contracts/task.schema.json",
    "contracts/approval.schema.json",
    "contracts/permission.schema.json",
    "contracts/proof.schema.json",
    "contracts/lifecycle.schema.json",
    "contracts/artifact.schema.json",
    "templates/task.json",
    "templates/gate-state.json",
    "templates/transition-log.md",
    "templates/freshness-map.json",
    "templates/approval-decision.json",
    "templates/permission-decision.json",
    "templates/proof-receipt.json",
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
    "harness_v2/gate.py",
    "harness_v2/lifecycle.py",
    "harness_v2/layout.py",
    "harness_v2/freshness.py",
    "harness_v2/modes.py",
    "harness_v2/decisions.py",
    "harness_v2/mcp.py",
    "tests/test_harness_v2.py",
    "tests/fixtures/valid-task.json",
    "tests/fixtures/invalid-missing-approval.json",
    "tests/fixtures/invalid-gate-mismatch.json",
    "tests/fixtures/valid-transition-log.md",
    "tests/fixtures/invalid-transition-stale-approval.md",
    "tests/fixtures/invalid-stale-approval.json",
    "tests/fixtures/invalid-stale-proof.json",
    "tests/fixtures/invalid-record-strength.json",
    "tests/fixtures/valid-approval-decision.json",
    "tests/fixtures/invalid-broad-approval.json",
    "tests/fixtures/valid-proof-receipt.json",
    "tests/fixtures/invalid-stale-proof-receipt.json",
}
ALLOWED_COMMANDS = {
    "python -m compileall harness_v2",
    "python -m unittest discover tests",
    "node bin\\harness-v2.js status --root .",
    "node bin\\harness-v2.js verify tests\\fixtures\\valid-task.json",
    "node bin\\harness-v2.js preflight tests\\fixtures\\valid-task.json --side-effect \"python -m compileall harness_v2\"",
    "node bin\\harness-v2.js gate tests\\fixtures\\valid-task.json --root . --side-effect \"python -m compileall harness_v2\"",
    "node bin\\harness-v2.js doctor --root .",
    "node bin\\harness-v2.js mcp < JSON-RPC smoke input",
    "node bin\\harness-v2.js init --root <temporary project>",
    "python -m harness_v2 status --root <repo root>",
    "python -m harness_v2 verify tests\\fixtures\\valid-task.json",
    "python -m harness_v2 preflight tests\\fixtures\\valid-task.json --side-effect \"python -m unittest discover tests\"",
    "python -m harness_v2 gate tests\\fixtures\\valid-task.json --root . --side-effect \"python -m unittest discover tests\"",
    "python -m harness_v2 doctor --root <repo root>",
    "python -m harness_v2 mcp < JSON-RPC smoke input",
    "python -m harness_v2 init --root <temporary project>",
    "python -m harness_v2 verify <temporary project>\\contracts\\harness-task.json",
    "npm pack --dry-run",
}
GOAL6_COMMANDS = {
    "python -m compileall harness_v2",
    "python -m unittest discover tests",
    "python -m harness_v2 status --root .",
    "python -m harness_v2 verify tests\\fixtures\\valid-task.json",
    "python -m harness_v2 gate tests\\fixtures\\valid-task.json --root .",
    "python -m harness_v2 doctor --root .",
    "node bin\\harness-v2.js status --root .",
    "node bin\\harness-v2.js verify tests\\fixtures\\valid-task.json",
    "node bin\\harness-v2.js gate tests\\fixtures\\valid-task.json --root .",
    "node bin\\harness-v2.js doctor --root .",
    "npm pack --dry-run",
}
PERMISSION_COMMANDS = GOAL6_COMMANDS
ALLOWED_GIT_COMMANDS = {
    "git add <intended Goal 6 product files>",
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
    "records\\README.md",
    "records\\current-task.md",
    "records\\stages\\spec.md",
    "records\\stages\\spec-review.md",
    "records\\stages\\plan.md",
    "records\\stages\\plan-review.md",
    "records\\stages\\plan-approval.md",
    "records\\stages\\development.md",
    "records\\stages\\development-review.md",
    "records\\stages\\improvement.md",
    "records\\decisions.md",
    "records\\proof.md",
    "records\\handoff.md",
    "contracts\\harness-task.json",
    "templates\\task.json",
}
EXPECTED_SCAFFOLD_FILES = {path.replace("\\", "/") for path in EXPECTED_SCAFFOLD_CREATED}
INITIAL_APPROVED_PATHS = {
    "records\\current-task.md",
    "records\\stages\\spec.md",
    "records\\decisions.md",
}
INITIAL_ALLOWED_SIDE_EFFECTS = {
    "local file writes to records\\current-task.md",
    "local file writes to records\\stages\\spec.md",
    "local file writes to records\\decisions.md",
    "local readback of generated HARNESS V2 scaffold files",
    "harness-v2 status --root .",
    "harness-v2 verify contracts\\harness-task.json",
    "harness-v2 gate contracts\\harness-task.json --root .",
    "harness-v2 doctor --root .",
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
    "generated records/stages scaffold tracks spec through improvement",
    "harness-v2 status --root .",
    "harness-v2 verify contracts\\harness-task.json",
    "harness-v2 gate contracts\\harness-task.json --root .",
    "harness-v2 doctor --root .",
}
WORKFLOW_STAGES = {
    "spec",
    "spec_review",
    "plan",
    "plan_review",
    "plan_approval",
    "development",
    "development_review",
    "improvement",
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
    case.assertEqual({path.name for path in root.iterdir() if path.is_dir()}, {"control", "contracts", "records", "templates"})
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
    target_state: str = "workflow_realignment_review",
) -> dict:
    payload = valid_task_payload()
    payload["task_id"] = f"harness-v2-{stage}-task"
    payload["title"] = f"Validate {stage} workflow stage"
    payload["workflow_stage"] = stage
    payload["current_gate"] = stage
    payload["source"]["basis"] = source_basis or ["CURRENT.md"]
    payload["record_density"]["required_read_set_size"] = len(payload["source"]["basis"])
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
            self.assertIn("harness_v2-0.1.12.dist-info/METADATA", names)
            self.assertIn("harness_v2-0.1.12.dist-info/entry_points.txt", names)
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
            self.assertIn("harness_v2-0.1.12.dist-info/METADATA", names)
            self.assertIn("harness_v2-0.1.12.dist-info/entry_points.txt", names)
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
        self.assertIn("<spec|spec_review|plan|plan_review|plan_approval|development|development_review|improvement>", template)
        for heading in (
            "## Spec Workflow",
            "## Spec Review Workflow",
            "## Plan Workflow",
            "## Plan Review Workflow",
            "## Plan Approval Workflow",
            "## Development Workflow",
            "## Development Review Workflow",
            "## Improvement Workflow",
        ):
            self.assertIn(heading, workflow_rules)

    def test_records_index_uses_canonical_plan_stage_names(self):
        records = (ROOT / "records" / "README.md").read_text(encoding="utf-8")

        self.assertIn("| `plan` | `records\\stages\\plan.md` |", records)
        self.assertIn("| `plan_approval` | `records\\stages\\plan-approval.md` |", records)
        self.assertNotIn("| `planning` |", records)
        self.assertNotIn("| `approval` |", records)

    def test_artifact_log_does_not_reintroduce_legacy_stage_aliases(self):
        log = (ROOT / "artifacts" / "log.md").read_text(encoding="utf-8")

        self.assertIn("spec", log)
        self.assertIn("plan_approval", log)
        self.assertNotIn("planning", log)
        self.assertNotIn("approval ->", log)

    def test_generated_scaffold_path_inventory_matches_current_init_surface(self):
        expected_generated_paths = {
            "AGENTS.md",
            "RULES.md",
            "CURRENT.md",
            "control\\source.md",
            "control\\approval.md",
            "control\\permission.md",
            "control\\proof.md",
            "control\\lifecycle.md",
            "contracts\\harness-task.json",
            "records\\README.md",
            "records\\current-task.md",
            "records\\decisions.md",
            "records\\proof.md",
            "records\\handoff.md",
            "records\\stages\\spec.md",
            "records\\stages\\spec-review.md",
            "records\\stages\\plan.md",
            "records\\stages\\plan-review.md",
            "records\\stages\\plan-approval.md",
            "records\\stages\\development.md",
            "records\\stages\\development-review.md",
            "records\\stages\\improvement.md",
            "templates\\task.json",
        }
        source_only_paths = {
            "routing\\manifest.md",
            "artifacts\\registry.md",
            "artifacts\\log.md",
            "safety\\regression.md",
            "release\\transaction.md",
            "records\\gate-state.json",
            "records\\freshness-map.json",
            "templates\\gate-state.json",
            "templates\\freshness-map.json",
        }

        self.assertEqual(EXPECTED_SCAFFOLD_CREATED, expected_generated_paths)
        self.assertTrue(expected_generated_paths.isdisjoint(source_only_paths))

    def test_generated_scaffold_documents_hybrid_planning_workflow(self):
        from harness_v2.core import initialize_project

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            result = initialize_project(root)

            self.assertTrue(result.ok, result.errors)
            current = (root / "CURRENT.md").read_text(encoding="utf-8")
            task = json.loads((root / "contracts" / "harness-task.json").read_text(encoding="utf-8"))
            self.assertIn("spec", current)
            self.assertIn("plan_approval", current)
            self.assertIn("artifact_observation", current)
            self.assertIn("workflow stage가 아니라 control 또는 관찰 표면", current)
            self.assertEqual(task["workflow_stage"], "spec")
            self.assertEqual(task["current_gate"], "spec")
            self.assertIn("approval", task)
            self.assertIn("permission", task)
            self.assertIn("proof", task)
            self.assertIn("lifecycle", task)

    def test_hybrid_workflow_forbidden_wording_absent(self):
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [
                ROOT / "rules" / "workflows.md",
                ROOT / "templates" / "task.json",
                ROOT / "README.md",
            ]
        )

        self.assertNotIn("artifact_observation is a workflow stage", text)
        self.assertNotIn("routing is a workflow stage", text)
        self.assertNotIn("release_boundary is a workflow stage", text)

    def test_artifact_surfaces_separate_stage_and_domain_owner_language(self):
        manifest = (ROOT / "routing" / "manifest.md").read_text(encoding="utf-8")
        improvement = (ROOT / "safety" / "improvement.md").read_text(encoding="utf-8")

        self.assertIn("domain:improvement", manifest + improvement)
        self.assertNotIn("domain owner is a workflow stage", manifest + improvement)

    def test_authority_control_docs_and_schemas_state_evidence_carrier_boundary(self):
        control_paths = [
            ROOT / "control" / "approval.md",
            ROOT / "control" / "permission.md",
            ROOT / "control" / "proof.md",
            ROOT / "control" / "lifecycle.md",
        ]
        schema_paths = [
            ROOT / "contracts" / "approval.schema.json",
            ROOT / "contracts" / "permission.schema.json",
            ROOT / "contracts" / "proof.schema.json",
            ROOT / "contracts" / "lifecycle.schema.json",
        ]

        for path in control_paths:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertIn("evidence carrier, not authority generator", text)
        for path in schema_paths:
            with self.subTest(path=path):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("evidence carrier, not authority generator", schema["description"])

    def test_current_layout_paths_are_centralized(self):
        from harness_v2.layout import CURRENT_LAYOUT_VERSION, HarnessLayout

        layout = HarnessLayout()

        self.assertEqual(CURRENT_LAYOUT_VERSION, "legacy-control-records-v1")
        self.assertEqual(layout.task_contract.as_posix(), "contracts/harness-task.json")
        self.assertEqual(layout.gate_state.as_posix(), "records/gate-state.json")
        self.assertEqual(layout.freshness_map.as_posix(), "records/freshness-map.json")
        self.assertEqual(layout.lifecycle_control.as_posix(), "control/lifecycle.md")
        self.assertEqual(layout.current_pointer.as_posix(), "CURRENT.md")

    def test_missing_layout_version_uses_current_legacy_layout(self):
        from harness_v2.core import validate_task
        from harness_v2.layout import CURRENT_LAYOUT_VERSION

        payload = valid_task_payload()
        payload.pop("layout_version", None)

        result = validate_task(payload, root=ROOT)

        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.layout_version, CURRENT_LAYOUT_VERSION)
        self.assertTrue(result.layout_report["current_layout_paths_active"])
        self.assertFalse(result.layout_report["domain_layout_enabled"])
        self.assertFalse(result.layout_report["domain_layout_candidate"])

    def test_known_layout_version_uses_current_legacy_layout(self):
        from harness_v2.core import validate_task
        from harness_v2.layout import CURRENT_LAYOUT_VERSION

        payload = valid_task_payload()
        payload["layout_version"] = CURRENT_LAYOUT_VERSION

        result = validate_task(payload, root=ROOT)

        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.layout_version, CURRENT_LAYOUT_VERSION)
        self.assertEqual(result.layout_report["layout_version"], CURRENT_LAYOUT_VERSION)

    def test_unknown_layout_version_fails_with_migration_diagnostic(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["layout_version"] = "domain-v99"

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("unknown layout_version", "\n".join(result.errors))

    def test_status_and_doctor_report_current_layout_fields(self):
        from harness_v2.core import read_current_status
        from harness_v2.doctor import inspect_project
        from harness_v2.layout import CURRENT_LAYOUT_VERSION

        status = read_current_status(ROOT)
        doctor = inspect_project(ROOT)

        for payload in (status, doctor):
            with self.subTest(payload=payload):
                self.assertEqual(payload["layout_version"], CURRENT_LAYOUT_VERSION)
                self.assertTrue(payload["current_layout_paths_active"])
                self.assertFalse(payload["domain_layout_enabled"])
                self.assertFalse(payload["domain_layout_candidate"])

    def test_domain_layout_migration_report_exposes_current_read_only_fields(self):
        from harness_v2.layout import CURRENT_LAYOUT_VERSION, domain_layout_migration_report

        report = domain_layout_migration_report()

        self.assertEqual(
            set(report),
            {
                "current_layout_version",
                "generated_scaffold_paths",
                "source_package_surfaces",
                "runtime_lookup_paths",
                "domain_layout_candidate",
                "migration_required",
                "migration_blockers",
            },
        )
        self.assertEqual(report["current_layout_version"], CURRENT_LAYOUT_VERSION)
        self.assertEqual(
            set(report["generated_scaffold_paths"]),
            {path.replace("\\", "/") for path in EXPECTED_SCAFFOLD_CREATED},
        )
        self.assertIn("AGENTS.md", report["generated_scaffold_paths"])
        self.assertIn("contracts/harness-task.json", report["generated_scaffold_paths"])
        self.assertIn("harness_v2/layout.py", report["source_package_surfaces"])
        self.assertEqual(
            report["runtime_lookup_paths"],
            {
                "task_contract": "contracts/harness-task.json",
                "gate_state": "records/gate-state.json",
                "freshness_map": "records/freshness-map.json",
                "lifecycle_control": "control/lifecycle.md",
                "current_pointer": "CURRENT.md",
            },
        )
        self.assertFalse(report["domain_layout_candidate"])
        self.assertFalse(report["migration_required"])
        self.assertEqual(report["migration_blockers"], [])

    def test_domain_layout_report_is_read_only(self):
        from harness_v2.core import initialize_project
        from harness_v2.doctor import inspect_project

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            init = initialize_project(root)
            self.assertTrue(init.ok, init.errors)

            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            report = inspect_project(root)
            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))

        self.assertEqual(before, after)
        self.assertEqual(report["mutation"], "none")
        self.assertFalse(report["domain_layout_candidate"])
        migration = report["domain_layout_migration"]
        self.assertEqual(migration["current_layout_version"], "legacy-control-records-v1")
        self.assertFalse(migration["domain_layout_candidate"])
        self.assertFalse(migration["migration_required"])
        self.assertEqual(migration["migration_blockers"], [])

    def test_npm_wrapper_package_metadata_is_dependency_free(self):
        package_json = json.loads((ROOT / "package.json").read_text())

        self.assertEqual(package_json["name"], "harness-v2")
        self.assertEqual(package_json["version"], "0.1.12")
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
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        current = (ROOT / "CURRENT.md").read_text(encoding="utf-8")

        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 vibedong", license_text)
        self.assertIn("## HARNESS V2 0.1.12 릴리스 노트", release_notes)
        self.assertIn("이 README는 사람을 위한 제품 설명서입니다", readme)
        self.assertIn("npm install -g harness-v2", readme)
        self.assertIn("npm install -g harness-v2@latest", readme)
        self.assertIn("GitHub 저장소를 프로젝트 폴더에 clone하지 않습니다", readme)
        self.assertIn("git clone https://github.com/vibedong/harness-v2.git .", readme)
        self.assertIn("HARNESS V2 소스 체크아웃", readme)
        self.assertIn("HARNESS V2는 Codex 앱에서 프로젝트 작업을 시작할 때 AI가 현재 작업 경계", readme)
        self.assertIn("이 프로젝트에 HARNESS V2 적용해줘.", readme)
        self.assertIn("vibedong/harness-v2 기준으로 이 프로젝트에 HARNESS V2 적용해줘.", readme)
        self.assertIn("이 프로젝트에 하네스 설치해줘.", readme)
        self.assertIn("https://github.com/vibedong/harness-v2 이 프로젝트에 하네스 설치해줘.", readme)
        self.assertIn("링크는 어떤 하네스를 설치할지 알려주는 식별자입니다", readme)
        self.assertIn("현재 프로젝트 폴더에 clone하라는 뜻이 아닙니다", readme)
        self.assertIn("GitHub clone하지 말고 현재 프로젝트 루트에 scaffold만 적용합니다", readme)
        self.assertIn("status`, `verify`, `gate`, `doctor` 결과를 확인합니다", readme)
        self.assertIn("harness-v2 init --root .", readme)
        self.assertIn("harness-v2 apply --root .", readme)
        self.assertIn("harness-v2 task start --root .", readme)
        self.assertIn("실제 작업 요청 등록", readme)
        self.assertIn("scope_pending", readme)
        self.assertIn("0.1.12 업데이트 내용", readme)
        self.assertIn("하네스 업데이트해줘.", readme)
        self.assertIn("중첩된 `harness-v2` 폴더를 만들거나 남겨두지 마세요", readme)
        self.assertIn("local stdio MCP adapter", readme)
        self.assertIn("harness-v2 mcp", readme)
        self.assertIn("harness-v2 gate", readme)
        self.assertIn("hook-equivalent gate", readme)
        self.assertIn("shell이나 editor를 자동으로 차단하지 않습니다", readme)
        self.assertIn("shell이나 editor를 자동으로 차단하지 않습니다", readme)
        self.assertIn("Python 3.11", readme)
        self.assertIn("Python 3.11", release_notes)
        self.assertIn("NPM_PUBLISHED", release_notes)
        self.assertIn("새 프로젝트 scaffold 검증", readme)
        self.assertIn("새 프로젝트 scaffold 검증", current)
        self.assertIn("대상 프로젝트 루트 바로 아래", readme)
        self.assertIn("중첩된 `harness-v2` 소스 폴더", readme)
        self.assertNotIn(REMOVED_PACKAGE_REGISTRY_ACRONYM, readme)
        self.assertNotIn(REMOVED_PACKAGE_REGISTRY_ACRONYM, release_notes)

    def test_readme_tracks_current_update_status(self):
        package_json = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        current = (ROOT / "CURRENT.md").read_text(encoding="utf-8")

        self.assertIn("## README 업데이트 기록 유지 원칙", readme)
        self.assertIn(f"## {package_json['version']} 업데이트 내용", readme)
        self.assertIn("사용자가 체감하는 변경은 README의 업데이트 내용에 함께 남깁니다", readme)
        self.assertIn("README 업데이트 내용 없이 release, package, scaffold, workflow 변경을 완료로 말하지 않습니다", readme)
        self.assertIn("local unreleased task binding 업데이트", readme)
        self.assertIn("records\\stages\\spec.md`도 현재 사용자 요청으로 갱신", readme)
        self.assertIn("README 업데이트 기록 유지", current)

    def test_readme_task_contract_examples_match_goal0_contract(self):
        from harness_v2.core import validate_task

        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertNotIn('"workflow": "package_publish_review"', readme)
        example = _json_block_after(readme, '"task_id": "readme-docs-update"')
        result = validate_task(json.loads(example), root=ROOT)

        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.current_gate, "development")
        self.assertFalse(result.compatibility_mode)
        self.assertEqual(result.record_strength, "light")
        self.assertEqual(result.effective_record_strength, "strict")

    def test_release_version_policy_is_consistent(self):
        import harness_v2

        package_json = json.loads((ROOT / "package.json").read_text())

        pyproject = (ROOT / "pyproject.toml").read_text()

        self.assertEqual(harness_v2.__version__, "0.1.12")
        self.assertEqual(package_json["version"], "0.1.12")
        self.assertIn('version = "0.1.12"', pyproject)
        self.assertIn("0.1.12", (ROOT / "RELEASE_NOTES.md").read_text())

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
        verify_payload = json.loads(verify.stdout)
        self.assertEqual(verify_payload["task_id"], "harness-v2-valid-task")
        self.assertEqual(verify_payload["current_gate"], "development")
        self.assertEqual(verify_payload["task_mode"], "planned_change")
        self.assertEqual(verify_payload["record_strength"], "light")
        self.assertEqual(verify_payload["effective_record_strength"], "strict")
        self.assertTrue(verify_payload["classification_required"])
        self.assertFalse(verify_payload["compatibility_mode"])
        self.assertEqual(verify_payload["mode_profile"]["strength_inputs"]["classification_required"], "strict")

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
                "harness_v2\\core.py",
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

    def test_cli_gate_accepts_valid_task_status_and_preflight_checks(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "harness_v2",
                "gate",
                str(VALID_TASK),
                "--root",
                ".",
                "--side-effect",
                "python -m unittest discover tests",
                "--path",
                "harness_v2\\core.py",
                "--mode",
                "write",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["ok"])
        self.assertTrue(payload["hook_equivalent"])
        self.assertFalse(payload["automatic_enforcement"])
        self.assertEqual(payload["task_id"], "harness-v2-valid-task")
        self.assertEqual(payload["status"]["workflow"], "remaining_completion_program")
        self.assertTrue(payload["verify"]["ok"])
        self.assertEqual(len(payload["preflight"]), 1)
        self.assertTrue(payload["preflight"][0]["ok"])

    def test_cli_gate_rejects_denied_side_effect_and_unapproved_write_path(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "harness_v2",
                "gate",
                str(VALID_TASK),
                "--root",
                ".",
                "--side-effect",
                "npm publish",
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

        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stdout)
        self.assertFalse(payload["ok"])
        errors = "\n".join(payload["errors"])
        self.assertIn("permission.denied_side_effects", errors)
        self.assertIn("write path is not approved: outside.md", errors)

    def test_node_wrapper_delegates_gate_to_python_cli(self):
        completed = subprocess.run(
            [
                "node",
                "bin/harness-v2.js",
                "gate",
                "tests/fixtures/valid-task.json",
                "--root",
                ".",
                "--side-effect",
                "python -m compileall harness_v2",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["ok"])
        self.assertTrue(payload["hook_equivalent"])
        self.assertFalse(payload["automatic_enforcement"])

    def test_node_wrapper_delegates_doctor_to_python_cli(self):
        completed = subprocess.run(
            ["node", "bin/harness-v2.js", "doctor", "--root", "."],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["mutation"], "none")
        self.assertEqual(payload["release_boundary"]["status"], "closed")
        self.assertIn("gate", payload["integrated_surfaces"])

    def test_python_mcp_adapter_lists_and_calls_core_tools(self):
        with tempfile.TemporaryDirectory() as temp_root, tempfile.TemporaryDirectory() as decision_root:
            root = Path(temp_root)
            decision_path = Path(decision_root) / "valid-proof-receipt.json"
            decision_path.write_text(json.dumps(fresh_proof_receipt_payload()), encoding="utf-8")
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
                    {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "harness_gate", "arguments": {"task": "tests\\fixtures\\valid-task.json", "root": ".", "side_effects": ["python -m unittest discover tests"]}}},
                    {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "harness_init", "arguments": {"root": str(root)}}},
                    {"jsonrpc": "2.0", "id": 8, "method": "tools/call", "params": {"name": "harness_decision", "arguments": {"record": str(decision_path), "task": "tests\\fixtures\\valid-task.json", "root": "."}}},
                ),
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(completed.stderr, "")
            responses = [json.loads(line) for line in completed.stdout.splitlines()]
            self.assertEqual([response["id"] for response in responses], [1, 2, 3, 4, 5, 6, 7, 8])
            self.assertEqual(responses[0]["result"]["capabilities"], {"tools": {"listChanged": False}})

            tool_names = {tool["name"] for tool in responses[1]["result"]["tools"]}
            self.assertEqual(tool_names, {"harness_status", "harness_verify", "harness_preflight", "harness_gate", "harness_decision", "harness_init", "harness_apply"})

            status_payload = responses[2]["result"]["structuredContent"]
            verify_payload = responses[3]["result"]["structuredContent"]
            preflight_payload = responses[4]["result"]["structuredContent"]
            gate_payload = responses[5]["result"]["structuredContent"]
            init_payload = responses[6]["result"]["structuredContent"]
            decision_payload = responses[7]["result"]["structuredContent"]

            self.assertEqual(status_payload["status"]["workflow"], "remaining_completion_program")
            self.assertTrue(verify_payload["ok"])
            self.assertEqual(verify_payload["current_gate"], "development")
            self.assertEqual(verify_payload["task_mode"], "planned_change")
            self.assertEqual(verify_payload["record_strength"], "light")
            self.assertEqual(verify_payload["effective_record_strength"], "strict")
            self.assertTrue(verify_payload["classification_required"])
            self.assertFalse(verify_payload["compatibility_mode"])
            self.assertEqual(verify_payload["mode_profile"]["proof_profile"], "current")
            self.assertIn("freshness", verify_payload)
            self.assertFalse(verify_payload["freshness"]["present"])
            self.assertTrue(preflight_payload["ok"])
            self.assertTrue(gate_payload["ok"])
            self.assertTrue(gate_payload["hook_equivalent"])
            assert_fresh_scaffold_shape(self, root, init_payload, root)
            self.assertTrue(decision_payload["ok"], decision_payload["errors"])
            self.assertEqual(decision_payload["kind"], "ProofReceipt")

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
        tool_names = {tool["name"] for tool in responses[1]["result"]["tools"]}
        self.assertIn("harness_preflight", tool_names)
        self.assertIn("harness_gate", tool_names)
        self.assertIn("harness_decision", tool_names)

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
        self.assertIn("harness-v2-0.1.12.tgz", completed.stdout)
        self.assertNotIn("__pycache__", completed.stdout)
        self.assertNotIn(".pyc", completed.stdout)

    def test_command_authority_lists_only_approved_verification_commands(self):
        self.assertEqual(
            commands_under_heading(ROOT / "CURRENT.md", "## 현재 허용된 Local Verification Commands"),
            ALLOWED_COMMANDS,
        )
        self.assertEqual(
            commands_under_heading(ROOT / "control" / "approval.md", "## Bound Local Verification Commands"),
            GOAL6_COMMANDS,
        )
        self.assertEqual(
            commands_under_heading(ROOT / "control" / "proof.md", "## Verification Commands"),
            GOAL6_COMMANDS,
        )
        self.assertEqual(
            commands_under_heading(ROOT / "control" / "permission.md", "## 허용된 Local Commands"),
            PERMISSION_COMMANDS,
        )
        self.assertEqual(
            commands_under_heading(ROOT / "control" / "permission.md", "## 허용된 Git/GitHub Commands"),
            ALLOWED_GIT_COMMANDS,
        )

    def test_github_facing_commands_are_portable(self):
        readme = (ROOT / "README.md").read_text()
        approval = (ROOT / "control" / "approval.md").read_text()
        permission = (ROOT / "control" / "permission.md").read_text()
        current_commands = commands_under_heading(
            ROOT / "CURRENT.md",
            "## 현재 허용된 Local Verification Commands",
        )

        self.assertIn("--root .", readme)
        self.assertNotIn("--root F:\\Folder\\harness-v2", readme)
        self.assertNotIn("--root F:\\Folder\\harness-v2", approval)
        self.assertNotIn("--root F:\\Folder\\harness-v2", permission)
        self.assertIn("--root .", approval)
        self.assertIn("--root .", permission)
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
        for path in (
            ROOT / "control" / "approval.md",
            ROOT / "control" / "permission.md",
            ROOT / "control" / "proof.md",
            ROOT / "control" / "lifecycle.md",
        ):
            content = path.read_text()
            self.assertIn("whole_plan_conformance_audit", content)
            self.assertNotIn("The active Goal is Goal 3", content)
            self.assertNotIn("verified Goal 3 commit", content)

        root_rules = (ROOT / "RULES.md").read_text()
        self.assertNotIn("Do not create package metadata", root_rules)
        self.assertIn("Windows/macOS npm wrapper metadata", root_rules)
        self.assertIn("npm publish", root_rules)
        self.assertIn("수행하지 않습니다", root_rules)

    def test_task_fixtures_match_remaining_completion_program_state(self):
        valid = json.loads(VALID_TASK.read_text())
        invalid = json.loads(INVALID_TASK.read_text())

        self.assertEqual(valid["workflow"], "remaining_completion_program")
        self.assertEqual(valid["workflow_stage"], "development")
        self.assertEqual(valid["contract_version"], "0.1.8")
        self.assertEqual(valid["task_mode"], "planned_change")
        self.assertEqual(valid["record_strength"], "light")
        self.assertEqual(valid["proof_profile"], "current")
        self.assertTrue(valid["classification_required"])
        self.assertEqual(valid["lifecycle"]["current_state"], "workflow_realignment_review")
        self.assertEqual(valid["lifecycle"]["target_state"], "workflow_realignment_review")
        self.assertEqual(invalid["workflow"], "remaining_completion_program")
        self.assertEqual(invalid["workflow_stage"], "development")
        self.assertEqual(invalid["lifecycle"]["current_state"], "workflow_realignment_review")
        self.assertEqual(invalid["lifecycle"]["target_state"], "workflow_realignment_review")
        self.assertIn("contracts\\task.schema.json", valid["approval"]["approved_paths"])
        self.assertIn("templates\\task.json", valid["approval"]["approved_paths"])
        self.assertIn("harness_v2\\core.py", valid["approval"]["approved_paths"])
        self.assertIn("harness_v2\\cli.py", valid["approval"]["approved_paths"])
        self.assertIn("harness_v2\\modes.py", valid["approval"]["approved_paths"])
        self.assertIn("harness_v2\\mcp.py", valid["approval"]["approved_paths"])
        self.assertIn("tests\\fixtures\\invalid-record-strength.json", valid["approval"]["approved_paths"])
        self.assertIn("python -m harness_v2 doctor --root .", valid["permission"]["allowed_side_effects"])
        self.assertIn("node bin\\harness-v2.js doctor --root .", valid["permission"]["allowed_side_effects"])
        self.assertNotIn("npm publish", valid["permission"]["allowed_side_effects"])
        self.assertIn("npm publish", valid["permission"]["denied_side_effects"])
        self.assertIn("Python package registry publish", valid["permission"]["denied_side_effects"])
        self.assertIn("release execution", valid["permission"]["denied_side_effects"])

    def test_artifact_surfaces_include_package_github_scope(self):
        registry = (ROOT / "artifacts" / "registry.md").read_text()
        log = (ROOT / "artifacts" / "log.md").read_text()
        regression = (ROOT / "safety" / "regression.md").read_text()

        self.assertIn("package-metadata", registry)
        self.assertIn("package-backend", registry)
        self.assertIn("fourth-slice package and GitHub MVP", log)
        self.assertIn("docs/control sync", log)
        self.assertIn("MCP stdio adapter implementation", log)
        self.assertIn("hook-equivalent gate hardening", log)
        self.assertIn("author-local paths copied into GitHub-facing commands", regression)
        self.assertIn("npm wrapper MVP mistaken for npm release", regression)
        self.assertIn("MCP stdio adapter mistaken for source of truth", regression)
        self.assertIn("hook-equivalent gate mistaken for a real shell/editor blocker", regression)

    def test_goal6_classification_and_release_boundary_are_honest(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        release = (ROOT / "release" / "transaction.md").read_text()
        release_notes = (ROOT / "RELEASE_NOTES.md").read_text()
        lifecycle = (ROOT / "control" / "lifecycle.md").read_text()

        for content in (readme, lifecycle):
            self.assertIn("workflow_binding_engine", content)
        self.assertIn("shell이나 editor", readme)
        self.assertIn("shell/editor hook", lifecycle)
        self.assertIn("명시적인 CLI, MCP, task contract 표면", readme)
        self.assertIn("사람을 위한 제품 설명서", readme)
        self.assertIn("closed release target", release)
        self.assertIn("closed release history", release.casefold())
        self.assertNotIn("current release transaction allows", release.casefold())
        self.assertIn("npm publish 1회", release)
        self.assertIn("GitHub release creation 또는 mutation", release)
        self.assertIn(
            "`spec`, `spec_review`, `plan`, `plan_review`, `plan_approval`, `development`, `development_review`, `improvement`",
            release_notes,
        )
        self.assertNotIn("`planning`, `plan_review`, `approval`", release_notes)

    def test_mcp_adapter_is_stdio_wrapper_not_source_of_truth(self):
        readme = (ROOT / "README.md").read_text()
        routing = (ROOT / "routing" / "manifest.md").read_text()
        proof = (ROOT / "control" / "proof.md").read_text()
        improvement = (ROOT / "safety" / "improvement.md").read_text()

        self.assertIn("local stdio MCP adapter", readme)
        self.assertIn("`CURRENT.md`, task contract, approval, permission, proof, lifecycle, release boundary를 대체하지 않습니다", readme)
        self.assertIn("decision", readme)
        self.assertIn("MCP stdio adapter", routing)
        self.assertIn("local stdio only", routing)
        self.assertIn("decision", routing)
        self.assertIn("MCP wrapper behavior", proof)
        self.assertIn("MCP adapter around `status`, `verify`, `preflight`, `gate`, `decision`, `init/apply`", improvement)

    def test_hook_equivalent_gate_is_not_claimed_as_real_shell_or_editor_hook(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        routing = (ROOT / "routing" / "manifest.md").read_text()
        proof = (ROOT / "control" / "proof.md").read_text()
        lifecycle = (ROOT / "control" / "lifecycle.md").read_text()
        improvement = (ROOT / "safety" / "improvement.md").read_text()

        for content in (readme, routing, proof, lifecycle, improvement):
            self.assertIn("hook-equivalent gate", content)
        self.assertIn("harness_gate", routing)
        self.assertIn("직접 연결되는 Codex app hook 표면은 없습니다", readme)
        self.assertIn("shell이나 editor를 자동으로 차단하지 않습니다", readme)
        self.assertIn("shell이나 editor를 자동으로 차단하지 않습니다", readme)


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

    def test_verifier_rejects_control_surfaces_as_workflow_stages(self):
        from harness_v2.core import validate_task

        for stage in ("artifact_observation", "routing", "safety_improvement", "release_boundary"):
            with self.subTest(stage=stage):
                payload = valid_task_payload()
                payload["workflow_stage"] = stage

                result = validate_task(payload, root=ROOT)

                self.assertFalse(result.ok)
                self.assertIn(f"workflow_stage is not a known stage: {stage}", "\n".join(result.errors))

    def test_domain_owner_names_are_not_accepted_as_workflow_stages(self):
        from harness_v2.core import validate_task

        owner_names = [
            "task",
            "source",
            "workflow",
            "approval",
            "permission",
            "proof",
            "lifecycle",
            "route",
            "artifact",
            "inventory",
            "regression",
            "domain:improvement",
            "release",
            "contract",
            "artifact_observation",
            "safety_improvement",
            "release_boundary",
        ]
        for owner_name in owner_names:
            with self.subTest(owner_name=owner_name):
                payload = valid_task_payload()
                payload["workflow_stage"] = owner_name

                result = validate_task(payload, root=ROOT)

                self.assertFalse(result.ok, owner_name)
                errors = "\n".join(result.errors)
                if owner_name == "approval":
                    self.assertIn("workflow_stage uses legacy alias 'approval'; use 'plan_approval'", errors)
                else:
                    self.assertIn("workflow_stage is not a known stage", errors)
                    self.assertIn("workflow_stage is a responsibility/domain owner, not a workflow stage", errors)

    def test_domain_owner_names_are_not_accepted_as_current_gate_values(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["current_gate"] = "domain:improvement"

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("current_gate is not a known stage: domain:improvement", "\n".join(result.errors))
        self.assertIn("current_gate is a responsibility/domain owner, not a workflow stage: domain:improvement", "\n".join(result.errors))

    def test_folder_existence_does_not_satisfy_decision_or_receipt_requirements(self):
        from harness_v2.core import validate_task

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "CURRENT.md").write_text(
                "\n".join(
                    [
                        "workflow: `remaining_completion_program`",
                        "state: `workflow_realignment_review`",
                        "substate: `authority-negative-test`",
                    ]
                ),
                encoding="utf-8",
            )
            for name in ["approval", "permission", "proof", "lifecycle"]:
                (root / name).mkdir()
            task = valid_task_payload()
            task["approval"].pop("approved_paths", None)

            result = validate_task(task, root=root)

        self.assertFalse(result.ok)
        self.assertIn("approval.approved_paths is required", "\n".join(result.errors))

    def test_registry_and_log_rows_do_not_satisfy_authority_records(self):
        from harness_v2.core import validate_task

        task = valid_task_payload()
        task["permission"]["allowed_side_effects"] = ["git push"]
        task["approval"]["excluded_side_effects"] = ["git push"]
        task["proof"]["obligations"] = [
            "artifact registry row proves approval",
            "artifact log row grants permission",
        ]

        result = validate_task(task, root=ROOT)

        self.assertFalse(result.ok)
        errors = "\n".join(result.errors)
        self.assertIn("permission side effect is excluded by approval: git push", errors)
        self.assertIn(
            "authority carrier cannot substitute for approval, permission, proof, or lifecycle transition: artifact registry row proves approval",
            errors,
        )
        self.assertIn(
            "authority carrier cannot substitute for approval, permission, proof, or lifecycle transition: artifact log row grants permission",
            errors,
        )

    def test_verifier_rejects_legacy_stage_aliases_with_migration_diagnostic(self):
        from harness_v2.core import validate_task

        aliases = {"planning": "plan", "approval": "plan_approval"}
        for legacy_stage, canonical_stage in aliases.items():
            with self.subTest(legacy_stage=legacy_stage):
                payload = valid_task_payload()
                payload["workflow_stage"] = legacy_stage

                result = validate_task(payload, root=ROOT)

                self.assertFalse(result.ok)
                self.assertIn(
                    f"workflow_stage uses legacy alias {legacy_stage!r}; use {canonical_stage!r}",
                    "\n".join(result.errors),
                )

    def test_goal0_compatibility_derives_current_gate_and_record_defaults(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["contract_version"] = "0.1.7"
        payload.pop("task_mode", None)
        payload.pop("record_strength", None)
        payload.pop("current_gate", None)
        payload.pop("risk_flags", None)
        payload.pop("proof_profile", None)
        payload.pop("capability_request", None)
        payload.pop("classification_required", None)

        result = validate_task(payload, root=ROOT)

        self.assertTrue(result.ok, result.errors)
        self.assertTrue(result.compatibility_mode)
        self.assertEqual(result.current_gate, "development")
        self.assertEqual(result.task_mode, "planned_change")
        self.assertEqual(result.record_strength, "light")
        self.assertEqual(result.effective_record_strength, "strict")

    def test_goal0_rejects_current_gate_mismatch(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["current_gate"] = "plan"

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("current_gate must match workflow_stage when present", "\n".join(result.errors))

    def test_goal0_strict_contract_requires_mode_and_record_strength(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        payload["contract_version"] = "0.1.8"
        payload.pop("task_mode", None)
        payload.pop("record_strength", None)

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        errors = "\n".join(result.errors)
        self.assertIn("strict task contracts require task_mode", errors)
        self.assertIn("strict task contracts require record_strength", errors)

    def test_goal4_task_schema_template_and_fixture_cover_mode_fields(self):
        schema = json.loads((ROOT / "contracts" / "task.schema.json").read_text(encoding="utf-8"))
        template = json.loads((ROOT / "templates" / "task.json").read_text(encoding="utf-8"))
        valid = valid_task_payload()

        for field in ("risk_flags", "proof_profile", "capability_request", "classification_required", "record_density"):
            self.assertIn(field, schema["properties"])
            self.assertIn(field, template)
            self.assertIn(field, valid)
        self.assertEqual(template["contract_version"], "0.1.8")
        self.assertEqual(valid["contract_version"], "0.1.8")
        self.assertEqual(valid["record_density"]["required_read_set_size"], len(valid["source"]["basis"]))
        self.assertEqual(valid["record_density"]["field_presence"], "strict")

    def test_goal4_mode_engine_computes_stage_defaults_and_risk_escalation(self):
        from harness_v2.modes import evaluate_mode

        base = {
            "task_mode": "planned_change",
            "record_strength": "minimal",
            "risk_flags": [],
            "proof_profile": "none",
            "capability_request": [],
            "classification_required": False,
            "source": {"basis": ["CURRENT.md"]},
            "approval": {"approved_paths": []},
            "permission": {"allowed_side_effects": []},
            "proof": {"obligations": ["not_required"]},
            "lifecycle": {"current_state": "ready", "target_state": "ready"},
            "record_density": {
                "generated_file_count": 0,
                "required_read_set_size": 1,
                "field_presence": "strict",
            },
        }

        development = evaluate_mode(base, "development", compatibility_mode=False)
        plan = evaluate_mode(base, "plan", compatibility_mode=False)
        plan_review = evaluate_mode(base, "plan_review", compatibility_mode=False)
        risky = evaluate_mode({**base, "classification_required": True, "risk_flags": ["ambiguous_scope"]}, "development", compatibility_mode=False)
        stale = evaluate_mode(base, "development", compatibility_mode=False, freshness={"stale": [{"anchor_id": "a"}], "errors": []})

        self.assertEqual(development.effective_record_strength, "light")
        self.assertEqual(plan.effective_record_strength, "light")
        self.assertEqual(plan_review.effective_record_strength, "strict")
        self.assertEqual(risky.effective_record_strength, "strict")
        self.assertEqual(risky.strength_inputs["classification_required"], "strict")
        self.assertEqual(stale.effective_record_strength, "strict")
        self.assertEqual(stale.strength_inputs["stale_status"], "strict")

    def test_goal4_invalid_record_strength_fixture_is_rejected(self):
        from harness_v2.core import validate_task_file

        result = validate_task_file(INVALID_RECORD_STRENGTH)

        self.assertFalse(result.ok)
        self.assertIn("record_strength is not known: medium", "\n".join(result.errors))

    def test_goal4_record_density_denies_read_only_write_shortcut(self):
        from harness_v2.core import validate_task
        from harness_v2.modes import evaluate_mode

        read_only = {
            "task_id": "harness-v2-read-only-analysis",
            "title": "Read-only HARNESS V2 audit",
            "workflow": "remaining_completion_program",
            "contract_version": "0.1.8",
            "workflow_stage": "development",
            "current_gate": "development",
            "task_mode": "read_only_analysis",
            "record_strength": "light",
            "risk_flags": [],
            "proof_profile": "none",
            "capability_request": [],
            "classification_required": False,
            "record_density": {
                "generated_file_count": 0,
                "required_read_set_size": 2,
                "field_presence": "light",
            },
            "source": {
                "basis": ["CURRENT.md", "README.md"],
                "current_pointer": "CURRENT.md",
            },
            "approval": {
                "packet": "Approve read-only audit of README surface",
                "approved_paths": ["README.md"],
                "excluded_side_effects": list(COMMON_DENIED_SIDE_EFFECTS),
            },
            "permission": {
                "allowed_side_effects": ["local readback/search only"],
                "denied_side_effects": list(COMMON_DENIED_SIDE_EFFECTS),
            },
            "proof": {
                "obligations": ["not_required"],
            },
            "lifecycle": {
                "current_state": "workflow_realignment_review",
                "target_state": "workflow_realignment_review",
            },
        }
        read_only_result = validate_task(read_only, root=ROOT)

        self.assertTrue(read_only_result.ok, read_only_result.errors)
        self.assertEqual(read_only_result.effective_record_strength, "light")
        self.assertEqual(read_only_result.mode_profile["strength_inputs"]["write_surface"], "minimal")

        payload = valid_task_payload()
        payload["task_mode"] = "read_only_analysis"
        payload["record_strength"] = "light"

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("read_only_analysis task_mode cannot allow mutating side effects", "\n".join(result.errors))

        docs_only = evaluate_mode(
            {
                "task_mode": "read_only_analysis",
                "record_strength": "light",
                "risk_flags": [],
                "proof_profile": "none",
                "capability_request": [],
                "classification_required": False,
                "source": {"basis": ["CURRENT.md"]},
                "approval": {"approved_paths": ["README.md"]},
                "permission": {"allowed_side_effects": ["local readback/search only"]},
                "proof": {"obligations": ["not_required"]},
                "lifecycle": {"current_state": "ready", "target_state": "ready"},
                "record_density": {
                    "generated_file_count": 0,
                    "required_read_set_size": 1,
                    "field_presence": "light",
                },
            },
            "development",
            compatibility_mode=False,
        )

        self.assertEqual(docs_only.errors, ())

    def test_goal4_strict_contract_requires_record_density_fields(self):
        from harness_v2.core import validate_task

        payload = valid_task_payload()
        for key in ("risk_flags", "proof_profile", "capability_request", "classification_required", "record_density"):
            payload.pop(key, None)

        result = validate_task(payload, root=ROOT)

        self.assertFalse(result.ok)
        errors = "\n".join(result.errors)
        self.assertIn("strict task contracts require risk_flags", errors)
        self.assertIn("strict task contracts require proof_profile", errors)
        self.assertIn("strict task contracts require capability_request", errors)
        self.assertIn("strict task contracts require classification_required", errors)
        self.assertIn("strict task contracts require record_density", errors)

    def test_goal4_record_density_rejects_shortcuts(self):
        from harness_v2.core import validate_task

        read_set = valid_task_payload()
        read_set["record_density"]["required_read_set_size"] = len(read_set["source"]["basis"]) + 1
        read_set_result = validate_task(read_set, root=ROOT)

        generated = valid_task_payload()
        generated["task_mode"] = "scaffold_only"
        generated["record_density"]["generated_file_count"] = len(generated["approval"]["approved_paths"]) + 1
        generated_result = validate_task(generated, root=ROOT)

        field_presence = valid_task_payload()
        field_presence["record_density"]["field_presence"] = "minimal"
        field_presence_result = validate_task(field_presence, root=ROOT)

        capability = valid_task_payload()
        capability["capability_request"] = ""
        capability_result = validate_task(capability, root=ROOT)

        self.assertIn("record_density.required_read_set_size cannot exceed source.basis count", "\n".join(read_set_result.errors))
        self.assertIn("record_density.generated_file_count cannot exceed approval.approved_paths count", "\n".join(generated_result.errors))
        self.assertIn("record_density.field_presence must be at least effective_record_strength", "\n".join(field_presence_result.errors))
        self.assertIn("capability_request must be a non-empty string when present", "\n".join(capability_result.errors))

    def test_goal5_decision_schema_template_and_fixture_surfaces_exist(self):
        for stem in ("approval-decision", "permission-decision", "proof-receipt"):
            schema = json.loads((ROOT / "contracts" / f"{stem}.schema.json").read_text(encoding="utf-8"))
            template = json.loads((ROOT / "templates" / f"{stem}.json").read_text(encoding="utf-8"))

            self.assertIn("HARNESS V2", schema["title"])
            self.assertIn("kind", schema["required"])
            self.assertIn("source_refs", schema["properties"])
            self.assertIn("kind", template)
            self.assertFalse(template["lifecycle_transition"])

        self.assertEqual(json.loads(VALID_APPROVAL_DECISION.read_text(encoding="utf-8"))["kind"], "ApprovalDecision")
        self.assertEqual(json.loads(VALID_PROOF_RECEIPT.read_text(encoding="utf-8"))["kind"], "ProofReceipt")

    def test_goal5_approval_decision_binds_user_response_and_scope(self):
        from harness_v2.decisions import evaluate_decision

        valid_payload = fresh_approval_decision_payload()
        valid = evaluate_decision(valid_payload, task=valid_task_payload(), root=ROOT)
        broad = evaluate_decision(json.loads(INVALID_BROAD_APPROVAL.read_text(encoding="utf-8")), task=valid_task_payload(), root=ROOT)
        no_user_response = fresh_approval_decision_payload()
        no_user_response.pop("user_response")
        no_user_response_result = evaluate_decision(no_user_response, task=valid_task_payload(), root=ROOT)
        broad_with_metadata = fresh_approval_decision_payload()
        broad_with_metadata["user_response"]["text"] = "Approve broad unspecified work."
        broad_with_metadata["user_response"]["sha256"] = "76aa8eaeee04042890cec8789a8a945e62e42d71125bee81f6b9fd83d08a665b"
        broad_with_metadata_result = evaluate_decision(broad_with_metadata, task=valid_task_payload(), root=ROOT)
        git_scope_widening = fresh_approval_decision_payload()
        git_scope_widening["git_scope"] = "git push"
        git_scope_widening_result = evaluate_decision(git_scope_widening, task=valid_task_payload(), root=ROOT)

        self.assertTrue(valid.ok, valid.errors)
        self.assertEqual(valid.kind, "ApprovalDecision")
        self.assertFalse(broad.ok)
        self.assertIn("ApprovalDecision requires exact edit_paths", "\n".join(broad.errors))
        self.assertFalse(no_user_response_result.ok)
        self.assertIn("ApprovalDecision requires user_response binding", "\n".join(no_user_response_result.errors))
        self.assertFalse(broad_with_metadata_result.ok)
        self.assertIn("ApprovalDecision user_response is too broad to bind approval", "\n".join(broad_with_metadata_result.errors))
        self.assertFalse(git_scope_widening_result.ok)
        self.assertIn("ApprovalDecision git_scope exceeds task permission ceiling: git push", "\n".join(git_scope_widening_result.errors))

    def test_goal5_permission_decision_cannot_exceed_approval_ceiling(self):
        from harness_v2.decisions import evaluate_decision

        task = valid_task_payload()
        permission_decision = {
            "kind": "PermissionDecision",
            "decision_id": "permission-decision-exceeds-approval",
            "task_id": task["task_id"],
            "approval_decision_ref": "tests\\fixtures\\valid-approval-decision.json",
            "side_effect_class": "git",
            "requested_side_effects": ["git push"],
            "approved_side_effects": ["git push"],
            "denied_side_effects": [],
            "approval_ceiling": {
                "side_effects": ["local file writes under F:\\Folder\\harness-v2"],
                "exclusions": ["npm publish", "release execution"],
            },
            "preflight": {
                "ok": True,
                "task_id": task["task_id"],
                "command": "harness-v2 preflight tests\\fixtures\\valid-task.json --side-effect \"git push\"",
            },
            "source_refs": [
                {
                    "path": "CURRENT.md",
                    "sha256": "046229e6f7c8009afec331482dd67c4e265fc9e34bf3c114f5a3bbc4a5bbae95",
                }
            ],
            "lifecycle_transition": False,
        }

        result = evaluate_decision(permission_decision, task=task, root=ROOT)

        self.assertFalse(result.ok)
        self.assertIn("PermissionDecision approved side effect exceeds approval ceiling: git push", "\n".join(result.errors))

        missing_ref = dict(permission_decision)
        missing_ref["approval_decision_ref"] = "tests\\fixtures\\missing-approval-decision.json"
        missing_ref_result = evaluate_decision(missing_ref, task=task, root=ROOT)

        self.assertFalse(missing_ref_result.ok)
        self.assertIn("PermissionDecision approval_decision_ref does not exist", "\n".join(missing_ref_result.errors))

    def test_goal5_proof_receipt_binds_obligation_and_current_source(self):
        from harness_v2.decisions import evaluate_decision, evaluate_decision_file

        valid_payload = fresh_proof_receipt_payload()
        valid = evaluate_decision(valid_payload, task=valid_task_payload(), root=ROOT)
        stale = evaluate_decision_file(INVALID_STALE_PROOF_RECEIPT, task_path=VALID_TASK, root=ROOT)
        missing_source = fresh_proof_receipt_payload()
        missing_source.pop("source_refs")
        transition_claim = fresh_proof_receipt_payload()
        transition_claim["lifecycle_transition"] = True

        missing_source_result = evaluate_decision(missing_source, task=valid_task_payload(), root=ROOT)
        transition_result = evaluate_decision(transition_claim, task=valid_task_payload(), root=ROOT)

        self.assertTrue(valid.ok, valid.errors)
        self.assertEqual(valid.kind, "ProofReceipt")
        self.assertFalse(stale.ok)
        self.assertEqual(stale.stale[0]["path"], "CURRENT.md")
        self.assertFalse(missing_source_result.ok)
        self.assertIn("ProofReceipt requires current source_refs", "\n".join(missing_source_result.errors))
        self.assertFalse(transition_result.ok)
        self.assertIn("decision/receipt records cannot declare lifecycle transition", "\n".join(transition_result.errors))

    def test_goal5_required_proof_receipt_is_not_replaced_by_test_pass(self):
        from harness_v2.core import validate_task
        from harness_v2.decisions import evaluate_proof_receipt_requirement

        task = valid_task_payload()
        task["proof"]["receipt_required"] = True
        task["proof"]["receipts"] = []

        missing = validate_task(task, root=ROOT)

        requirement = evaluate_proof_receipt_requirement(
            task,
            [fresh_proof_receipt_payload()],
            root=ROOT,
        )
        task["proof"]["receipts"] = ["tests\\fixtures\\valid-approval-decision.json"]
        substituted = validate_task(task, root=ROOT)

        self.assertFalse(missing.ok)
        self.assertIn("proof receipt required but proof.receipts is empty", "\n".join(missing.errors))
        self.assertTrue(requirement.ok, requirement.errors)
        self.assertFalse(substituted.ok)
        self.assertIn("expected ProofReceipt, got ApprovalDecision", "\n".join(substituted.errors))

    def test_goal5_cli_decision_command_reports_decision_result(self):
        with tempfile.TemporaryDirectory() as temp_root:
            decision_path = Path(temp_root) / "valid-proof-receipt.json"
            decision_path.write_text(json.dumps(fresh_proof_receipt_payload()), encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "decision",
                    str(decision_path),
                    "--task",
                    str(VALID_TASK),
                    "--root",
                    str(ROOT),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["ok"], payload["errors"])
        self.assertEqual(payload["kind"], "ProofReceipt")

    def test_goal1_gate_state_schema_and_template_are_product_surfaces(self):
        schema = json.loads((ROOT / "contracts" / "gate-state.schema.json").read_text(encoding="utf-8"))
        template = json.loads((ROOT / "templates" / "gate-state.json").read_text(encoding="utf-8"))

        self.assertEqual(schema["title"], "HARNESS V2 Gate State")
        self.assertEqual(
            schema["required"],
            [
                "schema_version",
                "source_task_ref",
                "source_sha256",
                "derived_current_gate",
                "derived_from",
                "generated_at",
            ],
        )
        self.assertEqual(template["derived_from"], "workflow_stage")
        self.assertEqual(template["derived_current_gate"], "<derived from source task workflow_stage>")
        self.assertIn("source_sha256", template)

    def test_goal1_strict_matching_gate_state_passes(self):
        from harness_v2.core import validate_task_file

        with tempfile.TemporaryDirectory() as temp_root:
            task_path = write_goal1_project(
                Path(temp_root),
                contract_version="0.1.8",
                gate="development",
            )

            result = validate_task_file(task_path)

        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.current_gate, "development")
        self.assertEqual(result.gate_state["present"], True)
        self.assertEqual(result.gate_state["derived_from"], "workflow_stage")

    def test_goal1_rejects_mismatched_gate_state(self):
        from harness_v2.core import validate_task_file

        with tempfile.TemporaryDirectory() as temp_root:
            task_path = write_goal1_project(
                Path(temp_root),
                contract_version="0.1.8",
                gate="plan",
            )

            result = validate_task_file(task_path)

        self.assertFalse(result.ok)
        self.assertIn("gate-state derived_current_gate must match workflow_stage", "\n".join(result.errors))

    def test_goal1_rejects_domain_owner_gate_state_as_current_gate(self):
        from harness_v2.core import validate_task_file

        with tempfile.TemporaryDirectory() as temp_root:
            task_path = write_goal1_project(
                Path(temp_root),
                contract_version="0.1.8",
                gate="domain:improvement",
            )

            result = validate_task_file(task_path)

        self.assertFalse(result.ok)
        errors = "\n".join(result.errors)
        self.assertIn("gate-state derived_current_gate is not a known stage: domain:improvement", errors)
        self.assertIn("gate-state derived_current_gate is a responsibility/domain owner, not a workflow stage: domain:improvement", errors)

    def test_goal1_rejects_stale_gate_state_source_hash(self):
        from harness_v2.core import validate_task_file

        with tempfile.TemporaryDirectory() as temp_root:
            task_path = write_goal1_project(
                Path(temp_root),
                contract_version="0.1.8",
                gate="development",
                source_sha256="0" * 64,
            )

            result = validate_task_file(task_path)

        self.assertFalse(result.ok)
        self.assertIn("gate-state source_sha256 does not match source_task_ref", "\n".join(result.errors))

    def test_goal1_rejects_gate_state_bound_to_other_task_file(self):
        from harness_v2.core import validate_task_file

        with tempfile.TemporaryDirectory() as temp_root:
            task_path = write_goal1_project(
                Path(temp_root),
                contract_version="0.1.8",
                gate="development",
                source_task_ref="contracts\\other-task.json",
                duplicate_source_task=True,
            )

            result = validate_task_file(task_path)

        self.assertFalse(result.ok)
        self.assertIn("gate-state source_task_ref must match validated task path", "\n".join(result.errors))

    def test_goal1_rejects_gate_state_derived_from_stale_in_memory_task_data(self):
        from harness_v2.core import validate_task

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            task_path = write_goal1_project(
                root,
                contract_version="0.1.8",
                gate="plan",
            )
            stale_data = json.loads(task_path.read_text(encoding="utf-8"))
            stale_data["workflow_stage"] = "plan"
            stale_data["approval"]["approved_paths"] = ["records\\stages\\plan.md"]
            stale_data["permission"]["allowed_side_effects"] = ["local file writes to stage record files"]

            result = validate_task(stale_data, root=root, task_path=task_path)

        self.assertFalse(result.ok)
        self.assertIn("gate-state derived_current_gate must match source_task_ref workflow_stage", "\n".join(result.errors))

    def test_cli_verify_reports_current_gate_read_model_without_authority_claims(self):
        completed = subprocess.run(
            [sys.executable, "-m", "harness_v2", "verify", str(VALID_TASK)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["current_gate"], "development")
        self.assertEqual(payload["gate_state"]["present"], False)
        self.assertNotIn("approval", payload["gate_state"])
        self.assertNotIn("proof", payload["gate_state"])
        self.assertNotIn("permission", payload["gate_state"])
        self.assertNotIn("lifecycle_transition", payload["gate_state"])

    def test_goal2_transition_schema_template_and_parser_contract(self):
        from harness_v2.lifecycle import parse_transition_log

        schema = json.loads((ROOT / "contracts" / "transition.schema.json").read_text(encoding="utf-8"))
        template = (ROOT / "templates" / "transition-log.md").read_text(encoding="utf-8")
        transitions = parse_transition_log((ROOT / "tests" / "fixtures" / "valid-transition-log.md").read_text(encoding="utf-8"))

        self.assertEqual(schema["title"], "HARNESS V2 Transition")
        self.assertEqual(schema["required"], ["timestamp", "from_gate", "to_gate", "reason", "source_refs", "approval_ref", "permission_ref", "proof_ref", "freshness_refs", "stale_check", "actor"])
        self.assertIn("lifecycle movement는 evaluated operation이며, log line 자체가 아닙니다.", template)
        self.assertEqual(transitions[-1].from_gate, "plan_approval")
        self.assertEqual(transitions[-1].to_gate, "development")

    def test_goal2_valid_transition_appends_and_evaluates(self):
        from harness_v2.lifecycle import TransitionRecord, append_transition_record, evaluate_transition_log, parse_transition_log

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            task_path = write_goal2_task(root, stage="plan_approval")
            log_path = root / "records" / "transition-log.md"
            log_path.parent.mkdir(parents=True, exist_ok=True)

            append_transition_record(
                log_path,
                TransitionRecord(
                    timestamp="2026-06-19T00:00:00Z",
                    from_gate="plan_approval",
                    to_gate="development",
                    reason="exact plan approval permits development entry",
                    source_refs=("CURRENT.md",),
                    approval_ref="control\\approval.md",
                    permission_ref="control\\permission.md",
                    proof_ref="not_required",
                    freshness_refs=("CURRENT.md",),
                    stale_check="fresh",
                    actor="test",
                ),
            )
            result = evaluate_transition_log(task_path, log_path)

            self.assertTrue(result.ok, result.errors)
            self.assertEqual(result.transition["from_gate"], "plan_approval")
            self.assertEqual(result.transition["to_gate"], "development")
            self.assertEqual(len(parse_transition_log(log_path.read_text(encoding="utf-8"))), 1)

    def test_goal2_denies_review_only_transition_into_development(self):
        from harness_v2.lifecycle import TransitionRecord, evaluate_transition_record

        task = goal2_task_payload(stage="plan_review")
        result = evaluate_transition_record(
            task,
            TransitionRecord(
                timestamp="2026-06-19T00:00:00Z",
                from_gate="plan_review",
                to_gate="development",
                reason="review pass only",
                source_refs=("records\\stages\\plan-review.md",),
                approval_ref="missing",
                permission_ref="missing",
                proof_ref="not_required",
                freshness_refs=("records\\stages\\plan-review.md",),
                stale_check="fresh",
                actor="test",
            ),
        )

        self.assertFalse(result.ok)
        self.assertIn("transition route is not allowed: plan_review -> development", result.errors)
        self.assertIn("development entry requires active approval and permission", result.errors)

    def test_goal2_denies_stale_approval_transition_into_development(self):
        from harness_v2.lifecycle import TransitionRecord, evaluate_transition_record

        task = goal2_task_payload(stage="plan_approval")
        result = evaluate_transition_record(
            task,
            TransitionRecord(
                timestamp="2026-06-19T00:00:00Z",
                from_gate="plan_approval",
                to_gate="development",
                reason="approval exists but stale",
                source_refs=("CURRENT.md",),
                approval_ref="control\\approval.md",
                permission_ref="control\\permission.md",
                proof_ref="not_required",
                freshness_refs=("CURRENT.md",),
                stale_check="stale_approval",
                actor="test",
            ),
        )

        self.assertFalse(result.ok)
        self.assertIn("stale approval denies lifecycle transition", result.errors)

    def test_goal2_denies_stale_permission_proof_and_source(self):
        from harness_v2.lifecycle import TransitionRecord, evaluate_transition_record

        cases = [
            ("stale_permission", "plan_approval", "development", "stale permission denies lifecycle transition"),
            ("stale_proof", "development_review", "improvement", "stale proof denies lifecycle transition"),
            ("stale_source", "plan_approval", "development", "stale source denies lifecycle transition"),
        ]

        for stale_check, from_gate, to_gate, expected_error in cases:
            with self.subTest(stale_check=stale_check):
                result = evaluate_transition_record(
                    goal2_task_payload(stage=from_gate),
                    TransitionRecord(
                        timestamp="2026-06-19T00:00:00Z",
                        from_gate=from_gate,
                        to_gate=to_gate,
                        reason="stale evidence must fail closed",
                        source_refs=("CURRENT.md",),
                        approval_ref="control\\approval.md",
                        permission_ref="control\\permission.md",
                        proof_ref="records\\proof.md",
                        freshness_refs=("CURRENT.md", "records\\proof.md"),
                        stale_check=stale_check,
                        actor="test",
                    ),
                )

                self.assertFalse(result.ok)
                self.assertIn(expected_error, result.errors)

    def test_goal2_denies_proof_only_transition_into_improvement(self):
        from harness_v2.lifecycle import TransitionRecord, evaluate_transition_record

        task = goal2_task_payload(stage="development_review")
        result = evaluate_transition_record(
            task,
            TransitionRecord(
                timestamp="2026-06-19T00:00:00Z",
                from_gate="development_review",
                to_gate="improvement",
                reason="proof alone must not create approval or permission",
                source_refs=("records\\stages\\development-review.md",),
                approval_ref="not_required",
                permission_ref="not_required",
                proof_ref="records\\proof.md",
                freshness_refs=("records\\stages\\development-review.md", "records\\proof.md"),
                stale_check="fresh",
                actor="test",
            ),
        )

        self.assertFalse(result.ok)
        self.assertIn("improvement entry requires active approval and permission", result.errors)

    def test_lifecycle_transition_refs_reject_observability_surfaces_as_authority(self):
        from harness_v2.lifecycle import TransitionRecord, evaluate_transition_record

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            write_goal2_task(root, stage="development_review")
            for relative_path in (
                "artifacts\\registry.md",
                "artifacts\\log.md",
                "routing\\manifest.md",
                "release\\transaction.md",
                "records\\stages\\development-review.md",
            ):
                path = root / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# {relative_path}\n", encoding="utf-8")
            result = evaluate_transition_record(
                goal2_task_payload(stage="development_review"),
                TransitionRecord(
                    timestamp="2026-06-19T00:00:00Z",
                    from_gate="development_review",
                    to_gate="improvement",
                    reason="observability rows are not authority",
                    source_refs=("records\\stages\\development-review.md",),
                    approval_ref="artifacts\\registry.md",
                    permission_ref="artifacts\\log.md",
                    proof_ref="routing\\manifest.md",
                    freshness_refs=("records\\stages\\development-review.md", "release\\transaction.md"),
                    stale_check="fresh",
                    actor="test",
                ),
                root=root,
            )

        self.assertFalse(result.ok)
        self.assertIn("approval_ref cannot use artifact registry/log, review, route, or release surface as authority: artifacts\\registry.md", result.errors)
        self.assertIn("permission_ref cannot use artifact registry/log, review, route, or release surface as authority: artifacts\\log.md", result.errors)
        self.assertIn("proof_ref cannot use artifact registry/log, review, route, or release surface as authority: routing\\manifest.md", result.errors)

    def test_goal2_valid_improvement_requires_active_approval_permission_and_current_proof(self):
        from harness_v2.lifecycle import TransitionRecord, evaluate_transition_record

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            task_path = write_goal2_task(root, stage="development_review")
            task = json.loads(task_path.read_text(encoding="utf-8"))
            result = evaluate_transition_record(
                task,
                TransitionRecord(
                    timestamp="2026-06-19T00:00:00Z",
                    from_gate="development_review",
                    to_gate="improvement",
                    reason="review proof permits improvement intake",
                    source_refs=("records\\stages\\development-review.md",),
                    approval_ref="control\\approval.md",
                    permission_ref="control\\permission.md",
                    proof_ref="records\\proof.md",
                    freshness_refs=("records\\stages\\development-review.md", "records\\proof.md"),
                    stale_check="fresh",
                    actor="test",
                ),
                root=root,
            )

        self.assertTrue(result.ok, result.errors)

    def test_goal2_denies_absolute_parent_and_missing_transition_refs(self):
        from harness_v2.lifecycle import TransitionRecord, evaluate_transition_log, evaluate_transition_record

        with tempfile.TemporaryDirectory() as temp_root, tempfile.TemporaryDirectory() as outside_temp:
            root = Path(temp_root)
            task_path = write_goal2_task(root, stage="plan_approval")
            task = json.loads(task_path.read_text(encoding="utf-8"))
            outside_log = Path(outside_temp) / "outside-transition-log.md"
            outside_log.write_text("# outside\n", encoding="utf-8")
            result = evaluate_transition_record(
                task,
                TransitionRecord(
                    timestamp="2026-06-19T00:00:00Z",
                    from_gate="plan_approval",
                    to_gate="development",
                    reason="bad refs",
                    source_refs=("..\\outside.md",),
                    approval_ref="C:\\outside\\approval.md",
                    permission_ref="control\\missing-permission.md",
                    proof_ref="not_required",
                    freshness_refs=("missing\\freshness.md",),
                    stale_check="fresh",
                    actor="test",
                ),
                root=root,
            )
            outside_log_result = evaluate_transition_log(task_path, outside_log)

        self.assertFalse(result.ok)
        self.assertIn("source_refs entry must stay under project root: ..\\outside.md", result.errors)
        self.assertIn("approval_ref must be project-relative: C:\\outside\\approval.md", result.errors)
        self.assertIn("permission_ref does not exist: control\\missing-permission.md", result.errors)
        self.assertIn("freshness_refs entry does not exist: missing\\freshness.md", result.errors)
        self.assertFalse(outside_log_result.ok)
        self.assertIn("transition log path must stay under project root", outside_log_result.errors)

    def test_goal2_transition_fixture_and_hash_guard_are_exercised(self):
        from harness_v2.lifecycle import (
            TransitionRecord,
            append_transition_record,
            evaluate_transition_log,
            transition_log_sha256,
        )

        stale_fixture = evaluate_transition_log(
            VALID_TASK,
            ROOT / "tests" / "fixtures" / "invalid-transition-stale-approval.md",
        )
        self.assertFalse(stale_fixture.ok)
        self.assertIn("stale approval denies lifecycle transition", stale_fixture.errors)

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            log_path = root / "records" / "transition-log.md"
            log_path.parent.mkdir(parents=True)
            append_transition_record(
                log_path,
                TransitionRecord(
                    timestamp="2026-06-19T00:00:00Z",
                    from_gate="spec",
                    to_gate="spec_review",
                    reason="initial append",
                    source_refs=("records\\stages\\spec.md",),
                    approval_ref="not_required",
                    permission_ref="not_required",
                    proof_ref="not_required",
                    freshness_refs=("records\\stages\\spec.md",),
                    stale_check="fresh",
                    actor="test",
                ),
            )
            previous_hash = transition_log_sha256(log_path)
            log_path.write_text(log_path.read_text(encoding="utf-8").replace("initial append", "tampered"), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "transition ledger hash mismatch"):
                append_transition_record(
                    log_path,
                    TransitionRecord(
                        timestamp="2026-06-19T00:01:00Z",
                        from_gate="spec_review",
                        to_gate="plan",
                        reason="append after tamper",
                        source_refs=("records\\stages\\spec-review.md",),
                        approval_ref="not_required",
                        permission_ref="not_required",
                        proof_ref="not_required",
                        freshness_refs=("records\\stages\\spec-review.md",),
                        stale_check="fresh",
                        actor="test",
                    ),
                    previous_ledger_hash=previous_hash,
                )

    def test_goal2_denies_legacy_or_same_task_improvement_to_spec_transitions(self):
        from harness_v2.lifecycle import TransitionRecord, evaluate_transition_record

        legacy = evaluate_transition_record(
            goal2_task_payload(stage="plan_approval"),
            TransitionRecord(
                timestamp="2026-06-19T00:00:00Z",
                from_gate="approval",
                to_gate="development",
                reason="legacy transition",
                source_refs=("CURRENT.md",),
                approval_ref="control\\approval.md",
                permission_ref="control\\permission.md",
                proof_ref="not_required",
                freshness_refs=("CURRENT.md",),
                stale_check="fresh",
                actor="test",
            ),
        )
        same_task_loop = evaluate_transition_record(
            goal2_task_payload(stage="improvement"),
            TransitionRecord(
                timestamp="2026-06-19T00:00:00Z",
                from_gate="improvement",
                to_gate="spec",
                reason="same task loop",
                source_refs=("records\\stages\\improvement.md",),
                approval_ref="not_required",
                permission_ref="not_required",
                proof_ref="not_required",
                freshness_refs=("records\\stages\\improvement.md",),
                stale_check="fresh",
                actor="test",
            ),
        )

        self.assertFalse(legacy.ok)
        self.assertIn("transition uses legacy stage alias 'approval'; use 'plan_approval'", legacy.errors)
        self.assertFalse(same_task_loop.ok)
        self.assertIn("same-task improvement-to-spec transition is denied", same_task_loop.errors)

    def test_goal2_transition_rejects_domain_owner_gate_values(self):
        from harness_v2.lifecycle import TransitionRecord, evaluate_transition_record

        result = evaluate_transition_record(
            goal2_task_payload(stage="development_review"),
            TransitionRecord(
                timestamp="2026-06-19T00:00:00Z",
                from_gate="development_review",
                to_gate="domain:improvement",
                reason="domain owner is not a workflow stage",
                source_refs=("records\\stages\\development-review.md",),
                approval_ref="control\\approval.md",
                permission_ref="control\\permission.md",
                proof_ref="records\\proof.md",
                freshness_refs=("records\\stages\\development-review.md",),
                stale_check="fresh",
                actor="test",
            ),
            root=ROOT,
        )

        self.assertFalse(result.ok)
        self.assertIn("transition gate is not known: domain:improvement", result.errors)

    def test_goal3_freshness_schema_template_and_compatibility_diagnostic(self):
        from harness_v2.core import validate_task_file
        from harness_v2.freshness import evaluate_freshness_map

        schema = json.loads((ROOT / "contracts" / "freshness.schema.json").read_text(encoding="utf-8"))
        template = json.loads((ROOT / "templates" / "freshness-map.json").read_text(encoding="utf-8"))
        result = validate_task_file(VALID_TASK)
        freshness = evaluate_freshness_map(ROOT)
        stale_approval = evaluate_freshness_map(ROOT, ROOT / "tests" / "fixtures" / "invalid-stale-approval.json")
        stale_proof = evaluate_freshness_map(ROOT, ROOT / "tests" / "fixtures" / "invalid-stale-proof.json")

        self.assertEqual(schema["title"], "HARNESS V2 Freshness Map")
        self.assertIn("anchors", schema["required"])
        self.assertIn("evidence_refs", schema["properties"]["anchors"]["items"]["required"])
        self.assertEqual(template["schema_version"], "0.1.8")
        self.assertIn("anchors", template)
        self.assertIn("evidence_refs", template["anchors"][0])
        self.assertTrue(result.ok, result.errors)
        self.assertFalse(result.freshness["present"])
        self.assertIn("compatibility_diagnostic", result.freshness)
        self.assertFalse(freshness.present)
        self.assertTrue(freshness.ok)
        self.assertFalse(stale_approval.ok)
        self.assertEqual(stale_approval.stale[0]["backtrack_target"], "plan_approval")
        self.assertFalse(stale_proof.ok)
        self.assertEqual(stale_proof.stale[0]["backtrack_target"], "development_review")

    def test_goal3_stale_plan_source_emits_backtrack_target(self):
        from harness_v2.core import validate_task_file
        from harness_v2.freshness import evaluate_freshness_map

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            task_path = write_goal2_task(root, stage="plan_review")
            plan_path = root / "records" / "stages" / "plan.md"
            plan_hash = sha256_file(plan_path)
            evidence_ref = write_goal3_evidence(root, "records\\stages\\plan-review.md", plan_hash)
            write_goal3_freshness_map(
                root,
                [
                    goal3_anchor(
                        "plan-source",
                        "records\\stages\\plan.md",
                        plan_hash,
                        affects=["plan_review", "plan_approval"],
                        backtrack_target="plan",
                        reason="plan source changed",
                        evidence_refs=[evidence_ref],
                    )
                ],
            )
            plan_path.write_text("# Plan Stage Record\nchanged\n", encoding="utf-8")
            freshness = evaluate_freshness_map(root)
            validation = validate_task_file(task_path)

        self.assertFalse(freshness.ok)
        self.assertEqual(freshness.stale[0]["backtrack_target"], "plan")
        self.assertEqual(freshness.stale[0]["reason"], "plan source changed")
        self.assertIn("plan_review", freshness.stale[0]["affects"])
        self.assertFalse(validation.ok)
        self.assertIn("freshness stale: plan-source -> plan: plan source changed", validation.errors)

    def test_goal3_approval_scope_invalidates_permission_and_development_transition(self):
        from harness_v2.freshness import evaluate_freshness_map

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            write_goal2_task(root, stage="plan_approval")
            approval_path = root / "control" / "approval.md"
            approval_hash = sha256_file(approval_path)
            evidence_ref = write_goal3_evidence(root, "control\\permission.md", approval_hash)
            write_goal3_freshness_map(
                root,
                [
                    goal3_anchor(
                        "approval-scope",
                        "control\\approval.md",
                        approval_hash,
                        affects=["permission", "development_transition"],
                        backtrack_target="plan_approval",
                        reason="approval scope changed",
                        evidence_refs=[evidence_ref],
                    )
                ],
            )
            approval_path.write_text("# Approval\nchanged scope\n", encoding="utf-8")
            result = evaluate_freshness_map(root)

        self.assertFalse(result.ok)
        self.assertEqual(result.stale[0]["anchor_id"], "approval-scope")
        self.assertEqual(result.stale[0]["backtrack_target"], "plan_approval")
        self.assertIn("permission", result.stale[0]["affects"])
        self.assertIn("development_transition", result.stale[0]["affects"])

    def test_goal3_permission_side_effect_scope_invalidates_development_transition(self):
        from harness_v2.freshness import evaluate_freshness_map

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            write_goal2_task(root, stage="development")
            permission_path = root / "control" / "permission.md"
            permission_hash = sha256_file(permission_path)
            evidence_ref = write_goal3_evidence(root, "records\\stages\\development.md", permission_hash)
            write_goal3_freshness_map(
                root,
                [
                    goal3_anchor(
                        "permission-side-effect-scope",
                        "control\\permission.md",
                        permission_hash,
                        affects=["permission", "development_transition"],
                        backtrack_target="development",
                        reason="permission side-effect scope changed after development started",
                        evidence_refs=[evidence_ref],
                    )
                ],
            )
            permission_path.write_text("# Permission\nchanged side effect scope\n", encoding="utf-8")
            result = evaluate_freshness_map(root)

        self.assertFalse(result.ok)
        self.assertEqual(result.stale[0]["anchor_id"], "permission-side-effect-scope")
        self.assertEqual(result.stale[0]["backtrack_target"], "development")
        self.assertEqual(result.stale[0]["reason"], "permission side-effect scope changed after development started")

    def test_goal3_proof_and_test_changes_invalidate_proof_receipt(self):
        from harness_v2.freshness import evaluate_freshness_map

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            write_goal2_task(root, stage="development_review")
            proof_path = root / "control" / "proof.md"
            tests_path = root / "tests" / "test_harness_v2.py"
            tests_path.parent.mkdir(parents=True)
            tests_path.write_text("# proof test\n", encoding="utf-8")
            proof_hash = sha256_file(proof_path)
            tests_hash = sha256_file(tests_path)
            evidence_ref = write_goal3_evidence(root, "records\\proof.md", proof_hash, tests_hash)
            write_goal3_freshness_map(
                root,
                [
                    goal3_anchor("proof-obligation", "control\\proof.md", proof_hash, affects=["proof_receipt"], backtrack_target="development_review", reason="proof obligation changed", evidence_refs=[evidence_ref]),
                    goal3_anchor("proof-tests", "tests\\test_harness_v2.py", tests_hash, affects=["proof_receipt"], backtrack_target="development_review", reason="proof test changed", evidence_refs=[evidence_ref]),
                ],
            )
            proof_path.write_text("# Proof\nchanged predicate\n", encoding="utf-8")
            tests_path.write_text("# proof test changed\n", encoding="utf-8")
            result = evaluate_freshness_map(root)

        self.assertFalse(result.ok)
        self.assertEqual({item["anchor_id"] for item in result.stale}, {"proof-obligation", "proof-tests"})
        self.assertTrue(all(item["backtrack_target"] == "development_review" for item in result.stale))

    def test_goal3_artifact_registry_stale_survives_metadata_only_edits(self):
        from harness_v2.freshness import evaluate_freshness_map

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            write_goal2_task(root, stage="development_review")
            registry_path = root / "artifacts" / "registry.md"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text("# Artifact Registry\ninitial\n", encoding="utf-8")
            registry_hash = sha256_file(registry_path)
            evidence_ref = write_goal3_evidence(root, "records\\stages\\development-review.md", registry_hash)
            map_path = write_goal3_freshness_map(
                root,
                [
                    goal3_anchor(
                        "artifact-registry",
                        "artifacts\\registry.md",
                        registry_hash,
                        affects=["artifact_freshness_refs"],
                        backtrack_target="development_review",
                        reason="artifact registry changed",
                        evidence_refs=[evidence_ref],
                    )
                ],
            )
            registry_path.write_text("# Artifact Registry\nchanged\n", encoding="utf-8")
            first = evaluate_freshness_map(root)
            payload = json.loads(map_path.read_text(encoding="utf-8"))
            payload["anchors"][0]["source_sha256"] = sha256_file(registry_path)
            payload["anchors"][0]["reason"] = "metadata-only attempted clear"
            map_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
            second = evaluate_freshness_map(root)

        self.assertFalse(first.ok)
        self.assertFalse(second.ok)
        self.assertEqual(second.stale[0]["anchor_id"], "artifact-registry")
        self.assertEqual(second.stale[0]["backtrack_target"], "development_review")
        self.assertIn("evidence_ref does not bind source_sha256", "\n".join(second.stale[0]["evidence_errors"]))

    def test_goal3_rejects_invalid_backtrack_target_and_directory_anchor_without_crash(self):
        from harness_v2.freshness import evaluate_freshness_map

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            write_goal2_task(root, stage="development_review")
            directory_anchor = root / "records" / "stages"
            evidence_ref = write_goal3_evidence(root, "records\\stages\\development-review.md", "0" * 64)
            write_goal3_freshness_map(
                root,
                [
                    goal3_anchor(
                        "bad-target",
                        "records\\stages",
                        "0" * 64,
                        affects=["proof_receipt"],
                        backtrack_target="nonsense",
                        reason="bad target must not pass",
                        evidence_refs=[evidence_ref],
                    )
                ],
            )
            self.assertTrue(directory_anchor.is_dir())
            result = evaluate_freshness_map(root)

        self.assertFalse(result.ok)
        joined_errors = "\n".join(result.errors)
        self.assertIn("backtrack_target 'nonsense' is not allowed", joined_errors)
        self.assertIn("path must reference a file: records\\stages", joined_errors)

    def test_goal3_rejects_domain_owner_backtrack_target(self):
        from harness_v2.freshness import evaluate_freshness_map

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            write_goal2_task(root, stage="development_review")
            evidence_ref = write_goal3_evidence(root, "records\\stages\\development-review.md", "0" * 64)
            write_goal3_freshness_map(
                root,
                [
                    goal3_anchor(
                        "domain-owner-target",
                        "records\\stages\\development-review.md",
                        "0" * 64,
                        affects=["proof_receipt"],
                        backtrack_target="domain:improvement",
                        reason="domain owner must not be a backtrack target",
                        evidence_refs=[evidence_ref],
                    )
                ],
            )
            result = evaluate_freshness_map(root)

        self.assertFalse(result.ok)
        self.assertIn("backtrack_target 'domain:improvement' is not allowed", "\n".join(result.errors))

    def test_goal3_cli_verify_failure_outputs_stale_reason_and_freshness_payload(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            task_path = write_goal2_task(root, stage="plan_review")
            plan_path = root / "records" / "stages" / "plan.md"
            plan_hash = sha256_file(plan_path)
            evidence_ref = write_goal3_evidence(root, "records\\stages\\plan-review.md", plan_hash)
            write_goal3_freshness_map(
                root,
                [
                    goal3_anchor(
                        "plan-source",
                        "records\\stages\\plan.md",
                        plan_hash,
                        affects=["plan_review", "plan_approval"],
                        backtrack_target="plan",
                        reason="plan source changed",
                        evidence_refs=[evidence_ref],
                    )
                ],
            )
            plan_path.write_text("# Plan Stage Record\nchanged\n", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "-m", "harness_v2", "verify", str(task_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 1)
        payload = json.loads(completed.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["freshness"]["stale"][0]["backtrack_target"], "plan")
        self.assertEqual(payload["freshness"]["stale"][0]["reason"], "plan source changed")
        self.assertIn("freshness stale: plan-source -> plan: plan source changed", completed.stderr)

    def test_goal3_mcp_verify_reports_stale_freshness_details(self):
        from harness_v2.mcp import handle_message

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            task_path = write_goal2_task(root, stage="development")
            permission_path = root / "control" / "permission.md"
            permission_hash = sha256_file(permission_path)
            evidence_ref = write_goal3_evidence(root, "records\\stages\\development.md", permission_hash)
            write_goal3_freshness_map(
                root,
                [
                    goal3_anchor(
                        "permission-side-effect-scope",
                        "control\\permission.md",
                        permission_hash,
                        affects=["permission", "development_transition"],
                        backtrack_target="development",
                        reason="permission side-effect scope changed after development started",
                        evidence_refs=[evidence_ref],
                    )
                ],
            )
            permission_path.write_text("# Permission\nchanged side effect scope\n", encoding="utf-8")
            response = handle_message(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {"name": "harness_verify", "arguments": {"task": str(task_path)}},
                    }
                )
            )

        payload = response["result"]["structuredContent"]
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["freshness"]["stale"][0]["anchor_id"], "permission-side-effect-scope")
        self.assertEqual(payload["freshness"]["stale"][0]["reason"], "permission side-effect scope changed after development started")

    def test_verifier_accepts_all_known_workflow_stages(self):
        from harness_v2.core import validate_task

        examples = {
            "spec": stage_payload(
                "spec",
                ["records\\stages\\spec.md"],
                allowed_side_effects=["local file writes to stage record files"],
            ),
            "spec_review": stage_payload(
                "spec_review",
                ["records\\stages\\spec-review.md"],
                allowed_side_effects=["local file writes to stage record files"],
            ),
            "plan": stage_payload(
                "plan",
                ["records\\stages\\plan.md"],
                allowed_side_effects=["local file writes to stage record files"],
            ),
            "plan_review": stage_payload(
                "plan_review",
                ["records\\stages\\plan-review.md"],
                allowed_side_effects=["local file writes to stage record files"],
            ),
            "plan_approval": stage_payload("plan_approval", ["control\\approval.md", "records\\stages\\plan-approval.md"]),
            "development": stage_payload(
                "development",
                ["AGENTS.md"],
                allowed_side_effects=["local file writes under F:\\Folder\\harness-v2"],
            ),
            "development_review": stage_payload(
                "development_review",
                ["records\\stages\\development-review.md"],
                allowed_side_effects=["local file writes to stage record files"],
            ),
            "improvement": stage_payload(
                "improvement",
                ["records\\stages\\improvement.md", "safety\\improvement.md"],
                allowed_side_effects=["local file writes to stage record files"],
            ),
        }

        for stage, payload in examples.items():
            with self.subTest(stage=stage):
                result = validate_task(payload, root=ROOT)
                self.assertTrue(result.ok, result.errors)

    def test_workflow_stage_engine_rejects_stage_rule_violations(self):
        from harness_v2.core import validate_task

        cases = [
            (
                "spec_product_path",
                stage_payload("spec", ["harness_v2\\core.py"]),
                "spec stage approved path is outside allowed surface: harness_v2\\core.py",
            ),
            (
                "plan_non_record_mutation",
                stage_payload("plan", ["records\\stages\\plan.md"], allowed_side_effects=["git push"]),
                "plan stage cannot allow non-record side effect: git push",
            ),
            (
                "plan_review_lifecycle",
                stage_payload("plan_review", ["records\\stages\\plan-review.md"], target_state="public_release_candidate"),
                "plan_review stage cannot move lifecycle state",
            ),
            (
                "plan_approval_broad_packet",
                {**stage_payload("plan_approval", ["control\\approval.md"]), "approval": {
                    **stage_payload("plan_approval", ["control\\approval.md"])["approval"],
                    "packet": "go ahead",
                    "excluded_side_effects": []
                }},
                "plan_approval stage requires an exact approval packet, not a broad approval phrase",
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
                stage_payload("development_review", ["records\\stages\\development-review.md"], allowed_side_effects=["git push"]),
                "development_review stage cannot allow non-record side effect: git push",
            ),
            (
                "development_review_lifecycle",
                stage_payload("development_review", ["records\\stages\\development-review.md"], target_state="public_release_candidate"),
                "development_review stage cannot move lifecycle state",
            ),
            (
                "development_review_authority_claim",
                stage_payload(
                    "development_review",
                    ["records\\stages\\development-review.md"],
                    proof_obligations=["review findings produce proof result"],
                ),
                "development_review stage cannot claim authority from review/route/artifact material: review findings produce proof result",
            ),
            (
                "improvement_product_path",
                stage_payload("improvement", ["harness_v2\\core.py"]),
                "improvement stage approved path is outside allowed surface: harness_v2\\core.py",
            ),
            (
                "improvement_release_execution",
                stage_payload(
                    "improvement",
                    ["records\\stages\\improvement.md"],
                    allowed_side_effects=["npm publish"],
                ),
                "improvement stage cannot allow release execution side effect: npm publish",
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
        self.assertEqual(status["state"], "workflow_realignment_review")
        self.assertIn("workflow_binding_engine_classified", status["substate"])
        self.assertIn("unreleased_local", status["substate"])
        self.assertIn("release_closed", status["substate"])

    def test_doctor_reports_integration_hardening_without_mutation_or_release_claim(self):
        from harness_v2.doctor import inspect_project

        report = inspect_project(ROOT)

        self.assertEqual(report["mutation"], "none")
        self.assertEqual(report["root_kind"], "harness_v2_source_checkout")
        self.assertTrue(report["source_checkout"])
        self.assertFalse(report["applied_project"])
        self.assertIn("not an applied project scaffold", report["misinstall_warning"])
        self.assertIn("Do not git clone vibedong/harness-v2", report["misinstall_warning"])
        self.assertEqual(report["release_ready"], False)
        self.assertEqual(report["release_boundary"]["status"], "closed")
        self.assertEqual(
            report["release_boundary"]["denied"],
            [
                "npm publish",
                "Python package registry publish",
                "GitHub release creation",
                "release tag creation",
            ],
        )
        self.assertEqual(
            report["integrated_surfaces"],
            ["init", "status", "verify", "preflight", "gate", "task-start", "mcp", "doctor", "npm-wrapper"],
        )
        self.assertEqual(
            report["recommended_sequence"],
            [
                "harness-v2 status --root .",
                "harness-v2 verify contracts\\harness-task.json",
                "harness-v2 gate contracts\\harness-task.json --root .",
            ],
        )
        self.assertIn("npm install -g harness-v2@latest", report["next_action"])
        self.assertIn("harness-v2 init --root <project>", report["next_action"])
        self.assertIn("next_action", report)
        self.assertNotIn(".git", report["shape"]["first_level_dirs"])
        self.assertFalse(any("__pycache__" in part for part in report["shape"]["first_level_dirs"]))

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

    def test_init_places_scaffold_in_target_root_not_nested_source_folder(self):
        from harness_v2.core import initialize_project

        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            init = initialize_project(root)
            payload = init.to_json()

            self.assertTrue(init.ok, init.errors)
            assert_fresh_scaffold_shape(self, root, payload, root)
            self.assertTrue((root / "AGENTS.md").exists())
            self.assertTrue((root / "RULES.md").exists())
            self.assertTrue((root / "CURRENT.md").exists())
            self.assertTrue((root / "contracts" / "harness-task.json").exists())
            self.assertFalse((root / "harness-v2").exists())
            self.assertFalse((root / "harness_v2").exists())
            self.assertFalse((root / "bin").exists())
            self.assertFalse((root / "package.json").exists())

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
            self.assertIn("harness-v2 doctor --root .", payload["next"])
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
            spec_record = (root / "records" / "stages" / "spec.md").read_text(encoding="utf-8")
            plan_record = (root / "records" / "stages" / "plan.md").read_text(encoding="utf-8")
            improvement_record = (root / "records" / "stages" / "improvement.md").read_text(encoding="utf-8")
            initial_task = json.loads((root / "contracts" / "harness-task.json").read_text(encoding="utf-8"))

            self.assertIn("AI 에이전트가 작업을 시작할 때 읽는 진입점", agents)
            self.assertIn("`README.md`는 사용자 설명서", agents)
            self.assertIn("task contract validator", agents)
            self.assertIn("CLI helper", agents)
            self.assertIn("자동 enforcement sandbox", agents)
            self.assertIn("completion layer", agents)
            self.assertIn("증거 수준에 맞춘 읽기 순서", agents)
            self.assertIn("설치, `init`, `apply`, CLI 사용 가능 상태는 임의의 미래 작업을 승인하지 않습니다", agents)
            self.assertIn("active task contract", agents)
            self.assertIn("harness-v2 doctor --root .", agents)
            self.assertIn("현재 작업 등록", agents)
            self.assertIn("harness-v2 task start --root .", agents)
            self.assertIn("records\\current-task.md", agents)
            self.assertIn("records\\stages\\spec.md", agents)
            self.assertIn("대화 답변만으로 기획, 분석, 구현 방향을 진행하지 않습니다", agents)
            self.assertIn("README 파일은 사용자용 문서일 뿐입니다", rules)
            self.assertIn("task-contract validator", rules)
            self.assertIn("자동 enforcement sandbox", rules)
            self.assertIn("completion layer", rules)
            self.assertIn("증거 수준에 맞춘 읽기", rules)
            self.assertIn("어떤 표면도 다른 표면을 대신하지 않습니다", rules)
            self.assertIn("harness-v2 task start --root .", rules)
            self.assertIn("records\\current-task.md", rules)
            self.assertIn("records\\stages\\spec.md", rules)
            self.assertIn("대화 답변만으로 진행하지 않습니다", rules)
            self.assertIn("자동 enforcement sandbox", current)
            self.assertIn("not_automatic_enforcement_completion", current)
            self.assertIn("harness-v2 doctor --root .", current)
            self.assertIn("harness-v2 task start --root .", current)
            self.assertIn("임의의 feature 작업", current)
            self.assertIn("## 현재 작업", current)
            self.assertIn("## 중지 조건", current)
            self.assertNotIn("## Current Task", current)
            self.assertNotIn("## Stop Conditions", current)
            self.assertIn("init/apply 성공", approval)
            self.assertIn("다음 작업의 permission을 부여하지 않습니다", permission)
            self.assertIn("설치/init/apply 성공", proof)
            self.assertIn("# Spec 단계 기록", spec_record)
            self.assertIn("# Plan 단계 기록", plan_record)
            self.assertIn("# Improvement 단계 기록", improvement_record)

            self.assertEqual(initial_task["source"]["basis"], ["AGENTS.md", "RULES.md", "CURRENT.md"])
            self.assertEqual(set(initial_task["approval"]["approved_paths"]), INITIAL_APPROVED_PATHS)
            self.assertEqual(set(initial_task["approval"]["excluded_side_effects"]), INITIAL_DENIED_SIDE_EFFECTS)
            self.assertEqual(set(initial_task["permission"]["allowed_side_effects"]), INITIAL_ALLOWED_SIDE_EFFECTS)
            self.assertEqual(set(initial_task["permission"]["denied_side_effects"]), INITIAL_DENIED_SIDE_EFFECTS)
            self.assertEqual(set(initial_task["proof"]["obligations"]), INITIAL_PROOF_OBLIGATIONS)
            self.assertEqual(initial_task["contract_version"], "0.1.8")
            self.assertEqual(initial_task["workflow_stage"], "spec")
            self.assertEqual(initial_task["current_gate"], "spec")
            self.assertEqual(initial_task["task_mode"], "scaffold_only")
            self.assertEqual(initial_task["record_strength"], "light")
            self.assertEqual(initial_task["risk_flags"], ["scaffold_generation"])
            self.assertEqual(initial_task["proof_profile"], "current")
            self.assertEqual(initial_task["capability_request"], ["init_scaffold"])
            self.assertTrue(initial_task["classification_required"])
            self.assertEqual(
                initial_task["record_density"],
                {
                    "generated_file_count": len(INITIAL_APPROVED_PATHS),
                    "required_read_set_size": 3,
                    "field_presence": "strict",
                },
            )
            self.assertEqual(initial_task["lifecycle"], {"current_state": "ready", "target_state": "ready"})

            from harness_v2.core import validate_task

            for denied in INITIAL_DENIED_SIDE_EFFECTS:
                mutated = json.loads(json.dumps(initial_task))
                mutated["permission"]["allowed_side_effects"].append(denied)
                result = validate_task(mutated, root=root)
                self.assertFalse(result.ok, denied)
                self.assertIn(f"permission side effect conflicts with denied side effect: {denied}", "\n".join(result.errors))

    def test_cli_task_start_registers_real_task_from_initial_scaffold(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            subprocess.run(
                [sys.executable, "-m", "harness_v2", "init", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )

            started = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "task",
                    "start",
                    "--root",
                    str(root),
                    "--title",
                    "나라장터 실시설계 크롤링 판단",
                    "--summary",
                    "전체 추출 후 통과/검토필요/제외 판정 흐름을 설계한다.",
                    "--source",
                    "F:\\dailynara",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(started.returncode, 0, started.stderr)
            payload = json.loads(started.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["task"], "contracts\\harness-task.json")
            self.assertIn("CURRENT.md", payload["written"])
            self.assertIn("contracts\\harness-task.json", payload["written"])
            self.assertIn("records\\current-task.md", payload["written"])
            self.assertIn("records\\stages\\spec.md", payload["written"])
            self.assertEqual(
                payload["next"],
                [
                    "harness-v2 status --root .",
                    "harness-v2 verify contracts\\harness-task.json",
                    "harness-v2 gate contracts\\harness-task.json --root .",
                ],
            )

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
            gate = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "gate",
                    str(root / "contracts" / "harness-task.json"),
                    "--root",
                    str(root),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            denied_publish = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "preflight",
                    str(root / "contracts" / "harness-task.json"),
                    "--side-effect",
                    "npm publish",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            denied_readme_write = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "preflight",
                    str(root / "contracts" / "harness-task.json"),
                    "--mode",
                    "write",
                    "--path",
                    "README.md",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            allowed_record_write = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "preflight",
                    str(root / "contracts" / "harness-task.json"),
                    "--mode",
                    "write",
                    "--path",
                    "records\\current-task.md",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(status.returncode, 0, status.stderr)
            status_payload = json.loads(status.stdout)
            self.assertEqual(status_payload["workflow"], "default")
            self.assertEqual(status_payload["state"], "active")
            self.assertEqual(status_payload["substate"], "task_registered / scope_pending")
            self.assertEqual(status_payload["layout_version"], "legacy-control-records-v1")
            self.assertTrue(status_payload["current_layout_paths_active"])
            self.assertFalse(status_payload["domain_layout_enabled"])
            self.assertFalse(status_payload["domain_layout_candidate"])
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertEqual(gate.returncode, 0, gate.stderr)
            self.assertNotEqual(denied_publish.returncode, 0)
            self.assertIn("side effect is not explicitly allowed", "\n".join(json.loads(denied_publish.stdout)["errors"]))
            self.assertNotEqual(denied_readme_write.returncode, 0)
            self.assertIn("write path is not approved", "\n".join(json.loads(denied_readme_write.stdout)["errors"]))
            self.assertEqual(allowed_record_write.returncode, 0, allowed_record_write.stderr)

            current = (root / "CURRENT.md").read_text(encoding="utf-8")
            task = json.loads((root / "contracts" / "harness-task.json").read_text(encoding="utf-8"))
            current_task = (root / "records" / "current-task.md").read_text(encoding="utf-8")
            spec = (root / "records" / "stages" / "spec.md").read_text(encoding="utf-8")
            self.assertIn("나라장터 실시설계 크롤링 판단", current)
            self.assertIn("전체 추출 후 통과/검토필요/제외 판정 흐름", current)
            self.assertEqual(task["title"], "나라장터 실시설계 크롤링 판단")
            self.assertEqual(task["workflow_stage"], "spec")
            self.assertEqual(task["current_gate"], "spec")
            self.assertEqual(task["task_mode"], "planned_change")
            self.assertEqual(task["lifecycle"], {"current_state": "active", "target_state": "active"})
            self.assertIn("F:\\dailynara", task["source"]["basis"])
            self.assertEqual(
                set(task["approval"]["approved_paths"]),
                {"records\\current-task.md", "records\\stages\\spec.md", "records\\decisions.md"},
            )
            self.assertIn("local file writes to records\\current-task.md", task["permission"]["allowed_side_effects"])
            self.assertIn("task scope remains pending", task["proof"]["obligations"])
            self.assertIn("나라장터 실시설계 크롤링 판단", current_task)
            self.assertIn("나라장터 실시설계 크롤링 판단", spec)
            self.assertIn("전체 추출 후 통과/검토필요/제외 판정 흐름", spec)
            self.assertIn("대화 답변만으로 흘려보내지 않습니다", spec)
            self.assertIn("Spec 진행 원칙", spec)
            current = (root / "CURRENT.md").read_text(encoding="utf-8")
            self.assertIn("## 현재 작업", current)
            self.assertIn("## 중지 조건", current)
            self.assertNotIn("## Current Task", current)
            self.assertNotIn("## Stop Conditions", current)

    def test_cli_task_start_refuses_to_replace_registered_task_without_force(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            subprocess.run(
                [sys.executable, "-m", "harness_v2", "init", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            first = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "task",
                    "start",
                    "--root",
                    str(root),
                    "--title",
                    "First task",
                    "--summary",
                    "First task summary.",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            second = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "task",
                    "start",
                    "--root",
                    str(root),
                    "--title",
                    "Second task",
                    "--summary",
                    "Second task summary.",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 1)
            payload = json.loads(second.stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("active task already registered", "\n".join(payload["errors"]))
            self.assertIn("--force", second.stderr)
            current = (root / "CURRENT.md").read_text(encoding="utf-8")
            self.assertIn("First task", current)
            self.assertNotIn("Second task", current)

    def test_cli_task_start_rejects_empty_title_and_missing_scaffold(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            missing = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "task",
                    "start",
                    "--root",
                    str(root),
                    "--title",
                    "Task",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(missing.returncode, 1)
            self.assertIn("HARNESS V2 scaffold is missing", "\n".join(json.loads(missing.stdout)["errors"]))

            subprocess.run(
                [sys.executable, "-m", "harness_v2", "init", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            empty = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "task",
                    "start",
                    "--root",
                    str(root),
                    "--title",
                    "   ",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(empty.returncode, 1)
            self.assertIn("task title must be a non-empty string", "\n".join(json.loads(empty.stdout)["errors"]))

    def test_cli_task_start_rolls_back_when_registered_contract_fails_validation(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            subprocess.run(
                [sys.executable, "-m", "harness_v2", "init", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            previous_current = (root / "CURRENT.md").read_text(encoding="utf-8")
            previous_task = (root / "contracts" / "harness-task.json").read_text(encoding="utf-8")
            previous_current_task = (root / "records" / "current-task.md").read_text(encoding="utf-8")
            (root / "control" / "lifecycle.md").write_text(
                "# HARNESS V2 Lifecycle Control\n\nKnown local states:\n\n- `ready`\n",
                encoding="utf-8",
            )

            started = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "harness_v2",
                    "task",
                    "start",
                    "--root",
                    str(root),
                    "--title",
                    "Rollback task",
                    "--summary",
                    "This should fail validation and rollback.",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(started.returncode, 1)
            self.assertIn("not a known state: active", "\n".join(json.loads(started.stdout)["errors"]))
            self.assertEqual((root / "CURRENT.md").read_text(encoding="utf-8"), previous_current)
            self.assertEqual((root / "contracts" / "harness-task.json").read_text(encoding="utf-8"), previous_task)
            self.assertEqual((root / "records" / "current-task.md").read_text(encoding="utf-8"), previous_current_task)

    def test_node_wrapper_delegates_task_start_to_python_cli(self):
        with tempfile.TemporaryDirectory() as temp_root:
            root = Path(temp_root)
            init = subprocess.run(
                ["node", "bin/harness-v2.js", "init", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            started = subprocess.run(
                [
                    "node",
                    "bin/harness-v2.js",
                    "task",
                    "start",
                    "--root",
                    str(root),
                    "--title",
                    "npm wrapper task",
                    "--summary",
                    "Register through the npm wrapper.",
                ],
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
            self.assertEqual(started.returncode, 0, started.stderr)
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertEqual(json.loads(verify.stdout)["task_id"], "npm-wrapper-task")

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
            protected_edits = {
                "AGENTS.md": "# Custom AGENTS\n\nKeep this file.\n",
                "CURRENT.md": "# Custom CURRENT\n\nworkflow: `custom`\nstate: `custom_state`\nsubstate: `custom_substate`\n",
                "control\\approval.md": "# Custom Approval\n\nDo not overwrite approval state.\n",
                "control\\permission.md": "# Custom Permission\n\nDo not overwrite permission state.\n",
                "control\\proof.md": "# Custom Proof\n\nDo not overwrite proof state.\n",
                "control\\lifecycle.md": "# Custom Lifecycle\n\nDo not overwrite lifecycle state.\n",
                "contracts\\harness-task.json": json.dumps({"custom": "contract"}, indent=2) + "\n",
                "records\\stages\\spec.md": "# Custom Spec Record\n\nDo not overwrite record state.\n",
                "records\\proof.md": "# Custom Proof Record\n\nDo not overwrite proof notes.\n",
            }
            for relative_path, content in protected_edits.items():
                (root / relative_path).write_text(content, encoding="utf-8")

            applied = subprocess.run(
                [sys.executable, "-m", "harness_v2", "apply", "--root", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(applied.returncode, 0, applied.stderr)
            payload = json.loads(applied.stdout)
            self.assertEqual(payload["overwritten"], [])
            self.assertGreaterEqual(set(payload["skipped"]), EXPECTED_SCAFFOLD_CREATED)
            for relative_path, content in protected_edits.items():
                self.assertIn(relative_path, payload["skipped"])
                self.assertEqual((root / relative_path).read_text(encoding="utf-8"), content)

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

    def test_cli_init_refuses_direct_source_checkout_as_project_root(self):
        with tempfile.TemporaryDirectory() as temp_root:
            target = Path(temp_root) / "mptech"
            target.mkdir()
            (target / "harness_v2").mkdir()
            (target / "bin").mkdir()
            (target / "package.json").write_text(
                json.dumps({"name": "harness-v2", "version": "0.0.0"}),
                encoding="utf-8",
            )
            (target / "harness_v2" / "core.py").write_text("# marker\n", encoding="utf-8")
            (target / "bin" / "harness-v2.js").write_text("// marker\n", encoding="utf-8")

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
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(init.returncode, 1)
            payload = json.loads(init.stdout)
            self.assertFalse(payload["ok"])
            self.assertFalse(payload["redirected_from_package_root"])
            self.assertEqual(Path(payload["root"]), target.resolve())
            self.assertIn("HARNESS V2 source checkout", "\n".join(payload["errors"]))
            self.assertIn("do not git clone", init.stderr)
            self.assertFalse((target / "contracts" / "harness-task.json").exists())
            self.assertFalse((target.parent / "AGENTS.md").exists())


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


def _json_block_after(content: str, marker: str) -> str:
    marker_index = content.index(marker)
    fence_start = content.rfind("```json", 0, marker_index)
    fence_end = content.find("```", marker_index)
    if fence_start == -1 or fence_end == -1:
        raise AssertionError(f"JSON block not found for marker {marker}")
    json_start = content.find("\n", fence_start) + 1
    return content[json_start:fence_end].strip()


def mcp_input(*messages: dict) -> str:
    return "\n".join(json.dumps(message, separators=(",", ":")) for message in messages) + "\n"


def write_goal1_project(
    root: Path,
    *,
    contract_version: str,
    gate: str,
    source_sha256: str | None = None,
    source_task_ref: str = "contracts\\harness-task.json",
    duplicate_source_task: bool = False,
) -> Path:
    (root / "contracts").mkdir(parents=True)
    (root / "records").mkdir()
    (root / "CURRENT.md").write_text(
        "\n".join(
            [
                "workflow: `remaining_completion_program`",
                "state: `workflow_realignment_review`",
                "substate: `goal1-test`",
            ]
        ),
        encoding="utf-8",
    )
    payload = valid_task_payload()
    payload["contract_version"] = contract_version
    payload["task_mode"] = "planned_change"
    payload["record_strength"] = "strict"
    payload.pop("current_gate", None)
    task_path = root / "contracts" / "harness-task.json"
    task_bytes = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    task_path.write_bytes(task_bytes)
    if duplicate_source_task:
        duplicate_path = root / source_task_ref
        duplicate_path.parent.mkdir(parents=True, exist_ok=True)
        duplicate_path.write_bytes(task_bytes)
    actual_hash = hashlib.sha256(task_bytes).hexdigest()
    (root / "records" / "gate-state.json").write_text(
        json.dumps(
            {
                "schema_version": "0.1.8",
                "source_task_ref": source_task_ref,
                "source_sha256": source_sha256 or actual_hash,
                "derived_current_gate": gate,
                "derived_from": "workflow_stage",
                "generated_at": "2026-06-19T00:00:00Z",
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return task_path


def goal2_task_payload(stage: str) -> dict:
    payload = valid_task_payload()
    payload["task_id"] = f"harness-v2-goal2-{stage}"
    payload["title"] = f"Validate Goal 2 transition from {stage}"
    payload["workflow_stage"] = stage
    payload["approval"]["packet"] = f"Approve exact Goal 2 {stage} transition test"
    payload["approval"]["approved_paths"] = {
        "plan_approval": ["control\\approval.md", "control\\permission.md", "records\\stages\\plan-approval.md"],
        "plan_review": ["records\\stages\\plan-review.md"],
        "improvement": ["records\\stages\\improvement.md", "records\\handoff.md"],
    }.get(stage, ["control\\approval.md", "control\\permission.md", "records\\stages\\development-review.md", "records\\proof.md"])
    payload["permission"]["allowed_side_effects"] = {
        "plan_approval": ["local readback/search only"],
        "plan_review": ["local readback/search only"],
        "improvement": ["local file writes to stage record files"],
    }.get(stage, ["local readback/search only"])
    payload["proof"]["obligations"] = [f"{stage} transition evaluation checked"]
    return payload


def write_goal2_task(root: Path, *, stage: str) -> Path:
    (root / "contracts").mkdir(parents=True)
    (root / "control").mkdir(parents=True)
    (root / "records" / "stages").mkdir(parents=True)
    (root / "CURRENT.md").write_text(
        "\n".join(
            [
                "workflow: `remaining_completion_program`",
                "state: `workflow_realignment_review`",
                "substate: `goal2-test`",
            ]
        ),
        encoding="utf-8",
    )
    for relative_path in (
        "control\\approval.md",
        "control\\permission.md",
        "control\\proof.md",
        "records\\proof.md",
        "records\\stages\\spec.md",
        "records\\stages\\spec-review.md",
        "records\\stages\\plan.md",
        "records\\stages\\plan-review.md",
        "records\\stages\\plan-approval.md",
        "records\\stages\\development-review.md",
    ):
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {relative_path}\n", encoding="utf-8")
    task_path = root / "contracts" / "harness-task.json"
    task_path.write_text(json.dumps(goal2_task_payload(stage), indent=2, sort_keys=True), encoding="utf-8")
    return task_path


def write_goal3_freshness_map(root: Path, anchors: list[dict]) -> Path:
    map_path = root / "records" / "freshness-map.json"
    map_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.write_text(
        json.dumps({"schema_version": "0.1.8", "anchors": anchors}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return map_path


def goal3_anchor(
    anchor_id: str,
    path: str,
    source_sha256: str,
    *,
    affects: list[str],
    backtrack_target: str,
    reason: str,
    evidence_refs: list[dict[str, str]],
) -> dict:
    return {
        "id": anchor_id,
        "path": path,
        "source_sha256": source_sha256,
        "affects": affects,
        "backtrack_target": backtrack_target,
        "reason": reason,
        "evidence_refs": evidence_refs,
    }


def write_goal3_evidence(root: Path, relative_path: str, *source_hashes: str) -> dict[str, str]:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Freshness Evidence", *[f"source_sha256: {source_hash}" for source_hash in source_hashes]]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": relative_path, "sha256": sha256_file(path)}


def fresh_approval_decision_payload() -> dict:
    payload = json.loads(VALID_APPROVAL_DECISION.read_text(encoding="utf-8"))
    payload["source_refs"] = [
        {
            "path": "CURRENT.md",
            "sha256": sha256_file(ROOT / "CURRENT.md"),
        }
    ]
    return payload


def fresh_proof_receipt_payload() -> dict:
    payload = json.loads(VALID_PROOF_RECEIPT.read_text(encoding="utf-8"))
    payload["source_refs"] = [
        {
            "path": "CURRENT.md",
            "sha256": sha256_file(ROOT / "CURRENT.md"),
            "affects": ["proof predicate"],
        },
        {
            "path": "harness_v2\\decisions.py",
            "sha256": sha256_file(ROOT / "harness_v2" / "decisions.py"),
            "affects": ["implementation"],
        },
        {
            "path": "tests\\test_harness_v2.py",
            "sha256": sha256_file(ROOT / "tests" / "test_harness_v2.py"),
            "affects": ["tests"],
        },
        {
            "path": "tests\\fixtures\\valid-task.json",
            "sha256": sha256_file(ROOT / "tests" / "fixtures" / "valid-task.json"),
            "affects": ["proof command"],
        },
    ]
    return payload


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_task_payload() -> dict:
    return json.loads(VALID_TASK.read_text())


def npm_executable() -> str:
    return "npm.cmd" if sys.platform == "win32" else "npm"


if __name__ == "__main__":
    unittest.main()
