#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def parse_version(raw: str) -> tuple[int, int, int] | None:
    match = VERSION_RE.search(raw)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def classify(before: tuple[int, int, int], after: tuple[int, int, int]) -> str:
    if after[0] != before[0]:
        return "high"
    if after[1] != before[1]:
        return "medium"
    if after[2] != before[2]:
        return "low"
    return "none"


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify dependency upgrade risk from version diffs.")
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    args = parser.parse_args()

    before = json.loads(Path(args.before).read_text(encoding="utf-8")).get("dependencies", {})
    after = json.loads(Path(args.after).read_text(encoding="utf-8")).get("dependencies", {})

    max_risk = "none"
    ordering = {"none": 0, "low": 1, "medium": 2, "high": 3}

    for dep, new_value in after.items():
        old_value = before.get(dep)
        if not isinstance(old_value, str) or not isinstance(new_value, str):
            continue

        old_v = parse_version(old_value)
        new_v = parse_version(new_value)
        if not old_v or not new_v:
            continue

        risk = classify(old_v, new_v)
        if ordering[risk] > ordering[max_risk]:
            max_risk = risk
        if risk != "none":
            print(f"{dep}: {old_value} -> {new_value} ({risk})")

    print(f"overall_risk={max_risk}")
    return 0 if max_risk in {"none", "low", "medium"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
