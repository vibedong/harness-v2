from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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
TASK_MODES = frozenset(
    {
        "setup_only",
        "read_only_analysis",
        "scaffold_only",
        "planned_change",
        "defect_repair",
        "continuity_only",
    }
)
RECORD_STRENGTHS = frozenset({"minimal", "light", "strict"})
STRENGTH_RANK = {"minimal": 0, "light": 1, "strict": 2}
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
    compatibility_mode: bool = True


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
            "next": [
                "harness-v2 status --root .",
                f"harness-v2 verify {self.initial_task}",
                f"harness-v2 gate {self.initial_task} --root .",
                "harness-v2 doctor --root .",
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
    return validate_task(data, root=_find_project_root(payload_path))


def initialize_project(root: str | Path, force: bool = False) -> InitResult:
    requested_root = Path(root).resolve()
    redirected = _looks_like_harness_package_root(requested_root)
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


def validate_task(data: dict[str, Any], root: str | Path | None = None) -> ValidationResult:
    errors: list[str] = []
    task_id = data.get("task_id")
    root_path = Path(root) if root is not None else None
    compatibility_mode = not _is_strict_task_contract(data)
    workflow_stage = data.get("workflow_stage")
    current_gate = _derive_current_gate(data)
    task_mode = _task_mode_value(data)
    record_strength = _record_strength_value(data)
    effective_record_strength = _effective_record_strength(
        workflow_stage if isinstance(workflow_stage, str) else None,
        task_mode,
        record_strength,
    )

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

    return ValidationResult(
        ok=not errors,
        task_id=task_id if isinstance(task_id, str) else None,
        errors=tuple(errors),
        current_gate=current_gate,
        task_mode=task_mode,
        record_strength=record_strength,
        effective_record_strength=effective_record_strength,
        compatibility_mode=compatibility_mode,
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


def _derive_current_gate(data: dict[str, Any]) -> str | None:
    current_gate = data.get("current_gate")
    if isinstance(current_gate, str) and current_gate.strip():
        return current_gate
    workflow_stage = data.get("workflow_stage")
    if isinstance(workflow_stage, str) and workflow_stage.strip():
        return workflow_stage
    return None


def _task_mode_value(data: dict[str, Any]) -> str:
    value = data.get("task_mode")
    return value if isinstance(value, str) and value.strip() else "planned_change"


def _record_strength_value(data: dict[str, Any]) -> str:
    value = data.get("record_strength")
    return value if isinstance(value, str) and value.strip() else "minimal"


def _effective_record_strength(stage: str | None, task_mode: str, record_strength: str) -> str:
    stage_default = {
        "spec": "light",
        "spec_review": "light",
        "plan": "strict",
        "plan_review": "strict",
        "plan_approval": "strict",
        "development": "light",
        "development_review": "strict",
        "improvement": "light",
    }.get(stage or "", "light")
    task_mode_default = {
        "setup_only": "minimal",
        "read_only_analysis": "minimal",
        "scaffold_only": "light",
        "planned_change": "strict",
        "defect_repair": "strict",
        "continuity_only": "minimal",
    }.get(task_mode, "light")
    candidates = tuple(value if value in STRENGTH_RANK else "strict" for value in (stage_default, task_mode_default, record_strength))
    return max(candidates, key=lambda value: STRENGTH_RANK.get(value, STRENGTH_RANK["strict"]))


def _validate_goal0_compatibility_fields(data: dict[str, Any], compatibility_mode: bool, errors: list[str]) -> None:
    workflow_stage = data.get("workflow_stage")
    current_gate = data.get("current_gate")
    task_mode = data.get("task_mode")
    record_strength = data.get("record_strength")

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

    if task_mode is None:
        if not compatibility_mode:
            errors.append("strict task contracts require task_mode")
    elif task_mode not in TASK_MODES:
        errors.append(f"task_mode is not known: {task_mode}")

    if record_strength is None:
        if not compatibility_mode:
            errors.append("strict task contracts require record_strength")
    elif record_strength not in RECORD_STRENGTHS:
        errors.append(f"record_strength is not known: {record_strength}")


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
        if not any(_contains_fragment(value, ("write", "modify", "create")) for value in allowed_side_effects):
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


def _looks_like_harness_package_root(path: Path) -> bool:
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


def _agents_md() -> str:
    return """# HARNESS V2 Agent Entry

This project has HARNESS V2 applied at the project root. This file is the AI agent entry point.

The applied surface is a scaffold, task-contract validator, and CLI helper. It is not an automatic enforcement sandbox, completion layer, approval engine, proof generator, or lifecycle transition engine.

HARNESS V2 provides a hook-equivalent gate command for Codex-app-focused work. `harness-v2 gate <task.json> --root .` combines `status`, `verify`, and optional `preflight` checks into one executable boundary check. It does not automatically block shell or editor actions.

`README.md` and `README.ko.md` are user documentation. They explain the tool, but they do not grant source authority, approval, permission, proof, lifecycle state, or release authority.

## Evidence-Scaled Read Order

For routine current-task work, read:

1. `RULES.md`
2. `CURRENT.md`
3. The active task contract, initially `contracts\\harness-task.json`

Then read only the owner surface required by the task. Expand to exact `control\\source.md`, `control\\approval.md`, `control\\permission.md`, `control\\proof.md`, or `control\\lifecycle.md` text before approval binding, permission-sensitive commands, proof/completion claims, lifecycle movement, stale/conflicting state, release work, external mutation, destructive action, or product implementation risk.

## Required Preflight

Run these checks before changing files or side-effectful commands:

```powershell
harness-v2 status --root .
harness-v2 verify contracts\\harness-task.json
harness-v2 gate contracts\\harness-task.json --root .
harness-v2 doctor --root .
```

## Working Boundary

Installation, `init`, `apply`, and CLI availability do not approve arbitrary future work. Stay inside `approval.approved_paths`. Do not execute `approval.excluded_side_effects` or `permission.denied_side_effects`.

If the current user request does not fit the active task contract, stop before mutating files or running side-effectful commands and ask for a new or amended task contract.

Completion requires current proof from `proof.obligations`; previous chat, README text, skipped checks, or successful installation are not proof.
"""


def _rules_md() -> str:
    return """# HARNESS V2 Project Rules

HARNESS V2 records the current task boundary for AI-assisted work. It is a scaffold, task-contract validator, and CLI helper. It is not an automatic enforcement sandbox, completion layer, approval engine, proof generator, lifecycle transition engine, editor, shell, network, or release sandbox.

The local hook-equivalent gate is an explicit command: `harness-v2 gate <task.json> --root .`. It checks the active task boundary through status, verify, and optional preflight. It does not install a real Codex app hook and does not automatically block shell or editor actions.

README files are user-facing documentation only. They never grant approval, permission, proof, lifecycle state, route authority, release readiness, or package publish authority.

## Required Flow

1. Read `CURRENT.md`.
2. Read the active task contract.
3. Verify the task contract with `harness-v2 verify <task.json>`.
4. Run `harness-v2 gate <task.json> --root .` before file changes or side-effectful commands.
5. Run `harness-v2 doctor --root .` when checking local integration and release boundary status.
6. Modify only paths named in `approval.approved_paths`.
7. Do not execute side effects named in `approval.excluded_side_effects` or `permission.denied_side_effects`.
8. Before completion, run or report every item in `proof.obligations`.

## Evidence-Scaled Readback

Routine current-task work may start from this file, `CURRENT.md`, and the active task contract.

Read exact source, approval, permission, proof, and lifecycle control text before approval binding, permission-sensitive commands, proof/completion claims, lifecycle movement, stale/conflicting state, release work, external mutation, destructive action, or product implementation risk. Extra reading must improve the current decision evidence; it does not widen the active contract.

## Authority Separation

- `source` names what can be trusted.
- `approval` names exact user-approved paths and exclusions.
- `permission` names allowed and denied side effects.
- `proof` names required current evidence.
- `lifecycle` names the current and target state.

No one surface substitutes for another. Installation, package metadata, README examples, prior conversation, and tool availability do not widen the active contract.

If source, approval, permission, proof, lifecycle, or requested paths conflict, fail closed and ask for a new contract.
"""


def _current_md() -> str:
    return """# HARNESS V2 Current State

status: applied_project_surface / init / current_pointer

This project root has HARNESS V2 applied. AI agents should use `AGENTS.md`, `RULES.md`, this file, `control\\`, and the active task contract as the operating boundary.

The applied surface is a scaffold, task-contract validator, and CLI helper. It is not an automatic enforcement sandbox, completion layer, approval engine, proof generator, or lifecycle transition engine, and it does not approve future work by installation, `init`, `apply`, or CLI availability.

Use `harness-v2 gate contracts\\harness-task.json --root .` as the local hook-equivalent gate before work. The gate is explicit and checkable, but it does not automatically block shell or editor actions.

Use `harness-v2 doctor --root .` as a read-only integration report. It does not create release readiness, proof by itself, or lifecycle movement.

workflow: `default`

state: `ready`

substate: `initialized / not_automatic_enforcement_completion`

source basis:

- `AGENTS.md`
- `RULES.md`
- `contracts\\harness-task.json`

## Current Task

The initial task contract is `contracts\\harness-task.json`.

That initial contract proves the scaffold was applied and can be verified. It does not authorize arbitrary feature work, package work, dependency changes, release execution, secrets, destructive operations, or external mutation.

For each real task, create or receive a task contract whose source, approval, permission, proof, and lifecycle fields match the requested work.

## Stop Conditions

Stop if the requested work needs paths, commands, side effects, secrets, external mutation, dependency changes, package publish, release execution, or destructive operations outside the active task contract.
"""


def _source_md() -> str:
    return """# HARNESS V2 Source Control

status: applied_project_surface / init / source_control

Source basis is declared by each task contract in `source.basis`.

`README.md`, package metadata, old chat, skipped checks, and successful installation are not source authority unless the active task contract names them as source basis for the current task.

This file is guidance only. The active task contract and `CURRENT.md` decide the current source pointer.
"""


def _approval_md() -> str:
    return """# HARNESS V2 Approval Control

status: applied_project_surface / init / approval_control

Approval is declared by each task contract in `approval.packet` and `approval.approved_paths`.

No file path is approved unless the active task contract names it.

Broad phrases such as "go ahead", installation success, init/apply success, README examples, or tool availability do not approve extra paths, package publish, release execution, dependency installation, secrets, external mutation, or destructive operations.
"""


def _permission_md() -> str:
    return """# HARNESS V2 Permission Control

status: applied_project_surface / init / permission_control

Permission is declared by each task contract in `permission.allowed_side_effects` and `permission.denied_side_effects`.

Denied side effects win over broad requests. Secrets, dependency installation, package publish, release execution, external mutation, and destructive operations require a separate explicit task contract.

Approval text does not become permission by itself. Permission must be checked against the active task contract before running commands or changing files.

`harness-v2 init`, `harness-v2 apply`, and successful verification do not grant permission for the next task.
"""


def _proof_md() -> str:
    return """# HARNESS V2 Proof Control

status: applied_project_surface / init / proof_control

Proof obligations are declared by each task contract in `proof.obligations`.

Do not claim completion until the active proof obligations are run or their blocked status is reported.

Proof must be current evidence from the actual project root or the consumer surface named by the task. README text, previous success, installation/init/apply success, and unverified assumptions are not proof.
"""


def _lifecycle_md() -> str:
    return """# HARNESS V2 Lifecycle Control

status: applied_project_surface / init / lifecycle_control

Known local states:

- `ready`
- `active`
- `blocked`
- `done`

Lifecycle movement must be named in the active task contract. Progress notes are not lifecycle transitions.

Do not mark work done, release-ready, published, migrated, or automatically enforced unless the active task contract names that transition and current proof satisfies it.
"""


def _records_readme_md() -> str:
    return """# HARNESS V2 Records

This folder keeps task-local records for the applied project.

`records\\stages\\` follows the official HARNESS V2 workflow stages:

1. `spec`
2. `spec_review`
3. `plan`
4. `plan_review`
5. `plan_approval`
6. `development`
7. `development_review`
8. `improvement`

These records support continuity. They are not source authority, approval, permission, proof, lifecycle transition, routing permission, or release readiness by themselves.
"""


def _current_task_md() -> str:
    return """# Current Task Record

Use this file to summarize the current task in human-readable form.

Keep it aligned with `contracts\\harness-task.json`. If the task contract and this note disagree, the task contract and `CURRENT.md` win.
"""


def _stage_record_md(title: str) -> str:
    return f"""# {title} Stage Record

status: initialized / empty

Use this file for task-local notes from the `{title.casefold().replace(" ", "_")}` workflow stage.

Do not treat this record as approval, permission, proof, lifecycle transition, route authority, release readiness, or source of truth by itself.
"""


def _decisions_md() -> str:
    return """# Decision Record

Use this file to summarize task-local decisions and deferred items.

Every decision must point back to the active task contract, current source basis, or user-approved packet before it can affect implementation.
"""


def _records_proof_md() -> str:
    return """# Proof Record

Use this file to summarize proof commands, outputs, blocked checks, and readback evidence for the active task.

Proof is valid only when it matches the active task contract's `proof.obligations` and current consumer surface.
"""


def _handoff_md() -> str:
    return """# Handoff Record

Use this file only when continuity notes are needed for another agent or later session.

Handoff notes are not approval, permission, proof, lifecycle transition, or source authority.
"""


def _initial_task_json() -> str:
    return """{
  "task_id": "harness-v2-initial-task",
  "title": "Scaffold-only initial HARNESS V2 project binding",
  "workflow": "default",
  "workflow_stage": "development",
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
  "contract_version": "0.1.7",
  "workflow_stage": "<spec|spec_review|plan|plan_review|plan_approval|development|development_review|improvement>",
  "current_gate": "<derived from workflow_stage unless strict migration changes ownership>",
  "task_mode": "<setup_only|read_only_analysis|scaffold_only|planned_change|defect_repair|continuity_only>",
  "record_strength": "<minimal|light|strict>",
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
