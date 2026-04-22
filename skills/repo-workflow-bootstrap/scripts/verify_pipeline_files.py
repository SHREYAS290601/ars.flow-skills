#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_RELATIVE_PATHS = [
    "README.md",
    ".github/workflows/ci.yml",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify required workflow files exist.")
    parser.add_argument("--repo", required=True, help="Path to repository root")
    args = parser.parse_args()

    repo_root = Path(args.repo)
    missing = [path for path in REQUIRED_RELATIVE_PATHS if not (repo_root / path).exists()]

    if missing:
        for path in missing:
            print(f"FAIL: missing required file {path}")
        return 1

    print("PASS: required workflow files detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
