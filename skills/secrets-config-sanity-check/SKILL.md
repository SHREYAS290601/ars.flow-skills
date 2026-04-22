---
name: secrets-config-sanity-check
description: Check environment/config definitions for missing keys, unsafe defaults, and secret-handling mistakes before deployment.
---

# Secrets Config Sanity Check

## Scope
Perform deterministic sanity checks on environment and config files to catch dangerous defaults and missing critical settings.

## When to Use
- New services introduce `.env` or runtime configuration.
- Deployment manifests are updated.
- Security reviews before release.

## When Not to Use
- Repositories without config/environment conventions.
- Generated test fixtures that are not deployed.

## Required Inputs
- `.env.example` or equivalent required key list.
- environment/config files for target environment.

## Expected Outputs
- `config_sanity_report.md` with failures/warnings.
- `missing_required_keys.txt` list.
- `unsafe_defaults.txt` list.

## Workflow
1. Parse required keys from `.env.example`.
2. Parse target config values.
3. Detect missing required keys.
4. Detect unsafe defaults (placeholder or insecure values).
5. Emit pass/fail report with remediation actions.

## Validation Strategy
- Run `scripts/scan_env_sanity.py` in CI before deploy.
- Treat missing required keys as hard-fail.
- Treat unsafe defaults as fail for production-bound configs.

## Failure Modes
- Required key list in `.env.example` is stale.
- Secrets are injected by external platform and not represented locally.
- False positives for intentionally empty values without context.

## Examples
- `examples/example-run.md`: catches missing/unsafe config values.

## Sub-Documentation
- `references/required-keys-policy.md`: policy for required configuration keys.
- `references/unsafe-defaults-list.md`: known dangerous defaults.
