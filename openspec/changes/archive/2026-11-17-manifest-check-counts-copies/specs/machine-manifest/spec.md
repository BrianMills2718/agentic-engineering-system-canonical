## MODIFIED Requirements

### Requirement: local-only-units-are-reported

`check` SHALL rebuild the manifest in memory, list every `local-only` file, print the count, and exit 1 when there is any. A `local-only` file whose copy in the units repository (`--units-repo`, default as `check-units`) is byte-identical, and a symlink outside git whose recorded `NAME.symlink` target equals the live link target, SHALL instead be listed and counted under "(e) local-only files and links with an identical copy in the units repository", which does not fail the check. A file with no copy or a differing copy, a link whose recorded target differs, and every file when the units repository folder does not exist, SHALL be reported and fail as before.

Source: inferred by agent, from the AES consolidation plan row 11 ("Before item 11", step 7: `check` and `check-units` exit 0) and item 6 slice 2 (the units repository restores these files).

#### Scenario: local-only-units-are-reported

- **WHEN** a unit or drop-in file is a regular file not generated from the job list
- **THEN** `check` names it under "local-only files, lost on a clean machine" and exits 1

#### Scenario: identical-copies-do-not-fail

- **WHEN** every local-only file has a byte-identical copy in the units repository and a `/dev/null` link has a matching `.symlink` record
- **THEN** `check` lists them under (e), reports (a) and (b) as 0 and exits 0; removing or changing one copy, changing the recorded link target, or pointing at a missing units repository makes it exit 1
