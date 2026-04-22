---
name: secure-endpoint-review
description: Review API endpoint implementations for secure defaults, auth enforcement, input validation, and least-privilege behavior. Use when introducing or modifying HTTP endpoints, especially in services handling sensitive data.
---

# Secure Endpoint Review

## Scope
Identify, prioritize, and remediate endpoint security weaknesses before merge by combining deterministic checks with manual threat-aware review.

## When to Use
- New routes/controllers are introduced.
- Existing endpoint auth/authorization logic changes.
- Endpoint handles PII, financial, or internal-sensitive data.
- Error handling, logging, or serialization behavior changes.

## When Not to Use
- Static website-only changes with no backend request handling.
- Internal scripts with no external request boundary.
- Throwaway prototypes not shipping to real users.

## Required Inputs
- `endpoint_code`: route + middleware + handler implementation.
- `auth_policy`: required actor roles and permissions.
- `data_sensitivity`: classification for request/response fields.
- `threat_assumptions` (optional but recommended): abuse scenarios in scope.

## Expected Outputs
- `security_findings.md` with severity, evidence, and fix recommendation.
- `secure_patch.diff` with minimum required fixes.
- `residual_risk.md` when findings are accepted but not fixed in this PR.

## Workflow
1. Map trust boundaries.
- Identify entrypoint, auth middleware, and business logic boundary.
- Identify attacker-controlled inputs.
2. Validate authentication.
- Confirm endpoint cannot bypass auth path.
- Confirm anonymous/default principals are handled intentionally.
3. Validate authorization.
- Confirm resource-level access checks exist.
- Confirm least-privilege role mapping.
4. Validate input handling.
- Confirm schema validation and size constraints.
- Confirm sanitization/normalization rules.
5. Validate data handling.
- Confirm no sensitive fields are logged.
- Confirm response and error paths do not leak internals.
6. Validate abuse controls.
- Check rate limiting, idempotency, and replay considerations when relevant.
7. Emit findings and fixes.
- Tag each issue with severity and exploitability.
- Provide precise file/line remediation guidance.

## Validation Strategy
- Run `scripts/scan_fastapi_route.py` for baseline static checks.
- Use manual review for context-specific threat paths.
- Require explicit approval for unresolved high findings.
- Re-run scan after remediation to prevent regression.

## Failure Modes
- Middleware exists but is bypassed on alternate route path.
- Authorization checks validate role but not resource ownership.
- Validation library exists but model is not applied to the handler input.
- Errors leak stack traces or token-like values.

## Examples
- `examples/example-run.md`: route-hardening review with high-severity findings and fix path.

## Severity Model
- `high`: exploitable auth/data exposure risk, block merge.
- `medium`: meaningful risk, require fix or explicit security sign-off.
- `low`: hygiene issue, track in backlog with owner.

## Sub-Documentation
- `references/review-template.md`: standard output template.
- `references/owasp-mapping.md`: mapping common endpoint flaws to OWASP categories.
- `references/secure-defaults-checklist.md`: operational secure-default checklist.
