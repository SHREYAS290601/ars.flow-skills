---
name: pr-change-risk-review
description: Assess pull-request blast radius and deployment risk with deterministic heuristics and explicit mitigation actions. Use for medium/high-impact changes that touch shared services, data paths, or security-sensitive code.
---

# PR Change Risk Review

## Scope
Generate a defendable risk assessment for pull requests and map each risk signal to required mitigation actions before merge.

## When to Use
- Medium/large PRs with broad blast radius.
- PRs touching security, auth, data, migrations, or critical paths.
- Releases during constrained operational windows.

## When Not to Use
- Tiny docs/typo-only updates.
- Auto-generated lockfile-only bumps with known policy handling.
- Repos not shipping to active production environments.

## Required Inputs
- `diff_stats.json`: files changed, churn, and sensitive path flags.
- `change_context.md`: business scope and deployment plan.
- `test_evidence.md`: targeted and regression coverage summary.
- `service_criticality`: system criticality tier.

## Expected Outputs
- `risk_report.md` with score breakdown and severity.
- `mitigation_checklist.md` with owner + due state.
- `deployment_recommendation.md` (`standard`, `staged`, `freeze-required`).

## Workflow
1. Compute deterministic baseline score.
- Use churn, file count, and sensitive-path indicators.
2. Adjust with context multipliers.
- Apply service criticality and rollout risk factors.
3. Evaluate verification coverage.
- Penalize missing tests in changed high-risk areas.
4. Assign severity tier.
- low / medium / high with explicit criteria.
5. Map mitigations.
- staged rollout
- rollback owner assignment
- additional approvers
- incident-readiness checks
6. Gate merge/deploy.
- Block if required mitigations are incomplete.

## Validation Strategy
- Use `scripts/score_risk.py` for baseline score reproducibility.
- Require written justification for manual score overrides.
- Recalculate score after scope changes.
- Keep score history for calibration reviews.

## Failure Modes
- Heuristic model misses nuanced domain risk.
- Teams normalize frequent high scores and ignore alerts.
- Incomplete context data leads to false confidence.
- Mitigations are listed but not enforced.

## Examples
- `examples/example-run.md`: high-risk PR with mitigation plan.
- `examples/diff_stats.json`: sample risk scoring input.

## Severity Guidance
- `high`: merge/deploy blocked until mitigation complete.
- `medium`: merge allowed with explicit mitigation owner.
- `low`: standard merge process.

## Sub-Documentation
- `references/scoring-rubric.md`: baseline scoring factors.
- `references/mitigation-catalog.md`: mitigation actions by risk class.
- `references/manual-override-policy.md`: controls for score overrides.
