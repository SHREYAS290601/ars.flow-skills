from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_SKILL_SECTIONS = [
    "Scope",
    "When to Use",
    "When Not to Use",
    "Required Inputs",
    "Expected Outputs",
    "Workflow",
    "Validation Strategy",
    "Failure Modes",
    "Examples",
]

VALID_RELIABILITY_LEVELS = {"high", "medium", "low"}
VALID_RISK_LEVELS = {"high", "medium", "low"}
VALID_CATEGORIES = {
    "structured-output",
    "test-first",
    "security-review",
    "repo-workflows",
    "etl-validation",
    "pr-risk",
    "debug-triage",
    "migrations",
}


@dataclass(frozen=True)
class SkillRecord:
    slug: str
    path: Path
    frontmatter_name: str
    frontmatter_description: str
    metadata: dict[str, Any]


def _parse_frontmatter(markdown: str) -> tuple[dict[str, str], str]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter delimited by '---'")

    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break

    if end_index is None:
        raise ValueError("SKILL.md frontmatter is missing closing '---'")

    frontmatter_lines = lines[1:end_index]
    body = "\n".join(lines[end_index + 1 :]).strip()

    data: dict[str, str] = {}
    for raw_line in frontmatter_lines:
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    allowed_keys = {"name", "description"}
    unexpected = sorted(set(data) - allowed_keys)
    if unexpected:
        raise ValueError(f"Unexpected frontmatter fields: {', '.join(unexpected)}")

    missing = sorted(allowed_keys - set(data))
    if missing:
        raise ValueError(f"Missing frontmatter fields: {', '.join(missing)}")

    return data, body


def _parse_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error


def _validate_iso_datetime(value: str, field_name: str) -> str | None:
    if not isinstance(value, str):
        return f"{field_name} must be an ISO datetime string"

    normalized = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(normalized)
    except ValueError:
        return f"{field_name} must be a valid ISO datetime"

    return None


def _require_string(metadata: dict[str, Any], key: str, errors: list[str]) -> None:
    value = metadata.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{key} must be a non-empty string")


def _require_string_list(metadata: dict[str, Any], key: str, errors: list[str], min_items: int = 0) -> None:
    value = metadata.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be a list of strings")
        return

    if len(value) < min_items:
        errors.append(f"{key} must have at least {min_items} item(s)")
        return

    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{key}[{index}] must be a non-empty string")


def _require_field_list(metadata: dict[str, Any], key: str, errors: list[str]) -> None:
    value = metadata.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be a list")
        return

    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
            continue

        for field_name in ("name", "type", "description"):
            field_value = item.get(field_name)
            if not isinstance(field_value, str) or not field_value.strip():
                errors.append(f"{key}[{index}].{field_name} must be a non-empty string")

        required = item.get("required")
        if not isinstance(required, bool):
            errors.append(f"{key}[{index}].required must be a boolean")


def _require_asset_list(metadata: dict[str, Any], key: str, errors: list[str]) -> None:
    value = metadata.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be a list")
        return

    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
            continue
        for field_name in ("type", "name", "description"):
            field_value = item.get(field_name)
            if not isinstance(field_value, str) or not field_value.strip():
                errors.append(f"{key}[{index}].{field_name} must be a non-empty string")


def _require_examples_list(metadata: dict[str, Any], key: str, errors: list[str]) -> None:
    value = metadata.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"{key} must be a non-empty list")
        return

    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
            continue
        for field_name in ("title", "summary", "inputPreview", "outputPreview"):
            field_value = item.get(field_name)
            if not isinstance(field_value, str) or not field_value.strip():
                errors.append(f"{key}[{index}].{field_name} must be a non-empty string")
        if not isinstance(item.get("validated"), bool):
            errors.append(f"{key}[{index}].validated must be a boolean")


def _require_changelog(metadata: dict[str, Any], key: str, errors: list[str]) -> None:
    value = metadata.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be a list")
        return

    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{key}[{index}] must be an object")
            continue
        if not isinstance(item.get("version"), str) or not item["version"].strip():
            errors.append(f"{key}[{index}].version must be a non-empty string")
        if not isinstance(item.get("summary"), str) or not item["summary"].strip():
            errors.append(f"{key}[{index}].summary must be a non-empty string")
        date_error = _validate_iso_datetime(item.get("date"), f"{key}[{index}].date")
        if date_error:
            errors.append(date_error)


def _extract_headings(markdown_body: str) -> set[str]:
    headings: set[str] = set()
    for line in markdown_body.splitlines():
        match = re.match(r"^#{1,6}\s+(.*\S)\s*$", line.strip())
        if match:
            headings.add(match.group(1).strip().lower())
    return headings


