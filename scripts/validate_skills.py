#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skill_catalog.core import validate_catalog


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    errors = validate_catalog(repo_root)

    if errors:
        print("Skill validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("All skills passed validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
