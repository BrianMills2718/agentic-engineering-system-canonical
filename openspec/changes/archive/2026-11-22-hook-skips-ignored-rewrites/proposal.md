## Why

A new copy of the template ignores `docs/status.md` in `.gitignore`, but its pre-commit job `lockstep-fast` passes
every file `lockstep check project` rewrote to `git add`, including `docs/status.md`. `git add` refuses an ignored
path, so every commit that changes the status page fails (exit 123). Seen in the second-user test on 2026-11-22:
a plan edit in a fresh copy could not be committed.

Source: inferred by agent from that failure; Brian asked for a portable template ("the whole thing should be
configurable and shareable/protable", 2026-11-20).

## What Changes

- The template's `lockstep-fast` pre-commit job stages each rewritten file unless git ignores it.

## Impact

- `template/lefthook.yml.jinja`; test in `tests/test_template_portable.py`. Existing copies need the same line.
