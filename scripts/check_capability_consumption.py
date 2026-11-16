#!/usr/bin/env python3
"""Detect real capability consumption from imports and cross-check declared dependencies.

Two governed surfaces claim to track cross-project reuse, and both are
hand-maintained with no scanner behind them: PROJECT_GRAPH.json's per-repo
``depends_on`` list, and ``capability_ownership_registry.yaml``'s per-capability
``known_consumers`` list. Neither updates when a project actually starts
importing another project's code -- registration only happens if someone
remembers to write it down.

This is a report-only detector, not an enforcement gate. For each active repo
with a resolvable local path, it AST-walks the repo's Python files, infers
which other active repos' top-level packages it imports, reads which other
repos' folders its code names by path (``~/code2/B/...``) and which of their
commands it runs, and flags two gaps:

1. ``undeclared_project_dependency`` -- repo A imports repo B's package, names
   a path inside B, or runs a command B provides, but B is not in A's
   PROJECT_GRAPH.json ``depends_on``.
2. ``unregistered_capability_consumer`` -- repo A imports repo B's package,
   and B is a capability registry ``source_project``, but A is not in that
   capability's ``known_consumers``.

Only active repos with a local path that resolves on *this* machine can be
scanned; repos with an unresolvable path are reported separately as
"unverifiable" rather than silently treated as dependency-free.

Usage:
    python scripts/check_capability_consumption.py           # report only; writes nothing
    python scripts/check_capability_consumption.py --json
    python scripts/check_capability_consumption.py --write   # add detected links to depends_on
    python scripts/check_capability_consumption.py --capability-registry FILE   # also check known_consumers

``--write`` only adds: a hand-written ``depends_on`` entry is never removed,
because a dependency can be real without anything the scan sees (an HTTP API,
a shared file format).

HTTP links are not detected, by design. A local port has no owner (5173 is
served by six repos, 8765 by three), and nothing maps a public hostname to
the repo behind it. On 2026-10-26, 1 of about 11 port and hostname candidates
was a real use (ecosystem-ops reading the Paperclip board), so those links are
written by hand after reading the calling code.

Copied from Project Meta scripts/check_capability_consumption.py (retirement plan step 4, Decision 20). The graph is
one person's own data: --project-graph names it, else the PROJECT_GRAPH environment variable, else it is read from
the private `aes-config` repository (~/code2/aes-config/PROJECT_GRAPH.json). The capability registry is Project
Meta's file and has no home here yet (retirement plan step 5), so it is optional: --capability-registry or the
CAPABILITY_REGISTRY environment variable names it, and without one the known_consumers check is skipped and the
report says so. A missing graph stops the run naming where to put it.
Implements: project-graph-dependency-scan/graph-from-config
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

def default_project_graph() -> Path:
    """The graph named by PROJECT_GRAPH, else the aes-config copy. Read when a scan runs, not at import."""
    return Path(os.path.expanduser(os.environ.get("PROJECT_GRAPH") or "~/code2/aes-config/PROJECT_GRAPH.json"))


def default_capability_registry() -> Path | None:
    """The registry named by CAPABILITY_REGISTRY, or None: the known_consumers check then does not run."""
    named = os.environ.get("CAPABILITY_REGISTRY")
    return Path(os.path.expanduser(named)) if named else None

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    ".tox",
    "node_modules",
    "dist",
    "build",
    "worktrees",
    "archive",
    "repos",
    # Not runtime code: captured copies of other repos' files (a wiki's raw/
    # sources) and probe scripts kept beside plans and docs.
    "raw",
    "docs",
}

# Names too generic to identify an owning repo even when only one repo has a
# package of that name: other repos import their own (or a PyPI) module by it.
GENERIC_PACKAGE_NAMES = {
    "agents", "api", "app", "cli", "common", "config", "core", "data", "lib", "llm",
    "main", "models", "schemas", "scripts", "server", "services", "shared", "src",
    "tests", "tools", "ui", "utils", "web", "world",
} | set(sys.stdlib_module_names)

# Repos with more .py files than this are almost certainly data dumps or
# vendored trees rather than scannable source (seen: a "Personal Data Files"
# repo with 30k+ stray .py files under tmp.* directories). Skip rather than
# hang; report them as unverifiable-by-size, not silently clean.
MAX_PY_FILES_PER_REPO = 3000

# Records that are not a live repository of their own: retired ones, and
# containers/pointers whose path holds other repos.
SKIP_STATUSES = {"deleted", "merged", "archive", "archived"}
SKIP_RECORD_KINDS = {"container", "pointer"}


@dataclass
class ConsumptionScanResult:
    """Serializable scan result."""

    repos_scanned: list[str] = field(default_factory=list)
    repos_unverifiable: list[str] = field(default_factory=list)
    repos_skipped_oversized: list[str] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)
    capability_registry: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)


def _normalize(name: str) -> str:
    """Normalize a project/package identifier for loose matching."""
    return name.strip().lower().replace("-", "_")


def _resolve_path(raw: str | None) -> Path | None:
    """Resolve a repo-graph path string to a local directory, or None."""
    if not raw:
        return None
    candidate = Path(raw).expanduser()
    return candidate if candidate.is_dir() else None


def _iter_py_files(repo_root: Path):
    """Yield repo_root's .py files, pruning SKIP_DIRS, dot-dirs and nested git repos.

    Pruning happens before descent, so a ``.venv`` or ``node_modules`` costs
    nothing; a nested repository is its own record and is scanned on its own.
    """
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in SKIP_DIRS
            and not d.startswith(".")
            and not (Path(dirpath, d, ".git").exists())
        ]
        for name in filenames:
            if name.endswith(".py"):
                yield Path(dirpath, name)


def _package_names_for_repo(repo_root: Path) -> set[str]:
    """Infer this repo's importable top-level package names.

    Combines the declared pyproject.toml project name (dash-normalized) with
    any top-level directory that looks like a Python package (has __init__.py).
    Heuristic, not authoritative -- a repo with an unconventional layout may
    be under- or over-detected.
    """
    names: set[str] = set()
    pyproject = repo_root / "pyproject.toml"
    if pyproject.exists():
        try:
            import tomllib

            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            name = data.get("project", {}).get("name")
            if isinstance(name, str) and name:
                names.add(_normalize(name))
        except Exception:
            pass
    for base in (repo_root, repo_root / "src"):
        try:
            children = list(base.iterdir())
        except OSError:
            continue
        for child in children:
            if (
                child.is_dir()
                and child.name not in SKIP_DIRS
                and not child.name.startswith(".")
                and child.name.isidentifier()
                and (child / "__init__.py").exists()
            ):
                names.add(child.name)
    return names


_IMPORT_CACHE: dict[Path, set[str]] = {}
_LOCAL_NAMES_CACHE: dict[Path, set[str]] = {}


def _local_module_names(repo_root: Path) -> set[str]:
    """Return every directory name and .py stem inside repo_root (pruned, cached).

    An import of one of these names resolves inside the repo itself (``import
    core`` next to its own ``core/``), so it is not evidence of a dependency on
    another repo that happens to own a package of the same generic name.
    """
    if repo_root in _LOCAL_NAMES_CACHE:
        return _LOCAL_NAMES_CACHE[repo_root]
    names: set[str] = set()
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in SKIP_DIRS
            and not d.startswith(".")
            and not (Path(dirpath, d, ".git").exists())
        ]
        names.update(dirnames)
        names.update(name[:-3] for name in filenames if name.endswith(".py"))
    _LOCAL_NAMES_CACHE[repo_root] = names
    return names


def _collect_imports(repo_root: Path) -> set[str]:
    """AST-walk repo_root's .py files and collect top-level imported module names (cached)."""
    if repo_root in _IMPORT_CACHE:
        return _IMPORT_CACHE[repo_root]
    imports: set[str] = set()
    _IMPORT_CACHE[repo_root] = imports
    for path in _iter_py_files(repo_root):
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source, filename=str(path))
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    imports.add(node.module.split(".")[0])
    return imports


