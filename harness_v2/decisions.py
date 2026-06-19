from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Any


DECISION_KINDS = {"ApprovalDecision", "PermissionDecision", "ProofReceipt"}
BROAD_APPROVAL_TEXT = {"go ahead", "ok", "okay", "approved", "do it", "all approved"}
BROAD_APPROVAL_FRAGMENTS = ("broad", "unspecified", "whatever", "anything", "everything", "all files", "all work")
RISKY_SIDE_EFFECT_FRAGMENTS = (
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
    "package",
    "secret",
    "external network",
    "destructive",
)


@dataclass(frozen=True)
class DecisionResult:
    ok: bool
    kind: str | None
    record_id: str | None
    task_id: str | None
    errors: tuple[str, ...]
    stale: tuple[dict[str, Any], ...] = ()

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "kind": self.kind,
            "record_id": self.record_id,
            "task_id": self.task_id,
            "errors": list(self.errors),
            "stale": list(self.stale),
        }


def load_json(path: str | Path) -> dict[str, Any]:
    record_path = Path(path)
    with record_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{record_path} must contain a JSON object")
    return payload


def evaluate_decision_file(
    record_path: str | Path,
    *,
    task_path: str | Path | None = None,
    task: dict[str, Any] | None = None,
    root: str | Path | None = None,
) -> DecisionResult:
    try:
        record = load_json(record_path)
    except Exception as exc:
        return DecisionResult(False, None, None, None, (f"json: {exc}",))
    task_data = task
    if task_data is None and task_path is not None:
        try:
            task_data = load_json(task_path)
        except Exception as exc:
            return DecisionResult(False, _string(record.get("kind")) or None, _record_id(record), _string(record.get("task_id")) or None, (f"task json: {exc}",))
    root_path = Path(root) if root is not None else _find_project_root(Path(record_path))
    return evaluate_decision(record, task=task_data, root=root_path)


def evaluate_decision(
    record: dict[str, Any],
    *,
    task: dict[str, Any] | None = None,
    root: str | Path | None = None,
) -> DecisionResult:
    errors: list[str] = []
    stale: list[dict[str, Any]] = []
    kind = _string(record.get("kind"))
    record_id = _record_id(record)
    task_id = _string(record.get("task_id"))

    if kind not in DECISION_KINDS:
        errors.append(f"decision kind is not known: {kind or '<missing>'}")
    if not record_id:
        errors.append("decision record requires decision_id, receipt_id, or record_id")
    if not task_id:
        errors.append("decision record requires task_id")
    if task is not None and task_id and task_id != _string(task.get("task_id")):
        errors.append("decision task_id must match task contract task_id")

    if kind == "ApprovalDecision":
        _evaluate_approval_decision(record, task, errors)
    elif kind == "PermissionDecision":
        _evaluate_permission_decision(record, task, root, errors, stale)
    elif kind == "ProofReceipt":
        _evaluate_proof_receipt(record, task, root, errors, stale)

    _reject_lifecycle_transition_authority(record, errors)
    _evaluate_source_refs(record, root, errors, stale)

    return DecisionResult(not errors and not stale, kind or None, record_id or None, task_id or None, tuple(errors), tuple(stale))


def evaluate_proof_receipt_requirement(
    task: dict[str, Any],
    receipts: list[dict[str, Any]] | None,
    *,
    root: str | Path | None = None,
) -> DecisionResult:
    proof = task.get("proof") if isinstance(task.get("proof"), dict) else {}
    if proof.get("receipt_required") is not True:
        return DecisionResult(True, "ProofReceiptRequirement", None, _string(task.get("task_id")) or None, ())
    if not receipts:
        return DecisionResult(
            False,
            "ProofReceiptRequirement",
            None,
            _string(task.get("task_id")) or None,
            ("proof receipt required but no ProofReceipt records were supplied",),
        )

    errors: list[str] = []
    stale: list[dict[str, Any]] = []
    for index, receipt in enumerate(receipts):
        result = evaluate_decision(receipt, task=task, root=root)
        if result.kind != "ProofReceipt":
            errors.append(f"proof receipt {index}: expected ProofReceipt, got {result.kind or '<missing>'}")
        if not result.ok:
            errors.extend(f"proof receipt {index}: {error}" for error in result.errors)
            stale.extend(result.stale)
    return DecisionResult(not errors and not stale, "ProofReceiptRequirement", None, _string(task.get("task_id")) or None, tuple(errors), tuple(stale))


