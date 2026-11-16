#!/usr/bin/env python3
"""Turn every failed systemd --user unit into one keyed concern issue.

A timer job that crashes leaves only a journal line unless it reports its own
failure, and a crash early in a script skips that reporting (2026-10-13: the
brianmills.dev/me check died at its first step for a day, silently). This watch
covers every user unit at once, so a job does not have to get its own failure
path right to be heard (Policy `loud-failures-reach-an-agent`).

It runs every 30 minutes from failed-unit-watch.timer. An instant variant (a top-level OnFailure=
drop-in on every user service) was tried and removed on 2026-10-13: services with Restart=on-failure
fire OnFailure= on every crash, and three crash-looping services started the sweep about 500 times in
an hour. Instant reporting needs a design that handles restart loops (issue #2583).

Each run:
  * lists failing user units: those in the failed state now, those whose last recorded run failed, and those
    already reported with no later success. A reboot clears systemd's failed state without any job having
    recovered, and WSL reboots often, so the failed state alone closed issues as "verified green" on jobs that
    were still broken;
  * opens (or comments on) concern key `failed-unit:<unit>` in the repository
    that owns the unit's ExecStart script (falls back to the configured concern repository), with the
    unit's last journal lines as the body;
  * closes the concern for a reported unit once a later run succeeded or the unit no longer exists, in the
    repository the concern was opened in (the owner is worked out once, when the unit is first reported);
  * adopts an open `failed-unit:` concern the state has no entry for (one stranded by the owner drift of #2599, a
    lost state file, or a close that gave up), so the same close path reaches it. Adopted units are treated as
    reported with no run since, so a reboot's empty journal does not close them either (project-meta#2664 stayed
    open for four days after the unit had been green for four runs);
  * then does the same for Healthchecks.io: a job that never runs fails no unit, so it is invisible above,
    but its check goes "down" (personal-file-infra#248: run-artifacts-pack sat down 19 days and only
    emailed Brian). Each down check from `GET /api/v3/checks/` gets concern key `healthcheck-down:<slug>`
    in the repository that owns `<slug>.service` (check slugs are unit names, see personal-file-infra
    hc_sync.py), reported once, and closed once the check is no longer down (up, or paused on purpose).
    The key is separate from `failed-unit:` so neither path closes the other's issue.

State (which units and checks were reported) lives in two small JSON files so a
unit or check that recovered can be closed. Exit 0 when the sweep ran (failures are
carried by the issues), 2 when either sweep could not run or could not file an issue
(including Healthchecks.io unreachable twice, or HEALTHCHECKS_API_KEY missing from
~/.secrets/api_keys.env).

Usage:
  python3 scripts/failed_unit_watch.py            # sweep and report
  python3 scripts/failed_unit_watch.py --dry-run  # print what it would do
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from collections.abc import Callable, Iterable
from pathlib import Path

HOME = Path.home()
CONFIG = Path(os.environ.get("PROJECT_GRAPH") or HOME / "code2/aes-config/PROJECT_GRAPH.json").parent / "graph-config.yaml"


def setting(key: str, env: str) -> str:
    """One value from the environment, else `key:` in graph-config.yaml beside the project graph. No value is a loud stop."""
    named = os.environ.get(env)
    if named:
        return named
    try:
        found = re.search(rf"^{key}:\s*(\S+)", CONFIG.read_text(), re.M)
    except OSError:
        found = None
    if not found:
        raise SystemExit(f"failed_unit_watch: no {key} named: set {env} or put `{key}:` in {CONFIG}")
    return found.group(1)


OWNER = setting("owner", "PROJECT_GRAPH_OWNER")
FALLBACK_REPO = setting("concern_repo", "CONCERN_REPO")  # a unit whose script has no repository of the owner's files its concern here
CONCERN = Path(__file__).resolve().parent / "concern_issue.py"
STATE = HOME / "projects/data/logs/failed_unit_watch_state.json"
JOURNAL_LINES = 30
UNIT_FAILURE = "d9b373ed55a64feb8242e02dbe79a49c"  # systemd SD_MESSAGE_UNIT_FAILURE
UNIT_SUCCESS = "7ad2d189f7e94e70a38c781354912448"  # systemd SD_MESSAGE_UNIT_SUCCESS
UNIT_STARTED = "39f53479d3a045ac8e11786248231fbf"  # systemd SD_MESSAGE_UNIT_STARTED, "Finished" for a one-shot job
CLOSE_RETRIES = 4  # runs to keep looking for a just-opened issue before giving up
HC_STATE = HOME / "projects/data/logs/healthchecks_watch_state.json"
HC_API = "https://healthchecks.io/api/v3/checks/"
SECRETS = HOME / ".secrets/api_keys.env"


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def failed_units() -> list[str]:
    out = run(["systemctl", "--user", "list-units", "--failed", "--plain", "--no-legend", "--no-pager"])
    return parse_failed(out)


# A transient unit from `systemd-run` without a name (run-u2958.service, run-r1a2b.scope) is an agent's one-off
# experiment, not a recurring job: it gets no concern issue (harness review 2026-11-07, Work flow decision 9, under
# Brian's decision rule of 2026-11-07: "i am auto approving al decisions that arent high significane and low
# confidence").
TRANSIENT = re.compile(r"^run-[ur][0-9a-f]+\.(service|scope)$")


def parse_failed(listing: str) -> list[str]:
    """First column of each line is the unit name (a leading status bullet is dropped); transient run-u* units are left out."""
    units = []
    for line in listing.splitlines():
        parts = line.replace("●", " ").split()
        if parts and "." in parts[0] and not TRANSIENT.match(parts[0]):
            units.append(parts[0])
    return units


def last_outcomes() -> dict[str, bool]:
    """For each unit in the journal, whether the last run it recorded failed. Reads systemd's message ids, not words."""
    out = run(["journalctl", "--user", f"MESSAGE_ID={UNIT_FAILURE}", "+", f"MESSAGE_ID={UNIT_SUCCESS}", "+",
               f"MESSAGE_ID={UNIT_STARTED}", "-o", "json", "--no-pager", "--output-fields=USER_UNIT,UNIT,MESSAGE_ID"])
    return read_outcomes(out)


