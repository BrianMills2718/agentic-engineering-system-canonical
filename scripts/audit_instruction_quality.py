#!/usr/bin/env python3
"""Audit the quality of active project instruction surfaces.

Existing ecosystem checks answer whether instruction files exist, pair with
their Codex projection, and are fresh:

* ``check_agents_mirror.py``       -- active root instruction-file coverage
* ``check_subtree_instructions.py``-- registry-declared nested coverage
* ``scan_doc_freshness_ecosystem.py`` -- staleness against git history
* ``check_repo_documentation_profiles.py`` -- declared authority shape

None of them answer whether a file that exists is any good. This one does, on
the dimensions that actually cost an agent something:

``oversized``
    Instruction files load in full and compete with the conversation for
    context. Claude Code's own guidance is under 200 lines per file, and
    adherence degrades on longer ones.

``misplaced``
    A block in a parent whose every path reference lives under exactly one
    child that has its own instruction file. That content is loaded for all
    sibling work that will never need it. This is the delta-only rule made
    measurable, but it reports a candidate rather than a verdict: a
    repository-wide rule may invoke one directory's tooling and still govern
    the whole repository, so confirm intent before moving a block.

``duplicated``
    Substantive lines a child repeats from its parent. The parent is always in
    context when the child is, so the repetition is pure cost.

``derivable``
    Directory trees and file inventories an agent can read off the filesystem
    more accurately than off a doc that drifts.

Findings are advisory and report-only. Instruction files are prose owned by
their repositories; this reports what to consider moving or cutting and never
rewrites them.

Implements: instruction-audit/instruction-quality-findings-are-advisory
Implements: instruction-audit/the-project-graph-comes-from-the-settings
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# Copied from Project Meta scripts/audit_instruction_quality.py at f6f0d6f91 (AES consolidation plan, "Before item 11", step 5). The only
# change: the project graph is one person's own data, so the PROJECT_GRAPH environment variable names it, else it is read
# from the private `aes-config` repository, as md_file_cap.py does.
DEFAULT_GRAPH_PATH = Path(os.environ.get("PROJECT_GRAPH") or Path.home() / "code2/aes-config/PROJECT_GRAPH.json").expanduser()

LEGACY_INSTRUCTION_FILENAME = "CLAUDE.md"
INSTRUCTION_FILENAME = "AGENTS.md"

# Claude Code documents a target under 200 lines per instruction file; longer files
# consume more context and reduce adherence.
LINE_GUIDANCE = 200

# Lines are a poor proxy on their own. project-meta's root file sits at 188
# lines and 19,429 bytes: it passes a line check while being among the heaviest
# instruction files in the repository. Roughly four bytes per token puts this
# threshold near 3k tokens of always-on context.
BYTE_GUIDANCE = 12_000

SKIP_DIRECTORIES = frozenset(
    {
        ".git",
        "worktrees",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "archive",
        "vendor",
        "third_party",
        "site-packages",
        ".claude",
    }
)

# A path-ish token: backticked paths, or bare tokens containing a slash.
_BACKTICKED = re.compile(r"`([^`\n]+)`")
# A heading that introduces navigation rather than rules.
_ROUTING_HEADING = re.compile(
    r"^#+\s*(route|routing|navigat|where\b|contents|index|map\b|layout|structure)",
    re.IGNORECASE,
)
# A bare relative path inside a fenced command, e.g. "scripts/meta/run.py".
_BARE_PATH = re.compile(r"(?<![\w./~-])([A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+)")

# A pointer line: "topic -> `path`" or "`path` - gloss". Routing, not content.
_POINTER_LINE = re.compile(r"(->|\u2192)|^\s*[-*]\s*`[^`]+`\s*[-\u2014:]")

# A rendered tree line, not a markdown bullet: box-drawing glyphs, or the ASCII
# connectors `|--` / `+--` / `` `-- ``. A bare "- item" is a list, not a tree.
_TREE_CONNECTOR = re.compile(r"^\s*(?:[│├└┌┐┘┬┴┼─╭╰]|\|--|\+--|`--|\\--)")

# `|------|------|` opens with a pipe and dashes, so the ASCII-connector branch
# matched every markdown table delimiter. Deleting those breaks the table.
_TABLE_DELIMITER = re.compile(r"^\s*\|[-\s|:]+\|?\s*$")

# A tree line names a file or directory. Flow diagrams drawn with the same
# glyphs -- "├─ [Hypothesis Generation LLM] -> ..." -- are not derivable from a
# checkout, and neither is a layout of runtime output under a gitignored path.
_NAMES_A_PATH = re.compile(r"[A-Za-z0-9_.-]+\.[A-Za-z0-9]+|[A-Za-z0-9_.-]+/")


@dataclass
class Finding:
    """One advisory observation about an instruction file."""

    kind: str
    path: str
    detail: str
    recoverable_bytes: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""

        return {
            "kind": self.kind,
            "path": self.path,
            "detail": self.detail,
            "recoverable_bytes": self.recoverable_bytes,
        }


@dataclass
class RepoReport:
    """Per-repository audit result."""

    repo: str
    files: int = 0
    total_bytes: int = 0
    findings: list[Finding] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""

        return {
            "repo": self.repo,
            "files": self.files,
            "total_bytes": self.total_bytes,
            "findings": [finding.to_dict() for finding in self.findings],
        }


def _read_text(path: Path) -> str | None:
    """Read one instruction file, reporting rather than raising on bad input.

    A single unreadable or non-UTF-8 file must not abort an ecosystem-wide
    audit, but it must not pass silently either.
    """

    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"warning: skipping {path}: {exc}", file=sys.stderr)
        return None


def _instruction_files(repo_root: Path) -> list[Path]:
    """Return instruction files in a repository, skipping derived trees."""

    found: list[Path] = []
    filename = (
        LEGACY_INSTRUCTION_FILENAME
        if (repo_root / LEGACY_INSTRUCTION_FILENAME).is_file()
        else INSTRUCTION_FILENAME
    )
    for path in repo_root.rglob(filename):
        relative = path.relative_to(repo_root)
        if _is_derived(relative.parts[:-1]):
            continue
        if path.is_file():
            found.append(path)
    return sorted(found)


def _is_derived(parts: tuple[str, ...]) -> bool:
    """Return whether a path sits in a derived, vendored, or retired tree.

    Prefix matching matters: retired trees are named ``archive``,
    ``archive_full_record``, ``archived_runs``, and similar. Exact-name
    matching alone let one repository's archived lineage variants supply 138
    of its 150 findings and bury the live ones.
    """

    for part in parts:
        lowered = part.lower()
        if lowered in SKIP_DIRECTORIES:
            return True
        if lowered.startswith(("archive", "archived", "backup", "deprecated", "legacy")):
            return True
    return False


def _blocks(text: str) -> list[tuple[int, str]]:
    """Split instruction prose into logical blocks with their start lines.

    A block is a markdown section body or a standalone paragraph. Fenced code
    is kept with its owning block so a command example is never judged apart
    from the sentence explaining it.
    """

    lines = text.splitlines()
    blocks: list[tuple[int, str]] = []
    current: list[str] = []
    start = 1
    fenced = False

    def flush(end_start: int) -> None:
        body = "\n".join(current).strip()
        if body:
            blocks.append((end_start, body))

    for index, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        is_heading = not fenced and line.startswith("#")
        is_break = not fenced and not line.strip()
        if is_heading:
            flush(start)
            current = [line]
            start = index
            continue
        if is_break and current and not fenced:
            flush(start)
            current = []
            start = index + 1
            continue
        if not current:
            start = index
        current.append(line)
    flush(start)
    return blocks


def _path_tokens(block: str) -> list[str]:
    """Return path-like references from a block, including fenced commands.

    Fenced blocks carry no backticks, so a parent listing thirty commands under
    one subdirectory went undetected while being the single largest misplaced
    block in the ecosystem. Command lines are scanned for bare path tokens too.
    """

    tokens: list[str] = []
    for match in _BACKTICKED.findall(block):
        candidate = match.strip()
        if "/" in candidate and not candidate.startswith(("http", "-")):
            tokens.append(candidate.split()[0])
    for match in _BARE_PATH.findall(block):
        if not match.startswith(("http", "-", "/", "~")):
            tokens.append(match)
    seen: set[str] = set()
    unique: list[str] = []
    for token in tokens:
        normalized = token.rstrip("/")
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(token)
    return unique


def _is_routing(block: str) -> bool:
    """Return whether a block routes to children rather than carrying content.

    The delta-only rule requires parents to point at their children, so a
    routing table is correct by construction and must never be reported as
    misplaced. Dogfooding caught this on the first repaired repository: a
    "Route By Question" list was flagged as content belonging in the child it
    pointed at.
    """

    lines = [line for line in block.splitlines() if line.strip()]
    if not lines:
        return False
    if _ROUTING_HEADING.match(lines[0].strip()):
        return True
    body = [line for line in lines if not line.lstrip().startswith("#")]
    if not body:
        return False
    pointers = sum(1 for line in body if _POINTER_LINE.search(line))
    return pointers / len(body) >= 0.6


def _child_directories(instruction: Path, all_files: set[Path]) -> list[Path]:
    """Return directories below this file that carry their own instructions."""

    parent = instruction.parent
    children: list[Path] = []
    for other in all_files:
        if other == instruction:
            continue
        try:
            other.relative_to(parent)
        except ValueError:
            continue
        children.append(other.parent)
    return children


def _misplaced_blocks(
    instruction: Path, repo_root: Path, children: list[Path]
) -> list[Finding]:
    """Flag blocks whose references all live under one instruction-owning child."""

    if not children:
        return []
    text = _read_text(instruction)
    if text is None:
        return []

    findings: list[Finding] = []
    parent = instruction.parent
    for line_number, block in _blocks(text):
        if _is_routing(block):
            continue
        tokens = _path_tokens(block)
        if len(tokens) < 2:
            # One incidental pointer is routing, which parents are supposed to
            # do. Two or more references all aimed at one child is content.
            continue
        owners: set[Path] = set()
        resolved = 0
        for token in tokens:
            candidate = (parent / token.lstrip("./")).resolve()
            owning = None
            for child in children:
                if candidate == child or child in candidate.parents:
                    if owning is None or len(child.parts) > len(owning.parts):
                        owning = child
            if owning is None:
                if candidate.exists():
                    # Real path in this subtree but owned by no child: content
                    # that legitimately belongs to the parent.
                    owners.add(parent)
                    break
                continue
            resolved += 1
            owners.add(owning)
        if resolved >= 2 and len(owners) == 1:
            owner = next(iter(owners))
            if owner == parent:
                continue
            relative_owner = owner.relative_to(repo_root)
            findings.append(
                Finding(
                    kind="misplaced",
                    path=f"{instruction.relative_to(repo_root)}:{line_number}",
                    detail=(
                        f"Block references only {relative_owner}/ and may belong in "
                        f"{relative_owner}/{instruction.name}; it currently loads for "
                        "all sibling work. Confirm before moving: a repository-wide rule "
                        "can invoke one directory's tooling and still govern everything."
                    ),
                    recoverable_bytes=len(block.encode("utf-8")),
                )
            )
    return findings


def _substantive(line: str) -> bool:
    """Return whether a line carries enough content to count as duplication."""

    stripped = line.strip()
    if len(stripped) < 40:
        return False
    return not stripped.startswith(("#", "|", "```", "---", "<!--"))


def _duplicated(
    instruction: Path, repo_root: Path, all_files: set[Path]
) -> list[Finding]:
    """Flag substantive lines a child repeats from an ancestor already in context."""

    ancestors = [
        other
        for other in all_files
        if other != instruction and other.parent in instruction.parent.parents
    ]
    if not ancestors:
        return []
    own_text = _read_text(instruction)
    if own_text is None:
        return []
    own = {line.strip() for line in own_text.splitlines() if _substantive(line)}
    if not own:
        return []

    inherited: set[str] = set()
    for ancestor in ancestors:
        ancestor_text = _read_text(ancestor)
        if ancestor_text is None:
            continue
        inherited |= {
            line.strip() for line in ancestor_text.splitlines() if _substantive(line)
        }

    repeated = own & inherited
    if not repeated:
        return []
    wasted = sum(len(line.encode("utf-8")) for line in repeated)
    return [
        Finding(
            kind="duplicated",
            path=str(instruction.relative_to(repo_root)),
            detail=(
                f"{len(repeated)} substantive line(s) repeat an ancestor "
                "instruction file that is already in context whenever this one is."
            ),
            recoverable_bytes=wasted,
        )
    ]


def _derivable(instruction: Path, repo_root: Path) -> list[Finding]:
    """Flag rendered directory trees an agent can read from the filesystem."""

    text = _read_text(instruction)
    if text is None:
        return []
    lines = text.splitlines()
    tree_lines = [
        line
        for line in lines
        if _TREE_CONNECTOR.match(line)
        and not _TABLE_DELIMITER.match(line)
        and _NAMES_A_PATH.search(line)
    ]
    if len(tree_lines) < 6:
        return []
    return [
        Finding(
            kind="derivable",
            path=str(instruction.relative_to(repo_root)),
            detail=(
                f"{len(tree_lines)} rendered directory-tree line(s). The filesystem "
                "is more accurate than a tree that drifts, and this competes with "
                "rules for context."
            ),
            recoverable_bytes=sum(len(line.encode("utf-8")) for line in tree_lines),
        )
    ]


def _scope(instruction: Path, repo_root: Path) -> str:
    """Describe when this file loads, which is what its cost depends on."""

    if instruction.parent == repo_root:
        return "repo root, so it loads for all work in the repository"
    return f"subtree {instruction.parent.relative_to(repo_root)}/, so it loads only when working there"


def _oversized(instruction: Path, repo_root: Path) -> list[Finding]:
    """Flag files past the length or weight guidance, ranked by blast radius."""

    text = _read_text(instruction)
    if text is None:
        return []
    line_count = len(text.splitlines())
    byte_count = len(text.encode("utf-8"))
    over_lines = line_count > LINE_GUIDANCE
    over_bytes = byte_count > BYTE_GUIDANCE
    if not (over_lines or over_bytes):
        return []

    excess = max(0, byte_count - BYTE_GUIDANCE)
    breached = []
    if over_lines:
        breached.append(f"{line_count} lines against the {LINE_GUIDANCE}-line guidance")
    if over_bytes:
        breached.append(f"{byte_count} bytes (~{byte_count // 4} tokens) against {BYTE_GUIDANCE}")
    return [
        Finding(
            kind="oversized",
            path=str(instruction.relative_to(repo_root)),
            detail=f"{' and '.join(breached)}. This file is the {_scope(instruction, repo_root)}.",
            # Only the excess over guidance is recoverable, not the whole file:
            # counting the full size double-counted every `misplaced` block
            # inside the same file and inflated that repo's rank. A root file is
            # still weighted up, because it is paid on every session in the repo.
            recoverable_bytes=(
                excess if instruction.parent == repo_root else excess // 8
            ),
        )
    ]


def audit_repo(repo_root: Path) -> RepoReport:
    """Audit one repository's instruction surfaces."""

    report = RepoReport(repo=str(repo_root))
    files = _instruction_files(repo_root)
    file_set = set(files)
    report.files = len(files)

    for instruction in files:
        text = _read_text(instruction)
        if text is None:
            continue
        report.total_bytes += len(text.encode("utf-8"))
        report.findings.extend(_oversized(instruction, repo_root))
        report.findings.extend(_derivable(instruction, repo_root))
        report.findings.extend(_duplicated(instruction, repo_root, file_set))
        children = _child_directories(instruction, file_set)
        report.findings.extend(_misplaced_blocks(instruction, repo_root, children))

    report.findings.sort(key=lambda f: (-f.recoverable_bytes, f.kind, f.path))
    return report


