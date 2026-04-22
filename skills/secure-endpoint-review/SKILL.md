---
name: secure-endpoint-review
description: Review API endpoint implementations for secure defaults, auth enforcement, input validation, and least-privilege behavior. Use when introducing or modifying HTTP endpoints, especially in services handling sensitive data.
---

# Secure Endpoint Review

## Scope
Identify and remediate insecure endpoint behavior before merge by enforcing deterministic secure-default checks.

## When to Use
- New route handlers or controller logic.
- Authentication and authorization refactors.
- Endpoints touching payment, identity, or PII workflows.

## When Not to Use
- Static content-only changes unrelated to request handling.
- Internal scripts with no inbound API surface.
- Exploratory prototypes not intended for deployment.

## Required Inputs
- `endpoint_code`: route/controller code under review.
- `auth_policy`: expected actor permissions.
- `data_sensitivity`: classification of payload fields.

## Expected Outputs
- `security_findings.md`: prioritized findings with severity and fixes.
- `secure_patch.diff`: changes that enforce safe defaults.

## Workflow
1. Identify endpoint entrypoints and auth middleware path.
2. Verify authentication is enforced before business logic.
3. Verify authorization checks align with policy.
4. Validate input schema and sanitization.
5. Check logging for sensitive data leakage.
6. Verify response and error handling do not expose internals.
7. Capture findings and proposed remediations.

## Validation Strategy
- Run `scripts/scan_fastapi_route.py` for simple static checks.
- Pair script findings with manual review for context-specific risks.
- Require explicit approval for unresolved high severity findings.

## Failure Modes
- Security middleware exists but is bypassed for some code paths.
- Input validators accept unbounded payloads leading to abuse.
- Logs leak secrets, tokens, or PII during error handling.

## Examples
- See `examples/example-run.md` for a route hardening review.
