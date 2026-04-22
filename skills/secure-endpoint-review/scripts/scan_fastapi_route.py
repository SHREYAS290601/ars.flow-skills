#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Perform lightweight static checks for FastAPI routes.")
    parser.add_argument("--file", required=True, help="Path to route file")
    args = parser.parse_args()

    source = Path(args.file).read_text(encoding="utf-8")
    errors: list[str] = []

    if "Depends(get_current_user)" not in source and "@require_auth" not in source:
        errors.append("route file appears to miss authentication dependency")

    if "except Exception as" in source and "HTTPException" not in source:
        errors.append("broad exception handling without controlled HTTP error mapping")

    if "request.json()" in source and "pydantic" not in source and "BaseModel" not in source:
        errors.append("request body read detected without explicit model validation")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: no obvious secure-default violations found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
