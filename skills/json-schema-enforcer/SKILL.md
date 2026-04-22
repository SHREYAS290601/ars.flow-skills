---
name: json-schema-enforcer
description: Enforce strict JSON outputs against an explicit contract with deterministic checks and explicit repair loops. Use for API payload generation, tool calls, and machine-consumed agent outputs where malformed fields, schema drift, or extra keys are unacceptable.
---

# JSON Schema Enforcer

## Scope
Produce machine-consumable JSON outputs that strictly follow a declared contract, fail deterministically when the payload diverges, and provide a repair path that is explicit and reproducible.

The goal is not only "valid JSON" but "contract-sound JSON".

## When to Use
- A downstream system parses the output automatically.
- The output is used as input to a tool call, API, or job runner.
- Team policy requires no undeclared keys and controlled enums.
- You need deterministic pass/fail behavior for CI or production gates.

## When Not to Use
- Free-form analysis, drafting, or brainstorming outputs.
- Tasks where slight schema drift is acceptable and manually reviewed.
- Early exploration before the output contract is known.

## Required Inputs
- `contract_definition`:
  - required keys
  - expected primitive types
  - allowed values for constrained fields
  - forbidden keys
- `candidate_output`: the JSON object to validate.
- `strictness_policy`:
  - how to handle nulls
  - whether unknown keys are hard-fail
  - whether coercion is allowed (default: not allowed)

## Expected Outputs
- `validated_output.json` when checks pass.
- `validation_report.md` with deterministic violation list when checks fail.
- optional `repair_log.md` describing each correction applied between attempts.

## Workflow
1. Normalize inputs before validation.
- Ensure contract and candidate are parseable JSON.
- Confirm expected root object type.
2. Execute structural checks.
- Verify required keys exist.
- Verify forbidden keys are absent.
3. Execute type checks.
- Compare each declared key to its expected type.
- Reject implicit coercions unless strictness policy allows them.
4. Execute domain checks.
- Validate constrained enums and known literal sets.
- Validate sentinel values (`unknown`, `n/a`) according to policy.
5. Emit deterministic violations.
- Every failure must include field path, expected value/type, and observed value/type.
6. Repair and revalidate.
- Apply one logical repair batch.
- Re-run validator.
- Repeat until pass or max attempts reached.
7. Publish only after pass.
- Do not publish partially repaired data without final passing run.

## Validation Strategy
- Use `scripts/assert_contract.py` as the deterministic gate.
- Store failing fixtures in `examples/` for regression rechecks.
- Require identical results across repeated runs with same inputs.
- For high-risk workflows, add a human sign-off on semantic correctness even after schema pass.

## Failure Modes
- Contract underspecification allows semantically wrong values to pass.
- Contract overspecification blocks valid payload evolution.
- Enum drift after upstream changes causes widespread hard failures.
- Optional fields become de facto required by downstream systems without contract updates.

## Examples
- `examples/example-run.md`: full pass/fail/repair walk-through.
- `examples/contract.json`: reference contract.
- `examples/candidate_fail.json`: deterministic fail fixture.
- `examples/candidate_pass.json`: deterministic pass fixture.

## Output Contract for This Skill
When you apply this skill, produce:
1. Validation status (`PASS` or `FAIL`).
2. Violation table with path, expected, observed, severity.
3. Repair actions (if any).
4. Final publish recommendation (`publish`, `block`, `requires-human-review`).

## Sub-Documentation
Read these references based on context:
- `references/contract-format.md`: canonical contract schema used by the checker.
- `references/edge-cases.md`: nullability, arrays, nested objects, and enum drift patterns.
- `references/repair-playbook.md`: deterministic fix ordering and retry policy.
