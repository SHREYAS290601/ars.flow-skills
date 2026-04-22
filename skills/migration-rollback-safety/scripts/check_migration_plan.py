#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Preconditions",
    "## Preflight Checks",
    "## Rollout Steps",
    "## Rollback Steps",
    "## Abort Criteria",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate migration plan includes required safety sections.")
    parser.add_argument("--plan", required=True, help="Path to migration plan markdown")
    args = parser.parse_args()

    content = Path(args.plan).read_text(encoding="utf-8")
    missing = [section for section in REQUIRED_SECTIONS if section not in content]

    if missing:
        for section in missing:
            print(f"FAIL: missing {section}")
        return 1

    print("PASS: migration plan includes required safety sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
