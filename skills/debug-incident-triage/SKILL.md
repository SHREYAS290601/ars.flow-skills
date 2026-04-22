---
name: debug-incident-triage
description: Triage incidents by clustering error signatures, ranking likely causes, and mapping immediate containment actions. Use during active failures where teams need fast, structured debugging under time pressure.
---

# Debug Incident Triage

## Scope
Turn noisy incident evidence into a prioritized hypothesis list, concrete containment actions, and a verifiable next-check plan that can be executed quickly under on-call pressure.

## When to Use
- Active production incidents with repeated error patterns.
- CI/CD failures with high-volume unstructured logs.
- Urgent handoffs where structured context is missing.

## When Not to Use
- Final postmortem writing after root cause is confirmed.
- Cases with no telemetry/log evidence.
- Trivial deterministic failures already root-caused.

## Required Inputs
- `incident_logs.txt`: error/warn logs during incident window.
- `service_context.md`: topology, dependencies, and recent deploys.
- `recent_changes.md`: merged PRs/config changes in lookback window.
- `impact_summary.md` (recommended): user/system impact signals.

## Expected Outputs
- `triage_report.md`:
  - ranked hypotheses
  - confidence level
  - supporting/refuting evidence
- `next_checks.md`: concrete commands, owners, and ETA.
- `containment_plan.md`: immediate blast-radius reduction actions.

## Workflow
1. Normalize evidence.
- Remove irrelevant noise.
- Normalize log signatures for grouping.
2. Cluster signals.
- Group recurring signatures by normalized message.
- Rank by frequency and timing.
3. Correlate timeline.
- Align error spikes with deploy/config/dependency changes.
4. Build hypotheses.
- State top plausible causes with confidence.
- Include disconfirming checks for each hypothesis.
5. Propose containment.
- Recommend low-risk actions to reduce impact quickly.
6. Execute and update.
- Track check outcomes and update ranking after each result.
7. Prepare handoff-ready output.
- Ensure next on-call can continue without reconstructing context.

## Validation Strategy
- Use `scripts/cluster_log_signatures.py` for deterministic grouping.
- Require each hypothesis to include confirmation + refutation checks.
- Track decision log to avoid repeated dead-end checks.
- Re-rank hypotheses after each new evidence batch.

## Failure Modes
- Incomplete logs hide root trigger.
- Frequency bias overweights noisy secondary errors.
- Team converges too quickly and skips hypothesis falsification.
- Containment actions mask symptoms while root cause remains active.

## Examples
- `examples/example-run.md`: checkout incident triage example.
- `examples/incident_logs.txt`: sample log stream for clustering.

## Handoff Standard
Every triage output should include:
1. Incident state and impact.
2. Top 3 hypotheses.
3. Checks already executed.
4. Checks pending with owners.
5. Containment status.

## Sub-Documentation
- `references/triage-template.md`: standard report template.
- `references/hypothesis-ranking.md`: confidence scoring guidance.
- `references/containment-playbook.md`: safe containment action patterns.
