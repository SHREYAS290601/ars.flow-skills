# Example Run: Invoice Endpoint

- Route lacked explicit role authorization check.
- Error path included raw exception message.
- Fixes: enforce `require_role("billing_admin")`, sanitize exception response.
