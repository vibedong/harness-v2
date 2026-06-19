from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .modes import evaluate_mode


CURRENT_SURFACES = (
    "AGENTS.md",
    "RULES.md",
    "CURRENT.md",
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
)
DEFAULT_KNOWN_STATES = frozenset(
    {
        "scaffold_only",
        "planning_artifact_complete",
        "product_markdown_mvp_authoring",
        "product_markdown_mvp_review",
        "executable_mvp_authoring",
        "executable_mvp_review",
        "package_publish_authoring",
        "package_publish_review",
        "package_candidate_ready",
        "workflow_realignment_authoring",
        "workflow_realignment_review",
        "blocked",
        "deferred",
    }
)
REQUIRED_TASK_OBJECTS = (
    "source",
    "approval",
    "permission",
    "proof",
    "lifecycle",
)
WORKFLOW_STAGES = frozenset(
    {
        "spec",
        "spec_review",
        "plan",
        "plan_review",
        "plan_approval",
        "development",
        "development_review",
        "improvement",
    }
)
LEGACY_STAGE_ALIASES = {
    "planning": "plan",
    "approval": "plan_approval",
}
SPEC_PATHS = {"records\\current-task.md", "records\\stages\\spec.md", "records\\decisions.md"}
SPEC_REVIEW_PATHS = {"records\\stages\\spec-review.md", "records\\decisions.md"}
PLAN_PATHS = {"records\\stages\\plan.md", "records\\decisions.md"}
PLAN_REVIEW_PATHS = {"records\\stages\\plan-review.md", "records\\decisions.md"}
PLAN_APPROVAL_PATHS = {"control\\approval.md", "records\\stages\\plan-approval.md", "records\\decisions.md"}
DEVELOPMENT_REVIEW_PATHS = {"records\\stages\\development-review.md", "records\\proof.md", "records\\decisions.md"}
IMPROVEMENT_PATHS = {
    "records\\stages\\improvement.md",
    "records\\decisions.md",
    "records\\handoff.md",
    "safety\\regression.md",
    "safety\\improvement.md",
}
PRODUCT_IMPLEMENTATION_PREFIXES = (
    "harness_v2\\",
    "contracts\\",
    "tests\\",
    "bin\\",
    "_build_backend\\",
)
PRODUCT_IMPLEMENTATION_FILES = {
    "package.json",
    "pyproject.toml",
    "license",
    "release_notes.md",
    ".gitignore",
    ".gitattributes",
}
MUTATING_SIDE_EFFECT_FRAGMENTS = (
    "write",
    "modify",
    "create",
    "delete",
    "remove",
    "move",
    "rename",
    "commit",
    "push",
    "publish",
    "release",
    "tag",
    "deploy",
    "install",
    "secret",
    "external network mutation",
    "destructive",
    "npm pack",
)
RECORD_SIDE_EFFECT_FRAGMENTS = (
    "stage record",
    "record file",
    "records\\",
    "records/",
)
RELEASE_EXECUTION_FRAGMENTS = (
    "npm publish",
    "python package registry publish",
    "github release",
    "release tag",
    "release execution",
    "deploy",
)
REQUIRED_RELEASE_DENIALS = (
    "npm publish",
    "Python package registry publish",
    "GitHub release creation",
    "release tag creation",
)
CORE_DENIED_FRAGMENTS = (
    "publish",
    "release",
    "dependency install",
    "secret",
    "external network mutation",
    "destructive",
)
BROAD_APPROVAL_PACKETS = {"go ahead", "ok", "okay", "approved", "do it", "all approved"}
INITIAL_TASK_PATH = "contracts\\harness-task.json"


def _scaffold_files() -> tuple[tuple[tuple[str, ...], str], ...]:
    return (
        (("AGENTS.md",), _agents_md()),
        (("RULES.md",), _rules_md()),
        (("CURRENT.md",), _current_md()),
        (("control", "source.md"), _source_md()),
        (("control", "approval.md"), _approval_md()),
        (("control", "permission.md"), _permission_md()),
        (("control", "proof.md"), _proof_md()),
        (("control", "lifecycle.md"), _lifecycle_md()),
        (("records", "README.md"), _records_readme_md()),
        (("records", "current-task.md"), _current_task_md()),
        (("records", "stages", "spec.md"), _stage_record_md("Spec")),
        (("records", "stages", "spec-review.md"), _stage_record_md("Spec Review")),
        (("records", "stages", "plan.md"), _stage_record_md("Plan")),
        (("records", "stages", "plan-review.md"), _stage_record_md("Plan Review")),
        (("records", "stages", "plan-approval.md"), _stage_record_md("Plan Approval")),
        (("records", "stages", "development.md"), _stage_record_md("Development")),
        (("records", "stages", "development-review.md"), _stage_record_md("Development Review")),
        (("records", "stages", "improvement.md"), _stage_record_md("Improvement")),
        (("records", "decisions.md"), _decisions_md()),
        (("records", "proof.md"), _records_proof_md()),
        (("records", "handoff.md"), _handoff_md()),
        (("contracts", "harness-task.json"), _initial_task_json()),
        (("templates", "task.json"), _task_template_json()),
    )


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    task_id: str | None
    errors: tuple[str, ...]
    current_gate: str | None = None
    task_mode: str | None = None
    record_strength: str | None = None
    effective_record_strength: str | None = None
    classification_required: bool | None = None
    compatibility_mode: bool = True
    gate_state: dict[str, Any] | None = None
    freshness: dict[str, Any] | None = None
    mode_profile: dict[str, Any] | None = None


@dataclass(frozen=True)
class InitResult:
    ok: bool
    requested_root: str
    root: str
    initial_task: str
    created: tuple[str, ...]
    skipped: tuple[str, ...]
    overwritten: tuple[str, ...]
    redirected_from_package_root: bool
    errors: tuple[str, ...] = ()

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "requested_root": self.requested_root,
            "root": self.root,
            "initial_task": self.initial_task,
            "created": list(self.created),
            "skipped": list(self.skipped),
            "overwritten": list(self.overwritten),
            "redirected_from_package_root": self.redirected_from_package_root,
            "errors": list(self.errors),
            "next": [
                "harness-v2 status --root .",
                f"harness-v2 verify {self.initial_task}",
                f"harness-v2 gate {self.initial_task} --root .",
                "harness-v2 doctor --root .",
            ],
        }


@dataclass(frozen=True)
class TaskStartResult:
    ok: bool
    root: str
    task: str
    task_id: str | None
    written: tuple[str, ...]
    errors: tuple[str, ...] = ()

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "root": self.root,
            "task": self.task,
            "task_id": self.task_id,
            "written": list(self.written),
            "errors": list(self.errors),
            "next": [
                "harness-v2 status --root .",
                f"harness-v2 verify {self.task}",
                f"harness-v2 gate {self.task} --root .",
            ],
        }


def load_json(path: str | Path) -> dict[str, Any]:
    payload_path = Path(path)
    with payload_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{payload_path} must contain a JSON object")
    return data


def validate_task_file(path: str | Path) -> ValidationResult:
    payload_path = Path(path)
    try:
        data = load_json(payload_path)
    except Exception as exc:  # pragma: no cover - exact parser messages vary.
        return ValidationResult(False, None, (f"json: {exc}",))
    return validate_task(data, root=_find_project_root(payload_path), task_path=payload_path)


