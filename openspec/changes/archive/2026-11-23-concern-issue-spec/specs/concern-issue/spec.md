## ADDED Requirements

### Requirement: An open concern's title follows the repository's current status

`scripts/concern_issue.py open` SHALL give an existing issue for the key the title it was called with
whenever the two differ (`gh issue edit --title`), whether it comments on the open issue, finds the
occurrence already recorded, or reopens a closed issue, and SHALL create no second issue for the key.
Because the compliance list passes `Planning package <status>` on every run, a repository's
`planning-compliance` issue SHALL carry its current status in its title, and a repository SHALL have
one such issue, not one per status. A failed edit SHALL fail the call.

Source: code2-workspace #93 (Brian's issue, 2026-11-05: "Concerns should be keyed by repository and
retitled to the current status"); the choice to retitle inside the shared adapter, so every caller gets it, is the
agent's. Copied from code2-workspace `openspec/specs/compliance-list/spec.md` for AES's copy of the script (Brian,
2026-11-23: "i approve", to Q52).

#### Scenario: An open concern's title follows the repository's current status

- **GIVEN** an open `planning-compliance` issue titled "Planning package error" and a repository the list now reads as out of date
- **WHEN** the concern is opened with the title "Planning package out of date"
- **THEN** the same issue is retitled and commented on, and no second issue is created

#### Scenario: A current title is left alone

- **GIVEN** an open issue already titled "Planning package out of date"
- **WHEN** the concern is opened with that title
- **THEN** the issue is commented on and not edited

#### Scenario: A reopened concern takes the current title

- **GIVEN** a closed issue titled "Planning package error"
- **WHEN** the concern is opened with the title "Planning package not compliant"
- **THEN** the issue is reopened and retitled

#### Scenario: An issue that already records the occurrence is still retitled

- **GIVEN** an open issue with the old title that already holds this occurrence
- **WHEN** the concern is opened with the same occurrence and a new title
- **THEN** the issue is retitled and not commented on again

#### Scenario: A failed retitle fails the call

- **GIVEN** an open issue with an old title and a `gh issue edit` that fails
- **WHEN** the concern is opened with a new title
- **THEN** the call raises
