# required-evidence-inputs Specification

## Purpose

Keep historical observations from claiming current support when a consumer explicitly requires subprocess inputs those observations did not declare.

Source: Brian's active Lockstep completion goal, 2026-11-07; narrow retained-engine integration, with the former universal self-governance program still on hold.

## Requirements

### Requirement: Required declared input coverage

The evidence and reconciliation library APIs SHALL accept an optional mapping from existing verification-subject ids to literal repository-relative required file or directory paths. Omitting the mapping SHALL preserve current behavior. When ordinary freshness is CURRENT but applicable required paths lack recorded declared coverage, the observation SHALL be UNKNOWN and SHALL NOT support or refute criterion standing. Its original record and assessments SHALL remain unchanged. Existing revision, target-entry, supersession and qualified-refutation rules SHALL remain authoritative.

#### Scenario: weak-history-cannot-mask-staleness

- **WHEN** a weak subprocess observation omits a required source directory, a correctly declared observation is later recorded, and that source changes again
- **THEN** the old weak observation is UNKNOWN, the correctly declared observation is STALE, and neither supplies current support

#### Scenario: refutation-is-retained

- **WHEN** a current refuting observation declares all required inputs
- **THEN** it remains CURRENT and its assessment still refutes the requirement

#### Scenario: legacy-route-inference

- **WHEN** a legacy observation names a criterion instead of a verification subject
- **THEN** applicable configured subjects are inferred through assessed evidence requirements and its recorded dependency paths supply the legacy coverage fallback

### Requirement: Literal repository path coverage

Required-input qualification SHALL normalize lexical path components, permit a declared directory to cover descendant inputs, and reject unsafe, absolute, traversal, wildcard and repository-escaping paths. A child file SHALL NOT cover its ancestor directory. For observations with a dependency basis, explicit declared dependencies SHALL supply coverage; discovered imports SHALL NOT substitute for required declarations. Legacy observations without a dependency basis SHALL use their recorded dependency paths.

#### Scenario: unsafe-paths-fail

- **WHEN** a required path is unsafe or escapes the repository through a symlink
- **THEN** qualification fails with an evidence error instead of accepting or silently ignoring it
