## MODIFIED Requirements

### Requirement: needs-you-comes-first

`scripts/hub_page.py` SHALL put the "Needs you" section first. It SHALL hold only what the owner must decide or do, each listed once: the open issues labelled `waiting_label` in the configured owners' repositories and the open issues in `concern_repo` labelled `needs_human_label`, less the waiting issues that a quiet label, an FYI rule or Broken services takes. An issue carrying a label under `quiet_issue_labels` SHALL be shown with its reason and not counted. Issues SHALL be sorted by labels, fixed title prefixes and links only, never by reading what the words mean. Every colour SHALL come with a word, using blue, orange and grey only, and the page SHALL be readable at phone width. The page SHALL say how often it is rebuilt (the `refresh` setting), or that it is rebuilt only when someone runs it.

Source: Brian, 2026-11-16 ("i approve 7 tight": only significant items go to him) and 2026-11-17 (the hub-page brief: he does not want to decide high-confidence or low-significance items; AES #926, #927)

#### Scenario: needs-you-comes-first

- **WHEN** the sources hold one waiting decision, a records ask with no FYI rule, records notices, a failing unit's own issue, a shared cause's issue, an issue with a quiet label and one AES concern
- **THEN** Needs you is the first section and counts 3 (the decision, the records ask and the concern), and names the quiet issue with its reason

### Requirement: what-changed-since-the-last-run

"What changed" SHALL name the items under Needs you and Broken services that are new and those cleared since the previous run's `hub.json` on the data branch, comparing every section so an item that only moved section is neither, skipping any item whose source was not read on either run, and SHALL list the pull requests merged into `concern_repo` in the last day.

Source: inferred by agent (basis in Purpose above); the cross-section comparison follows Brian, 2026-11-17 (the hub-page brief)

#### Scenario: what-changed-since-the-last-run

- **WHEN** a failed unit appeared and another went away since the last run, or the previous run listed records notices and failed units under Needs you
- **THEN** the first is listed as new and the second as cleared; items that only moved section are neither; an unread source clears nothing

## ADDED Requirements

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
