# Flaky Test Triage

## Detection
- Re-run suspect tests 10x.
- Mark tests flaky only with reproducible evidence.

## Common Causes
- Time dependence
- Shared mutable state
- External network calls
- Non-isolated test data

## Remediation
1. Isolate dependencies.
2. Remove time/network nondeterminism.
3. Stabilize fixtures.
4. Re-enable test in required suite.
