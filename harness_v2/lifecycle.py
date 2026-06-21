from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Any

from .core import LEGACY_STAGE_ALIASES, WORKFLOW_STAGES, load_json
from .layout import DEFAULT_LAYOUT

TERMINAL_GATE = "completed"
ALLOWED_ROUTE_EDGES = {
    ("spec", "spec_review"),
    ("spec_review", "spec"),
    ("spec_review", "plan"),
    ("plan", "plan_review"),
    ("plan_review", "plan"),
    ("plan_review", "plan_approval"),
    ("plan_approval", "plan"),
    ("plan_approval", "development"),
    ("development", "development_review"),
    ("development_review", "development"),
    ("development_review", "improvement"),
    ("improvement", TERMINAL_GATE),
}
REQUIRED_FIELDS = (
    "from_gate",
    "to_gate",
    "reason",
    "source_refs",
    "approval_ref",
    "permission_ref",
    "proof_ref",
    "freshness_refs",
    "stale_check",
    "actor",
)
NON_AUTHORITY_REF_FRAGMENTS = (
    "artifacts\\",
    "artifacts/",
    "artifact registry",
    "artifact log",
    "registry.md",
    "log.md",
    "routing\\",
    "routing/",
    "routing manifest",
    "route row",
    "records\\stages\\",
    "records/stages/",
    "review note",
    "review findings",
    "release\\",
    "release/",
    "release note",
    "release notes",
    "release_notes.md",
)


@dataclass(frozen=True)
class TransitionRecord:
    timestamp: str
    from_gate: str
    to_gate: str
    reason: str
    source_refs: tuple[str, ...]
    approval_ref: str
    permission_ref: str
    proof_ref: str
    freshness_refs: tuple[str, ...]
    stale_check: str
    actor: str

    def to_json(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "from_gate": self.from_gate,
            "to_gate": self.to_gate,
            "reason": self.reason,
            "source_refs": list(self.source_refs),
            "approval_ref": self.approval_ref,
            "permission_ref": self.permission_ref,
            "proof_ref": self.proof_ref,
            "freshness_refs": list(self.freshness_refs),
            "stale_check": self.stale_check,
            "actor": self.actor,
        }


@dataclass(frozen=True)
class LifecycleEvaluation:
    ok: bool
    transition: dict[str, Any] | None
    errors: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "transition": self.transition,
            "errors": list(self.errors),
        }


def parse_transition_log(content: str) -> tuple[TransitionRecord, ...]:
    records: list[TransitionRecord] = []
    current_timestamp: str | None = None
    current_fields: dict[str, str] = {}

    def flush() -> None:
        nonlocal current_timestamp, current_fields
        if current_timestamp is None:
            return
        missing = [field for field in REQUIRED_FIELDS if not current_fields.get(field)]
        if missing:
            raise ValueError(f"transition {current_timestamp} missing fields: {', '.join(missing)}")
        records.append(
            TransitionRecord(
                timestamp=current_timestamp,
                from_gate=current_fields["from_gate"],
                to_gate=current_fields["to_gate"],
                reason=current_fields["reason"],
                source_refs=_field_list(current_fields["source_refs"]),
                approval_ref=current_fields["approval_ref"],
                permission_ref=current_fields["permission_ref"],
                proof_ref=current_fields["proof_ref"],
                freshness_refs=_field_list(current_fields["freshness_refs"]),
                stale_check=current_fields["stale_check"],
                actor=current_fields["actor"],
            )
        )
        current_timestamp = None
        current_fields = {}

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line.startswith("## transition:"):
            flush()
            current_timestamp = line.split(":", 1)[1].strip()
            current_fields = {}
            continue
        if current_timestamp is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in REQUIRED_FIELDS:
            current_fields[key] = value.strip()
    flush()
    return tuple(records)


def transition_log_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def append_transition_record(
    path: str | Path,
    record: TransitionRecord,
    *,
    previous_ledger_hash: str | None = None,
    root: str | Path | None = None,
) -> None:
    log_path = Path(path)
    if root is not None:
        errors: list[str] = []
        _ensure_path_under_root(Path(root), log_path, "transition log path", errors)
        if errors:
            raise ValueError(errors[0])
    if previous_ledger_hash is not None:
        if not log_path.exists():
            raise ValueError("transition ledger hash mismatch; earlier blocks may have changed")
        current_hash = transition_log_sha256(log_path)
        if current_hash != previous_ledger_hash:
            raise ValueError("transition ledger hash mismatch; earlier blocks may have changed")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = "\n" if log_path.exists() and log_path.read_text(encoding="utf-8").strip() else ""
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(prefix)
        handle.write(_record_markdown(record))


