#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare ETL source and target summary JSON.")
    parser.add_argument("--source", required=True, help="Path to source summary")
    parser.add_argument("--target", required=True, help="Path to target summary")
    args = parser.parse_args()

    source = load(Path(args.source))
    target = load(Path(args.target))

    errors: list[str] = []
    if source.get("row_count") != target.get("row_count"):
        errors.append(f"row_count mismatch: {source.get('row_count')} != {target.get('row_count')}")

    if source.get("duplicate_rows") != target.get("duplicate_rows"):
        errors.append(
            f"duplicate_rows mismatch: {source.get('duplicate_rows')} != {target.get('duplicate_rows')}"
        )

    source_checksums = source.get("checksums", {})
    target_checksums = target.get("checksums", {})
    for key in sorted(set(source_checksums) | set(target_checksums)):
        if source_checksums.get(key) != target_checksums.get(key):
            errors.append(
                f"checksum mismatch for {key}: {source_checksums.get(key)!r} != {target_checksums.get(key)!r}"
            )

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: source and target summaries reconcile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
