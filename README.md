# Agentic Engineering System (AES), canonical

AES helps autonomous coding agents deliver software that stays true to its intent.
It includes Lockstep, the feedback loop and the policy layer. Alignment between
plans, code and documentation is a means to that goal.

Start at the [navigational wiki](wiki/index.md) or the [documentation reading order](docs/index.md).

- [AES purpose and thesis](docs/architecture/GOAL.md): the complete system and its boundaries.
- [Lockstep](docs/architecture/LOCKSTEP.md): plan behavior, files, typed interfaces and tests;
  project requirements into docstrings and observed implementation status back into documents;
  preserve a source-local normative change path and navigate the linked sources.
- [Documentation roles](docs/architecture/DOCUMENTATION.md): normative, research, decisions,
  plans, evidence, generated views, PRDs and wiki navigation.
- [Feedback and policy](docs/architecture/FEEDBACK_AND_POLICY.md): turn corrections into
  verified changes and keep rule authority distinct from enforcement machinery.
- [Current state](.project-brain/now.md) and [discussion ledger](wiki/open-questions.md):
  distinguish intended behavior, implementation, dated observations and open gaps.

Lockstep ships from `src/lockstep/` here. The old `aes` command and `.aes/target.yaml`
retire consumer by consumer; the [retirement record](docs/retired/2026-11-12.md)
explains this repository's historical governance. This reading-path repair changes
no product behavior and does not certify every consumer's hooks or generated views.

## Install and test

