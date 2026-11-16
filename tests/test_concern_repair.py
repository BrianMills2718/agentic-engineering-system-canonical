"""Focused tests for root-cause concern repair (ADR-2026-09-14 slice 3)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

needs_llm_client = pytest.mark.skipif(
    importlib.util.find_spec("llm_client") is None,
    reason="llm_client (Brian's shared library) is not installed in this environment",
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import concern_repair_agents as agents  # noqa: E402
import concern_repair_feedback as feedback  # noqa: E402
from concern_repair_contract import (  # noqa: E402
    RepairBinding,
    RootCauseRepairReport,
    RootCauseReview,
    VerificationRecord,
    report_path_for,
)

KEY = "policy-friction-cluster:documentation-health"
NOW = datetime(2026, 9, 14, 12, 0, tzinfo=UTC)


# --------------------------------------------------------------------------- fixtures


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def _report(**overrides) -> dict:
    payload = {
        "schema_version": "concern-root-cause-repair/v2",
        "concern_key": KEY,
        "issue_number": 1883,
        "symptom": "The guard accepted malformed intent records without failing.",
        "root_cause": "The loader returned an empty mapping on a parse error instead of raising, so callers saw no records.",
        "why_existing_controls_missed_it": "No test exercised the parse-error branch of the loader.",
        "failure_class": "Silent fallback on parse failure",
        "class_sweep": {
            "search_method": "grep for 'except yaml' across scripts/",
            "instances_found": ["scripts/guard.py"],
            "instances_fixed": ["scripts/guard.py"],
        },
        "prevention_mechanism": {
            "kind": "check_script",
            "paths": ["checks/check_guard.py"],
            "description": "Fails when the loader swallows a parse error.",
        },
        "recurrence_proof": {
            "command": [sys.executable, "checks/check_guard.py"],
            "harness_paths": ["checks/check_guard.py"],
            "fails_on_observed_revision": True,
            "passes_on_fix": True,
            "explanation": "The check imports the loader and requires a raise on malformed input.",
        },
        "source_signal_resolution": "Cluster documentation-health marked resolved with closure_verification.",
        "residual_risk": "none known",
    }
    payload.update(overrides)
    return payload


def _clusters(status: str, verification: list | None = None) -> str:
    return yaml.safe_dump(
        {"clusters": [{"id": "documentation-health", "status": status, "closure_verification": verification or []}]}
    )


class FakeGh:
    def __init__(self, issues: list | None = None):
        self.issues = issues or []
        self.calls: list[list[str]] = []

    def __call__(self, args):
        args = list(args)
        self.calls.append(args)
        if args[:2] == ["issue", "list"]:
            return json.dumps(self.issues)
        if args[:2] == ["issue", "view"]:
            return json.dumps({"title": "Recurring policy friction: documentation-health", "body": "body"})
        if args[:2] == ["issue", "comment"]:
            return ""
        raise AssertionError(f"unexpected gh call {args}")


def _repair_repo(tmp_path: Path, *, fixed: bool, control_catches: bool, resolved: bool, report: dict | None = None):
    """Observed commit has a buggy loader; the repair branch commits the fix, control, report, and cluster."""
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "policy").mkdir()
    (repo / "checks").mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    (repo / "scripts" / "guard.py").write_text("def load(text):\n    return {}\n")
    (repo / "policy" / "friction_clusters.yaml").write_text(_clusters("open"))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "observed")
    observed = _git(repo, "rev-parse", "HEAD")
    branch = "feedback-repair/abc-c1-i1"
    _git(repo, "checkout", "-qb", branch)
    if fixed:
        (repo / "scripts" / "guard.py").write_text("def load(text):\n    raise ValueError('malformed')\n")
    check = (
        "import sys\nsys.path.insert(0, 'scripts')\nimport guard\n"
        "try:\n    guard.load('::')\nexcept ValueError:\n    sys.exit(0)\nsys.exit(1)\n"
        if control_catches
        else "import sys\nsys.exit(0)\n"
    )
    (repo / "checks" / "check_guard.py").write_text(check)
    verification = [{"claim": "loader raises on malformed input", "evidence_refs": ["checks/check_guard.py"]}]
    (repo / "policy" / "friction_clusters.yaml").write_text(
        _clusters("resolved", verification) if resolved else _clusters("open")
    )
    report_file = repo / report_path_for(KEY)
    report_file.parent.mkdir(parents=True)
    report_file.write_text(json.dumps(report or _report()))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "repair")
    state = tmp_path / "state"
    binding = RepairBinding(
        run_id="abc-c1-i1",
        branch=branch,
        issue_number=1883,
        concern_key=KEY,
        observed_revision=observed,
        repair_client="claude-code",
        report_path=report_path_for(KEY),
        trace_id="project-meta/concern-repair/abc-c1-i1",
        recorded_at=NOW,
    )
    path = feedback.binding_path(state, branch)
    path.parent.mkdir(parents=True)
    path.write_text(binding.model_dump_json())
    return repo, state


def _reviewer(verdict: str = "root_cause_fixed", catches: bool = True):
    calls = []

    def review(messages, *, order, workspace, task, trace_id, timeout_seconds):
        calls.append({"order": order, "messages": messages})
        return order[0], RootCauseReview(
            verdict=verdict,
            root_cause_addressed=verdict == "root_cause_fixed",
            failure_class_addressed=verdict == "root_cause_fixed",
            prevention_would_catch_recurrence=catches,
            reasons=["diff-grounded reason"],
        ), []

    review.calls = calls
    return review


# --------------------------------------------------------------------------- contract


def test_report_contract_accepts_complete_report():
    assert RootCauseRepairReport.model_validate(_report()).issue_number == 1883


@pytest.mark.parametrize(
    "override",
    [
        {"recurrence_proof": {**_report()["recurrence_proof"], "fails_on_observed_revision": False}},
        {"prevention_mechanism": {**_report()["prevention_mechanism"], "paths": ["/etc/passwd"]}},
        {"prevention_mechanism": {**_report()["prevention_mechanism"], "paths": []}},
        {"root_cause": "too short"},
        {"unexpected": "field"},
    ],
)
def test_report_contract_rejects_incomplete_or_unsafe_reports(override):
    with pytest.raises(ValidationError):
        RootCauseRepairReport.model_validate(_report(**override))


# --------------------------------------------------------------------------- observer


def _issue(number: int, key: str | None = KEY, labels=("concern:feedback", "agent:repair"), comments=()):
    body = "text" + (f"\n<!-- concern-key: {key} -->" if key else "")
    return {
        "number": number,
        "title": f"issue {number}",
        "body": body,
        "state": "OPEN",
        "labels": [{"name": name} for name in labels],
        "comments": list(comments),
    }


def test_select_concern_picks_oldest_supported_and_skips_unlabeled_or_unsupported():
    issues = [
        _issue(1900),
        _issue(1850, key="project-meta-daily-audit"),
        _issue(1840, labels=("concern:feedback",)),
        _issue(1883),
    ]
    assert feedback.select_concern(issues, NOW)["number"] == 1883


def test_select_concern_honors_active_backoff_and_resumes_after_expiry():
    active = {"body": f"<!-- concern-repair-backoff-until: {(NOW + timedelta(hours=3)).isoformat()} -->"}
    expired = {"body": f"<!-- concern-repair-backoff-until: {(NOW - timedelta(hours=1)).isoformat()} -->"}
    assert feedback.select_concern([_issue(1883, comments=[active])], NOW) is None
    assert feedback.select_concern([_issue(1883, comments=[expired])], NOW)["number"] == 1883


def _observe_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "canonical"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    (repo / "f").write_text("x")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "c")
    return repo


def test_observe_emits_failing_observation_for_selected_concern(tmp_path, monkeypatch):
    monkeypatch.setenv("FEEDBACK_SYSTEM_STATE_ROOT", str(tmp_path / "state"))
    repo = _observe_repo(tmp_path)
    out = tmp_path / "state" / "obs" / "observation.json"
    observation = feedback.observe(repo, out, run=FakeGh([_issue(1883)]), now=NOW)
    assert observation["result"] == "fail"
    assert observation["concern_key"] == KEY
    evidence = json.loads(Path(observation["evidence_ref"]["artifact"]).read_text())
    assert evidence["selected"]["issue_number"] == 1883
    assert json.loads(out.read_text())["observed_revision"] == _git(repo, "rev-parse", "HEAD")


def test_observe_daily_cap_emits_passing_queue_observation(tmp_path, monkeypatch):
    state = tmp_path / "state"
    monkeypatch.setenv("FEEDBACK_SYSTEM_STATE_ROOT", str(state))
    monkeypatch.setenv("CONCERN_REPAIR_DAILY_CAP", "1")
    binding = RepairBinding(
        run_id="r", branch="feedback-repair/r", issue_number=1, concern_key=KEY,
        observed_revision="a" * 40, repair_client="claude-code", report_path="x", trace_id="t",
        recorded_at=NOW - timedelta(hours=2),
    )
    path = feedback.binding_path(state, "feedback-repair/r")
    path.parent.mkdir(parents=True)
    path.write_text(binding.model_dump_json())
    observation = feedback.observe(_observe_repo(tmp_path), state / "o.json", run=FakeGh([_issue(1883)]), now=NOW)
    assert observation["result"] == "pass"
    assert observation["concern_key"] == feedback.QUEUE_KEY


# --------------------------------------------------------------------------- client selection and failover


def test_client_order_parses_and_rejects_unknown():
    assert agents.client_order("codex, claude-code,codex") == ["codex", "claude-code"]
    with pytest.raises(ValueError):
        agents.client_order("gemini")


@needs_llm_client
def test_failover_skips_unavailable_client_and_records_it(tmp_path):
    from llm_client.core.errors import LLMQuotaExhaustedError

    seen = []

    def call(model, messages, **kwargs):
        seen.append((model, messages[0]["content"], kwargs))
        if model.startswith("codex/"):
            raise LLMQuotaExhaustedError("usage exhausted")
        return "ok"

    run = agents.run_with_failover(
        lambda client: [{"role": "user", "content": f"claim as {client}"}],
        order=["codex", "claude-code"], workspace=tmp_path, task="t", trace_id="root/x", timeout_seconds=5, call=call,
    )
    assert run.client == "claude-code"
    assert run.unavailable and run.unavailable[0].startswith("codex:")
    assert seen[1][1] == "claim as claude-code"
    assert seen[1][2]["setting_sources"] == ["user", "project", "local"]


@needs_llm_client
def test_failover_raises_real_failures_instead_of_switching(tmp_path):
    def call(model, messages, **kwargs):
        raise RuntimeError("agent crashed mid-repair")

    with pytest.raises(RuntimeError):
        agents.run_with_failover(
            lambda c: [], order=["claude-code", "codex"], workspace=tmp_path, task="t", trace_id="r", timeout_seconds=5, call=call
        )


@needs_llm_client
def test_failover_with_no_available_client_fails_loud(tmp_path):
    from llm_client.core.errors import LLMAuthError

    def call(model, messages, **kwargs):
        raise LLMAuthError("not logged in")

    with pytest.raises(agents.NoAvailableClientError):
        agents.run_with_failover(
            lambda c: [], order=["claude-code", "codex"], workspace=tmp_path, task="t", trace_id="r", timeout_seconds=5, call=call
        )


def test_harness_kwargs_full_for_repairer_and_isolated_for_reviewer(tmp_path):
    claude = agents.harness_kwargs("claude-code", tmp_path, timeout_seconds=10)
    codex = agents.harness_kwargs("codex", tmp_path, timeout_seconds=10)
    assert claude["setting_sources"] == ["user", "project", "local"]
    assert codex["codex_home"] == str(Path.home())
    assert agents.harness_kwargs("claude-code", tmp_path, timeout_seconds=10, reviewer=True)["setting_sources"] == []
    reviewer_codex = agents.harness_kwargs("codex", tmp_path, timeout_seconds=10, reviewer=True)
    assert "codex_home" not in reviewer_codex and reviewer_codex["sandbox_mode"] == "read-only"


# --------------------------------------------------------------------------- verifier gates


@pytest.mark.req("concern-repair-verifier/five-gates-pass-root-cause-fix")
@needs_llm_client
def test_verifier_passes_a_root_cause_fix_and_uses_the_other_client_as_reviewer(tmp_path):
    repo, state = _repair_repo(tmp_path, fixed=True, control_catches=True, resolved=True)
    review = _reviewer()
    gh = FakeGh()
    passed, record = feedback.verify_repair(repo, state, review_trace_id="root/review", review=review, run=gh)
    assert passed, [g.model_dump() for g in record.gates]
    assert review.calls[0]["order"][0] == "codex"
    assert not any(call[:2] == ["issue", "comment"] for call in gh.calls)
    canonical_ok, detail = feedback.verify_canonical(repo, state)
    assert canonical_ok, detail


@pytest.mark.req("concern-repair-verifier/patch-is-rejected")
def test_verifier_rejects_patch_whose_control_does_not_fail_on_observed_revision(tmp_path):
    repo, state = _repair_repo(tmp_path, fixed=True, control_catches=False, resolved=True)
    review = _reviewer()
    gh = FakeGh()
    passed, record = feedback.verify_repair(repo, state, review_trace_id="root/review", review=review, run=gh)
    gates = {g.gate: g for g in record.gates}
    assert not passed
    assert not gates["recurrence_proof_executed"].passed
    assert not gates["independent_root_cause_review"].passed and not review.calls
    comments = [call for call in gh.calls if call[:2] == ["issue", "comment"]]
    assert comments and "concern-repair-backoff-until" in comments[0][-1]


@pytest.mark.req("concern-repair-verifier/patch-is-rejected")
def test_verifier_rejects_fix_that_does_not_pass_its_own_control(tmp_path):
    repo, state = _repair_repo(tmp_path, fixed=False, control_catches=True, resolved=True)
    passed, record = feedback.verify_repair(repo, state, review_trace_id="r", review=_reviewer(), run=FakeGh())
    assert not passed
    assert not {g.gate: g for g in record.gates}["recurrence_proof_executed"].passed


_INLINE_GUARD_PROOF = [
    sys.executable,
    "-c",
    "import sys; sys.path.insert(0, 'scripts'); import guard\n"
    "try:\n    guard.load('::')\nexcept ValueError:\n    sys.exit(0)\nsys.exit(1)",
]


@pytest.mark.req("concern-repair-verifier/proof-fails-closed")
@needs_llm_client
def test_recurrence_proof_can_fail_when_the_control_is_the_fix_itself(tmp_path):
    """Live #1883 run: the verifier copied the prevention paths (the fix itself) onto the observed
    revision, so a control that *is* the fix could never fail there. Only harness files are copied now."""
    report = _report(
        prevention_mechanism={**_report()["prevention_mechanism"], "kind": "validator", "paths": ["scripts/guard.py"]},
        recurrence_proof={**_report()["recurrence_proof"], "command": _INLINE_GUARD_PROOF, "harness_paths": []},
    )
    repo, state = _repair_repo(tmp_path, fixed=True, control_catches=True, resolved=True, report=report)
    passed, record = feedback.verify_repair(repo, state, review_trace_id="r", review=_reviewer(), run=FakeGh())
    gates = {g.gate: g for g in record.gates}
    assert gates["recurrence_proof_executed"].passed, gates["recurrence_proof_executed"].detail
    assert passed, [g.model_dump() for g in record.gates]


@pytest.mark.req("concern-repair-verifier/proof-fails-closed")
def test_recurrence_proof_rejects_harness_that_copies_the_fix_onto_observed(tmp_path):
    """Declaring the fix file as harness makes the observed revision equal the fix, so the proof
    cannot distinguish them and must be rejected."""
    report = _report(
        recurrence_proof={**_report()["recurrence_proof"], "command": _INLINE_GUARD_PROOF, "harness_paths": ["scripts/guard.py"]},
    )
    repo, state = _repair_repo(tmp_path, fixed=True, control_catches=True, resolved=True, report=report)
    passed, record = feedback.verify_repair(repo, state, review_trace_id="r", review=_reviewer(), run=FakeGh())
    assert not passed
    assert not {g.gate: g for g in record.gates}["recurrence_proof_executed"].passed


@pytest.mark.req("concern-repair-verifier/patch-is-rejected")
@needs_llm_client
def test_verifier_rejects_when_reviewer_judges_patch_only(tmp_path):
    repo, state = _repair_repo(tmp_path, fixed=True, control_catches=True, resolved=True)
    passed, record = feedback.verify_repair(repo, state, review_trace_id="r", review=_reviewer("patch_only"), run=FakeGh())
    gates = {g.gate: g for g in record.gates}
    assert not passed
    assert all(gates[name].passed for name in ("report_contract", "prevention_in_diff", "recurrence_proof_executed", "source_signal_green"))
    assert not gates["independent_root_cause_review"].passed


@pytest.mark.req("concern-repair-verifier/patch-is-rejected")
def test_verifier_rejects_unresolved_source_signal(tmp_path):
    repo, state = _repair_repo(tmp_path, fixed=True, control_catches=True, resolved=False)
    passed, record = feedback.verify_repair(repo, state, review_trace_id="r", review=_reviewer(), run=FakeGh())
    assert not passed and not {g.gate: g for g in record.gates}["source_signal_green"].passed


@pytest.mark.req("concern-repair-verifier/patch-is-rejected")
def test_verifier_rejects_prevention_path_not_in_diff(tmp_path):
    report = _report(prevention_mechanism={**_report()["prevention_mechanism"], "paths": ["scripts/untouched.py"]})
    repo, state = _repair_repo(tmp_path, fixed=True, control_catches=True, resolved=True, report=report)
    passed, record = feedback.verify_repair(repo, state, review_trace_id="r", review=_reviewer(), run=FakeGh())
    assert not passed and not {g.gate: g for g in record.gates}["prevention_in_diff"].passed


def test_verifier_rejects_missing_report_and_canonical_without_record(tmp_path):
    repo, state = _repair_repo(tmp_path, fixed=True, control_catches=True, resolved=True)
    _git(repo, "rm", "-q", report_path_for(KEY))
    _git(repo, "commit", "-qm", "drop report")
    passed, record = feedback.verify_repair(repo, state, review_trace_id="r", review=_reviewer(), run=FakeGh())
    assert not passed and not {g.gate: g for g in record.gates}["report_contract"].passed
    ok, _ = feedback.verify_canonical(repo, tmp_path / "empty-state")
    assert not ok


def test_verifier_requires_executor_binding(tmp_path):
    repo, state = _repair_repo(tmp_path, fixed=True, control_catches=True, resolved=True)
    with pytest.raises(ValueError, match="no executor-written repair binding"):
        feedback.verify_repair(repo, tmp_path / "other-state", review_trace_id="r", review=_reviewer(), run=FakeGh())


@needs_llm_client
def test_prompts_render_with_every_required_variable():
    from llm_client import render_prompt

    repair = render_prompt(
        ROOT / "prompts" / "concern_repair" / "repair.yaml",
        repo="o/r", issue_number=1, issue_title="t", issue_body="b", concern_key=KEY, observed_revision="a" * 40,
        repository="/r", worktree="/r/worktrees/x", branch="feedback-repair/x", client="codex",
        write_paths=["scripts", "tests"], report_path=report_path_for(KEY), report_schema="{}",
    )
    assert "WORKTREE_AGENT=codex" in repair[-1]["content"]
    review = render_prompt(
        ROOT / "prompts" / "concern_repair" / "review.yaml",
        repo="o/r", issue_number=1, issue_title="t", issue_body="b", report_json="{}", gates_json="[]",
        observed_revision="a" * 40, repair_revision="b" * 40, diff="d",
    )
    assert review[0]["role"] == "system"


def test_verification_record_round_trips():
    record = VerificationRecord(
        concern_key=KEY, issue_number=1, repair_tree="c" * 40, repair_client="codex", reviewer_client="claude-code",
        gates=[], passed=False, recorded_at=NOW,
    )
    assert VerificationRecord.model_validate_json(record.model_dump_json()) == record


@needs_llm_client
def test_agent_kwargs_satisfy_llm_client_call_contract(tmp_path, monkeypatch):
    """Live probe 2026-09-14: llm_client rejects agent models without model_justification,
    ignores per-call timeouts under its default policy, and cancels any attempt at its 300s
    safety ceiling -- which would kill every real repair after five minutes."""
    for client in ("claude-code", "codex"):
        for reviewer in (False, True):
            kwargs = agents.harness_kwargs(client, tmp_path, timeout_seconds=2400, reviewer=reviewer)
            assert kwargs["model_justification"]
            assert "timeout" not in kwargs
    monkeypatch.delenv("LLM_CLIENT_SAFETY_TIMEOUT", raising=False)
    agents.run_with_failover(
        lambda c: [], order=["claude-code"], workspace=tmp_path, task="t", trace_id="r", timeout_seconds=2400,
        call=lambda *a, **k: "ok",
    )
    import os

    assert os.environ["LLM_CLIENT_SAFETY_TIMEOUT"] == "2400"
