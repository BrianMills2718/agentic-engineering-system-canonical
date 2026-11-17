# hub-page Specification

## Purpose

One page, built inside AES, whose top section lists only what the owner must do or decide, then what changed, then a link to each source page (AES consolidation plan, item 10: "The hourly front page as the one hub inside AES, 'Needs you' on top"). The machinery is public in AES; what the page lists (issue titles, failed services, approvals) is the owner's private record, so the page is pushed only to a data branch of a private repository that the private plan site serves behind the owner's login, and every private value (repository, branch, address, labels, data file, links) is a setting in the private configuration repository. This first slice sits beside the existing front page and does not replace it.

Source: inferred by agent (AES consolidation plan item 10 and the harness grid review of 2026-11-16, Human interface row `new/front-page`: "Port to AES as the one hub; cut run cost"; the decision to put "Needs you" on top is recorded there as approved on 2026-11-05/06, not re-read here). Also inferred by agent: showing the inferred approvals as a count rather than as items to act on (163 on 2026-11-17, most not significant under Brian's 2026-11-16 "i approve 7 tight"), and reading AES's `owner:brian` label because AES has no `needs-human` label.

## Requirements

### Requirement: needs-you-comes-first

`scripts/hub_page.py` SHALL put the "Needs you" section first. It SHALL list every open issue labelled `waiting_label` in the configured owners' repositories, every failed systemd user unit except those named under `quiet_units` (which are shown below the list with their reason and not counted), and every open issue in `concern_repo` labelled `needs_human_label`; and SHALL show the requirements an agent inferred, read from `approvals_file`, as a separate count with its date and a short list, not counted in the Needs-you total. Every colour SHALL come with a word, using blue, orange and grey only, and the page SHALL be readable at phone width. The page SHALL say how often it is rebuilt (the `refresh` setting), or that it is rebuilt only when someone runs it.

Source: inferred by agent (basis in Purpose above)

#### Scenario: needs-you-comes-first

- **WHEN** the sources hold one waiting decision, two failed units of which one is quiet, one AES concern and an inferred approval listed in two checkouts
- **THEN** Needs you is the first section, counts 3, names the quiet unit with its reason, and counts the approval once

### Requirement: an-unread-source-is-not-checked

A source that cannot be read, or a label that does not exist in `concern_repo`, SHALL be shown as "Not checked" with the reason, never as none or 0.

Source: inferred by agent (the old front page's rule front-page/a-source-that-cannot-be-read-is-not-checked)

#### Scenario: an-unread-source-is-not-checked

- **WHEN** systemctl or the issue search fails, or the needs-human label is missing
- **THEN** that group shows "Not checked" and the heading says how many sources were not checked

### Requirement: what-changed-since-the-last-run

"What changed" SHALL name the Needs-you items that are new and those cleared since the previous run's `hub.json` on the data branch, skipping any group whose source was not read on either run, and SHALL list the pull requests merged into `concern_repo` in the last day.

Source: inferred by agent (basis in Purpose above)

#### Scenario: what-changed-since-the-last-run

- **WHEN** a failed unit appeared and another went away since the last run
- **THEN** the first is listed as new and the second as cleared; an unread source clears nothing

### Requirement: links-to-each-source-page

The page SHALL link every page listed under `links`, each with what it shows.

Source: inferred by agent (basis in Purpose above)

#### Scenario: links-to-each-source-page

- **WHEN** the settings list source pages
- **THEN** each one is linked from the page

### Requirement: page-goes-to-a-private-data-branch

The page and `hub.json` SHALL be committed only to `data_branch` of `repo` (never main, never AES), through the configured SSH alias; a missing setting SHALL stop the run with exit 2. Each run SHALL append every command with its exit status and time to one log per day.

Source: inferred by agent (basis in Purpose above; publish route of project-graph-refresh/page-goes-to-data-branch)

#### Scenario: page-goes-to-a-private-data-branch

- **WHEN** the page changed
- **THEN** the push names only the data branch, and settings without `repo` stop the run
