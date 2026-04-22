#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

COMMAND_RE = re.compile(r"npm run ([a-zA-Z0-9:-]+)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check README command drift against package scripts.")
    parser.add_argument("--readme", required=True)
    parser.add_argument("--package", required=True)
    args = parser.parse_args()

    readme_text = Path(args.readme).read_text(encoding="utf-8")
    documented = set(COMMAND_RE.findall(readme_text))

    package_data = json.loads(Path(args.package).read_text(encoding="utf-8"))
    scripts = set(package_data.get("scripts", {}).keys())

    missing = sorted(documented - scripts)
    undocumented = sorted(scripts - documented)

    for cmd in missing:
        print(f"FAIL: documented command missing from scripts: {cmd}")

    for cmd in undocumented:
        print(f"WARN: script not documented in README: {cmd}")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
