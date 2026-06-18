# HARNESS V2 Source Control

status: package_github_surface / remaining_completion_program / source_control

This file defines source authority for local HARNESS V2 package and GitHub MVP operation.

## Source Tiers

1. Current product-local files in `F:\Folder\harness-v2` for their own local operating rules.
2. User messages bound to an exact scope for the work unit they name.
3. Active HARNESS V2 planning gates and progress ledgers for historical gate context.
4. Confirmed Stage 00~05 planning artifacts for design intent and boundary language.

Summaries, cached notes, subagent reports, broad approval, old progress text, registry rows, log entries, route suggestions, and placeholder text are not source authority by themselves.

## Freshness

A source is fresh only for the scope it names.

A source becomes stale when target files, write surface, user objective, approval scope, permission scope, proof obligation, lifecycle state, route surface, artifact surface, regression surface, improvement surface, or release boundary changes.

## Conflict Rule

If sources conflict, use the narrowest current source that names the target surface and fail closed until the conflict is resolved.

If a product-local file conflicts with an exact user approval packet for the same work unit, treat the user packet as the write-scope input and update product-local files only inside that packet's target surface.

## Non-Source List

- Tool availability.
- Prior review pass.
- Subagent confidence.
- Registry or log presence.
- Route suggestion.
- Placeholder text.
- File existence alone.
- Heading match alone.
- Search result without readback.

This file does not create approval, permission, proof result, lifecycle state, route permission, regression pass, improvement execution, or release readiness.
