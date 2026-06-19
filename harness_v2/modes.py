from __future__ import annotations

from dataclasses import dataclass
from typing import Any


TASK_MODES = frozenset(
    {
        "setup_only",
        "read_only_analysis",
        "scaffold_only",
        "planned_change",
        "defect_repair",
        "continuity_only",
    }
)
RECORD_STRENGTHS = frozenset({"minimal", "light", "strict"})
STRENGTH_RANK = {"minimal": 0, "light": 1, "strict": 2}
STAGE_MINIMUMS = {
    "spec": "light",
    "spec_review": "light",
    "plan": "light",
    "plan_review": "strict",
    "plan_approval": "strict",
    "development": "light",
    "development_review": "strict",
    "improvement": "light",
}
TASK_MODE_DEFAULTS = {
    "setup_only": "minimal",
    "read_only_analysis": "light",
    "scaffold_only": "light",
    "planned_change": "light",
    "defect_repair": "strict",
    "continuity_only": "light",
}
PROOF_PROFILE_STRENGTHS = {
    "none": "minimal",
    "basic": "light",
    "current": "strict",
    "strict": "strict",
}
STRICT_SIDE_EFFECT_FRAGMENTS = (
    "write",
    "modify",
    "create",
    "delete",
    "remove",
    "move",
    "rename",
    "commit",
    "push",
    "publish",
    "release",
    "deploy",
    "install",
    "package",
    "secret",
    "external network",
    "destructive",
)


@dataclass(frozen=True)
class ModeEvaluation:
    task_mode: str
    record_strength: str
    effective_record_strength: str
    classification_required: bool
    risk_flags: tuple[str, ...]
    proof_profile: str
    capability_request: tuple[str, ...]
    record_density: dict[str, Any]
    strength_inputs: dict[str, str]
    errors: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "task_mode": self.task_mode,
            "record_strength": self.record_strength,
            "effective_record_strength": self.effective_record_strength,
            "classification_required": self.classification_required,
            "risk_flags": list(self.risk_flags),
            "proof_profile": self.proof_profile,
            "capability_request": list(self.capability_request),
            "record_density": dict(self.record_density),
            "strength_inputs": dict(self.strength_inputs),
        }


def evaluate_mode(
    data: dict[str, Any],
    stage: str | None,
    compatibility_mode: bool,
    *,
    freshness: dict[str, Any] | None = None,
) -> ModeEvaluation:
    errors: list[str] = []
    task_mode = _task_mode(data, compatibility_mode, errors)
    record_strength = _record_strength(data, compatibility_mode, errors)
    risk_flags = _string_list(data.get("risk_flags"), "risk_flags", errors, required=not compatibility_mode)
    capability_request = _capability_request(data.get("capability_request"), compatibility_mode, errors)
    proof_profile = _proof_profile(data, compatibility_mode, errors)
    classification_required = _classification_required(data, compatibility_mode, errors)

    source = data.get("source") if isinstance(data.get("source"), dict) else {}
    approval = data.get("approval") if isinstance(data.get("approval"), dict) else {}
    permission = data.get("permission") if isinstance(data.get("permission"), dict) else {}
    proof = data.get("proof") if isinstance(data.get("proof"), dict) else {}
    lifecycle = data.get("lifecycle") if isinstance(data.get("lifecycle"), dict) else {}

    approved_paths = _string_list(approval.get("approved_paths"), "approval.approved_paths", [])
    allowed_side_effects = _string_list(permission.get("allowed_side_effects"), "permission.allowed_side_effects", [])
    proof_obligations = _string_list(proof.get("obligations"), "proof.obligations", [])
    source_basis = _string_list(source.get("basis"), "source.basis", [])
    record_density = _record_density(data.get("record_density"), compatibility_mode, errors)

    strength_inputs = {
        "stage_minimum": STAGE_MINIMUMS.get(stage or "", "light"),
        "task_mode_default": TASK_MODE_DEFAULTS.get(task_mode, "strict"),
        "record_strength": record_strength if record_strength in RECORD_STRENGTHS else "strict",
        "risk_flags": "strict" if risk_flags else "minimal",
        "proof_profile": PROOF_PROFILE_STRENGTHS.get(proof_profile, "strict"),
        "capability_request": "strict" if _has_capability_request(capability_request) else "minimal",
        "classification_required": "strict" if classification_required else "minimal",
        "write_surface": "strict" if _has_write_surface(task_mode, approved_paths, allowed_side_effects) else "minimal",
        "proof_obligations": "strict" if _has_real_proof_obligation(proof_obligations) else "minimal",
        "lifecycle": "strict" if _lifecycle_moves(lifecycle) else "minimal",
        "stale_status": "strict" if _freshness_has_stale(freshness) else "minimal",
        "source_volume": _source_volume_strength(source),
    }
    effective = max(strength_inputs.values(), key=lambda value: STRENGTH_RANK.get(value, STRENGTH_RANK["strict"]))

    _validate_record_density(
        task_mode,
        approved_paths,
        allowed_side_effects,
        source_basis,
        record_density,
        effective,
        errors,
    )

    return ModeEvaluation(
        task_mode=task_mode,
        record_strength=record_strength,
        effective_record_strength=effective,
        classification_required=classification_required,
        risk_flags=tuple(risk_flags),
        proof_profile=proof_profile,
        capability_request=tuple(capability_request),
        record_density=record_density,
        strength_inputs=strength_inputs,
        errors=tuple(errors),
    )


