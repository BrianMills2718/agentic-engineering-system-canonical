#!/usr/bin/env python3
"""The AES hub page: one page whose top section, "Needs you", lists only what the owner must do or decide, then
what changed, then a link to each source page.

Each run reads four sources, each on its own so one that cannot be read is shown as "Not checked" and never as 0:

  * decisions: every open issue labelled `waiting_label` (default `waiting:brian`) in the configured owners'
    repositories, through the gh wrapper `github_accounts` names for that owner (`gh search issues`);
  * failed services: `systemctl --user list-units --failed`; a unit listed under `quiet_units`, with its reason,
    is shown below the list as known and not counted;
  * AES concerns waiting on a person: open issues in `concern_repo` labelled `needs_human_label`;
  * approvals waiting: the requirements an agent inferred that wait for a yes, read from the oversight data file
    `approvals_file` (each item whose `source` is `inferred`); shown as a count, its age and a short list.

"What changed" compares this run's items with the previous run's `hub.json` on the data branch (new, cleared) and
lists the pull requests merged into `concern_repo` in the last day. The page and `hub.json` are committed to
`data_branch` of the private repository `repo` (never main, never this public repository), where the private plan
site serves them behind the owner's login. Nothing here calls a model; a run takes seconds.

Settings come from the `hub_page:` section of `graph-config.yaml` (the private aes-config repository, found the way
workspace_map.py finds it). Every run appends its inputs, each command with its exit status and time, and its output
to ~/projects/data/logs/aes-hub/<day>.log (AES_HUB_LOG_DIR moves it).

    python3 scripts/hub_page.py                 # build, then publish to the data branch
    python3 scripts/hub_page.py --no-push --out DIR   # build into DIR only
Exit 0 when every source was read and the page published, 1 when a source or the publish failed (the page is still
built), 2 when a setting is missing.

Implements: hub-page/needs-you-comes-first
Implements: hub-page/an-unread-source-is-not-checked
Implements: hub-page/what-changed-since-the-last-run
Implements: hub-page/links-to-each-source-page
Implements: hub-page/page-goes-to-a-private-data-branch
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import workspace_map as wm  # noqa: E402

LOG_DIR = Path(os.environ.get("AES_HUB_LOG_DIR") or Path.home() / "projects/data/logs/aes-hub")
RUNTIME = Path(os.environ.get("AES_HUB_RUNTIME") or Path.home() / ".local/share/ecosystem-runtime/aes-hub")
PAGE, DATA = "proposals/aes-hub/review-page/index.html", "proposals/aes-hub/review-page/hub.json"
APPROVALS_SHOWN = 8
NEEDED = ("repo", "data_branch", "site_url", "waiting_owners", "concern_repo", "needs_human_label", "approvals_file")


# ---------------------------------------------------------------- settings and commands

def settings(cfg: dict | None = None) -> dict:
    """The hub_page settings with the shared ones they use; a missing one is a loud stop (exit 2)."""
    cfg = wm.graph_config() if cfg is None else cfg
    hub = dict(cfg.get("hub_page") or {})
    absent = [k for k in NEEDED if not hub.get(k)]
    for k in ("ssh_host_alias", "github_accounts"):
        if not cfg.get(k):
            absent.append(k)
    who = cfg.get("git_identity") or {}
    if not (who.get("name") and who.get("email")):
        absent.append("git_identity")
    if absent:
        raise wm.ConfigMissing(f"hub_page: no {', '.join(absent)} in {wm.config_path()} (hub_page: section)")
    hub.setdefault("waiting_label", "waiting:brian")
    hub.setdefault("quiet_units", {})
    hub.setdefault("links", [])
    hub.setdefault("refresh", "")
    hub["accounts"] = cfg["github_accounts"]
    hub["identity"] = who
    hub["remote"] = f"git@{cfg['ssh_host_alias']}:{hub['repo']}.git"
    return hub


class Run:
    """Runs commands, each timed and written to the day's log with its output."""

    def __init__(self, log_dir: Path | None = None):
        log_dir = Path(log_dir or LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = log_dir / f"{time.strftime('%Y-%m-%d')}.log"

    def log(self, text: str) -> None:
        line = f"{time.strftime('%H:%M:%S')} {text}"
        print(line, flush=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def __call__(self, name: str, cmd: list[str], cwd: str | None = None, timeout: int = 120) -> subprocess.CompletedProcess:
        start = time.time()
        try:
            out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        except (OSError, subprocess.TimeoutExpired) as exc:
            out = subprocess.CompletedProcess(cmd, 127, "", repr(exc))
        self.log(f"step={name} exit={out.returncode} seconds={time.time() - start:.1f} cmd={' '.join(map(str, cmd))}")
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(((out.stdout or "") + (out.stderr or ""))[-8000:] + "\n")
        return out


def source(name: str, ok: bool, error: str = "", count: int | None = None) -> dict:
    return {"name": name, "ok": ok, "error": error, "count": count}


# ---------------------------------------------------------------- readers (pure parsers, commands injected)

def parse_issues(text: str) -> list[dict]:
    """gh --json repository,number,title,url,updatedAt output to items, oldest-updated last."""
    rows = []
    for i in json.loads(text):
        repo = i.get("repository", {})
        name = repo.get("nameWithOwner") or repo.get("name", "")
        rows.append({"key": f"issue:{name}#{i['number']}", "title": i["title"], "where": f"{name}#{i['number']}",
                     "url": i.get("url", ""), "updated": i.get("updatedAt", "")})
    rows.sort(key=lambda r: r["updated"], reverse=True)
    return rows


def parse_failed_units(text: str, quiet: dict) -> tuple[list[dict], list[dict]]:
    """`systemctl --user list-units --failed --plain --no-legend` to (needs you, known and quiet)."""
    shown, known = [], []
    for line in text.splitlines():
        parts = line.split(None, 4)
        if len(parts) < 4 or not parts[0].endswith((".service", ".timer", ".path", ".socket", ".mount")):
            continue
        unit = {"key": f"unit:{parts[0]}", "title": parts[0], "where": parts[4] if len(parts) > 4 else "",
                "url": "", "updated": ""}
        if parts[0] in quiet:
            known.append({**unit, "reason": quiet[parts[0]]})
        else:
            shown.append(unit)
    return shown, known


def parse_approvals(data: dict) -> dict:
    """Distinct requirements an agent inferred (oversight data), with the file's own date."""
    seen: dict[str, dict] = {}
    for repo in data["repos"]:
        for i in repo["items"]:
            if i.get("source") == "inferred":
                seen.setdefault(i["id"], {"key": f"approval:{i['id']}", "title": i["title"], "where": repo["repo"],
                                          "url": i.get("file_url", ""), "updated": ""})
    items = sorted(seen.values(), key=lambda r: r["key"])
    return {"count": len(items), "items": items, "as_of": data.get("generated", "")}


def gh_for(owner_or_repo: str, accounts: dict) -> str:
    return accounts.get(owner_or_repo.split("/")[0], "gh")


def read_decisions(s: dict, run) -> tuple[list[dict] | None, dict]:
    rows: list[dict] = []
    for owner in s["waiting_owners"]:
        out = run(f"waiting-{owner}", [gh_for(owner, s["accounts"]), "search", "issues", "--owner", owner, "--label",
                                       s["waiting_label"], "--state", "open", "--limit", "200",
                                       "--json", "repository,number,title,url,updatedAt"])
        if out.returncode != 0:
            return None, source(f"Decisions ({s['waiting_label']} issues)", False, f"gh search exit {out.returncode}: {out.stderr.strip()[-200:]}")
        try:
            rows += parse_issues(out.stdout)
        except (ValueError, KeyError) as exc:
            return None, source(f"Decisions ({s['waiting_label']} issues)", False, f"unreadable output: {exc!r}"[:200])
    return rows, source(f"Decisions ({s['waiting_label']} issues)", True, count=len(rows))


def read_failed(s: dict, run) -> tuple[tuple[list, list] | None, dict]:
    out = run("failed-units", ["systemctl", "--user", "list-units", "--failed", "--plain", "--no-legend"])
    if out.returncode != 0:
        return None, source("Failed services (systemctl)", False, f"systemctl exit {out.returncode}: {out.stderr.strip()[-200:]}")
    shown, known = parse_failed_units(out.stdout, s["quiet_units"])
    return (shown, known), source("Failed services (systemctl)", True, count=len(shown))


def read_concerns(s: dict, run) -> tuple[list[dict] | None, dict]:
    name = f"AES concerns ({s['needs_human_label']})"
    repo = s["concern_repo"]
    labels = run("concern-labels", [gh_for(repo, s["accounts"]), "label", "list", "--repo", repo, "--limit", "500",
                                    "--json", "name"])
    if labels.returncode == 0:
        try:
            if s["needs_human_label"] not in {x["name"] for x in json.loads(labels.stdout)}:
                return None, source(name, False, f"the label {s['needs_human_label']} does not exist in {repo}")
        except (ValueError, KeyError):
            pass
    out = run("concerns", [gh_for(repo, s["accounts"]), "issue", "list", "--repo", repo, "--label", s["needs_human_label"],
                           "--state", "open", "--limit", "200", "--json", "number,title,url,updatedAt"])
    if out.returncode != 0:
        return None, source(name, False, f"gh issue list exit {out.returncode}: {out.stderr.strip()[-200:]}")
    try:
        rows = [{**i, "repository": {"nameWithOwner": repo}} for i in json.loads(out.stdout)]
        items = parse_issues(json.dumps(rows))
    except (ValueError, KeyError) as exc:
        return None, source(name, False, f"unreadable output: {exc!r}"[:200])
    return items, source(name, True, count=len(items))


def read_approvals(s: dict) -> tuple[dict | None, dict]:
    path = Path(os.path.expanduser(s["approvals_file"]))
    try:
        rec = parse_approvals(json.loads(path.read_text()))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return None, source("Approvals waiting (oversight data)", False, f"{path.name} could not be read: {exc!r}"[:200])
    return rec, source("Approvals waiting (oversight data)", True, count=rec["count"])


def read_merged(s: dict, run, now: dt.datetime) -> tuple[list[dict] | None, dict]:
    since = (now - dt.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    repo = s["concern_repo"]
    out = run("merged", [gh_for(repo, s["accounts"]), "pr", "list", "--repo", repo, "--state", "merged", "--search",
                         f"merged:>={since}", "--limit", "50", "--json", "number,title,url,mergedAt"])
    if out.returncode != 0:
        return None, source("Merged into AES (last day)", False, f"gh pr list exit {out.returncode}")
    try:
        rows = sorted(json.loads(out.stdout), key=lambda r: r["mergedAt"], reverse=True)
    except (ValueError, KeyError) as exc:
        return None, source("Merged into AES (last day)", False, f"unreadable output: {exc!r}"[:200])
    return rows, source("Merged into AES (last day)", True, count=len(rows))


# ---------------------------------------------------------------- the record

def changes(previous: dict | None, current: dict, sources_ok: dict) -> dict:
    """Items new since the previous run, and items gone from it, by key. A source not read on either run is
    skipped so an unread source never reads as everything cleared."""
    if not previous:
        return {"compared": False, "new": [], "cleared": []}
    prev_ok = {s["name"]: s["ok"] for s in previous.get("sources", [])}
    groups = ("decisions", "failed", "concerns")
    new, cleared = [], []
    for g in groups:
        name = current["group_sources"][g]
        if not (sources_ok.get(name) and prev_ok.get(name)):
            continue
        before = {i["key"]: i for i in previous.get("needs_you", {}).get(g) or []}
        after = {i["key"]: i for i in current["needs_you"][g] or []}
        new += [{**after[k], "group": g} for k in after if k not in before]
        cleared += [{**before[k], "group": g} for k in before if k not in after]
    return {"compared": True, "since": previous.get("built", ""), "new": new, "cleared": cleared}


def build_record(s: dict, run, now: dt.datetime, previous: dict | None = None, read_approvals_=read_approvals) -> dict:
    decisions, dsrc = read_decisions(s, run)
    failed, fsrc = read_failed(s, run)
    concerns, csrc = read_concerns(s, run)
    approvals, asrc = read_approvals_(s)
    merged, msrc = read_merged(s, run, now)
    sources = [dsrc, fsrc, csrc, asrc, msrc]
    rec = {
        "built": now.isoformat(timespec="minutes"),
        "sources": sources,
        "group_sources": {"decisions": dsrc["name"], "failed": fsrc["name"], "concerns": csrc["name"],
                          "approvals": asrc["name"]},
        "needs_you": {"decisions": decisions, "failed": failed[0] if failed else None, "concerns": concerns},
        "known_failed": failed[1] if failed else [],
        "approvals": approvals,
        "merged": merged,
        "links": s["links"],
        "site_url": s["site_url"],
    }
    rec["changed"] = changes(previous, rec, {x["name"]: x["ok"] for x in sources})
    rec["needs_you_total"] = sum(len(v) for v in rec["needs_you"].values() if v is not None)
    return rec


# ---------------------------------------------------------------- page

def esc(text) -> str:
    return html.escape(str(text if text is not None else ""), quote=True)


def stamp(iso: str) -> str:
    try:
        return dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone().strftime("%d %b %H:%M")
    except (ValueError, AttributeError):
        return iso or "unknown time"


def item_li(i: dict) -> str:
    title = f'<a href="{esc(i["url"])}">{esc(i["title"])}</a>' if i.get("url") else f'<b>{esc(i["title"])}</b>'
    return f'<li>{title} <span class="dim">{esc(i["where"])}</span></li>'


GROUPS = (("decisions", "Decisions waiting on you", "Open issues labelled {label}: answer on the issue or in a session."),
          ("failed", "Failed services", "Services on this machine whose last run failed. Most an agent can fix; each needs a yes to fix or retire."),
          ("concerns", "AES concerns for you", "Open issues in AES labelled {needs}."))


def needs_html(rec: dict, s: dict) -> str:
    by_name = {x["name"]: x for x in rec["sources"]}
    total = rec["needs_you_total"]
    unread = [g for g, *_ in GROUPS if rec["needs_you"][g] is None]
    head = f"Needs you ({total})" + (f", {len(unread)} source{'s' if len(unread) > 1 else ''} not checked" if unread else "")
    tone, word = ("orange", "Waiting") if total else ("blue", "None")
    out = [f'<section class="needs" id="needs"><h2><span class="tag {tone}">{word}</span> {esc(head)}</h2>']
    for g, title, what in GROUPS:
        items, src = rec["needs_you"][g], by_name[rec["group_sources"][g]]
        what = what.format(label=s["waiting_label"], needs=s["needs_human_label"])
        if items is None:
            out.append(f'<h3><span class="tag grey">Not checked</span> {esc(title)}</h3>'
                       f'<p class="dim">{esc(what)} Not read on this run: {esc(src["error"])}. Nothing is claimed.</p>')
            continue
        tag = '<span class="tag orange">Waiting</span>' if items else '<span class="tag blue">None</span>'
        out.append(f'<h3>{tag} {esc(title)} ({len(items)})</h3><p class="dim">{esc(what)}</p>')
        if items:
            out.append("<ul>" + "".join(item_li(i) for i in items) + "</ul>")
    if rec["known_failed"]:
        out.append('<p class="dim">Also failed, not counted (you said not to act on these): '
                   + "; ".join(f"{esc(k['title'])} ({esc(k['reason'])})" for k in rec["known_failed"]) + ".</p>")
    ap, asrc = rec["approvals"], by_name[rec["group_sources"]["approvals"]]
    if ap is None:
        out.append(f'<h3><span class="tag grey">Not checked</span> Approvals waiting</h3><p class="dim">{esc(asrc["error"])}.</p>')
    else:
        page = next((link["url"] for link in rec["links"] if "oversight" in link.get("name", "").lower()), "")
        more = f' <a href="{esc(page)}">All of them on the oversight page</a>.' if page else ""
        out.append(f'<h3><span class="tag grey">Count only</span> Approvals waiting ({ap["count"]})</h3>'
                   f'<p class="dim">Requirements an agent inferred that wait for your yes or a cut, from the oversight data '
                   f'written {esc(stamp(ap["as_of"]))}. Not counted in the number above.{more}</p>')
        if ap["items"]:
            out.append("<ul>" + "".join(item_li(i) for i in ap["items"][:APPROVALS_SHOWN]) + "</ul>")
    out.append("</section>")
    return "\n".join(out)


def changed_html(rec: dict) -> str:
    ch, merged = rec["changed"], rec["merged"]
    out = ['<section id="changed"><h2>What changed</h2>']
    if not ch["compared"]:
        out.append('<p class="dim">First run: there is no earlier run to compare with.</p>')
    else:
        out.append(f'<p class="dim">Since the run at {esc(stamp(ch["since"]))}.</p>')
        if ch["new"]:
            out.append('<h3><span class="tag orange">New</span> New items (' + str(len(ch["new"])) + ")</h3><ul>"
                       + "".join(item_li(i) for i in ch["new"]) + "</ul>")
        if ch["cleared"]:
            out.append('<h3><span class="tag blue">Cleared</span> Cleared items (' + str(len(ch["cleared"])) + ")</h3><ul>"
                       + "".join(item_li(i) for i in ch["cleared"]) + "</ul>")
        if not ch["new"] and not ch["cleared"]:
            out.append("<p>Nothing new and nothing cleared.</p>")
    if merged is None:
        out.append('<h3><span class="tag grey">Not checked</span> Merged into AES in the last day</h3>')
    else:
        out.append(f"<h3>Merged into AES in the last day ({len(merged)})</h3>")
        if merged:
            out.append("<ul>" + "".join(f'<li><a href="{esc(m["url"])}">#{esc(m["number"])} {esc(m["title"])}</a> '
                                        f'<span class="dim">{esc(stamp(m["mergedAt"]))}</span></li>' for m in merged) + "</ul>")
    out.append("</section>")
    return "\n".join(out)


def links_html(rec: dict) -> str:
    if not rec["links"]:
        return '<section id="sources"><h2>Source pages</h2><p class="dim">No source pages are configured.</p></section>'
    return ('<section id="sources"><h2>Source pages</h2><ul>'
            + "".join(f'<li><a href="{esc(link["url"])}">{esc(link["name"])}</a> <span class="dim">{esc(link.get("what", ""))}</span></li>'
                      for link in rec["links"]) + "</ul></section>")


def sources_html(rec: dict) -> str:
    rows = "".join(f'<li><span class="tag {"blue" if x["ok"] else "grey"}">{"Read" if x["ok"] else "Not read"}</span> '
                   f'{esc(x["name"])}' + (f' ({x["count"]})' if x["ok"] and x["count"] is not None else f': {esc(x["error"])}' if not x["ok"] else "")
                   + "</li>" for x in rec["sources"])
    return f'<section id="read"><h2>What this run read</h2><ul>{rows}</ul></section>'


STYLE = """
:root{--bg:#fff;--fg:#1b1f24;--dim:#57606a;--line:#d0d7de;--blue:#0550ae;--blue-bg:#ddf4ff;--orange:#953800;--orange-bg:#fff1e5;--grey:#57606a;--grey-bg:#eaeef2}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--dim:#9198a1;--line:#30363d;--blue:#79c0ff;--blue-bg:#0c2d6b;--orange:#ffa657;--orange-bg:#3d1d00;--grey:#9198a1;--grey-bg:#21262d}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:760px;margin:0 auto;padding:16px}
h1{font-size:1.5rem;margin:.2rem 0}h2{font-size:1.2rem;margin:1.6rem 0 .4rem;border-bottom:1px solid var(--line);padding-bottom:.2rem}
h3{font-size:1rem;margin:1rem 0 .2rem}ul{padding-left:1.2rem;margin:.3rem 0}li{margin:.25rem 0;overflow-wrap:anywhere}
a{color:var(--blue)}.dim{color:var(--dim);font-size:.92rem}
.tag{display:inline-block;border-radius:4px;padding:0 .4rem;font-size:.8rem;font-weight:600;vertical-align:1px}
.tag.blue{color:var(--blue);background:var(--blue-bg)}.tag.orange{color:var(--orange);background:var(--orange-bg)}
.tag.grey{color:var(--grey);background:var(--grey-bg)}
section.needs{border:2px solid var(--orange);border-radius:8px;padding:0 12px 10px}
section.needs h2{border:0}
"""


def render(rec: dict, s: dict) -> str:
    unread = [x["name"] for x in rec["sources"] if not x["ok"]]
    note = (f"Not read on this run: {', '.join(unread)} (shown as Not checked, never as none)." if unread
            else "Every source was read.")
    refresh = f"Rebuilt {s['refresh']}." if s.get("refresh") else "Rebuilt only when someone runs it."
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AES hub</title><style>{STYLE}</style></head><body><main>
<h1>AES hub</h1>
<p class="dim">Built {esc(stamp(rec["built"]))}. {esc(refresh)} {esc(note)} Colours always come with a word: orange means waiting on you or new,
blue means none or cleared, grey means not checked or count only.</p>
{needs_html(rec, s)}
{changed_html(rec)}
{links_html(rec)}
{sources_html(rec)}
<p class="dim">Built by <code>scripts/hub_page.py</code> in AES. Data for agents: <a href="hub.json">hub.json</a> beside this page.</p>
</main></body></html>
"""


# ---------------------------------------------------------------- publish

def prepare_data(run, s: dict) -> Path:
    """This job's own clone of the data branch (generated files only, started with no history the first time)."""
    path = RUNTIME / "data"
    if not (path / ".git").exists():
        path.mkdir(parents=True, exist_ok=True)
        run("init-data", ["git", "-C", str(path), "init", "--quiet"])
        run("remote-data", ["git", "-C", str(path), "remote", "add", "origin", s["remote"]])
    heads = run("find-data-branch", ["git", "-C", str(path), "ls-remote", "--heads", "origin", s["data_branch"]])
    if heads.returncode != 0:
        raise RuntimeError(f"ls-remote exit {heads.returncode}: {heads.stderr.strip()[-200:]}")
    if heads.stdout.strip():
        for name, cmd in (("fetch-data", ["fetch", "--quiet", "origin", s["data_branch"]]),
                          ("reset-data", ["checkout", "--quiet", "--force", "-B", "data", "FETCH_HEAD"])):
            out = run(name, ["git", "-C", str(path), *cmd])
            if out.returncode != 0:
                raise RuntimeError(f"{name} exit {out.returncode}: {out.stderr.strip()[-200:]}")
    else:
        run("start-data", ["git", "-C", str(path), "symbolic-ref", "HEAD", "refs/heads/data"])
    return path


def publish(run, path: Path, s: dict, when: str) -> bool:
    ident = ["-c", f"user.name={s['identity']['name']}", "-c", f"user.email={s['identity']['email']}"]
    if run("add-data", ["git", "-C", str(path), "add", "--", PAGE, DATA]).returncode != 0:
        return False
    if run("diff-data", ["git", "-C", str(path), "diff", "--cached", "--quiet"]).returncode == 0:
        run.log("nothing changed on the data branch")
        return True
    if run("commit-data", ["git", "-C", str(path), *ident, "commit", "--quiet", "-m", f"AES hub: {when}"]).returncode != 0:
        return False
    return run("push-data", ["git", "-C", str(path), "push", "--quiet", "origin",
                             f"HEAD:refs/heads/{s['data_branch']}"], timeout=180).returncode == 0


def write(folder: Path, page: str, rec: dict) -> None:
    (folder / PAGE).parent.mkdir(parents=True, exist_ok=True)
    (folder / PAGE).write_text(page, encoding="utf-8")
    (folder / DATA).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--no-push", action="store_true", help="build only; commit and push nothing")
    ap.add_argument("--out", type=Path, help="also write the page and hub.json under this folder")
    args = ap.parse_args(argv)
    try:
        s = settings()
    except wm.ConfigMissing as exc:
        print(exc, file=sys.stderr)
        return 2
    run = Run()
    start = time.time()
    now = dt.datetime.now(dt.timezone.utc)
    run.log(f"start settings={wm.config_path()} branch={s['data_branch']} push={not args.no_push}")
    data, previous, ok = None, None, True
    try:
        data = prepare_data(run, s)
        if (data / DATA).exists():
            previous = json.loads((data / DATA).read_text())
    except (RuntimeError, ValueError, OSError) as exc:
        run.log(f"data branch not read: {exc}")
        ok = False
    rec = build_record(s, run, now, previous)
    page = render(rec, s)
    ok = ok and all(x["ok"] for x in rec["sources"])
    if args.out:
        write(args.out, page, rec)
    if data is not None:
        write(data, page, rec)
        if not args.no_push and not publish(run, data, s, now.strftime("%Y-%m-%d %H:%M")):
            ok = False
    run.log(f"done needs_you={rec['needs_you_total']} sources_read={sum(x['ok'] for x in rec['sources'])}/"
            f"{len(rec['sources'])} new={len(rec['changed']['new'])} cleared={len(rec['changed']['cleared'])} "
            f"seconds={time.time() - start:.1f} page={s['site_url']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