def _evaluate_approval_decision(record: dict[str, Any], task: dict[str, Any] | None, errors: list[str]) -> None:
    if not _string(record.get("approval_request_ref")):
        errors.append("ApprovalDecision requires approval_request_ref")
    _validate_user_response_binding(record.get("user_response"), errors)

    edit_paths = _string_list(record.get("edit_paths"))
    commands = _present_string_list(record, "commands", errors)
    side_effects = _present_string_list(record, "side_effects", errors)
    exclusions = _present_string_list(record, "exclusions", errors)
    git_scope = _string(record.get("git_scope"))
    release_scope = _string(record.get("release_scope"))

    if not edit_paths:
        errors.append("ApprovalDecision requires exact edit_paths")
    _reject_broad_paths("ApprovalDecision.edit_paths", edit_paths, errors)
    if not git_scope:
        errors.append("ApprovalDecision requires git_scope")
    if not release_scope:
        errors.append("ApprovalDecision requires release_scope")

    user_response = record.get("user_response") if isinstance(record.get("user_response"), dict) else {}
    response_text = _normalize_text(_string(user_response.get("text")))
    if _is_broad_approval_text(response_text):
        errors.append("ApprovalDecision user_response is too broad to bind approval")

    excluded_normalized = {_normalize_text(value) for value in exclusions}
    for value in (*commands, *side_effects):
        if _normalize_text(value) in excluded_normalized:
            errors.append(f"ApprovalDecision grants excluded side effect: {value}")

    if task is not None:
        approval = task.get("approval") if isinstance(task.get("approval"), dict) else {}
        task_paths = {_normalize_path(value) for value in _string_list(approval.get("approved_paths"))}
        for value in edit_paths:
            if _normalize_path(value) not in task_paths:
                errors.append(f"ApprovalDecision edit path exceeds task approval scope: {value}")
        task_exclusions = {_normalize_text(value) for value in _string_list(approval.get("excluded_side_effects"))}
        missing_exclusions = sorted(task_exclusions - excluded_normalized)
        for value in missing_exclusions:
            errors.append(f"ApprovalDecision omits task approval exclusion: {value}")
        permission = task.get("permission") if isinstance(task.get("permission"), dict) else {}
        task_allowed_side_effects = {_normalize_text(value) for value in _string_list(permission.get("allowed_side_effects"))}
        task_commands_or_side_effects = {*commands, *side_effects}
        for value in task_commands_or_side_effects:
            if _normalize_text(value) not in task_allowed_side_effects:
                errors.append(f"ApprovalDecision side effect exceeds task permission ceiling: {value}")
        if _normalize_text(git_scope) != "none" and _normalize_text(git_scope) not in task_allowed_side_effects:
            errors.append(f"ApprovalDecision git_scope exceeds task permission ceiling: {git_scope}")
        if _normalize_text(release_scope) != "none" and _normalize_text(release_scope) not in task_allowed_side_effects:
            errors.append(f"ApprovalDecision release_scope exceeds task permission ceiling: {release_scope}")


