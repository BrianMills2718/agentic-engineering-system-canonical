## Why

Brian's instruction-file policy (`project-meta/docs/ops/SUBTREE_INSTRUCTION_HIERARCHY.md`, "Canonical Rule" and
"Delta-Only Authoring Rules") is one authored `AGENTS.md` per repository, no `CLAUDE.md` with its own content, nested
files that repeat nothing from their parents, and a root small enough that the Codex chain fits its 32,768-byte
budget. Nothing blocks a breach: the audit is advisory (`instruction-audit`), the Project Meta payload check is wired
to no hook, and 32 of 229 repositories' root files are over 12 KB (`hermes-agent` 75,191 bytes). A repository cleanup
needs a check to be judged by first.

Source: Brian, 2026-11-17: "check first." (Decision 19: build the Lockstep check before cleaning the repositories).

## What Changes

- New check `lockstep check instructions` (`src/lockstep/checks/instructions.py`), mode block, warn or off in
  `lockstep.yaml` like the other checks. It reads files only and rewrites none.
- Findings: `payload_over_cap`, `root_oversized`, `claude_md_content`, `duplicated`.
- The advisory `instruction-audit` stays as it is; this check is the blocking subset that has a clear threshold.
- Not in this change: a subtree registry (the Project Meta subtree checker needed one; this check does not), and
  adding the check to other repositories' `make check`.

## Impact

`CHECK_NAMES` in `checks/config.py` gains `instructions`; `checks/cli.py` gains its runner. No repository runs the
check until its `make check` calls it.
