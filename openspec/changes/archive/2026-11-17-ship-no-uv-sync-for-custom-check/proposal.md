## Why

`ship --check '<cmd>'` still ran `uv sync --all-extras` first. research_v3 could not ship a hook-only change because that sync fails on its open-web-retrieval extra, and the failed sync left an empty `.venv` behind, which the next run read as a present environment.

## What Changes

- `uv sync --all-extras` runs only when the check is the repository's own Makefile check (a `make ...` command, the default `make check` included). A `--check` that names another command skips it; ship prints one line saying so. `npm ci` is unchanged.
- A failed `uv sync` or `npm ci` removes the `.venv` or `node_modules` that the failed step just created.
- The existing fresh-worktree and failing-setup tests now use a Makefile check; three tests are new.