HOME = Path.home()

# Code that can run another repo's file or command: Python string literals
# (docstrings excluded), shell, Makefiles, systemd units and JS/TS. Data files
# and notes only mention paths, so they are not read for references.
REFERENCE_SUFFIXES = {".py", ".sh", ".bash", ".js", ".mjs", ".ts", ".service", ".timer"}
REFERENCE_FILE_NAMES = {"Makefile", "justfile", "Dockerfile"}
# Beyond SKIP_DIRS: tests and fixtures, one-off proposal and dataset scripts,
# and the enforced_planning copy every governed repo vendors.
REFERENCE_SKIP_DIRS = SKIP_DIRS | {
    "tests", "test", "fixtures", "examples", "generated", "logs", "data", "output", "outputs",
    "proposals", "datasets", "enforced_planning",
}
# Machine-wide wrappers on ~/.local/bin that nearly every repo calls; a link for
# each would only say "runs on Brian's machine".
MACHINE_TOOL_COMMANDS = {
    "gh-insidesuccess", "gh-personal", "gh-auth-git-credential-personal",
    "storage-policy", "run-artifacts",
}
_PATH_RE = re.compile(
    r"(?:~|/home/[A-Za-z0-9_.-]+|\$HOME|\$\{HOME\})/((?:code2?|projects)/[A-Za-z0-9_.-]+)"
)
_PATHLIB_RE = re.compile(
    r"Path\.home\(\)\s*/\s*[\"']((?:code2?|projects))(?:[\"']\s*/\s*[\"']|/)([A-Za-z0-9_.-]+)"
)

