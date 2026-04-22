---
name: test-first-change-guardrail
description: Drive code changes through explicit failing tests first, then implementation, then regression verification. Use when shipping risky or behavior-changing modifications where preventing silent regressions is required.
---

# Test-First Change Guardrail

## Scope
Enforce a repeatable test-first workflow that proves a bug or feature gap before code changes and verifies no regressions after implementation.

## When to Use
- Bug fixes where prior behavior is unclear.
- Feature changes that can be represented as deterministic tests.
- Pull requests that modify business logic or data transformations.

## When Not to Use
- Pure refactors that intentionally keep behavior identical and already have broad coverage.
- Spikes or exploration work that is not ready for deterministic acceptance criteria.
- UI polish-only changes without reliable test harnesses.

## Required Inputs
- `change_request`: bug report or feature requirement.
- `existing_tests`: current test coverage context.
- `acceptance_criteria`: deterministic behavior expectations.

## Expected Outputs
- `failing_test_patch`: tests proving the gap before implementation.
- `implementation_patch`: minimal code changes to satisfy new tests.
- `verification_log`: command output showing full regression run.

## Workflow
1. Reproduce failure with a deterministic test.
2. Commit or stage failing test separately.
3. Implement minimal code to make new test pass.
4. Run target tests and full relevant suite.
5. Document what was intentionally not changed.
6. Block merge if regression checks fail.

## Validation Strategy
- Use `scripts/check_test_plan.py` to ensure plans include baseline, failing test, and regression steps.
- Require command logs for test execution in PR notes.
- Keep failing-test-first discipline mandatory for high-risk files.

## Failure Modes
- Test added after implementation hides whether behavior truly changed.
- Overly broad implementation passes tests but introduces side effects.
- Regression suite is too narrow and misses adjacent breakages.

## Examples
- See `examples/example-run.md` for a bug-fix timeline with red-green-refactor checkpoints.
