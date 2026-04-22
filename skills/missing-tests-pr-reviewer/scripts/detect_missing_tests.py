#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def expected_test(path: str) -> str:
    if path.startswith("src/") and path.endswith(".ts"):
        return path.replace("src/", "tests/").replace(".ts", ".test.ts")
    if path.startswith("app/") and path.endswith(".py"):
        return "tests/test_" + Path(path).stem + ".py"
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect likely missing tests for changed source files.")
    parser.add_argument("--changed", required=True)
    parser.add_argument("--tests", required=True)
    args = parser.parse_args()

    changed = [line.strip() for line in Path(args.changed).read_text(encoding="utf-8").splitlines() if line.strip()]
    tests = {line.strip() for line in Path(args.tests).read_text(encoding="utf-8").splitlines() if line.strip()}

    missing: list[str] = []
    for path in changed:
        expected = expected_test(path)
        if not expected:
            continue
        if expected not in tests:
            missing.append(f"{path} -> expected {expected}")

    if missing:
        for item in missing:
            print(f"FAIL: missing test mapping {item}")
        return 1

    print("PASS: no obvious missing test mappings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
