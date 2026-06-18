from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .core import load_json, validate_task_file


@dataclass(frozen=True)
class PreflightResult:
    ok: bool
    task_id: str | None
    mode: str
    side_effect: str | None
    path: str | None
    errors: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "task_id": self.task_id,
            "mode": self.mode,
            "side_effect": self.side_effect,
            "path": self.path,
            "errors": list(self.errors),
        }


def evaluate_preflight(
    task_path: str | Path,
    *,
    side_effect: str | None = None,
    path: str | None = None,
    mode: str = "command",
) -> PreflightResult:
    errors: list[str] = []
    normalized_mode = mode.strip().casefold()
    if normalized_mode not in {"command", "read", "write"}:
        errors.append(f"mode must be one of command, read, or write: {mode}")

    validation = validate_task_file(task_path)
    if not validation.ok:
        errors.extend(f"task: {error}" for error in validation.errors)
        return PreflightResult(False, validation.task_id, normalized_mode, side_effect, path, tuple(errors))

    payload = load_json(task_path)
    approval = payload.get("approval") if isinstance(payload.get("approval"), dict) else {}
    permission = payload.get("permission") if isinstance(payload.get("permission"), dict) else {}

    approved_paths = _string_list(approval.get("approved_paths"))
    allowed_side_effects = _string_list(permission.get("allowed_side_effects"))
    denied_side_effects = _string_list(permission.get("denied_side_effects"))
    excluded_side_effects = _string_list(approval.get("excluded_side_effects"))

    if side_effect:
        _check_side_effect(side_effect, allowed_side_effects, denied_side_effects, excluded_side_effects, errors)
    if path:
        _check_path(path, normalized_mode, approved_paths, errors)
    if not side_effect and not path:
        errors.append("preflight requires --side-effect, --path, or both")

    return PreflightResult(not errors, validation.task_id, normalized_mode, side_effect, path, tuple(errors))


def _check_side_effect(
    side_effect: str,
    allowed_side_effects: list[str],
    denied_side_effects: list[str],
    excluded_side_effects: list[str],
    errors: list[str],
) -> None:
    normalized = _normalize_text(side_effect)
    if any(_side_effect_conflicts(normalized, denied) for denied in denied_side_effects):
        errors.append(f"side effect conflicts with permission.denied_side_effects: {side_effect}")
    if any(_side_effect_conflicts(normalized, excluded) for excluded in excluded_side_effects):
        errors.append(f"side effect conflicts with approval.excluded_side_effects: {side_effect}")
    if not any(normalized == _normalize_text(allowed) for allowed in allowed_side_effects):
        errors.append(f"side effect is not explicitly allowed: {side_effect}")


def _check_path(path: str, mode: str, approved_paths: list[str], errors: list[str]) -> None:
    if mode != "write":
        return
    normalized = _normalize_path(path)
    if not any(_path_matches(normalized, approved) for approved in approved_paths):
        errors.append(f"write path is not approved: {path}")


def _side_effect_conflicts(normalized_side_effect: str, denied_or_excluded: str) -> bool:
    normalized_denied = _normalize_text(denied_or_excluded)
    return bool(normalized_denied and normalized_denied in normalized_side_effect)


def _path_matches(normalized_path: str, approved_path: str) -> bool:
    normalized_approved = _normalize_path(approved_path)
    return normalized_path == normalized_approved


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


def _normalize_path(value: str) -> str:
    normalized = value.strip().replace("/", "\\")
    while normalized.startswith(".\\"):
        normalized = normalized[2:]
    return normalized.casefold()