def _evaluate_permission_decision(
    record: dict[str, Any],
    task: dict[str, Any] | None,
    root: str | Path | None,
    errors: list[str],
    stale: list[dict[str, Any]],
) -> None:
    requested = _present_string_list(record, "requested_side_effects", errors)
    approved = _present_string_list(record, "approved_side_effects", errors)
    denied = _present_string_list(record, "denied_side_effects", errors)
    side_effect_class = _string(record.get("side_effect_class"))
    approval_ref = _string(record.get("approval_decision_ref"))

    if not side_effect_class:
        errors.append("PermissionDecision requires side_effect_class")
    if (requested or approved) and not approval_ref:
        errors.append("PermissionDecision requires approval_decision_ref when side effects exist")

    approval_ceiling = record.get("approval_ceiling") if isinstance(record.get("approval_ceiling"), dict) else {}
    ceiling_side_effects = {_normalize_text(value) for value in _string_list(approval_ceiling.get("side_effects"))}
    ceiling_exclusions = {_normalize_text(value) for value in _string_list(approval_ceiling.get("exclusions"))}
    if approved and not ceiling_side_effects:
        errors.append("PermissionDecision approval_ceiling.side_effects must be present when approving side effects")
    for value in approved:
        normalized = _normalize_text(value)
        if normalized not in ceiling_side_effects:
            errors.append(f"PermissionDecision approved side effect exceeds approval ceiling: {value}")
        if normalized in ceiling_exclusions:
            errors.append(f"PermissionDecision approved side effect conflicts with approval exclusion: {value}")
    for value in denied:
        if _normalize_text(value) in {_normalize_text(item) for item in approved}:
            errors.append(f"PermissionDecision cannot both approve and deny side effect: {value}")

    preflight = record.get("preflight") if isinstance(record.get("preflight"), dict) else {}
    if any(_is_risky_side_effect(value) for value in (*requested, *approved)):
        if not preflight:
            errors.append("PermissionDecision requires preflight for risky side effects")
        elif preflight.get("ok") is not True:
            errors.append("PermissionDecision preflight must be ok for risky side effects")
    if preflight and task is not None and _string(preflight.get("task_id")) and _string(preflight.get("task_id")) != _string(task.get("task_id")):
        errors.append("PermissionDecision preflight task_id must match task contract task_id")

    approval_decision: dict[str, Any] | None = None
    if approval_ref and root is not None:
        approval_path = _resolve_ref(root, approval_ref, "PermissionDecision approval_decision_ref", errors)
        if approval_path is not None:
            if not approval_path.exists():
                errors.append(f"PermissionDecision approval_decision_ref does not exist: {approval_ref}")
            else:
                try:
                    approval_decision = load_json(approval_path)
                except Exception as exc:
                    errors.append(f"PermissionDecision approval_decision_ref json: {exc}")
                    approval_decision = None
        if approval_path is not None and approval_path.exists():
            result = evaluate_decision(approval_decision or {}, task=task, root=root)
            if not result.ok:
                errors.extend(f"approval_decision_ref: {error}" for error in result.errors)
                stale.extend(result.stale)
            if result.kind != "ApprovalDecision":
                errors.append(f"PermissionDecision approval_decision_ref must reference ApprovalDecision, got {result.kind or '<missing>'}")
    elif approval_ref and root is None:
        errors.append("PermissionDecision approval_decision_ref requires project root")

    if approval_decision is not None:
        approved_ceiling = {_normalize_text(value) for value in _string_list(approval_decision.get("side_effects"))}
        approved_exclusions = {_normalize_text(value) for value in _string_list(approval_decision.get("exclusions"))}
        declared_side_effects = {_normalize_text(value) for value in _string_list(approval_ceiling.get("side_effects"))}
        declared_exclusions = {_normalize_text(value) for value in _string_list(approval_ceiling.get("exclusions"))}
        if not declared_side_effects.issubset(approved_ceiling):
            errors.append("PermissionDecision approval_ceiling.side_effects exceed referenced ApprovalDecision")
        if not approved_exclusions.issubset(declared_exclusions):
            errors.append("PermissionDecision approval_ceiling.exclusions omit referenced ApprovalDecision exclusions")


