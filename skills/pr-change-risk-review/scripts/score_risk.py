#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Score PR risk using deterministic heuristics.")
    parser.add_argument("--stats", required=True, help="Path to diff stats JSON")
    args = parser.parse_args()

    stats = json.loads(Path(args.stats).read_text(encoding="utf-8"))

    score = 0
    files_changed = int(stats.get("files_changed", 0))
    lines_added = int(stats.get("lines_added", 0))
    lines_deleted = int(stats.get("lines_deleted", 0))

    if files_changed >= 25:
        score += 3
    elif files_changed >= 10:
        score += 2
    elif files_changed >= 3:
        score += 1

    churn = lines_added + lines_deleted
    if churn >= 1500:
        score += 3
    elif churn >= 600:
        score += 2
    elif churn >= 200:
        score += 1

    if stats.get("touches_security_paths"):
        score += 2
    if stats.get("touches_migration_paths"):
        score += 2

    tests = int(stats.get("new_tests_added", 0))
    if tests == 0:
        score += 2
    elif tests <= 2:
        score += 1

    score = min(score, 10)
    severity = "high" if score >= 8 else "medium" if score >= 4 else "low"

    print(json.dumps({"score": score, "severity": severity}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
