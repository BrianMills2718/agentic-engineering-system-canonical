## Why

`docs/links.json` lists the chain from requirement markers in code and tests, but repositories already write
three more kinds of link lines that nothing puts in that file: `Closes:` lines in plans and change proposals
(which plan changed which requirement), `Source:` lines (where a requirement came from), and
`<!-- lockstep quote: <id> -->` markers (which document passage repeats which requirement). Reading them gives a
person and a tool one file for "why does this requirement exist and where else is it stated", with no new line
for anyone to write.

Source: Brian, 2026-11-23: "i approve" (to reading the existing `Closes:`, `Source:` and quote lines into
`links.json`, with no new lines); plan `docs/planning/links-existing-lines-2026-11-23.md`.

## What Changes

- `docs/links.json` gains `plan` nodes (active and archived proposals and plans with a `Closes:` line, field
  `state`) and `quote` nodes (one per marker, field `state` from the quotes check), each linking to the IDs it
  names; IDs no node has go in the node's `unknown` list.
- Requirement nodes gain `source` (the `Source:` text) and `source_kind` (`brian`, `inferred`, `other`,
  `missing`, using the repository's configured human pattern).
- No check changes its exit code; `plan_files()` and the plan status blocks are unchanged.

## Impact

- `src/lockstep/checks/status.py`, `src/lockstep/checks/project.py`, tests. Copies get it at their next lock
  upgrade; their `links.json` is git-ignored build output.
