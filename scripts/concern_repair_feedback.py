#!/usr/bin/env python3
"""Observer and verifier for root-cause concern repair (ADR-2026-09-14 slice 3).

``observe`` selects the oldest open GitHub concern labeled both
``concern:feedback`` and ``agent:repair`` whose kind has a source-signal check,
skipping concerns in repair backoff and honoring a daily repair cap. It emits a
Plan 273 ``feedback-observation/v1`` envelope; when nothing is eligible it emits
a passing queue observation, which creates no repair work.

``verify`` runs in the repair workspace (the runtime sets cwd). On a repair
branch it enforces every closure gate and never trusts the agent's report:

a. the committed report validates against ``RootCauseRepairReport``;
b. the declared prevention paths are actually changed in the diff;
c. the recurrence proof is executed: run on the observed revision with only its
   declared harness files (never the fix) copied in, it fails there, and it passes
   on the fix;
d. the concern's own source signal is green at the fix revision;
e. an independent reviewer (the other client when available) judges the diff a
   root-cause fix, not a patch.

On the canonical branch after landing it requires a passing verification record
for the exact landed tree and re-checks the source signal.

Implements: concern-repair-verifier/closure-needs-all-five-gates-judged-by-the-verifier
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from concern_repair_contract import (  # noqa: E402
    BRANCH_PREFIX,
    CONCERN_LABEL,
    REPAIR_LABEL,
    REPO,
    GateResult,
    RepairBinding,
    RootCauseRepairReport,
    VerificationRecord,
    concern_slug,
    other_client,
)

PROJECT_ID = "aes"
LOOP_ID = "concern-root-cause-repair"
QUEUE_KEY = "concern-repair:queue"
FRICTION_PREFIX = "policy-friction-cluster:"
BACKOFF_MARKER = re.compile(r"<!-- concern-repair-backoff-until: (\S+) -->")
KEY_MARKER = re.compile(r"<!-- concern-key: (.+?) -->")
BACKOFF_HOURS = 24
DEFAULT_DAILY_CAP = 3
PROOF_TIMEOUT_SECONDS = 900
DIFF_CHAR_LIMIT = 60_000

Runner = Callable[[Sequence[str]], str]


# --------------------------------------------------------------------------- shared helpers


def _git(repository: Path, *args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=repository, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise ValueError(completed.stderr.strip() or f"git {' '.join(args)} failed")
    return completed.stdout.strip()


def _gh_env() -> dict[str, str]:
    env = dict(os.environ)
    if env.get("GITHUB_ACTIONS") != "true":
        env.pop("GITHUB_TOKEN", None)
    return env


def gh_runner(args: Sequence[str]) -> str:
    gh = shutil.which("gh")
    if gh is None:
        raise RuntimeError("gh CLI not found on PATH; cannot reach the concern register")
    completed = subprocess.run([gh, *args], capture_output=True, text=True, timeout=120, env=_gh_env())
    if completed.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {completed.stderr.strip()}")
    return completed.stdout


def state_root() -> Path:
    configured = os.environ.get("FEEDBACK_SYSTEM_STATE_ROOT")
    if not configured:
        raise ValueError("FEEDBACK_SYSTEM_STATE_ROOT is required")
    return Path(configured).expanduser().resolve()


def binding_path(root: Path, branch: str) -> Path:
    return root / "concern-repair" / "bindings" / f"{concern_slug(branch)}.json"


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def concern_key_from_body(body: str) -> str | None:
    match = KEY_MARKER.search(body or "")
    return match.group(1).strip() if match else None


def source_signal_supported(concern_key: str) -> bool:
    return concern_key.startswith(FRICTION_PREFIX)


def source_signal_green(repository: Path, concern_key: str) -> tuple[bool, str]:
    """The concern's own producer-side signal, read from the working tree at ``repository``."""
    if not concern_key.startswith(FRICTION_PREFIX):
        return False, f"no source-signal check is registered for concern kind of {concern_key!r}"
    cluster_id = concern_key[len(FRICTION_PREFIX):]
    path = repository / "policy" / "friction_clusters.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    clusters = [c for c in payload.get("clusters", []) if isinstance(c, dict) and c.get("id") == cluster_id]
    if len(clusters) != 1:
        return False, f"expected exactly one friction cluster {cluster_id!r}, found {len(clusters)}"
    cluster = clusters[0]
    if cluster.get("status") != "resolved":
        return False, f"cluster {cluster_id!r} status is {cluster.get('status')!r}, not 'resolved'"
    if not cluster.get("closure_verification"):
        return False, f"cluster {cluster_id!r} is resolved without closure_verification evidence"
    return True, f"cluster {cluster_id!r} resolved with {len(cluster['closure_verification'])} closure_verification item(s)"


