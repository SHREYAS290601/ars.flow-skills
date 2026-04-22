# Edge Cases: JSON Schema Enforcer

## 1. Nullable vs Missing
Treat `null` and missing as distinct states.
- Missing required key: hard fail.
- Present with `null`: follow strictness policy.

## 2. Numeric Strings
`"42"` is not an integer unless coercion is explicitly allowed.

## 3. Boolean-like Strings
Reject `"true"`/`"false"` when field type is boolean.

## 4. Enum Drift
When upstream introduces a new enum value:
1. Fail deterministically.
2. Record unknown value frequency.
3. Update contract intentionally with version note.

## 5. Nested Object Partials
If nested object support is limited in the validator:
- Fail at top-level path with explicit limitation note.
- Route to manual review for nested semantic checks.
