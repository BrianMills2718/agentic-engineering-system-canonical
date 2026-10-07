"""`aes adopt`: bring an existing repository under AES without planning its old files (`RU-AES-ADOPT`).

AES v0.2 refuses every tracked file under a governed root that the target does not
plan (`topology`). That is right for a new project and stops an old one: its own
`aes init` commit is refused (issue #155) and DIGIMON's ~1,800 files would all need
planning first (issue #180). Following SonarQube's clean-as-you-code and the
ESLint/mypy/Betterer baselines, `aes adopt` freezes today's files in one file:

`.aes/legacy_baseline.json` lists every tracked file under the governed roots at a
named revision, bound to its Git blob, minus files the target already plans. It is
one sorted JSON object with one line per file, never one file per entry.

- **Legacy, not orphan.** A baseline path the target does not plan is legacy:
  `topology`, `characterize` and `reconcile` do not report it as an orphan. A file in
  neither the target nor the baseline is an orphan exactly as before.
- **Unplanned legacy edit.** `commit_rule.judge` refuses a commit that modifies a
  legacy path; the commit rule's own mode decides whether that refuses (enforce) or
  is only logged (observe). Deleting a legacy file is allowed.
- **Only shrinks.** `aes plan accept` calls `prune_baseline`, which drops entries the
  target now plans or Git no longer tracks. Nothing ever adds an entry after adoption.
- **Visible.** `aes status` prints `render_legacy(legacy_state(root))`: the legacy
  share, and how many legacy files changed since adoption (edits that landed in
  observe mode).

A repository without a baseline behaves exactly as before: `legacy_paths` is empty
and `legacy_state` is None.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .project import ProjectError, initialize_project
from .records import TargetRecord, load_project, load_target

BASELINE_PATH = Path(".aes") / "legacy_baseline.json"
SCHEMA_VERSION = "aes.v0_2.legacy_baseline.v1"
_HEX40 = re.compile(r"[0-9a-f]{40}")


class AdoptError(ProjectError):
    """Adoption refused, or the baseline file does not load."""


@dataclass(frozen=True)
class Baseline:
    adopted_at_revision: str
    adopted_at: str
    governed_roots: tuple[str, ...]
    files: dict[str, str]  # path -> blob sha at adopted_at_revision


@dataclass(frozen=True)
class AdoptResult:
    root: Path
    baseline: Baseline
    initialized: bool  # .aes/ was created by this adoption
    dry_run: bool
    written: tuple[Path, ...]
    already_planned: int  # tracked governed files left out because the target plans them
    not_at_revision: tuple[str, ...]  # indexed governed files absent at the revision: still orphans


@dataclass(frozen=True)
class LegacyState:
    adopted_at_revision: str
    governed: int  # governed files in the Git index
    legacy: int  # of those, still in the baseline and not planned
    changed: tuple[str, ...]  # legacy files whose indexed blob differs from the baseline's


def _git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise AdoptError(f"git {' '.join(args)} failed in {root}: {done.stderr.strip()}")
    return done.stdout


def _roots(roots: Sequence[str]) -> tuple[str, ...]:
    from .topology import TopologyError, normalized_roots

    try:
        return normalized_roots(list(roots))
    except TopologyError as exc:
        raise AdoptError(str(exc)) from exc


def _tree_blobs(root: Path, revision: str, roots: tuple[str, ...]) -> dict[str, str]:
    out = _git(root, "ls-tree", "-r", "-z", "--full-tree", revision, "--", *roots)
    blobs = {}
    for entry in filter(None, out.split("\0")):
        meta, path = entry.split("\t", 1)
        _mode, kind, sha = meta.split()
        if kind == "blob":  # submodules (commit) are not files of this repository
            blobs[path] = sha
    return blobs


def _index_blobs(root: Path, roots: tuple[str, ...]) -> dict[str, str]:
    out = _git(root, "ls-files", "-s", "-z", "--", *roots)
    blobs = {}
    for entry in filter(None, out.split("\0")):
        meta, path = entry.split("\t", 1)
        blobs[path] = meta.split()[1]
    return blobs


def _planned(target: TargetRecord) -> set[str]:
    return {a.locator.exact_path for a in target.planned_artifacts}


def _dump(b: Baseline) -> str:
    return json.dumps({
        "schema_version": SCHEMA_VERSION,
        "adopted_at_revision": b.adopted_at_revision,
        "adopted_at": b.adopted_at,
        "governed_roots": list(b.governed_roots),
        "files": dict(sorted(b.files.items())),
    }, indent=1) + "\n"


def load_baseline(root: Path) -> Baseline | None:
    """The baseline, or None when the repository was never adopted. A malformed file is an error."""
    path = Path(root) / BASELINE_PATH
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise AdoptError(f"{path}: not valid JSON: {exc}") from exc
    problems = []
    if not isinstance(data, dict):
        raise AdoptError(f"{path}: expected a JSON object")
    if data.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"schema_version must be {SCHEMA_VERSION!r}, not {data.get('schema_version')!r}")
    if not _HEX40.fullmatch(str(data.get("adopted_at_revision", ""))):
        problems.append("adopted_at_revision must be a 40-hex commit id")
    roots = data.get("governed_roots")
    if not isinstance(roots, list) or not all(isinstance(r, str) for r in roots):
        problems.append("governed_roots must be a list of directories")
    files = data.get("files")
    if not isinstance(files, dict) or not all(isinstance(k, str) and _HEX40.fullmatch(str(v)) for k, v in files.items()):
        problems.append("files must map each path to its 40-hex blob id")
    if problems:
        raise AdoptError(f"{path}: " + "; ".join(problems))
    return Baseline(data["adopted_at_revision"], str(data.get("adopted_at", "")), tuple(roots), dict(files))


def _write(root: Path, baseline: Baseline, *, exclusive: bool) -> Path:
    path = root / BASELINE_PATH
    if exclusive:
        with path.open("x", encoding="utf-8") as fh:
            fh.write(_dump(baseline))
    else:
        staging = path.with_name(f".{path.name}.tmp")
        staging.write_text(_dump(baseline), encoding="utf-8")
        staging.replace(path)
    return path


def adopt(
    root: Path,
    *,
    revision: str = "HEAD",
    dry_run: bool = False,
    project_id: str | None = None,
    actor: str | None = None,
    outcome: str | None = None,
    governed_roots: Sequence[str] | None = None,
    language: str = "python",
    now: datetime | None = None,
) -> AdoptResult:
    """Write the legacy baseline at `revision`; initialize the project first when it has no `.aes/`."""
    root = Path(root).resolve()
    if (root / BASELINE_PATH).exists():
        raise AdoptError(f"{root / BASELINE_PATH}: already exists; a repository is adopted once and its "
                         f"baseline only shrinks (aes plan accept prunes it)")
    top = Path(_git(root, "rev-parse", "--show-toplevel").strip()).resolve()
    if top != root:
        raise AdoptError(f"{root}: not the top of its Git work tree ({top}); run `aes adopt` there")
    initialized = not (root / ".aes" / "project.yaml").is_file()
    if initialized:
        missing = [f"--{n}" for n, v in (("project-id", project_id), ("actor", actor), ("outcome", outcome)) if not v]
        if missing:
            raise AdoptError(f"{root}: no .aes/ yet, so aes adopt initializes the project and needs "
                             f"{', '.join(missing)} (the same as aes init)")
        roots = _roots(governed_roots or ("src/", "tests/"))
        planned: set[str] = set()
    else:
        given = [n for n, v in (("--project-id", project_id), ("--actor", actor), ("--outcome", outcome),
                                ("--governed-root", governed_roots)) if v]
        if given:
            raise AdoptError(f"{root}: already initialized; aes adopt only writes the baseline here, "
                             f"so {', '.join(given)} would be ignored: drop them")
        project = load_project(root / ".aes" / "project.yaml")
        roots = _roots(project.governed_roots)
        planned = _planned(load_target(root / project.materialization.target_path))

    sha = _git(root, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}").strip()
    tree = _tree_blobs(root, sha, roots)
    files = {p: b for p, b in tree.items() if p not in planned}
    if not files:
        raise AdoptError(f"no unplanned tracked file under {list(roots)} at {sha[:12]}: there is nothing to "
                         f"adopt; use aes init (a new project) or check --governed-root")
    not_at_revision = tuple(sorted(p for p in _index_blobs(root, roots) if p not in tree and p not in planned))
    baseline = Baseline(
        adopted_at_revision=sha,
        adopted_at=(now or datetime.now(UTC)).replace(microsecond=0).isoformat(),
        governed_roots=roots,
        files=files,
    )
    written: list[Path] = []
    if not dry_run:
        if initialized:
            done = initialize_project(root, project_id=project_id or "", actor=actor or "", outcome=outcome or "",
                                      governed_roots=list(roots), language=language)
            written += done.written
        written.append(_write(root, baseline, exclusive=True))
    return AdoptResult(root, baseline, initialized, dry_run, tuple(written),
                       already_planned=len(tree) - len(files), not_at_revision=not_at_revision)


def legacy_paths(root: Path, target: TargetRecord | None = None) -> frozenset[str]:
    """Baseline paths the target does not plan; empty for a repository never adopted."""
    root = Path(root)
    baseline = load_baseline(root)
    if baseline is None:
        return frozenset()
    if target is None:
        project = load_project(root / ".aes" / "project.yaml")
        target = load_target(root / project.materialization.target_path)
    return frozenset(baseline.files) - _planned(target)


def legacy_state(root: Path) -> LegacyState | None:
    root = Path(root).resolve()
    baseline = load_baseline(root)
    if baseline is None:
        return None
    project = load_project(root / ".aes" / "project.yaml")
    planned = _planned(load_target(root / project.materialization.target_path))
    index = _index_blobs(root, _roots(project.governed_roots))
    legacy = [p for p in baseline.files if p in index and p not in planned]
    return LegacyState(baseline.adopted_at_revision, len(index), len(legacy),
                       tuple(sorted(p for p in legacy if index[p] != baseline.files[p])))


def prune_baseline(root: Path) -> tuple[str, ...]:
    """Drop entries the target now plans or Git no longer tracks; return them (sorted)."""
    root = Path(root).resolve()
    baseline = load_baseline(root)
    if baseline is None:
        return ()
    project = load_project(root / ".aes" / "project.yaml")
    planned = _planned(load_target(root / project.materialization.target_path))
    tracked = set(_index_blobs(root, _roots(project.governed_roots)))
    keep = {p: b for p, b in baseline.files.items() if p not in planned and p in tracked}
    removed = tuple(sorted(set(baseline.files) - set(keep)))
    if removed:
        _write(root, Baseline(baseline.adopted_at_revision, baseline.adopted_at, baseline.governed_roots, keep),
               exclusive=False)
    return removed


def tracked_under(root: Path, roots: Sequence[str]) -> int:
    """How many tracked files the governed roots already hold (aes init warns when non-zero)."""
    return len(_index_blobs(Path(root), _roots(roots)))


def render_adopted(r: AdoptResult) -> str:
    b = r.baseline
    by_root = {root: sum(p.startswith(root) for p in b.files) for root in b.governed_roots}
    lines = [
        f"{'would adopt (dry run, nothing written)' if r.dry_run else 'adopted'} at {b.adopted_at_revision}",
        f"  {len(b.files)} legacy file(s) under {list(b.governed_roots)}: "
        + ", ".join(f"{root} {n}" for root, n in by_root.items()),
        f"  {r.already_planned} already planned in the target (left out)",
        f"  baseline {BASELINE_PATH}: {len(_dump(b).encode())} bytes",
    ]
    if r.not_at_revision:
        lines.append(f"  {len(r.not_at_revision)} indexed file(s) not at {b.adopted_at_revision[:12]} stay orphans "
                     f"until planned or committed before adopting: {', '.join(r.not_at_revision[:5])}"
                     + (" ..." if len(r.not_at_revision) > 5 else ""))
    lines += [f"  wrote {p.relative_to(r.root)}" for p in r.written]
    if not r.dry_run:
        lines.append(f"  next: git add .aes && git commit, then aes hooks install; edit a legacy file only "
                     f"after planning it (aes plan accept removes it from the baseline)")
    return "\n".join(lines)


def render_legacy(s: LegacyState) -> str:
    share = 100.0 * s.legacy / s.governed if s.governed else 0.0
    line = (f"  legacy: {s.legacy} of {s.governed} governed file(s) still in the baseline ({share:.1f}%), "
            f"{len(s.changed)} changed since adoption at {s.adopted_at_revision[:12]}")
    if s.changed:
        line += "\n" + "\n".join(f"    changed legacy: {p}" for p in s.changed[:10])
        if len(s.changed) > 10:
            line += f"\n    ... {len(s.changed) - 10} more"
    return line
