# OWASP Mapping for Endpoint Reviews

## Broken Access Control
Indicators:
- Missing ownership checks
- Role checks without scope constraints

## Security Misconfiguration
Indicators:
- Debug error payloads in production
- Missing secure headers or weak defaults

## Injection
Indicators:
- Unsanitized query/body fields reaching SQL, shell, or template layers

## Identification and Authentication Failures
Indicators:
- Optional auth path on protected endpoints
- Session/token verification gaps
