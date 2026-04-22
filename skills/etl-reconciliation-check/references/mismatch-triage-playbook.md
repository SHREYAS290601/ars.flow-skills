# Mismatch Triage Playbook

## Step 1: Classify
- Count mismatch
- Duplicate mismatch
- Checksum mismatch

## Step 2: Isolate Layer
- Extraction
- Transformation
- Load

## Step 3: Containment
- Block publish for critical datasets
- Trigger rollback if already published

## Step 4: Verify Fix
Regenerate summaries and rerun reconciliation before releasing.