def evaluate_transition_log(task_path: str | Path, log_path: str | Path) -> LifecycleEvaluation:
    task_file = Path(task_path)
    task = load_json(task_file)
    root = _find_project_root(task_file)
    log_file = Path(log_path)
    if root is not None and not _under_root(log_file.resolve(), root):
        return LifecycleEvaluation(False, None, ("transition log path must stay under project root",))
    transitions = parse_transition_log(log_file.read_text(encoding="utf-8"))
    if not transitions:
        return LifecycleEvaluation(False, None, ("transition log contains no transition records",))
    return evaluate_transition_record(task, transitions[-1], root=root)


def evaluate_transition_record(
    task: dict[str, Any],
    record: TransitionRecord,
    *,
    root: str | Path | None = None,
) -> LifecycleEvaluation:
    errors: list[str] = []
    transition = record.to_json()
    from_gate = record.from_gate
    to_gate = record.to_gate
    root_path = Path(root) if root is not None else None

    for gate in (from_gate, to_gate):
        if gate in LEGACY_STAGE_ALIASES:
            errors.append(f"transition uses legacy stage alias {gate!r}; use {LEGACY_STAGE_ALIASES[gate]!r}")
        elif gate != TERMINAL_GATE and gate not in WORKFLOW_STAGES:
            errors.append(f"transition gate is not known: {gate}")

    if (from_gate, to_gate) == ("improvement", "spec"):
        errors.append("same-task improvement-to-spec transition is denied")
    elif not errors and (from_gate, to_gate) not in ALLOWED_ROUTE_EDGES:
        errors.append(f"transition route is not allowed: {from_gate} -> {to_gate}")

    task_stage = task.get("workflow_stage")
    if isinstance(task_stage, str) and task_stage != from_gate:
        errors.append("transition from_gate must match task workflow_stage")

    _validate_transition_refs(record, root_path, errors)
    _reject_stale(record.stale_check, errors)

    if to_gate == "development":
        _require_active_approval(task, record.approval_ref, errors, "development entry requires active approval and permission")
        _require_active_permission(task, record.permission_ref, errors, "development entry requires active approval and permission")
    if to_gate == "improvement":
        _require_active_approval(task, record.approval_ref, errors, "improvement entry requires active approval and permission")
        _require_active_permission(task, record.permission_ref, errors, "improvement entry requires active approval and permission")
        _require_current_proof(task, record.proof_ref, errors, "improvement entry requires current proof")

    return LifecycleEvaluation(not errors, transition, tuple(errors))


def _record_markdown(record: TransitionRecord) -> str:
    return (
        f"## transition: {record.timestamp}\n"
        f"from_gate: {record.from_gate}\n"
        f"to_gate: {record.to_gate}\n"
        f"reason: {record.reason}\n"
        f"source_refs: {', '.join(record.source_refs)}\n"
        f"approval_ref: {record.approval_ref}\n"
        f"permission_ref: {record.permission_ref}\n"
        f"proof_ref: {record.proof_ref}\n"
        f"freshness_refs: {', '.join(record.freshness_refs)}\n"
        f"stale_check: {record.stale_check}\n"
        f"actor: {record.actor}\n"
    )


def _field_list(value: str) -> tuple[str, ...]:
    return tuple(item.strip().replace("/", "\\") for item in value.split(",") if item.strip())


def _empty_ref(value: str) -> bool:
    return value.strip().lower() in {"", "missing", "none", "not_required", "not required"}


def _validate_transition_refs(record: TransitionRecord, root: Path | None, errors: list[str]) -> None:
    if not record.source_refs:
        errors.append("transition requires source_refs")
    for value in record.source_refs:
        _validate_project_ref(value, "source_refs entry", root, errors, required=True)

    if not record.freshness_refs:
        errors.append("transition requires freshness_refs")
    for value in record.freshness_refs:
        _validate_project_ref(value, "freshness_refs entry", root, errors, required=True)

    _validate_project_ref(record.approval_ref, "approval_ref", root, errors, required=False)
    _reject_non_authority_ref(record.approval_ref, "approval_ref", errors)
    _validate_project_ref(record.permission_ref, "permission_ref", root, errors, required=False)
    _reject_non_authority_ref(record.permission_ref, "permission_ref", errors)
    _validate_project_ref(record.proof_ref, "proof_ref", root, errors, required=False)
    _reject_non_authority_ref(record.proof_ref, "proof_ref", errors)


