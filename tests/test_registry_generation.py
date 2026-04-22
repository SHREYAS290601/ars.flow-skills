from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skill_catalog.core import build_registry, write_registry


class RegistryGenerationTests(unittest.TestCase):
    def test_write_registry_creates_json_file(self) -> None:
        catalog_root = Path(__file__).resolve().parents[1]
        registry = build_registry(
            catalog_root,
            website_base_url="http://localhost:3000",
            generated_at="2026-04-22T00:00:00Z",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "registry" / "skills.json"
            write_registry(registry, output)

            self.assertTrue(output.exists())
            parsed = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(parsed["generatedAt"], "2026-04-22T00:00:00Z")
            self.assertGreaterEqual(len(parsed["skills"]), 16)


if __name__ == "__main__":
    unittest.main()
