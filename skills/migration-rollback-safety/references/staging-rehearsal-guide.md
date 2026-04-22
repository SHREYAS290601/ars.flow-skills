# Staging Rehearsal Guide

## Goals
- Validate forward migration steps.
- Validate rollback speed and correctness.
- Measure operational timing.

## Procedure
1. Snapshot baseline metrics.
2. Run forward migration.
3. Trigger rollback scenario.
4. Execute rollback.
5. Compare post-rollback integrity to baseline.

## Exit Criteria
- Data integrity restored.
- Service health returns to baseline thresholds.
- Total rollback duration within RTO.
