from __future__ import annotations

from pathlib import Path
from typing import Any

from .core import project_shape, read_current_status


def inspect_project(root: str | Path) -> dict[str, Any]:
    root_path = Path(root)
    status = read_current_status(root_path)
    shape = project_shape(root_path)
    return {
        "mutation": "none",
        "workflow": status["workflow"],
        "state": status["state"],
        "release_ready": False,
        "shape": shape,
        "next_action": "Use verify on a task file, or keep release/package/install work closed until a later exact packet.",
    }
