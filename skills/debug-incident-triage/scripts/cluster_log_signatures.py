#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

NORMALIZE_NUMBER = re.compile(r"\b\d+\b")


def normalize(line: str) -> str:
    line = line.strip().lower()
    # Drop leading timestamp token when present to cluster repeated messages.
    parts = line.split(maxsplit=2)
    if len(parts) == 3 and parts[0].endswith("z"):
        line = f"{parts[1]} {parts[2]}"
    line = NORMALIZE_NUMBER.sub("<num>", line)
    return line


def main() -> int:
    parser = argparse.ArgumentParser(description="Cluster log lines by normalized signature.")
    parser.add_argument("--logs", required=True, help="Path to log file")
    args = parser.parse_args()

    lines = [line for line in Path(args.logs).read_text(encoding="utf-8").splitlines() if line.strip()]
    counter = Counter(normalize(line) for line in lines)

    for signature, count in counter.most_common():
        print(f"{count:4d} | {signature}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