def _task_mode(data: dict[str, Any], compatibility_mode: bool, errors: list[str]) -> str:
    value = data.get("task_mode")
    if value is None:
        if not compatibility_mode:
            errors.append("strict task contracts require task_mode")
        return "planned_change"
    if not isinstance(value, str) or not value.strip():
        errors.append("task_mode must be a non-empty string when present")
        return "planned_change"
    if value not in TASK_MODES:
        errors.append(f"task_mode is not known: {value}")
        return value
    return value


def _record_strength(data: dict[str, Any], compatibility_mode: bool, errors: list[str]) -> str:
    value = data.get("record_strength")
    if value is None:
        if not compatibility_mode:
            errors.append("strict task contracts require record_strength")
        return "light"
    if not isinstance(value, str) or not value.strip():
        errors.append("record_strength must be a non-empty string when present")
        return "minimal"
    if value not in RECORD_STRENGTHS:
        errors.append(f"record_strength is not known: {value}")
        return value
    return value


def _proof_profile(data: dict[str, Any], compatibility_mode: bool, errors: list[str]) -> str:
    value = data.get("proof_profile")
    if value is None:
        if not compatibility_mode:
            errors.append("strict task contracts require proof_profile")
        return "current" if _has_real_proof_obligation(_string_list((data.get("proof") or {}).get("obligations") if isinstance(data.get("proof"), dict) else None, "proof.obligations", [])) else "none"
    if not isinstance(value, str) or not value.strip():
        errors.append("proof_profile must be a non-empty string when present")
        return "strict"
    if value not in PROOF_PROFILE_STRENGTHS:
        errors.append(f"proof_profile is not known: {value}")
    return value


def _classification_required(data: dict[str, Any], compatibility_mode: bool, errors: list[str]) -> bool:
    value = data.get("classification_required")
    if value is None:
        if not compatibility_mode:
            errors.append("strict task contracts require classification_required")
        return False
    if not isinstance(value, bool):
        errors.append("classification_required must be a boolean when present")
        return True
    return value


def _capability_request(value: Any, compatibility_mode: bool, errors: list[str]) -> list[str]:
    if value is None:
        if not compatibility_mode:
            errors.append("strict task contracts require capability_request")
        return []
    if isinstance(value, str):
        if not value.strip():
            errors.append("capability_request must be a non-empty string when present")
            return []
        return [value.strip()]
    return _string_list(value, "capability_request", errors)


def _string_list(value: Any, label: str, errors: list[str], *, required: bool = False) -> list[str]:
    if value is None:
        if required:
            errors.append(f"strict task contracts require {label}")
        return []
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return []
    parsed = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if len(parsed) != len(value):
        errors.append(f"{label} must contain only non-empty strings")
    return parsed


