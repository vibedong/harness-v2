from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import read_current_status
from .doctor import inspect_project
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

    doctor = subparsers.add_parser("doctor", help="Report read-only next action and local project shape.")
    doctor.add_argument("--root", default=".", help="HARNESS V2 product root. Defaults to current directory.")

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
            print(json.dumps({"ok": True, "task_id": result.task_id}, sort_keys=True))
            return 0
        print("\n".join(result.errors), file=sys.stderr)
        return 1

    if args.command == "doctor":
        payload = inspect_project(Path(args.root))
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2