def _graph_repos(graph_path: Path, status: str) -> list[Path]:
    """Resolve active repository roots from the project graph."""

    payload = json.loads(graph_path.read_text(encoding="utf-8"))
    entries = payload.get("projects", payload) if isinstance(payload, dict) else payload
    if isinstance(entries, dict):
        entries = list(entries.values())

    roots: list[Path] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if status and entry.get("status") != status:
            continue
        raw = entry.get("path") or entry.get("root")
        if not isinstance(raw, str) or not raw:
            continue
        root = Path(raw).expanduser()
        if root.is_dir():
            roots.append(root.resolve())
    return sorted(set(roots))


def _print_human(reports: list[RepoReport]) -> None:
    """Render a reviewer-facing summary ordered by recoverable context."""

    ranked = sorted(
        reports,
        key=lambda r: -sum(f.recoverable_bytes for f in r.findings),
    )
    total_findings = sum(len(r.findings) for r in reports)
    print(
        f"Audited {len(reports)} repo(s), "
        f"{sum(r.files for r in reports)} instruction file(s), "
        f"{sum(r.total_bytes for r in reports)} bytes. "
        f"{total_findings} finding(s)."
    )
    for report in ranked:
        if not report.findings:
            continue
        recoverable = sum(f.recoverable_bytes for f in report.findings)
        print(f"\n{report.repo}  ({len(report.findings)} findings, ~{recoverable} recoverable bytes)")
        for finding in report.findings[:12]:
            print(f"  [{finding.kind}] {finding.path}")
            print(f"      {finding.detail}")
        if len(report.findings) > 12:
            print(f"  ... {len(report.findings) - 12} more")


def main(argv: list[str] | None = None) -> int:
    """Audit instruction-surface quality for one repository or the ecosystem."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, help="Audit a single repository.")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Audit every repository resolved from PROJECT_GRAPH.json.",
    )
    parser.add_argument("--project-graph", type=Path, default=DEFAULT_GRAPH_PATH)
    parser.add_argument("--status", default="active", help="Project graph status filter.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    if args.repo_root:
        roots = [args.repo_root.expanduser().resolve()]
    elif args.all:
        roots = _graph_repos(args.project_graph, args.status)
    else:
        parser.error("pass --repo-root PATH or --all")

    reports = [audit_repo(root) for root in roots if root.is_dir()]

    if args.json:
        print(json.dumps({"repos": [r.to_dict() for r in reports]}, indent=2))
    else:
        _print_human(reports)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
