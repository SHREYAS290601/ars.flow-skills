# Window Alignment Guide

## Why It Matters
Most false reconciliation failures come from comparing non-identical windows.

## Alignment Checklist
- Same start/end timestamps
- Same timezone normalization
- Same late-arrival handling policy
- Same partition inclusion rules

## Recommended Practice
Persist window metadata with each summary file and fail fast if metadata differs.
