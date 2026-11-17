# failed-unit-watch Specification

## Purpose

Every 30 minutes, find systemd user units that failed (or whose last run failed), file one keyed concern issue per unit in the repository that owns the unit's script, and close it when the unit is healthy. Also sweeps Healthchecks.io checks. The owner and fallback concern repository are configuration, not code.

Source: inferred by agent from Project Meta's `scripts/failed_unit_watch.py`, ported under Brian's 2026-11-16 "do all the steps" and D21 yes (timers become a job list; port failed-unit-watch).

## Requirements

### Requirement: settings-come-from-config

The owner and the fallback concern repository SHALL come from the environment or from `graph-config.yaml` beside the project graph, and a missing value SHALL stop the run with a message naming where to set it.

#### Scenario: settings-come-from-config

- **WHEN** neither the environment nor `graph-config.yaml` names an owner
- **THEN** the script exits with "no owner named" and files nothing

### Requirement: issue-body-carries-one-line-not-the-log

A concern body for a failed unit or a down Healthchecks.io check SHALL carry one line from the unit's journal, the newest
entry the job itself printed (its `SYSLOG_IDENTIFIER` is not `systemd`), or systemd's own newest entry when the job printed
nothing, with no host name or process id, passed through `public_text.redact`; and the command that shows the full log on
the machine that ran it. It SHALL NOT carry a block of journal lines.

Source: Brian, 2026-11-17: "make AES's own public issue bodies carry only the first error line and a pointer to the private log path ... and redact home paths/addresses."

#### Scenario: issue-body-carries-one-line-not-the-log

- **WHEN** a unit's journal holds systemd's start line, the job's line `could not read the Windows user name` and systemd's failure lines
- **THEN** the body holds `could not read the Windows user name` and `journalctl --user -u <unit>`, and neither systemd's lines nor the host name

### Requirement: ssh-host-alias-remotes-find-their-repository

`repo_from_remote` SHALL read the owner and repository from an SSH remote whose host is `github.com-<alias>` as well as
`github-<alias>` and `github.com`.

Source: inferred by agent: `brent-fdot-feed.service` runs from a checkout whose remote is `git@github.com-personal:BrianMills2718/brent-chatgpt.git` and its concern went to the fallback repository (AES #945, 2026-11-17).

#### Scenario: ssh-host-alias-remotes-find-their-repository

- **WHEN** the remote is `git@github.com-personal:BrianMills2718/brent-chatgpt.git`
- **THEN** the repository is `BrianMills2718/brent-chatgpt`
