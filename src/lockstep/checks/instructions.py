"""Instructions check: the agent instruction files of one repository obey the size, filename and delta-only rules.

Reads files only; rewrites none. Findings: `payload_over_cap` (the chain files that exist plus the root
`AGENTS.md` are over 32,768 bytes, the Codex budget), `root_oversized` (the root `AGENTS.md` alone is over 12,000
bytes), `claude_md_content` (a `CLAUDE.md` holding anything but `@AGENTS.md`) and `duplicated` (a nested
`AGENTS.md` repeating three or more long lines of one above it).

Implements: lockstep-checks/instructions-the-agent-chain-fits-its-budget,
    lockstep-checks/instructions-no-claude-md-with-its-own-content,
    lockstep-checks/instructions-a-nested-file-repeats-nothing-from-its-parents,
    lockstep-checks/instructions-count-line-and-exit-status

Requirement text (generated):
    lockstep-checks/instructions-the-agent-chain-fits-its-budget: The instructions check SHALL
        report `payload_over_cap` when the byte sizes of the chain files that exist (default
        `~/code2/AGENTS.md`, the project-root file Codex reads above the repository's own; `--chain
        FILE`, repeatable, or `INSTRUCTION_CHAIN` separated by the path separator, replace it) plus
        the repository's root `AGENTS.md` add up to more than 32,768 bytes, and `root_oversized`
        when the root `AGENTS.md` alone is more than 12,000 bytes. The global `~/.codex/AGENTS.md`
        SHALL NOT be counted, because Codex's budget (`project_doc_max_bytes`) applies to project
        files only.
    lockstep-checks/instructions-no-claude-md-with-its-own-content: The instructions check SHALL
        report `claude_md_content` for every `CLAUDE.md` in the repository (outside `.git`,
        `node_modules`, virtual environments, `worktrees` and `*_worktrees` folders) whose content
        is anything other than the single line `@AGENTS.md`. A pure pointer is counted, not
        reported.
    lockstep-checks/instructions-a-nested-file-repeats-nothing-from-its-parents: The instructions
        check SHALL report `duplicated` for a nested `AGENTS.md` that has three or more lines of 40
        or more characters, after trimming, identical to lines of an `AGENTS.md` above it in the
        same repository.
    lockstep-checks/instructions-count-line-and-exit-status: The instructions check SHALL print one
        count line `instructions: files=N payload_bytes=N payload_over_cap=N root_oversized=N
        claude_md_content=N duplicated=N`, then one line per finding (kind, path, reason), and exit
        0 when there is no finding and 1 otherwise. A repository with no `AGENTS.md` prints the
        count line with `files=0` and exits 0.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:instructions.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/instructions-the-agent-chain-fits-its-budget, lockstep-checks/instructions-no-claude-md-with-its-own-content, lockstep-checks/instructions-a-nested-file-repeats-nothing-from-its-parents, lockstep-checks/instructions-count-line-and-exit-status

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

Tested by: tests/lockstep/checks/test_lockstep_check_instructions.py
[[[end]]]
"""

from dataclasses import dataclass, field
import os
from pathlib import Path

PAYLOAD_CAP = 32_768
ROOT_CAP = 12_000
MIN_LINE = 40
MIN_REPEATED = 3
POINTER = "@AGENTS.md"
SKIP = {".git", "node_modules", ".venv", "venv", "__pycache__", "worktrees"}
DEFAULT_CHAIN = ("~/code2/AGENTS.md",)
KINDS = ("payload_over_cap", "root_oversized", "claude_md_content", "duplicated")


@dataclass(frozen=True)
class Finding:
    """One breach: its kind, the file (relative to the repository), and the reason."""

    kind: str
    where: str
    reason: str


@dataclass
class Result:
    """What the check saw and every breach it found."""

    files: int = 0
    payload_bytes: int = 0
    findings: list[Finding] = field(default_factory=list)

    def count_line(self) -> str:
        """Return the one-line summary the command prints first."""
        counts = " ".join(f"{k}={sum(f.kind == k for f in self.findings)}" for k in KINDS)
        return f"instructions: files={self.files} payload_bytes={self.payload_bytes} {counts}"


def default_chain() -> list[Path]:
    """Return the chain files from `INSTRUCTION_CHAIN` (path-separated), else the workspace defaults."""
    env = os.environ.get("INSTRUCTION_CHAIN")
    raw = [p for p in env.split(os.pathsep) if p] if env is not None else list(DEFAULT_CHAIN)
    return [Path(p).expanduser() for p in raw]


def _walk(root: Path) -> list[Path]:
    """Return every `AGENTS.md` and `CLAUDE.md` under root, skipping tool, environment and worktree folders."""
    found: list[Path] = []
    for here, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not d.endswith("_worktrees"))
        found += [Path(here) / n for n in names if n in ("AGENTS.md", "CLAUDE.md")]
    return found


def _long_lines(path: Path) -> set[str]:
    """Return the trimmed lines of a file that are at least MIN_LINE characters."""
    return {s for s in (line.strip() for line in path.read_text(errors="replace").splitlines()) if len(s) >= MIN_LINE}


def check(root: Path, chain: list[Path] | None = None) -> Result:
    """Judge the instruction files of the repository at `root`.

    Args:
        root: Repository root.
        chain: Files loaded before the repository's own (default: `default_chain()`); missing ones are skipped.

    Returns:
        The counts and findings.
    """
    chain = default_chain() if chain is None else chain
    result = Result()
    files = _walk(root)
    agents = [p for p in files if p.name == "AGENTS.md"]
    result.files = len(agents)
    root_file = root / "AGENTS.md"
    if root_file.is_file():
        size = root_file.stat().st_size
        result.payload_bytes = size + sum(p.stat().st_size for p in chain if p.is_file())
        if size > ROOT_CAP:
            result.findings.append(Finding("root_oversized", "AGENTS.md", f"{size} bytes against {ROOT_CAP}"))
        if result.payload_bytes > PAYLOAD_CAP:
            result.findings.append(Finding("payload_over_cap", "AGENTS.md",
                                           f"chain plus root is {result.payload_bytes} bytes against {PAYLOAD_CAP}"))
    for path in files:
        if path.name == "CLAUDE.md" and path.read_text(errors="replace").strip() != POINTER:
            result.findings.append(Finding("claude_md_content", str(path.relative_to(root)),
                                           f"holds its own content; keep only the line {POINTER} or delete it"))
    for path in agents:
        above = [p for p in agents if p.parent != path.parent and path.parent.is_relative_to(p.parent)]
        if not above:
            continue
        theirs = set().union(*(_long_lines(p) for p in above))
        repeated = len(_long_lines(path) & theirs)
        if repeated >= MIN_REPEATED:
            result.findings.append(Finding("duplicated", str(path.relative_to(root)),
                                           f"{repeated} long lines repeat a parent file"))
    return result
