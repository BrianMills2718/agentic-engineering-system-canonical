## Why

Since AES #1020 the edit hook refuses an edit to a stale planned file under `src/lockstep/` and names
`lockstep check project` as the fix. That command did not rewrite cog plan copies, and it wrote its own
requirement block inside a copy (`src/lockstep/hook.py` was already flagged at HEAD), so after any requirement
rewording every edit to the implementing file would be refused with no working recovery. Found by a session
audit on 2026-11-23. AES AGENTS.md: "A block must provide a runnable recovery path".

## What Changes

- `lockstep check project` re-renders each cog plan copy in a layout repository, and `--check` reports one that differs.
- It no longer treats an `Implements:` line inside a plan copy as the place for its own block.
- A layout repository whose specs yield no statement text (issue #1019) is still projected.

## Impact

The recovery the hook's refusal names now works. Source: inferred by agent from the audit finding.
