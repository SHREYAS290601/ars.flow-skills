---
name: repo-workflow-bootstrap
description: Bootstrap repository-level build, test, and CI workflow conventions with deterministic checks and minimal baseline automation. Use when onboarding a codebase that lacks reliable engineering guardrails.
---

# Repo Workflow Bootstrap

## Scope
Establish deterministic local and CI workflow conventions so every repository has a reproducible command contract and predictable quality gates.

## When to Use
- New repos with no shared engineering workflow.
- Legacy repos with inconsistent tooling and weak CI.
- Teams onboarding multiple contributors quickly.

## When Not to Use
- Mature repos that already enforce stable conventions.
- Repositories that are archived or no longer actively developed.
- Experimental one-off code where governance is intentionally minimal.

## Required Inputs
- `repo_layout`: existing files, package managers, and build/test tooling.
- `required_checks`: organization-level quality gates.
- `ci_environment`: target runner and constraints.
- `language_matrix` (optional): multi-language repo execution expectations.

## Expected Outputs
- `workflow_plan.md`: canonical commands and ownership model.
- `bootstrap_patch.diff`: scripts/config updates.
- `adoption_notes.md`: migration steps for contributors.

## Workflow
1. Inventory current state.
- Detect package manager(s), lockfiles, and script surfaces.
- Detect current CI workflows and failure policies.
2. Define canonical command contract.
- `install`, `lint`, `typecheck`, `test`, `build`.
- Document expected runtime and artifacts.
3. Align local and CI execution.
- Ensure CI calls the same commands as local workflow.
- Remove hidden CI-only command branches when possible.
4. Add baseline governance files.
- README workflow instructions.
- CI workflow file(s).
- contributor or quality gate notes.
5. Validate command contract.
- Confirm required files exist.
- Dry-run commands or command presence checks.
6. Roll out and stabilize.
- Document fallback path for legacy commands.
- Track adoption issues and resolve command drift.

## Validation Strategy
- Use `scripts/verify_pipeline_files.py` for baseline file checks.
- Require one-command quality gate path for CI and local.
- Detect and fail multi-package-manager ambiguity unless explicitly allowed.
- Run periodic audit for command drift.

## Failure Modes
- Local commands diverge from CI over time.
- Multiple lockfiles create nondeterministic installs.
- CI workflow exists but does not block merge on failures.
- Documentation exists but omits critical environment assumptions.

## Examples
- `examples/example-run.md`: repo audit and bootstrap plan example.

## Rollout Guidance
- Prefer incremental adoption: stabilize command contract first, then enforce strict gates.
- For large legacy repos, use a transition period with deprecation dates.

## Sub-Documentation
- `references/repo-baseline.md`: minimum required workflow artifacts.
- `references/command-contract-template.md`: template for standardized commands.
- `references/migration-strategy.md`: phased rollout approach for legacy repos.
