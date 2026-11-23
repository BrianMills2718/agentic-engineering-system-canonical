## Why

Lockstep was not used on its own code: AES's `lockstep.yaml` had `governed: []` and `layout: []`, and the AES client
settings ran only `lockstep refresh`, not the edit hook. The settled design (`docs/architecture/LOCKSTEP.md:22-29` and
`:52-62`; `proposals/one-planning-tool/DESIGN.md` steps 2-4, approved by Brian 2026-11-11) says planned structure comes
before code and a write to an unplanned file is refused. Source: Brian, 2026-11-23, "i approve" to turning the full
system on in AES (plan `docs/planning/back-on-design-2026-11-23.md`).

## What Changes

- `lockstep.yaml` governs `src/lockstep/`, marks it `fixed` so the hook refuses rather than warns, and has one layout row
  per tracked file in it (rows for existing files derived from their docstrings and markers).
- `.claude/settings.json` and `.codex/hooks.json` run `lockstep-hook` before edits.
- New requirement `lockstep-plan-format/lockstep-governs-its-own-package`, with a test, so dropping any of this fails.
- `work_units.py` named a requirement ID no spec defines (`work-units-form-a-dag`); corrected to
  `work-units-form-a-checked-dag`, the ID of the requirement it implements.
- Quote markers in `LOCKSTEP.md` on the two passages the new requirement restates.

## Impact

Every agent editing `src/lockstep/` in AES now gets the file's requirement text, and a new file there needs a layout row
first.
