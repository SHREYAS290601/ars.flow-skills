# Command Contract Template

## Required Commands
- `install`
- `lint`
- `typecheck`
- `test`
- `build`

## Contract Rules
- Commands must run non-interactively.
- Commands must return non-zero on failure.
- CI must invoke the same commands.
