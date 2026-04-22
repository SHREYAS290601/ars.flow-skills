---
name: test-first-change-guardrail
description: Drive code changes through explicit failing tests first, then implementation, then regression verification. Use when shipping risky or behavior-changing modifications where preventing silent regressions is required.
---

# Test-First Change Guardrail

## Scope
Enforce a repeatable red-green-refactor workflow where behavior change is proven by tests before code implementation and validated again with regression gates after implementation.

The skill is optimized for reliability, not speed.

## When to Use
- Bug fixes where expected behavior must be proven.
- Feature changes with deterministic acceptance criteria.
- High-risk modules where regressions are expensive.
- PRs where reviewer confidence depends on evidence.

## When Not to Use
- Pure formatting or comment-only edits.
- Disposable exploratory spikes.
- Workflows with no reliable test harness yet.

## Required Inputs
- `change_request`: bug ticket, requirement, or acceptance criteria.
- `existing_tests`: current tests around impacted behavior.
- `execution_environment`: commands needed to run targeted and full suites.

## Expected Outputs
- `failing_test_patch`: tests that fail before implementation.
- `implementation_patch`: minimal logic change to make tests pass.
- `verification_log`: command output proving green state.
- `risk_note.md`: explicit residual-risk statement when coverage is partial.

## Workflow
1. Freeze behavior assumptions.
- Write baseline behavior statement from ticket and current code.
- Document unknowns before adding tests.
2. Add failing test first.
- Add one focused failing test per distinct behavior gap.
- Verify failure is for the expected reason.
3. Implement minimal fix.
- Change only what is required for failing tests.
- Avoid opportunistic refactors in same patch unless justified.
4. Run targeted suite.
- Run local tests covering changed code paths.
- Confirm no flaky behavior is introduced.
5. Run broader regression suite.
- Run package/service-level tests based on blast radius.
- Capture command outputs.
6. Produce verification artifact.
- Include exact commands, pass/fail status, and runtime.
7. Final gate.
- If tests are missing for any critical path, block merge or require explicit exception.

## Validation Strategy
- Use `scripts/check_test_plan.py` to verify plan completeness.
- Require evidence of both failing-first and passing-final states.
- Enforce that regression command list is explicit and reproducible.
- Prefer deterministic tests; quarantine flaky tests before relying on them.

## Failure Modes
- Test added after implementation (sequence inversion).
- Overly broad implementation passes tests but changes unrelated behavior.
- Narrow regression scope misses neighboring risk.
- Flaky tests create false confidence.

## Examples
- `examples/example-run.md`: timeline of red-green-refactor with verification logs.

## Quality Gates
A change is only complete when:
1. Failing test evidence is recorded.
2. Implementation is minimal and traceable to test expectations.
3. Targeted + regression suites are green.
4. Residual risk is explicit.

## Sub-Documentation
- `references/checklist.md`: concise execution checklist.
- `references/test-design-patterns.md`: strategies for deterministic test design.
- `references/flaky-test-triage.md`: handling unstable tests without faking green.
