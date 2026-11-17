## ADDED Requirements

### Requirement: Notices route by who must act

`scripts/operator_notify_router.py` SHALL record every notice in `notifications.jsonl` before any delivery and then
attempt the routes of its severity: `info` none, `agent` a keyed concern, `attention` and `urgent` an ntfy push checked
at the broker, `needs-human` a desktop toast, a Telegram message and a concern labelled with the waiting label. A
`needs-human` notice SHALL be refused unless its title and action pass the wording check, SHALL count as delivered only
when Telegram accepted it, and SHALL be sent once per state of its key until the key is resolved.

Source: Brian, 2026-10-06 ("these should go to an autonomous agent to fix unless my input is actually needed"; Project
Meta issue #1958), carried over unchanged from Project Meta `ee2957b1f`.

#### Scenario: routes-by-severity

- **WHEN** a `needs-human` notice with an allowed title and action is sent twice with the same state
- **THEN** the toast, Telegram and concern routes are attempted the first time only, and both notices are in the record

### Requirement: The concern repository comes from the settings

The router SHALL file concerns in the repository named by `OPERATOR_CONCERN_REPO`, else by `concern_repo:` under
`operator_notify:` in `graph-config.yaml` beside the project graph. With neither, the concern route SHALL fail with a
reason naming both, and SHALL NOT fall back to any built-in repository. The Telegram token, chat id and ntfy topic
SHALL NOT be read from that settings file.

Source: inferred by agent, from the AES consolidation plan row 11 and the aes-config split (Brian, 2026-11-16, "i approve
d20 and d21": the machinery is public, his settings are private).

#### Scenario: concern-repository-comes-from-the-settings

- **WHEN** the settings name `concern_repo` and a `needs-human` concern is filed
- **THEN** it is created in that repository with the configured waiting label
- **AND WHEN** no repository is named anywhere
- **THEN** the concern route reports not delivered with the reason and no `gh` call is made

### Requirement: An open legacy concern is not duplicated

While a repository listed in `legacy_concern_repos:` holds an open concern for a key (the `concern:feedback` label and
the hidden `concern-key` marker, as `concern_issue.find_existing` reads them), the router SHALL update or close that
concern there instead of using the concern repository. A closed or missing legacy concern SHALL NOT be reopened by the
router; the concern is filed in the concern repository.

Source: inferred by agent: Project Meta #2713 (key `usage-pace`, `waiting:brian`) was open when the router moved, and
moving it would change its `repo#number`, which the waiting-issue push treats as a new issue for Brian.

#### Scenario: an-open-legacy-concern-is-not-duplicated

- **WHEN** a legacy repository holds an open concern for the key and the router files or resolves that key
- **THEN** the legacy concern is commented on or closed and nothing is created in the concern repository
