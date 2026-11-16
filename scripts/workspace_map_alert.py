#!/usr/bin/env python3
"""Run the ~/code workspace check and tell the operator about NEW problems, once.

Implements: workspace-map-check/alert-once-per-state-change
Implements: workspace-map-check/crash-is-not-a-finding

Wraps scripts/workspace_map.py --check with this repository's existing channels (nothing new invented):
  * GitHub concern  scripts/concern_issue.py  (one keyed concern, closed when resolved), filed in the concern
                    repository: CONCERN_REPO, else `concern_repo:` in graph-config.yaml beside the project graph
  * phone push      scripts/learning_loop/notify.py push(): one Telegram message (Decision 17 A). It replaces
                    Project Meta's ntfy router, whose 6-hour minimum interval between pushes is not carried over:
                    this script already pushes only on a state change.

Once per state change:
  clean -> problems   : open the concern and push one ntfy message
  problems change     : comment the new occurrence on the concern and push one message (hash of the findings differs)
  problems unchanged  : nothing (the daily run stays silent; --occurrence makes the issue call a no-op too)
  problems -> clean   : close the concern with the clean run as evidence (no push; the issue closing is the "cleared")

--test uses a separate concern key, a [TEST] title and its own state file, so the behaviour can be proven without touching the real alert.
Exit code is 1 while problems exist, so the systemd unit also shows as failed; 2 when the check crashed
(including a missing settings file), so a crash never looks like an ordinary day with findings.

Ported from Project Meta `scripts/workspace_map_alert.py` (retirement plan step 6). The state files in STATE_DIR
keep the same keys and hash format.
"""
import argparse, hashlib, importlib.util, json, os, re, subprocess, sys, time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import workspace_map as wm  # noqa: E402

KEY = "workspace-map-check"
STATE_DIR = os.path.expanduser("~/.local/state/workspace-map-check")
CONCERN = os.path.join(HERE, "concern_issue.py")
NO_RUN_CLAIM = "workspace housekeeping check; diagnoses no run"


def setting(key: str, env: str) -> str:
    """One value from the environment, else `key:` in graph-config.yaml beside the project graph. No value is a loud stop."""
    named = os.environ.get(env)
    if named:
        return named
    config = Path(os.environ.get("PROJECT_GRAPH") or Path.home() / "code2/aes-config/PROJECT_GRAPH.json").parent / "graph-config.yaml"
    try:
        found = re.search(rf"^{key}:\s*(\S+)", config.read_text(), re.M)
    except OSError:
        found = None
    if not found:
        raise wm.ConfigMissing(f"workspace_map_alert: no {key} named: set {env} or put `{key}:` in {config}")
    return found.group(1)


def telegram_push(title: str, body: str) -> dict:
    """learning_loop/notify.py push(), loaded by path (learning_loop is not a package)."""
    spec = importlib.util.spec_from_file_location("learning_loop_notify", os.path.join(HERE, "learning_loop", "notify.py"))
    notify = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(notify)
    return notify.push(title, body)


def _load(path):
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return {"open": False, "hash": None}


