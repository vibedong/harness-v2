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
        "substate": status["substate"],
        "release_ready": False,
        "integrated_surfaces": [
            "init",
            "status",
            "verify",
            "preflight",
            "gate",
            "mcp",
            "doctor",
            "npm-wrapper",
        ],
        "recommended_sequence": [
            "harness-v2 status --root .",
            "harness-v2 verify contracts\\harness-task.json",
            "harness-v2 gate contracts\\harness-task.json --root .",
        ],
        "release_boundary": {
            "status": "closed",
            "denied": [
                "npm publish",
                "Python package registry publish",
                "GitHub release creation",
                "release tag creation",
            ],
        },
        "shape": shape,
        "next_action": "Use the remaining completion sequence, then keep release/package/install work closed until a later exact packet.",
    }
