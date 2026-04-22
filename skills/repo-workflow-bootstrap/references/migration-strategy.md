# Migration Strategy for Legacy Repos

## Phase 1: Baseline
- Add command aliases without changing behavior.
- Document required environment.

## Phase 2: Alignment
- Remove duplicate scripts.
- Make CI call canonical commands.

## Phase 3: Enforcement
- Enable required checks on protected branches.
- Deprecate old commands with cutoff date.
