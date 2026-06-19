from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, TextIO

from . import __version__
from .core import initialize_project, read_current_status
from .decisions import evaluate_decision_file
from .gate import evaluate_gate
from .preflight import evaluate_preflight
from .verify import verify_task

PROTOCOL_VERSION = "2025-06-18"


def run_stdio_server(stdin: TextIO | None = None, stdout: TextIO | None = None) -> int:
    input_stream = stdin if stdin is not None else sys.stdin
    output_stream = stdout if stdout is not None else sys.stdout

    for raw_line in input_stream:
        line = raw_line.strip()
        if not line:
            continue
        response = handle_message(line)
        if response is None:
            continue
        output_stream.write(json.dumps(response, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        output_stream.write("\n")
        output_stream.flush()
    return 0


def handle_message(line: str) -> dict[str, Any] | None:
    try:
        message = json.loads(line)
    except json.JSONDecodeError as exc:
        return _error(None, -32700, f"Parse error: {exc.msg}")
    if not isinstance(message, dict):
        return _error(None, -32600, "Invalid Request")

    request_id = message.get("id")
    method = message.get("method")
    if not isinstance(method, str):
        return _error(request_id, -32600, "Invalid Request")

    if request_id is None:
        _handle_notification(method)
        return None

    params = message.get("params")
    try:
        if method == "initialize":
            return _result(request_id, _initialize_result(params))
        if method == "ping":
            return _result(request_id, {})
        if method == "tools/list":
            return _result(request_id, {"tools": _tools()})
        if method == "tools/call":
            return _result(request_id, _call_tool(params))
    except ValueError as exc:
        return _error(request_id, -32602, str(exc))
    except Exception as exc:  # pragma: no cover - defensive JSON-RPC boundary.
        return _error(request_id, -32603, f"Internal error: {exc}")

    return _error(request_id, -32601, f"Method not found: {method}")


def _handle_notification(method: str) -> None:
    if method == "notifications/initialized":
        return


def _initialize_result(params: Any) -> dict[str, Any]:
    requested_version = None
    if isinstance(params, dict) and isinstance(params.get("protocolVersion"), str):
        requested_version = params["protocolVersion"]
    return {
        "protocolVersion": requested_version or PROTOCOL_VERSION,
        "capabilities": {"tools": {"listChanged": False}},
        "serverInfo": {
            "name": "harness-v2",
            "title": "HARNESS V2",
            "version": __version__,
        },
        "instructions": (
            "HARNESS V2 MCP is a thin adapter over the local CLI/core. "
            "It does not replace CURRENT.md, task contracts, approval, permission, proof, or lifecycle surfaces."
        ),
    }


def _tools() -> list[dict[str, Any]]:
    return [
        {
            "name": "harness_status",
            "title": "HARNESS V2 Status",
            "description": "Read CURRENT.md from a HARNESS V2 root and return workflow, state, and substate.",
            "inputSchema": {
                "type": "object",
                "properties": {"root": {"type": "string", "description": "HARNESS V2 root. Defaults to current directory."}},
                "additionalProperties": False,
            },
        },
        {
            "name": "harness_verify",
            "title": "HARNESS V2 Verify",
            "description": "Validate a HARNESS V2 task contract file.",
            "inputSchema": {
                "type": "object",
                "properties": {"task": {"type": "string", "description": "Path to the task JSON file."}},
                "required": ["task"],
                "additionalProperties": False,
            },
        },
        {
            "name": "harness_preflight",
            "title": "HARNESS V2 Preflight",
            "description": "Check a proposed side effect or write path against a task contract before acting.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "Path to the task JSON file."},
                    "side_effect": {"type": "string", "description": "Proposed command or side-effect label."},
                    "path": {"type": "string", "description": "Proposed path to check."},
                    "mode": {
                        "type": "string",
                        "enum": ["command", "read", "write"],
                        "description": "Preflight mode. Write mode checks approval.approved_paths.",
                    },
                },
                "required": ["task"],
                "additionalProperties": False,
            },
        },
        {
            "name": "harness_gate",
            "title": "HARNESS V2 Hook-Equivalent Gate",
            "description": "Run status, verify, and optional preflight checks as a hook-equivalent gate. This does not automatically block shell or editor actions.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "Path to the task JSON file."},
                    "root": {"type": "string", "description": "HARNESS V2 root. Defaults to current directory."},
                    "side_effects": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Proposed commands or side-effect labels to check.",
                    },
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Proposed paths to check.",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["command", "read", "write"],
                        "description": "Preflight mode for proposed paths. Write mode checks approval.approved_paths.",
                    },
                },
                "required": ["task"],
                "additionalProperties": False,
            },
        },
        {
            "name": "harness_decision",
            "title": "HARNESS V2 Decision Record Verify",
            "description": "Validate an ApprovalDecision, PermissionDecision, or ProofReceipt record against an optional task contract.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "record": {"type": "string", "description": "Path to the decision or receipt JSON file."},
                    "task": {"type": "string", "description": "Optional task JSON file to bind the record against."},
                    "root": {"type": "string", "description": "HARNESS V2 root. Defaults to current directory."},
                },
                "required": ["record"],
                "additionalProperties": False,
            },
        },
        {
            "name": "harness_init",
            "title": "HARNESS V2 Init",
            "description": "Apply HARNESS V2 scaffold files to a project root.",
            "inputSchema": _init_apply_schema(),
            "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
        },
        {
            "name": "harness_apply",
            "title": "HARNESS V2 Apply",
            "description": "Alias for init: apply HARNESS V2 scaffold files to a project root.",
            "inputSchema": _init_apply_schema(),
            "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
        },
    ]


