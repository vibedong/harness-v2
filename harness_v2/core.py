from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_TASK_OBJECTS = (
    "source",
    "approval",
    "permission",
    "proof",
    "lifecycle",
)


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    task_id: str | None
    errors: tuple[str, ...]


def load_json(path: str | Path) -> dict[str, Any]:
    payload_path = Path(path)
    with payload_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{payload_path} must contain a JSON object")
    return data


def validate_task_file(path: str | Path) -> ValidationResult:
    try:
        data = load_json(path)
    except Exception as exc:  # pragma: no cover - exact parser messages vary.
        return ValidationResult(False, None, (f"json: {exc}",))
    return validate_task(data)


def validate_task(data: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    task_id = data.get("task_id")

    for key in ("task_id", "title", "workflow"):
        if not _non_empty_string(data.get(key)):
            errors.append(f"{key} must be a non-empty string")

    for key in REQUIRED_TASK_OBJECTS:
        if not isinstance(data.get(key), dict):
            errors.append(f"{key} must be an object")

    source = data.get("source") if isinstance(data.get("source"), dict) else {}
    if not _non_empty_list(source.get("basis")):
        errors.append("source.basis must be a non-empty list")
    if not _non_empty_string(source.get("current_pointer")):
        errors.append("source.current_pointer must be a non-empty string")

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

    return ValidationResult(
        ok=not errors,
        task_id=task_id if isinstance(task_id, str) else None,
        errors=tuple(errors),
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
    files = [path for path in root_path.rglob("*") if path.is_file()]
    dirs = [path for path in root_path.iterdir() if path.is_dir()]
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