def _validate_metadata(metadata: dict[str, Any], folder_slug: str) -> list[str]:
    errors: list[str] = []

    for key in (
        "id",
        "slug",
        "name",
        "shortDescription",
        "longDescription",
        "category",
        "categoryLabel",
        "version",
        "author",
    ):
        _require_string(metadata, key, errors)

    slug = metadata.get("slug")
    if isinstance(slug, str) and slug != folder_slug:
        errors.append(f"slug must match folder name '{folder_slug}'")

    category = metadata.get("category")
    if isinstance(category, str) and category not in VALID_CATEGORIES:
        errors.append(f"category must be one of {sorted(VALID_CATEGORIES)}")

    reliability = metadata.get("reliabilityLevel")
    if reliability not in VALID_RELIABILITY_LEVELS:
        errors.append(f"reliabilityLevel must be one of {sorted(VALID_RELIABILITY_LEVELS)}")

    risk_level = metadata.get("riskLevel")
    if risk_level not in VALID_RISK_LEVELS:
        errors.append(f"riskLevel must be one of {sorted(VALID_RISK_LEVELS)}")

    _require_string_list(metadata, "tags", errors)
    _require_string_list(metadata, "languages", errors)
    _require_string_list(metadata, "frameworks", errors)
    _require_string_list(metadata, "verificationTypes", errors, min_items=1)
    _require_string_list(metadata, "idealUseCases", errors, min_items=1)
    _require_string_list(metadata, "failureModes", errors, min_items=1)
    _require_field_list(metadata, "inputs", errors)
    _require_field_list(metadata, "outputs", errors)
    _require_asset_list(metadata, "includedAssets", errors)
    _require_examples_list(metadata, "examples", errors)
    _require_changelog(metadata, "changelog", errors)

    downloads = metadata.get("downloads")
    if not isinstance(downloads, int) or downloads < 0:
        errors.append("downloads must be a non-negative integer")

    updated_at_error = _validate_iso_datetime(metadata.get("updatedAt"), "updatedAt")
    if updated_at_error:
        errors.append(updated_at_error)

    return errors


def _validate_skill_folder(skill_dir: Path) -> tuple[list[str], SkillRecord | None]:
    errors: list[str] = []
    slug = skill_dir.name

    if not re.fullmatch(r"[a-z0-9-]{1,64}", slug):
        errors.append("folder name must match [a-z0-9-]{1,64}")

    skill_md_path = skill_dir / "SKILL.md"
    metadata_path = skill_dir / "skill.json"
    examples_dir = skill_dir / "examples"

    if not skill_md_path.is_file():
        errors.append("missing SKILL.md")

    if not metadata_path.is_file():
        errors.append("missing skill.json")

    if not examples_dir.is_dir():
        errors.append("missing examples/ directory")
    else:
        example_files = [path for path in examples_dir.iterdir() if path.is_file()]
        if not example_files:
            errors.append("examples/ must contain at least one file")

    if errors:
        return errors, None

    markdown = skill_md_path.read_text(encoding="utf-8")
    try:
        frontmatter, body = _parse_frontmatter(markdown)
    except ValueError as error:
        errors.append(str(error))
        return errors, None

    front_name = frontmatter["name"].strip()
    if front_name != slug:
        errors.append("frontmatter name must match folder slug")

    front_description = frontmatter["description"].strip()
    if not front_description:
        errors.append("frontmatter description must be non-empty")

    headings = _extract_headings(body)
    for section in REQUIRED_SKILL_SECTIONS:
        if section.lower() not in headings:
            errors.append(f"missing required section heading: ## {section}")

    try:
        metadata = _parse_json(metadata_path)
    except ValueError as error:
        errors.append(str(error))
        return errors, None
    errors.extend(_validate_metadata(metadata, slug))

    if errors:
        return errors, None

    return (
        [],
        SkillRecord(
            slug=slug,
            path=skill_dir,
            frontmatter_name=front_name,
            frontmatter_description=front_description,
            metadata=metadata,
        ),
    )


def load_skill_records(catalog_root: Path) -> tuple[list[SkillRecord], list[str]]:
    skills_root = catalog_root / "skills"
    if not skills_root.is_dir():
        return [], [f"Missing skills directory: {skills_root}"]

    records: list[SkillRecord] = []
    all_errors: list[str] = []

    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        errors, record = _validate_skill_folder(skill_dir)
        all_errors.extend([f"{skill_dir.name}: {error}" for error in errors])
        if record:
            records.append(record)

    return records, all_errors


def validate_catalog(catalog_root: Path) -> list[str]:
    _, errors = load_skill_records(catalog_root)
    return errors


def _build_urls(website_base_url: str, slug: str, repo_url: str | None = None) -> dict[str, str]:
    website_trimmed = website_base_url.rstrip("/")
    if repo_url:
        repo_trimmed = repo_url.rstrip("/")
        return {
            "sourceUrl": f"{repo_trimmed}/tree/main/skills/{slug}",
            "downloadUrl": f"{repo_trimmed}/tree/main/skills/{slug}",
            "docsUrl": f"{repo_trimmed}/blob/main/skills/{slug}/SKILL.md",
        }

    return {
        "sourceUrl": f"{website_trimmed}/skills/{slug}/docs#source",
        "downloadUrl": f"{website_trimmed}/api/download/{slug}",
        "docsUrl": f"{website_trimmed}/skills/{slug}/docs",
    }


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def build_registry(
    catalog_root: Path,
    website_base_url: str,
    generated_at: str | None = None,
    repo_url: str | None = None,
) -> dict[str, Any]:
    records, errors = load_skill_records(catalog_root)
    if errors:
        message = "\n".join(errors)
        raise ValueError(f"Catalog validation failed:\n{message}")

    output_skills: list[dict[str, Any]] = []
    for record in sorted(records, key=lambda item: item.slug):
        metadata = dict(record.metadata)
        metadata.update(_build_urls(website_base_url=website_base_url, slug=record.slug, repo_url=repo_url))
        output_skills.append(metadata)

    return {
        "generatedAt": generated_at or _utc_timestamp(),
        "skills": output_skills,
    }


def write_registry(registry: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
