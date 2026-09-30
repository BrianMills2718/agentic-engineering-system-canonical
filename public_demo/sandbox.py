"""Real AES runs for the public demo: throwaway git repositories driven by the real ``aes`` CLI.

Nothing here simulates AES. Every judgement shown to a visitor comes from the installed
``agentic_engineering_system`` package: the ``aes`` command writes and validates the target, runs the sample
project's pytest and records the observation, and ``evidence.assess`` / ``reconcile.reconcile`` compute every
standing and freshness from the repository and its recorded observations.

Visitors never name a path, a command or code. The sample project ("greeter") is a fixed fixture; a visitor's own
goal is only ever text inside a proposal that is validated, never executed.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from agentic_engineering_system import evidence, reconcile
from agentic_engineering_system.records import load_target

AES = shutil.which("aes") or str(Path(sys.executable).with_name("aes"))
STEP_TIMEOUT_SECONDS = 60

GREETER_OUTCOME = "Calling greet with a name returns a greeting that contains that name."
GREETER_ACTOR = "a script author who needs a greeting"

GREETER_PROPOSAL = """\
schema_version: aes.v0_2.proposal.probe0
proposal_id: PLAN-001-GREET
title: Greet by name
rationale: >
  OUT-001 has nothing planned under it yet. This plans one chain from the outcome to a test before any code is written.
closes_gaps: []
target_delta:
  add:
    normative_items:
      - id: NI-001
        kind: behavior
        outcome_refs: [OUT-001]
        statement: >
          greet(name) returns "Hello, <name>!" and rejects an empty name with ValueError instead of greeting nobody.
    success_criteria:
      - id: SC-001
        statement: greet greets a given name and refuses an empty one.
        target_refs: [NI-001]
        disproof: >
          greet returns a string without the name, or returns anything for an empty name.
        evidence_requirements:
          - id: ER-001-01
            kind: deterministic_test
            requirement: >
              A test calls greet("Ada") and checks the exact greeting, and checks that greet("") raises ValueError.
    components:
      - id: CMP-GREETER
        responsibility: produce greetings
        target_refs: [NI-001]
        planned_artifact_refs: [ART-PKG, ART-TEST-GREET]
    planned_artifacts:
      - id: ART-PKG
        locator: {exact_path: src/greeter/__init__.py}
        kind: source
        purpose: the greet function
        semantic_justification_refs: [NI-001]
      - id: ART-TEST-GREET
        locator: {exact_path: tests/test_greet.py}
        kind: test
        purpose: prove SC-001
        semantic_justification_refs: [SC-001]
    verification_subjects:
      - id: VS-GREET
        criterion_refs: [SC-001]
        evidence_requirement_refs: [ER-001-01]
        proof_kind: deterministic_test
        proof_role: direct
        locator: tests/test_greet.py
        purpose: prove greet greets a name and refuses an empty one
"""

# The same proposal without its verification subject: nothing would ever prove ER-001-01, so AES must refuse it.
REFUSED_PROPOSAL = GREETER_PROPOSAL.split("    verification_subjects:")[0].replace("PLAN-001-GREET", "PLAN-001-NOPROOF")

GREETER_SRC = '''def greet(name: str) -> str:
    if not name:
        raise ValueError("name must not be empty")
    return f"Hello, {name}!"
'''
GREETER_SRC_CHANGED = GREETER_SRC.replace("Hello", "Hi")
GREETER_TEST = '''import pytest

from greeter import greet


def test_greets_the_name() -> None:
    assert greet("Ada") == "Hello, Ada!"


def test_refuses_an_empty_name() -> None:
    with pytest.raises(ValueError):
        greet("")
'''

# step -> (label shown to visitors, step that must come first, or None)
GREETER_STEPS = {
    "plan": ("Plan the goal", None),
    "build": ("Write the code and run its test", "plan"),
    "change": ("Change the greeting to \"Hi\"", "build"),
    "retest": ("Run the test again", "change"),
}


class SandboxError(Exception):
    """A plain-sentence failure that is safe to show a visitor."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


def _env(home: Path) -> dict[str, str]:
    """A minimal environment: no API key, no user config, a fixed git identity."""
    return {
        "PATH": str(Path(AES).parent) + os.pathsep + "/usr/local/bin:/usr/bin:/bin",
        "HOME": str(home),
        "LC_ALL": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "GIT_AUTHOR_NAME": "AES demo", "GIT_AUTHOR_EMAIL": "demo@example.invalid",
        "GIT_COMMITTER_NAME": "AES demo", "GIT_COMMITTER_EMAIL": "demo@example.invalid",
        "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull,
    }