_REFERENCE_CACHE: dict[Path, tuple[set[tuple[str, str]], str]] = {}


def _iter_reference_files(repo_root: Path):
    """Yield repo_root's code files that can reference another repo (pruned like _iter_py_files)."""
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in REFERENCE_SKIP_DIRS
            and not d.startswith(".")
            and not (Path(dirpath, d, ".git").exists())
        ]
        for name in filenames:
            if name.startswith("test_") or ".test." in name or ".spec." in name:
                continue
            if name in REFERENCE_FILE_NAMES or Path(name).suffix in REFERENCE_SUFFIXES:
                yield Path(dirpath, name)


def _code_text(path: Path, text: str) -> str:
    """Return the part of a file that is code: Python non-docstring strings, else non-comment lines."""
    if path.suffix != ".py":
        return "\n".join(
            line for line in text.splitlines() if not line.lstrip().startswith(("#", "//"))
        )
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return ""
    docstrings: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            first = node.body[0] if node.body else None
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                docstrings.add(id(first.value))
    strings = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings
    ]
    # Path.home() / "code2" / "repo" splits the path across literals; keep the call text.
    calls = [match.group(0) for match in _PATHLIB_RE.finditer(text)]
    return "\n".join(strings + calls)


def _collect_references(repo_root: Path) -> set[tuple[str, str]]:
    """Return (workspace-relative path like "code2/repo", file) pairs found in repo_root's code (cached).

    The joined code text is cached beside them, so command names, known only
    after every repo is indexed, are matched without reading the files again.
    """
    if repo_root in _REFERENCE_CACHE:
        return _REFERENCE_CACHE[repo_root][0]
    paths: set[tuple[str, str]] = set()
    chunks: list[str] = []
    for path in _iter_reference_files(repo_root):
        try:
            if path.stat().st_size > 400_000:
                continue
            text = _code_text(path, path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
        rel = str(path.relative_to(repo_root))
        for match in _PATH_RE.finditer(text):
            paths.add((match.group(1), rel))
        for match in _PATHLIB_RE.finditer(text):
            paths.add((f"{match.group(1)}/{match.group(2)}", rel))
        chunks.append(f"\0{rel}\0\n{text}")
    _REFERENCE_CACHE[repo_root] = (paths, "\n".join(chunks))
    return paths


def _command_owners(roots: dict[str, Path]) -> dict[str, str]:
    """Map a distinctive command name to the one repo that provides it.

    Sources: pyproject.toml ``[project.scripts]`` and ``~/.local/bin`` symlinks
    into a repo. A name is kept only when one repo provides it, it is not
    itself a repo name (those match prose, not invocations), it has a dash or
    underscore and five or more characters, and it is not a machine-wide tool.
    """
    import tomllib

    by_dir = {root.resolve(): repo_id for repo_id, root in roots.items()}
    providers: dict[str, set[str]] = {}
    for repo_id, root in roots.items():
        pyproject = root / "pyproject.toml"
        try:
            scripts = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {}).get("scripts") or {}
        except (OSError, ValueError):
            scripts = {}
        for name in scripts:
            providers.setdefault(name, set()).add(repo_id)
    bin_dir = HOME / ".local" / "bin"
    for link in bin_dir.iterdir() if bin_dir.is_dir() else []:
        if not link.is_symlink():
            continue
        target = link.resolve()
        for parent in target.parents:
            if parent in by_dir:
                providers.setdefault(link.name, set()).add(by_dir[parent])
                break
    repo_names = {_normalize(r) for r in roots} | {_normalize(root.name) for root in roots.values()}
    return {
        name: next(iter(owners))
        for name, owners in providers.items()
        if len(owners) == 1
        and len(name) >= 5
        and ("-" in name or "_" in name)
        and _normalize(name) not in repo_names
        and name not in MACHINE_TOOL_COMMANDS
    }


