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

The hook body is the same bytes on every machine. `.githooks/pre-commit` is a
tracked, shared file, so the installing checkout's absolute interpreter path
(step 1) is not written into it: `aes hooks install` records that path in the
repository's own `.git/config` as `aes.installer` and the hook reads it back.
Baking it in instead left the hook dirty in `git status` after the documented
install, so one `git add -A` published a path that exists on nobody else's
machine, where step 1 would silently fail over to step 2.

Refusals (nothing is written): the root is not the top of a Git work tree; the
target named by `.aes/project.yaml` is absent; a pre-commit hook AES did not
write exists in `.githooks/` or the repository's own hooks directory; a local
`core.hooksPath` points elsewhere. A global `core.hooksPath` is overridden for
this repository and reported. AES-written hooks carry `MANAGED_MARKER` on their
second line (the first is the shebang) and are rewritten.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .records import load_project

HOOKS_DIR = ".githooks"
MANAGED_MARKER = "# managed by aes hooks install"
INSTALLER_CONFIG_KEY = "aes.installer"

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
# the interpreter that ran `aes hooks install`, in this clone's .git/config so
# that this tracked file stays byte-identical on every machine
installer=$(git config --get {config_key} 2>/dev/null) || installer=
if [ -n "$installer" ] && [ -x "$installer" ]; then
  aes() {{ "$installer" -m agentic_engineering_system.cli "$@"; }}
elif [ -x "$root/.venv/bin/aes" ]; then aes() {{ "$root/.venv/bin/aes" "$@"; }}
elif [ -x "$main/.venv/bin/aes" ]; then aes() {{ "$main/.venv/bin/aes" "$@"; }}
elif command -v aes >/dev/null 2>&1; then aes() {{ command aes "$@"; }}
else
  echo "pre-commit: 'aes' not found (tried {config_key}=${{installer:-<unset>}}," \\
       "$root/.venv, $main/.venv, PATH)." >&2
  echo "pre-commit: install AES into the project venv, then rerun 'aes hooks install'." >&2
  exit 1
fi
aes target validate --root "$root" >/dev/null
aes topology check --root "$root"
"""


_COMMIT_MSG_TEMPLATE = """#!/bin/sh
{marker}
# AES commit rule (AP-REQ-001): the first line's tag is checked against facts about
# the staged change and the plan it names (`aes commit check`). Mode is set in
# .aes/commit_rule.yaml (observe: log only; enforce: refuse). Regenerate with
# `aes hooks install`; edits here are overwritten.
set -e
root=$(git rev-parse --show-toplevel)
main=$(cd "$(git rev-parse --git-common-dir)/.." && pwd)
installer=$(git config --get {config_key} 2>/dev/null) || installer=
if [ -n "$installer" ] && [ -x "$installer" ]; then
  aes() {{ "$installer" -m agentic_engineering_system.cli "$@"; }}
elif [ -x "$root/.venv/bin/aes" ]; then aes() {{ "$root/.venv/bin/aes" "$@"; }}
elif [ -x "$main/.venv/bin/aes" ]; then aes() {{ "$main/.venv/bin/aes" "$@"; }}
elif command -v aes >/dev/null 2>&1; then aes() {{ command aes "$@"; }}
else
  echo "commit-msg: 'aes' not found (tried {config_key}=${{installer:-<unset>}}," \\
       "$root/.venv, $main/.venv, PATH)." >&2
  echo "commit-msg: install AES into the project venv, then rerun 'aes hooks install'." >&2
  exit 1
fi
aes commit check "$1" --root "$root"
"""


class HookInstallError(ValueError):
    """The hook was not installed; the message says why and what to do."""


def render_hook() -> str:
    """The hook body: machine-independent, so the tracked file never churns."""
    return _TEMPLATE.format(marker=MANAGED_MARKER, config_key=INSTALLER_CONFIG_KEY)


def render_commit_msg_hook() -> str:
    """The commit-msg hook body; machine-independent like the pre-commit hook."""
    return _COMMIT_MSG_TEMPLATE.format(marker=MANAGED_MARKER, config_key=INSTALLER_CONFIG_KEY)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)


def _is_managed(path: Path) -> bool:
    return MANAGED_MARKER in path.read_text(encoding="utf-8", errors="replace").splitlines()[:2]


def _refuse_foreign_hook(path: Path) -> None:
    if path.exists() and not _is_managed(path):
        raise HookInstallError(
            f"{path}: a {path.name} hook AES did not write already exists; "
            f"merge it by hand or move it away, then rerun `aes hooks install`"
        )


def install_hooks(root: Path, interpreter: str | None = None) -> tuple[Path, str | None]:
    """Write `<root>/.githooks/pre-commit` and `commit-msg`, set `core.hooksPath` and `aes.installer`.

    The hook body is machine-independent; the installing interpreter goes into
    this clone's `.git/config` as `aes.installer`, never into the tracked file.

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
    commit_msg = root / HOOKS_DIR / "commit-msg"
    _refuse_foreign_hook(hook)
    _refuse_foreign_hook(commit_msg)
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
        _refuse_foreign_hook(root / common.stdout.strip() / "hooks" / "commit-msg")

    hook.parent.mkdir(exist_ok=True)
    hook.write_text(render_hook(), encoding="utf-8")
    hook.chmod(0o755)
    commit_msg.write_text(render_commit_msg_hook(), encoding="utf-8")
    commit_msg.chmod(0o755)
    configured = _git(root, "config", "--local", "core.hooksPath", HOOKS_DIR)
    if configured.returncode != 0:
        raise HookInstallError(f"{root}: git config core.hooksPath failed: {configured.stderr.strip()}")
    recorded = _git(root, "config", "--local", INSTALLER_CONFIG_KEY, interpreter or sys.executable)
    if recorded.returncode != 0:
        raise HookInstallError(
            f"{root}: git config {INSTALLER_CONFIG_KEY} failed: {recorded.stderr.strip()}"
        )
    overridden = _git(root, "config", "--global", "--get", "core.hooksPath")
    return hook, (overridden.stdout.strip() or None) if overridden.returncode == 0 else None