def read_outcomes(journal_json: str) -> dict[str, bool]:
    outcomes: dict[str, bool] = {}
    for line in journal_json.splitlines():
        entry = json.loads(line)
        unit = entry.get("USER_UNIT") or entry.get("UNIT")
        if unit:
            outcomes[unit] = entry.get("MESSAGE_ID") == UNIT_FAILURE
    return outcomes


def is_scheduled(unit: str) -> bool:
    """Still installed and something still runs it: a timer, or it is enabled or static. A disabled unit nothing starts is not a job."""
    shown = dict(line.partition("=")[::2] for line in run(["systemctl", "--user", "show", "-p", "LoadState,UnitFileState,TriggeredBy", unit]).splitlines())
    return scheduled_from(shown)


def scheduled_from(shown: dict[str, str]) -> bool:
    if shown.get("LoadState") != "loaded":
        return False
    return bool(shown.get("TriggeredBy")) or shown.get("UnitFileState") in {"enabled", "enabled-runtime", "static", "linked", "linked-runtime", "generated"}


def failing_units(now_failed: list[str], outcomes: dict[str, bool], previous: Iterable[str], loaded=is_scheduled) -> list[str]:
    """Failed now, or last run failed, or reported before with no recorded run since. A removed or switched-off unit is not failing."""
    failing = list(now_failed)
    others = {u for u, failed in outcomes.items() if failed} | {u for u in previous if u not in outcomes}
    failing += [u for u in sorted(others - set(now_failed)) if loaded(u) and not TRANSIENT.match(u)]
    return failing


def repo_from_remote(url: str) -> str | None:
    # github.com, or an SSH host alias such as `github-personal` (git@github-personal:Owner/repo.git)
    m = re.search(r"github(?:\.com|-[\w.-]+)[:/]([^/]+)/([^/\s]+?)(?:\.git)?$", url.strip())
    if m and m.group(1).lower() == OWNER.lower():
        return f"{m.group(1)}/{m.group(2)}"
    return None


def exec_paths(show_execstart: str) -> list[str]:
    """Absolute paths named in `systemctl show -p ExecStart` output (interpreter and script)."""
    return re.findall(r"(/[^\s;]+)", show_execstart)


