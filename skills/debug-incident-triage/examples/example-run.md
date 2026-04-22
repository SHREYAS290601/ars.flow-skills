# Example Run: Checkout Timeouts

- Clustered 382 timeout errors and 214 DB pool errors.
- Correlated spike with deployment at 14:20 UTC.
- Suggested immediate containment: reduce worker concurrency and roll back pool config change.
