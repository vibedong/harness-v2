from __future__ import annotations

from pathlib import Path
from typing import Any

from .core import is_harness_source_checkout, project_shape, read_current_status
from .layout import domain_layout_migration_report


def inspect_project(root: str | Path) -> dict[str, Any]:
    root_path = Path(root).resolve()
    status = read_current_status(root_path)
    shape = project_shape(root_path)
    source_checkout = is_harness_source_checkout(root_path)
    misinstall_warning = (
        "This root is the HARNESS V2 source repository, not an applied project scaffold. "
        "For project application, install with `npm install -g harness-v2@latest` and run "
        "`harness-v2 init --root <project>`. Do not git clone vibedong/harness-v2 into the target project folder."
        if source_checkout
        else None
    )
    return {
        "mutation": "none",
        "workflow": status["workflow"],
        "state": status["state"],
        "substate": status["substate"],
        "layout_version": status["layout_version"],
        "current_layout_paths_active": status["current_layout_paths_active"],
        "domain_layout_enabled": status["domain_layout_enabled"],
        "domain_layout_candidate": status["domain_layout_candidate"],
        "domain_layout_migration": domain_layout_migration_report(),
        "root_kind": "harness_v2_source_checkout" if source_checkout else "applied_project_or_project_root",
        "source_checkout": source_checkout,
        "applied_project": not source_checkout,
        "misinstall_warning": misinstall_warning,
        "release_ready": False,
        "integrated_surfaces": [
            "init",
            "status",
            "verify",
            "preflight",
            "gate",
            "task-start",
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
        "next_action": (
            "Use npm install -g harness-v2@latest, then run harness-v2 init --root <project>; this source checkout is not the applied project surface."
            if source_checkout
            else "Use the remaining completion sequence, then keep release/package/install work closed until a later exact packet."
        ),
    }