def _evaluate_proof_receipt(
    record: dict[str, Any],
    task: dict[str, Any] | None,
    root: str | Path | None,
    errors: list[str],
    stale: list[dict[str, Any]],
) -> None:
    obligation = _string(record.get("proof_obligation"))
    if not obligation:
        errors.append("ProofReceipt requires proof_obligation")
    obligation_sha256 = _string(record.get("proof_obligation_sha256"))
    if not _is_sha256(obligation_sha256):
        errors.append("ProofReceipt proof_obligation_sha256 must be a lowercase SHA-256 hex string")
    elif obligation and hashlib.sha256(obligation.encode("utf-8")).hexdigest() != obligation_sha256:
        errors.append("ProofReceipt proof_obligation_sha256 does not match proof_obligation")
    if task is not None:
        proof = task.get("proof") if isinstance(task.get("proof"), dict) else {}
        obligations = {_normalize_text(value) for value in _string_list(proof.get("obligations"))}
        if obligation and _normalize_text(obligation) not in obligations:
            errors.append(f"ProofReceipt proof_obligation is not required by task: {obligation}")

    verifier = record.get("verifier") if isinstance(record.get("verifier"), dict) else {}
    if not verifier:
        errors.append("ProofReceipt requires verifier")
    else:
        if not _string(verifier.get("method")):
            errors.append("ProofReceipt verifier.method must be a non-empty string")
        if not (_string(verifier.get("command")) or _string(verifier.get("readback"))):
            errors.append("ProofReceipt verifier requires command or readback")
        command = _string(verifier.get("command"))
        command_sha256 = _string(verifier.get("command_sha256"))
        if command:
            if not _is_sha256(command_sha256):
                errors.append("ProofReceipt verifier.command_sha256 must be a lowercase SHA-256 hex string when command is present")
            elif hashlib.sha256(command.encode("utf-8")).hexdigest() != command_sha256:
                errors.append("ProofReceipt verifier.command_sha256 does not match verifier.command")
        if verifier.get("ok") is not True:
            errors.append("ProofReceipt verifier.ok must be true")
        output_sha256 = _string(verifier.get("output_sha256"))
        if not _is_sha256(output_sha256):
            errors.append("ProofReceipt verifier.output_sha256 must be a lowercase SHA-256 hex string")

    source_refs = record.get("source_refs")
    if not isinstance(source_refs, list) or not source_refs:
        errors.append("ProofReceipt requires current source_refs")
    elif root is None:
        errors.append("ProofReceipt source_refs require project root for freshness")
    else:
        affects = {_normalize_text(value) for item in source_refs if isinstance(item, dict) for value in _string_list(item.get("affects"))}
        for required in ("implementation", "tests", "proof command", "proof predicate"):
            if required not in affects:
                errors.append(f"ProofReceipt source_refs must include {required} anchor")