def owning_repo(unit: str) -> str:
    try:
        show = run(["systemctl", "--user", "show", "-p", "ExecStart", "--value", unit])
    except subprocess.CalledProcessError:
        return FALLBACK_REPO
    for path in exec_paths(show):
        p = Path(path)
        if not str(p).startswith(str(HOME)):
            continue  # /usr/bin/python3 and the like
        folder = p if p.is_dir() else p.parent
        if not folder.exists():
            continue
        try:
            url = run(["git", "-C", str(folder), "remote", "get-url", "origin"])
        except subprocess.CalledProcessError:
            continue
        repo = repo_from_remote(url)
        if repo:
            return repo
    return FALLBACK_REPO


def journal_tail(unit: str) -> str:
    try:
        return run(["journalctl", "--user", "-u", unit, "-n", str(JOURNAL_LINES), "--no-pager", "-o", "short-iso"])
    except subprocess.CalledProcessError as exc:
        return f"(journal unavailable: {exc})"


def load_state(path: Path = STATE) -> dict:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def plan(previous: dict[str, str], failing: dict[str, str]) -> tuple[dict[str, str], dict[str, str]]:
    """(to_open, to_close): a unit is reported once, when it first fails; previously reported units now healthy close.

    Reporting every failing unit on every run commented on a still-failing unit each sweep (#2574, 100 comments)."""
    to_open = {u: r for u, r in failing.items() if u not in previous}
    to_close = {u: r for u, r in previous.items() if u not in failing}
    return to_open, to_close


CONCERN_KEY = re.compile(r"<!-- concern-key: failed-unit:(\S+) -->")
CONCERN_SOURCE_LABEL = "source:failed-unit-watch"


def open_concerns() -> list[dict]:
    """Every open issue this watch filed, under the owner's repositories: repository, number, body, updatedAt.

    One retry: an external call that fails twice is treated as down. GITHUB_TOKEN is dropped as concern_issue does,
    because gh prefers it over its stored login."""
    env = {k: v for k, v in os.environ.items() if k != "GITHUB_TOKEN"}
    cmd = ["gh", "search", "issues", "--owner", OWNER, "--state", "open", "--label", CONCERN_SOURCE_LABEL,
           "--limit", "200", "--json", "repository,number,body,updatedAt"]
    for attempt in (1, 2):
        try:
            return json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120, env=env).stdout or "[]")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            if attempt == 2:
                raise
            time.sleep(5)
    return []


def adoptable(state: dict[str, str], issues: Iterable[dict]) -> dict[str, str]:
    """unit -> repo for each open `failed-unit:` concern whose unit has no state entry (the most recently updated
    issue when one unit has several). A unit already in the state keeps the repository recorded there."""
    found: dict[str, str] = {}
    for issue in sorted(issues, key=lambda i: i.get("updatedAt") or ""):
        m = CONCERN_KEY.search(issue.get("body") or "")
        if m and m.group(1) not in state:
            found[m.group(1)] = issue["repository"]["nameWithOwner"]
    return found


def concern(action: str, repo: str, key: str, extra: list[str], dry: bool) -> str:
    cmd = [sys.executable, str(CONCERN), action, "--repo", repo, "--key", key, *extra]
    if dry:
        print("DRY", " ".join(cmd[:8]))
        return ""
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def hc_api_key(secrets_text: str) -> str:
    """The read key from ~/.secrets/api_keys.env text (`[export ]HEALTHCHECKS_API_KEY=...`). Never printed."""
    for line in secrets_text.splitlines():
        m = re.match(r"^(?:export )?HEALTHCHECKS_API_KEY=(.*)$", line)
        if m:
            return m.group(1).strip().strip("'\"")
    return ""


def _hc_get(url: str, key: str):
    req = urllib.request.Request(url, headers={"X-Api-Key": key})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def hc_fetch_checks(key: str) -> list[dict]:
    """Every check on the project. One retry: an external call that fails twice is treated as down."""
    try:
        return _hc_get(HC_API, key)["checks"]
    except OSError:
        time.sleep(5)
        return _hc_get(HC_API, key)["checks"]


