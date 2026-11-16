# concern-repair-verifier Specification

## Purpose

Close a repair of a feedback concern only when the repair is proved, never on the repairing agent's own report, so a patch that would not catch the next recurrence cannot close the concern (retirement plan, slice 3).

Source: Brian, 2026-11-16, "no we arent waiting. wha else can we do of value?" (instruction to continue the retirement plan with its next slice). Inferred by agent: the verifier is copied from Project Meta unchanged apart from names (repository, project id, trace names); the repair launcher (`concern_repair_executor.py`) is not ported because it depends on the retired claims system.

## Requirements

### Requirement: Closure needs all five gates, judged by the verifier

The verifier SHALL pass a repair only when all five gates pass: the committed report validates and matches the executor binding; every declared prevention path changed in the diff; the recurrence proof fails on the observed revision (with only its declared harness files copied in) and passes on the fix; the concern's own source signal is green; and an independent reviewer judges the diff a root-cause fix. It SHALL NOT run the reviewer when a mechanical gate failed.

#### Scenario: five-gates-pass-root-cause-fix

- **WHEN** a repair has a valid report, changed prevention paths, a proof that fails before and passes after, a green source signal and a reviewer verdict of root cause fixed
- **THEN** the verification record passes and names the other client as reviewer

#### Scenario: patch-is-rejected

- **WHEN** the proof passes on the observed revision, fails on the fix, the prevention path is unchanged, the source signal is unresolved, or the reviewer judges a patch only
- **THEN** the verification record fails, naming the failed gate

### Requirement: A recurrence proof that cannot fail does not count

The recurrence proof SHALL fail closed: when its harness files are missing, when the control is the fix itself, or when it cannot be executed, the gate fails.

#### Scenario: proof-fails-closed

- **WHEN** the declared harness path does not exist in the fix revision, or the proof also passes on the observed revision
- **THEN** the recurrence gate fails with the reason in its detail
