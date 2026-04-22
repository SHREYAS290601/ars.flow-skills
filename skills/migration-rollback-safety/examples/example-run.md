# Example Run: Orders Schema Migration

- Preflight checks confirmed table size, lock profile, and index readiness.
- Rollout split into additive schema + backfill + read switch.
- Abort threshold: p99 latency +20% for 10 minutes.
- Rollback owner assigned for each phase.