def main(argv=None, runner=subprocess.run, push=telegram_push):
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=os.path.expanduser("~/projects/data/logs/workspace_health.md"))
    ap.add_argument("--test", action="store_true", help="separate concern key + [TEST] label + separate state file")
    ap.add_argument("--dry-run", action="store_true", help="print what would be filed/pushed; touch nothing")
    a = ap.parse_args(argv)
    repo = setting("concern_repo", "CONCERN_REPO")
    key = KEY + ("-test" if a.test else "")
    prefix = "[TEST] " if a.test else ""
    state_path = os.path.join(STATE_DIR, key + ".json")

    rows, ex = wm.classify()
    f = wm.check(rows, ex)
    text, n = wm.render_report(f, rows)
    os.makedirs(os.path.dirname(a.report), exist_ok=True)
    open(a.report, "w").write(text + "\n")
    actionable = {k: sorted(v) for k, v in f.items() if not k.startswith("INFO")}
    h = hashlib.sha256(json.dumps(actionable, sort_keys=True).encode()).hexdigest()[:16]
    state = _load(state_path)
    stamp = time.strftime("%Y-%m-%d %H:%M")

    if not actionable:
        if state.get("open"):
            print(f"cleared: closing concern {key}")
            if not a.dry_run:
                runner([sys.executable, CONCERN, "close", "--repo", repo, "--key", key,
                        "--evidence", f"{prefix}Fresh workspace check at {stamp} found nothing needing action."], check=True)
                state = {"open": False, "hash": None}
        else:
            print("clean; nothing to do")
        if not a.dry_run:
            os.makedirs(STATE_DIR, exist_ok=True)
            json.dump(state, open(state_path, "w"))
        return 0

    def _label(cat, items):
        short = cat.split(" (")[0].split(":")[0].replace("WARN ", "").strip()
        first = items[0].split(" ")[0].rstrip(":")
        return f"{short} ({first}{' +%d more' % (len(items) - 1) if len(items) > 1 else ''})" if not first[:1].isdigit() else short
    summary = "; ".join(_label(c, v) for c, v in actionable.items())[:180]
    if state.get("open") and state.get("hash") == h:
        print(f"unchanged ({summary}); staying silent")
        return 1
    title = f"{prefix}Workspace check: {summary}"[:200]
    body = f"{prefix}Run `python3 scripts/workspace_map.py --check` for details. Report: ~/projects/data/logs/workspace_health.md\n\n" + text
    print(f"NEW/CHANGED -> {title}")
    if a.dry_run:
        return 1
    runner([sys.executable, CONCERN, "open", "--repo", repo, "--key", key, "--title", title,
            "--body", body, "--source", "workspace-map-check", "--occurrence", h, "--no-run-claim", NO_RUN_CLAIM], check=True)
    msg = f"{prefix}{summary}. Details: GitHub concern '{key}' in {repo}, or ~/projects/data/logs/workspace_health.md."
    res = push(f"{prefix}Workspace check needs you", msg[:400])
    print(f"  push: delivered={res.get('delivered')} {res.get('evidence')}")  # arrival evidence in the log, not just a call
    os.makedirs(STATE_DIR, exist_ok=True)
    json.dump({"open": True, "hash": h}, open(state_path, "w"))
    return 1


MD_CAP_KEY = "md-file-cap"


