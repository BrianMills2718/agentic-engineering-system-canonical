## Why

Lockstep launches some verification inputs in subprocesses, outside AES import discovery. Existing observations can therefore remain current after those inputs change. Adding correct new records alone does not fix this: older weak SUPPORTS observations can still mask later staleness.

Source: Brian's active Lockstep completion goal, 2026-11-07, authorizes necessary narrow AES component integration; the former AES self-governance program remains on hold.

## What Changes

Add optional `required_dependency_paths` mappings to the existing `evidence.assess` and `reconcile` library APIs. Qualify current observations against recorded declared coverage, retaining historical records and existing freshness/standing ownership. Default calls retain existing behavior. No record format, recorder, CLI, execution cache, or former governance regime changes.

## Capabilities

### New Capabilities

- `required-evidence-inputs`: caller-specified repository inputs qualify existing evidence before standing is computed.

## Impact

Changes the evidence and reconciliation APIs, focused evidence regressions, and current engine architecture/state documentation. Lockstep owns caller configuration and explicit dependency recording.