@dataclass
class Workspace:
    """One throwaway git repository plus the log of real commands run in it."""

    root: Path
    log: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def create(cls, parent: Path) -> "Workspace":
        parent.mkdir(parents=True, exist_ok=True)
        root = Path(tempfile.mkdtemp(prefix="ws-", dir=parent))
        (root / "repo").mkdir()
        ws = cls(root=root / "repo")
        ws.run(["git", "init", "-q", "-b", "main"], show=False)
        return ws

    def run(self, argv: list[str], *, show: bool = True, ok_codes: tuple[int, ...] = (0,)) -> tuple[int, str]:
        try:
            done = subprocess.run(
                argv, cwd=self.root, env=_env(self.root.parent), capture_output=True, text=True,
                timeout=STEP_TIMEOUT_SECONDS, stdin=subprocess.DEVNULL,
            )
        except subprocess.TimeoutExpired as exc:
            raise SandboxError(504, "AES took too long on that step, so it was stopped. Nothing was made up.") from exc
        text = (done.stdout + done.stderr).strip()
        text = text.replace(str(self.root), "<project>")
        if show:
            self.log.append({"cmd": " ".join(["aes" if argv[0] == AES else argv[0], *argv[1:]]), "exit": done.returncode, "output": text})
        if done.returncode not in ok_codes:
            raise SandboxError(500, f"A real AES command failed unexpectedly: {' '.join(argv[1:3])} (exit {done.returncode}).")
        return done.returncode, text

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, message: str) -> str:
        self.run(["git", "add", "-A"], show=False)
        self.run(["git", "commit", "-q", "-m", message], show=False)
        _, sha = self.run(["git", "rev-parse", "--short=7", "HEAD"], show=False)
        return sha

    def aes(self, *args: str, ok_codes: tuple[int, ...] = (0,)) -> tuple[int, str]:
        return self.run([AES, *args], ok_codes=ok_codes)

    def destroy(self) -> None:
        shutil.rmtree(self.root.parent, ignore_errors=True)


# --------------------------------------------------------------------------- reading the real state
_STANDING_WORD = {"SUPPORTED": "supported", "INSUFFICIENT": "insufficient", "REFUTED": "refuted"}


def read_state(root: Path, *, observation_limit: int | None = None) -> dict[str, Any]:
    """Standings, observations and artifacts, computed by AES's own code (not parsed from text)."""
    target = load_target(root / ".aes" / "target.yaml")
    report = evidence.assess(root)
    by_id = {o.observation_id: o for o in evidence.load_observations(root, ".aes/observations/", target)} if (root / ".aes" / "observations").exists() else {}
    superseded = dict(report.superseded)
    sc_by_id = {sc.id: sc for sc in target.success_criteria}
    kinds = {er_id: er.kind for er_id, (_, er) in target.evidence_requirements().items()}
    requirement_text = {er_id: er.requirement for er_id, (_, er) in target.evidence_requirements().items()}
    routes: dict[str, str] = {}
    for vs in target.verification_subjects:
        for er in vs.evidence_requirement_refs:
            routes[er] = f"{vs.proof_kind}: {vs.locator}"
    for eb in target.external_boundaries:
        routes.setdefault(eb.evidence_requirement_ref, f"outside the repo: {eb.boundary}")
    criteria = []
    for c in report.criteria:
        sc = sc_by_id[c.criterion_id]
        criteria.append({
            "id": c.criterion_id, "statement": sc.statement, "disproof": sc.disproof, "standing": c.standing,
            "requirements": [
                {"id": s.er_id, "status": s.status, "detail": s.detail, "kind": kinds.get(s.er_id),
                 "text": requirement_text.get(s.er_id), "route": routes.get(s.er_id)}
                for s in c.requirements
            ],
        })
    observations = []
    for oid, fresh, why in report.observations:
        rec = by_id.get(oid)
        assessment = rec.assessments[0].assessment if rec and rec.assessments else None
        observations.append({
            "id": oid, "freshness": fresh, "reason": why, "superseded_by": superseded.get(oid),
            "assessment": assessment,
            "commit": (rec.subject_revision or "")[:7] if rec else "",
            "criteria": sorted({ref for ref in (rec.subject_refs if rec else [])}),
            "ers": [a.evidence_requirement_ref for a in rec.assessments] if rec else [],
            "produced_at": rec.produced_at.isoformat() if rec else None,
        })
    counts = {k: sum(1 for c in criteria if c["standing"] == k) for k in _STANDING_WORD}
    return {"target_id": target.target_id, "criteria": criteria, "counts": counts, "observations": observations,
            "outcomes": [{"id": o.id, "statement": o.statement, "actor": o.actor_or_consumer} for o in target.outcomes],
            "freshness_counts": report.counts()}


