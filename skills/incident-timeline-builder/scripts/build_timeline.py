#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic chronological timeline from event records.")
    parser.add_argument("--events", required=True)
    args = parser.parse_args()

    events = json.loads(Path(args.events).read_text(encoding="utf-8"))
    if not isinstance(events, list):
        print("FAIL: events input must be a list")
        return 1

    try:
        sorted_events = sorted(events, key=lambda e: parse_ts(e["timestamp"]))
    except Exception as error:  # noqa: BLE001
        print(f"FAIL: unable to parse/sort timestamps: {error}")
        return 1

    for event in sorted_events:
        print(f"{event.get('timestamp')} | {event.get('source', 'unknown')} | {event.get('event')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
