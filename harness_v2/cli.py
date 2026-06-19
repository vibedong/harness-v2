from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import initialize_project, read_current_status
from .doctor import inspect_project
from .gate import evaluate_gate
from .preflight import evaluate_preflight
from .verify import verify_task


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="harness_v2",
        description="HARNESS V2 local executable MVP",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Read CURRENT.md and print workflow status as JSON.")
    status.add_argument("--root", default=".", help="HARNESS V2 product root. Defaults to current directory.")

    verify = subparsers.add_parser("verify", help="Validate a task JSON file against the local MVP contract.")
    verify.add_argument("task", help="Path to a task JSON file.")

    preflight = subparsers.add_parser("preflight", help="Check a proposed side effect or write path against a task contract.")
    preflight.add_argument("task", help="Path to a task JSON file.")
    preflight.add_argument("--side-effect", help="Proposed command or side-effect label to check.")
    preflight.add_argument("--path", help="Proposed path to check.")
    preflight.add_argument("--mode", choices=("command", "read", "write"), default="command", help="Preflight mode. Write mode checks approval.approved_paths.")

    gate = subparsers.add_parser("gate", help="Run hook-equivalent status, verify, and optional preflight checks.")
    gate.add_argument("task", help="Path to a task JSON file.")
    gate.add_argument("--root", default=".", help="HARNESS V2 product root. Defaults to current directory.")
    gate.add_argument("--side-effect", dest="side_effects", action="append", default=[], help="Proposed command or side-effect label to check. May be repeated.")
    gate.add_argument("--path", dest="paths", action="append", default=[], help="Proposed path to check. May be repeated.")
    gate.add_argument("--mode", choices=("command", "read", "write"), default="command", help="Preflight mode for proposed paths. Write mode checks approval.approved_paths.")

    doctor = subparsers.add_parser("doctor", help="Report read-only next action and local project shape.")
    doctor.add_argument("--root", default=".", help="HARNESS V2 product root. Defaults to current directory.")

    subparsers.add_parser("mcp", help="Run the HARNESS V2 MCP stdio adapter.")

    init = subparsers.add_parser("init", help="Apply HARNESS V2 scaffold files to a project root.")
    init.add_argument("--root", default=".", help="Project root to initialize. Defaults to current directory.")
    init.add_argument("--force", action="store_true", help="Overwrite existing HARNESS V2 scaffold files.")

    apply = subparsers.add_parser("apply", help="Alias for init: apply HARNESS V2 to a project root.")
    apply.add_argument("--root", default=".", help="Project root to apply HARNESS V2 to. Defaults to current directory.")
    apply.add_argument("--force", action="store_true", help="Overwrite existing HARNESS V2 scaffold files.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "status":
        payload = read_current_status(Path(args.root))
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return 0

    if args.command == "verify":
        result = verify_task(Path(args.task))
        if result.ok:
            print(json.dumps(_verify_payload(result), sort_keys=True))
            return 0
        print(json.dumps(_verify_payload(result), sort_keys=True))
        print("\n".join(result.errors), file=sys.stderr)
        return 1

    if args.command == "preflight":
        result = evaluate_preflight(
            Path(args.task),
            side_effect=args.side_effect,
            path=args.path,
            mode=args.mode,
        )
        print(json.dumps(result.to_json(), ensure_ascii=False, sort_keys=True))
        return 0 if result.ok else 1

    if args.command == "gate":
        result = evaluate_gate(
            Path(args.task),
            root=Path(args.root),
            side_effects=args.side_effects,
            paths=args.paths,
            mode=args.mode,
        )
        print(json.dumps(result.to_json(), ensure_ascii=False, sort_keys=True))
        return 0 if result.ok else 1

    if args.command == "doctor":
        payload = inspect_project(Path(args.root))
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return 0

    if args.command == "mcp":
        from .mcp import run_stdio_server

        return run_stdio_server()

    if args.command in {"init", "apply"}:
        payload = initialize_project(Path(args.root), force=args.force)
        print(json.dumps(payload.to_json(), ensure_ascii=False, sort_keys=True))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


def _verify_payload(result) -> dict:
    return {
        "ok": result.ok,
        "task_id": result.task_id,
        "errors": list(result.errors),
        "current_gate": result.current_gate,
        "task_mode": result.task_mode,
        "record_strength": result.record_strength,
        "effective_record_strength": result.effective_record_strength,
        "compatibility_mode": result.compatibility_mode,
        "gate_state": result.gate_state,
        "freshness": result.freshness,
    }
