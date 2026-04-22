---
name: repo-workflow-bootstrap
description: Bootstrap repository-level build, test, and CI workflow conventions with deterministic checks and minimal baseline automation. Use when onboarding a codebase that lacks reliable engineering guardrails.
---

# Repo Workflow Bootstrap

## Scope
Establish repeatable local and CI workflows so repositories have deterministic build and test expectations.

## When to Use
- New repositories with inconsistent developer setup.
- Legacy repositories missing CI standards.
- Team onboarding where baseline engineering controls are absent.

## When Not to Use
- Mature repos with stable conventions already enforced.
- One-off scripts that are not shared or maintained.
- Repositories intentionally frozen and not accepting active development.

## Required Inputs
- `repo_layout`: current build/test files and language stack.
- `required_checks`: mandatory quality gates for merge.
- `ci_environment`: target CI platform assumptions.

## Expected Outputs
- `workflow_plan.md`: recommended local and CI command contract.
- `bootstrap_patch.diff`: baseline scripts and config updates.

## Workflow
1. Detect current package manager and build toolchain.
2. Define canonical commands (`install`, `lint`, `test`, `typecheck`, `build`).
3. Standardize CI entrypoint and failure behavior.
4. Add local scripts that mirror CI behavior.
5. Verify new workflow files exist and are discoverable.
6. Document maintenance expectations.

## Validation Strategy
- Run `scripts/verify_pipeline_files.py` to confirm required workflow files exist.
- Execute canonical commands in a dry run where possible.
- Block adoption if command contract is ambiguous.

## Failure Modes
- Tooling mismatch across local and CI environments.
- Multiple package managers cause nondeterministic lockfile behavior.
- Missing docs lead to drift in command conventions.

## Examples
- See `examples/example-run.md` for a repo bootstrap audit and patch plan.
