# timer-config Specification

## Purpose

Keep every scheduled job as one entry in a person's own list, with the reason it exists, and generate the systemd unit files from the list, so a timer change is a recorded change and the same setup can be installed on another machine (retirement plan, step 6).

Source: Brian, 2026-11-16, "does it make snese to again make this a configuration thing that aes handles timers thorugh a configuration?" and "i apporve d20 and d21" (Decision 21 yes). Inferred by agent: the list format and the choice to write unit files directly and not manage drop-ins.

## Requirements

### Requirement: Each job in the list becomes a service and a timer unit

`scripts/timers.py` SHALL turn each job (name, description, reason, command, schedule) into a `<name>.service` and a `<name>.timer` file. It SHALL refuse a list in which a job has no reason or no command, a repeated or malformed name, or a key it does not know.

Source: Brian, 2026-11-16: "does it make snese to again make this a configuration thing that aes handles timers thorugh a configuration?" (this spec's Purpose; Decision 21; commit 0e0698283)

#### Scenario: jobs-become-units

- **WHEN** a list holds a job with a command and a schedule
- **THEN** the rendered service runs that command as a oneshot and the rendered timer carries that schedule

#### Scenario: incomplete-job-is-refused

- **WHEN** a job has no `why`, a duplicate name, or an unknown key
- **THEN** loading the list fails and names the job

### Requirement: Installing never deletes

`install` SHALL copy each installed file it replaces into a timestamped backup folder before writing, SHALL write only files whose content differs, and SHALL run `systemctl --user daemon-reload` after writing.

Source: inferred by agent (timer-config spec Purpose, commit 0e0698283, 2026-11-16; workspace rule against deleting without asking)

#### Scenario: install-backs-up-first

- **WHEN** an installed unit differs from the rendered one
- **THEN** the old file is in the backup folder, the new file is installed, and daemon-reload ran once

#### Scenario: install-never-writes-through-a-link

- **WHEN** an installed unit is a symbolic link to a file in some repository
- **THEN** the link's target text and the file's content are in the backup folder, the link itself is replaced by a regular file, and the file the link pointed at is unchanged
