"""Every test runs as on a clean machine: no machine-wide Git config, so no machine-wide hooks.

The tests create throwaway repositories and make real commits. On a machine whose global
`core.hooksPath` installs hooks (a disk-space guard that pauses `git worktree add`, for example),
those hooks ran inside the tests' repositories too: on 2026-10-07 the
guard refused `git worktree add` in two linked-worktree tests while C: was near its reserve, and
`make aes-check` failed for a reason that had nothing to do with AES. Pointing GIT_CONFIG_GLOBAL at a
file holding only a test identity, and setting GIT_CONFIG_NOSYSTEM, removes that dependence for every
subprocess the tests start.

Tests marked `slow` (end-to-end installs and whole-repository runs) are left out of `make check`
and run by `make check-full`.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

_CLEAN = Path(tempfile.mkdtemp(prefix="aes-tests-git-")) / "gitconfig"
_CLEAN.write_text("[user]\n\tname = AES tests\n\temail = aes-tests@example.invalid\n", encoding="utf-8")


def pytest_configure(config: object) -> None:
    os.environ["GIT_CONFIG_GLOBAL"] = str(_CLEAN)
    os.environ["GIT_CONFIG_NOSYSTEM"] = "1"
