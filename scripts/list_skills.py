#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skill_catalog.core import load_skill_records


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    records, errors = load_skill_records(repo_root)

    if errors:
        print("Catalog has validation errors; refusing to list skills:")
        for error in errors:
            print(f"- {error}")
        return 1

    grouped: dict[str, list[str]] = defaultdict(list)
    for record in records:
        grouped[record.metadata["categoryLabel"]].append(record.metadata["name"])

    print("Skills by category:\n")
    for category in sorted(grouped):
        print(f"{category}")
        for name in sorted(grouped[category]):
            print(f"  - {name}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
