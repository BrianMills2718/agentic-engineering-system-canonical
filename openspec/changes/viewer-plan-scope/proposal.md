## Why

Brian, 2026-11-28, on what the replay counts as the plan: "i think i thought of plan as actually all
documentation/files that arent code (other than the navigational wiki) but maybe thats not best?", then "continue
through all remainign hihg condience items". The replay counted only `lockstep.yaml` and OpenSpec files as the plan,
so a session that wrote its architecture page or decision record first was reported as not writing the plan first.

## What Changes

- A plan write is a write, not refused, to `lockstep.yaml`, any file under `openspec/`, or an authored document
  (`.md`, `.rst`, `.txt`, `.adoc`, `.json`, `.c4`) anywhere in the checkout, including `AGENTS.md` and `CLAUDE.md`.
- Not plan, even when the file is a document: the navigational wiki (`wiki/`, `generated/wiki/`), anything under
  `generated/` (a tool rewrites it), tests (`tests/`), and config folders (`.claude/`, `.agents/`, `.codex/`,
  `.github/`). Code and config files (`pyproject.toml`, `Makefile`, `lefthook.yml`) are never plan.
- A path outside the repository is never a plan write.

Plan size: small
