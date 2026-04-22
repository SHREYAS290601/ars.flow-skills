---
name: api-contract-diff-checker
description: Compare old and new API contracts and deterministically flag breaking changes before merge. Use for OpenAPI/spec updates where backward compatibility must be enforced.
---

# API Contract Diff Checker

## Scope
Detect breaking API contract changes between two versions of an API specification and produce a deterministic compatibility report.

## When to Use
- Pull requests update `openapi.json` or API schema files.
- Public or shared internal APIs require compatibility guarantees.
- Release gates require explicit breaking-change evidence.

## When Not to Use
- Initial API design with no prior stable version.
- Experimental endpoints that are explicitly non-versioned.
- Non-contract changes (copy/docs only).

## Required Inputs
- `old_contract`: previous stable contract file (OpenAPI/JSON schema format).
- `new_contract`: proposed contract file.
- `compatibility_policy`: allowed vs disallowed change classes.

## Expected Outputs
- `contract_diff_report.md` with additive, modified, and removed surfaces.
- `breaking_changes.json` with machine-checkable failures.
- `release_recommendation.md` (`safe`, `safe-with-version-bump`, `block`).

## Workflow
1. Parse old and new contracts.
2. Enumerate endpoint + method surfaces.
3. Identify removals and method deletions.
4. Detect request-schema required-field additions.
5. Detect response-schema narrowing when applicable.
6. Classify each change as `breaking`, `non-breaking`, or `review`.
7. Emit deterministic report and release recommendation.

## Validation Strategy
- Run `scripts/compare_openapi.py` with old/new contract fixtures.
- Treat removed endpoints/methods as hard-breaking by default.
- Require human override note for policy exceptions.
- Archive every breaking change report for release auditability.

## Failure Modes
- Contract files omit runtime behavior constraints.
- Schema references are incomplete or flattened differently.
- Policy rules are too permissive and miss practical breakage.

## Examples
- `examples/example-run.md`: sample compatibility review.
- `examples/old_openapi.json` and `examples/new_openapi.json`: deterministic diff fixtures.

## Sub-Documentation
- `references/breaking-change-rules.md`: what is considered breaking.
- `references/versioning-guidance.md`: when to require API version bumps.
