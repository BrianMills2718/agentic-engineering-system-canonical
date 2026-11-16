# machine-manifest Specification

## Purpose

List every systemd user unit on a machine with where its file comes from (a git repository, the AES job list, or only this disk), its schedule, the script it runs and whether it is enabled, so a clean machine can be rebuilt without losing jobs, and say which units would be lost (AES consolidation plan, item 6). The machinery is public in AES; the manifest itself names a person's jobs and paths and lives in their private configuration repository.

Source: inferred by agent from the AES consolidation plan item 6, approved by Brian 2026-11-16 (Decision 25 A). Inferred by agent: the file layout of the manifest, covering `.path`, `.socket` and `.slice` units and `*.timer.d` drop-ins beside the timers and services the plan names, and counting a symlink to an uncommitted change as a finding.

## Requirements

### Requirement: every-unit-has-a-source

`scripts/machine_manifest.py build` SHALL write one entry per unit name, sorted by name, covering every `*.timer`, `*.service`, `*.path`, `*.socket` and `*.slice` file and every `*.d/*.conf` drop-in in the unit folder. Each file SHALL carry a source: for a symlink, the target's repository (`owner/name` from its origin remote, or `no-remote`), its path inside the repository and whether it is tracked and committed; for a file `scripts/timers.py` generated, `job-list` with the job name; otherwise `local-only`. Enabled state SHALL be read with `systemctl --user is-enabled`; the script changes nothing on the machine.

#### Scenario: every-unit-has-a-source

- **WHEN** the unit folder holds a symlink into a git repository, a generated job, a regular file and drop-ins
- **THEN** every file in the manifest has a source of the matching kind, and a timer drop-in's schedule override is reflected

### Requirement: local-only-units-are-reported

`check` SHALL rebuild the manifest in memory, list every `local-only` file, print the count, and exit 1 when there is any.

#### Scenario: local-only-units-are-reported

- **WHEN** a unit or drop-in file is a regular file not generated from the job list
- **THEN** `check` names it under "local-only files, lost on a clean machine" and exits 1

### Requirement: missing-or-untracked-target-is-reported

`check` SHALL list each symlink whose target is missing, outside any git repository, not tracked, or changed and not committed; each file in the saved manifest that is no longer on disk; and each file on disk that the saved manifest lacks. It SHALL exit 1 when any list is non-empty and 0 when all are empty.

#### Scenario: missing-or-untracked-target-is-reported

- **WHEN** a symlink points at a missing file or a file git does not track, or the disk and the manifest differ
- **THEN** `check` names each one and exits 1; a folder with none of these exits 0

### Requirement: output-is-stable

The manifest SHALL carry no timestamp and SHALL list units and drop-ins in sorted order, so an unchanged machine produces the same bytes and a change shows as a small diff.

#### Scenario: output-is-stable

- **WHEN** `build` runs twice on an unchanged folder
- **THEN** the two outputs are identical and units are in name order

### Requirement: no-environment-values-are-written

The manifest SHALL record only how many `Environment=` and `EnvironmentFile=` lines a service and its drop-ins have, never their values or paths, and from `ExecStart` only the program and the script path, never other arguments.

#### Scenario: no-environment-values-are-written

- **WHEN** a service or drop-in sets a value through `Environment=`, `EnvironmentFile=` or a command argument
- **THEN** that value does not appear in the manifest, and the counts do
