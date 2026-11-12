"""Shared pieces of the A1 and A5 runs: take the install command from the README text, install into fresh repos.

The command is parsed from the README's `uvx --from <source> lockstep init` line, never typed here. With `--source`
the source in that command is replaced (a local folder or another git address); without it the published address stays.
Every install and check uses a fresh UV_CACHE_DIR, so nothing comes from this machine's uv cache. Environment variables
are never recorded.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from _common import ENV, git

PUBLISHED = "https://github.com/BrianMills2718/agentic-engineering-system-canonical"
CANONICAL = "BrianMills2718/agentic-engineering-system-canonical"
INSTALL_LINE = re.compile(r"(?m)^uvx --from (\S+) lockstep init$")


def parse_args(doc: str) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=doc)
    ap.add_argument("--source", default=PUBLISHED, help="URL or local folder to install Lockstep from (default: published)")
    return ap.parse_args()


def is_local(source: str) -> bool:
    return not re.match(r"^(git\+)?[a-z][a-z0-9+.-]*://", source)


def uvx_source(source: str) -> str:
    """What goes after `--from`: a local folder as is, a git address with `git+` in front."""
    if is_local(source) or source.startswith("git+"):
        return source
    return "git+" + source


def readme_text(source: str) -> str:
    """The README of the source: the folder's README.md, or the repository's main-branch README over https."""
    if is_local(source):
        return (Path(source) / "README.md").read_text(encoding="utf-8")
    m = re.match(r"^(?:git\+)?https://github\.com/([^/]+/[^/]+?)(?:\.git)?/?$", source)
    if not m:
        raise SystemExit(f"cannot find a README for source {source}")
    url = f"https://raw.githubusercontent.com/{m.group(1)}/main/README.md"
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode()


def install_command(readme: str, source: str) -> tuple[str, str]:
    """(the command as the README gives it, the same command with the source substituted)."""
    m = INSTALL_LINE.search(readme)
    if not m:
        raise SystemExit("no `uvx --from <source> lockstep init` line in the README")
    return m.group(0), m.group(0).replace(m.group(1), uvx_source(source))


def readme_for_agent(readme: str, source: str) -> str:
    """The README text with the source substituted in every copy of the install address (for the agent run)."""
    given = INSTALL_LINE.search(readme).group(1)
    return readme.replace(given, uvx_source(source)) if uvx_source(source) != given else readme


def fresh_env(prefix: str) -> tuple[dict, Path]:
    """The run environment with a new, empty UV_CACHE_DIR (and a new tool dir so no installed tool is reused)."""
    cache = Path(tempfile.mkdtemp(prefix=f"{prefix}-uvcache-"))
    return {**ENV, "UV_CACHE_DIR": str(cache), "UV_TOOL_DIR": str(cache / "tools")}, cache


def fresh_repo(prefix: str, origin: str) -> Path:
    """A new git repository in a temp folder with the given origin."""
    root = Path(tempfile.mkdtemp(prefix=f"{prefix}-")) / "demo"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "remote", "add", "origin", origin)
    return root


def written_files(root: Path) -> dict[str, str]:
    """Every file in the repo (outside .git) with its full text."""
    out = {}
    for line in git(root, "status", "--short", "-uall").splitlines():
        rel = line[3:].strip()
        p = root / rel
        if p.is_file():
            out[rel] = p.read_text(encoding="utf-8", errors="replace")
    return dict(sorted(out.items()))


def under_test(source: str) -> dict:
    """Record fields naming what was installed: for a local folder its HEAD (plus -dirty), else the address's main head."""
    if is_local(source):
        sha = git(Path(source), "rev-parse", "HEAD").strip()
        dirty = git(Path(source), "status", "--short", "--", "src/lockstep").strip()
        rev = sha + ("-dirty" if dirty else "")
    else:
        addr = re.sub(r"^git\+", "", source)
        out = subprocess.run(["git", "ls-remote", addr, "HEAD"], capture_output=True, text=True, env=ENV).stdout.split()
        rev = out[0] if out else "unknown"
    return {"lockstep_revision": rev, "lockstep_bin": "uvx, installed fresh from the source (no machine cache)"}