def _record_density(value: Any, compatibility_mode: bool, errors: list[str]) -> dict[str, Any]:
    default = {
        "generated_file_count": 0,
        "required_read_set_size": 1,
        "field_presence": "light",
    }
    if value is None:
        if not compatibility_mode:
            errors.append("strict task contracts require record_density")
        return default
    if not isinstance(value, dict):
        errors.append("record_density must be an object when present")
        return default

    result = dict(default)
    for key in ("generated_file_count", "required_read_set_size"):
        item = value.get(key)
        if not isinstance(item, int) or item < 0:
            errors.append(f"record_density.{key} must be a non-negative integer")
        else:
            result[key] = item
    field_presence = value.get("field_presence")
    if not isinstance(field_presence, str) or not field_presence.strip():
        errors.append("record_density.field_presence must be a non-empty string")
    elif field_presence not in RECORD_STRENGTHS:
        errors.append(f"record_density.field_presence is not known: {field_presence}")
    else:
        result["field_presence"] = field_presence
    return result


def _validate_record_density(
    task_mode: str,
    approved_paths: list[str],
    allowed_side_effects: list[str],
    source_basis: list[str],
    record_density: dict[str, Any],
    effective_record_strength: str,
    errors: list[str],
) -> None:
    if task_mode == "read_only_analysis" and _has_mutating_side_effect(allowed_side_effects):
        errors.append("read_only_analysis task_mode cannot allow mutating side effects")
    if task_mode == "setup_only" and _has_release_or_external_side_effect(allowed_side_effects):
        errors.append("setup_only task_mode cannot allow publish, release, external, secret, or destructive side effects")
    if task_mode == "scaffold_only" and record_density["generated_file_count"] == 0:
        errors.append("scaffold_only task_mode requires record_density.generated_file_count greater than 0")
    if record_density["generated_file_count"] > len(approved_paths):
        errors.append("record_density.generated_file_count cannot exceed approval.approved_paths count")
    if record_density["required_read_set_size"] > len(source_basis):
        errors.append("record_density.required_read_set_size cannot exceed source.basis count")
    if STRENGTH_RANK.get(record_density["field_presence"], 0) < STRENGTH_RANK.get(effective_record_strength, 0):
        errors.append("record_density.field_presence must be at least effective_record_strength")


def _has_write_surface(task_mode: str, paths: list[str], side_effects: list[str]) -> bool:
    if _has_mutating_side_effect(side_effects):
        return True
    if task_mode == "read_only_analysis":
        return False
    return bool(paths)


def _has_mutating_side_effect(side_effects: list[str]) -> bool:
    return any(any(fragment in value.casefold() for fragment in STRICT_SIDE_EFFECT_FRAGMENTS) for value in side_effects)


def _has_release_or_external_side_effect(side_effects: list[str]) -> bool:
    fragments = ("publish", "release", "external", "secret", "destructive")
    return any(any(fragment in value.casefold() for fragment in fragments) for value in side_effects)


def _has_real_proof_obligation(obligations: list[str]) -> bool:
    if not obligations:
        return False
    return any(value.casefold() not in {"none", "not_required", "not required", "no proof required"} for value in obligations)


def _has_capability_request(values: list[str]) -> bool:
    return any(value.casefold() not in {"none", "not_required", "not required"} for value in values)


def _lifecycle_moves(lifecycle: dict[str, Any]) -> bool:
    current = lifecycle.get("current_state")
    target = lifecycle.get("target_state")
    return isinstance(current, str) and isinstance(target, str) and current != target


def _source_volume_strength(source: dict[str, Any]) -> str:
    basis = source.get("basis")
    if isinstance(basis, list) and len(basis) > 6:
        return "strict"
    return "minimal"


def _freshness_has_stale(freshness: dict[str, Any] | None) -> bool:
    if not freshness:
        return False
    stale = freshness.get("stale")
    errors = freshness.get("errors")
    return bool(stale or errors)
