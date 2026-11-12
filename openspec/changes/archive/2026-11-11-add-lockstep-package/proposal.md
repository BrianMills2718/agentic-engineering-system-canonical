# Lockstep ships from AES canonical (one-tool design, slice 1)

## Why

Brian approved one planning-and-checking tool, named Lockstep, shipped from this repository
(`proposals/one-planning-tool/DESIGN.md`; Brian, 2026-11-11: "i approve single tool desing re d4").
Slice 1 moves Lockstep's code (`pcw`, repository lockstep at 150d5a8) here as package `lockstep`, with its tests,
and keeps the old names working for lifelike and Team-Brains' runner.

## What changes

- New package `src/lockstep/` (the 26 modules of `pcw`, imports renamed); `src/pcw/` is an alias package that
  resolves `pcw.<module>` to `lockstep.<module>`.
- Commands `lockstep`, `lockstep-hook`, and the old `pcw`, `pcw-hook`.
- `cogapp` becomes a dependency; MkDocs is the optional `wiki` extra (and part of `dev`).
- Lockstep's tests move to `tests/lockstep/` with the example projects they copy. The tests that judge the lockstep
  repository's own plan and its walkthrough site stay in that repository.

## Not in this change

Reading OpenSpec plus `lockstep.yaml` as the plan (slice 2), the guard's shell parsing (slice 3), the commit checks
(slice 4), the plan check (slice 5), switching users (slice 6).
