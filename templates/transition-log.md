# HARNESS V2 Transition Log

lifecycle movement는 evaluated operation이며, log line 자체가 아닙니다.

## transition: <iso8601 timestamp>
from_gate: <spec|spec_review|plan|plan_review|plan_approval|development|development_review|improvement>
to_gate: <spec_review|spec|plan|plan_review|plan_approval|development|development_review|improvement|completed>
reason: <why this transition is requested>
source_refs: <repo-relative source refs>
approval_ref: <approval ref or not_required>
permission_ref: <permission ref or not_required>
proof_ref: <proof ref or not_required>
freshness_refs: <freshness refs>
stale_check: <fresh|stale_approval|stale_permission|stale_proof|stale_source>
actor: <agent or user>
