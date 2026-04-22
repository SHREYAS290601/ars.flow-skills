#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Preconditions",
    "## Dry-Run Steps",
    "## Success Criteria",
    "## Abort Criteria",
    "## Rollback Plan",
    "## Validation Checks",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate migration dry-run plan sections.")
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()

    content = Path(args.plan).read_text(encoding="utf-8")
    missing = [section for section in REQUIRED_SECTIONS if section not in content]
    if missing:
        for section in missing:
            print(f"FAIL: missing section {section}")
        return 1

    print("PASS: dry-run plan contains required sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
