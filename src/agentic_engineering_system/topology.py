"""Governed-root topology check (`RU-AES-TOPOLOGY`, `SC-GF-003`).

Every durable file under a governed root declared in `.aes/project.yaml` must be
a planned artifact with the exact same path in `.aes/target.yaml` (decision D1:
"governed" is a declared namespace, not every tracked file).

"Durable" means in the Git index: tracked or staged. Ignored and untracked files
are not durable, so a build tool writing `*.egg-info/` under `src/` is fine only
while `.gitignore` keeps it out of Git. The index, not the working tree, is what
a commit records, so the same check is correct as a pre-commit gate.

Findings:
- orphan: a durable governed file no planned artifact accounts for. Failure.
- unrealized: a planned artifact under a governed root with no durable file yet.
  Reported, not a failure; planned work legitimately precedes its files.

Bounded generation rules (the second locator form in the candidate topology)
are not implemented: the first consumer has no file that needs one.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .records import TargetRecord, load_project, load_target


class TopologyError(ValueError):
    """The topology could not be computed (not a Git repository, bad root)."""


@dataclass(frozen=True)
class TopologyReport:
    governed_roots: tuple[str, ...]
    governed_files: tuple[str, ...]
    orphans: tuple[str, ...]
    unrealized: tuple[tuple[str, str], ...]  # (artifact id, exact path)

    @property
    def ok(self) -> bool:
        return not self.orphans


def _under(path: str, roots: tuple[str, ...]) -> bool:
    return any(path.startswith(root) for root in roots)


def normalized_roots(roots: list[str]) -> tuple[str, ...]:
    out = []
    for root in roots:
        if root.startswith("/") or ".." in Path(root).parts or root.strip("/") == "":
            raise TopologyError(f"governed root must be a relative subdirectory: {root!r}")
        out.append(root.rstrip("/") + "/")
    return tuple(out)


def _indexed_files(root: Path, governed: tuple[str, ...]) -> tuple[str, ...]:
    proc = subprocess.run(
        ["git", "ls-files", "--cached", "-z", "--", *governed],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        raise TopologyError(f"{root}: git ls-files failed: {proc.stderr.strip()}")
    return tuple(sorted(p for p in proc.stdout.split("\0") if p))


def check_topology(root: Path) -> TopologyReport:
    root = Path(root).resolve()
    project = load_project(root / ".aes" / "project.yaml")
    target = load_target(root / project.materialization.target_path)
    governed = normalized_roots(project.governed_roots)

    return compare_topology(governed, _indexed_files(root, governed), target)


def compare_topology(governed: tuple[str, ...], files: tuple[str, ...], target: TargetRecord) -> TopologyReport:
    """Orphans and unrealized artifacts for a given governed file list.

    `check_topology` feeds it the Git index; `characterize.drift` feeds it the
    files of the characterized revision, so both apply one rule.
    """
    files = tuple(sorted(files))
    planned = {a.locator.exact_path: a.id for a in target.planned_artifacts}
    present = set(files)
    return TopologyReport(
        governed_roots=governed,
        governed_files=files,
        orphans=tuple(p for p in files if p not in planned),
        unrealized=tuple(
            (aid, path) for path, aid in sorted(planned.items())
            if _under(path, governed) and path not in present
        ),
    )


def render_report(report: TopologyReport) -> str:
    lines = [
        f"{'OK' if report.ok else 'FAIL'} topology: {len(report.governed_files)} governed file(s) "
        f"under {list(report.governed_roots)}, {len(report.orphans)} orphan(s), "
        f"{len(report.unrealized)} planned but not yet realized",
    ]
    for path in report.orphans:
        lines.append(f"  orphan: {path}")
    if report.orphans:
        lines.append(
            "  fix: add a planned_artifacts entry with this exact_path to the target, "
            "move the file outside the governed roots, or remove it from Git"
        )
    for aid, path in report.unrealized:
        lines.append(f"  unrealized: {aid} -> {path}")
    return "\n".join(lines)
