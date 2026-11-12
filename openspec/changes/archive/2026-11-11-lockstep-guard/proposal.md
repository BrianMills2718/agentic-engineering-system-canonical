## Why

Lockstep's edit hook found a shell command's written paths with regexes over the command text. Per
BrianMills2718/lockstep#111, `python -c "open(p,'w')..."` creating an unplanned file under a governed root
was let through, and `cp <planned> /tmp/x`, which only reads a planned file, was refused. code2check's guard
(code2-template `src/code2check/guard.py` at 6ce00a9, pull requests 25 and 26) already judges both correctly.

## What changes

- New `src/lockstep/shell_targets.py`: the guard's shell-target parser, ported (quote-aware command
  splitting, heredoc bodies joined to their command, a copy writes only its destination, code writes only
  what it calls something to write), with `cd` following kept.
- `src/lockstep/hook.py` finds a shell command's written paths through it. Plan text handed over, stale
  refusal, symbol gate, logging, PCW_MODE and both output protocols are unchanged.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md, slice 3).
