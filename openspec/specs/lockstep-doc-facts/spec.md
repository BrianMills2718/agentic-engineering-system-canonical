# lockstep-doc-facts Specification

## Purpose

Keep declared wiki and document facts in step with their authoritative source metadata, Python interfaces and native evidence records through generation, post-edit refresh and a read-only freshness gate.

## Requirements

### Requirement: Declared source facts have one authority

`lockstep check project` SHALL generate Markdown fact blocks declared by
`projections` in `lockstep.yaml`, each with id, source, target and fields,
with an optional Python symbol. It SHALL read Markdown YAML front matter,
JSON/YAML mapping fields and Python AST descriptions and signatures without
importing or executing source. `--check` SHALL report stale target paths and
exit 1 without writing. Generation SHALL preserve unrelated target content,
include a relative source link (or an HTTP(S) source_base_url link when configured), escape HTML and table delimiters in projected scalar values, and remain idempotent. Consumers with no recognized OpenSpec requirement text SHALL project only
declared facts, without creating an empty coverage page or rewriting historical plans.

Source: Brian, 2026-11-12, "its not jsut a status tag ... ther should be hooks and stuff that automatically keep this all up to date", followed by "ok proceed"; AES-CTX-004 and accepted Decision 0013.

#### Scenario: Markdown facts regenerate and stale check is read only

- **GIVEN** a declared wiki block for a plan's description and status
- **WHEN** the source changes from active to done
- **THEN** check mode exits 1 without writes and generation updates both facts while preserving other prose

#### Scenario: Python description and interface are static

- **GIVEN** a source module that would fail if imported, with a documented function
- **WHEN** its description or signature changes
- **THEN** the AST projection detects and repairs the stale block without executing the module

#### Scenario: Evidence fields are read from native records

- **GIVEN** a JSON or YAML evidence record's result is projected
- **WHEN** that native result changes
- **THEN** the target is stale until regenerated from that record

### Requirement: Invalid input is not a pass

Projection SHALL reject missing sources or fields, invalid or duplicate marker
pairs and paths escaping the repository, including symlinks. It SHALL validate
all declared fact projections before any projection write and report invalid
input with exit 2. Targets SHALL NOT also be sources.

Source: inferred by agent from AES-POL-002, source-local authority and the read-only untrusted-tree boundary.

#### Scenario: Invalid projection input fails before writing

- **GIVEN** a missing field/source/marker, duplicate marker or escaping path
- **WHEN** generation or checking is requested
- **THEN** it exits 2, names the problem and leaves every target unchanged

### Requirement: Installed edit and merge paths maintain facts

`lockstep refresh` SHALL refresh only declared source-local fact blocks without
regenerating requirement docstrings or coverage. `lockstep init` SHALL install
it as a PostToolUse hook for Claude Code and Codex while preserving existing
hooks. It SHALL include `lockstep check project --check` in the pre-commit
command so edits bypassing hooks are still checked. Refresh SHALL append one
trace per run to a daily projection log with source/target hashes and rewritten
paths. No declarations SHALL be a no-op.

Source: Brian, 2026-11-12, "ther should be hooks and stuff that automatically keep this all up to date", followed by "ok proceed"; AES-CTX-004.

#### Scenario: Refresh only updates declared facts

- **GIVEN** a consumer with declared fact blocks and a docs directory
- **WHEN** refresh runs
- **THEN** only those blocks change and no empty coverage page is created

#### Scenario: Installed post edit hook refreshes and precommit rejects stale

- **GIVEN** fresh initialization for each supported native client
- **WHEN** the installed refresh command receives a source edit event
- **THEN** it updates the target; a source edit bypassing the hook fails the read-only freshness check
