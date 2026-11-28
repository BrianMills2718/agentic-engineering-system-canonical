## Why

Brian, 2026-11-27: "the wiki is more for the agent than anyone ... it always has the high level navigational wiki
index in its context". A fresh copy of the template tells the agent, in `AGENTS.md`, to read
`generated/wiki/index.md` first, but nothing puts the index in its context: an agent that skips the instruction
never sees it.

Closes: portable-template/a-fresh-copy-starts-each-session-with-the-wiki-index

Plan size: small

## What Changes

- The template's `.claude/settings.json` and `.codex/hooks.json` get a `SessionStart` hook that hands the agent
  `generated/wiki/index.md` as added context, the same way in both clients. When the file does not exist the hook
  prints nothing.

## Impact

- `template/.claude/settings.json`, `template/.codex/hooks.json`, `tests/test_template_portable.py`.
