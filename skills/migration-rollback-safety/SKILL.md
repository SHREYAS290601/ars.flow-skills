---
name: migration-rollback-safety
description: Design safe schema or configuration migrations with explicit preflight checks, staged rollout, and tested rollback criteria. Use for production-impacting changes where irreversible mistakes are costly.
---

# Migration Rollback Safety

## Scope
Create migration runbooks that reduce production risk through deterministic preflight, phased execution, and rollback triggers.

## When to Use
- Database schema migrations in production systems.
- High-impact config changes requiring staged rollout.
- Any change where rollback complexity is non-trivial.

## When Not to Use
- Local-only migrations with disposable data.
- Purely additive non-breaking changes with verified backward compatibility.
- Environments without rollback capability or ownership clarity.

## Required Inputs
- `migration_plan.md`: step-by-step forward plan.
- `rollback_constraints.md`: data-loss and RTO/RPO limits.
- `environment_inventory.md`: infra dependencies and owners.

## Expected Outputs
- `safe_runbook.md`: preflight, rollout, and rollback plan.
- `rollback_matrix.md`: trigger thresholds and owner actions.

## Workflow
1. Declare migration assumptions and non-reversible steps.
2. Define preflight checks and abort criteria.
3. Split execution into observable phases.
4. Define rollback triggers and owner responsibilities.
5. Validate rollback path in staging.
6. Execute with checkpoints and hold points.
7. Document post-rollout verification evidence.

## Validation Strategy
- Run `scripts/check_migration_plan.py` to verify critical runbook sections exist.
- Require staging rollback rehearsal evidence for high-risk changes.
- Block production rollout if rollback owner is undefined.

## Failure Modes
- Hidden irreversible operations invalidate rollback plans.
- Rollback steps are documented but never rehearsed.
- Runtime lock contention exceeds maintenance window assumptions.

## Examples
- See `examples/example-run.md` for a phased schema migration runbook.
