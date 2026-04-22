---
name: pr-change-risk-review
description: Assess pull-request blast radius and deployment risk with deterministic heuristics and explicit mitigation actions. Use for medium/high-impact changes that touch shared services, data paths, or security-sensitive code.
---

# PR Change Risk Review

## Scope
Generate a defensible risk assessment for pull requests and require explicit mitigation before merge.

## When to Use
- PRs with large diff size or multi-module impact.
- Changes affecting auth, data integrity, or money movement.
- Releases during constrained incident windows.

## When Not to Use
- Trivial typo or docs-only edits.
- Automated dependency bumps already covered by policy.
- Archived repositories with no production usage.

## Required Inputs
- `diff_stats.json`: files changed, churn metrics, and test delta.
- `change_context.md`: business impact and rollout plan.
- `service_criticality`: severity tier for impacted systems.

## Expected Outputs
- `risk_report.md` with score, rationale, and severity.
- `mitigation_checklist.md` tied to the identified risks.

## Workflow
1. Compute baseline risk from churn and file criticality.
2. Increase risk for auth/data/migration-sensitive paths.
3. Evaluate test coverage delta and rollback readiness.
4. Assign severity tier and required controls.
5. Document mitigation steps and approval requirements.
6. Gate merge when controls are missing.

## Validation Strategy
- Run `scripts/score_risk.py` for deterministic baseline scoring.
- Require human override note for manual score adjustments.
- Recompute score when PR scope changes.

## Failure Modes
- Heuristics underweight subtle logic changes in critical code.
- Score inflation causes alert fatigue and low trust.
- Missing context on operational readiness skews severity.

## Examples
- See `examples/example-run.md` for an elevated-risk data-layer PR.
