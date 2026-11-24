## ADDED Requirements

### Requirement: Suppressions: An added suppression comment names its reason

`lockstep check suppressions --base <rev>` SHALL read the lines added between where the branch started (as for the
changed check) and the working tree in tracked `.py` files, and report each added line holding `# noqa`,
`# type: ignore`, `# pyright: ignore` or `# pylint: disable` that is not followed, later on the same line, by a
further `#` comment of at least three words, printing `unreasoned <path>:<line> <directive>`. Lines present at the
base SHALL never be reported.

Source: Brian, 2026-11-24: "i approve adding the redit ideas to the plan and i will trust your jdugement on the
impelemtnation prirotiy" (this session; plan in `.project-brain/now.md`). The reason format and the three-word
minimum are inferred by agent: mypy rejects `# type: ignore[x] -- reason` and accepts a further `#` comment.

#### Scenario: Suppressions: An added noqa with no reason fails

- **GIVEN** a branch that adds the line `import os  # noqa: F401` to a tracked Python file
- **WHEN** `lockstep check suppressions --base main` runs
- **THEN** it prints `unreasoned` with that file and line and exits 1

#### Scenario: Suppressions: A reason after the directive passes

- **GIVEN** a branch that adds `import os  # noqa: F401  # re-exported for the plugin loader` and `x = f()  # type: ignore[no-untyped-call]  # vendored stub has no types`
- **WHEN** `lockstep check suppressions --base main` runs
- **THEN** it reports neither line and exits 0

#### Scenario: Suppressions: A suppression already at the base is not judged

- **GIVEN** a file that holds `import os  # noqa: F401` at the base and a branch that changes a different line of it
- **WHEN** `lockstep check suppressions --base main` runs
- **THEN** it reports nothing and exits 0

### Requirement: Suppressions: An added import-linter ignore names its reason

The suppressions check SHALL report each entry added to an import-linter `ignore_imports` list with no reason,
printing `unreasoned <path>:<line> ignore_imports`. In `.importlinter` and `setup.cfg` the reason SHALL be a `#` or `;`
comment line of at least three words directly above the entry; in `pyproject.toml` it SHALL be a `#` comment of at
least three words on the entry's line.

Source: as the requirement above (Brian, 2026-11-24). Inferred by agent: import-linter reads `.importlinter` with
configparser, which strips a full-line comment and keeps an inline `#` as part of the value.

#### Scenario: Suppressions: An INI ignore needs a comment line above it

- **GIVEN** a branch that adds two entries under `ignore_imports` in `.importlinter`, one directly below `# the CLI wires the adapter in` and one with no comment above it
- **WHEN** `lockstep check suppressions --base main` runs
- **THEN** it reports only the entry with no comment above it and exits 1

### Requirement: Suppressions: Count line and exit status

The suppressions check SHALL end with `RESULT suppressions added=<n> reasoned=<n> unreasoned=<n> exit=<0|1>`,
counting added suppressions, and exit 1 when `unreasoned` is above zero. When `<rev>` names no commit it SHALL
check nothing, print `RESULT suppressions skipped="base <rev> not found" exit=0` and exit 0.

Source: as the requirements above (Brian, 2026-11-24); the line shape follows the changed check's.

#### Scenario: Suppressions: A base that names no commit skips

- **GIVEN** a repository with no revision named `nope`
- **WHEN** `lockstep check suppressions --base nope` runs
- **THEN** it prints `RESULT suppressions skipped="base nope not found" exit=0` and exits 0
