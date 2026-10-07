"""Revision-bound characterization and target drift (`RU-AES-CHARACTERIZE`, `SC-GF-006`).

`characterize(root)` records what the repository contains at HEAD under the
governed roots of `.aes/project.yaml`: every file with its blob hash and size,
and for Python files the facts from `characterize_python` (AST only). Files
are read from the HEAD tree (`git ls-tree`), not the working tree or index, so
every fact is a fact about `subject_revision`. `dirty` says whether a tracked
governed file differs from HEAD in the index or working tree; a dirty
characterization still describes HEAD, not what is on disk.

The body is deterministic: sorted paths, no timestamps. `produced_at` is a
separate field, so two runs at one revision differ only there, and the text
report omits it.

`drift(target, characterization)` compares the target with a characterization:
- missing_export / signature_changed: a planned artifact's `exports` names a
  symbol the file does not define at top level, or defines with another
  signature (only when the commitment is written `name(args) -> ret`);
- missing_file: a planned artifact with `exports` whose file is absent;
- orphan / unrealized: `topology.compare_topology` over the characterized files.
Unrealized artifacts are reported but, as in `aes topology check`, are not drift
failures; every other kind is.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Final, Literal

from .characterize_python import PythonFacts, analyze, module_name, parse_export
from .records import StrictModel, TargetRecord, load_project, load_target
from .adopt import legacy_paths
from .topology import compare_topology, normalized_roots

CHARACTERIZATION_SCHEMA: Final = "aes.v0_2.characterization.probe0"
DISTRIBUTION = "agentic-engineering-system"


class CharacterizeError(ValueError):
    """The repository could not be characterized."""


class Producer(StrictModel):
    identity: str
    version: str


class CharacterizedFile(StrictModel):
    path: str
    blob_sha: str
    size: int
    python: PythonFacts | None = None


class Characterization(StrictModel):
    schema_version: Literal["aes.v0_2.characterization.probe0"]
    subject_revision: str
    dirty: bool
    producer: Producer
    governed_roots: list[str]
    files: list[CharacterizedFile]
    produced_at: datetime

    def python_facts(self) -> dict[str, PythonFacts]:
        return {f.path: f.python for f in self.files if f.python is not None}


def _git(root: Path, *args: str, input: bytes | None = None) -> bytes:
    proc = subprocess.run(["git", *args], cwd=root, input=input, capture_output=True, check=False)
    if proc.returncode != 0:
        raise CharacterizeError(f"git {' '.join(args)} failed: {proc.stderr.decode().strip()}")
    return proc.stdout


def _source_checkout_revision(module_file: Path) -> str | None:
    """`git describe --always --dirty` of the checkout that tracks `module_file`, else None.

    None when the file is not inside a Git work tree, or is inside one that does
    not track it (a venv's site-packages under a consumer checkout).
    """
    def git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
        except FileNotFoundError:  # no git executable: the checkout cannot be described
            return None

    top = git(module_file.parent, "rev-parse", "--show-toplevel")
    if top is None or top.returncode != 0:
        return None
    toplevel = Path(top.stdout.strip())
    tracked = git(toplevel, "ls-files", "--error-unmatch", "--", str(module_file))
    if tracked is None or tracked.returncode != 0:
        return None
    described = git(toplevel, "describe", "--always", "--dirty")
    if described is None or described.returncode != 0:
        raise CharacterizeError(
            f"{module_file} is tracked by {toplevel}, but git describe failed there: "
            f"{described.stderr.strip() if described else 'git not found'}"
        )
    return described.stdout.strip()


def running_version(module_file: Path | None = None) -> str:
    """The AES version of the code that is actually executing.

    `importlib.metadata` names what was installed, which in an editable venv
    shared by linked worktrees is the main checkout's install-time version
    (§13 of `24-pre-probe-decisions.md`). When the running module is tracked by
    a Git checkout, that checkout's `git describe --always --dirty` is appended:
    `0.1.dev371+g4979c9df8 (running: 3833a8b-dirty)`. Otherwise the installed
    version alone. Neither determinable fails.
    """
    module_file = Path(module_file or __file__).resolve()
    try:
        installed: str | None = version(DISTRIBUTION)
    except PackageNotFoundError:
        installed = None
    running = _source_checkout_revision(module_file)
    if running is None:
        if installed is None:
            raise CharacterizeError(
                f"distribution {DISTRIBUTION!r} is not installed and {module_file} is not tracked by a Git "
                "checkout; no producer version can be reported"
            )
        return installed
    return f"{installed or 'not installed'} (running: {running})"


def _producer_version() -> str:
    return running_version()


def _read_blobs(root: Path, shas: list[str]) -> dict[str, bytes]:
    """Blob contents by sha, through one `git cat-file --batch` call."""
    if not shas:
        return {}
    out = _git(root, "cat-file", "--batch", input="".join(f"{s}\n" for s in shas).encode())
    blobs: dict[str, bytes] = {}
    pos = 0
    for sha in shas:
        header_end = out.index(b"\n", pos)
        got, kind, size = out[pos:header_end].decode().split(" ")
        if got != sha or kind != "blob":
            raise CharacterizeError(f"git cat-file returned {got} {kind} for {sha}")
        start = header_end + 1
        blobs[sha] = out[start:start + int(size)]
        pos = start + int(size) + 1  # trailing newline after each object
    return blobs


def characterize(root: Path) -> Characterization:
    root = Path(root).resolve()
    project = load_project(root / ".aes" / "project.yaml")
    governed = normalized_roots(project.governed_roots)
    revision = _git(root, "rev-parse", "--verify", "HEAD^{commit}").decode().strip()

    entries: list[tuple[str, str, int]] = []
    for line in _git(root, "ls-tree", "-r", "-l", "-z", "HEAD", "--", *governed).split(b"\0"):
        if not line:
            continue
        meta, path = line.decode().split("\t", 1)
        _mode, kind, sha, size = meta.split()
        if kind != "blob":
            raise CharacterizeError(f"{path}: governed {kind} entries (submodules) are not supported")
        entries.append((path, sha, int(size)))
    entries.sort()

    dirty = bool(_git(root, "status", "--porcelain", "--untracked-files=no", "--", *governed).strip())

    py = [(p, s) for p, s, _ in entries if p.endswith(".py")]
    modules = {module_name(p): p for p, _ in py}
    blobs = _read_blobs(root, sorted({s for _, s in py}))
    facts: dict[str, PythonFacts] = {}
    for path, sha in py:
        try:
            source = blobs[sha].decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CharacterizeError(f"{path}: not UTF-8 at HEAD: {exc}") from exc
        facts[path] = analyze(path, source, modules)

    return Characterization(
        schema_version=CHARACTERIZATION_SCHEMA,
        subject_revision=revision,
        dirty=dirty,
        producer=Producer(identity="aes", version=_producer_version()),
        governed_roots=list(governed),
        files=[CharacterizedFile(path=p, blob_sha=s, size=n, python=facts.get(p)) for p, s, n in entries],
        produced_at=datetime.now(UTC).replace(microsecond=0),
    )


# --------------------------------------------------------------------------- #
# Drift
# --------------------------------------------------------------------------- #

DriftKind = Literal["missing_export", "signature_changed", "missing_file", "orphan", "unrealized"]


@dataclass(frozen=True)
class Drift:
    kind: DriftKind
    path: str
    artifact_id: str | None
    detail: str

    @property
    def failing(self) -> bool:
        return self.kind != "unrealized"


def drift(target: TargetRecord, characterization: Characterization,
          legacy: frozenset[str] = frozenset()) -> list[Drift]:
    files = {f.path: f for f in characterization.files}
    found: list[Drift] = []
    for a in target.planned_artifacts:
        if not a.exports:
            continue
        path = a.locator.exact_path
        if path not in files:
            found.append(Drift("missing_file", path, a.id, f"file with {len(a.exports)} committed export(s) is absent"))
            continue
        facts = files[path].python
        if facts is None or facts.parse_error:
            reason = facts.parse_error if facts else "not characterized as Python (outside the governed roots?)"
            found.append(Drift("missing_export", path, a.id, f"cannot check exports: {reason}"))
            continue
        symbols = {s.name: s for s in facts.symbols}
        for entry in a.exports:
            name, signature = parse_export(entry)
            symbol = symbols.get(name)
            if symbol is None:
                found.append(Drift("missing_export", path, a.id, f"committed export '{name}' is not a top-level public symbol"))
            elif signature is not None and symbol.signature != signature:
                actual = symbol.signature if symbol.signature is not None else f"a {symbol.kind}, no signature"
                found.append(Drift("signature_changed", path, a.id, f"'{name}' committed {signature}, found {actual}"))

    topology = compare_topology(
        tuple(characterization.governed_roots), tuple(files), target, legacy,
    )
    found += [Drift("orphan", p, None, "no planned artifact has this exact_path") for p in topology.orphans]
    found += [Drift("unrealized", p, aid, "planned, no file at this revision") for aid, p in topology.unrealized]
    return found


@dataclass(frozen=True)
class CharacterizeReport:
    characterization: Characterization
    drift: tuple[Drift, ...]

    @property
    def ok(self) -> bool:
        return not any(d.failing for d in self.drift)


def check(root: Path) -> CharacterizeReport:
    root = Path(root).resolve()
    project = load_project(root / ".aes" / "project.yaml")
    target = load_target(root / project.materialization.target_path)
    c = characterize(root)
    return CharacterizeReport(c, tuple(drift(target, c, legacy_paths(root, target))))


def render_report(report: CharacterizeReport) -> str:
    """Text report; deterministic for one revision (no produced_at)."""
    c = report.characterization
    failing = [d for d in report.drift if d.failing]
    lines = [
        f"{'OK' if report.ok else 'DRIFT'} characterize: {c.subject_revision}"
        f"{' (dirty: working tree differs from HEAD; facts are of HEAD)' if c.dirty else ''}",
        f"  producer: {c.producer.identity} {c.producer.version}",
        f"  {len(c.files)} governed file(s) under {c.governed_roots}, "
        f"{sum(f.python is not None for f in c.files)} Python; "
        f"{len(failing)} drift, {len(report.drift) - len(failing)} unrealized",
    ]
    for f in c.files:
        line = f"  {f.path} {f.blob_sha[:12]} {f.size}B"
        if f.python is not None:
            p = f.python
            line += (f" [{p.module}: parse error {p.parse_error}]" if p.parse_error else
                     f" [{p.module}: {len(p.symbols)} public symbol(s), imports {p.imports or 'none'}]")
        lines.append(line)
    for d in report.drift:
        who = f" ({d.artifact_id})" if d.artifact_id else ""
        lines.append(f"  {d.kind}: {d.path}{who} - {d.detail}")
    return "\n".join(lines)
