# Example Run: Order Status Validation

## Input
- Contract: `contract.json`
- Candidate payload: `candidate_fail.json`

## Validation output
- Missing required field: `timestamp`
- Invalid enum value for `status`: `pending_review`
- Forbidden field present: `debug`

## Repair
- Added `timestamp` in ISO UTC format
- Changed `status` to `processing`
- Removed `debug`

## Result
`candidate_pass.json` passes all checks.
