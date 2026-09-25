"""`aes hooks install`: ship the consumer's pre-commit gate (`RU-AES-DISTRIBUTION`).

The hook runs `aes target validate` and `aes topology check` on every commit, so
an orphan under a governed root, and a target with an evidence requirement that
no verification subject or external boundary routes (SC-GF-004), are refused
before they are recorded. It replaces the
hook whygame5 copied by hand, which broke in linked worktrees (no `.venv` there).

Interpreter lookup, in order:
1. the interpreter that ran `aes hooks install` (`python -m agentic_engineering_system.cli`),
   so the hook runs the AES that installed it;
2. `<worktree>/.venv/bin/aes`, then `<main checkout>/.venv/bin/aes` via
   `git rev-parse --git-common-dir` (linked worktrees share the main checkout's venv);
3. `aes` on PATH.
None found is a hook failure with the install command, never a silent pass.

Refusals (nothing is written): the root is not the top of a Git work tree; the
target named by `.aes/project.yaml` is absent; a pre-commit hook AES did not
write exists in `.githooks/` or the repository's own hooks directory; a local
`core.hooksPath` points elsewhere. A global `core.hooksPath` is overridden for
this repository and reported. AES-written hooks carry `MANAGED_MARKER` on their
second line (the first is the shebang) and are rewritten.
"""

from __future__ import annotations

import shlex
import subprocess
import sys
from pathlib import Path

from .records import load_project

HOOKS_DIR = ".githooks"
MANAGED_MARKER = "# managed by aes hooks install"

_TEMPLATE = """#!/bin/sh
{marker}
# AES v0.2 gate: the target must load strictly, every evidence requirement in it
# must have a route, and every file staged under a governed root must be a
# planned artifact in the target. Regenerate with
# `aes hooks install`; edits here are overwritten.
set -e
root=$(git rev-parse --show-toplevel)
# linked worktrees have no .venv of their own; fall back to the main checkout's
main=$(cd "$(git rev-parse --git-common-dir)/.." && pwd)
installer={installer}
if [ -x "$installer" ]; then aes() {{ "$installer" -m agentic_engineering_system.cli "$@"; }}
elif [ -x "$root/.venv/bin/aes" ]; then aes() {{ "$root/.venv/bin/aes" "$@"; }}
elif [ -x "$main/.venv/bin/aes" ]; then aes() {{ "$main/.venv/bin/aes" "$@"; }}
elif command -v aes >/dev/null 2>&1; then aes() {{ command aes "$@"; }}
else
  echo "pre-commit: 'aes' not found (tried $installer, $root/.venv, $main/.venv, PATH)." >&2
  echo "pre-commit: install AES into the project venv, then rerun 'aes hooks install'." >&2
  exit 1
fi
aes target validate --root "$root" >/dev/null
aes topology check --root "$root"
"""


class HookInstallError(ValueError):
    """The hook was not installed; the message says why and what to do."""


def render_hook(interpreter: str) -> str:
    return _TEMPLATE.format(marker=MANAGED_MARKER, installer=shlex.quote(interpreter))


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)


def _is_managed(path: Path) -> bool:
    return MANAGED_MARKER in path.read_text(encoding="utf-8", errors="replace").splitlines()[:2]


def _refuse_foreign_hook(path: Path) -> None:
    if path.exists() and not _is_managed(path):
        raise HookInstallError(
            f"{path}: a pre-commit hook AES did not write already exists; "
            f"merge it by hand or move it away, then rerun `aes hooks install`"
        )


def install_hooks(root: Path, interpreter: str | None = None) -> tuple[Path, str | None]:
    """Write `<root>/.githooks/pre-commit` and set the repository's `core.hooksPath`.

    Returns the hook path and, when a global `core.hooksPath` exists, that path:
    the local setting overrides it for this repository, which the caller reports.
    """
    root = Path(root).resolve()
    top = _git(root, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        raise HookInstallError(f"{root}: not a Git repository ({top.stderr.strip()})")
    if Path(top.stdout.strip()).resolve() != root:
        raise HookInstallError(f"{root}: not the top of its Git work tree ({top.stdout.strip()})")

    project = load_project(root / ".aes" / "project.yaml")
    target = root / project.materialization.target_path
    if not target.is_file():
        raise HookInstallError(f"{target}: target absent; the hook would fail every commit")

    hook = root / HOOKS_DIR / "pre-commit"
    _refuse_foreign_hook(hook)
    current = _git(root, "config", "--local", "--get", "core.hooksPath")
    if current.returncode == 0 and current.stdout.strip() not in (HOOKS_DIR, HOOKS_DIR + "/"):
        raise HookInstallError(
            f"{root}: core.hooksPath is already {current.stdout.strip()!r}; "
            f"setting it to {HOOKS_DIR!r} would disable those hooks"
        )
    if current.returncode != 0:
        # A real hook in the repository's own hooks directory would go dark. A global
        # core.hooksPath is overridden for this repository too; that is reported,
        # not refused, because the governed-repo convention is a local hooksPath.
        common = _git(root, "rev-parse", "--git-common-dir")
        _refuse_foreign_hook(root / common.stdout.strip() / "hooks" / "pre-commit")

    hook.parent.mkdir(exist_ok=True)
    hook.write_text(render_hook(interpreter or sys.executable), encoding="utf-8")
    hook.chmod(0o755)
    configured = _git(root, "config", "--local", "core.hooksPath", HOOKS_DIR)
    if configured.returncode != 0:
        raise HookInstallError(f"{root}: git config core.hooksPath failed: {configured.stderr.strip()}")
    overridden = _git(root, "config", "--global", "--get", "core.hooksPath")
    return hook, (overridden.stdout.strip() or None) if overridden.returncode == 0 else None
