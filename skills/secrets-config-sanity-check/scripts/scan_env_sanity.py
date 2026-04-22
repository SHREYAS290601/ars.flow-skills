#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

UNSAFE_VALUES = {"changeme", "example", "test", ""}


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate required env keys and unsafe defaults.")
    parser.add_argument("--required", required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    required = parse_env(Path(args.required))
    target = parse_env(Path(args.target))

    errors: list[str] = []

    for key in required:
        if key not in target:
            errors.append(f"missing required key: {key}")

    for key, value in target.items():
        lower = value.lower()
        if key == "DEBUG" and lower == "true":
            errors.append("unsafe default: DEBUG=true")
        if "SECRET" in key and lower in UNSAFE_VALUES:
            errors.append(f"unsafe secret default for {key}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: config sanity checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
