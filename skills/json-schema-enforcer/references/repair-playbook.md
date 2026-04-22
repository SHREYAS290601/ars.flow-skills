# Repair Playbook: JSON Schema Enforcer

## Repair Order
1. Parse and syntax fixes.
2. Required key insertion.
3. Forbidden key removal.
4. Type correction.
5. Enum correction.

## Retry Policy
- Maximum 3 repair attempts per payload.
- Abort early if violation count increases after a repair.

## Escalation Rules
Escalate to human review when:
- 2+ fields are ambiguous in meaning.
- Enum values are unknown and business-critical.
- Contract likely outdated.
