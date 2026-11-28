## Why

In the 2026-11-28 Sonnet end-to-end run the edit hook refused a `python3 - <<'EOF'` script that wrote only an
OpenSpec proposal, because the proposal's text named `src/e2e_sonnet/core.py` and `src/e2e_sonnet/cli.py`
(hook log `~/.local/state/lockstep/e2e-sonnet/hook-2026-11-28.jsonl`, 05:56:40, `shell_write` deny). The rule
counted every path a writing script names as written, including paths inside the text it writes.

Plan size: small

## What Changes

- For Python code in a command (a `python -c` argument, or a heredoc Python reads as its program), the hook
  reads the code with Python's own parser. Only when it can vouch for all of the code (every import, name, call
  and keyword known, every write target worked out) does it count just the paths the writing calls target.
- Anything else keeps the old rule, every path the code names: aliases, unknown calls, code that runs other
  programs, bindings it does not follow, shell expansion, a crash while reading. The independent review of the
  first version found 42 of 70 probes where narrowing missed a write; each is now a test.

## Impact

- `src/lockstep/shell_targets.py`, `tests/lockstep/test_lockstep_shell_targets.py`, the lockstep-guard spec.
