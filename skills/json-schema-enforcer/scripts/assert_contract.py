#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

TYPE_MAP = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list,
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(contract: dict, candidate: dict) -> list[str]:
    errors: list[str] = []

    for key in contract.get("required_fields", []):
        if key not in candidate:
            errors.append(f"missing required field: {key}")

    for key, expected_type in contract.get("field_types", {}).items():
        if key not in candidate:
            continue
        expected = TYPE_MAP.get(expected_type)
        if expected is None:
            errors.append(f"unsupported expected type in contract: {expected_type} for {key}")
            continue
        if not isinstance(candidate[key], expected):
            errors.append(f"invalid type for {key}: expected {expected_type}")

    for key, allowed_values in contract.get("allowed_values", {}).items():
        if key not in candidate:
            continue
        if candidate[key] not in allowed_values:
            errors.append(f"invalid value for {key}: {candidate[key]!r} not in {allowed_values}")

    for key in contract.get("forbidden_fields", []):
        if key in candidate:
            errors.append(f"forbidden field present: {key}")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate JSON payload against a contract definition.")
    parser.add_argument("--contract", required=True, help="Path to contract JSON")
    parser.add_argument("--candidate", required=True, help="Path to candidate JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    contract = load_json(Path(args.contract))
    candidate = load_json(Path(args.candidate))

    errors = validate(contract, candidate)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: candidate satisfies contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
