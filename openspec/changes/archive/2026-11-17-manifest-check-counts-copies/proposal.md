## Why

`machine_manifest.py check` exits 1 whenever any unit file is `local-only`, even when the slice-2 copy of that file in
the units repository (`aes-config/machine-units`) is byte-identical and `install-units` would restore it. On this
machine 115 local-only files and one `/dev/null` link all have identical copies (`check-units`: same 115, differ 0,
recorded symlinks same 1), so `check` can never pass, and the AES consolidation plan item 6 refresh asks for `check`
and `check-units` to exit 0. No timer, unit, nightly gate or page acts on `check`'s exit code (searched aes-config,
code2-workspace, the AES runtime clone and the user unit folder on 2026-11-17).

Source: inferred by agent, from the AES consolidation plan row 11 ("Before item 11", step 7) and item 6 slice 2.

## What Changes

- `check` takes `--units-repo` (default as `check-units`). A local-only file whose units-repository copy is identical,
  and a symlink outside git whose recorded `.symlink` target equals the live target, are listed under a new count (e)
  that does not fail the check. A missing, differing or absent copy, or no units repository, fails as before.
- `build` and the manifest are unchanged: such files stay `local-only`.

## Impact

`scripts/machine_manifest.py`, `tests/test_machine_manifest.py`, the `machine-manifest` spec.
