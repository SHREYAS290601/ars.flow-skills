---
name: etl-reconciliation-check
description: Reconcile ETL outputs against source expectations using deterministic row-count and checksum checks. Use for batch pipelines, migration cutovers, and data-quality gates where silent drift is unacceptable.
---

# ETL Reconciliation Check

## Scope
Verify that ETL outputs preserve required data integrity guarantees before downstream publication by applying deterministic, reproducible reconciliation checks.

## When to Use
- Batch ETL pipelines across storage systems.
- Data migrations and cutovers.
- Financial, billing, or analytics datasets requiring strict trust.
- Any pipeline where silent drift is operationally expensive.

## When Not to Use
- Exploratory ad-hoc analysis.
- Near-real-time streams where this batch summary method is insufficient.
- Sources lacking stable keys or comparable windows.

## Required Inputs
- `source_summary.json`:
  - row counts
  - duplicate counts
  - checksum aggregates
- `target_summary.json`: same fields over target output.
- `tolerance_policy`:
  - allowed count delta
  - allowed duplicate delta
  - critical checksum fields
- `window_definition` (recommended): exact extraction/load window.

## Expected Outputs
- `reconciliation_report.md` with pass/fail and reason codes.
- `mismatch_summary.csv` for key discrepancies.
- `release_gate_decision.md` (`proceed`, `block`, or `manual-override`).

## Workflow
1. Verify window parity.
- Ensure source and target summaries cover identical time/key window.
2. Validate structural comparability.
- Ensure table/entity names match.
- Ensure critical checksum fields exist on both sides.
3. Compare counts.
- row count delta
- duplicate count delta
- null-rate or optional completeness metrics when available
4. Compare checksums/hashes.
- Validate critical columns first.
- Classify mismatch severity by business impact.
5. Generate deterministic report.
- Include exact metrics and thresholds.
- Label each check as `pass`, `warn`, or `fail`.
6. Make gate decision.
- Fail on critical mismatches.
- Allow only documented override paths for non-critical deltas.

## Validation Strategy
- Use `scripts/reconcile_summaries.py` for deterministic comparison.
- Treat checksum mismatch on critical fields as blocking.
- Store mismatch signatures for trend analysis.
- Require explicit owner approval for override decisions.

## Failure Modes
- Source and target windows are offset, producing false alarms.
- Summaries omit high-impact fields.
- Tolerance settings are too permissive.
- Reconciliation is run after publish, making rollback costly.

## Examples
- `examples/example-run.md`: reconciliation failure and decision path.
- `examples/source_summary.json`, `examples/target_summary.json`: sample mismatch fixtures.

## Decision Model
- `block`: any critical checksum mismatch or severe count divergence.
- `manual-override`: non-critical mismatch with explicit risk acceptance.
- `proceed`: all checks pass within policy.

## Sub-Documentation
- `references/reconciliation-policy.md`: baseline thresholds and rules.
- `references/window-alignment-guide.md`: avoiding false mismatches from window skew.
- `references/mismatch-triage-playbook.md`: root-cause classification and remediation steps.
