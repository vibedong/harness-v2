from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Any


DEFAULT_MAP_PATH = Path("records") / "freshness-map.json"
COMPATIBILITY_DIAGNOSTIC = (
    "freshness map is absent; compatibility mode keeps verification read-only and does not overwrite existing projects"
)
BACKTRACK_TARGETS_BY_AFFECT = {
    "spec": {"spec"},
    "spec_review": {"spec", "spec_review"},
    "plan": {"plan"},
    "plan_review": {"plan", "plan_review"},
    "plan_approval": {"plan", "plan_approval"},
    "permission": {"plan_approval", "development"},
    "development_transition": {"plan_approval", "development"},
    "proof_receipt": {"development", "development_review"},
    "transition_ledger": {"last_verified_lifecycle_gate"},
    "release_boundary": {"improvement", "blocked_release_audit"},
    "artifact_freshness_refs": {
        "spec",
        "spec_review",
        "plan",
        "plan_review",
        "plan_approval",
        "development",
        "development_review",
        "improvement",
        "last_verified_lifecycle_gate",
        "blocked_release_audit",
    },
}


@dataclass(frozen=True)
class FreshnessEvaluation:
    ok: bool
    present: bool
    stale: tuple[dict[str, Any], ...]
    errors: tuple[str, ...]
    compatibility_diagnostic: str | None = None

    def to_json(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "ok": self.ok,
            "present": self.present,
            "stale": list(self.stale),
            "errors": list(self.errors),
        }
        if self.compatibility_diagnostic is not None:
            payload["compatibility_diagnostic"] = self.compatibility_diagnostic
        return payload