- Python 3.11 or newer is required ([pyproject.toml:9](pyproject.toml#L9)).
- Install with uv: `uv venv .venv && uv pip install -e ".[dev]"` ([pyproject.toml:9](pyproject.toml#L9)).
- `make check` runs the AGENTS.md sync check, pytest without slow tests, and mypy ([Makefile:19-29](Makefile#L19-L29)).
- `make check-full` adds the slow end-to-end tests ([Makefile:31-33](Makefile#L31-L33)).

## Make a repository

This repository holds the starter template (`copier.yml` and [template/](template/)). Make a new repository with:

```
uvx copier copy --trust gh:BrianMills2718/agentic-engineering-system-canonical <dir>
```

It needs `git`, [uv](https://docs.astral.sh/uv/), [OpenSpec](https://github.com/Fission-AI/OpenSpec) (`openspec`),
[lefthook](https://github.com/evilmartians/lefthook), [gitleaks](https://github.com/gitleaks/gitleaks) and
[Node.js](https://nodejs.org/) (`npx`); `ship` and `run-plan` also need a logged-in GitHub CLI and Claude Code or
Codex. The copy asks for a name and a one-sentence description, and a few questions `--defaults` answers; then it installs
Lockstep and generates its docs. New copies take this repository's `main` as it stands (there are no version tags).
A new copy ships `lockstep.yaml` with a `layout:` row for each starter file, so the edit hook and `make check` refuse
a file under `src/<package>/` that no row names; a plan adds rows with its OpenSpec change, and
`uv run lockstep layout` creates the planned files with their requirement text. `copier update` of a copy made
before this adds no `lockstep.yaml` and leaves its starter files under `src/<package>/` unchanged.
Spec: [portable-template](openspec/specs/portable-template/spec.md); why this layout:
[decision 0015](docs/decisions/0015-off-the-shelf-documentation-stack.md).

## Run one plan and merge it

A repository made from the template already depends on this package. To have an agent build one OpenSpec change and
merge it:

```
uv run lockstep run-plan <change> --agent claude    # or --agent codex
cd <the worktree it prints> && uv run ship
```

`run-plan` has a separate session write hidden acceptance tests from the plan, runs the implementer, then runs those
tests, `make check` and a departure report (files changed outside `tasks.md`). `ship` merges only when `make check`
passed on that commit, the newest hidden-test run for the branch passed at that commit, and every OpenSpec change
that adds a requirement holds a decided `prior-art.json` (`lockstep check prior-art`). Outside such a repository,
install `ship` with `uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical ship`.
It needs `git`, `uv` and a logged-in [GitHub CLI](https://cli.github.com/). Specs:
[plan-run](openspec/specs/plan-run/spec.md), [ship](openspec/specs/ship/spec.md),
[prior-art-check](openspec/specs/prior-art-check/spec.md).

## Install Lockstep in a repository

In the root of any git repository (needs [uv](https://docs.astral.sh/uv/); the repository is public):

```
uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical lockstep init
```

It writes only what is missing, never overwrites, and prints one line per file (`wrote` or `skipped`):

- `lockstep.yaml`: the one settings file. `checks:` sets each commit check to `block`, `warn` or `off`; `owner:` is `--owner NAME`, else the owner of the git `origin`, else a placeholder to edit; `sources.human_pattern` is the text a `Source:` line starts with to count as a person's word (default `brian`, the same default the checks use; `--human-pattern REGEX` sets another); `governed:` and `layout:` start empty and hold the plan.
- `.claude/settings.json` and `.codex/hooks.json`: a PreToolUse hook that runs the edit guard (`lockstep-hook`) before each edit or shell command. An existing file keeps its other settings.
- `lefthook.yml`: a `lockstep` pre-commit command. Run `lefthook install` once (see [lefthook](https://lefthook.dev/)) so git calls it.
- `.gitignore`: a `.lockstep/` line, for older logs. The guard logs each decision outside the checkout, to `${XDG_STATE_HOME:-~/.local/state}/lockstep/<repository>/hook-<date>.jsonl`, or to `$LOCKSTEP_LOG_DIR` when set.

No written file holds an absolute path: the hooks install Lockstep from the git address above on any machine.

To switch a check, edit `lockstep.yaml`:

```yaml
checks:
  trace: warn     # prints a warning and passes
  docmeta: off    # skipped
```

`lockstep check <name>` runs one check (`trace`, `arch`, `test-first`, `sources`, `docmeta`, `project`); `lockstep check` with no name judges the whole tree against the plan; `lockstep layout` creates the planned files. The edit guard refuses edits to files outside the plan under `governed:` folders; while `governed:` is empty it refuses nothing. A planned file that existed before its `layout:` row keeps the `Implements:` block `lockstep check project` writes, and the guard and `lockstep check` treat it as current while that command would leave it unchanged (#977, #979). Copy a `lockstep.yaml` into another repository and change `owner:` and it works there. Design: [proposals/one-planning-tool/DESIGN.md](proposals/one-planning-tool/DESIGN.md).

## Lineage

- This repository replaced `Inside-Success/agentic-engineering-system`, archived on 2026-09-26 ([docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:44-47](docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md#L44-L47)).
- It adopts project-agnostic architecture from `BrianMills2718/wiki_methodology` at revision `0cddc6b1` ([CLAUDE.md:10](CLAUDE.md#L10)).

## Project source-owned facts

Artifact descriptions, lifecycle status, native evidence fields and Python
interfaces can be displayed without a second handwritten copy. Declare each
projection in `lockstep.yaml`:

```yaml
projections:
  - id: plan-61
    source: docs/plans/61.md
    target: wiki/index.md
    fields: [description, status]
  - id: public-api
    source: src/api.py
    symbol: greet
    target: docs/reference.md
    fields: [description, signature]
  - id: last-check
    source: docs/evidence/check.json
    target: docs/reference.md
    fields: [result]
# Optional when source files are outside the docs site's published directory:
source_base_url: https://github.com/OWNER/REPO/blob/main/
```

Put each marker pair in its target, preserving the id from the declaration:

```markdown
<!-- lockstep facts: plan-61 -->
<!-- /lockstep facts: plan-61 -->
```

Run `lockstep refresh` to update declared fact blocks only, or
`lockstep check project` to update them along with existing requirement/coverage
projections. `lockstep check project --check` writes nothing and exits 1 for a
stale copy. Repositories with no OpenSpec requirements do not get an empty coverage page
or historical-plan rewrites.
Fact blocks can share a plan file with its generated coverage block. In a
repository with OpenSpec requirements, `docs/status.md` belongs to the full-file
coverage renderer; use another fact target.

Markdown fields come from YAML front matter; JSON and YAML fields come from
native mapping keys. Python `description` is its docstring's first paragraph,
`docstring` is the whole docstring, and `signature` is extracted from the named
function or class with the AST. A dotted `symbol` names a class member. Project
code is never imported or run. Source links are relative by default; the
optional HTTP(S) `source_base_url` makes links portable on a docs site. Unknown
fields, missing sources, escaping paths or malformed markers fail with exit 2
before projection writes.

`lockstep init` adds post-edit refresh hooks for Claude Code and Codex and a
read-only projection check to its lefthook pre-commit command. It preserves
existing hooks and can add this post-edit entry to an older installation.
An exact previous generated pre-commit command is upgraded in place; a custom
`lockstep` command is preserved and gets a separate `lockstep-project` freshness
command. A conflicting custom `lockstep-project` name reports an error.
Native client trust/enablement still applies; a generated hook declaration is
not proof the client executed it. The merge command must also run the
read-only check to cover bypassed or unavailable hooks.

Refresh records source/target hashes, selected fact values and changed paths
in one `.lockstep/projection-YYYY-MM-DD.jsonl` file per day. A concrete edit to
an applicable source that fails records its error and declared source identities
when the trace path is contained and writable, without copying raw tool input.
An edit to
an unrelated file is a no-op; shell events compare declared facts conservatively
because scripts can write paths not evident from command arguments. No
projection declarations means refresh does nothing.

This is source-copy freshness, not proof that an authored description is true
of its implementation. Narrative explanation and behavioral adequacy still need
their own source review. The contract is
[lockstep-doc-facts](openspec/specs/lockstep-doc-facts/spec.md).