def read_artifacts(root: Path) -> list[dict[str, str]]:
    rec = reconcile.reconcile(root)
    return [{"id": a.artifact_id, "path": a.path, "status": a.status} for a in rec.artifacts]


def git_commits(ws: Workspace) -> list[dict[str, Any]]:
    _, out = ws.run(["git", "log", "--reverse", "--format=%h%x09%s"], show=False)
    commits = []
    for line in out.splitlines():
        if not line:
            continue
        sha, message = line.split("\t", 1)
        _, files = ws.run(["git", "show", "--name-only", "--format=", sha], show=False)
        commits.append({"sha": sha, "message": message, "files": [f for f in files.splitlines() if f]})
    return commits


# --------------------------------------------------------------------------- the sample project
def _greeter_state(ws: Workspace, done: list[str], note: str) -> dict[str, Any]:
    state = read_state(ws.root)
    state.update(commits=git_commits(ws), artifacts=read_artifacts(ws.root), done=list(done), note=note,
                 log=list(ws.log), steps=[{"id": k, "label": v[0]} for k, v in GREETER_STEPS.items()])
    return state


def greeter_init() -> Workspace:
    return Workspace.create(Path(os.environ.get("AES_DEMO_TMP", tempfile.gettempdir())) / "aes-demo")


def greeter_step(ws: Workspace, done: list[str], step: str) -> dict[str, Any]:
    """Run one fixed step of the sample project. Order is enforced; nothing here comes from the visitor."""
    if step not in GREETER_STEPS:
        raise SandboxError(400, "That step does not exist.")
    if step in done:
        raise SandboxError(409, "That step has already run. Use Start over to begin again.")
    needed = GREETER_STEPS[step][1]
    if needed and needed not in done:
        raise SandboxError(409, f"Run \"{GREETER_STEPS[needed][0]}\" first.")
    note = ""
    if step == "plan":
        ws.write(".gitignore", ".venv/\n__pycache__/\n.pytest_cache/\n")
        ws.write("pyproject.toml", '[tool.pytest.ini_options]\npythonpath = ["src"]\n')
        ws.aes("init", "--project-id", "greeter", "--actor", GREETER_ACTOR, "--outcome", GREETER_OUTCOME)
        ws.commit("Initialize AES")
        ws.write("proposal.yaml", GREETER_PROPOSAL)
        ws.aes("plan", "validate", "proposal.yaml")
        ws.aes("plan", "accept", "proposal.yaml")
        (ws.root / "proposal.yaml").unlink()
        ws.commit("Plan the goal: greet by name")
        note = "AES accepted the plan. The goal is written down with a test that would prove it, but nothing has been proven yet."
    elif step == "build":
        ws.write("src/greeter/__init__.py", GREETER_SRC)
        ws.write("tests/test_greet.py", GREETER_TEST)
        ws.commit("Write greet and its test")
        ws.aes("evidence", "record", "VS-GREET", "--depends-on", "src/greeter/__init__.py")
        ws.commit("Record the test result")
        note = "The test ran for real at this commit and passed, so AES now counts the goal as supported."
    elif step == "change":
        ws.write("src/greeter/__init__.py", GREETER_SRC_CHANGED)
        ws.commit("Change the greeting to Hi")
        note = "The code the evidence depended on changed. AES does not re-run anything; it just stops trusting the old result."
    elif step == "retest":
        ws.aes("evidence", "record", "VS-GREET", "--depends-on", "src/greeter/__init__.py", ok_codes=(0, 1))
        ws.commit("Record the new test result")
        note = "The test now fails (it expects \"Hello\"), so the recorded evidence refutes the goal."
    done = [*done, step]
    ws.aes("evidence", "status", ok_codes=(0, 1))
    return _greeter_state(ws, done, note)