def evaluate_freshness_map(root: str | Path, map_path: str | Path | None = None) -> FreshnessEvaluation:
    root_path = Path(root)
    freshness_path = Path(map_path) if map_path is not None else root_path / DEFAULT_MAP_PATH
    if not freshness_path.exists():
        return FreshnessEvaluation(True, False, (), (), COMPATIBILITY_DIAGNOSTIC)
    if not _under_root(freshness_path.resolve(), root_path):
        return FreshnessEvaluation(False, True, (), ("freshness map path must stay under project root",))

    try:
        payload = json.loads(freshness_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return FreshnessEvaluation(False, True, (), (f"freshness map json: {exc}",))
    if not isinstance(payload, dict):
        return FreshnessEvaluation(False, True, (), ("freshness map must contain a JSON object",))

    anchors = payload.get("anchors")
    if not isinstance(anchors, list):
        return FreshnessEvaluation(False, True, (), ("freshness map anchors must be a list",))

    errors: list[str] = []
    stale: list[dict[str, Any]] = []
    for index, value in enumerate(anchors):
        if not isinstance(value, dict):
            errors.append(f"freshness anchor {index} must be an object")
            continue
        _evaluate_anchor(root_path, index, value, stale, errors)

    return FreshnessEvaluation(not errors and not stale, True, tuple(stale), tuple(errors))


def _evaluate_anchor(
    root: Path,
    index: int,
    anchor: dict[str, Any],
    stale: list[dict[str, Any]],
    errors: list[str],
) -> None:
    anchor_id = _string(anchor.get("id"))
    relative_path = _string(anchor.get("path"))
    expected_hash = _string(anchor.get("source_sha256"))
    affects = _string_list(anchor.get("affects"))
    backtrack_target = _string(anchor.get("backtrack_target"))
    reason = _string(anchor.get("reason"))
    evidence_refs = _evidence_refs(anchor.get("evidence_refs"))

    label = anchor_id or f"anchor-{index}"
    missing = [
        name
        for name, current in (
            ("id", anchor_id),
            ("path", relative_path),
            ("source_sha256", expected_hash),
            ("backtrack_target", backtrack_target),
            ("reason", reason),
        )
        if not current
    ]
    if missing:
        errors.append(f"freshness anchor {label} missing fields: {', '.join(missing)}")
        return
    if not affects:
        errors.append(f"freshness anchor {label} affects must be a non-empty list")
        return
    if not _is_sha256(expected_hash):
        errors.append(f"freshness anchor {label} source_sha256 must be a lowercase SHA-256 hex string")
        return
    if not evidence_refs:
        errors.append(f"freshness anchor {label} evidence_refs must be a non-empty list")
        return
    _validate_backtrack_target(label, affects, backtrack_target, errors)

    normalized = _normalize_ref(relative_path)
    if _is_absolute_windows_ref(relative_path) or _escapes_project_ref(normalized):
        errors.append(f"freshness anchor {label} path must stay under project root")
        return

    source_path = (root / normalized).resolve()
    if not _under_root(source_path, root):
        errors.append(f"freshness anchor {label} path must stay under project root")
        return
    if not source_path.exists():
        stale.append(
            {
                "anchor_id": label,
                "path": normalized,
                "expected_sha256": expected_hash,
                "actual_sha256": None,
                "affects": affects,
                "backtrack_target": backtrack_target,
                "reason": reason,
            }
        )
        return

    if not source_path.is_file():
        errors.append(f"freshness anchor {label} path must reference a file: {normalized}")
        return
    try:
        actual_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    except OSError as exc:
        errors.append(f"freshness anchor {label} path cannot be read: {normalized}: {exc}")
        return

    evidence_errors = _evaluate_evidence_refs(root, label, evidence_refs, expected_hash, errors)
    if actual_hash != expected_hash or evidence_errors:
        stale.append(_stale_item(label, normalized, expected_hash, actual_hash, affects, backtrack_target, reason, evidence_errors))


def _stale_item(
    label: str,
    normalized: str,
    expected_hash: str,
    actual_hash: str | None,
    affects: list[str],
    backtrack_target: str,
    reason: str,
    evidence_errors: list[str] | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "anchor_id": label,
        "path": normalized,
        "expected_sha256": expected_hash,
        "actual_sha256": actual_hash,
        "affects": affects,
        "backtrack_target": backtrack_target,
        "reason": reason,
    }
    if evidence_errors:
        item["evidence_errors"] = evidence_errors
    return item


def _validate_backtrack_target(label: str, affects: list[str], target: str, errors: list[str]) -> None:
    unknown = sorted(set(affects) - BACKTRACK_TARGETS_BY_AFFECT.keys())
    if unknown:
        errors.append(f"freshness anchor {label} affects contains unknown rule keys: {', '.join(unknown)}")
        return

    allowed: set[str] | None = None
    for affect in affects:
        candidates = BACKTRACK_TARGETS_BY_AFFECT[affect]
        allowed = set(candidates) if allowed is None else allowed & candidates
    if allowed is not None and target not in allowed:
        allowed_text = ", ".join(sorted(allowed))
        errors.append(f"freshness anchor {label} backtrack_target {target!r} is not allowed for affects; allowed: {allowed_text}")


def _evaluate_evidence_refs(
    root: Path,
    label: str,
    evidence_refs: list[dict[str, str]],
    expected_hash: str,
    errors: list[str],
) -> list[str]:
    stale: list[str] = []
    expected_bytes = expected_hash.encode("ascii")
    for index, evidence_ref in enumerate(evidence_refs):
        evidence_label = f"{label} evidence_ref {index}"
        relative_path = evidence_ref["path"]
        expected_evidence_hash = evidence_ref["sha256"]
        if _is_absolute_windows_ref(relative_path):
            errors.append(f"freshness anchor {evidence_label} path must be project-relative")
            continue
        normalized = _normalize_ref(relative_path)
        if _escapes_project_ref(normalized):
            errors.append(f"freshness anchor {evidence_label} path must stay under project root")
            continue
        evidence_path = (root / normalized).resolve()
        if not _under_root(evidence_path, root):
            errors.append(f"freshness anchor {evidence_label} path must stay under project root")
            continue
        if not evidence_path.exists():
            stale.append(f"evidence_ref missing: {normalized}")
            continue
        if not evidence_path.is_file():
            errors.append(f"freshness anchor {evidence_label} path must reference a file: {normalized}")
            continue
        try:
            content = evidence_path.read_bytes()
        except OSError as exc:
            errors.append(f"freshness anchor {evidence_label} path cannot be read: {normalized}: {exc}")
            continue
        actual_evidence_hash = hashlib.sha256(content).hexdigest()
        if actual_evidence_hash != expected_evidence_hash:
            stale.append(f"evidence_ref hash changed: {normalized}")
        if expected_bytes not in content:
            stale.append(f"evidence_ref does not bind source_sha256: {normalized}")
    return stale


def _string(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _evidence_refs(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    parsed: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            return []
        path = _string(item.get("path"))
        sha256 = _string(item.get("sha256"))
        if not path or not _is_sha256(sha256):
            return []
        parsed.append({"path": path, "sha256": sha256})
    return parsed


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _normalize_ref(value: str) -> str:
    normalized = value.strip().replace("/", "\\")
    while normalized.startswith(".\\"):
        normalized = normalized[2:]
    return normalized


def _is_absolute_windows_ref(value: str) -> bool:
    path = PureWindowsPath(value.strip())
    return path.is_absolute() or bool(path.drive) or value.strip().startswith(("\\", "/"))


def _escapes_project_ref(value: str) -> bool:
    return any(part == ".." for part in PureWindowsPath(value).parts)


def _under_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True
