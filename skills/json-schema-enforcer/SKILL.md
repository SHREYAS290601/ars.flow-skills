---
name: json-schema-enforcer
description: Enforce strict JSON outputs against an explicit contract with deterministic checks and clear repair loops. Use for API payload generation, tool calls, and machine-consumed agent outputs where malformed fields or schema drift are unacceptable.
---

# JSON Schema Enforcer

## Scope
Produce machine-consumable JSON outputs that strictly follow a pre-declared contract and fail fast on schema mismatches.

## When to Use
- Responses must be parsed by downstream systems.
- A workflow requires deterministic pass/fail checks on output structure.
- Team policy forbids extra keys or ambiguous enum values.

## When Not to Use
- Exploratory writing tasks where free-form text is desired.
- One-off tasks without any machine consumer.
- Cases where a loose schema is acceptable and no validation is required.

## Required Inputs
- `contract_definition`: required keys, allowed values, and type expectations.
- `candidate_output`: JSON object produced by the agent or pipeline.
- `strictness_policy`: whether additional keys are allowed and how to handle nulls.

## Expected Outputs
- `validated_output.json` when all checks pass.
- `validation_report.md` listing deterministic failures and repair actions.

## Workflow
1. Load contract and candidate output.
2. Validate JSON parseability before semantic checks.
3. Enforce required fields and field types.
4. Enforce constrained values (enums, known states).
5. Reject forbidden keys and emit exact failure paths.
6. Repair output and rerun checks until deterministic pass.
7. Publish output only after checks pass.

## Validation Strategy
- Run `scripts/assert_contract.py` to verify required fields, basic types, allowed values, and forbidden keys.
- Save failed runs in `examples/` to keep a regression corpus.
- Treat all validation failures as blocking for deployment workflows.

## Failure Modes
- Contract omits required business constraints and allows semantically wrong outputs.
- Upstream task produces valid JSON with incorrect field semantics.
- Enum drift introduces values not represented in the contract.

## Examples
- See `examples/example-run.md` for a pass/fail walkthrough.
- Sample files are provided in `examples/contract.json`, `examples/candidate_pass.json`, and `examples/candidate_fail.json`.
