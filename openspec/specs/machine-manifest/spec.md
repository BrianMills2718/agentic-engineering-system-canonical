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

`check` SHALL rebuild the manifest in memory, list every `local-only` file, print the count, and exit 1 when there is any. A `local-only` file whose copy in the units repository (`--units-repo`, default as `check-units`) is byte-identical, and a link to `/dev/null` (a mask) whose recorded `NAME.symlink` target is also `/dev/null`, SHALL instead be listed and counted under "(e) local-only files and links with an identical copy in the units repository", which does not fail the check. A file with no copy or a differing copy, a link whose recorded target differs, a link to any other file outside git (its record restores the link, not the file), and every file when the units repository folder does not exist, SHALL be reported and fail as before.

Source: inferred by agent, from the AES consolidation plan row 11 ("Before item 11", step 7: `check` and `check-units` exit 0) and item 6 slice 2 (the units repository restores these files).

#### Scenario: local-only-units-are-reported

- **WHEN** a unit or drop-in file is a regular file not generated from the job list
- **THEN** `check` names it under "local-only files, lost on a clean machine" and exits 1

#### Scenario: identical-copies-do-not-fail

- **WHEN** every local-only file has a byte-identical copy in the units repository and a `/dev/null` link has a matching `.symlink` record
- **THEN** `check` lists them under (e), reports (a) and (b) as 0 and exits 0; removing or changing one copy, changing the recorded link target, or pointing at a missing units repository makes it exit 1

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

### Requirement: repository-copies-can-be-compared

`check-units` SHALL compare each file under the units repository folder (default `~/code2/aes-config/machine-units`, laid out as the unit folder is) with the same path in the unit folder, print counts of same, differ, missing and under-a-symlink files and of recorded symlinks (a `NAME.symlink` file holds the link target text), list the differing ones, and exit 1 when any file or recorded symlink differs. Missing files do not fail it: a clean machine is expected to lack them. It changes nothing.

#### Scenario: repository-copies-can-be-compared

- **WHEN** the disk has one identical, one differing and one absent copy of repository files
- **THEN** `check-units` prints one of each in its counts and exits 1; once the differing file matches it exits 0

### Requirement: install-never-deletes-or-writes-through-links

`install-units` SHALL be a dry run unless `--apply` is given, printing what it would install or replace. With `--apply` it SHALL copy only files that are missing or differ, first copying each differing disk file to `~/archive/systemd-units-replaced/<path>-<date>/`; it SHALL never delete a file and SHALL skip, and report, any destination that is a symlink or sits under one. It SHALL run `systemctl --user daemon-reload` only when `--daemon-reload` is also given.

#### Scenario: install-never-deletes-or-writes-through-links

- **WHEN** `install-units` runs without `--apply`, then with it, on a folder holding a differing file, a missing file, a file only on disk and a drop-in folder that is a symlink
- **THEN** the first run writes nothing; the second backs up and replaces the differing file, installs the missing one, leaves the disk-only file and the symlinked folder untouched
