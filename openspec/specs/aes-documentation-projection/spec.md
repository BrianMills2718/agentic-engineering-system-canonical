# aes-documentation-projection Specification

## Purpose

AES's narrow self-adoption of authored component assessments through declared
fact projection and a facts-only freshness gate, preserving existing policy.

## Requirements

### Requirement: AES projects its source-owned component assessment

AES SHALL project the real projection component's authored current assessment, gaps and linked plan from its module docstring into declared architecture and wiki blocks using the existing static fact projector. Evidence SHALL remain distinguishable from the assessment.

Source: Brian, 2026-11-13: “proceed” after the worked projection assessment.

#### Scenario: One source updates both views

- **GIVEN** the component docstring and both declared targets
- **WHEN** a native client edits the authored narrative and its post-edit refresh runs
- **THEN** both copies contain the new narrative and the trace identifies their source and changes

### Requirement: AES checks declared fact freshness without broad regeneration

AES's local check and pre-commit path SHALL reject stale declared fact copies without writing or regenerating unrelated requirement copies or coverage. Existing hook and commit configuration SHALL be preserved.

Source: inferred by agent from the accepted narrow self-adoption plan and existing repository policy.

#### Scenario: Bypassed refresh is refused

- **GIVEN** a source edit bypassed post-edit refresh
- **WHEN** the facts-only local gate runs
- **THEN** it exits nonzero naming stale targets and leaves them unchanged

#### Scenario: Explicit refresh recovers

- **GIVEN** stale declared copies
- **WHEN** existing refresh runs
- **THEN** both copies update and the same facts-only gate passes
