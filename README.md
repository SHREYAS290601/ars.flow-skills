# Skills Catalog

`skills-catalog/` is the source-of-truth repository for ARS.FLOW skills.

It owns:
- skill authoring (`skills/<slug>/`)
- validation rules
- registry generation (`registry/skills.json`)

It does not own website UI concerns.

## Layout

```text
skills-catalog/
  skills/
    <slug>/
      SKILL.md
      skill.json
      examples/
      scripts/      # optional
      references/   # optional
  scripts/
    validate_skills.py
    generate_registry.py
    list_skills.py
  registry/
    skills.json     # generated
  tests/
```

## Commands

From `skills-catalog/`:

```bash
python3 scripts/validate_skills.py
python3 scripts/generate_registry.py
python3 scripts/generate_registry.py --sync-website ../website/public/registry/skills.json
python3 scripts/list_skills.py
python3 -m unittest discover -s tests
```

## Skill quality bar

Every skill must be narrow, reusable, and verification-first. Each skill must include:
- explicit use and non-use cases
- required inputs and expected outputs
- deterministic validation strategy
- documented failure modes
- examples

## Adding a new skill

1. Create `skills/<slug>/`.
2. Add `SKILL.md` with YAML frontmatter (`name`, `description`) and required sections.
3. Add `skill.json` matching catalog metadata schema.
4. Add at least one file in `examples/`.
5. Run validation and tests.
6. Regenerate `registry/skills.json`.

## Notes on URLs

The registry generator sets `sourceUrl`, `docsUrl`, and `downloadUrl` from a configurable base URL.
Default base URL is `http://localhost:3000` for local testing.
