## MODIFIED Requirements

### Requirement: Arch: Code imports match the diagram

`lockstep check arch check`, when the committed contracts file matches the diagram, SHALL run the contracts against the code with import-linter and exit 1 when any contract is broken, printing the broken contract and the importing module. When import-linter is not installed it SHALL print that and exit 1; it SHALL NOT pass. When the diagram maps no Python packages there is nothing to check, and it SHALL pass without running import-linter.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: Arch: An import the diagram forbids is refused

- **GIVEN** a current contracts file forbidding `app.detect` to import `app.cli`
- **WHEN** `app.detect` imports `app.cli` and the check runs
- **THEN** the check exits 1 and its output names the broken contract and `app.detect`

#### Scenario: Arch: Missing import-linter fails loudly

- **GIVEN** a current contracts file and no `lint-imports` command
- **WHEN** the check runs
- **THEN** it prints that import-linter is not installed and exits 1

#### Scenario: Arch: A diagram that maps no packages passes

- **GIVEN** a diagram whose elements map no Python packages
- **WHEN** the check runs
- **THEN** it passes without running import-linter

### Requirement: Trace: A marked quote matches its requirement

The trace check SHALL read, in every Markdown file tracked by git outside `openspec/`, each passage between `<!-- lockstep quote: <requirement id> -->` and `<!-- /lockstep quote -->`. It SHALL report `stale-quote` and fail when the passage, with runs of whitespace counting as one space, does not appear in the text of that requirement or of one of its scenarios, in `openspec/specs/` or in an active change's spec delta. It SHALL report `unknown` when no spec or active change defines the ID, and `unclosed-quote` when a start marker has no end marker after it in the same file. Each finding SHALL name the file and line of the start marker. A marker inside a code span or a fenced code block is shown as code, not used as a marker, and SHALL be skipped; a passage SHALL be compared with its code words kept. In a folder that is not a git repository it SHALL read every Markdown file outside `openspec/` and folders whose name starts with a dot.

Source: Brian, 2026-10-22: "this doc string linkage system where the normative and docs tring stuff and gaps and planns would stay algined over time" (code2-workspace decision 0006); Brian, 2026-11-17: "if there is a change in the nromative docuemtnation ..." (code2-workspace issue 842, where seven hand-typed copies of one requirement's number stayed unchanged after the requirement changed). The marker form is inferred by agent.

#### Scenario: Trace: A quote that matches passes

- **GIVEN** a Markdown file with a marked passage that appears word for word in its requirement's statement
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

#### Scenario: Trace: A quote left behind by a changed requirement fails

- **GIVEN** the same file after the requirement's statement changed so that the passage no longer appears in it
- **WHEN** the trace check runs
- **THEN** it reports `stale-quote` with the file and line, and exits 1

#### Scenario: Trace: A quote of a scenario's text passes

- **GIVEN** a marked passage that appears in the text of one of the requirement's scenarios
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

#### Scenario: Trace: A quote of an unknown requirement fails

- **GIVEN** a marked passage naming an ID no spec defines
- **WHEN** the trace check runs
- **THEN** it reports `unknown` for the passage and exits 1

#### Scenario: Trace: A quote matching an active change's text passes

- **GIVEN** a marked passage that appears only in an active change's spec delta for that requirement
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage

#### Scenario: Trace: A start marker with no end marker fails

- **GIVEN** a Markdown file with a start marker and no end marker after it
- **WHEN** the trace check runs
- **THEN** it reports `unclosed-quote` with the file and line, and exits 1

#### Scenario: Trace: A marker written as code is not a quote

- **GIVEN** a Markdown file that shows the marker inside backticks and inside a fenced block
- **WHEN** the trace check runs
- **THEN** it reports no finding for those lines

#### Scenario: Trace: A quoted passage keeps its code words

- **GIVEN** a marked passage containing a backticked command that appears in its requirement's statement
- **WHEN** the trace check runs
- **THEN** it reports no finding for the passage