def hc_fetch_pings(key: str, uuid: str) -> list[dict]:
    """Newest pings first; best effort (only for the issue body), so any failure gives no pings."""
    try:
        return _hc_get(f"{HC_API}{uuid}/pings/", key).get("pings", [])
    except (OSError, ValueError, KeyError):
        return []


def down_checks(checks: list[dict]) -> dict[str, dict]:
    """slug -> check for checks Healthchecks.io calls "down" (a fail ping, or no success by its deadline plus grace)."""
    return {c["slug"]: c for c in checks if c.get("status") == "down" and c.get("slug")}


def hc_down_body(check: dict, pings: list[dict], tail: str) -> str:
    slug = check["slug"]
    unit = f"{slug}.service"
    recent = "\n".join(f"- {p.get('date', '?')} {p.get('type', '?')}" for p in pings[:5]) or "- (pings unavailable)"
    return (f"The Healthchecks.io check `{slug}` is down: the job `{unit}` either reported a failure or did not "
            f"report a success by its deadline (schedule `{check.get('schedule') or check.get('timeout')}`, "
            f"grace {check.get('grace')} s). A job that never starts fails no systemd unit, so this is the only alert "
            f"that reaches an agent (personal-file-infra#248).\n\n"
            f"Look at `systemctl --user status {unit}` and `systemctl --user list-timers` for why it did not run or "
            f"what failed; fix the cause and let it run (`systemctl --user start {unit}`). This concern closes itself "
            f"once the check is no longer down (a success ping, or the check paused on purpose).\n\n"
            f"Last ping: {check.get('last_ping')}\n\nRecent pings (newest first):\n{recent}\n\n"
            f"Last journal lines:\n```\n{tail}\n```")


