# inert-characterization Specification

## Purpose

Keep retained read-only structural inspection and producer identification independent of executable repository Git integrations.

## Requirements

### Requirement: Git inspection is inert

Source: inferred by agent from Brian's active Lockstep goal requiring structural inspection without executing inspected code, and the reproduced local fsmonitor command, 2026-11-08.

Read-only characterization and source-checkout producer identification SHALL disable repository Git hooks and fsmonitor commands. They SHALL preserve committed revision binding, accurate dirty state and static source facts without executing the inspected repository's integrations.

#### Scenario: Local monitor during characterization

- **GIVEN** a committed project whose local Git configuration names a monitor command
- **WHEN** its files are characterized
- **THEN** the monitor is not invoked and facts retain their actual revision and dirty state

#### Scenario: Local monitor during producer identity

- **GIVEN** a tracked source checkout whose local Git configuration names a monitor command
- **WHEN** the running producer's checkout revision is identified
- **THEN** the monitor is not invoked and the actual checkout identity is retained
