"""Counterexamples cross the actual CP provider, not a fabricated passing receipt."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from agentic_engineering_system.evidence import assess
from agentic_engineering_system.trace_review import check_source_review
from test_trace_review import REVIEW, WHYGAME5_AES, _observation, _target_with_trace_review_er
from agentic_engineering_system.records import load_project

PROBE_EVENTS = []


def checked(root, observation, criterion_id):
    result = check_source_review(root, observation, criterion_id)
    native = dict(vars(observation))
    tr = native.get("trace_review")
    native["trace_review"] = vars(tr) if hasattr(tr, "__dict__") else "legacy undeclared record"
    PROBE_EVENTS.append({"input": {"criterion": criterion_id, "native_binding": native},
                         "output": vars(result)})
    return result


@pytest.fixture(scope="session", autouse=True)
def retain_probe_trace(request):
    yield
    destination = os.environ.get("AES_TRACE_REVIEW_PROBE_LOG")
    if destination:
        Path(destination).write_text(json.dumps({"run_id": "aes-source-bound-native-probes",
            "events": PROBE_EVENTS, "outcome": "fail" if request.session.testsfailed else "pass"}, indent=2) + "\n")


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


@pytest.fixture
def provider(monkeypatch):
    command = os.environ.get("AES_TRACE_REVIEW_TEST_PROVIDER")
    if not command:
        pytest.skip("real CP provider command not configured; integration is not verified")
    monkeypatch.setenv("AES_TRACE_REVIEW_COMMAND", command)
    original = subprocess.run
    provider_argv = json.loads(command)
    def traced_run(argv, **kwargs):
        if argv[:len(provider_argv)] != provider_argv:
            return original(argv, **kwargs)
        root = Path(kwargs["cwd"])
        review = json.loads((root / argv[len(provider_argv)]).read_text())
        source = json.loads((root / review["source"]["path"]).read_text())
        result = original(argv, **kwargs)
        PROBE_EVENTS.append({"input": {"command": argv, "review": review, "source": source},
                             "output": {"stdout": result.stdout, "stderr": result.stderr,
                                        "exit_status": result.returncode}})
        return result
    monkeypatch.setattr(subprocess, "run", traced_run)


def packet(root):
    source = {"run_id": "native-probe", "events": [{"input": {"arguments": "required"},
              "output": {"result": "retained"}}], "outcome": "pass"}
    raw = json.dumps(source).encode(); (root / "trace.json").write_bytes(raw)
    review = {"schema_version": "1.0", "record_type": "trace_review", "review_id": "review-native",
              "reviewer": "session-b", "goal_ref": "goal:test", "criterion_ids": ["SC-NATIVE"],
              "evidence_revision": "a" * 40, "run_id": "native-probe", "run_outcome": "pass",
              "source": {"path": "trace.json", "sha256": hashlib.sha256(raw).hexdigest(),
                         "format": "execution_trace"},
              "reviewed_entries": [{"pointer": p, "sha256": _digest(v),
                                    "observation": "Examined retained input and output"}
                                   for p, v in [("/events/0", source["events"][0]),
                                                ("/outcome", source["outcome"])]], "findings": []}
    (root / "review.json").write_text(json.dumps(review))
    tr = SimpleNamespace(reviewer="session-b", trace_refs=["trace.json"], steps_read=2, steps_total=2)
    obs = SimpleNamespace(trace_review=tr, result={"trace_reviews": ["review.json"], "run_id": "native-probe"},
                          retained_artifact_refs=["review.json", "trace.json"], subject_revision="a" * 40)
    return source, review, obs


def test_legacy_claim_without_retained_review_is_unavailable(tmp_path):
    obs = SimpleNamespace(trace_review=object(), result={"read": True})
    assert checked(tmp_path, obs, "SC-NATIVE").status == "unavailable"


def test_missing_provider_cannot_support(tmp_path, monkeypatch):
    _, _, obs = packet(tmp_path)
    monkeypatch.setenv("AES_TRACE_REVIEW_COMMAND", "[]")
    assert checked(tmp_path, obs, "SC-NATIVE").status == "unavailable"


def test_real_provider_accepts_complete_passing_review(tmp_path, provider):
    _, _, obs = packet(tmp_path)
    result = checked(tmp_path, obs, "SC-NATIVE")
    assert (result.status, result.run_outcome) == ("complete", "pass"), result.reason


@pytest.mark.parametrize("mutation", ["source", "partial", "citation", "criterion", "revision",
                                      "reviewer", "run", "retention", "steps", "extra_source", "duplicate"])
def test_real_provider_rejects_counterexamples(tmp_path, provider, mutation):
    source, review, obs = packet(tmp_path)
    if mutation == "source":
        source["events"][0]["output"] = {"result": "changed"}
        (tmp_path / "trace.json").write_text(json.dumps(source))
    elif mutation == "partial":
        review["reviewed_entries"].pop()
    elif mutation == "citation":
        review["findings"] = [{"classification": "unresolved", "description": "Unsupported claimed diagnosis", "citations":
                               [{"pointer": "/outcome", "quote": "fabricated"}]}]
    elif mutation == "criterion": review["criterion_ids"] = ["SC-OTHER"]
    elif mutation == "revision": obs.subject_revision = "b" * 40
    elif mutation == "reviewer": obs.trace_review.reviewer = "session-other"
    elif mutation == "run": obs.result["run_id"] = "other-run"
    elif mutation == "retention": obs.retained_artifact_refs = ["review.json"]
    elif mutation == "steps": obs.trace_review.steps_total = 1
    elif mutation == "extra_source": obs.trace_review.trace_refs.append("unreviewed-trace.json")
    elif mutation == "duplicate": obs.result["trace_reviews"].append("review.json")
    (tmp_path / "review.json").write_text(json.dumps(review))
    result = checked(tmp_path, obs, "SC-NATIVE")
    PROBE_EVENTS.append({"input": {"case": mutation, "review": review,
                                  "native_binding": vars(obs) | {"trace_review": vars(obs.trace_review)}},
                         "output": vars(result)})
    assert result.status != "complete", result
    if mutation == "citation": assert "unsupported finding citation" in result.reason


@pytest.mark.parametrize("payload", ["[]", "null", "broken"])
def test_invalid_provider_response_is_visible_unavailable(tmp_path, monkeypatch, payload):
    _, _, obs = packet(tmp_path)
    monkeypatch.setenv("AES_TRACE_REVIEW_COMMAND", '["configured-provider"]')
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw:
                        SimpleNamespace(stdout=payload, stderr="", returncode=0))
    result = checked(tmp_path, obs, "SC-NATIVE")
    assert result.status == "unavailable", result


def test_source_changed_during_provider_call_is_not_accepted(tmp_path, provider, monkeypatch):
    _, _, obs = packet(tmp_path)
    original = subprocess.run
    def mutate_after_validation(*args, **kwargs):
        result = original(*args, **kwargs)
        (tmp_path / "trace.json").write_text('{"outcome":"changed"}')
        return result
    monkeypatch.setattr(subprocess, "run", mutate_after_validation)
    result = checked(tmp_path, obs, "SC-NATIVE")
    assert result.status == "unavailable" and "changed during" in result.reason


def test_authentic_reviewed_failure_stays_failed(provider):
    root = Path(__file__).resolve().parents[2]
    ref = "proposals/trace-review-enforcement/authentic.review.json"
    review = json.loads((root / ref).read_text())
    source = review["source"]["path"]
    count = len(review["reviewed_entries"])
    obs = SimpleNamespace(trace_review=SimpleNamespace(reviewer=review["reviewer"], trace_refs=[source],
                          steps_read=count, steps_total=count),
                          result={"trace_reviews": [ref], "run_id": review["run_id"]},
                          retained_artifact_refs=[ref, source], subject_revision=review["evidence_revision"])
    result = checked(root, obs, "privacy-diagnosis")
    assert (result.status, result.run_outcome) == ("complete", "fail"), result.reason


@pytest.mark.parametrize("case,expected", [("pass", "SUPPORTED"), ("missing", "NO_CURRENT_SUPPORT"),
                                         ("partial", "NO_CURRENT_SUPPORT"),
                                         ("failed", "NO_CURRENT_SUPPORT"), ("refuted", "REFUTED")])
def test_native_standing_requires_source_bound_passing_review(tmp_path, provider, case, expected):
    target, er_id = _target_with_trace_review_er(tmp_path)
    aes = tmp_path / ".aes"; aes.mkdir()
    (aes / "project.yaml").write_bytes((WHYGAME5_AES / "project.yaml").read_bytes())
    project = load_project(aes / "project.yaml")
    target_path = tmp_path / project.materialization.target_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes((tmp_path / "target.yaml").read_bytes())
    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, capture_output=True,
                              text=True, check=True).stdout.strip()
    git("init", "-q")
    git("add", ".")
    git("-c", "user.name=AES test", "-c", "user.email=aes-test@example.invalid",
        "commit", "-qm", "synthetic acceptance fixture")
    revision = git("rev-parse", "HEAD")
    source, review, _ = packet(tmp_path)
    review["criterion_ids"] = [target.success_criteria[0].id]
    review["evidence_revision"] = revision
    if case in ("failed", "refuted"):
        source["outcome"] = "fail"
        raw = json.dumps(source).encode(); (tmp_path / "trace.json").write_bytes(raw)
        review["source"]["sha256"] = hashlib.sha256(raw).hexdigest()
        review["run_outcome"] = "fail"
        review["reviewed_entries"][1]["sha256"] = _digest("fail")
        review["findings"] = [{"classification": "unresolved", "description": "Retained failure requires investigation", "citations":
                               [{"pointer": "/outcome", "quote": "fail"}]}]
    if case == "partial": review["reviewed_entries"].pop()
    (tmp_path / "review.json").write_text(json.dumps(review))
    native = copy.deepcopy(REVIEW)
    native.update(trace_refs=["trace.json"], steps_read=2, steps_total=2)
    obs = json.loads(_observation(er_id, "REFUTES" if case == "refuted" else "SUPPORTS", native))
    obs.update(subject_revision=revision, dependency_paths=[project.materialization.target_path],
               retained_artifact_refs=["trace.json", "review.json"],
               result={"trace_reviews": [] if case == "missing" else ["review.json"], "run_id": "native-probe"})
    directory = tmp_path / project.materialization.observations_root
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "OBS-TRACE-1.yaml").write_text(json.dumps(obs))
    report = assess(tmp_path)
    first = report.criteria[0].requirements[0]
    PROBE_EVENTS.append({"input": {"case": case, "native_observation": obs},
                         "output": {"criterion": report.criteria[0].criterion_id,
                                    "standing": report.criteria[0].standing,
                                    "er_status": first.status, "detail": first.detail}})
    assert first.status == expected, first
    if case == "failed": assert "full review complete; run=fail" in first.detail
    # Projection checks never rewrite the preserved native observation.
    assert json.loads((directory / "OBS-TRACE-1.yaml").read_text()) == obs