# --------------------------------------------------------------------------- observe


def backoff_until(comments: Sequence[dict[str, Any]]) -> datetime | None:
    latest: datetime | None = None
    for comment in comments:
        for raw in BACKOFF_MARKER.findall(comment.get("body") or ""):
            value = datetime.fromisoformat(raw)
            if latest is None or value > latest:
                latest = value
    return latest


def repairs_started_since(root: Path, since: datetime) -> int:
    directory = root / "concern-repair" / "bindings"
    if not directory.is_dir():
        return 0
    count = 0
    for path in directory.glob("*.json"):
        binding = RepairBinding.model_validate_json(path.read_text(encoding="utf-8"))
        if binding.recorded_at >= since:
            count += 1
    return count


def select_concern(issues: Sequence[dict[str, Any]], now: datetime) -> dict[str, Any] | None:
    """Oldest open, repair-labeled, supported, not-in-backoff concern."""
    candidates = []
    for issue in issues:
        labels = {label.get("name") for label in issue.get("labels") or []}
        if CONCERN_LABEL not in labels or REPAIR_LABEL not in labels or issue.get("state", "OPEN").upper() != "OPEN":
            continue
        key = concern_key_from_body(issue.get("body") or "")
        if key is None or not source_signal_supported(key):
            continue
        until = backoff_until(issue.get("comments") or [])
        if until is not None and until > now:
            continue
        candidates.append({**issue, "concern_key": key})
    return min(candidates, key=lambda item: item["number"]) if candidates else None


def observe(repository: Path, output: Path, *, run: Runner = gh_runner, now: datetime | None = None) -> dict[str, Any]:
    repository = repository.resolve()
    output = output.resolve()
    now = now or datetime.now(UTC)
    revision = _git(repository, "rev-parse", "HEAD")
    if len(revision) != 40:
        raise ValueError("concern-repair observation requires an exact Git revision")
    daily_cap = int(os.environ.get("CONCERN_REPAIR_DAILY_CAP", str(DEFAULT_DAILY_CAP)))
    started_today = repairs_started_since(state_root(), now - timedelta(days=1))
    issues = json.loads(
        run(
            [
                "issue", "list", "-R", REPO, "--label", CONCERN_LABEL, "--label", REPAIR_LABEL,
                "--state", "open", "--json", "number,title,body,labels,state,comments", "--limit", "100",
            ]
        )
        or "[]"
    )
    selected = None if started_today >= daily_cap else select_concern(issues, now)
    native: dict[str, Any] = {
        "schema_version": "concern-repair-selection/v1",
        "observed_revision": revision,
        "observed_at": now.isoformat(),
        "daily_cap": daily_cap,
        "repairs_started_last_24h": started_today,
        "eligible_open_issues": len(issues),
    }
    if selected is None:
        native["selected"] = None
        native["reason"] = "daily repair cap reached" if started_today >= daily_cap else "no eligible concern"
        concern_key, result = QUEUE_KEY, "pass"
    else:
        native["selected"] = {
            "issue_number": selected["number"],
            "title": selected["title"],
            "body": selected["body"],
            "concern_key": selected["concern_key"],
        }
        concern_key, result = selected["concern_key"], "fail"
    native_bytes = (json.dumps(native, indent=2, sort_keys=True) + "\n").encode("utf-8")
    digest = hashlib.sha256(native_bytes).hexdigest()
    evidence_path = output.with_name(f"concern-repair-selection-{digest}.json")
    if not evidence_path.exists():
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = evidence_path.with_name(f".{evidence_path.name}.tmp")
        tmp.write_bytes(native_bytes)
        tmp.replace(evidence_path)
    identity = hashlib.sha256(f"{concern_key}\0{revision}\0{result}\0{now.date()}".encode()).hexdigest()[:20]
    observation = {
        "schema_version": "feedback-observation/v1",
        "observation_id": f"concern-repair:{identity}",
        "concern_key": concern_key,
        "loop_id": LOOP_ID,
        "project": PROJECT_ID,
        "observed_at": now.isoformat(),
        "result": result,
        "evidence_ref": {"store": "aes-concern-repair", "artifact": str(evidence_path), "sha256": digest},
        "repository_path": str(repository),
        "repository_identity": REPO,
        "base_branch": "main",
        "observed_revision": revision,
        # The repair starts from this exact committed revision in its own worktree,
        # so unrelated uncommitted edits in the canonical checkout do not enter it.
        "revision_state": "clean",
        "promotable": True,
        "verifier_command": ["python3", "scripts/concern_repair_feedback.py", "verify"],
        "repair_prompt": "Repair the root cause of the selected feedback concern.",
        "allowed_write_paths": ["scripts"],
    }
    _atomic_write(output, json.dumps(observation, indent=2) + "\n")
    return observation