def initialize_project(root: str | Path, force: bool = False) -> InitResult:
    requested_root = Path(root).resolve()
    redirected = _looks_like_harness_package_root(requested_root)
    if _looks_like_harness_source_checkout(requested_root) and not redirected:
        error = (
            "target appears to be a HARNESS V2 source checkout, not an applied project root; "
            "do not git clone vibedong/harness-v2 into the project folder. "
            "Install the CLI with `npm install -g harness-v2@latest`, then run "
            "`harness-v2 init --root <project>` in the real project root."
        )
        return InitResult(
            ok=False,
            requested_root=str(requested_root),
            root=str(requested_root),
            initial_task=INITIAL_TASK_PATH,
            created=(),
            skipped=(),
            overwritten=(),
            redirected_from_package_root=False,
            errors=(error,),
        )
    root_path = requested_root.parent if redirected else requested_root
    root_path.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    skipped: list[str] = []
    overwritten: list[str] = []

    for parts, content in _scaffold_files():
        target = root_path.joinpath(*parts)
        relative_path = _display_path(parts)
        if target.exists() and not force:
            skipped.append(relative_path)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            overwritten.append(relative_path)
        else:
            created.append(relative_path)
        target.write_text(content, encoding="utf-8")

    return InitResult(
        ok=True,
        requested_root=str(requested_root),
        root=str(root_path.resolve()),
        initial_task=INITIAL_TASK_PATH,
        created=tuple(created),
        skipped=tuple(skipped),
        overwritten=tuple(overwritten),
        redirected_from_package_root=redirected,
    )


