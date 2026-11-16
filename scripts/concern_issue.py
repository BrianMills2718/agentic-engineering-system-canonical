#!/usr/bin/env python3
"""Open, update, or close one keyed feedback concern in GitHub Issues.

ADR-2026-09-14 (one feedback concern lifecycle) makes GitHub Issues the single
register of open/closed feedback concerns. Native evidence (logs, receipts,
registers) stays where it is; this adapter only owns concern identity and state.

Implements: compliance-list/an-open-concern-s-title-follows-the-repository-s-current-status

Identity is a stable key, carried as a hidden marker in the issue body
(``<!-- concern-key: KEY -->``) under the ``concern:feedback`` label:

- ``open``  -- no issue for the key: create it. An open issue: comment one new
  occurrence. A closed issue: reopen it and comment the recurrence (a later
  failure after closure is the same concern, not a new one). The title passed
  is the concern's current title: an existing issue holding a different one is
  retitled (one issue per key, never one per status; code2-workspace#93).
- ``close`` -- an open issue for the key: comment the verifying evidence and
  close it. Nothing open: no-op.

Fails loud: any ``gh`` failure raises and exits non-zero, so the caller can
treat an un-registered concern as a failed step rather than a quiet success.

Trace reviews (the user, 2026-10-11, project-meta#2508): a concern that diagnoses,
scores or accepts a run passes ``--trace-review PATH`` (a TraceReviewV1 json
committed in a git repository; checked by company-planning
``validate_trace_review.py --retained`` before anything is filed) and the body
gains a ``Trace-Review: PATH`` line. A concern about no run passes
``--no-run-claim REASON``. Both are optional here so automated callers keep
working; agents are made to supply one by jev-gate rule T1.

Outside GitHub Actions, ``GITHUB_TOKEN`` is dropped from the child environment:
``~/.secrets/api_keys.env`` exports one meant for something else, and stock
``gh`` prefers it over its stored login (see ecosystem-ops scout.py preflight).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass

CONCERN_LABEL = "concern:feedback"
LABEL_COLORS = {"concern": "B60205", "source": "5319E7"}

Runner = Callable[[Sequence[str]], str]


@dataclass(frozen=True)
class Existing:
    """An issue already carrying a concern key: its number, state and title."""
    number: int
    state: str  # "OPEN" | "CLOSED"
    title: str = ""


def marker(key: str) -> str:
    """Return the hidden body marker that carries a concern key."""
    return f"<!-- concern-key: {key} -->"


def _child_env() -> dict[str, str]:
    """Return the environment for gh, without a GITHUB_TOKEN outside GitHub Actions."""
    env = dict(os.environ)
    if env.get("GITHUB_ACTIONS") != "true":
        env.pop("GITHUB_TOKEN", None)
    return env


REAL_GH_IN_TESTS_ENV = "CONCERN_ISSUE_ALLOW_REAL_GH"


def gh_runner(args: Sequence[str]) -> str:
    """Run gh with args and return its stdout; refuse under pytest and raise on failure."""
    # A test must never mutate the real concern register. Measured 2026-10-06:
    # one test called file_audit_escalation.main with a fake date and closed
    # seven real open audit-step concerns as "not red on 2026-09-08" -- and the
    # daily audit's own full-pytest step runs that test every day.
    if os.environ.get("PYTEST_CURRENT_TEST") and os.environ.get(REAL_GH_IN_TESTS_ENV) != "1":
        raise RuntimeError(
            "refusing to call the real gh from a test; inject a fake runner "
            f"(or set {REAL_GH_IN_TESTS_ENV}=1 deliberately)"
        )
    gh = shutil.which("gh")
    if gh is None:
        raise RuntimeError("gh CLI not found on PATH; cannot reach the concern register")
    result = subprocess.run(
        [gh, *args], capture_output=True, text=True, timeout=120, env=_child_env()
    )
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {result.stderr.strip()}")
    return result.stdout


def find_existing(repo: str, key: str, run: Runner) -> Existing | None:
    """Return the newest issue carrying the exact key marker, if any."""
    out = run(
        [
            "issue", "list", "-R", repo, "--label", CONCERN_LABEL, "--state", "all",
            "--search", f'"concern-key: {key}" in:body',
            "--json", "number,state,body,title", "--limit", "50",
        ]
    )
    # GitHub search is fuzzy; only an exact marker counts as the same concern.
    hits = [i for i in json.loads(out or "[]") if marker(key) in (i.get("body") or "")]
    if not hits:
        return None
    newest = max(hits, key=lambda i: i["number"])
    return Existing(number=newest["number"], state=newest["state"].upper(), title=newest.get("title") or "")


def ensure_labels(repo: str, labels: Sequence[str], run: Runner) -> None:
    """Create or update each label in repo."""
    for label in labels:
        color = LABEL_COLORS.get(label.split(":", 1)[0], "C5DEF5")
        run(["label", "create", label, "-R", repo, "--color", color, "--force"])


def occurrence_marker(occurrence: str) -> str:
    """Return the hidden marker that records one occurrence of a concern."""
    return f"<!-- concern-occurrence: {occurrence} -->"


def _already_recorded(repo: str, number: int, occurrence: str, run: Runner) -> bool:
    """Say whether issue number already records this occurrence in its body or comments."""
    out = run(["issue", "view", str(number), "-R", repo, "--json", "body,comments"])
    data = json.loads(out or "{}")
    texts = [data.get("body") or ""] + [c.get("body") or "" for c in data.get("comments") or []]
    return any(occurrence_marker(occurrence) in text for text in texts)


def _retitle(repo: str, existing: Existing, title: str, run: Runner) -> str:
    """Give the existing issue the concern's current title; return ", retitled" when it changed, else "".

    The title is set only when an issue is created, so a concern whose status moved on (a repository
    that was an error and is now out of date) kept its first title for good (code2-workspace#93).
    """
    if existing.title == title:
        return ""
    run(["issue", "edit", str(existing.number), "-R", repo, "--title", title])
    return ", retitled"


def open_concern(
    repo: str,
    key: str,
    title: str,
    body: str,
    source: str,
    run: Runner,
    occurrence: str | None = None,
    extra_labels: Sequence[str] = (),
) -> str:
    """Create, update, or reopen the keyed concern.

    ``occurrence`` identifies one observation (a date, a count). When the open
    issue already carries that occurrence it is not commented on again, so a job
    that re-runs on unchanged evidence does not comment every cycle. An existing
    issue is retitled to ``title`` whenever the two differ, in every one of those
    cases; the result names it (``commented #4, retitled``).
    """
    labels = [CONCERN_LABEL, f"source:{source}", *extra_labels]
    ensure_labels(repo, labels, run)
    existing = find_existing(repo, key, run)
    if occurrence is not None:
        body = f"{body}\n\n{occurrence_marker(occurrence)}"
    if existing is None:
        full_body = f"{body}\n\n{marker(key)}\n"
        url = run(
            ["issue", "create", "-R", repo, "--title", title, "--body", full_body,
             "--label", ",".join(labels)]
        ).strip()
        # gh has exited 0 with no output when GitHub refused the create (secondary rate limit, 2026-10-13).
        if "/issues/" not in url:
            raise RuntimeError(f"gh issue create returned no issue URL (got {url!r}); the concern was not filed")
        return f"created {url}"
    retitled = _retitle(repo, existing, title, run)
    if existing.state == "CLOSED":
        run(["issue", "reopen", str(existing.number), "-R", repo])
        run(["issue", "comment", str(existing.number), "-R", repo,
             "--body", f"**Recurred after closure.**\n\n{body}"])
        return f"reopened #{existing.number}{retitled}"
    if occurrence is not None and _already_recorded(repo, existing.number, occurrence, run):
        return f"unchanged #{existing.number}{retitled}"
    run(["issue", "comment", str(existing.number), "-R", repo,
         "--body", f"**Still red (new occurrence).**\n\n{body}"])
    return f"commented #{existing.number}{retitled}"


def close_concern(repo: str, key: str, evidence: str, run: Runner) -> str:
    """Comment the evidence and close the open concern for key; no-op when none is open."""
    existing = find_existing(repo, key, run)
    if existing is None or existing.state != "OPEN":
        return "no open concern"
    run(["issue", "comment", str(existing.number), "-R", repo,
         "--body", f"**Verified green; closing.**\n\n{evidence}"])
    run(["issue", "close", str(existing.number), "-R", repo, "--reason", "completed"])
    return f"closed #{existing.number}"


TRACE_REVIEW_VALIDATOR = os.environ.get("TRACE_REVIEW_VALIDATOR") or os.path.expanduser(
    "~/code/inside-success/repos/company-planning/plugins/company-planning/scripts/validate_trace_review.py")


def check_trace_review(path: str) -> str:
    """Validate a retained trace review; return its repo-relative path or raise SystemExit."""
    full = os.path.abspath(os.path.expanduser(path))
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=os.path.dirname(full) or ".",
                         capture_output=True, text=True)
    if top.returncode or not os.path.isfile(full):
        raise SystemExit(f"--trace-review {path}: not a file inside a git repository")
    if not os.path.isfile(TRACE_REVIEW_VALIDATOR):
        raise SystemExit(f"--trace-review: validator not found at {TRACE_REVIEW_VALIDATOR}")
    root = top.stdout.strip()
    rel = os.path.relpath(full, root)
    done = subprocess.run([sys.executable, TRACE_REVIEW_VALIDATOR, "--repo-root", root, "--retained", rel],
                          cwd=root, capture_output=True, text=True)
    print(done.stdout.strip(), file=sys.stderr)
    if done.returncode:
        raise SystemExit(f"--trace-review {path}: invalid ({done.stdout.strip()[-600:] or done.stderr.strip()[-600:]})")
    return full


def trace_review_lines(reviews: Sequence[str], no_run_claim: str | None,
                       check: Callable[[str], str] | None = None) -> str:
    """Return the body lines naming each checked trace review, or the no-run-claim reason."""
    check = check or check_trace_review
    if reviews and no_run_claim:
        raise SystemExit("pass --trace-review or --no-run-claim, not both")
    if no_run_claim is not None:
        if len(no_run_claim.strip()) < 8:
            raise SystemExit("--no-run-claim needs a reason of 8+ characters")
        return f"Trace-Review: none ({no_run_claim.strip()})"
    return "\n".join(f"Trace-Review: {check(r)}" for r in reviews)


def main(argv: list[str] | None = None, run: Runner = gh_runner) -> int:
    """Parse the command line and open or close one concern; return the exit status."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    op = sub.add_parser("open", help="create, update, or reopen the keyed concern")
    op.add_argument("--repo", required=True)
    op.add_argument("--key", required=True)
    op.add_argument("--title", required=True)
    op.add_argument("--body", required=True)
    op.add_argument("--source", required=True, help="label suffix, e.g. daily-audit")
    op.add_argument("--occurrence", default=None, help="skip commenting if this occurrence is already recorded")
    op.add_argument("--trace-review", action="append", default=[], metavar="PATH",
                    help="committed TraceReviewV1 json for a run this concern diagnoses (repeatable)")
    op.add_argument("--no-run-claim", default=None, metavar="REASON",
                    help="why this concern makes no claim about a run")
    cl = sub.add_parser("close", help="close the keyed concern with verifying evidence")
    cl.add_argument("--repo", required=True)
    cl.add_argument("--key", required=True)
    cl.add_argument("--evidence", required=True)
    args = parser.parse_args(argv)

    if args.command == "open":
        lines = trace_review_lines(args.trace_review, args.no_run_claim)
        body = f"{args.body}\n\n{lines}" if lines else args.body
        print(open_concern(args.repo, args.key, args.title, body, args.source, run, occurrence=args.occurrence))
    else:
        print(close_concern(args.repo, args.key, args.evidence, run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
