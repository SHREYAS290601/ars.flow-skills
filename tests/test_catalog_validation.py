from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skill_catalog.core import build_registry, validate_catalog


class CatalogValidationTests(unittest.TestCase):
    def test_real_catalog_validates(self) -> None:
        catalog_root = Path(__file__).resolve().parents[1]
        errors = validate_catalog(catalog_root)
        self.assertEqual(errors, [])

    def test_registry_generation_contains_expected_skill_count(self) -> None:
        catalog_root = Path(__file__).resolve().parents[1]
        registry = build_registry(catalog_root, base_url="http://localhost:3000", generated_at="2026-04-22T00:00:00Z")

        self.assertEqual(registry["generatedAt"], "2026-04-22T00:00:00Z")
        self.assertEqual(len(registry["skills"]), 8)

        sample = registry["skills"][0]
        self.assertTrue(sample["sourceUrl"].startswith("http://localhost:3000/skills/"))
        self.assertTrue(sample["docsUrl"].startswith("http://localhost:3000/skills/"))
        self.assertTrue(sample["downloadUrl"].startswith("http://localhost:3000/api/download/"))

    def test_invalid_skill_missing_required_sections_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill_dir = root / "skills" / "bad-skill"
            examples_dir = skill_dir / "examples"
            examples_dir.mkdir(parents=True)

            (skill_dir / "SKILL.md").write_text(
                """---
name: bad-skill
description: minimal
---

# Bad Skill

## Scope
Incomplete skill body.
""",
                encoding="utf-8",
            )

            metadata = {
                "id": "skill-bad-skill",
                "slug": "bad-skill",
                "name": "Bad Skill",
                "shortDescription": "bad",
                "longDescription": "bad",
                "category": "structured-output",
                "categoryLabel": "Structured Output & Schema Enforcement",
                "tags": ["bad"],
                "languages": ["Python"],
                "frameworks": ["None"],
                "reliabilityLevel": "low",
                "verificationTypes": ["manual review required"],
                "riskLevel": "low",
                "version": "0.1.0",
                "author": "Test",
                "inputs": [],
                "outputs": [],
                "includedAssets": [],
                "idealUseCases": ["test"],
                "failureModes": ["test"],
                "examples": [
                    {
                        "title": "x",
                        "summary": "x",
                        "inputPreview": "x",
                        "outputPreview": "x",
                        "validated": True,
                    }
                ],
                "changelog": [
                    {
                        "version": "0.1.0",
                        "date": "2026-04-22T00:00:00.000Z",
                        "summary": "x",
                    }
                ],
                "downloads": 0,
                "updatedAt": "2026-04-22T00:00:00.000Z",
            }
            (skill_dir / "skill.json").write_text(json.dumps(metadata), encoding="utf-8")
            (examples_dir / "example.md").write_text("example", encoding="utf-8")

            errors = validate_catalog(root)
            self.assertTrue(any("missing required section heading" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
