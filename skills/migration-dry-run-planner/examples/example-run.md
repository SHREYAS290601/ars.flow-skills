# Example Run: Dry-Run Plan

- Preflight checks: backup recency, lock contention baseline.
- Dry-run phases: schema add -> backfill -> verification.
- Rollback trigger: error-rate > 2% for 10 min.
