## ADDED Requirements

### Requirement: every-script-outside-git-has-a-record

The manifest SHALL carry a hand-written `scripts` list, one record per script a unit (or a Windows scheduled task) runs that is in no git repository, each with its original `path` and a `kind`: `copied` (a verbatim copy at `copy`, relative to the configuration repository), `repo-file` (byte-identical to `repo_path` in the recorded `checkout`, optionally `refresh: each-run` when the unit re-extracts it before running), `installed-tool` (the package and version that provide it) or `missing` (gone from disk, with the reason). `build --out FILE` SHALL keep the `scripts`, `windows_layer` and `other_machines` sections of the FILE it replaces unchanged. `check` SHALL list under "(f) scripts the units run that are in no git repository and have no `scripts` record" every unit script outside git whose path is not under `/usr/`, `/bin/`, `/sbin/` or `/lib/` and has no record, and exit 1 when there is any.

Source: inferred by agent, from the AES consolidation plan item 6 ("Still open: 15 scripts the units run are in no git repository"). Inferred by agent: exempting operating-system programs, which their package manager restores.

#### Scenario: every-script-outside-git-has-a-record

- **WHEN** a unit runs a script outside git that has a `scripts` record, and `build --out` rewrites the manifest
- **THEN** `check` reports (f) as 0, the rebuilt file still holds `scripts` and `windows_layer`; removing the record makes `check` name the script under (f) and exit 1; a program under `/usr/` is never listed

### Requirement: script-copies-can-be-compared-and-installed

`check-scripts` SHALL compare each `scripts` record with its source without changing anything: a `copied` script with its copy, a `repo-file` with `git show <ref>:<repo_path>` (ref default `origin/main`) in its checkout, and report presence for `installed-tool` and `missing` records. It SHALL exit 1 when a copy differs or is missing from the configuration repository, or a repository file differs or cannot be read; a difference for a `refresh: each-run` record is reported as stale and does not fail; a script absent from disk does not fail. `install-scripts` SHALL be a dry run unless `--apply` is given; with it, it SHALL copy each `copied` script that is missing or differs to its path, keeping the file's mode, first copying a differing disk file to `~/archive/machine-scripts-replaced/<path>-<date>/`; it SHALL never delete a file, never install another kind, and skip, and report, any path that is a symlink or sits under one.

Source: inferred by agent, from the AES consolidation plan item 6 and the safe-install rules of `install-units` (slice 2).

#### Scenario: script-copies-can-be-compared-and-installed

- **WHEN** a copied script and an installed repository file match their sources, then each is changed, then the record is marked `refresh: each-run` and the copy removed
- **THEN** `check-scripts` exits 0, then exits 1 naming both, then reports the repository file as stale and the copy as missing; `install-scripts` writes nothing without `--apply`, backs up and replaces the changed script with `--apply`, and skips a path under a symlink