def _init_apply_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "root": {"type": "string", "description": "Project root to initialize or apply. Defaults to current directory."},
            "force": {"type": "boolean", "description": "Overwrite existing scaffold files. Defaults to false."},
        },
        "additionalProperties": False,
    }


def _call_tool(params: Any) -> dict[str, Any]:
    if not isinstance(params, dict):
        raise ValueError("tools/call params must be an object")
    name = params.get("name")
    arguments = params.get("arguments", {})
    if not isinstance(name, str):
        raise ValueError("tools/call params.name must be a string")
    if not isinstance(arguments, dict):
        raise ValueError("tools/call params.arguments must be an object")

    if name == "harness_status":
        payload = {"ok": True, "status": read_current_status(Path(_string_arg(arguments, "root", ".")))}
    elif name == "harness_verify":
        result = verify_task(Path(_required_string_arg(arguments, "task")))
        payload = {
            "ok": result.ok,
            "task_id": result.task_id,
            "errors": list(result.errors),
            "current_gate": result.current_gate,
            "task_mode": result.task_mode,
            "record_strength": result.record_strength,
            "effective_record_strength": result.effective_record_strength,
            "classification_required": result.classification_required,
            "compatibility_mode": result.compatibility_mode,
            "gate_state": result.gate_state,
            "freshness": result.freshness,
            "mode_profile": result.mode_profile,
        }
    elif name == "harness_preflight":
        result = evaluate_preflight(
            Path(_required_string_arg(arguments, "task")),
            side_effect=_optional_string_arg(arguments, "side_effect"),
            path=_optional_string_arg(arguments, "path"),
            mode=_string_arg(arguments, "mode", "command"),
        )
        payload = result.to_json()
    elif name == "harness_gate":
        result = evaluate_gate(
            Path(_required_string_arg(arguments, "task")),
            root=Path(_string_arg(arguments, "root", ".")),
            side_effects=_optional_string_list_arg(arguments, "side_effects"),
            paths=_optional_string_list_arg(arguments, "paths"),
            mode=_string_arg(arguments, "mode", "command"),
        )
        payload = result.to_json()
    elif name == "harness_decision":
        result = evaluate_decision_file(
            Path(_required_string_arg(arguments, "record")),
            task_path=Path(_optional_string_arg(arguments, "task")) if _optional_string_arg(arguments, "task") else None,
            root=Path(_string_arg(arguments, "root", ".")),
        )
        payload = result.to_json()
    elif name == "harness_init":
        payload = initialize_project(Path(_string_arg(arguments, "root", ".")), force=_bool_arg(arguments, "force", False)).to_json()
    elif name == "harness_apply":
        payload = initialize_project(Path(_string_arg(arguments, "root", ".")), force=_bool_arg(arguments, "force", False)).to_json()
    else:
        raise ValueError(f"Unknown tool: {name}")
    return _tool_result(payload)


def _tool_result(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, sort_keys=True)}],
        "structuredContent": payload,
        "isError": False,
    }


def _required_string_arg(arguments: dict[str, Any], name: str) -> str:
    value = arguments.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"argument {name} must be a non-empty string")
    return value


def _optional_string_arg(arguments: dict[str, Any], name: str) -> str | None:
    value = arguments.get(name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"argument {name} must be a string")
    return value


def _optional_string_list_arg(arguments: dict[str, Any], name: str) -> list[str]:
    value = arguments.get(name)
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"argument {name} must be an array of strings")
    return value


def _string_arg(arguments: dict[str, Any], name: str, default: str) -> str:
    value = arguments.get(name, default)
    if not isinstance(value, str):
        raise ValueError(f"argument {name} must be a string")
    return value


def _bool_arg(arguments: dict[str, Any], name: str, default: bool) -> bool:
    value = arguments.get(name, default)
    if not isinstance(value, bool):
        raise ValueError(f"argument {name} must be a boolean")
    return value


def _result(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}