def _reference_links(
    repo_id: str, root: Path, roots: dict[str, Path], command_owner: dict[str, str]
) -> dict[str, set[str]]:
    """Return provider id -> evidence ("path code2/x in f", "runs cmd in f") for one repo's code."""
    by_dir = {r.resolve(): rid for rid, r in roots.items()}
    via: dict[str, set[str]] = {}
    _collect_references(root)
    paths, text = _REFERENCE_CACHE[root]
    for rel_path, file in paths:
        try:
            target = (HOME / rel_path).resolve()
        except OSError:
            continue
        owner = next((by_dir[p] for p in (target, *target.parents) if p in by_dir), None)
        if owner and owner != repo_id:
            via.setdefault(owner, set()).add(f"path ~/{rel_path} in {file}")
    if command_owner and text:
        names = "|".join(sorted(map(re.escape, command_owner), key=len, reverse=True))
        # Shell-like files: the name as a word anywhere on a code line. Python:
        # a string that starts with the command (``["na-brain", ...]``, ``"na-brain run"``).
        # JS/TS strings name skills, jobs and labels too often to count.
        shell = re.compile(r"(?<![\w./-])(" + names + r")(?![\w.:-])")
        python = re.compile(r"^\s*(?:\S*/)?(" + names + r")(?=\s|$)", re.M)
        parts = text.split("\0")
        # parts: ["", rel, "\n<text>", rel, "\n<text>", ...]
        for i in range(1, len(parts) - 1, 2):
            file, body = parts[i], parts[i + 1]
            suffix = Path(file).suffix
            if suffix == ".py":
                pattern = python
            elif suffix in {".js", ".mjs", ".ts"}:
                continue
            else:
                pattern = shell
            for match in pattern.finditer(body):
                owner = command_owner[match.group(1)]
                if owner != repo_id:
                    via.setdefault(owner, set()).add(f"runs {match.group(1)} in {file}")
    return via


