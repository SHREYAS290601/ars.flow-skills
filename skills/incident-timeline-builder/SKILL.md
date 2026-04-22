---
name: incident-timeline-builder
description: Build a chronological incident timeline from logs, alerts, and commits to improve root-cause and post-incident analysis.
---

# Incident Timeline Builder

## Scope
Convert timestamped incident evidence into an ordered timeline with normalized event types and confidence annotations.

## When to Use
- Active incident investigations.
- Post-incident analysis requiring chronology.
- Cross-source evidence correlation (alerts, logs, deploys, PRs).

## When Not to Use
- Inputs without timestamps.
- Single-source deterministic failures where timeline adds little value.

## Required Inputs
- timestamped event records from logs/alerts/changes.
- optional source labels.

## Expected Outputs
- `incident_timeline.md` ordered event narrative.
- `incident_timeline.json` machine-readable ordered list.

## Workflow
1. Parse events and normalize timestamps.
2. Normalize event categories.
3. Sort chronologically.
4. Highlight key transitions (deploy, error spike, mitigation).
5. Emit timeline artifacts.

## Validation Strategy
- Run `scripts/build_timeline.py` to enforce timestamp parsing and ordering.
- Fail when events have invalid timestamps.
- Require source tagging for ambiguous event descriptions.

## Failure Modes
- Timezone inconsistencies can misorder events.
- Missing event coverage can bias conclusions.
- Duplicate events can inflate perceived severity.

## Examples
- `examples/example-run.md` demonstrates log-to-timeline conversion.

## Sub-Documentation
- `references/event-schema.md`: expected event input shape.
- `references/timeline-quality-checks.md`: quality checklist for usable timelines.
