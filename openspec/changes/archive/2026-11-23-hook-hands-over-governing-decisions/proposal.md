## Why

A decision record says why the code is the way it is, but an agent editing that code never sees it, and nothing
notices when a decision is superseded while code still follows it. Every AES decision record already names what it
governs on a `Governs:` line and its state on a status line; nothing reads them. Reading those lines lets the edit
hook hand the agent the decisions behind a file, flag a superseded one, and put decisions in `docs/links.json`,
with no new line for anyone to write.

Source: Brian, 2026-11-23: "i approve" (decision -> requirement or code links that the hook hands over); plan
`docs/planning/links-existing-lines-2026-11-23.md`. A search of Brian's earlier chats found no earlier rule on this.

## What Changes

- New `lockstep/decisions.py` reads `docs/decisions/[0-9]*.md`: title, status, successor, decision paragraph,
  source, and `Governs:` targets resolved to paths (folders too) or requirement and capability IDs.
- The edit hook (edit and shell routes) appends the decisions governing the file after the requirement text, at
  most three in full, superseded ones flagged; a file only a decision governs now gets that text. Log field
  `decisions`.
- `docs/links.json` gains `decision` nodes.
- Template decision 0001 gains `- Governs: docs/architecture/model.c4`; the README says what the line does.
- No check changes its exit code.

## Impact

- `src/lockstep/decisions.py` (new), `src/lockstep/hook.py`, `src/lockstep/checks/status.py`,
  `template/docs/decisions/0001-use-the-code2-layout.md`, `template/README.md.jinja`, tests. Copies get the
  template line at `copier update` and the hook change at their next lock upgrade.
