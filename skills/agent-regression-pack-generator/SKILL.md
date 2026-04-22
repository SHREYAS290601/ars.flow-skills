---
name: agent-regression-pack-generator
description: Generate and validate regression case packs for agent workflow changes so behavior can be re-tested consistently.
---

# Agent Regression Pack Generator

## Scope
Create structured regression test packs for prompt/tool/workflow updates and validate pack completeness before execution.

## When to Use
- Agent prompt/workflow/tool behavior changes.
- Pre-release evaluation for agent reliability.
- CI checks for behavior regression risk.

## When Not to Use
- One-off exploratory agent prompts.
- Systems without reusable evaluation harness.

## Required Inputs
- `change_summary.md`: what behavior changed.
- `baseline_cases.json`: existing evaluation cases.
- `risk_areas.md`: scenarios with highest regression risk.

## Expected Outputs
- `regression_pack.json` structured test cases.
- `evaluation_plan.md` with execution and pass/fail criteria.
- `coverage_gaps.md` listing untested risk areas.

## Workflow
1. Identify behavior change surface.
2. Select impacted baseline cases.
3. Generate new edge and failure cases.
4. Validate pack schema completeness.
5. Emit execution plan with assertions.

## Validation Strategy
- Run `scripts/validate_regression_pack.py` to enforce case schema.
- Require each risk area to map to at least one case.
- Block release when high-risk areas remain uncovered.

## Failure Modes
- Cases validate structurally but miss semantic assertions.
- Risk areas are under-specified and produce shallow packs.
- Case maintenance lags behind feature evolution.

## Examples
- `examples/example-run.md` for regression pack generation and validation.

## Sub-Documentation
- `references/case-schema.md`: required fields for each case.
- `references/coverage-mapping-guide.md`: mapping risk areas to cases.
