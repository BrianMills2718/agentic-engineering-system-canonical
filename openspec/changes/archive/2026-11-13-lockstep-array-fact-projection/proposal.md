## Why

Consumers store work-unit status in an array of records. The existing projection copies the whole array, making a readable status table a manual copy.

## What Changes

Extend declared fact projection with an optional top-level array selector and selected scalar fields. Reuse the source, hook and check paths; no inference or second generator.

## Capabilities

### Modified Capabilities

- `lockstep-doc-facts`: project declared arrays as rows and refuse invalid records before writes.

## Impact

Changes projection declarations, rendering, trace metadata and focused tests; existing declarations retain their behavior.
