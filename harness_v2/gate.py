from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .core import read_current_status
from .preflight import PreflightResult, evaluate_preflight
from .verify import verify_task


@dataclass(frozen=True)
class GateResult:
    ok: bool
    task_id: str | None
    root: str
    status: dict[str, str] | None
    verify: dict[str, Any]
    preflight: tuple[PreflightResult, ...]
    errors: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "hook_equivalent": True,
            "automatic_enforcement": False,
            "task_id": self.task_id,
            "root": self.root,
            "status": self.status,
            "verify": self.verify,
            "preflight": [result.to_json() for result in self.preflight],
            "errors": list(self.errors),
        }


def evaluate_gate(
    task_path: str | Path,
    *,
    root: str | Path = ".",
    side_effects: Iterable[str] | None = None,
    paths: Iterable[str] | None = None,
    mode: str = "command",
) -> GateResult:
    root_path = Path(root)
    errors: list[str] = []

    try:
        status = read_current_status(root_path)
    except Exception as exc:
        status = None
        errors.append(f"current status: {exc}")

    validation = verify_task(Path(task_path))
    verify_payload = {
        "ok": validation.ok,
        "task_id": validation.task_id,
        "errors": list(validation.errors),
    }
    errors.extend(f"verify: {error}" for error in validation.errors)

    preflight_results = tuple(
        evaluate_preflight(Path(task_path), side_effect=side_effect, path=path, mode=mode)
        for side_effect, path in _preflight_pairs(side_effects, paths)
    )
    for result in preflight_results:
        errors.extend(f"preflight: {error}" for error in result.errors)

    return GateResult(
        ok=status is not None and validation.ok and all(result.ok for result in preflight_results) and not errors,
        task_id=validation.task_id,
        root=str(root_path),
        status=status,
        verify=verify_payload,
        preflight=preflight_results,
        errors=tuple(errors),
    )


def _preflight_pairs(
    side_effects: Iterable[str] | None,
    paths: Iterable[str] | None,
) -> tuple[tuple[str | None, str | None], ...]:
    side_effect_list = [value for value in (side_effects or []) if value is not None]
    path_list = [value for value in (paths or []) if value is not None]
    if not side_effect_list and not path_list:
        return ()
    count = max(len(side_effect_list), len(path_list))
    return tuple(
        (
            side_effect_list[index] if index < len(side_effect_list) else None,
            path_list[index] if index < len(path_list) else None,
        )
        for index in range(count)
    )
