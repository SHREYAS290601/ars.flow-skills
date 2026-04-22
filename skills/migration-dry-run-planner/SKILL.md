---
name: migration-dry-run-planner
description: Build migration execution plans with mandatory dry-run, rollback, and verification steps before production rollout.
---

# Migration Dry-Run Planner

## Scope
Create a migration plan that can be dry-run safely, validated deterministically, and rolled back within defined constraints.

## When to Use
- Database migrations with operational risk.
- Config migrations that could affect production behavior.
- Release plans requiring preflight and postflight checks.

## When Not to Use
- Trivial local-only migrations.
- One-off scripts with no rollback requirement.
- Environments lacking stable staging parity.

## Required Inputs
- `migration_request.md`: intended schema/config changes.
- `environment_context.md`: target environment and constraints.
- `rollback_constraints.md`: RTO/RPO and non-negotiables.

## Expected Outputs
- `dry_run_plan.md` with commands and success criteria.
- `rollback_plan.md` with trigger thresholds.
- `validation_queries.sql` or equivalent checks.

## Workflow
1. Parse migration objective and impacted assets.
2. Generate preflight checklist.
3. Define dry-run command sequence in staging.
4. Capture expected output checkpoints.
5. Define rollback commands and abort conditions.
6. Define post-run validation checks.
7. Approve only if dry-run evidence passes.

## Validation Strategy
- Run `scripts/validate_dry_run_plan.py` to enforce required plan sections.
- Require each migration phase to have explicit success and rollback criteria.
- Block production rollout when dry-run evidence is missing.

## Failure Modes
- Plan skips irreversible operation checks.
- Dry-run differs from production constraints.
- Rollback plan exists but is incomplete or untested.

## Examples
- `examples/example-run.md`: dry-run planning output for table migration.

## Sub-Documentation
- `references/dry-run-checklist.md`: mandatory checklist sections.
- `references/rollback-query-template.md`: validation and rollback query patterns.
