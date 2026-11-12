## Why

The code2check commit checks (trace, arch, test-first, sources, docmeta) live in a separate package, so a repository that adopts Lockstep needs a second tool. Slice 4 of the one-tool design moves them into Lockstep.

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 4).

## What Changes

- New package `lockstep.checks`, ported from code2-template `src/code2check` at 6ce00a9, and the command `lockstep check <name>`.
- `lockstep.yaml` gains `checks:` (block, warn or off per check), `sources.human_pattern`, `owner` and `likec4`; `side_file._TOP` accepts those keys.
- `lockstep check` with no name keeps running the whole-tree plan check.
- Not ported: code2check's `status`, `project`, `show` and `guard` commands and `arch gen`'s use outside the check.

## Impact

New capability `lockstep-checks`. Code: `src/lockstep/checks/`, `src/lockstep/check.py` (`cli`), `src/lockstep/side_file.py` (one set literal).
