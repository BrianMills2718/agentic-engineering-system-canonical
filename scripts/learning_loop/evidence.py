"""Resolve feedback references and count independent, verified observations.

Parsing a link establishes provenance syntax; resolution establishes that the
referenced evidence is available. Neither establishes the truth of its prose.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ISSUE = re.compile(r"^([\w.-]+/[\w.-]+)#(\d+)$")
GH_ISSUE = re.compile(r"^/([\w.-]+/[\w.-]+)/(?:issues|pull)/(\d+)(?:/.*)?$")


def github_issue(ref: str) -> tuple[str, str] | None:
    m = ISSUE.fullmatch(ref)
    if not m:
        u = urlsplit(ref)
        m = GH_ISSUE.fullmatch(u.path) if u.hostname == "github.com" else None
    return (m.group(1), m.group(2)) if m else None


def identity(link: dict, cwd: str = "") -> str:
    ref = link["ref"]
    issue = github_issue(ref)
    if issue:
        return f"issue:{issue[0].lower()}#{issue[1]}"
    if link["kind"] == "path":
        name = re.sub(r":\d+(?:-\d+)?$", "", ref)
        path = Path(name).expanduser()
        resolved = (Path(cwd) / path).resolve() if not path.is_absolute() else path.resolve()
        return f"path:{resolved}{ref[len(name):]}"
    return f"{link['kind']}:{ref}"


def gh_command(repo: str) -> str:
    return "gh-insidesuccess" if repo.lower().startswith("inside-success/") else "gh"


def resolve(link: dict, cwd: str = "") -> bool:
    ref, kind = link["ref"], link["kind"]
    issue = github_issue(ref)
    try:
        if issue:
            p = subprocess.run([gh_command(issue[0]), "api", f"repos/{issue[0]}/issues/{issue[1]}", "-q", ".number"],
                               capture_output=True, text=True, timeout=30)
            return p.returncode == 0 and p.stdout.strip() == issue[1]
        if kind == "path":
            m = re.fullmatch(r"(.+?):(\d+)(?:-(\d+))?", ref)
            path = Path(m.group(1) if m else ref).expanduser()
            if not path.is_absolute():
                if not cwd:
                    return False
                path = Path(cwd) / path
            if not path.is_file():
                return False
            if m:
                first, last = int(m.group(2)), int(m.group(3) or m.group(2))
                with path.open("rb") as fh:
                    lines = sum(1 for _ in fh)
                return 0 < first <= last <= lines
            return True
        if kind == "commit" and cwd:
            return subprocess.run(["git", "-C", cwd, "cat-file", "-e", f"{ref}^{{commit}}"],
                                  capture_output=True, timeout=10).returncode == 0
        if kind == "url" and urlsplit(ref).scheme in ("http", "https"):
            with urlopen(Request(ref, method="HEAD"), timeout=20) as response:
                return response.status == 200
    except (OSError, ValueError, subprocess.SubprocessError):
        pass
    return False


def resolve_records(records: list[dict], db=None) -> dict[str, int]:
    """Annotate derived state, without rewriting the immutable source records."""
    if db is not None:
        db.execute("CREATE TABLE IF NOT EXISTS link_resolution (key TEXT PRIMARY KEY, valid INT, checked TEXT)")
    now = dt.datetime.now(dt.timezone.utc)
    cache = {}
    counts = {"evidence_resolved": 0, "evidence_unresolved": 0}
    for record in records:
        cwd = (record.get("provenance") or {}).get("cwd", "")
        record["resolved_links"] = []
        for link in record.get("links", []):
            key = json.dumps([identity(link, cwd), cwd])
            if key not in cache:
                row = db.execute("SELECT valid, checked FROM link_resolution WHERE key=?", (key,)).fetchone() if db else None
                ttl = dt.timedelta(hours=24 if row and row[0] else 1)
                if row and now - dt.datetime.fromisoformat(row[1]) < ttl:
                    cache[key] = bool(row[0])
                else:
                    cache[key] = resolve(link, cwd)
                    if db is not None:
                        db.execute("INSERT OR REPLACE INTO link_resolution VALUES (?,?,?)", (key, cache[key], now.isoformat()))
            if cache[key]:
                record["resolved_links"].append(link)
            counts["evidence_resolved" if cache[key] else "evidence_unresolved"] += 1
    if db is not None:
        db.commit()
    return counts


def sightings(members: list[dict]) -> list[set[str]]:
    groups: list[tuple[set[str], set[str]]] = []
    for r in members:
        links = r.get("resolved_links", [])
        if r["kind"] != "observation" or not links:
            continue
        cwd = (r.get("provenance") or {}).get("cwd", "")
        ev = {identity(link, cwd) for link in links}
        session = r.get("session") or (r.get("provenance") or {}).get("session_id") or r.get("day")
        if not session:
            continue
        who = {session}
        hits = [g for g in groups if g[1] & ev or g[0] & who]
        for g in hits:
            groups.remove(g)
            who |= g[0]
            ev |= g[1]
        groups.append((who, ev))
    return [g[0] for g in groups]
