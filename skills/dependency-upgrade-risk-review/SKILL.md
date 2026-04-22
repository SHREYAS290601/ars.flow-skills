---
name: dependency-upgrade-risk-review
description: Assess dependency upgrade diffs and produce test-focus and breakage-risk recommendations before merge.
---

# Dependency Upgrade Risk Review

## Scope
Analyze dependency version changes and classify upgrade risk with actionable regression test focus areas.

## When to Use
- PR updates package/lock files.
- Batch upgrade efforts before release.
- Framework/runtime major version migrations.

## When Not to Use
- Dependency metadata formatting-only changes.
- Repositories without executable test harness.

## Required Inputs
- `before_dependencies` and `after_dependencies` manifests.
- optional changelog snippets and known breaking notes.

## Expected Outputs
- `upgrade_risk_report.md` with severity and rationale.
- `test_focus_plan.md` listing high-priority suites.
- `upgrade_gate_decision.md` (`safe`, `safe-with-guardrails`, `block`).

## Workflow
1. Parse dependency diff.
2. Detect major/minor/patch deltas.
3. Weight risk for core/runtime/framework packages.
4. Generate targeted regression plan.
5. Emit recommendation with mitigations.

## Validation Strategy
- Run `scripts/dependency_diff_risk.py` to classify version deltas.
- Require explicit notes for high-risk major upgrades.
- Verify recommended test suites executed before merge.

## Failure Modes
- Semver underestimates real breakage risk.
- Lockfile-only changes hide transitive upgrades.
- Changelog gaps reduce confidence.

## Examples
- `examples/example-run.md` demonstrates a major upgrade risk classification.

## Sub-Documentation
- `references/risk-matrix.md`: risk scoring rubric.
- `references/test-focus-template.md`: template for upgrade regression plans.
