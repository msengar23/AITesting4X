"""CLI entry point for the Test Plan Agent (SOP_trigger surfaces T1-T3).

Usage:
    py tools/run.py SAM1-1
    py tools/run.py SAM1-1 --instructions "Focus on boundary values"
    py tools/run.py --keys SAM1-1,SAM1-2
    py tools/run.py --project SAM1 --limit 5
    py tools/run.py SAM1-1 --quiet
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.config import load_config  # noqa: E402
from tools.errors import AppError  # noqa: E402
from tools.pipeline import generate_batch, generate_test_plan, resolve_keys  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="run.py",
        description="Generate a Markdown test plan from a Jira issue ID.",
    )
    parser.add_argument(
        "jira_key",
        nargs="?",
        help="Jira issue key, e.g. SAM1-1",
    )
    targets = parser.add_mutually_exclusive_group()
    targets.add_argument(
        "--project",
        default="",
        help="Generate plans for every issue in a Jira project, e.g. SAM1",
    )
    targets.add_argument(
        "--keys",
        default="",
        help="Comma-separated list of issue keys, e.g. SAM1-1,SAM1-2",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Max issues when using --project (default 10, max 50).",
    )
    parser.add_argument(
        "--instructions",
        default="",
        help="Optional extra guidance for the generated plan(s).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress messages.",
    )
    return parser.parse_args(argv)


def _progress(args: argparse.Namespace):
    def progress(message: str) -> None:
        if not args.quiet:
            print(f"[*] {message}")

    return progress


def run_single(args: argparse.Namespace) -> int:
    try:
        result = generate_test_plan(
            args.jira_key,
            instructions=args.instructions,
            on_stage=_progress(args),
        )
    except AppError as exc:
        print(f"[ERROR] {exc.message}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("[ERROR] Cancelled.", file=sys.stderr)
        return 130

    if args.quiet:
        print(result.output_path)
    else:
        print()
        print(f"[OK] Issue:      {result.issue.get('key')} — {result.issue.get('summary')}")
        print(f"[OK] Model:      {result.model}")
        print(f"[OK] Test cases: {len(result.plan.get('test_cases', []))}")
        print(f"[OK] Output:     {result.output_path}")
    return 0


def run_batch(args: argparse.Namespace) -> int:
    progress = _progress(args)

    try:
        cfg = load_config()
        if args.project and not args.quiet:
            print(f"[*] Resolving issues for project {args.project.upper()}…")
        keys = resolve_keys(cfg, project=args.project, keys=args.keys, limit=args.limit)
    except AppError as exc:
        print(f"[ERROR] {exc.message}", file=sys.stderr)
        return 1

    if not keys:
        print("[!] No issues found for the given target.")
        return 0

    if not args.quiet:
        print(f"[*] {len(keys)} issue(s) to process: {', '.join(keys)}")

    def on_key(key: str, index: int, total: int) -> None:
        if not args.quiet:
            print(f"\n[{index}/{total}] {key}")

    try:
        batch = generate_batch(
            keys,
            instructions=args.instructions,
            config=cfg,
            on_stage=progress,
            on_key=on_key,
        )
    except KeyboardInterrupt:
        print("\n[ERROR] Cancelled.", file=sys.stderr)
        return 130

    print()
    print("=" * 68)
    print(f"BATCH SUMMARY — {len(batch.succeeded)} ok, {len(batch.failed)} failed")
    print("=" * 68)
    for outcome in batch.outcomes:
        if outcome.ok:
            print(f"  [OK]   {outcome.key:<12} {outcome.case_count} cases  {outcome.output_path}")
        else:
            print(f"  [FAIL] {outcome.key:<12} {outcome.error}")
    print("=" * 68)

    return 0 if batch.all_ok else 1


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.project or args.keys:
        return run_batch(args)

    if not args.jira_key:
        print(
            "[ERROR] Provide an issue key, --keys, or --project. "
            "Run with --help for usage.",
            file=sys.stderr,
        )
        return 2

    return run_single(args)


if __name__ == "__main__":
    raise SystemExit(main())