def _load_project_graph(path: Path) -> list[dict[str, Any]]:
    """Load PROJECT_GRAPH.json's list of repo records; a missing file is a loud stop naming where to put it."""
    if not path.is_file():
        raise FileNotFoundError(
            f"check_capability_consumption: project graph not found at {path}: put it there, "
            "or name it with --project-graph or PROJECT_GRAPH"
        )
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"PROJECT_GRAPH.json root must be a list: {path}")
    return data


def _load_capability_registry(path: Path | None) -> list[dict[str, Any]]:
    """Load capability_ownership_registry.yaml's entries list; no registry named means no entries."""
    if path is None:
        return []
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    entries = data.get("entries")
    return entries if isinstance(entries, list) else []


def _py_file_count_within_limit(repo_root: Path, limit: int) -> bool:
    """Return False as soon as repo_root's .py file count (excluding SKIP_DIRS) exceeds limit."""
    count = 0
    for _ in _iter_py_files(repo_root):
        count += 1
        if count > limit:
            return False
    return True


def build_local_index(
    graph_entries: list[dict[str, Any]],
) -> tuple[dict[str, Path], dict[str, set[str]], list[str], list[str]]:
    """Return (repo_id -> local root, repo_id -> package names, unresolvable ids, oversized ids)."""
    roots: dict[str, Path] = {}
    packages: dict[str, set[str]] = {}
    unresolvable: list[str] = []
    oversized: list[str] = []
    for entry in graph_entries:
        if entry.get("status") in SKIP_STATUSES or entry.get("record_kind") in SKIP_RECORD_KINDS:
            continue
        repo_id = entry.get("id")
        if not isinstance(repo_id, str):
            continue
        root = _resolve_path(entry.get("path"))
        if root is None:
            unresolvable.append(repo_id)
            continue
        if not _py_file_count_within_limit(root, MAX_PY_FILES_PER_REPO):
            oversized.append(repo_id)
            continue
        roots[repo_id] = root
        packages[repo_id] = _package_names_for_repo(root)
    return roots, packages, unresolvable, oversized


def _unambiguous_package_owners(packages: dict[str, set[str]]) -> dict[str, str]:
    """Map package name -> the one repo that claims it, excluding names multiple repos share.

    Vendored/scaffolded packages (every governed repo carries its own local
    ``enforced_planning`` copy) and generic names (``tests``) are claimed by
    many repos independently and carry no real ownership signal -- a name
    only counts as evidence once exactly one active repo claims it.
    """
    counts: dict[str, set[str]] = {}
    for repo_id, names in packages.items():
        for name in names - GENERIC_PACKAGE_NAMES:
            counts.setdefault(name, set()).add(repo_id)
    resolved: dict[str, str] = {}
    for name, owners in counts.items():
        if len(owners) == 1:
            resolved[name] = next(iter(owners))
            continue
        # A fork or second clone carries the same package; the record whose id
        # is the package name is its owner (llm_client vs inside-success-llm-client).
        named = [owner for owner in owners if _normalize(owner) == name]
        if len(named) == 1:
            resolved[name] = named[0]
    return resolved


