# `lockstep init` installs Lockstep in a repository with one command (one-tool design, slice 6)

## Why

The design promises that Lockstep installs in a fresh repository with one command and writes no absolute path
(`proposals/one-planning-tool/DESIGN.md`, "A concrete example of the finished tool", step 1; acceptance A1 and A5).
No such command exists, so each repository still copies hook entries by hand from lifelike.

## What changes

- `lockstep init [--repo PATH] [--owner NAME] [--source URL]` writes, only when absent: `lockstep.yaml`, the Claude Code
  hook (`.claude/settings.json`), the Codex hook (`.codex/hooks.json`), a `lockstep` pre-commit command in `lefthook.yml`,
  and `.lockstep/` in `.gitignore`. It prints what it wrote and what it skipped, and never overwrites.
- The hook commands install from the git address of this repository through `uvx`, so they work on any machine.
- The edit guard writes its log to `.lockstep/` (the design's name) instead of `.pcw/`.

## Not in this change

The `likec4` pin and `governed`/`layout` content (the user writes the plan), and changing the default of
`sources.human_pattern` for a repository with no `lockstep.yaml`.