# --------------------------------------------------------------------------- verify


def _gate(gate: str, passed: bool, detail: str) -> GateResult:
    return GateResult(gate=gate, passed=passed, detail=detail[:4000])  # type: ignore[arg-type]


def _run_proof(worktree: Path, command: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        command, cwd=worktree, capture_output=True, text=True, timeout=PROOF_TIMEOUT_SECONDS, check=False
    )
    tail = (completed.stdout[-1500:] + "\n--- stderr ---\n" + completed.stderr[-1500:]).strip()
    return completed.returncode, tail


def recurrence_proof(repository: Path, observed: str, fix: str, report: RootCauseRepairReport) -> GateResult:
    """Run the proof on the observed revision (plus only its harness files) and on the fix.

    Only ``recurrence_proof.harness_paths`` -- files the command needs that exist only in the fix,
    such as a new regression test -- are copied onto the observed revision. The prevention
    mechanism's own paths are never copied: when the control *is* the fix (for example a check
    newly wired into a hook), copying it would make the observed revision identical to the fix
    and no proof could ever fail there.

    Implements: concern-repair-verifier/a-recurrence-proof-that-cannot-fail-does-not-count
    """
    command = report.recurrence_proof.command
    scratch = Path(tempfile.mkdtemp(prefix="concern-repair-proof-"))
    before, after = scratch / "observed", scratch / "fix"
    try:
        _git(repository, "worktree", "add", "--detach", str(before), observed)
        _git(repository, "worktree", "add", "--detach", str(after), fix)
        harness_paths = report.recurrence_proof.harness_paths
        if harness_paths:
            _git(before, "checkout", fix, "--", *harness_paths)
        before_code, before_tail = _run_proof(before, command)
        after_code, after_tail = _run_proof(after, command)
    except (ValueError, subprocess.TimeoutExpired) as exc:
        return _gate("recurrence_proof_executed", False, f"could not execute recurrence proof: {exc}")
    finally:
        for path in (before, after):
            if path.exists():
                subprocess.run(["git", "worktree", "remove", "--force", str(path)], cwd=repository, capture_output=True, check=False)
        shutil.rmtree(scratch, ignore_errors=True)
    passed = before_code != 0 and after_code == 0
    detail = (
        f"command={command!r}; harness_paths={list(report.recurrence_proof.harness_paths)!r}; "
        f"on observed {observed[:12]} with harness exit={before_code}; "
        f"on fix {fix[:12]} exit={after_code}. "
        f"observed output tail:\n{before_tail}\nfix output tail:\n{after_tail}"
    )
    if before_code == 0:
        detail = "control does not fail on the observed revision, so it would not catch recurrence. " + detail
    elif after_code != 0:
        detail = "control does not pass on the fix. " + detail
    return _gate("recurrence_proof_executed", passed, detail)