def md_cap_concern(dry_run=False, test=False, runner=subprocess.run):
    """Daily Markdown-file cap (scripts/md_file_cap.py) as its own keyed concern, once per state change.

    Agent work, not Brian's: an over-cap repo is pruned or given a reasoned exception by whichever
    agent works the concern queue, so this opens/comments/closes the concern and never pushes to his phone.
    """
    import md_file_cap
    repo = setting("concern_repo", "CONCERN_REPO")
    key = MD_CAP_KEY + ("-test" if test else "")
    prefix = "[TEST] " if test else ""
    state_path = os.path.join(STATE_DIR, key + ".json")
    rows = md_file_cap.evaluate(md_file_cap.owned_checkouts(wm.graph_path()), md_file_cap.DEFAULT_CAP)
    bad = sorted((r for r in rows if r["status"] in ("over", "not-checked") or r.get("reach") in ("orphans", "no-wiki")
                  or r.get("layout") == "findings" or r.get("durable") == "findings"),
                 key=lambda r: -(r["md"] or 0))
    print(f"md-file-cap: {len(rows)} repos checked, {len(bad)} breaking the cap, wiki reachability, the declared layout or the durable document set")
    # Which repos are over (and why, without counts): a file added to an already-listed repo is not news.
    h = hashlib.sha256(json.dumps([(r["repo"], r["status"], r["limit"] if r["md"] is not None else None, r.get("reach"), r.get("layout"), r.get("durable")) for r in bad]).encode()).hexdigest()[:16]
    state = _load(state_path)
    if not bad:
        if state.get("open") and not dry_run:
            runner([sys.executable, CONCERN, "close", "--repo", repo, "--key", key,
                            "--evidence", f"{prefix}Fresh md-file-cap run at {time.strftime('%Y-%m-%d %H:%M')}: every Brian-owned repo is within its cap, its wiki reaches its reader documents, and any declared layout and durable document set holds."], check=True)
        if not dry_run:
            os.makedirs(STATE_DIR, exist_ok=True)
            json.dump({"open": False, "hash": None}, open(state_path, "w"))
        return
    if state.get("open") and state.get("hash") == h:
        print("md-file-cap: unchanged; staying silent")
        return
    over = sum(r["status"] in ("over", "not-checked") for r in bad)
    unreach = sum(r.get("reach") in ("orphans", "no-wiki") for r in bad)
    misplaced = sum(r.get("layout") == "findings" for r in bad)
    drifted = sum(r.get("durable") == "findings" for r in bad)
    title = (f"{prefix}Docs rule: {over} repos over 100 .md, {unreach} with docs not reachable from wiki/index.md, "
             f"{misplaced} with documents outside their declared layout, {drifted} with a failing durable document set")[:200]
    body = (f"{prefix}Rule: a Brian-owned repo holds at most {md_file_cap.DEFAULT_CAP} git-tracked .md files unless it has a "
            f"`{md_file_cap.EXCEPTION_FILE}` with a `limit` and a plain `reason` (Brian, 2026-10-07). For each repo below, work in "
            "that repo: prune generated or stale Markdown (pack generated output instead of committing one file per item), or add "
            "the exception file when the Markdown is the repo's product. Second rule (same date): every reader document is "
            "reachable from the repo's wiki/index.md within two links; link it from the wiki section a reader would look in, or "
            "list a source-material folder under `unlinked_ok` in the exception file with its reason. Third: a repo that declares "
            "its layout in .agentic/repo.yaml keeps decisions, design, numbered plans and committed generator output under the "
            "declared roots and generated/; move the file there (repointing its readers), or list it under `layout_ok` with a "
            "reason. Fourth: a repo that declares `durable_documents` in .agentic/repo.yaml keeps that set passing company-planning's "
            "`durable_docs_check.py --repo <repo> --arc42` (goal, requirements, system model and trace, decisions with Governs lines, "
            "plans, catalog); fix the named document or trace entry. Re-run "
            "`python3 scripts/md_file_cap.py` to confirm.\n\n"
            + "\n".join(f"- {r['repo']}: " + "; ".join(x for x in (r['detail'] if r['status'] in ('over', 'not-checked') else '',
                                                                 r.get('reach_detail') or '', r.get('layout_detail') or '',
                                                                 r.get('durable_detail') if r.get('durable') == 'findings' else '') if x) for r in bad))
    print(f"md-file-cap: NEW/CHANGED -> {title}")
    if dry_run:
        return
    runner([sys.executable, CONCERN, "open", "--repo", repo, "--key", key, "--title", title,
            "--body", body, "--source", "md-file-cap", "--occurrence", h, "--no-run-claim", NO_RUN_CLAIM], check=True)
    os.makedirs(STATE_DIR, exist_ok=True)
    json.dump({"open": True, "hash": h}, open(state_path, "w"))


def run_main():
    """Exit 1 means findings; a crash must not look like findings, so it prints CRASH and returns 2."""
    try:
        return main()
    except Exception as exc:  # loud: exit 2 makes the unit show failed, unlike exit 1 (findings)
        import traceback
        traceback.print_exc()
        print(f"CRASH: workspace check did not finish: {exc!r}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    rc = run_main()
    _a = sys.argv[1:]
    try:
        md_cap_concern(dry_run="--dry-run" in _a, test="--test" in _a)
    except (Exception, SystemExit) as exc:  # loud: the unit fails and the log names the cause; the workspace check above already ran
        print(f"md-file-cap concern step FAILED: {exc!r}", file=sys.stderr)
        rc = rc or 2
    sys.exit(rc)
