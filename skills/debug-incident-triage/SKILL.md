---
name: debug-incident-triage
description: Triage incidents by clustering error signatures, ranking likely causes, and mapping immediate containment actions. Use during active failures where teams need fast, structured debugging under time pressure.
---

# Debug Incident Triage

## Scope
Convert noisy failure evidence into an actionable triage report with probable causes and next diagnostic steps.

## When to Use
- Active incidents with repeated application errors.
- CI/CD or runtime failures with large unstructured logs.
- On-call handoffs that need concise, prioritized context.

## When Not to Use
- Postmortem writing after incident is fully resolved.
- Issues with no log or telemetry evidence.
- Changes that are clearly deterministic and already root-caused.

## Required Inputs
- `incident_logs.txt`: relevant error and warning lines.
- `service_context.md`: deployment and dependency context.
- `recent_changes.md`: recent PRs or config changes.

## Expected Outputs
- `triage_report.md` with ranked hypotheses.
- `next_checks.md` with concrete commands and owners.

## Workflow
1. Collect and normalize error lines from logs.
2. Group similar failures by signature.
3. Rank hypotheses using frequency and recency.
4. Correlate with recent changes and dependency events.
5. Propose containment actions and verification steps.
6. Update report as evidence confirms or rejects hypotheses.

## Validation Strategy
- Run `scripts/cluster_log_signatures.py` to group recurring errors.
- Require each hypothesis to include confirming and disconfirming checks.
- Track which checks were executed and observed outcomes.

## Failure Modes
- Logs are incomplete or truncated, hiding the primary trigger.
- Frequency bias overweights noisy secondary symptoms.
- Teams skip hypothesis invalidation and prematurely converge.

## Examples
- See `examples/example-run.md` for a deployment incident triage run.
