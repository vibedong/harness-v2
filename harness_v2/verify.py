from __future__ import annotations

from pathlib import Path

from .core import ValidationResult, validate_task_file


def verify_task(path: str | Path) -> ValidationResult:
    return validate_task_file(path)
