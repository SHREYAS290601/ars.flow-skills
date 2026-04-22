#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate agent regression pack schema.")
    parser.add_argument("--pack", required=True)
    args = parser.parse_args()

    cases = json.loads(Path(args.pack).read_text(encoding="utf-8"))
    if not isinstance(cases, list) or not cases:
        print("FAIL: regression pack must be a non-empty list")
        return 1

    errors: list[str] = []
    for idx, case in enumerate(cases):
        if not isinstance(case, dict):
            errors.append(f"case[{idx}] must be an object")
            continue
        for field in ("id", "input", "expected"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"case[{idx}] missing/invalid field: {field}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: regression pack schema validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
