from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


CURRENT_LAYOUT_VERSION = "legacy-control-records-v1"
KNOWN_LAYOUT_VERSIONS = frozenset({CURRENT_LAYOUT_VERSION})
GENERATED_SCAFFOLD_PATHS = (
    "AGENTS.md",
    "RULES.md",
    "CURRENT.md",
    "control/source.md",
    "control/approval.md",
    "control/permission.md",
    "control/proof.md",
    "control/lifecycle.md",
    "records/README.md",
    "records/current-task.md",
    "records/stages/spec.md",
    "records/stages/spec-review.md",
    "records/stages/plan.md",
    "records/stages/plan-review.md",
    "records/stages/plan-approval.md",
    "records/stages/development.md",
    "records/stages/development-review.md",
    "records/stages/improvement.md",
    "records/decisions.md",
    "records/proof.md",
    "records/handoff.md",
    "contracts/harness-task.json",
    "templates/task.json",
)
SOURCE_PACKAGE_SURFACES = (
    "AGENTS.md",
    "RULES.md",
    "CURRENT.md",
    "README.md",
    "package.json",
    "pyproject.toml",
    "bin/harness-v2.js",
    "harness_v2/cli.py",
    "harness_v2/core.py",
    "harness_v2/doctor.py",
    "harness_v2/layout.py",
    "harness_v2/preflight.py",
    "harness_v2/gate.py",
    "harness_v2/lifecycle.py",
    "harness_v2/freshness.py",
    "harness_v2/modes.py",
    "harness_v2/decisions.py",
    "harness_v2/mcp.py",
    "contracts/*.schema.json",
    "templates/*.json",
    "templates/*.md",
    "control/*.md",
    "records/README.md",
    "routing/manifest.md",
    "safety/*.md",
    "release/transaction.md",
)


@dataclass(frozen=True)
class HarnessLayout:
    task_contract: Path = Path("contracts") / "harness-task.json"
    gate_state: Path = Path("records") / "gate-state.json"
    freshness_map: Path = Path("records") / "freshness-map.json"
    lifecycle_control: Path = Path("control") / "lifecycle.md"
    current_pointer: Path = Path("CURRENT.md")

    def resolve(self, root: str | Path, relative_path: Path) -> Path:
        return Path(root) / relative_path


DEFAULT_LAYOUT = HarnessLayout()


def current_layout_report() -> dict[str, object]:
    return {
        "layout_version": CURRENT_LAYOUT_VERSION,
        "current_layout_paths_active": True,
        "domain_layout_enabled": False,
        "domain_layout_candidate": False,
    }


def runtime_lookup_paths() -> dict[str, str]:
    return {
        "task_contract": DEFAULT_LAYOUT.task_contract.as_posix(),
        "gate_state": DEFAULT_LAYOUT.gate_state.as_posix(),
        "freshness_map": DEFAULT_LAYOUT.freshness_map.as_posix(),
        "lifecycle_control": DEFAULT_LAYOUT.lifecycle_control.as_posix(),
        "current_pointer": DEFAULT_LAYOUT.current_pointer.as_posix(),
    }


def domain_layout_migration_report() -> dict[str, object]:
    return {
        "current_layout_version": CURRENT_LAYOUT_VERSION,
        "generated_scaffold_paths": list(GENERATED_SCAFFOLD_PATHS),
        "source_package_surfaces": list(SOURCE_PACKAGE_SURFACES),
        "runtime_lookup_paths": runtime_lookup_paths(),
        "domain_layout_candidate": False,
        "migration_required": False,
        "migration_blockers": [],
    }


def resolve_layout_version(value: object) -> tuple[str, tuple[str, ...]]:
    if not isinstance(value, str) or not value.strip():
        return CURRENT_LAYOUT_VERSION, ()
    version = value.strip()
    if version in KNOWN_LAYOUT_VERSIONS:
        return version, ()
    return version, (f"unknown layout_version: {version}; migration required before using this layout",)
