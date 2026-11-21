## 1. Ignored status page

- [x] 1.1 Test: with `docs/status.md` in `.gitignore`, `project --check` does not name it, and `project` still writes it
- [x] 1.2 `project()` skips the page under `--check` when `git check-ignore` matches it

## 2. ship command line

- [x] 2.1 Test: `ship_command` gives `uv run ship` with the dependency and `ship` without; `run_plan` prints it
- [x] 2.2 `ship_command()` in `plan_run.py`, used by the final print
