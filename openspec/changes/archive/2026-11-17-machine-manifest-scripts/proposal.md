## Why

The AES consolidation plan item 6 asks that nothing the machine runs lives only on the laptop's disk. The unit files
are covered (slice 2), but 15 of the scripts the units run were in no git repository (checked 2026-11-17: 6 small
hand-written scripts with no copy anywhere, 5 byte-identical installed copies of committed repository files, 2
installed tools, 2 already gone from disk). `build` records a script's repository as `not-in-git` and nothing fails,
so a clean machine would lose the 6 and nobody would know how to bring back the rest. The Windows scheduled tasks and
the Mac mini and VPS are also not in the manifest.

Source: inferred by agent, from the AES consolidation plan item 6 ("Still open: 15 scripts the units run are in no git
repository"), approved by Brian 2026-11-16 (Decision 25 A).

## What Changes

- The manifest gains three hand-written sections, `scripts`, `windows_layer` and `other_machines`; `build --out FILE`
  keeps them from the FILE it replaces.
- `check` gains a failing count (f): a script a unit runs that is in no git repository, is not an operating-system
  program (`/usr/`, `/bin/`, `/sbin/`, `/lib/`), and has no `scripts` record.
- New `check-scripts`: each `scripts` record against its source (`copied`: the copy in the configuration repository;
  `repo-file`: `git show origin/main:<path>` in the recorded checkout; `installed-tool` and `missing`: presence). Exit 1
  on a differing copy, a missing copy, repository drift or an unreadable repository file.
- New `install-scripts`: dry run unless `--apply`; copies `copied` scripts that are missing or differ, backing up a
  differing file first; never deletes; never writes through a symlink.

## Impact

`scripts/machine_manifest.py`, `tests/test_machine_manifest.py`, the `machine-manifest` spec; aes-config gains
`machine-bin/` and the three sections in `machine-layer.yaml`.