def start_task(
    root: str | Path,
    *,
    title: str,
    summary: str = "",
    workflow: str | None = None,
    stage: str = "spec",
    source_basis: list[str] | None = None,
    force: bool = False,
) -> TaskStartResult:
    root_path = Path(root).resolve()
    current_path = root_path / "CURRENT.md"
    task_path = root_path / "contracts" / "harness-task.json"
    current_task_path = root_path / "records" / "current-task.md"

    if not current_path.exists() or not task_path.exists():
        return TaskStartResult(
            ok=False,
            root=str(root_path),
            task=INITIAL_TASK_PATH,
            task_id=None,
            written=(),
            errors=("HARNESS V2 scaffold is missing; run `harness-v2 init --root <project>` first",),
        )

    normalized_title = _one_line(title)
    if not normalized_title:
        return TaskStartResult(
            ok=False,
            root=str(root_path),
            task=INITIAL_TASK_PATH,
            task_id=None,
            written=(),
            errors=("task title must be a non-empty string",),
        )

    try:
        current = read_current_status(root_path)
    except Exception as exc:
        return TaskStartResult(
            ok=False,
            root=str(root_path),
            task=INITIAL_TASK_PATH,
            task_id=None,
            written=(),
            errors=(f"current status: {exc}",),
        )

    try:
        existing_task = load_json(task_path)
    except Exception as exc:
        return TaskStartResult(
            ok=False,
            root=str(root_path),
            task=INITIAL_TASK_PATH,
            task_id=None,
            written=(),
            errors=(f"task json: {exc}",),
        )

    previous_current_text = current_path.read_text(encoding="utf-8")
    previous_task_text = task_path.read_text(encoding="utf-8")
    previous_current_task_text = current_task_path.read_text(encoding="utf-8") if current_task_path.exists() else None

    if not force and not _is_initial_task_binding(existing_task, current):
        return TaskStartResult(
            ok=False,
            root=str(root_path),
            task=INITIAL_TASK_PATH,
            task_id=_string_value(existing_task.get("task_id")) or None,
            written=(),
            errors=("active task already registered; pass --force to replace the current task contract",),
        )

    if stage not in WORKFLOW_STAGES:
        return TaskStartResult(
            ok=False,
            root=str(root_path),
            task=INITIAL_TASK_PATH,
            task_id=None,
            written=(),
            errors=(f"workflow stage is not known: {stage}",),
        )
    if stage != "spec":
        return TaskStartResult(
            ok=False,
            root=str(root_path),
            task=INITIAL_TASK_PATH,
            task_id=None,
            written=(),
            errors=("task start currently registers new work at the spec stage only",),
        )

    selected_workflow = workflow.strip() if isinstance(workflow, str) and workflow.strip() else current["workflow"]
    task_id = _task_id_from_title(normalized_title)
    source_items = _dedupe_strings(["AGENTS.md", "RULES.md", "CURRENT.md", *(source_basis or [])])
    summary_text = _one_line(summary) or "User requested task registered through HARNESS V2 task start."
    task_data = _registered_task_json(task_id, normalized_title, summary_text, selected_workflow, stage, source_items)

    current_path.write_text(_registered_current_md(normalized_title, summary_text, selected_workflow), encoding="utf-8")
    task_path.write_text(json.dumps(task_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    current_task_path.parent.mkdir(parents=True, exist_ok=True)
    current_task_path.write_text(_registered_current_task_md(task_id, normalized_title, summary_text, stage, source_items), encoding="utf-8")

    validation = validate_task(task_data, root=root_path, task_path=task_path)
    if not validation.ok:
        current_path.write_text(previous_current_text, encoding="utf-8")
        task_path.write_text(previous_task_text, encoding="utf-8")
        if previous_current_task_text is None:
            if current_task_path.exists():
                current_task_path.unlink()
        else:
            current_task_path.write_text(previous_current_task_text, encoding="utf-8")
        return TaskStartResult(
            ok=False,
            root=str(root_path),
            task=INITIAL_TASK_PATH,
            task_id=task_id,
            written=(),
            errors=validation.errors,
        )

    return TaskStartResult(
        ok=True,
        root=str(root_path),
        task=INITIAL_TASK_PATH,
        task_id=task_id,
        written=("CURRENT.md", INITIAL_TASK_PATH, "records\\current-task.md"),
    )


def validate_task(data: dict[str, Any], root: str | Path | None = None, task_path: str | Path | None = None) -> ValidationResult:
    errors: list[str] = []
    task_id = data.get("task_id")
    root_path = Path(root) if root is not None else None
    validated_task_path = Path(task_path) if task_path is not None else None
    compatibility_mode = not _is_strict_task_contract(data)
    workflow_stage = data.get("workflow_stage")
    gate_state = _validate_gate_state(root_path, validated_task_path, data, errors)
    freshness = _validate_freshness(root_path, errors)
    current_gate = _derive_current_gate(data, gate_state)
    mode = evaluate_mode(data, workflow_stage if isinstance(workflow_stage, str) else None, compatibility_mode, freshness=freshness)
    errors.extend(mode.errors)

    for key in ("task_id", "title", "workflow"):
        if not _non_empty_string(data.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if not _non_empty_string(data.get("workflow_stage")):
        errors.append("workflow_stage must be a non-empty string")

    for key in REQUIRED_TASK_OBJECTS:
        if not isinstance(data.get(key), dict):
            errors.append(f"{key} must be an object")

    source = data.get("source") if isinstance(data.get("source"), dict) else {}
    if not _non_empty_list(source.get("basis")):
        errors.append("source.basis must be a non-empty list")
    if not _non_empty_string(source.get("current_pointer")):
        errors.append("source.current_pointer must be a non-empty string")
    elif source.get("current_pointer") != "CURRENT.md":
        errors.append("source.current_pointer must be CURRENT.md")
    if _non_empty_list(source.get("basis")) and not _contains_normalized(_string_list(source.get("basis")), "CURRENT.md"):
        errors.append("source.basis must include CURRENT.md")

    approval = data.get("approval") if isinstance(data.get("approval"), dict) else {}
    if not _non_empty_string(approval.get("packet")):
        errors.append("approval.packet must be a non-empty string")
    if not _non_empty_list(approval.get("approved_paths")):
        errors.append("approval.approved_paths must be a non-empty list")

    permission = data.get("permission") if isinstance(data.get("permission"), dict) else {}
    if not _non_empty_list(permission.get("allowed_side_effects")):
        errors.append("permission.allowed_side_effects must be a non-empty list")
    if not _non_empty_list(permission.get("denied_side_effects")):
        errors.append("permission.denied_side_effects must be a non-empty list")

    proof = data.get("proof") if isinstance(data.get("proof"), dict) else {}
    if not _non_empty_list(proof.get("obligations")):
        errors.append("proof.obligations must be a non-empty list")

    lifecycle = data.get("lifecycle") if isinstance(data.get("lifecycle"), dict) else {}
    if not _non_empty_string(lifecycle.get("current_state")):
        errors.append("lifecycle.current_state must be a non-empty string")
    if not _non_empty_string(lifecycle.get("target_state")):
        errors.append("lifecycle.target_state must be a non-empty string")

    _validate_current_context(data, root_path, errors)
    _validate_goal0_compatibility_fields(data, compatibility_mode, errors)
    _validate_workflow_stage(data, errors)
    _validate_proof_receipt_requirement(data, root_path, errors)

    return ValidationResult(
        ok=not errors,
        task_id=task_id if isinstance(task_id, str) else None,
        errors=tuple(errors),
        current_gate=current_gate,
        task_mode=mode.task_mode,
        record_strength=mode.record_strength,
        effective_record_strength=mode.effective_record_strength,
        classification_required=mode.classification_required,
        compatibility_mode=compatibility_mode,
        gate_state=gate_state,
        freshness=freshness,
        mode_profile=mode.to_json(),
    )


def read_current_status(root: str | Path) -> dict[str, str]:
    current_path = Path(root) / "CURRENT.md"
    result: dict[str, str] = {}
    for raw_line in current_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("workflow:"):
            result["workflow"] = _backtick_value(line)
        elif line.startswith("state:"):
            result["state"] = _backtick_value(line)
        elif line.startswith("substate:"):
            result["substate"] = _backtick_value(line)
    missing = {"workflow", "state", "substate"} - result.keys()
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"CURRENT.md missing {missing_text}")
    return result


def project_shape(root: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    files = [path for path in root_path.rglob("*") if path.is_file() and not _is_generated_or_vcs_path(path)]
    dirs = [path for path in root_path.iterdir() if path.is_dir() and not _is_generated_or_vcs_path(path)]
    forbidden = [
        name
        for name in ("skills",)
        if (root_path / name).exists()
    ]
    return {
        "file_count": len(files),
        "markdown_count": len([path for path in files if path.suffix == ".md"]),
        "non_markdown_count": len([path for path in files if path.suffix != ".md"]),
        "first_level_dirs": sorted(path.name for path in dirs),
        "forbidden_dirs": forbidden,
    }


def _is_generated_or_vcs_path(path: Path) -> bool:
    parts = set(path.parts)
    name = path.name
    return (
        ".git" in parts
        or "__pycache__" in parts
        or any(part.endswith(".egg-info") for part in parts)
        or name.endswith(".pyc")
        or name.endswith(".tgz")
    )


def _backtick_value(line: str) -> str:
    first = line.find("`")
    last = line.rfind("`")
    if first == -1 or last <= first:
        raise ValueError(f"expected backtick value in line: {line}")
    return line[first + 1:last]


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def _is_strict_task_contract(data: dict[str, Any]) -> bool:
    version = data.get("contract_version")
    return isinstance(version, str) and version.strip() not in {"", "0.1.7"}


def _derive_current_gate(data: dict[str, Any], gate_state: dict[str, Any] | None = None) -> str | None:
    current_gate = data.get("current_gate")
    if isinstance(current_gate, str) and current_gate.strip():
        return current_gate
    if gate_state and gate_state.get("present") and isinstance(gate_state.get("derived_current_gate"), str):
        return gate_state["derived_current_gate"]
    workflow_stage = data.get("workflow_stage")
    if isinstance(workflow_stage, str) and workflow_stage.strip():
        return workflow_stage
    return None


def _validate_freshness(root: Path | None, errors: list[str]) -> dict[str, Any]:
    if root is None:
        return {
            "ok": True,
            "present": False,
            "stale": [],
            "errors": [],
            "compatibility_diagnostic": "freshness map is absent; compatibility mode keeps verification read-only and does not overwrite existing projects",
        }
    from .freshness import evaluate_freshness_map

    result = evaluate_freshness_map(root)
    for item in result.stale:
        errors.append(f"freshness stale: {item['anchor_id']} -> {item['backtrack_target']}: {item['reason']}")
        for evidence_error in item.get("evidence_errors", []):
            errors.append(f"freshness stale evidence: {item['anchor_id']}: {evidence_error}")
    for error in result.errors:
        errors.append(f"freshness: {error}")
    return result.to_json()


def _validate_gate_state(root: Path | None, task_path: Path | None, data: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    status: dict[str, Any] = {"present": False, "derived_from": "workflow_stage"}
    if root is None:
        return status

    gate_state_path = root / "records" / "gate-state.json"
    if not gate_state_path.exists():
        return status

    status["present"] = True
    try:
        payload = load_json(gate_state_path)
    except Exception as exc:
        errors.append(f"gate-state json: {exc}")
        return status

    status.update(
        {
            "schema_version": payload.get("schema_version"),
            "source_task_ref": payload.get("source_task_ref"),
            "derived_current_gate": payload.get("derived_current_gate"),
            "derived_from": payload.get("derived_from"),
            "generated_at": payload.get("generated_at"),
        }
    )

    for key in ("schema_version", "source_task_ref", "source_sha256", "derived_current_gate", "derived_from", "generated_at"):
        if not _non_empty_string(payload.get(key)):
            errors.append(f"gate-state {key} must be a non-empty string")

    derived_from = payload.get("derived_from")
    if isinstance(derived_from, str) and derived_from != "workflow_stage":
        errors.append("gate-state derived_from must be workflow_stage")

    derived_current_gate = payload.get("derived_current_gate")
    workflow_stage = data.get("workflow_stage")
    if isinstance(derived_current_gate, str):
        if derived_current_gate in LEGACY_STAGE_ALIASES:
            errors.append(
                f"gate-state derived_current_gate uses legacy alias {derived_current_gate!r}; use {LEGACY_STAGE_ALIASES[derived_current_gate]!r}"
            )
        elif derived_current_gate not in WORKFLOW_STAGES:
            errors.append(f"gate-state derived_current_gate is not a known stage: {derived_current_gate}")
        elif workflow_stage in WORKFLOW_STAGES and derived_current_gate != workflow_stage:
            errors.append("gate-state derived_current_gate must match workflow_stage")

    source_task_ref = payload.get("source_task_ref")
    source_sha256 = payload.get("source_sha256")
    if isinstance(source_task_ref, str) and source_task_ref.strip():
        source_path = _resolve_project_relative_path(root, source_task_ref, "gate-state source_task_ref", errors)
        if source_path is not None and source_path.exists():
            if task_path is None:
                errors.append("gate-state source_task_ref cannot be verified without validated task path")
            elif source_path.resolve() != task_path.resolve():
                errors.append("gate-state source_task_ref must match validated task path")
            try:
                source_task = load_json(source_path)
            except Exception as exc:
                errors.append(f"gate-state source_task_ref json: {exc}")
                source_task = {}
            source_workflow_stage = source_task.get("workflow_stage")
            status["source_workflow_stage"] = source_workflow_stage
            if isinstance(derived_current_gate, str) and isinstance(source_workflow_stage, str) and derived_current_gate != source_workflow_stage:
                errors.append("gate-state derived_current_gate must match source_task_ref workflow_stage")
            actual_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
            status["source_sha256"] = source_sha256
            if isinstance(source_sha256, str) and source_sha256 != actual_hash:
                errors.append("gate-state source_sha256 does not match source_task_ref")
        elif source_path is not None:
            errors.append("gate-state source_task_ref does not exist")

    return status


def _resolve_project_relative_path(root: Path, value: str, label: str, errors: list[str]) -> Path | None:
    candidate = (root / value).resolve()
    root_resolved = root.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        errors.append(f"{label} must stay under project root")
        return None
    return candidate


def _validate_goal0_compatibility_fields(data: dict[str, Any], compatibility_mode: bool, errors: list[str]) -> None:
    workflow_stage = data.get("workflow_stage")
    current_gate = data.get("current_gate")

    if current_gate is not None:
        if not _non_empty_string(current_gate):
            errors.append("current_gate must be a non-empty string when present")
        elif current_gate in LEGACY_STAGE_ALIASES:
            errors.append(
                f"current_gate uses legacy alias {current_gate!r}; use {LEGACY_STAGE_ALIASES[current_gate]!r}"
            )
        elif current_gate not in WORKFLOW_STAGES:
            errors.append(f"current_gate is not a known stage: {current_gate}")
        elif workflow_stage in WORKFLOW_STAGES and current_gate != workflow_stage:
            errors.append("current_gate must match workflow_stage when present")


def _validate_current_context(data: dict[str, Any], root: Path | None, errors: list[str]) -> None:
    approval = data.get("approval") if isinstance(data.get("approval"), dict) else {}
    permission = data.get("permission") if isinstance(data.get("permission"), dict) else {}
    lifecycle = data.get("lifecycle") if isinstance(data.get("lifecycle"), dict) else {}

    allowed_side_effects = _string_list(permission.get("allowed_side_effects"))
    denied_side_effects = _string_list(permission.get("denied_side_effects"))
    excluded_side_effects = _string_list(approval.get("excluded_side_effects"))

    _reject_side_effect_conflicts(
        allowed_side_effects,
        denied_side_effects,
        "permission side effect conflicts with denied side effect",
        errors,
    )
    _reject_side_effect_conflicts(
        allowed_side_effects,
        excluded_side_effects,
        "permission side effect conflicts with approval exclusion",
        errors,
    )
    _reject_author_local_status_commands(allowed_side_effects, errors)

    known_states = _known_lifecycle_states(root)
    for key in ("current_state", "target_state"):
        state = lifecycle.get(key)
        if isinstance(state, str) and state not in known_states:
            errors.append(f"lifecycle.{key} is not a known state: {state}")

    if root is None:
        return

    try:
        current = read_current_status(root)
    except Exception as exc:
        errors.append(f"current status: {exc}")
        current = {}

    workflow = data.get("workflow")
    current_workflow = current.get("workflow")
    if isinstance(workflow, str) and current_workflow and workflow != current_workflow:
        errors.append(f"workflow must match CURRENT.md workflow {current_workflow}")

    current_state = current.get("state")
    lifecycle_current_state = lifecycle.get("current_state")
    if isinstance(lifecycle_current_state, str) and current_state and lifecycle_current_state != current_state:
        errors.append(f"lifecycle.current_state must match CURRENT.md state {current_state}")

    errors.extend(_stale_status_errors(root))


def _validate_workflow_stage(data: dict[str, Any], errors: list[str]) -> None:
    stage = data.get("workflow_stage")
    if not isinstance(stage, str) or not stage.strip():
        return
    if stage in LEGACY_STAGE_ALIASES:
        errors.append(f"workflow_stage uses legacy alias {stage!r}; use {LEGACY_STAGE_ALIASES[stage]!r}")
        return
    if stage not in WORKFLOW_STAGES:
        errors.append(f"workflow_stage is not a known stage: {stage}")
        return

    approval = data.get("approval") if isinstance(data.get("approval"), dict) else {}
    permission = data.get("permission") if isinstance(data.get("permission"), dict) else {}
    proof = data.get("proof") if isinstance(data.get("proof"), dict) else {}
    lifecycle = data.get("lifecycle") if isinstance(data.get("lifecycle"), dict) else {}
    task_mode = data.get("task_mode")

    approved_paths = _string_list(approval.get("approved_paths"))
    allowed_side_effects = _string_list(permission.get("allowed_side_effects"))
    denied_side_effects = _string_list(permission.get("denied_side_effects"))
    proof_obligations = _string_list(proof.get("obligations"))

    _reject_broad_approved_paths(approved_paths, errors)
    _reject_missing_core_denials(denied_side_effects, errors)

    if stage == "spec":
        _reject_path_set_outside("spec", approved_paths, SPEC_PATHS, errors)
        _reject_non_record_side_effects(stage, allowed_side_effects, errors)
    elif stage == "spec_review":
        _reject_path_set_outside("spec_review", approved_paths, SPEC_REVIEW_PATHS, errors)
        _reject_non_record_side_effects(stage, allowed_side_effects, errors)
        if lifecycle.get("current_state") != lifecycle.get("target_state"):
            errors.append("spec_review stage cannot move lifecycle state")
        _reject_claimed_authority(stage, proof_obligations, ("approval", "permission", "lifecycle transition"), errors)
    elif stage == "plan":
        _reject_path_set_outside("plan", approved_paths, PLAN_PATHS, errors)
        _reject_non_record_side_effects(stage, allowed_side_effects, errors)
    elif stage == "plan_review":
        _reject_path_set_outside("plan_review", approved_paths, PLAN_REVIEW_PATHS, errors)
        _reject_non_record_side_effects(stage, allowed_side_effects, errors)
        if lifecycle.get("current_state") != lifecycle.get("target_state"):
            errors.append("plan_review stage cannot move lifecycle state")
        _reject_claimed_authority(stage, proof_obligations, ("approval", "permission", "proof result", "lifecycle transition"), errors)
    elif stage == "plan_approval":
        _reject_path_set_outside("plan_approval", approved_paths, PLAN_APPROVAL_PATHS, errors)
        packet = approval.get("packet")
        if isinstance(packet, str) and _normalize_side_effect(packet) in BROAD_APPROVAL_PACKETS:
            errors.append("plan_approval stage requires an exact approval packet, not a broad approval phrase")
        if not _non_empty_list(approval.get("excluded_side_effects")):
            errors.append("plan_approval stage requires approval.excluded_side_effects")
    elif stage == "development":
        if task_mode != "read_only_analysis" and not any(_contains_fragment(value, ("write", "modify", "create")) for value in allowed_side_effects):
            errors.append("development stage requires an explicit local write side effect")
        _reject_release_execution_side_effects(stage, allowed_side_effects, errors)
    elif stage == "development_review":
        _reject_path_set_outside("development_review", approved_paths, DEVELOPMENT_REVIEW_PATHS, errors)
        _reject_non_record_side_effects(stage, allowed_side_effects, errors)
        if lifecycle.get("current_state") != lifecycle.get("target_state"):
            errors.append("development_review stage cannot move lifecycle state")
        _reject_claimed_authority(stage, proof_obligations, ("proof result", "lifecycle transition", "release readiness"), errors)
    elif stage == "improvement":
        _reject_path_set_outside("improvement", approved_paths, IMPROVEMENT_PATHS, errors)
        _reject_product_implementation_paths(stage, approved_paths, errors)
        _reject_non_record_side_effects(stage, allowed_side_effects, errors)
        _reject_release_execution_side_effects(stage, allowed_side_effects, errors)


def _validate_proof_receipt_requirement(data: dict[str, Any], root: Path | None, errors: list[str]) -> None:
    proof = data.get("proof") if isinstance(data.get("proof"), dict) else {}
    if proof.get("receipt_required") is not True:
        return
    receipt_refs = _string_list(proof.get("receipts"))
    if not receipt_refs:
        errors.append("proof receipt required but proof.receipts is empty")
        return
    if root is None:
        errors.append("proof receipt validation requires project root")
        return

    from .decisions import evaluate_decision_file

    for receipt_ref in receipt_refs:
        receipt_path = _resolve_project_relative_path(root, receipt_ref, "proof.receipts", errors)
        if receipt_path is None:
            continue
        if not receipt_path.exists():
            errors.append(f"proof receipt does not exist: {receipt_ref}")
            continue
        result = evaluate_decision_file(receipt_path, task=data, root=root)
        if result.kind != "ProofReceipt":
            errors.append(f"proof receipt {receipt_ref}: expected ProofReceipt, got {result.kind or '<missing>'}")
        if not result.ok:
            errors.extend(f"proof receipt {receipt_ref}: {error}" for error in result.errors)
            errors.extend(f"proof receipt {receipt_ref}: stale source ref {item.get('path')}" for item in result.stale)


def _reject_broad_approved_paths(paths: list[str], errors: list[str]) -> None:
    for value in paths:
        normalized = _normalize_path(value)
        if (
            not normalized
            or normalized in {".", "\\", "/", "<repo root>"}
            or "*" in normalized
            or normalized.endswith(":\\")
            or normalized.casefold() == "f:\\folder\\harness-v2"
        ):
            errors.append(f"approval.approved_paths contains broad path: {value}")


def _reject_missing_core_denials(denied_side_effects: list[str], errors: list[str]) -> None:
    for fragment in CORE_DENIED_FRAGMENTS:
        if not any(_contains_fragment(value, (fragment,)) for value in denied_side_effects):
            errors.append(f"permission.denied_side_effects must include denial for: {fragment}")


def _reject_paths_outside(stage: str, paths: list[str], prefixes: tuple[str, ...], errors: list[str]) -> None:
    for value in paths:
        normalized = _normalize_path(value)
        if not any(normalized.startswith(prefix) for prefix in prefixes):
            errors.append(f"{stage} stage approved path is outside allowed prefixes: {value}")


def _reject_path_set_outside(stage: str, paths: list[str], allowed_paths: set[str], errors: list[str]) -> None:
    for value in paths:
        normalized = _normalize_path(value)
        if normalized not in allowed_paths:
            errors.append(f"{stage} stage approved path is outside allowed surface: {value}")


def _reject_product_implementation_paths(stage: str, paths: list[str], errors: list[str]) -> None:
    for value in paths:
        normalized = _normalize_path(value)
        if normalized in PRODUCT_IMPLEMENTATION_FILES or any(
            normalized.startswith(prefix) for prefix in PRODUCT_IMPLEMENTATION_PREFIXES
        ):
            errors.append(f"{stage} stage cannot approve product implementation path: {value}")


def _reject_mutating_stage_side_effects(stage: str, side_effects: list[str], errors: list[str]) -> None:
    for value in side_effects:
        if _contains_fragment(value, MUTATING_SIDE_EFFECT_FRAGMENTS):
            errors.append(f"{stage} stage cannot allow mutating side effect: {value}")


def _reject_non_record_side_effects(stage: str, side_effects: list[str], errors: list[str]) -> None:
    for value in side_effects:
        if not _contains_fragment(value, MUTATING_SIDE_EFFECT_FRAGMENTS):
            continue
        if _contains_fragment(value, RECORD_SIDE_EFFECT_FRAGMENTS):
            continue
        errors.append(f"{stage} stage cannot allow non-record side effect: {value}")


def _reject_release_execution_side_effects(stage: str, side_effects: list[str], errors: list[str]) -> None:
    for value in side_effects:
        if _contains_fragment(value, RELEASE_EXECUTION_FRAGMENTS):
            errors.append(f"{stage} stage cannot allow release execution side effect: {value}")


def _reject_claimed_authority(stage: str, values: list[str], fragments: tuple[str, ...], errors: list[str]) -> None:
    for value in values:
        if _contains_fragment(value, fragments):
            errors.append(f"{stage} stage cannot claim authority from review/route/artifact material: {value}")


def _reject_side_effect_conflicts(
    allowed: list[str],
    denied: list[str],
    message: str,
    errors: list[str],
) -> None:
    denied_by_normalized = {_normalize_side_effect(value): value for value in denied}
    for value in allowed:
        if _normalize_side_effect(value) in denied_by_normalized:
            errors.append(f"{message}: {denied_by_normalized[_normalize_side_effect(value)]}")


def _reject_author_local_status_commands(side_effects: list[str], errors: list[str]) -> None:
    for value in side_effects:
        normalized = value.lower()
        if "python -m harness_v2 status" in normalized and "--root " in normalized and ":\\folder\\harness-v2" in normalized:
            errors.append("status command must use --root <repo root> or --root .")


def _known_lifecycle_states(root: Path | None) -> frozenset[str]:
    if root is None:
        return DEFAULT_KNOWN_STATES
    lifecycle_path = root / "control" / "lifecycle.md"
    if not lifecycle_path.exists():
        return DEFAULT_KNOWN_STATES
    states: set[str] = set()
    for raw_line in lifecycle_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- `") and line.endswith("`"):
            states.add(line[3:-1])
    return frozenset(states) if states else DEFAULT_KNOWN_STATES


def _stale_status_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in CURRENT_SURFACES:
        path = root / relative_path
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line.startswith("status:") and "executable_local_mvp_surface / third_slice" in line:
                errors.append(f"stale status surface: {relative_path}")
    return errors


def _find_project_root(path: Path) -> Path | None:
    resolved = path.resolve()
    for candidate in (resolved.parent, *resolved.parents):
        if (candidate / "CURRENT.md").exists():
            return candidate
    return None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _normalize_side_effect(value: str) -> str:
    return " ".join(value.casefold().split())


def _normalize_path(value: str) -> str:
    normalized = value.strip().replace("/", "\\")
    while normalized.startswith(".\\"):
        normalized = normalized[2:]
    return normalized.casefold()


def _contains_fragment(value: str, fragments: tuple[str, ...]) -> bool:
    normalized = _normalize_side_effect(value)
    return any(fragment.casefold() in normalized for fragment in fragments)


def _contains_normalized(values: list[str], expected: str) -> bool:
    expected_normalized = _normalize_side_effect(expected)
    return any(_normalize_side_effect(value) == expected_normalized for value in values)


def is_harness_source_checkout(path: str | Path) -> bool:
    return _looks_like_harness_source_checkout(Path(path).resolve())


def _looks_like_harness_package_root(path: Path) -> bool:
    if path.name.casefold() not in {"harness-v2", "harness_v2"}:
        return False
    return _looks_like_harness_source_checkout(path)


def _looks_like_harness_source_checkout(path: Path) -> bool:
    if path.parent == path:
        return False
    package_json = path / "package.json"
    if not package_json.exists():
        return False
    if not (path / "harness_v2" / "core.py").exists():
        return False
    if not (path / "bin" / "harness-v2.js").exists():
        return False
    try:
        package_data = json.loads(package_json.read_text(encoding="utf-8"))
    except Exception:
        return False
    return package_data.get("name") == "harness-v2"


def _display_path(parts: tuple[str, ...]) -> str:
    return "\\".join(parts)


def _string_value(value: Any) -> str:
    return value if isinstance(value, str) and value.strip() else ""


def _one_line(value: str) -> str:
    return " ".join(value.split()) if isinstance(value, str) else ""


def _is_initial_task_binding(task: dict[str, Any], current: dict[str, str]) -> bool:
    return (
        task.get("task_id") == "harness-v2-initial-task"
        and task.get("task_mode") == "scaffold_only"
        and current.get("state") == "ready"
        and "initialized" in current.get("substate", "")
    )


def _task_id_from_title(title: str) -> str:
    chars: list[str] = []
    previous_separator = False
    for char in title.casefold():
        if char.isascii() and char.isalnum():
            chars.append(char)
            previous_separator = False
        elif not previous_separator:
            chars.append("-")
            previous_separator = True
    slug = "".join(chars).strip("-")
    if not slug:
        slug = "task-" + hashlib.sha256(title.encode("utf-8")).hexdigest()[:12]
    return slug[:80]


def _dedupe_strings(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = value.strip() if isinstance(value, str) else ""
        if not item:
            continue
        normalized = _normalize_side_effect(item)
        if normalized in seen:
            continue
        result.append(item)
        seen.add(normalized)
    return result


def _registered_task_json(
    task_id: str,
    title: str,
    summary: str,
    workflow: str,
    stage: str,
    source_basis: list[str],
) -> dict[str, Any]:
    if stage != "spec":
        raise ValueError("task start currently registers new work at the spec stage only")
    approved_paths = [
        "records\\current-task.md",
        "records\\stages\\spec.md",
        "records\\decisions.md",
    ]
    denied_side_effects = [
        "package publish",
        "release execution",
        "dependency install from network",
        "secret access",
        "external network mutation",
        "destructive operation",
    ]
    return {
        "task_id": task_id,
        "title": title,
        "workflow": workflow,
        "contract_version": "0.1.8",
        "workflow_stage": stage,
        "current_gate": stage,
        "task_mode": "planned_change",
        "record_strength": "strict",
        "risk_flags": [
            "user_task_request",
            "scope_pending",
        ],
        "proof_profile": "current",
        "capability_request": [
            "task_registration",
        ],
        "classification_required": True,
        "record_density": {
            "generated_file_count": 0,
            "required_read_set_size": min(3, len(source_basis)),
            "field_presence": "strict",
        },
        "source": {
            "basis": source_basis,
            "current_pointer": "CURRENT.md",
        },
        "approval": {
            "packet": f"Register user task request for specification only: {title}. {summary}",
            "approved_paths": approved_paths,
            "excluded_side_effects": denied_side_effects,
        },
        "permission": {
            "allowed_side_effects": [
                "local file writes to records\\current-task.md",
                "local file writes to records\\stages\\spec.md",
                "local file writes to records\\decisions.md",
                "harness-v2 status --root .",
                "harness-v2 verify contracts\\harness-task.json",
                "harness-v2 gate contracts\\harness-task.json --root .",
            ],
            "denied_side_effects": denied_side_effects,
        },
        "proof": {
            "obligations": [
                "task scope remains pending",
                "harness-v2 status --root .",
                "harness-v2 verify contracts\\harness-task.json",
                "harness-v2 gate contracts\\harness-task.json --root .",
            ],
        },
        "lifecycle": {
            "current_state": "active",
            "target_state": "active",
        },
    }


def _registered_current_md(title: str, summary: str, workflow: str) -> str:
    return f"""# HARNESS V2 Current State

status: applied_project_surface / task_registered / current_pointer

이 프로젝트 루트에는 HARNESS V2가 적용되어 있습니다. AI 에이전트는 `AGENTS.md`, `RULES.md`, 이 파일, `control\\`, `contracts\\harness-task.json`을 작업 경계로 사용해야 합니다.

현재 작업은 사용자의 요청에서 등록되었습니다. 이 등록은 작업을 보이게 만들고 검증 가능하게 만들지만, 구현, dependency, release, secret, external mutation, destructive action 같은 넓은 권한을 자동으로 열지 않습니다.

workflow: `{workflow}`

state: `active`

substate: `task_registered / scope_pending`

source basis:

- `AGENTS.md`
- `RULES.md`
- `CURRENT.md`
- `contracts\\harness-task.json`

## Current Task

title: {title}

summary: {summary}

현재 작업 계약은 `contracts\\harness-task.json`입니다.

실질적인 작업 전에 아래 명령을 실행합니다.

```powershell
harness-v2 status --root .
harness-v2 verify contracts\\harness-task.json
harness-v2 gate contracts\\harness-task.json --root .
```

등록된 계약은 `spec` 단계에서 시작하며 범위는 `scope_pending` 상태로 둡니다. 구현, package 작업, release, external mutation, dependency 설치, secret 접근, destructive action, 넓은 파일 쓰기 전에 정확한 approval, permission, proof, lifecycle 필드를 가진 amended task contract를 만들거나 받아야 합니다.

## Stop Conditions

요청된 작업이 active task contract 밖의 경로, 명령, side effect, secret, external mutation, dependency 변경, package publish, release execution, destructive operation을 필요로 하면 멈춥니다.
"""


def _registered_current_task_md(task_id: str, title: str, summary: str, stage: str, source_basis: list[str]) -> str:
    source_lines = "\n".join(f"- `{item}`" for item in source_basis)
    return f"""# 현재 작업 기록

task_id: `{task_id}`

title: {title}

workflow_stage: `{stage}`

status: registered / scope_pending

## 요약

{summary}

## Source Basis

{source_lines}

이 기록은 `contracts\\harness-task.json`을 사람이 읽기 쉽게 보조하는 파일입니다. 이 파일, `CURRENT.md`, task contract가 서로 다르면 `CURRENT.md`와 task contract가 우선합니다.
"""


def _agents_md() -> str:
    return """# HARNESS V2 에이전트 진입점

이 프로젝트에는 루트에 HARNESS V2가 적용되어 있습니다. 이 파일은 AI 에이전트가 작업을 시작할 때 읽는 진입점입니다.

적용된 표면은 scaffold, task contract validator, CLI helper입니다. 자동 enforcement sandbox, completion layer, approval engine, proof generator, lifecycle transition engine이 아닙니다.

HARNESS V2는 Codex 앱 중심 작업을 위해 hook-equivalent gate 명령을 제공합니다. `harness-v2 gate <task.json> --root .`는 `status`, `verify`, 선택적 `preflight`를 하나의 실행 가능한 경계 확인으로 묶습니다. 이 명령은 shell이나 editor 동작을 자동으로 차단하지 않습니다.

`README.md`는 사용자 설명서입니다. 사람에게 도구를 설명하지만 source authority, approval, permission, proof, lifecycle state, release authority를 부여하지 않습니다.

## 증거 수준에 맞춘 읽기 순서

일반적인 현재 작업은 아래만 먼저 읽습니다.

1. `RULES.md`
2. `CURRENT.md`
3. active task contract. 초기값은 `contracts\\harness-task.json`입니다.

그 다음에는 작업에 필요한 owner surface만 읽습니다. approval binding, permission-sensitive command, proof/completion claim, lifecycle movement, stale/conflicting state, release work, external mutation, destructive action, product implementation risk가 있으면 `control\\source.md`, `control\\approval.md`, `control\\permission.md`, `control\\proof.md`, `control\\lifecycle.md`의 정확한 원문까지 확장해서 읽습니다.

## 현재 작업 등록

사용자가 구체적인 작업을 요청했는데 `CURRENT.md`가 아직 initial scaffold pointer라면, 실질 작업 전에 그 요청을 등록합니다.

```powershell
harness-v2 task start --root . --title "<짧은 작업명>" --summary "<사용자 요청 요약>"
```

등록 후 `status`, `verify`, `gate`를 실행합니다. 사용자 요청만 보고 구현, dependency, package, release, secret, external mutation, destructive permission을 넓게 추론하지 않습니다. 정확한 amended task contract가 명시하기 전까지 닫아둡니다.

## 필수 사전 확인

파일 변경이나 side-effectful command 전에 아래를 실행합니다.

```powershell
harness-v2 status --root .
harness-v2 verify contracts\\harness-task.json
harness-v2 gate contracts\\harness-task.json --root .
harness-v2 doctor --root .
```

## 작업 경계

설치, `init`, `apply`, CLI 사용 가능 상태는 임의의 미래 작업을 승인하지 않습니다. `approval.approved_paths` 안에서만 움직입니다. `approval.excluded_side_effects` 또는 `permission.denied_side_effects`에 있는 작업은 실행하지 않습니다.

현재 사용자 요청이 active task contract와 맞지 않으면 파일 변경이나 side-effectful command 전에 멈추고 새 contract 또는 amended contract를 요청합니다.

완료를 말하려면 `proof.obligations`에 맞는 현재 proof가 필요합니다. 이전 채팅, README 문구, 생략한 검사, 설치 성공은 proof가 아닙니다.
"""


def _rules_md() -> str:
    return """# HARNESS V2 프로젝트 규칙

HARNESS V2는 AI 보조 작업의 현재 작업 경계를 기록합니다. HARNESS V2는 scaffold, task-contract validator, CLI helper입니다. 자동 enforcement sandbox, completion layer, approval engine, proof generator, lifecycle transition engine, editor, shell, network, release sandbox가 아닙니다.

local hook-equivalent gate는 명시적인 명령입니다: `harness-v2 gate <task.json> --root .`. 이 명령은 status, verify, 선택적 preflight를 통해 active task boundary를 확인합니다. 실제 Codex app hook을 설치하지 않고, shell이나 editor 동작을 자동으로 차단하지 않습니다.

README 파일은 사용자용 문서일 뿐입니다. README는 approval, permission, proof, lifecycle state, route authority, release readiness, package publish authority를 부여하지 않습니다.

## 필수 흐름

1. `CURRENT.md`를 읽습니다.
2. active task contract를 읽습니다.
3. 사용자 요청이 실제 작업이고 active contract가 아직 initial scaffold binding이면 `harness-v2 task start --root . --title "<짧은 작업명>" --summary "<사용자 요청 요약>"`을 실행합니다.
4. `harness-v2 verify <task.json>`로 task contract를 검증합니다.
5. 파일 변경이나 side-effectful command 전에 `harness-v2 gate <task.json> --root .`를 실행합니다.
6. local integration과 release boundary 상태를 확인할 때는 `harness-v2 doctor --root .`를 실행합니다.
7. `approval.approved_paths`에 명시된 경로만 수정합니다.
8. `approval.excluded_side_effects` 또는 `permission.denied_side_effects`에 명시된 side effect는 실행하지 않습니다.
9. 완료 전에는 `proof.obligations`의 모든 항목을 실행하거나 blocked 상태를 보고합니다.

## 증거 수준에 맞춘 읽기

일반적인 현재 작업은 이 파일, `CURRENT.md`, active task contract에서 시작할 수 있습니다.

approval binding, permission-sensitive command, proof/completion claim, lifecycle movement, stale/conflicting state, release work, external mutation, destructive action, product implementation risk가 있으면 source, approval, permission, proof, lifecycle control 원문을 정확히 읽습니다. 추가 읽기는 현재 판단 증거를 강화하기 위한 것이며 active contract를 넓히지 않습니다.

## 권한 분리

- `source`는 신뢰할 수 있는 근거를 지정합니다.
- `approval`은 사용자가 승인한 정확한 경로와 제외 항목을 지정합니다.
- `permission`은 허용되거나 금지된 side effect를 지정합니다.
- `proof`는 필요한 현재 증거를 지정합니다.
- `lifecycle`은 현재 상태와 목표 상태를 지정합니다.

어떤 표면도 다른 표면을 대신하지 않습니다. 설치, package metadata, README 예시, 이전 대화, tool availability는 active contract를 넓히지 않습니다.

source, approval, permission, proof, lifecycle, 요청 경로가 충돌하면 fail closed하고 새 contract를 요청합니다.
"""


def _current_md() -> str:
    return """# HARNESS V2 Current State

status: applied_project_surface / init / current_pointer

이 프로젝트 루트에는 HARNESS V2가 적용되어 있습니다. AI 에이전트는 `AGENTS.md`, `RULES.md`, 이 파일, `control\\`, active task contract를 작업 경계로 사용해야 합니다.

적용된 표면은 scaffold, task-contract validator, CLI helper입니다. 자동 enforcement sandbox, completion layer, approval engine, proof generator, lifecycle transition engine이 아니며, 설치, `init`, `apply`, CLI 사용 가능 상태만으로 미래 작업을 승인하지 않습니다.

작업 전 local hook-equivalent gate로 `harness-v2 gate contracts\\harness-task.json --root .`를 사용합니다. 이 gate는 명시적이고 확인 가능하지만 shell이나 editor 동작을 자동으로 차단하지 않습니다.

`harness-v2 doctor --root .`는 read-only integration report로 사용합니다. 이 명령은 release readiness, proof 자체, lifecycle movement를 만들지 않습니다.

workflow: `default`

state: `ready`

substate: `initialized / not_automatic_enforcement_completion`

source basis:

- `AGENTS.md`
- `RULES.md`
- `contracts\\harness-task.json`

## Current Task

초기 task contract는 `contracts\\harness-task.json`입니다.

이 초기 contract는 scaffold가 적용되었고 검증 가능하다는 것만 증명합니다. 임의의 feature 작업, package 작업, dependency 변경, release execution, secret 접근, destructive operation, external mutation을 승인하지 않습니다.

실제 작업마다 요청된 작업에 맞는 source, approval, permission, proof, lifecycle 필드를 가진 task contract를 만들거나 받아야 합니다.

이 파일이 아직 initial scaffold pointer를 보여주고 있고 사용자가 구체적인 작업을 요청했다면 먼저 등록합니다.

```powershell
harness-v2 task start --root . --title "<짧은 작업명>" --summary "<사용자 요청 요약>"
```

## Stop Conditions

요청된 작업이 active task contract 밖의 경로, 명령, side effect, secret, external mutation, dependency 변경, package publish, release execution, destructive operation을 필요로 하면 멈춥니다.
"""


def _source_md() -> str:
    return """# HARNESS V2 Source Control

status: applied_project_surface / init / source_control

source basis는 각 task contract의 `source.basis`에 선언됩니다.

`README.md`, package metadata, 오래된 채팅, 생략된 검사, 설치 성공은 active task contract가 현재 작업의 source basis로 명시하지 않는 한 source authority가 아닙니다.

이 파일은 guidance입니다. 현재 source pointer는 active task contract와 `CURRENT.md`가 결정합니다.
"""


def _approval_md() -> str:
    return """# HARNESS V2 Approval Control

status: applied_project_surface / init / approval_control

approval은 각 task contract의 `approval.packet`과 `approval.approved_paths`에 선언됩니다.

active task contract가 명시하지 않은 파일 경로는 승인된 것이 아닙니다.

“진행해”, 설치 성공, init/apply 성공, README 예시, tool availability 같은 넓은 표현은 추가 경로, package publish, release execution, dependency 설치, secret 접근, external mutation, destructive operation을 승인하지 않습니다.
"""


def _permission_md() -> str:
    return """# HARNESS V2 Permission Control

status: applied_project_surface / init / permission_control

permission은 각 task contract의 `permission.allowed_side_effects`와 `permission.denied_side_effects`에 선언됩니다.

denied side effect는 넓은 요청보다 우선합니다. secret 접근, dependency 설치, package publish, release execution, external mutation, destructive operation은 별도의 명시적 task contract가 필요합니다.

approval 문구는 그 자체로 permission이 되지 않습니다. 명령 실행이나 파일 변경 전 active task contract에 맞춰 permission을 확인해야 합니다.

`harness-v2 init`, `harness-v2 apply`, 검증 성공은 다음 작업의 permission을 부여하지 않습니다.
"""


def _proof_md() -> str:
    return """# HARNESS V2 Proof Control

status: applied_project_surface / init / proof_control

proof obligation은 각 task contract의 `proof.obligations`에 선언됩니다.

active proof obligation을 실행하거나 blocked 상태를 보고하기 전에는 완료를 주장하지 않습니다.

proof는 실제 프로젝트 루트 또는 task가 명시한 consumer surface에서 나온 현재 증거여야 합니다. README 문구, 이전 성공, 설치/init/apply 성공, 검증되지 않은 추정은 proof가 아닙니다.
"""


def _lifecycle_md() -> str:
    return """# HARNESS V2 Lifecycle Control

status: applied_project_surface / init / lifecycle_control

알려진 local state:

- `ready`
- `active`
- `blocked`
- `done`

lifecycle movement는 active task contract에 명시되어야 합니다. 진행 메모는 lifecycle transition이 아닙니다.

active task contract가 해당 transition을 명시하고 현재 proof가 충족되기 전에는 작업을 done, release-ready, published, migrated, automatically enforced 상태로 표시하지 않습니다.
"""


def _records_readme_md() -> str:
    return """# HARNESS V2 Records

이 폴더는 적용된 프로젝트의 task-local record를 보관합니다.

`records\\stages\\`는 공식 HARNESS V2 workflow stage를 따릅니다.

1. `spec`
2. `spec_review`
3. `plan`
4. `plan_review`
5. `plan_approval`
6. `development`
7. `development_review`
8. `improvement`

이 기록들은 연속성을 돕습니다. 하지만 그 자체로 source authority, approval, permission, proof, lifecycle transition, routing permission, release readiness가 되지 않습니다.
"""


def _current_task_md() -> str:
    return """# 현재 작업 기록

이 파일은 현재 작업을 사람이 읽기 쉬운 형태로 요약할 때 사용합니다.

`contracts\\harness-task.json`과 맞춰 유지합니다. task contract와 이 메모가 다르면 task contract와 `CURRENT.md`가 우선합니다.
"""


def _stage_record_md(title: str) -> str:
    korean_title = {
        "Spec": "Spec",
        "Spec Review": "Spec Review",
        "Plan": "Plan",
        "Plan Review": "Plan Review",
        "Plan Approval": "Plan Approval",
        "Development": "Development",
        "Development Review": "Development Review",
        "Improvement": "Improvement",
    }.get(title, title)
    return f"""# {korean_title} 단계 기록

status: initialized / empty

이 파일은 `{title.casefold().replace(" ", "_")}` workflow stage의 task-local note를 기록할 때 사용합니다.

이 기록만으로 approval, permission, proof, lifecycle transition, route authority, release readiness, source of truth가 되지 않습니다.
"""


def _decisions_md() -> str:
    return """# 결정 기록

이 파일은 task-local decision과 deferred item을 요약할 때 사용합니다.

모든 decision은 구현에 영향을 주기 전에 active task contract, current source basis, user-approved packet 중 하나를 근거로 가져야 합니다.
"""


def _records_proof_md() -> str:
    return """# Proof 기록

이 파일은 active task의 proof command, output, blocked check, readback evidence를 요약할 때 사용합니다.

proof는 active task contract의 `proof.obligations`와 현재 consumer surface에 맞을 때만 유효합니다.
"""


def _handoff_md() -> str:
    return """# Handoff 기록

이 파일은 다른 에이전트나 이후 세션을 위한 continuity note가 필요할 때만 사용합니다.

handoff note는 approval, permission, proof, lifecycle transition, source authority가 아닙니다.
"""


def _initial_task_json() -> str:
    return """{
  "task_id": "harness-v2-initial-task",
  "title": "Scaffold-only initial HARNESS V2 project binding",
  "workflow": "default",
  "contract_version": "0.1.8",
  "workflow_stage": "development",
  "current_gate": "development",
  "task_mode": "scaffold_only",
  "record_strength": "light",
  "risk_flags": [
    "scaffold_generation"
  ],
  "proof_profile": "current",
  "capability_request": [
    "init_scaffold"
  ],
  "classification_required": true,
  "record_density": {
    "generated_file_count": 23,
    "required_read_set_size": 3,
    "field_presence": "strict"
  },
  "source": {
    "basis": [
      "AGENTS.md",
      "RULES.md",
      "CURRENT.md"
    ],
    "current_pointer": "CURRENT.md"
  },
  "approval": {
    "packet": "Scaffold-only initial local HARNESS V2 project application as scaffold, task-contract validator, and CLI helper",
    "approved_paths": [
      "AGENTS.md",
      "RULES.md",
      "CURRENT.md",
      "control\\\\source.md",
      "control\\\\approval.md",
      "control\\\\permission.md",
      "control\\\\proof.md",
      "control\\\\lifecycle.md",
      "records\\\\README.md",
      "records\\\\current-task.md",
      "records\\\\stages\\\\spec.md",
      "records\\\\stages\\\\spec-review.md",
      "records\\\\stages\\\\plan.md",
      "records\\\\stages\\\\plan-review.md",
      "records\\\\stages\\\\plan-approval.md",
      "records\\\\stages\\\\development.md",
      "records\\\\stages\\\\development-review.md",
      "records\\\\stages\\\\improvement.md",
      "records\\\\decisions.md",
      "records\\\\proof.md",
      "records\\\\handoff.md",
      "contracts\\\\harness-task.json",
      "templates\\\\task.json"
    ],
    "excluded_side_effects": [
      "dependency install from network",
      "package publish",
      "release execution",
      "secret access",
      "external network mutation",
      "destructive operation"
    ]
  },
  "permission": {
    "allowed_side_effects": [
      "local file writes to initial HARNESS V2 scaffold files",
      "local readback of generated HARNESS V2 scaffold files",
      "harness-v2 status --root .",
      "harness-v2 verify contracts\\\\harness-task.json",
      "harness-v2 gate contracts\\\\harness-task.json --root .",
      "harness-v2 doctor --root ."
    ],
    "denied_side_effects": [
      "dependency install from network",
      "package publish",
      "release execution",
      "secret access",
      "external network mutation",
      "destructive operation"
    ]
  },
  "proof": {
    "obligations": [
      "generated AGENTS/RULES/CURRENT bind AI agents without relying on README authority",
      "generated records/stages scaffold tracks spec through improvement",
      "harness-v2 status --root .",
      "harness-v2 verify contracts\\\\harness-task.json",
      "harness-v2 gate contracts\\\\harness-task.json --root .",
      "harness-v2 doctor --root ."
    ]
  },
  "lifecycle": {
    "current_state": "ready",
    "target_state": "ready"
  }
}
"""


def _task_template_json() -> str:
    return """{
  "task_id": "<task-id>",
  "title": "<task title>",
  "workflow": "default",
  "contract_version": "0.1.8",
  "workflow_stage": "<spec|spec_review|plan|plan_review|plan_approval|development|development_review|improvement>",
  "current_gate": "<derived from workflow_stage unless strict migration changes ownership>",
  "task_mode": "<setup_only|read_only_analysis|scaffold_only|planned_change|defect_repair|continuity_only>",
  "record_strength": "<minimal|light|strict>",
  "risk_flags": ["<risk flag or none>"],
  "proof_profile": "<none|basic|current|strict>",
  "capability_request": ["<capability request or none>"],
  "classification_required": true,
  "record_density": {
    "generated_file_count": 0,
    "required_read_set_size": 1,
    "field_presence": "<minimal|light|strict>"
  },
  "source": {
    "basis": ["CURRENT.md"],
    "current_pointer": "CURRENT.md"
  },
  "approval": {
    "packet": "<exact approval packet>",
    "approved_paths": ["<approved path>"],
    "excluded_side_effects": ["<excluded side effect>"]
  },
  "permission": {
    "allowed_side_effects": ["<allowed side effect>"],
    "denied_side_effects": ["<denied side effect>"]
  },
  "proof": {
    "obligations": ["<proof obligation>"]
  },
  "lifecycle": {
    "current_state": "ready",
    "target_state": "ready"
  }
}
"""
