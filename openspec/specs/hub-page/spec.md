# hub-page Specification

## Purpose

One page, built inside AES, whose top section lists only what the owner must do or decide, then what changed, then a link to each source page (AES consolidation plan, item 10: "The hourly front page as the one hub inside AES, 'Needs you' on top"). The machinery is public in AES; what the page lists (issue titles, failed services, approvals) is the owner's private record, so the page is pushed only to a data branch of a private repository that the private plan site serves behind the owner's login, and every private value (repository, branch, address, labels, data file, links) is a setting in the private configuration repository. This first slice sits beside the existing front page and does not replace it.

Source: inferred by agent (AES consolidation plan item 10 and the harness grid review of 2026-11-16, Human interface row `new/front-page`: "Port to AES as the one hub; cut run cost"; the decision to put "Needs you" on top is recorded there as approved on 2026-11-05/06, not re-read here). Also inferred by agent: reading AES's `owner:brian` label because AES has no `needs-human` label. What Needs you holds (only what the owner must decide or do, listed once; broken services, records updates and the approvals count outside it) is Brian's, 2026-11-16 ("i approve 7 tight") and 2026-11-17 (the hub-page brief).

## Requirements

### Requirement: needs-you-comes-first

`scripts/hub_page.py` SHALL put the "Needs you" section first. It SHALL hold only what the owner must decide or do, each listed once: the open issues labelled `waiting_label` in the configured owners' repositories and the open issues in `concern_repo` labelled `needs_human_label`, less the waiting issues that a quiet label, an FYI rule or Broken services takes. An issue carrying a label under `quiet_issue_labels` SHALL be shown with its reason and not counted. Issues SHALL be sorted by labels, fixed title prefixes and links only, never by reading what the words mean. Every colour SHALL come with a word, using blue, orange and grey only, and the page SHALL be readable at phone width. The page SHALL say how often it is rebuilt (the `refresh` setting), or that it is rebuilt only when someone runs it.

Source: Brian, 2026-11-16 ("i approve 7 tight": only significant items go to him) and 2026-11-17 (the hub-page brief: he does not want to decide high-confidence or low-significance items; AES #926, #927)

#### Scenario: needs-you-comes-first

- **WHEN** the sources hold one waiting decision, a records ask with no FYI rule, records notices, a failing unit's own issue, a shared cause's issue, an issue with a quiet label and one AES concern
- **THEN** Needs you is the first section and counts 3 (the decision, the records ask and the concern), and names the quiet issue with its reason

### Requirement: an-unread-source-is-not-checked

A source that cannot be read, or a label that does not exist in `concern_repo`, SHALL be shown as "Not checked" with the reason, never as none or 0.

Source: inferred by agent (the old front page's rule front-page/a-source-that-cannot-be-read-is-not-checked)

#### Scenario: an-unread-source-is-not-checked

- **WHEN** systemctl or the issue search fails, or the needs-human label is missing
- **THEN** that group shows "Not checked" and the heading says how many sources were not checked

### Requirement: what-changed-since-the-last-run

"What changed" SHALL name the items under Needs you and Broken services that are new and those cleared since the previous run's `hub.json` on the data branch, comparing every section so an item that only moved section is neither, skipping any item whose source was not read on either run, and SHALL list the pull requests merged into `concern_repo` in the last day.

Source: inferred by agent (basis in Purpose above); the cross-section comparison follows Brian, 2026-11-17 (the hub-page brief)

#### Scenario: what-changed-since-the-last-run

- **WHEN** a failed unit appeared and another went away since the last run, or the previous run listed records notices and failed units under Needs you
- **THEN** the first is listed as new and the second as cleared; items that only moved section are neither; an unread source clears nothing

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

### Requirement: broken-services-grouped-by-cause

Failed systemd user units, except those under `quiet_units`, SHALL be shown in a "Broken services" section after Needs you and not counted in it. Units and issues that a `shared_causes` entry names SHALL be grouped under that cause, shown only when one of them is present; every other unit SHALL be its own cause with the reason and start date from the failing-jobs page (`failures_file`), or a statement that the reason was not checked. A waiting issue that is a failing unit's own issue (the failing-jobs page's `issue_url`) or that a shown cause names SHALL be listed there once and not under Needs you.

Source: Brian, 2026-11-17 (the hub-page brief: "failed services move to their own section 'Broken services' with the root cause grouped ... and NOT counted in Needs you"; "fix the duplicate counting ... by listing once")

#### Scenario: broken-services-grouped-by-cause

- **WHEN** three units fail, two of them named by one shared cause with an issue, the third with its own issue, and a quiet unit fails
- **THEN** Broken services says 3 services, 2 causes; each issue appears once on the page; the quiet unit is shown with its reason

### Requirement: records-updates-are-for-information

A waiting issue that carries the label of an `fyi_rules` entry and whose title starts with that entry's prefix SHALL be shown under "FYI: records updates", grouped by rule, label and repository, with the rule stated on the page, and not counted under Needs you.

Source: Brian, 2026-11-17 (the hub-page brief: exclude records status notices "by a label or explicit title rule in config, not regex on prose meaning")

#### Scenario: records-updates-are-for-information

- **WHEN** three issues carry the records label with the prefix, in two repositories, and a fourth records issue has another label
- **THEN** FYI lists 3 in two groups and the fourth stays under Needs you

### Requirement: approvals-are-a-footer-count

The requirements an agent inferred, read from `approvals_file`, SHALL be shown only as a count in the page footer, with the date of the data, the words "Not shown: no significance field", and a link to the oversight page; none SHALL be listed under Needs you while the data has no field marking which are significant.

Source: Brian, 2026-11-17 (the hub-page brief: approvals "only the significant ones ... if the data has a significance marker; otherwise show 'not shown: no significance field' and the total as a count in a footer")

#### Scenario: approvals-are-a-footer-count

- **WHEN** the oversight data holds an inferred requirement in two checkouts
- **THEN** the footer counts 1, says no significance field, and no approval is listed

### Requirement: moved-issues-are-matched-by-concern-key

The hub SHALL read each waiting issue's concern key from the `<!-- concern-key: K -->` marker in its body, and SHALL treat it as equivalent to a label or issue reference: an issue whose key is under `quiet_concern_keys` is quiet; an `fyi_rules` entry matches an issue whose key starts with its `concern_key_prefix` (with its title prefix); a `shared_causes` entry gathers issues whose key it lists under `concern_keys`; a failing unit's own issue is also the one whose key is `failed-unit:<unit>`.

Source: Brian, 2026-11-17 (the hub-page brief); the key replaces labels and numbers that a move between repositories drops (observed 2026-11-17, project-meta to code2-workspace)

#### Scenario: moved-issues-are-matched-by-concern-key

- **WHEN** the waiting issues have moved to another repository with no labels, each with its concern key
- **THEN** the records notice is FYI, the usage issue is quiet, the unit's issue and the credit issue are under Broken services, and the records ask with no title prefix stays under Needs you
