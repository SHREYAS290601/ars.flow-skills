---
name: migration-rollback-safety
description: Design safe schema or configuration migrations with explicit preflight checks, staged rollout, and tested rollback criteria. Use for production-impacting changes where irreversible mistakes are costly.
---

# Migration Rollback Safety

## Scope
Design migration runbooks that minimize production risk through preflight validation, phased rollout, explicit abort criteria, and rehearsed rollback steps.

## When to Use
- Production schema migrations.
- High-impact config changes with broad system effects.
- Changes where rollback is non-trivial or time-sensitive.

## When Not to Use
- Disposable local environments.
- Purely additive, proven backward-compatible non-critical changes.
- Environments without rollback authority/ownership.

## Required Inputs
- `migration_plan.md`: forward steps and dependencies.
- `rollback_constraints.md`: RTO/RPO, data-loss boundaries.
- `environment_inventory.md`: systems, owners, and dependencies.
- `traffic_profile.md` (recommended): peak windows and capacity limits.

## Expected Outputs
- `safe_runbook.md`: preflight + phased rollout + rollback plan.
- `rollback_matrix.md`: triggers, owners, and target response time.
- `verification_log.md`: post-phase verification evidence.

## Workflow
1. Classify migration risk.
- Identify irreversible operations.
- Identify lock/contention-sensitive steps.
2. Define preflight checks.
- capacity and lock profile
- backup/restore readiness
- dependency health
3. Phase rollout plan.
- break migration into observable checkpoints.
- include hold points and success criteria per phase.
4. Define abort criteria.
- latency, error rate, lock wait, or data integrity thresholds.
5. Define rollback plan.
- exact rollback commands/steps
- ownership and communication chain
- target completion window
6. Rehearse in staging.
- execute forward and rollback paths.
- capture timing and unexpected behavior.
7. Execute production migration.
- run with checkpoint verification.
- stop immediately on abort threshold breach.

## Validation Strategy
- Use `scripts/check_migration_plan.py` to enforce required sections.
- Require staging rollback rehearsal evidence for high-risk migrations.
- Require explicit rollback owner before production run.
- Validate backup restore path regularly, not only during incidents.

## Failure Modes
- Hidden irreversible operations invalidate rollback assumptions.
- Preflight checks pass but runtime lock contention differs under production load.
- Rollback steps are incomplete or untested.
- Ownership ambiguity delays critical rollback actions.

## Examples
- `examples/example-run.md`: phased schema migration with rollback triggers.

## Execution Guardrails
- Never start migration without validated rollback path.
- Prefer smaller phased migrations over single large cutover.
- Keep communication protocol explicit for go/no-go decisions.

## Sub-Documentation
- `references/rollback-matrix-template.md`: trigger/action owner matrix.
- `references/preflight-check-catalog.md`: recommended preflight checks by migration type.
- `references/staging-rehearsal-guide.md`: how to run and evaluate rollback rehearsal.