def _validate_user_response_binding(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("ApprovalDecision requires user_response binding")
        return
    text = _string(value.get("text"))
    expected = _string(value.get("sha256"))
    if not text:
        errors.append("ApprovalDecision user_response.text must be a non-empty string")
    if not _is_sha256(expected):
        errors.append("ApprovalDecision user_response.sha256 must be a lowercase SHA-256 hex string")
    elif hashlib.sha256(text.encode("utf-8")).hexdigest() != expected:
        errors.append("ApprovalDecision user_response.sha256 does not match user_response.text")


def _evaluate_source_refs(
    record: dict[str, Any],
    root: str | Path | None,
    errors: list[str],
    stale: list[dict[str, Any]],
) -> None:
    refs = record.get("source_refs")
    if refs is None:
        errors.append("decision record requires source_refs")
        return
    if not isinstance(refs, list) or not refs:
        errors.append("source_refs must be a non-empty list when present")
        return
    if root is None:
        errors.append("source_refs require project root for freshness")
        return
    root_path = Path(root)
    for index, item in enumerate(refs):
        label = f"source_refs[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        relative_path = _string(item.get("path"))
        expected_hash = _string(item.get("sha256"))
        if not relative_path:
            errors.append(f"{label}.path must be a non-empty string")
            continue
        if not _is_sha256(expected_hash):
            errors.append(f"{label}.sha256 must be a lowercase SHA-256 hex string")
            continue
        source_path = _resolve_ref(root_path, relative_path, label, errors)
        if source_path is None:
            continue
        if not source_path.exists() or not source_path.is_file():
            stale.append({"path": _normalize_ref(relative_path), "expected_sha256": expected_hash, "actual_sha256": None})
            continue
        actual_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            stale.append({"path": _normalize_ref(relative_path), "expected_sha256": expected_hash, "actual_sha256": actual_hash})


def _reject_lifecycle_transition_authority(record: dict[str, Any], errors: list[str]) -> None:
    if record.get("lifecycle_transition") is True:
        errors.append("decision/receipt records cannot declare lifecycle transition")
    lifecycle = record.get("lifecycle") if isinstance(record.get("lifecycle"), dict) else {}
    if lifecycle.get("target_state") and lifecycle.get("target_state") != lifecycle.get("current_state"):
        errors.append("decision/receipt records cannot transition lifecycle")


def _is_broad_approval_text(normalized: str) -> bool:
    return normalized in BROAD_APPROVAL_TEXT or any(fragment in normalized for fragment in BROAD_APPROVAL_FRAGMENTS)


def _record_id(record: dict[str, Any]) -> str:
    for key in ("decision_id", "receipt_id", "record_id"):
        value = _string(record.get(key))
        if value:
            return value
    return ""


def _present_string_list(record: dict[str, Any], key: str, errors: list[str]) -> list[str]:
    if key not in record:
        errors.append(f"{key} must be present")
        return []
    value = record.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be a list")
        return []
    parsed = _string_list(value)
    if len(parsed) != len(value):
        errors.append(f"{key} must contain only non-empty strings")
    return parsed


def _reject_broad_paths(label: str, values: list[str], errors: list[str]) -> None:
    for value in values:
        normalized = _normalize_path(value)
        if not normalized or normalized in {".", "\\", "/", "<repo root>"} or "*" in normalized or normalized.endswith(":\\"):
            errors.append(f"{label} contains broad path: {value}")


def _is_risky_side_effect(value: str) -> bool:
    normalized = _normalize_text(value)
    return any(fragment in normalized for fragment in RISKY_SIDE_EFFECT_FRAGMENTS)


def _resolve_ref(root: str | Path, value: str, label: str, errors: list[str]) -> Path | None:
    if _is_absolute_or_escape(value):
        errors.append(f"{label} must stay under project root")
        return None
    root_path = Path(root).resolve()
    candidate = (root_path / _normalize_ref(value)).resolve()
    try:
        candidate.relative_to(root_path)
    except ValueError:
        errors.append(f"{label} must stay under project root")
        return None
    return candidate


def _find_project_root(path: Path) -> Path | None:
    resolved = path.resolve()
    for candidate in (resolved.parent, *resolved.parents):
        if (candidate / "CURRENT.md").exists():
            return candidate
    return None


def _string(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


def _normalize_path(value: str) -> str:
    normalized = value.strip().replace("/", "\\")
    while normalized.startswith(".\\"):
        normalized = normalized[2:]
    return normalized.casefold()


def _normalize_ref(value: str) -> str:
    normalized = value.strip().replace("/", "\\")
    while normalized.startswith(".\\"):
        normalized = normalized[2:]
    return normalized


def _is_absolute_or_escape(value: str) -> bool:
    stripped = value.strip()
    path = PureWindowsPath(stripped)
    return path.is_absolute() or bool(path.drive) or stripped.startswith(("\\", "/")) or any(part == ".." for part in path.parts)


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)