def detect_project_dependency_gaps(
    graph_entries: list[dict[str, Any]],
    roots: dict[str, Path],
    packages: dict[str, set[str]],
) -> list[dict[str, Any]]:
    """Flag repos that use another active repo without declaring it in depends_on.

    "Use" is an import of its package, a path into its folder, or a run of a
    command it provides; each finding's ``via`` lists that evidence.
    Implements: project-graph-dependency-scan/undeclared-use-is-found
    """
    package_to_owner = _unambiguous_package_owners(packages)
    command_owner = _command_owners(roots)

    by_id = {e["id"]: e for e in graph_entries if isinstance(e.get("id"), str)}
    findings: list[dict[str, Any]] = []
    for repo_id, root in roots.items():
        entry = by_id.get(repo_id, {})
        declared = set(entry.get("depends_on") or [])
        imports = _collect_imports(root) - _local_module_names(root)
        via: dict[str, set[str]] = {}
        for name in imports:
            if name in package_to_owner:
                via.setdefault(package_to_owner[name], set()).add(name)
        via.pop(repo_id, None)
        references = _reference_links(repo_id, root, roots, command_owner)
        for provider_id in sorted((set(via) | set(references)) - declared):
            evidence = [f"import {name}" for name in sorted(via.get(provider_id, ()))]
            evidence += sorted(references.get(provider_id, ()))
            how = "imports a package resolved to" if provider_id in via else "uses a path or command of"
            findings.append(
                {
                    "kind": "undeclared_project_dependency",
                    "consumer": repo_id,
                    "provider": provider_id,
                    "packages": sorted(via.get(provider_id, ())),
                    "via": evidence,
                    "detail": (
                        f"{repo_id} {how} {provider_id} ({evidence[0]}), "
                        f"not listed in PROJECT_GRAPH.json depends_on for {repo_id}"
                    ),
                }
            )
    return findings


def detect_capability_consumer_gaps(
    registry_entries: list[dict[str, Any]],
    roots: dict[str, Path],
    packages: dict[str, set[str]],
) -> list[dict[str, Any]]:
    """Flag repos that import a capability's source_project without appearing in known_consumers."""
    normalized_to_id = {_normalize(repo_id): repo_id for repo_id in roots}
    unambiguous_owner = _unambiguous_package_owners(packages)
    import_cache: dict[str, set[str]] = {}

    def imports_of(repo_id: str) -> set[str]:
        if repo_id not in import_cache:
            import_cache[repo_id] = _collect_imports(roots[repo_id])
        return import_cache[repo_id]

    findings: list[dict[str, Any]] = []
    for entry in registry_entries:
        capability_id = entry.get("capability_id")
        source_project = entry.get("source_project")
        if not isinstance(capability_id, str) or not isinstance(source_project, str):
            continue
        provider_id = normalized_to_id.get(_normalize(source_project))
        if provider_id is None:
            findings.append(
                {
                    "kind": "capability_source_unresolvable",
                    "capability_id": capability_id,
                    "source_project": source_project,
                    "detail": (
                        f"source_project {source_project!r} for capability "
                        f"{capability_id!r} does not resolve to any active repo "
                        "with a local path on this machine -- cannot verify consumption"
                    ),
                }
            )
            continue
        provider_packages = {
            name for name, owner in unambiguous_owner.items() if owner == provider_id
        }
        if not provider_packages:
            continue
        known_consumers = {
            _normalize(c) for c in (entry.get("known_consumers") or []) if isinstance(c, str)
        }
        for consumer_id in roots:
            if consumer_id == provider_id:
                continue
            if _normalize(consumer_id) in known_consumers:
                continue
            if provider_packages & imports_of(consumer_id):
                findings.append(
                    {
                        "kind": "unregistered_capability_consumer",
                        "capability_id": capability_id,
                        "provider": provider_id,
                        "consumer": consumer_id,
                        "detail": (
                            f"{consumer_id} imports {provider_id}'s package but is not "
                            f"listed in known_consumers for capability {capability_id!r}"
                        ),
                    }
                )
    return findings


def _scan_one(root: Path) -> tuple[Path, set[str], set[str], tuple[set[tuple[str, str]], str]]:
    """Return (root, imports, local names, references) for one repo; runs in a worker process."""
    _collect_references(root)
    return root, _collect_imports(root), _local_module_names(root), _REFERENCE_CACHE[root]


def _prefetch(roots: list[Path], workers: int = 8) -> None:
    """Fill the import and local-name caches for every root in parallel processes."""
    from concurrent.futures import ProcessPoolExecutor

    pending = [root for root in roots if root not in _IMPORT_CACHE]
    if not pending:
        return
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for root, imports, local, references in pool.map(_scan_one, pending, chunksize=4):
            _IMPORT_CACHE[root] = imports
            _LOCAL_NAMES_CACHE[root] = local
            _REFERENCE_CACHE[root] = references


