---
name: etl-reconciliation-check
description: Reconcile ETL outputs against source expectations using deterministic row-count and checksum checks. Use for batch pipelines, migration cutovers, and data-quality gates where silent drift is unacceptable.
---

# ETL Reconciliation Check

## Scope
Validate that transformed datasets match expected volume and key integrity constraints before downstream publication.

## When to Use
- Batch ETL jobs moving data across systems.
- Schema migrations where row integrity must be preserved.
- Data handoffs feeding analytics or billing workflows.

## When Not to Use
- Exploratory analysis without repeatable datasets.
- Real-time streams where this batch-oriented method does not apply.
- Pipelines lacking stable business keys for reconciliation.

## Required Inputs
- `source_summary.json`: source counts/checksums.
- `target_summary.json`: target counts/checksums.
- `tolerance_policy`: allowed numeric drift thresholds.

## Expected Outputs
- `reconciliation_report.md` with pass/fail status.
- `blocked_keys.csv` for mismatched entities.

## Workflow
1. Extract source and target summary metrics.
2. Compare row counts and duplicate counts.
3. Compare checksum or hash aggregates for key columns.
4. Flag discrepancies above tolerance.
5. Produce deterministic reconciliation report.
6. Block publish if severity threshold is exceeded.

## Validation Strategy
- Run `scripts/reconcile_summaries.py` for deterministic summary comparisons.
- Attach reconciliation output to deployment review.
- Require sign-off for tolerated mismatches.

## Failure Modes
- Source summary is stale and mismatches current extraction window.
- Hash/checksum fields do not cover critical business columns.
- Accepted drift accumulates and hides gradual corruption.

## Examples
- See `examples/example-run.md` for a mismatch detection and remediation flow.
