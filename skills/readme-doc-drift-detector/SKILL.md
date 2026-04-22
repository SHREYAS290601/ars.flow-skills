---
name: readme-doc-drift-detector
description: Detect drift between README instructions and actual runnable scripts/config so documentation stays operationally accurate.
---

# README Doc Drift Detector

## Scope
Compare documented commands and setup steps with repository executable surfaces to flag stale or incorrect README instructions.

## When to Use
- PR updates scripts/tooling/startup commands.
- Release readiness checks for developer onboarding docs.
- Documentation quality gates.

## When Not to Use
- Repositories without command-driven workflows.
- Docs unrelated to runnable setup instructions.

## Required Inputs
- `README.md` or equivalent docs.
- runtime command definitions (e.g., `package.json` scripts).

## Expected Outputs
- `doc_drift_report.md` with mismatches.
- `missing_commands.txt` and `undocumented_commands.txt` summaries.

## Workflow
1. Parse documented commands from README.
2. Parse executable command sources.
3. Compare command sets for mismatches.
4. Classify drift as blocking or advisory.
5. Emit remediation suggestions.

## Validation Strategy
- Run `scripts/check_readme_scripts.py` in CI for repos with script surfaces.
- Treat missing documented commands as warning.
- Treat documented-but-missing executable commands as fail.

## Failure Modes
- Commands appear in docs via prose but not standardized format.
- Script aliases obscure true command surfaces.
- Multi-tool repos require additional command sources.

## Examples
- `examples/example-run.md` with missing and stale command detection.

## Sub-Documentation
- `references/readme-command-format.md`: expected command documentation format.
- `references/drift-severity-policy.md`: fail vs warn policy.
