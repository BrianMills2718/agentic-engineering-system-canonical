"""Shared helpers for the Lockstep acceptance run scripts (A1 to A5).

Each run script does a real run of the installed Lockstep (this worktree's .venv) in a throwaway git
repository and writes a full-trace record to docs/planning/runs/lockstep-acceptance/<entry>.json, which
`build_page.py` turns into proposals/planning-package/review-page/lockstep-acceptance.html.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BIN = Path(sys.executable).parent  # the worktree's .venv/bin holds lockstep and lockstep-hook
RECORDS = ROOT / "docs/planning/runs/lockstep-acceptance"
MAX_LINES = 60  # an output is trimmed to this many lines (head), never edited; the count cut is recorded

ENV = {**os.environ, "PATH": f"{BIN}{os.pathsep}{os.environ['PATH']}", "PYTHONDONTWRITEBYTECODE": "1",
       "GIT_AUTHOR_NAME": "acceptance", "GIT_AUTHOR_EMAIL": "acceptance@example.invalid",
       "GIT_COMMITTER_NAME": "acceptance", "GIT_COMMITTER_EMAIL": "acceptance@example.invalid"}
for _var in subprocess.run(["git", "rev-parse", "--local-env-vars"], capture_output=True, text=True).stdout.split():
    ENV.pop(_var, None)


def revision() -> str:
    """The Lockstep source revision under test: this worktree's HEAD, plus -dirty when src/lockstep has edits."""
    sha = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--short", "src/lockstep"], capture_output=True,
                           text=True).stdout.strip()
    return sha + ("-dirty" if dirty else "")


def trim(text: str) -> dict:
    """Keep the first MAX_LINES lines of an output as they are; say how many were cut."""
    lines = text.splitlines()
    return {"text": "\n".join(lines[:MAX_LINES]), "lines_cut": max(0, len(lines) - MAX_LINES)}


class Trace:
    """Collects the steps and rows of one run."""

    def __init__(self, entry: str, title: str):
        self.entry, self.title = entry, title
        self.steps: list[dict] = []
        self.rows: list[dict] = []
        self.extra: dict = {}

    def run(self, name: str, argv_or_cmd, cwd: Path, stdin: str | None = None, env: dict | None = None) -> dict:
        """Run one command for real and record it: the exact command, hook input, exit code, stdout, stderr."""
        shell = isinstance(argv_or_cmd, str)
        p = subprocess.run(argv_or_cmd, shell=shell, cwd=cwd, env=env or ENV, input=stdin,
                           capture_output=True, text=True, timeout=600)
        step = {"name": name, "command": argv_or_cmd if shell else " ".join(argv_or_cmd), "cwd": str(cwd),
                "stdin": stdin, "exit_code": p.returncode, "stdout": trim(p.stdout), "stderr": trim(p.stderr)}
        self.steps.append(step)
        return step

    def row(self, rid: str, label: str, should: str, did: str, step: str, detail: dict | None = None) -> dict:
        """Add one row; pass is computed here by comparing should with did, never typed in."""
        row = {"id": rid, "label": label, "should": should, "did": did, "pass": should == did, "step": step,
               **(detail or {})}
        self.rows.append(row)
        return row

    def write(self) -> Path:
        """Write the record; its verdict is PASS only when every row passes."""
        RECORDS.mkdir(parents=True, exist_ok=True)
        verdict = "NOT RUN" if not self.rows else ("PASS" if all(r["pass"] for r in self.rows) else "FAIL")
        rec = {"entry": self.entry, "title": self.title, "verdict": verdict,
               "run_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
               "lockstep_revision": revision(), "lockstep_bin": str(BIN),
               "rows": self.rows, **self.extra, "steps": self.steps}
        path = RECORDS / f"{self.entry.lower()}.json"
        path.write_text(json.dumps(rec, indent=1) + "\n")
        print(f"{self.entry}: {verdict} ({sum(r['pass'] for r in self.rows)}/{len(self.rows)} rows) -> {path}")
        return path


def git(cwd: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(cwd), *args], env=ENV, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {p.stdout}{p.stderr}")
    return p.stdout


def tree(root: Path, *under: str) -> list[str]:
    """Sorted file paths (relative) below the given folders of root, skipping .git, caches and the hook's .pcw log."""
    out = []
    for u in under or (".",):
        for p in sorted((root / u).rglob("*")):
            rel = p.relative_to(root).as_posix()
            if p.is_file() and not any(s in rel for s in (".git/", "__pycache__", ".pcw/", ".pytest_cache")):
                out.append(rel)
    return out