def _render_review(**context: Any) -> list[dict[str, str]]:
    from llm_client import render_prompt

    return render_prompt(ROOT / "prompts" / "concern_repair" / "review.yaml", **context)


def post_backoff_comment(issue_number: int, reason: str, run: Runner, now: datetime | None = None) -> None:
    until = (now or datetime.now(UTC)) + timedelta(hours=BACKOFF_HOURS)
    body = (
        "Autonomous root-cause repair did not pass verification; retrying after the backoff.\n\n"
        f"{reason[:3000]}\n\n<!-- concern-repair-backoff-until: {until.isoformat()} -->"
    )
    run(["issue", "comment", str(issue_number), "-R", REPO, "--body", body])


def verify_repair(
    workspace: Path,
    root: Path,
    *,
    review_trace_id: str,
    review: Callable[..., Any] | None = None,
    run: Runner = gh_runner,
) -> tuple[bool, VerificationRecord]:
    branch = _git(workspace, "branch", "--show-current")
    path = binding_path(root, branch)
    if not path.is_file():
        raise ValueError(f"no executor-written repair binding for branch {branch!r} at {path}")
    binding = RepairBinding.model_validate_json(path.read_text(encoding="utf-8"))
    fix = _git(workspace, "rev-parse", "HEAD")
    tree = _git(workspace, "rev-parse", "HEAD^{tree}")
    gates: list[GateResult] = []

    report: RootCauseRepairReport | None = None
    report_file = workspace / binding.report_path
    if not report_file.is_file():
        gates.append(_gate("report_contract", False, f"report missing at {binding.report_path}"))
    else:
        try:
            report = RootCauseRepairReport.model_validate_json(report_file.read_text(encoding="utf-8"))
        except ValidationError as exc:
            gates.append(_gate("report_contract", False, f"report does not validate: {exc}"))
        else:
            if report.concern_key != binding.concern_key or report.issue_number != binding.issue_number:
                gates.append(_gate("report_contract", False, "report concern_key/issue_number do not match the executor binding"))
                report = None
            else:
                gates.append(_gate("report_contract", True, "report validates and matches the executor binding"))

    changed = set(_git(workspace, "diff", "--name-only", f"{binding.observed_revision}..{fix}").splitlines())
    if report is None:
        gates.append(_gate("prevention_in_diff", False, "no valid report"))
        gates.append(_gate("recurrence_proof_executed", False, "no valid report"))
    else:
        missing = [p for p in report.prevention_mechanism.paths if not any(c == p or c.startswith(f"{p}/") for c in changed)]
        gates.append(
            _gate("prevention_in_diff", not missing, f"unchanged prevention paths: {missing}" if missing else "every prevention path is changed in the diff")
        )
        gates.append(recurrence_proof(workspace, binding.observed_revision, fix, report))

    signal_ok, signal_detail = source_signal_green(workspace, binding.concern_key)
    gates.append(_gate("source_signal_green", signal_ok, signal_detail))

    reviewer_client = other_client(binding.repair_client)
    if all(g.passed for g in gates) and report is not None:
        if review is None:
            from concern_repair_agents import review_root_cause as review
        diff = _git(workspace, "diff", f"{binding.observed_revision}..{fix}")
        messages = _render_review(
            repo=REPO,
            issue_number=binding.issue_number,
            issue_title=_issue_title(binding.issue_number, run),
            issue_body=_issue_body(binding.issue_number, run),
            report_json=report.model_dump_json(indent=2),
            gates_json=json.dumps([g.model_dump() for g in gates], indent=2),
            observed_revision=binding.observed_revision,
            repair_revision=fix,
            diff=diff[:DIFF_CHAR_LIMIT] + ("\n[diff truncated]" if len(diff) > DIFF_CHAR_LIMIT else ""),
        )
        order = list(dict.fromkeys([reviewer_client, "claude-code"]))
        with tempfile.TemporaryDirectory(prefix="concern-repair-review-") as blank:
            reviewer_client, verdict, unavailable = review(
                messages,
                order=order,
                workspace=Path(blank),
                task="aes.concern_repair.review",
                trace_id=review_trace_id,
                timeout_seconds=900,
            )
        ok = verdict.verdict == "root_cause_fixed" and verdict.prevention_would_catch_recurrence
        detail = json.dumps({"reviewer": reviewer_client, "unavailable": unavailable, **verdict.model_dump()})
        gates.append(_gate("independent_root_cause_review", ok, detail))
    else:
        gates.append(_gate("independent_root_cause_review", False, "not run: a mechanical gate failed"))

    passed = all(g.passed for g in gates)
    record = VerificationRecord(
        concern_key=binding.concern_key,
        issue_number=binding.issue_number,
        repair_tree=tree,
        repair_client=binding.repair_client,
        reviewer_client=reviewer_client,
        gates=gates,
        passed=passed,
        recorded_at=datetime.now(UTC),
    )
    _atomic_write(root / "concern-repair" / "verifications" / f"{tree}.json", record.model_dump_json(indent=2))
    if not passed:
        failed = "\n".join(f"- {g.gate}: {g.detail[:500]}" for g in gates if not g.passed)
        post_backoff_comment(binding.issue_number, f"Failed gates (repair by {binding.repair_client}):\n{failed}", run)
    return passed, record


