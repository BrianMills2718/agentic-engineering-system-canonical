## MODIFIED Requirements

### Requirement: Instructions: The agent chain fits its budget

The instructions check SHALL report `payload_over_cap` when the byte sizes of the chain files that exist (default
`~/code2/AGENTS.md`, the project-root file Codex reads above the repository's own; `--chain FILE`, repeatable, or
`INSTRUCTION_CHAIN` separated by the path separator, replace it) plus the repository's root `AGENTS.md` add up to more
than 32,768 bytes, and `root_oversized` when the root `AGENTS.md` alone is more than 12,000 bytes. The global
`~/.codex/AGENTS.md` SHALL NOT be counted, because Codex's budget (`project_doc_max_bytes`) applies to project files
only.

Source: Brian, 2026-11-17: "leets figure this out re core.md this has to be testable and resarch able and might alreayd
be docuemtned"; Codex source `codex-rs/core/src/agents_md_manager.rs` (openai/codex 8011b92b): "The limit applies only
to project files." The 12 KB root guidance is in the `instruction-surfaces` skill.

#### Scenario: Instructions: An oversized root fails

- **GIVEN** a repository whose root `AGENTS.md` is 13,000 bytes
- **WHEN** `lockstep check instructions` runs
- **THEN** it reports `root_oversized` and exits 1

#### Scenario: Instructions: A chain over the cap fails

- **GIVEN** a 30,000-byte chain file and a 5,000-byte root `AGENTS.md`
- **WHEN** the check runs with that chain
- **THEN** it reports `payload_over_cap` and exits 1
