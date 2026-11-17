## ADDED Requirements

### Requirement: Trace: A marked quote matches its requirement

The trace check SHALL read, in every Markdown file tracked by git outside `openspec/`, each passage between `<!-- lockstep quote: <requirement id> -->` and `<!-- /lockstep quote -->`. It SHALL report `stale-quote` and fail when the passage, with runs of whitespace counting as one space, does not appear in the text of that requirement or of one of its scenarios, in `openspec/specs/` or in an active change's spec delta. It SHALL report `unknown` when no spec or active change defines the ID, and `unclosed-quote` when a start marker has no end marker after it in the same file. Each finding SHALL name the file and line of the start marker. In a folder that is not a git repository it SHALL read every Markdown file outside `openspec/` and folders whose name starts with a dot.

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

### Requirement: Changed: Documents that quote a listed requirement are listed with it

The changed check SHALL print, for each requirement it lists, every marked quote of it (`<!-- lockstep quote: <id> -->` in a tracked Markdown file outside `openspec/`) as `<path>:<line>` with the label `current` when the passage appears in the requirement's or its scenarios' current text and `stale` when it does not, and SHALL include them in its JSON output.

Source: Brian, 2026-11-17: "if there is a change in the nromative docuemtnation then that normative docuemtnation gets updated and then the gaps relevant to that normative docuemntation need to be replanned" (code2-workspace issue 842). Inferred by agent: that the list shows documents beside code and tests.

#### Scenario: Changed: A document quoting a changed requirement is listed as stale

- **GIVEN** a requirement whose statement differs from the base and a Markdown file with a marked quote of the old statement's words
- **WHEN** `lockstep check changed --base <rev>` runs
- **THEN** the requirement's block names the file and line with the label `stale`
