## ADDED Requirements

### Requirement: A citation may name the text it points at

Source: Brian, 2026-11-20: "start 1-2" (the first step: line citations in planning packages pass while the cited text has moved; `proposal.md` of this change).

A repository file cited in the acceptance file MAY be written `path#:~:text=<percent-encoded text>`, with an optional `prefix-,` before the text and `,-suffix` after it. `lockstep plan check` SHALL accept it only when the file exists and the text, with runs of whitespace counting as one space and the prefix and suffix if given, appears in the file exactly once. It SHALL exit 1 naming the citation when the text is not found, is found more than once, or the anchor is malformed (empty text, invalid percent-encoding, the range form `text,text`, or a directive other than `text=`); a malformed anchor SHALL NOT be skipped as a non-citation. A plain `path` or `path:line` citation SHALL behave as before.

#### Scenario: An anchored citation survives a line move

- **GIVEN** a router record whose cited text sits on a different line from where it was first written
- **WHEN** `lockstep plan check` runs on an entry citing it as `path#:~:text=...`
- **THEN** it exits 0

#### Scenario: An anchored citation whose text is gone fails

- **GIVEN** a cited file that no longer contains the quoted text
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and the line names the citation and says the text was not found

#### Scenario: Text found twice fails

- **GIVEN** a cited file where the quoted text appears twice and no prefix or suffix picks one
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and says the text matches 2 places

#### Scenario: A malformed anchor fails instead of being skipped

- **GIVEN** a citation `path#:~:text=` with no text
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and names the citation as malformed