def verify_canonical(workspace: Path, root: Path) -> tuple[bool, str]:
    tree = _git(workspace, "rev-parse", "HEAD^{tree}")
    path = root / "concern-repair" / "verifications" / f"{tree}.json"
    if not path.is_file():
        return False, f"no verification record for landed tree {tree}"
    record = VerificationRecord.model_validate_json(path.read_text(encoding="utf-8"))
    if not record.passed:
        return False, f"verification record for tree {tree} did not pass"
    ok, detail = source_signal_green(workspace, record.concern_key)
    return ok, f"landed tree {tree} has a passing root-cause verification; source signal: {detail}"


def _issue_view(number: int, run: Runner) -> dict[str, Any]:
    return json.loads(run(["issue", "view", str(number), "-R", REPO, "--json", "title,body"]) or "{}")


def _issue_title(number: int, run: Runner) -> str:
    return str(_issue_view(number, run).get("title", ""))


def _issue_body(number: int, run: Runner) -> str:
    return str(_issue_view(number, run).get("body", ""))


def verify(workspace: Path) -> tuple[bool, str]:
    root = state_root()
    branch = _git(workspace, "branch", "--show-current")
    if branch.startswith(BRANCH_PREFIX):
        from llm_client import ObservedRun

        tree = _git(workspace, "rev-parse", "HEAD^{tree}")
        run_id = f"concern-repair-verify-{concern_slug(branch)}-{tree[:12]}-{datetime.now(UTC):%Y%m%dT%H%M%S}"
        with ObservedRun(
            project="aes",
            operation="concern_root_cause_verify",
            executable="scripts/concern_repair_feedback.py",
            run_id=run_id,
            root_trace_id=f"aes.concern-repair-verify.{run_id}",
        ) as observed_run:
            observed_run.set_phase("closure_gates")
            passed, record = verify_repair(workspace, root, review_trace_id=observed_run.child_trace_id("review"))
        summary = "; ".join(f"{g.gate}={'pass' if g.passed else 'FAIL'}" for g in record.gates)
        return passed, summary
    return verify_canonical(workspace, root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("observe", "verify"))
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.mode == "verify":
            healthy, reason = verify(args.repository.resolve())
            print(reason)
            return 0 if healthy else 1
        configured = args.output or (Path(os.environ["FEEDBACK_OBSERVATION_PATH"]) if "FEEDBACK_OBSERVATION_PATH" in os.environ else None)
        if configured is None:
            raise ValueError("FEEDBACK_OBSERVATION_PATH or --output is required")
        print(json.dumps(observe(args.repository, configured)))
        return 0
    except (OSError, RuntimeError, ValueError, ValidationError) as exc:
        print(f"concern-repair: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
