## Why

AES's goal is that requirements, tests and code stay linked so an agent working on code sees what it must keep
true (`docs/architecture/GOAL.md:88`, `docs/architecture/LOCKSTEP.md:26`). A copy of the template has the links
(`Implements:` docstring lines and `req()` test markers) but no agent sees them while editing, because the edit
hook is installed only by `lockstep init`, and no file lists the links for a person or a tool. The minimal-core
list left this out; Brian, 2026-11-23: "isnt this the whole thing that makes the whle systme work?"

Source: Brian, 2026-11-23, quoted above, and the AES goal page lines cited; plan
`docs/planning/linked-chain-core-2026-11-23.md`.

## What Changes

- The template ships `.claude/settings.json` and `.codex/hooks.json` that run the copy's own `lockstep-hook` on
  edits. With no layout plan in the copy, the hook only hands over requirement text; it never refuses.
- For Claude, the hook no longer answers `permissionDecision: allow` when it only passes context, so it never
  skips the agent's own permission prompt (Codex already worked this way).
- `lockstep check project` writes `docs/links.json`: every capability, requirement, scenario, test, file and
  symbol, and the links between them, generated from the markers. The template ignores it like `docs/status.md`.
- The status page's requirement table shows the file and line of each implementing symbol.

## Impact

- `src/lockstep/hook.py`, `src/lockstep/checks/status.py`, `src/lockstep/checks/project.py`, `src/lockstep/ship.py`
  (generated paths), `template/.claude/settings.json`, `template/.codex/hooks.json`, `template/.gitignore`,
  `template/README.md.jinja`, tests. Existing copies get the hook files and the ignore line at `copier update`.