# --------------------------------------------------------------------------- a proposal AES refuses
def refused_proposal_demo() -> dict[str, Any]:
    """Run the real `aes plan validate` on a plan whose requirement has no proof. No model; fixed text."""
    ws = Workspace.create(Path(os.environ.get("AES_DEMO_TMP", tempfile.gettempdir())) / "aes-demo")
    try:
        ws.write("pyproject.toml", '[tool.pytest.ini_options]\npythonpath = ["src"]\n')
        ws.aes("init", "--project-id", "greeter", "--actor", GREETER_ACTOR, "--outcome", GREETER_OUTCOME)
        ws.commit("Initialize AES")
        ws.write("proposal.yaml", REFUSED_PROPOSAL)
        code, text = ws.aes("plan", "validate", "proposal.yaml", ok_codes=(0, 1, 2))
        violations = [ln.strip()[2:] for ln in text.splitlines() if ln.strip().startswith("- ")]
        return {"accepted": code == 0, "exit": code, "violations": violations, "log": ws.log, "outcome": GREETER_OUTCOME,
                "tree": proposal_tree(REFUSED_PROPOSAL, violations),
                "explanation": "This plan says greet must be proven but names no test or other way to prove it. AES refuses a goal it could never check."}
    finally:
        ws.destroy()


# --------------------------------------------------------------------------- the visitor's own goal
KINDS = ("deterministic_test", "runtime_observation", "human_review")


def build_goal_proposal(outcome: str, draft: dict[str, Any]) -> str:
    """Turn the model's draft into an AES proposal (YAML text). Ids and structure are made here, not by the model."""
    criteria = draft["criteria"]
    add: dict[str, list[dict[str, Any]]] = {"normative_items": [], "success_criteria": [], "verification_subjects": [],
                                            "planned_artifacts": [], "components": []}
    boundaries: list[dict[str, str]] = []
    artifact_ids: list[str] = []
    seen_paths: dict[str, str] = {}
    add["normative_items"].append({"id": "NI-001", "kind": "behavior", "outcome_refs": ["OUT-001"], "statement": outcome})
    for i, c in enumerate(criteria, 1):
        n = f"{i:03d}"
        sc: dict[str, Any] = {"id": f"SC-{n}", "statement": c["statement"].strip(), "target_refs": ["NI-001"],
                              "disproof": c["disproof"].strip(), "evidence_requirements": []}
        for j, r in enumerate(c["requirements"], 1):
            er_id = f"ER-SC-{n}-{j:02d}"
            sc["evidence_requirements"].append({"id": er_id, "kind": r["kind"], "requirement": r["requirement"].strip()})
            how = r["how"].strip()
            if r["kind"] == "deterministic_test":
                if how not in seen_paths:
                    art_id = f"ART-TEST-{len(seen_paths) + 1:02d}"
                    seen_paths[how] = art_id
                    artifact_ids.append(art_id)
                    add["planned_artifacts"].append({"id": art_id, "locator": {"exact_path": how}, "kind": "test",
                                                     "purpose": c["statement"].strip()[:120], "semantic_justification_refs": [f"SC-{n}"]})
                add["verification_subjects"].append({
                    "id": f"VS-{n}-{j:02d}", "criterion_refs": [sc["id"]], "evidence_requirement_refs": [er_id],
                    "proof_kind": "deterministic_test", "proof_role": "direct", "locator": how, "purpose": c["statement"].strip()[:120]})
            else:
                boundaries.append({"evidence_requirement_ref": er_id, "boundary": how})
        add["success_criteria"].append(sc)
    if artifact_ids:
        add["components"].append({"id": "CMP-GOAL", "responsibility": "deliver the goal", "target_refs": ["NI-001"],
                                  "planned_artifact_refs": artifact_ids})
    if boundaries:
        add["external_boundaries"] = boundaries  # type: ignore[assignment]
    add = {k: v for k, v in add.items() if v}
    proposal = {"schema_version": "aes.v0_2.proposal.probe0", "proposal_id": "PLAN-001-VISITOR-GOAL",
                "title": "Plan the visitor's goal", "rationale": "Drafted from the visitor's sentence; AES decides whether it is acceptable.",
                "closes_gaps": [], "target_delta": {"add": add}}
    return yaml.safe_dump(proposal, sort_keys=False, allow_unicode=False, width=100)