def _reject_non_authority_ref(value: str, label: str, errors: list[str]) -> None:
    if _empty_ref(value):
        return
    normalized = _normalize_ref(value).casefold()
    if any(fragment.casefold() in normalized for fragment in NON_AUTHORITY_REF_FRAGMENTS):
        errors.append(
            f"{label} cannot use artifact registry/log, review, route, or release surface as authority: {value}"
        )


def _validate_project_ref(
    value: str,
    label: str,
    root: Path | None,
    errors: list[str],
    *,
    required: bool,
) -> str | None:
    if _empty_ref(value):
        if required:
            errors.append(f"{label} is required")
        return None
    normalized = _normalize_ref(value)
    if _is_absolute_windows_ref(value):
        errors.append(f"{label} must be project-relative: {value}")
        return None
    if _escapes_project_ref(normalized):
        errors.append(f"{label} must stay under project root: {value}")
        return None
    if root is not None:
        candidate = (root / normalized).resolve()
        if not _under_root(candidate, root):
            errors.append(f"{label} must stay under project root: {value}")
            return None
        if not candidate.exists():
            errors.append(f"{label} does not exist: {normalized}")
            return None
    return normalized


def _require_active_approval(task: dict[str, Any], ref: str, errors: list[str], message: str) -> None:
    approval = task.get("approval") if isinstance(task.get("approval"), dict) else {}
    packet = approval.get("packet")
    approved_paths = _string_list(approval.get("approved_paths"))
    if _empty_ref(ref) or not isinstance(packet, str) or not packet.strip() or not approved_paths:
        _append_once(errors, message)


def _require_active_permission(task: dict[str, Any], ref: str, errors: list[str], message: str) -> None:
    permission = task.get("permission") if isinstance(task.get("permission"), dict) else {}
    allowed_side_effects = _string_list(permission.get("allowed_side_effects"))
    if _empty_ref(ref) or not allowed_side_effects:
        _append_once(errors, message)


def _require_current_proof(task: dict[str, Any], ref: str, errors: list[str], message: str) -> None:
    proof = task.get("proof") if isinstance(task.get("proof"), dict) else {}
    obligations = _string_list(proof.get("obligations"))
    if _empty_ref(ref) or not obligations:
        _append_once(errors, message)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item.strip()]


def _append_once(errors: list[str], message: str) -> None:
    if message not in errors:
        errors.append(message)


def _normalize_ref(value: str) -> str:
    normalized = value.strip().replace("/", "\\")
    while normalized.startswith(".\\"):
        normalized = normalized[2:]
    return normalized


def _is_absolute_windows_ref(value: str) -> bool:
    path = PureWindowsPath(value.strip())
    return path.is_absolute() or bool(path.drive) or value.strip().startswith(("\\", "/"))


def _escapes_project_ref(value: str) -> bool:
    return any(part == ".." for part in PureWindowsPath(value).parts)


def _ensure_path_under_root(root: Path, path: Path, label: str, errors: list[str]) -> None:
    if not _under_root(path.resolve(), root):
        errors.append(f"{label} must stay under project root")


def _under_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _find_project_root(path: Path) -> Path | None:
    resolved = path.resolve()
    for candidate in (resolved.parent, *resolved.parents):
        if DEFAULT_LAYOUT.resolve(candidate, DEFAULT_LAYOUT.current_pointer).exists():
            return candidate
    return None


def _reject_stale(stale_check: str, errors: list[str]) -> None:
    value = stale_check.strip().lower()
    if value in {"fresh", "pass", "passed"}:
        return
    if "approval" in value:
        errors.append("stale approval denies lifecycle transition")
    elif "permission" in value:
        errors.append("stale permission denies lifecycle transition")
    elif "proof" in value:
        errors.append("stale proof denies lifecycle transition")
    elif "source" in value:
        errors.append("stale source denies lifecycle transition")
    else:
        errors.append(f"stale_check does not pass: {stale_check}")