def healthchecks_sweep(dry: bool, state_path: Path = HC_STATE, fetch: Callable[[], list[dict]] | None = None,
                       repo_for: Callable[[str], str] = None, pings: Callable[[str], list[dict]] | None = None,
                       tail: Callable[[str], str] = None, concern_fn=None) -> tuple[int, int, int]:
    """(opened, recovered, errors). Same lifecycle as failed units: report once, close on recovery, retry a close
    that cannot find its just-opened issue."""
    repo_for = repo_for or owning_repo
    tail = tail or journal_tail
    concern_fn = concern_fn or concern
    if fetch is None or pings is None:
        try:
            key = hc_api_key(SECRETS.read_text())
        except OSError:
            key = ""
        if not key:
            print("HEALTHCHECKS SWEEP FAILED: no HEALTHCHECKS_API_KEY in ~/.secrets/api_keys.env")
            return 0, 0, 1
        fetch = fetch or (lambda: hc_fetch_checks(key))
        pings = pings or (lambda uuid: hc_fetch_pings(key, uuid))
    state = load_state(state_path)
    tries: dict[str, int] = state.pop("_close_tries", {})
    try:
        down = down_checks(fetch())
    except (OSError, ValueError, KeyError) as exc:
        print(f"HEALTHCHECKS SWEEP FAILED: could not read {HC_API}: {type(exc).__name__}: {exc}")
        return 0, 0, 1
    failing = {slug: state.get(slug) or repo_for(f"{slug}.service") for slug in down}
    to_open, to_close = plan(state, failing)
    errors = 0
    for slug, repo in to_open.items():
        check = down[slug]
        body = hc_down_body(check, pings(check["uuid"]) if check.get("uuid") else [], tail(f"{slug}.service"))
        try:
            concern_fn("open", repo, f"healthcheck-down:{slug}", ["--source", "failed-unit-watch",
                       "--title", f"Healthchecks.io check down: {slug}", "--body", body], dry)
            print(f"DOWN    {slug}  -> concern in {repo}")
        except subprocess.CalledProcessError as exc:
            errors += 1
            failing.pop(slug)  # not reported: try again next run
            print(f"REPORT FAILED {slug}: {exc}")
    for slug, repo in to_close.items():
        try:
            out = concern_fn("close", repo, f"healthcheck-down:{slug}",
                             ["--evidence", f"Healthchecks.io check {slug} is no longer down"], dry)
            if "no open concern" in out and tries.get(slug, 0) < CLOSE_RETRIES:
                failing[slug] = repo
                tries[slug] = tries.get(slug, 0) + 1
                print(f"UP      {slug}  -> no open issue found yet in {repo}; retry {tries[slug]}/{CLOSE_RETRIES}")
                continue
            print(f"UP      {slug}  -> {out.strip() or 'closed'} in {repo}")
        except subprocess.CalledProcessError as exc:
            errors += 1
            failing[slug] = repo
            print(f"CLOSE FAILED {slug}: {exc}")
    if not dry:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        tries = {s: n for s, n in tries.items() if s in failing and s not in to_open}
        state_path.write_text(json.dumps({**failing, "_close_tries": tries}, indent=1, sort_keys=True))
    opened = len([s for s in to_open if s in failing])
    print(f"HEALTHCHECKS: {opened} down, {len(to_close)} back up, {errors} reporting errors")
    return opened, len(to_close), errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    state = load_state()
    tries: dict[str, int] = state.pop("_close_tries", {})
    errors = 0
    try:
        adopted = adoptable(state, open_concerns())
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as exc:
        errors += 1
        adopted = {}
        print(f"ADOPT FAILED: could not list open concerns: {type(exc).__name__}: {exc}")
    for unit, repo in adopted.items():
        print(f"ADOPT   {unit}  -> open concern in {repo} had no state entry; tracked from now so a later run closes it")
    state = {**state, **adopted}
    try:
        # A unit already reported keeps the repository its issue was opened in. Working the owner out again on every
        # sweep moved the state to another repository when the answer changed (project-meta#2599: a remote alias fix),
        # and the close then looked for the issue in the wrong repository and gave up, leaving it open for good.
        failing = {u: state.get(u) or owning_repo(u) for u in failing_units(failed_units(), last_outcomes(), state)}
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"SWEEP FAILED: could not list failing units: {exc}")
        healthchecks_sweep(args.dry_run)  # a job that never ran is still reported when systemd cannot be read
        return 2
    to_open, to_close = plan(state, failing)
    for unit, repo in to_open.items():
        body = (f"The last run of the systemd --user unit `{unit}` failed on this machine. "
                f"Fix the cause, then run it (`systemctl --user start {unit}`) or let its next run succeed; "
                f"this concern closes itself once a run succeeds. Clearing the failed state does not close it.\n\n"
                f"Last journal lines:\n"
                f"```\n{journal_tail(unit)}\n```")
        try:
            concern("open", repo, f"failed-unit:{unit}", ["--source", "failed-unit-watch",
                                          "--title", f"Timer job failed: {unit}", "--body", body], args.dry_run)
            print(f"FAILED  {unit}  -> concern in {repo}")
        except subprocess.CalledProcessError as exc:
            errors += 1
            print(f"REPORT FAILED {unit}: {exc}")
    for unit, repo in to_close.items():
        try:
            out = concern("close", repo, f"failed-unit:{unit}", ["--evidence", f"{unit}: a later run succeeded, or the unit was removed"], args.dry_run)
            if "no open concern" in out and tries.get(unit, 0) < CLOSE_RETRIES:
                # concern_issue finds issues through GitHub search, which can miss one opened minutes ago;
                # keep the unit and try again next run rather than leave the issue open for good.
                failing[unit] = repo
                tries[unit] = tries.get(unit, 0) + 1
                print(f"RECOVERED {unit}  -> no open issue found yet in {repo}; retry {tries[unit]}/{CLOSE_RETRIES}")
                continue
            print(f"RECOVERED {unit}  -> {out.strip() or 'closed'} in {repo}")
        except subprocess.CalledProcessError as exc:
            errors += 1
            failing[unit] = repo  # keep it so the close is retried next run
            print(f"CLOSE FAILED {unit}: {exc}")
    if not args.dry_run:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        tries = {u: n for u, n in tries.items() if u in failing and u not in to_open}
        STATE.write_text(json.dumps({**failing, "_close_tries": tries}, indent=1, sort_keys=True))
    print(f"RESULT: {len(to_open)} failed, {len(to_close)} recovered, {errors} reporting errors")
    _, _, hc_errors = healthchecks_sweep(args.dry_run)
    return 2 if errors or hc_errors else 0


if __name__ == "__main__":
    sys.exit(main())
