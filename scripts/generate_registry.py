#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skill_catalog.core import build_registry, write_registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate skills registry JSON from source skills.")
    parser.add_argument(
        "--base-url",
        default="http://localhost:3000",
        help="Base URL used to generate source/docs/download links",
    )
    parser.add_argument(
        "--output",
        default="registry/skills.json",
        help="Output path relative to skills-catalog root",
    )
    parser.add_argument(
        "--sync-website",
        default=None,
        help="Optional path to copy generated registry into website fixture",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    output_path = (repo_root / args.output).resolve()

    try:
        registry = build_registry(repo_root, base_url=args.base_url)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1

    write_registry(registry, output_path)
    print(f"Generated registry: {output_path}")

    if args.sync_website:
        sync_target = Path(args.sync_website).resolve()
        sync_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output_path, sync_target)
        print(f"Synced registry to website: {sync_target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
