# Agentic Engineering System (AES), canonical

AES is the name for the whole agent system: Lockstep, the feedback loop and the policy layer ([CLAUDE.md:14-16](CLAUDE.md#L14-L16)).

- Lockstep, the one planning-and-checking tool (edit guard, commit checks, plan format), ships from this repository as package `src/lockstep/`; it moved here in #831-#837 and any repository can install it from this repository's git address ([CLAUDE.md:18-22](CLAUDE.md#L18-L22), [wiki/lockstep.md](wiki/lockstep.md), [.project-brain/now.md](.project-brain/now.md)).
- The feedback loop runs nightly from `scripts/learning_loop` in this repository ([.project-brain/now.md:9](.project-brain/now.md#L9)).
- The policy layer is the rules register here (`scripts/rules`, `docs/rules`) plus Brian's agent rules in code2-workspace `agents/` ([.project-brain/now.md:9](.project-brain/now.md#L9)).
- The `aes` command line and `.aes/target.yaml` retire one repository at a time (code2-workspace decision 0009) ([CLAUDE.md:17-20](CLAUDE.md#L17-L20)).
- AES no longer governs itself: its pre-commit refusal was removed on 2026-10-14 (#789) ([CLAUDE.md:22-23](CLAUDE.md#L22-L23)).
- The v0.2 governance regime is kept as history only ([CLAUDE.md:31-32](CLAUDE.md#L31-L32)).

## Where to start

- [wiki/index.md](wiki/index.md) is the front door ([CLAUDE.md:3](CLAUDE.md#L3)).
- [.project-brain/now.md](.project-brain/now.md) holds the current state; read it first ([CLAUDE.md:5-6](CLAUDE.md#L5-L6)).

## Install and test

- Python 3.11 or newer is required ([pyproject.toml:9](pyproject.toml#L9)).
- Install with uv: `uv venv .venv && uv pip install -e ".[dev]"` ([.project-brain/now.md:121-123](.project-brain/now.md#L121-L123)).
- `make check` runs the AGENTS.md sync check, pytest without slow tests, and mypy ([Makefile:543-553](Makefile#L543-L553)).
- `make check-full` adds the slow end-to-end tests ([Makefile:555-557](Makefile#L555-L557)).
- `make aes-check` runs the retained engine on this repository and its tests; it retires with `aes` ([Makefile:571-577](Makefile#L571-L577)).

## Install Lockstep in a repository

In the root of any git repository (needs [uv](https://docs.astral.sh/uv/); the repository is public):

```
uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical lockstep init
```

It writes only what is missing, never overwrites, and prints one line per file (`wrote` or `skipped`):

- `lockstep.yaml`: the one settings file. `checks:` sets each commit check to `block`, `warn` or `off`; `owner:` is `--owner NAME`, else the owner of the git `origin`, else a placeholder to edit; `sources.human_pattern` is the text a `Source:` line starts with to count as a person's word; `governed:` and `layout:` start empty and hold the plan.
- `.claude/settings.json` and `.codex/hooks.json`: a PreToolUse hook that runs the edit guard (`lockstep-hook`) before each edit or shell command. An existing file keeps its other settings.
- `lefthook.yml`: a `lockstep` pre-commit command. Run `lefthook install` once (see [lefthook](https://lefthook.dev/)) so git calls it.
- `.gitignore`: a `.lockstep/` line; the guard logs each decision to `.lockstep/hook-<date>.jsonl`.

No written file holds an absolute path: the hooks install Lockstep from the git address above on any machine.

To switch a check, edit `lockstep.yaml`:

```yaml
checks:
  trace: warn     # prints a warning and passes
  docmeta: off    # skipped
```

`lockstep check <name>` runs one check (`trace`, `arch`, `test-first`, `sources`, `docmeta`, `project`); `lockstep check` with no name judges the whole tree against the plan; `lockstep layout` creates the planned files. The edit guard refuses edits to files outside the plan under `governed:` folders. Copy a `lockstep.yaml` into another repository and change `owner:` and it works there. Design: [proposals/one-planning-tool/DESIGN.md](proposals/one-planning-tool/DESIGN.md).

## Lineage

- This repository replaced `Inside-Success/agentic-engineering-system`, archived on 2026-09-26 ([docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:44-47](docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L44-L47)).
- It adopts project-agnostic architecture from `BrianMills2718/wiki_methodology` at revision `0cddc6b1` ([CLAUDE.md:10](CLAUDE.md#L10)).
