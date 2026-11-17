## Why

`~/.local/bin/prune-merged-worktrees` links to Project Meta `scripts/prune_merged_worktrees.py`. personal-file-infra
`prune-all-worktrees` runs it across every repository each week (`disk-maintenance-weekly`), and Project Meta is being
retired (AES consolidation plan, row 11, "Before item 11"). The script removes a worktree only when the forge or the
content proves its branch landed, which no AES tool does (`lane_sweep.py` covers code2 lanes only).

Source: inferred by agent, from the AES consolidation plan row 11 (the ordered ports before the archive yes).

## What Changes

- `scripts/prune_merged_worktrees.py` is copied unchanged from Project Meta `b743c308a` (only the docstring gains its
  `Implements:` line and where it came from), with its three tests.
- The installed link `~/.local/bin/prune-merged-worktrees` points at the AES runtime clone's copy
  (`~/.hive-brain/aes/scripts/prune_merged_worktrees.py`) once this merges.

## Impact

New `scripts/prune_merged_worktrees.py` and `tests/test_prune_merged_worktrees.py`. No caller changes: they run the
command by name.
