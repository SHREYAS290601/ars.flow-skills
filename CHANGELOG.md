# Changelog

## 2026-04-22

### Added 8 new production-ready skills

1. `api-contract-diff-checker`
- Why: API contract regressions are high-cost and easily automatable.
- Reliability: deterministic OpenAPI diffing with breaking-change rules.

2. `migration-dry-run-planner`
- Why: migration failures require preflight and rollback discipline.
- Reliability: required dry-run/abort/rollback sections validated by script.

3. `dependency-upgrade-risk-review`
- Why: dependency upgrades are common and often risky.
- Reliability: semver-based risk classification plus explicit test-focus output.

4. `secrets-config-sanity-check`
- Why: config mistakes and unsafe defaults cause production incidents.
- Reliability: deterministic required-key and unsafe-default checks.

5. `readme-doc-drift-detector`
- Why: stale docs degrade developer velocity and trust.
- Reliability: compares documented commands against executable scripts.

6. `incident-timeline-builder`
- Why: chronology is essential for debugging and post-incident learning.
- Reliability: strict timestamp parsing and deterministic event ordering.

7. `missing-tests-pr-reviewer`
- Why: code changes often miss corresponding test updates.
- Reliability: source-to-test mapping heuristics with CI-friendly failures.

8. `agent-regression-pack-generator`
- Why: agent workflow changes need repeatable regression validation.
- Reliability: schema-validated regression pack structure and coverage guidance.

### Platform updates
- Registry expanded from 8 to 16 skills.
- Website registry fixture updated so new skills render immediately.
- Existing architecture preserved (`skills-catalog` source of truth, website consumes generated registry).
