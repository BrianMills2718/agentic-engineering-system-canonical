## Why

Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search so that we are only buidling what we need to. that needs to be ienforced". Today only the shared commit hook (code2-workspace `hooks/base.yml`, job `prior-art`) enforces it, and a commit made with hooks skipped, or in a repository that has not joined the shared hooks, is never checked. `ship` is the one door every merge goes through (code2-workspace issue 833, slice 1).

## What Changes

- Before the planning gate and the check, `ship` runs code2-workspace's `scripts/prior_art_check.py` with `--files` set to the files under `openspec/changes/` that the merge adds or changes, and refuses the merge, with nothing pushed, when it exits 1, showing what it printed.
- When the merge touches no file under `openspec/changes/`, nothing is run.
- When the script is missing, or cannot run (any exit other than 0 or 1), the merge is refused with what to do, and the message says it is not a verdict on the record.
- The script is read from `$SHIP_WORKSPACE` (default `~/code2/workspace`), run with `uv run --no-project --with jsonschema python` (`SHIP_PRIOR_ART_PYTHON` overrides the command).

Code2-workspace pull request 864 lets the script look at an archived change named by `--files`, because a change is usually archived before it is merged.

## Impact

- `scripts/ship.py`, `tests/test_ship.py`, `openspec/specs/ship/spec.md`.
- Every repository that merges with `ship`: a merge that adds an OpenSpec change adding a requirement, created on or after 2026-11-18, with no decided `prior-art.json`, is refused. Changes created earlier are exempt, as at commit time.

Plan size: small

Closes: ship/refuse-a-merge-whose-openspec-change-lacks-a-prior-art-record