def proposal_tree(proposal_yaml: str, violations: list[str], standings: dict[str, str] | None = None) -> dict[str, Any]:
    """The goal -> criteria -> requirements -> how-proven tree of a proposal, with each violation attached to the requirement it names."""
    add = yaml.safe_load(proposal_yaml)["target_delta"]["add"]
    routes: dict[str, str] = {}
    for vs in add.get("verification_subjects", []):
        for er in vs["evidence_requirement_refs"]:
            routes[er] = f"{vs['proof_kind']}: {vs['locator']}"
    for eb in add.get("external_boundaries", []):
        routes.setdefault(eb["evidence_requirement_ref"], f"outside the repo: {eb['boundary']}")
    criteria = []
    for sc in add.get("success_criteria", []):
        reqs = []
        for er in sc["evidence_requirements"]:
            problems = [v for v in violations if f"'{er['id']}'" in v]
            reqs.append({"id": er["id"], "kind": er["kind"], "text": " ".join(er["requirement"].split()),
                         "route": routes.get(er["id"]), "problems": problems})
        criteria.append({"id": sc["id"], "statement": " ".join(sc["statement"].split()), "disproof": " ".join(sc["disproof"].split()),
                         "standing": (standings or {}).get(sc["id"]), "requirements": reqs})
    attached = {p for c in criteria for r in c["requirements"] for p in r["problems"]}
    return {"criteria": criteria, "other_problems": [v for v in violations if v not in attached]}


def check_goal(outcome: str, draft: dict[str, Any]) -> dict[str, Any]:
    """Run the model's draft through real `aes plan validate` (and `accept` when it passes)."""
    for c in draft["criteria"]:
        for r in c["requirements"]:
            if r["kind"] not in KINDS:
                raise SandboxError(422, "The model proposed an evidence kind AES does not have, so nothing was checked.")
    ws = Workspace.create(Path(os.environ.get("AES_DEMO_TMP", tempfile.gettempdir())) / "aes-demo")
    try:
        ws.write("pyproject.toml", '[tool.pytest.ini_options]\npythonpath = ["src"]\n')
        ws.aes("init", "--project-id", "your-goal", "--actor", "the person who wrote this goal", "--outcome", outcome)
        ws.commit("Initialize AES")
        text = build_goal_proposal(outcome, draft)
        ws.write("proposal.yaml", text)
        code, out = ws.aes("plan", "validate", "proposal.yaml", ok_codes=(0, 1, 2))
        violations = [ln.strip()[2:] for ln in out.splitlines() if ln.strip().startswith("- ")]
        result: dict[str, Any] = {"accepted": code == 0, "violations": violations, "proposal_yaml": text, "outcome": outcome}
        result["tree"] = proposal_tree(text, violations)
        if code == 0:
            ws.aes("plan", "accept", "proposal.yaml")
            (ws.root / "proposal.yaml").unlink()
            ws.commit("Plan the goal")
            ws.aes("evidence", "status", ok_codes=(0, 1))
            result["state"] = read_state(ws.root)
            result["tree"] = proposal_tree(text, [], {c["id"]: c["standing"] for c in result["state"]["criteria"]})
        result["log"] = ws.log
        return result
    finally:
        ws.destroy()


# --------------------------------------------------------------------------- AES on its own repository
def self_state(root: Path) -> dict[str, Any]:
    """The real `aes status` / `aes evidence status` over a pinned checkout of AES itself."""
    state = read_state(root)
    rec = reconcile.reconcile(root)
    done = subprocess.run([AES, "status"], cwd=root, capture_output=True, text=True, stdin=subprocess.DEVNULL,
                          env=_env(Path(tempfile.gettempdir())), timeout=STEP_TIMEOUT_SECONDS)
    ev = subprocess.run([AES, "evidence", "status"], cwd=root, capture_output=True, text=True, stdin=subprocess.DEVNULL,
                        env=_env(Path(tempfile.gettempdir())), timeout=STEP_TIMEOUT_SECONDS)
    state.update(
        revision=rec.subject_revision, dirty=rec.dirty,
        components=[{"id": c.component_id, "gaps": [{"kind": g.kind, "ref": g.ref, "detail": g.detail} for g in c.gaps]} for c in rec.components],
        artifacts_total=len(rec.artifacts), artifacts_realized=sum(1 for a in rec.artifacts if a.status == "REALIZED"),
        log=[{"cmd": "aes status", "exit": done.returncode, "output": done.stdout.strip()},
             {"cmd": "aes evidence status", "exit": ev.returncode, "output": ev.stdout.strip()}],
    )
    return state


def jsonable(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)
