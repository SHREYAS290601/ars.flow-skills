---
name: missing-tests-pr-reviewer
description: Inspect changed files and detect likely missing tests for modified production code before merge.
---

# Missing Tests PR Reviewer

## Scope
Identify code changes that likely require test updates and flag missing coverage expectations.

## When to Use
- Pull requests modify business logic or APIs.
- Teams enforce test expectations on code changes.
- Review automation for regression prevention.

## When Not to Use
- Docs-only or style-only changes.
- Repositories without formal test structure.

## Required Inputs
- changed source file list.
- existing test file inventory.

## Expected Outputs
- `missing_tests_report.md` with source->expected test mapping gaps.
- `coverage_expectation_checklist.md` for reviewer sign-off.

## Workflow
1. Parse changed files.
2. Filter likely production code paths.
3. Derive expected corresponding test file patterns.
4. Compare with discovered tests.
5. Emit missing test findings and reviewer checklist.

## Validation Strategy
- Run `scripts/detect_missing_tests.py` in PR CI.
- Fail for high-risk paths missing expected tests.
- Allow explicit exemptions with reviewer note.

## Failure Modes
- Naming conventions may vary by repository.
- Cross-module tests can satisfy coverage but look missing by pattern.
- Generated code updates can produce false positives.

## Examples
- `examples/example-run.md`: identifies missing tests for changed service files.

## Sub-Documentation
- `references/test-mapping-rules.md`: source-to-test mapping heuristics.
- `references/exemption-policy.md`: policy for justified missing-test exceptions.
