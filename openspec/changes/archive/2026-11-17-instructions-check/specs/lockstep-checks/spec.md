## ADDED Requirements

### Requirement: Instructions: The agent chain fits its budget

The instructions check SHALL report `payload_over_cap` when the byte sizes of the chain files that exist (default
`~/code2/workspace/agents/core.md` and `~/code2/AGENTS.md`; `--chain FILE`, repeatable, or `INSTRUCTION_CHAIN`
separated by the path separator, replace them) plus the repository's root `AGENTS.md` add up to more than 32,768
bytes, and `root_oversized` when the root `AGENTS.md` alone is more than 12,000 bytes.

Source: Brian, 2026-11-17: "check first." (Decision 19); the 32,768-byte Codex budget and the 12 KB root guidance are
in `project-meta/docs/ops/SUBTREE_INSTRUCTION_HIERARCHY.md` ("Instruction Size") and the `instruction-surfaces` skill.

#### Scenario: Instructions: An oversized root fails

- **GIVEN** a repository whose root `AGENTS.md` is 13,000 bytes
- **WHEN** `lockstep check instructions` runs
- **THEN** it reports `root_oversized` and exits 1

#### Scenario: Instructions: A chain over the cap fails

- **GIVEN** a 30,000-byte chain file and a 5,000-byte root `AGENTS.md`
- **WHEN** the check runs with that chain
- **THEN** it reports `payload_over_cap` and exits 1

### Requirement: Instructions: No CLAUDE.md with its own content

The instructions check SHALL report `claude_md_content` for every `CLAUDE.md` in the repository (outside `.git`,
`node_modules`, virtual environments, `worktrees` and `*_worktrees` folders) whose content is anything other than the
single line `@AGENTS.md`. A pure pointer is counted, not reported.

Source: Brian, 2026-11-17: "shouldnt it be no claude.md since claud code supports agents.md now but codex doesnt
supprot claude.md?"; Claude Code reads `AGENTS.md` only when no `CLAUDE.md` is in or above the working directory
(https://code.claude.com/docs/en/memory.md), and Codex never reads `CLAUDE.md`.

#### Scenario: Instructions: A CLAUDE.md with content fails

- **GIVEN** a repository with a `CLAUDE.md` holding rules
- **WHEN** the check runs
- **THEN** it reports `claude_md_content` for that file and exits 1

#### Scenario: Instructions: A pointer CLAUDE.md passes

- **GIVEN** a `CLAUDE.md` holding only `@AGENTS.md`
- **WHEN** the check runs
- **THEN** it reports no finding for it

### Requirement: Instructions: A nested file repeats nothing from its parents

The instructions check SHALL report `duplicated` for a nested `AGENTS.md` that has three or more lines of 40 or more
characters, after trimming, identical to lines of an `AGENTS.md` above it in the same repository.

Source: Brian, 2026-11-17: "basically you work your way up from the most nested dir and each parent dir only gets what
is relevant" and the policy's delta-only rule, "children do not restate parent policy"
(`project-meta/docs/ops/SUBTREE_INSTRUCTION_HIERARCHY.md`).

#### Scenario: Instructions: A repeated parent block fails

- **GIVEN** a nested `AGENTS.md` that copies three long lines from the root `AGENTS.md`
- **WHEN** the check runs
- **THEN** it reports `duplicated` for the nested file and exits 1

### Requirement: Instructions: Count line and exit status

The instructions check SHALL print one count line `instructions: files=N payload_bytes=N payload_over_cap=N
root_oversized=N claude_md_content=N duplicated=N`, then one line per finding (kind, path, reason), and exit 0 when
there is no finding and 1 otherwise. A repository with no `AGENTS.md` prints the count line with `files=0` and exits 0.

Source: inferred by agent, from the docmeta check's output form.

#### Scenario: Instructions: A clean repository passes

- **GIVEN** a repository with a 2,000-byte root `AGENTS.md`
- **WHEN** the check runs
- **THEN** every count but `files` and `payload_bytes` is 0 and it exits 0
