#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def get_required_fields(doc: dict, path: str, method: str) -> set[str]:
    try:
        schema = doc["paths"][path][method]["requestBody"]["content"]["application/json"]["schema"]
    except KeyError:
        return set()
    required = schema.get("required", [])
    return {field for field in required if isinstance(field, str)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two OpenAPI specs for deterministic breaking changes.")
    parser.add_argument("--old", required=True)
    parser.add_argument("--new", required=True)
    args = parser.parse_args()

    old = load_json(Path(args.old))
    new = load_json(Path(args.new))

    old_paths = old.get("paths", {})
    new_paths = new.get("paths", {})

    errors: list[str] = []

    for path, old_methods in old_paths.items():
        if path not in new_paths:
            errors.append(f"removed path: {path}")
            continue

        for method in old_methods:
            if method not in new_paths[path]:
                errors.append(f"removed method: {method.upper()} {path}")
                continue

            old_required = get_required_fields(old, path, method)
            new_required = get_required_fields(new, path, method)
            added_required = sorted(new_required - old_required)
            if added_required:
                errors.append(
                    f"added required request fields for {method.upper()} {path}: {', '.join(added_required)}"
                )

    if errors:
        for error in errors:
            print(f"BREAKING: {error}")
        return 1

    print("PASS: no deterministic breaking changes detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
