## Why

The first version of `lockstep check instructions` (#958) counted the global `core.md` (21 KB) toward Codex's
32,768-byte budget, so every repository whose root passed 6.9 KB failed and the check had to ship in warn mode. Codex's
source says the budget covers project files only: `DEFAULT_PROJECT_DOC_MAX_BYTES` is 32 KiB "across all selected
environments", `load_project_instructions` subtracts only project entries, and the global instructions are outside it
(`codex-rs/core/src/agents_md_manager.rs`: "The limit applies only to project files"; openai/codex commit 8011b92b,
read 2026-11-17). Brian's own `~/.codex/config.toml` raises the budget to 131,072 bytes and keeps `CLAUDE.md` as a
fallback filename.

Source: Brian, 2026-11-17: "leets figure this out re core.md this has to be testable and resarch able and might alreayd
be docuemtned"; research result above.

## What Changes

- The default chain is the project-root file `~/code2/AGENTS.md` only; `core.md` is no longer counted.
- AES's own `lockstep.yaml` returns the check to block (the default).
