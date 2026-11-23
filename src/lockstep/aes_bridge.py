"""Read the AES plan: compiled context per ID and the path-to-artifact map.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:aes_bridge.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: (no requirement)
[[[end]]]
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

from lockstep.layout_plan import SOURCE, governed, has_layout, layout_context, target_from_layout


def find_root(start: Path) -> Path | None:
    """Nearest directory at or above `start` holding `.aes/project.yaml`, or a lockstep.yaml whose `layout:` is the plan."""
    start = start.resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".aes" / "project.yaml").is_file() or has_layout(candidate):
            return candidate
    return None


def plan_name(root: Path) -> str:
    """Where this repository's plan is written, for messages: `.aes/target.yaml` or the layout."""
    return SOURCE if has_layout(root) else ".aes/target.yaml"


def _aes() -> str:
    found = shutil.which("aes")
    if found:
        return found
    sibling = Path(sys.executable).with_name("aes")
    if sibling.exists():
        return str(sibling)
    raise RuntimeError("aes not found on PATH or next to this Python")


def run_aes(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([_aes(), *args], cwd=root, capture_output=True, text=True)


def context(root: Path, subject: str) -> dict:
    """`aes context SUBJECT --format json`, or the layout row's context; fails loudly on an unknown ID."""
    if has_layout(root):
        return layout_context(root, subject)
    proc = run_aes(root, "context", subject, "--format", "json")
    if proc.returncode != 0:
        raise RuntimeError(f"aes context {subject} failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def target(root: Path) -> dict:
    if has_layout(root):
        return target_from_layout(root)
    return yaml.safe_load((root / ".aes" / "target.yaml").read_text(encoding="utf-8"))


def governed_roots(root: Path) -> list[str]:
    if has_layout(root):
        return governed(root)
    project = yaml.safe_load((root / ".aes" / "project.yaml").read_text(encoding="utf-8"))
    return list(project.get("governed_roots") or target(root).get("governed_roots") or [])


def artifact_for_path(root: Path, relpath: str) -> str | None:
    for art in target(root).get("planned_artifacts") or []:
        if (art.get("locator") or {}).get("exact_path") == relpath:
            return art["id"]
    return None


def committed_text(root: Path, ref: str, relpath: str) -> str | None:
    """The text of `relpath` as committed at `ref`, or None when no file is there.

    Read from the object store, never the working tree, so a change cannot rewrite what is read (issue #67).
    """
    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", str(root), *args],
                              capture_output=True, text=True)
    if git("cat-file", "-t", f"{ref}:{relpath}").stdout.strip() != "blob":
        return None
    shown = git("show", f"{ref}:{relpath}")
    if shown.returncode != 0:
        raise RuntimeError(f"git show {ref}:{relpath} failed: {shown.stderr.strip()[:300]}")
    return shown.stdout


def legacy_files(root: Path, base: str | None = None) -> set[str]:
    """Files `aes adopt` accepted as they were; a real project's existing code starts here.

    With `base`, the list as committed at that revision, so a change cannot add its own files to it.
    """
    rel = ".aes/legacy_baseline.json"
    if base is not None:
        text = committed_text(root, base, rel)
    else:
        path = root / rel
        text = path.read_text(encoding="utf-8") if path.is_file() else None
    return set(json.loads(text).get("files") or []) if text else set()


def is_governed(root: Path, relpath: str, base: str | None = None) -> bool:
    """Under a governed root, and not a legacy file (those stay editable until planned)."""
    return any(relpath.startswith(g) for g in governed_roots(root)) and relpath not in legacy_files(root, base)
