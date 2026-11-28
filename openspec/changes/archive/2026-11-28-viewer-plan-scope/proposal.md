## Why

Brian, 2026-11-28, on what the replay counts as the plan: "i think i thought of plan as actually all
documentation/files that arent code (other than the navigational wiki) but maybe thats not best?", then "continue
through all remainign hihg condience items". The replay counted only `lockstep.yaml` and OpenSpec files as the plan,
so a session that wrote its architecture page or decision record first was reported as not writing the plan first.

## What Changes

- A plan write is a write, not refused, to `lockstep.yaml`, a document under `openspec/` (not `openspec/config.yaml`),
  or an authored document (`.md`, `.rst`, `.txt`, `.adoc`, `.json`, `.c4`) anywhere in the checkout, including
  `AGENTS.md` and `CLAUDE.md`.
- Not plan: a file under a wiki, generated, test, fixture, dependency, build, raw-source, run-evidence or agent-config
  folder at any depth, a dependency or licence file (`package.json`, `requirements*.txt`, `LICENSE*`, `*.lock` and the
  like), code and config, and any file outside the repository.
- A write stays `planned` when only a later document or a whole rewrite of `lockstep.yaml` names its file; only an
  edit that adds the row after the write makes it `row added later`.

Plan size: small
