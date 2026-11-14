# lockstep-catalog-upkeep Specification

## Purpose

Keep complete-file navigation current through explicit source-bound semantic review and deterministic rendering, without silently approving stale summaries.

## Requirements

### Requirement: Tracked file review stays bound to source

When catalog maintenance is configured, Lockstep SHALL compare every Git-index path and reviewed input hash with the existing inventory, reporting added, changed and removed files. An explicit semantic review SHALL name the observed source hash, a nonempty summary and a review reason; a changed source SHALL invalidate that review before inventory writes. Source files SHALL never be executed. Inventory and catalog self-output hashes SHALL be omitted explicitly while retaining their navigation entries.

Source: Brian, 2026-11-13: “i approve proceed” for complete-file wiki upkeep; exact hash-bound review mechanism inferred by agent from existing inventory freshness and native semantic-review protocol.

#### Scenario: Review acknowledges exactly the bytes read

- **WHEN** an agent reviews a changed file and records its observed hash and summary
- **THEN** only a matching current source is acknowledged and its reviewed summary is retained

#### Scenario: A source changes after reading

- **WHEN** review supplies a hash different from current bytes
- **THEN** the batch fails without changing the inventory

### Requirement: Catalog refresh never approves meaning

Deterministic refresh SHALL render the existing inventory into complete file navigation without acknowledging pending semantic reviews or silently replacing input hashes. Pending review SHALL remain visible. Read-only check SHALL fail for missing coverage, stale source review or stale rendered output without writing. Invalid configuration or escaping paths SHALL fail explicitly. Unconfigured consumers SHALL remain unchanged.

Source: inferred by agent from Brian's complete-file coverage requirement and distinction between source review and byte freshness.

#### Scenario: Refresh cannot conceal a bypass

- **WHEN** a source changes without semantic review and refresh runs
- **THEN** check still reports its pending review

### Requirement: Hooks and gates expose pending review

Configured post-edit refresh SHALL report pending files and recovery instructions to the active agent and refresh deterministic navigation without broad requirement regeneration. AES local and pre-commit checks SHALL independently check catalog freshness. Ordinary and failed review/refresh operations SHALL retain daily trace evidence distinguishing review from deterministic generation. Existing unrelated configuration SHALL be preserved.

Source: Brian, 2026-11-13: “i approve proceed”; native hook and facts-only gate reused from the accepted self-adoption slice.

#### Scenario: Native edit requests semantic review

- **WHEN** a native client edits a tracked source
- **THEN** its post-edit hook identifies pending review and the agent can follow the explicit review/render recovery path

#### Scenario: Bypassed edit fails locally

- **WHEN** an edit bypasses the native hook
- **THEN** the independent local check reports stale review or output without writing
