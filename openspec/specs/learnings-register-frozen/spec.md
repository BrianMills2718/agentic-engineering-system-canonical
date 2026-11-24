# learnings-register-frozen Specification

## Purpose

Keep Project Meta's old learnings register as a read-only record the feedback collector can still read, so Project Meta can be archived without a recurring failure looking new (retirement plan, Decision 18).

Source: Brian, 2026-11-16, "i approve A" (Decision 18: freeze the register). Inferred by agent: the frozen copy lives in the private repository `learnings-archive`, not in this public repository, because the publish-checker returned hold for the whole register (a live token, personal email addresses, Inside Success and personal material).

## Requirements

### Requirement: The collector reads the frozen copy and never writes to a register

The feedback collector SHALL read existing learnings only from the folder named by `LEARNINGS_REGISTER` (default `~/code2/learnings-archive/entries`). It SHALL NOT write to any learnings register: `file_item` SHALL fail, and `--legacy-register` SHALL be refused with a non-zero exit.

Source: Brian, 2026-11-16: "i approve A" (Decision 18: freeze the register; docs/planning/project-meta-retirement-plan.md row 2 and this spec's Purpose; commit 4e785b286)

#### Scenario: register-read-only

- **WHEN** the collector builds its repeat index and a caller tries `file_item` or `--legacy-register`
- **THEN** the index is built from the `LEARNINGS_REGISTER` folder, `file_item` raises, and `--legacy-register` exits non-zero before any work
