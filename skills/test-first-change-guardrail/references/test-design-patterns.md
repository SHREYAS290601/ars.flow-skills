# Test Design Patterns

## Pattern 1: Reproducible Bug Harness
- Freeze clocks and random seeds.
- Build smallest failing input fixture.

## Pattern 2: Boundary Table Tests
Use boundary values and expected outputs in a table-driven format.

## Pattern 3: Contract Snapshot
When output shape is critical, snapshot only stable fields.

## Pattern 4: Side-Effect Assertion
Assert both direct output and side effects (events, DB writes, external calls).
