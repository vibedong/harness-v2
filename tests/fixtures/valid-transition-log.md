# HARNESS V2 Transition Fixture

Lifecycle movement is an evaluated operation, not a log line.

## transition: 2026-06-19T00:00:00Z
from_gate: spec
to_gate: spec_review
reason: spec ready for review
source_refs: records\stages\spec.md
approval_ref: not_required
permission_ref: not_required
proof_ref: not_required
freshness_refs: records\stages\spec.md
stale_check: fresh
actor: fixture

## transition: 2026-06-19T00:01:00Z
from_gate: plan_approval
to_gate: development
reason: exact plan approval permits development entry
source_refs: CURRENT.md
approval_ref: control\approval.md
permission_ref: control\permission.md
proof_ref: not_required
freshness_refs: CURRENT.md
stale_check: fresh
actor: fixture
