"""`aes init` and project discovery (`RU-AES-PROJECT`, `SC-GF-001`).

Initialization follows `14-initialization-contract.candidate.yaml`. It creates
exactly the two seed artifacts the contract names and nothing else:

- `.aes/project.yaml` (INIT-PROJECT): adoption identity: project id, governed
  roots, the AES architecture line and the installed version that initialized
  it, the project's primary language (it selects the default test command of
  `aes evidence record`), and where the deferred artifacts will live;
- `.aes/target.yaml` (INIT-TARGET): the first accepted outcome, given on the
  command line. The target is never an empty shell: the other families are
  empty lists, which the contract lists as optional until planning.

The contract's deferred artifacts (analysis, plans, observations, generated
projections) are only named as paths in `project.yaml`; their directories are
not created. Before `.aes/` becomes visible, the staged tree is compared with
the seed set and both records are loaded strictly; any difference refuses.

Refusals (nothing is written): not a Git repository; not the top of its work
tree; `.aes/` already exists; an empty or whitespace outcome or actor; an
invalid project id or governed root. Both files are written into a temporary
sibling directory and renamed to `.aes/` in one step, so a failure part-way
leaves no `.aes/`.

`find_project_root` walks up from a directory to the nearest one holding
`.aes/project.yaml`; every other `aes` command uses it when `--root` is not
given, so commands work from subdirectories and from linked worktrees (which
check out their own `.aes/`).
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from .records import ProjectRecord, TargetRecord, load_project, load_target

AES_DIR = ".aes"
PROJECT_FILE = "project.yaml"
TARGET_FILE = "target.yaml"
SEED_ARTIFACTS = (f"{AES_DIR}/{PROJECT_FILE}", f"{AES_DIR}/{TARGET_FILE}")  # contract seed_artifacts
PROJECT_SCHEMA = "aes.v0_2.project.probe0"
TARGET_SCHEMA = "aes.v0_2.target.probe0"
ARCHITECTURE_LINE = "AES-v0.2"
DISTRIBUTION = "agentic-engineering-system"
FIRST_OUTCOME_ID = "OUT-001"
_PROJECT_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class ProjectError(ValueError):
    """No project was found or initialization was refused; nothing was written."""


@dataclass(frozen=True)
class InitResult:
    root: Path
    written: tuple[Path, ...]
    project: ProjectRecord
    target: TargetRecord


def find_project_root(start: Path) -> Path:
    """The nearest directory at or above `start` that holds `.aes/project.yaml`."""
    start = Path(start).resolve()
    for directory in (start, *start.parents):
        if (directory / AES_DIR / PROJECT_FILE).is_file():
            return directory
    raise ProjectError(
        f"{start}: no {AES_DIR}/{PROJECT_FILE} here or in any parent directory; "
        f"run `aes init` at the top of the repository, or pass --root"
    )


def _git_top(root: Path) -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], cwd=root, capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        raise ProjectError(f"{root}: not a Git repository ({proc.stderr.strip()})")
    return Path(proc.stdout.strip()).resolve()


def _installed_version() -> str:
    try:
        return version(DISTRIBUTION)
    except PackageNotFoundError as exc:
        raise ProjectError(
            f"distribution {DISTRIBUTION!r} is not installed, so the initializing version cannot be "
            f"recorded; install AES (pip install ...) and rerun"
        ) from exc


def _governed_roots(roots: Sequence[str]) -> list[str]:
    out: list[str] = []
    for root in roots:
        if root.startswith("/") or ".." in Path(root).parts or root.strip("/") == "":
            raise ProjectError(f"governed root must be a relative subdirectory: {root!r}")
        normalized = root.rstrip("/") + "/"
        if normalized in out:
            raise ProjectError(f"governed root given twice: {root!r}")
        out.append(normalized)
    if not out:
        raise ProjectError("at least one governed root is required")
    return out


def _required_text(name: str, value: str) -> str:
    if not value or not value.strip():
        raise ProjectError(f"{name} must be non-empty text; the target is never created as an empty shell")
    return value.strip()


def _documents(
    project_id: str, outcome: str, actor: str, governed_roots: list[str], architecture_line: str,
    language: str,
) -> dict[str, dict[str, Any]]:
    project = {
        "schema_version": PROJECT_SCHEMA,
        "project_id": project_id,
        "aes": {
            "architecture_line": architecture_line,
            "distribution_version": _installed_version(),
            "initialized_at": datetime.now(UTC).isoformat(timespec="seconds"),
        },
        "governed_roots": governed_roots,
        # Where deferred artifacts go once they exist; init creates none of them.
        "materialization": {
            "target_path": f"{AES_DIR}/{TARGET_FILE}",
            "plans_root": f"{AES_DIR}/plans/",
            "observations_root": f"{AES_DIR}/observations/",
            "generated_root": f"{AES_DIR}/generated/",
        },
        "ecosystem": {"primary_language_or_runtime": language},
    }
    target = {
        "schema_version": TARGET_SCHEMA,
        "target_id": f"{project_id}-target",
        "outcomes": [{"id": FIRST_OUTCOME_ID, "actor_or_consumer": actor, "statement": outcome}],
        "normative_items": [],
        "success_criteria": [],
        "components": [],
        "planned_artifacts": [],
        "verification_subjects": [],
    }
    return {PROJECT_FILE: project, TARGET_FILE: target}


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    yaml = YAML()
    yaml.width = 100
    with path.open("x", encoding="utf-8") as fh:
        yaml.dump(data, fh)


def initialize_project(
    root: Path,
    *,
    project_id: str,
    outcome: str,
    actor: str,
    governed_roots: Sequence[str] = ("src/", "tests/"),
    architecture_line: str = ARCHITECTURE_LINE,
    language: str = "python",
    _stage_hook: Callable[[Path], None] | None = None,
) -> InitResult:
    """Write `.aes/project.yaml` and `.aes/target.yaml` at the top of a Git work tree.

    `_stage_hook` runs on the staged directory before it is checked; tests use it
    to prove that an extra artifact in the staged tree refuses the whole init.
    """
    root = Path(root).resolve()
    top = _git_top(root)
    if top != root:
        raise ProjectError(f"{root}: not the top of its Git work tree ({top}); run `aes init` there")
    aes_dir = root / AES_DIR
    if aes_dir.exists() or aes_dir.is_symlink():
        raise ProjectError(f"{aes_dir}: already exists; this project is already initialized")
    if not _PROJECT_ID.fullmatch(project_id or ""):
        raise ProjectError(f"project id must match {_PROJECT_ID.pattern}: {project_id!r}")
    documents = _documents(
        project_id, _required_text("outcome", outcome), _required_text("actor", actor),
        _governed_roots(governed_roots), architecture_line, _required_text("language", language),
    )

    staging = Path(tempfile.mkdtemp(prefix=".aes-init-", dir=root))
    try:
        for name, data in documents.items():
            _write_yaml(staging / name, data)
        if _stage_hook is not None:
            _stage_hook(staging)
        staged = sorted(f"{AES_DIR}/{p.relative_to(staging).as_posix()}" for p in staging.rglob("*"))
        if staged != sorted(SEED_ARTIFACTS):
            extra = sorted(set(staged) - set(SEED_ARTIFACTS))
            raise ProjectError(
                f"refusing to create artifacts the initialization contract does not name "
                f"(deferred or undocumented): {extra or staged}"
            )
        project = load_project(staging / PROJECT_FILE)
        target = load_target(staging / TARGET_FILE)
        os.rename(staging, aes_dir)  # fails rather than merging if .aes/ appeared meanwhile
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return InitResult(root, tuple(root / p for p in SEED_ARTIFACTS), project, target)
