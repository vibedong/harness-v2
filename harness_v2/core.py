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
        (("contracts", "harness-task.json"), _initial_task_json()),
        (("templates", "task.json"), _task_template_json()),
    )


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    task_id: str | None
    errors: tuple[str, ...]


@dataclass(frozen=True)
class InitResult:
    ok: bool
    root: str
    initial_task: str
    created: tuple[str, ...]
    skipped: tuple[str, ...]
    overwritten: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "root": self.root,
            "initial_task": self.initial_task,
            "created": list(self.created),
            "skipped": list(self.skipped),
            "overwritten": list(self.overwritten),
            "next": [
                "harness-v2 status --root .",
                f"harness-v2 verify {self.initial_task}",
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
    root_path = Path(root)
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
        root=str(root_path.resolve()),
        initial_task=INITIAL_TASK_PATH,
        created=tuple(created),
        skipped=tuple(skipped),
        overwritten=tuple(overwritten),
    )


def validate_task(data: dict[str, Any], root: str | Path | None = None) -> ValidationResult:
    errors: list[str] = []
    task_id = data.get("task_id")
    root_path = Path(root) if root is not None else None

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

    _validate_current_context(data, root_path, errors)

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


def _display_path(parts: tuple[str, ...]) -> str:
    return "\\".join(parts)


def _agents_md() -> str:
    return """# HARNESS V2 Agent Entry

Before doing project work, read:

1. `RULES.md`
2. `CURRENT.md`
3. The active task contract, initially `contracts\\harness-task.json`

Run these checks before changing files:

```powershell
harness-v2 status --root .
harness-v2 verify contracts\\harness-task.json
```

Stay inside `approval.approved_paths`. Do not execute `approval.excluded_side_effects` or `permission.denied_side_effects`. If the requested work needs a wider scope, stop and ask for a new task contract.
"""


def _rules_md() -> str:
    return """# HARNESS V2 Project Rules

HARNESS V2 records the current task boundary for AI-assisted work. It is not a sandbox and does not replace human approval.

## Required Flow

1. Read `CURRENT.md`.
2. Read the active task contract.
3. Verify the task contract with `harness-v2 verify <task.json>`.
4. Modify only paths named in `approval.approved_paths`.
5. Do not execute side effects named in `approval.excluded_side_effects` or `permission.denied_side_effects`.
6. Before completion, run or report every item in `proof.obligations`.

If source, approval, permission, proof, lifecycle, or requested paths conflict, fail closed and ask for a new contract.
"""


def _current_md() -> str:
    return """# HARNESS V2 Current State

status: applied_project_surface / init / current_pointer

workflow: `default`

state: `ready`

substate: `initialized`

source basis:

- `AGENTS.md`
- `RULES.md`
- `contracts\\harness-task.json`

## Current Task

The initial task contract is `contracts\\harness-task.json`.

## Stop Conditions

Stop if the requested work needs paths, commands, side effects, secrets, external mutation, dependency changes, package publish, release execution, or destructive operations outside the active task contract.
"""


def _source_md() -> str:
    return """# HARNESS V2 Source Control

status: applied_project_surface / init / source_control

Source basis is declared by each task contract in `source.basis`.

This file is guidance only. The active task contract and `CURRENT.md` decide the current source pointer.
"""


def _approval_md() -> str:
    return """# HARNESS V2 Approval Control

status: applied_project_surface / init / approval_control

Approval is declared by each task contract in `approval.packet` and `approval.approved_paths`.

No file path is approved unless the active task contract names it.
"""


def _permission_md() -> str:
    return """# HARNESS V2 Permission Control

status: applied_project_surface / init / permission_control

Permission is declared by each task contract in `permission.allowed_side_effects` and `permission.denied_side_effects`.

Denied side effects win over broad requests. Secrets, dependency installation, package publish, release execution, external mutation, and destructive operations require a separate explicit task contract.
"""


def _proof_md() -> str:
    return """# HARNESS V2 Proof Control

status: applied_project_surface / init / proof_control

Proof obligations are declared by each task contract in `proof.obligations`.

Do not claim completion until the active proof obligations are run or their blocked status is reported.
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
"""


def _initial_task_json() -> str:
    return """{
  "task_id": "harness-v2-initial-task",
  "title": "Initial HARNESS V2 project binding",
  "workflow": "default",
  "source": {
    "basis": [
      "AGENTS.md",
      "RULES.md",
      "CURRENT.md"
    ],
    "current_pointer": "CURRENT.md"
  },
  "approval": {
    "packet": "Initial local HARNESS V2 project application",
    "approved_paths": [
      "AGENTS.md",
      "RULES.md",
      "CURRENT.md",
      "control\\\\source.md",
      "control\\\\approval.md",
      "control\\\\permission.md",
      "control\\\\proof.md",
      "control\\\\lifecycle.md",
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
      "harness-v2 status --root .",
      "harness-v2 verify contracts\\\\harness-task.json"
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
      "harness-v2 status --root .",
      "harness-v2 verify contracts\\\\harness-task.json"
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
