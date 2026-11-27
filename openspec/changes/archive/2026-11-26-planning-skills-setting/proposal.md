## Why

Company Planning's skills reach an agent only through a per-person plugin install, so a repository that relies on them
cannot say so, and a teammate or a fresh machine starts without them. Brian, 2026-11-25, adopting the settings model in
`docs/planning/next.goal.md`: "the whole systm should be configurable so you can congfigure what is on or off" (row
"Company Planning skills | per-person plugin install | slice 3").

Plan: `docs/planning/next.goal.md`, "Slice 3 (planned in full, 2026-11-26)".

Plan size: full

Planning package: `docs/planning/planning-package.json`

## What Changes

- New setting `planning.skills: {mode: block|warn|off, marketplace: OWNER/REPO}`; absent means `off`.
- `lockstep init` merges Claude Code's own plugin keys (`extraKnownMarketplaces`, `enabledPlugins`) into
  `.claude/settings.json`, never overwriting another source or an opt-out `false`, and prints the Codex commands and
  the per-clone `claude plugin install ... --scope project` line (also added to an existing `AGENTS.md`).
- `lockstep check project` reports drift between the setting and `.claude/settings.json`: refuse under block, warn
  under warn; a conflict only warns. Not a ship gate; `planning_modes` does not validate the key.

## Impact

- New `src/lockstep/checks/plugin_settings.py`; `src/lockstep/init_repo.py`, `src/lockstep/checks/cli.py`,
  `src/lockstep/side_file.py`.
- Tests: `tests/test_plugin_settings.py`.
- Not changed: `ship`, `CHECK_NAMES`, the lefthook command init writes, anything under `~/.codex/`.
