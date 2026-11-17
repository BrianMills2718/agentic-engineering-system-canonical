# instruction-audit Specification

## Purpose

Audit the agent instruction files across the workspace for size, placement, duplication, derivable inventories and staleness, and report without rewriting them.

Ported into AES from Project Meta `scripts/audit_instruction_quality.py` and `scripts/scan_doc_freshness_ecosystem.py` (commit `f6f0d6f91`) on 2026-11-17 under the AES consolidation plan, row 11, for code2-workspace `rule_audit_nightly.py` (the `context-upkeep` job). The only change is where the project graph is read.

## Requirements

### Requirement: Instruction quality findings are advisory

`scripts/audit_instruction_quality.py` SHALL report oversized, misplaced, duplicated and derivable content in the
instruction files of one repository (`--repo-root`) or of every repository in the project graph (`--all`), as text or
`--json`, and SHALL NOT rewrite any instruction file.

Source: Brian, 2026-11-06, approving the harness review's Context row ("i approve": a nightly check for stale or
contradicting rules); carried over unchanged from Project Meta `f6f0d6f91`.

#### Scenario: quality-findings-are-advisory

- **WHEN** a repository's instruction file is longer than the line budget
- **THEN** the audit reports an `oversized` finding and the file is unchanged

### Requirement: Freshness comes from git history

`scripts/scan_doc_freshness_ecosystem.py` SHALL date each active repository's root instruction file (AGENTS.md, else
legacy CLAUDE.md) and top-level `docs/*.md` by the last commit that touched it, and SHALL report the drift against the
repository's last code commit, never a self-declared date header.

Source: carried over unchanged from Project Meta `f6f0d6f91` (Brian, 2026-11-06, as above).

#### Scenario: freshness-comes-from-git-history

- **WHEN** a repository has an AGENTS.md committed in git
- **THEN** the scan names AGENTS.md as its primary document and dates it from git

### Requirement: The project graph comes from the settings

Both audits SHALL read the project graph named by `PROJECT_GRAPH`, else `~/code2/aes-config/PROJECT_GRAPH.json`, unless
a path is given on the command line; they SHALL NOT read a graph beside the script.

Source: inferred by agent, from the aes-config split (Brian, 2026-11-16, "i approve d20 and d21": the machinery is
public, his records are private).

#### Scenario: the-project-graph-comes-from-the-settings

- **WHEN** `PROJECT_GRAPH` is not set
- **THEN** the default graph is `~/code2/aes-config/PROJECT_GRAPH.json`, and when it is set, the named file