def run_scan(
    *,
    project_graph_path: Path | None = None,
    capability_registry_path: Path | None = None,
) -> ConsumptionScanResult:
    """Run the full consumption scan and return a structured result.

    Without a capability registry (argument or CAPABILITY_REGISTRY) only depends_on gaps are found."""
    project_graph_path = project_graph_path or default_project_graph()
    capability_registry_path = capability_registry_path or default_capability_registry()
    graph_entries = _load_project_graph(project_graph_path)
    registry_entries = _load_capability_registry(capability_registry_path)
    roots, packages, unresolvable, oversized = build_local_index(graph_entries)
    _prefetch(list(roots.values()))

    findings = detect_project_dependency_gaps(graph_entries, roots, packages)
    findings.extend(detect_capability_consumer_gaps(registry_entries, roots, packages))

    return ConsumptionScanResult(
        repos_scanned=sorted(roots),
        repos_unverifiable=sorted(unresolvable),
        repos_skipped_oversized=sorted(oversized),
        findings=findings,
        capability_registry=str(capability_registry_path) if capability_registry_path else None,
    )


def write_detected_dependencies(project_graph_path: Path, findings: list[dict[str, Any]]) -> int:
    """Append each undeclared provider to its consumer's depends_on; return links added.

    Only adds, keeps the file's two-space JSON layout, and keeps each list sorted
    after the existing hand-written order.
    Implements: project-graph-dependency-scan/write-only-adds
    """
    entries = _load_project_graph(project_graph_path)
    by_id = {e["id"]: e for e in entries if isinstance(e.get("id"), str)}
    added = 0
    for finding in findings:
        if finding.get("kind") != "undeclared_project_dependency":
            continue
        entry = by_id.get(finding["consumer"])
        if entry is None:
            continue
        current = list(entry.get("depends_on") or [])
        if finding["provider"] in current:
            continue
        current.append(finding["provider"])
        entry["depends_on"] = current
        added += 1
    project_graph_path.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return added


def format_text(result: ConsumptionScanResult) -> str:
    """Format the scan result as human-readable text."""
    lines = [
        f"Scanned {len(result.repos_scanned)} active repos with a resolvable local path "
        f"({len(result.repos_unverifiable)} active repos unverifiable on this machine, "
        f"{len(result.repos_skipped_oversized)} skipped as oversized/non-source).",
    ]
    if result.capability_registry is None:
        lines.append("No capability registry named: the known_consumers check was skipped.")
    lines.append("")
    if not result.findings:
        lines.append("No undeclared-dependency or unregistered-consumer gaps detected.")
        return "\n".join(lines)
    lines.append(f"{len(result.findings)} finding(s):")
    for f in result.findings:
        lines.append(f"- [{f['kind']}] {f['detail']}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-graph",
        default=None,
        help="Path to PROJECT_GRAPH.json (default: $PROJECT_GRAPH, else ~/code2/aes-config/PROJECT_GRAPH.json).",
    )
    parser.add_argument(
        "--capability-registry",
        default=None,
        help="Path to capability_ownership_registry.yaml (default: $CAPABILITY_REGISTRY; none skips that check).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Add each detected undeclared dependency to PROJECT_GRAPH.json depends_on.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the scanner CLI. Report-only: always exits 0 unless a real error occurs."""
    args = parse_args()
    graph = Path(args.project_graph).expanduser().resolve() if args.project_graph else default_project_graph()
    registry = Path(args.capability_registry).expanduser().resolve() if args.capability_registry else None
    try:
        result = run_scan(project_graph_path=graph, capability_registry_path=registry)
    except FileNotFoundError as exc:
        print(f"CRASH: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(format_text(result))
    if args.write:
        added = write_detected_dependencies(graph, result.findings)
        print(f"wrote {added} depends_on link(s) to {graph}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
