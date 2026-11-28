## Why

In the 2026-11-28 Sonnet end-to-end run the edit hook refused a `python3 - <<'EOF'` script that wrote only an
OpenSpec proposal, because the proposal's text named `src/e2e_sonnet/core.py` and `src/e2e_sonnet/cli.py`
(hook log `~/.local/state/lockstep/e2e-sonnet/hook-2026-11-28.jsonl`, 05:56:40, `shell_write` deny). The rule
counted every path a writing script names as written, including paths inside the text it writes.

Plan size: small

## What Changes

- For Python code in a command (a `python -c` argument, or a heredoc fed to `python`), the hook reads the code
  with Python's own parser and counts as written only the paths its writing calls target (`open(p, "w")`,
  `p.write_text`, `shutil.copy(src, dst)`, and the like), following simple assignments and `Path` joins.
- Code that does not parse, or whose write target cannot be worked out (an f-string path, say), keeps the old
  rule: every path it names counts.

## Impact

- `src/lockstep/shell_targets.py`, `tests/lockstep/test_lockstep_shell_targets.py`, the lockstep-guard spec.
