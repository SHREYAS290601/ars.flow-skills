#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_MARKERS = [
    "## Baseline Behavior",
    "## Failing Test",
    "## Implementation Plan",
    "## Regression Commands",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate test-first plan completeness.")
    parser.add_argument("--plan", required=True, help="Path to markdown plan")
    args = parser.parse_args()

    plan_text = Path(args.plan).read_text(encoding="utf-8")
    missing = [marker for marker in REQUIRED_MARKERS if marker not in plan_text]

    if missing:
        for marker in missing:
            print(f"FAIL: missing section {marker}")
        return 1

    print("PASS: plan includes required test-first sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
