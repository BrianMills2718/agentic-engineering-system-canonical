"""S4: licences for proposed fixes, derived by the Observation-to-Action evaluator (PLAN.md, slice S4).

A general fix that S3's analysis proposes for a recurring problem is a claim that would justify a rule
(Prevent) or a check (Detect). Its licence is a `sci:LicenseRelation` with three conditions, and its status
is derived by the metamodel's own `evaluate.derive_licence_status` (R-401), never set here:

  sightings   at least two independent sightings (problems.sightings)      judged by code   -> derived
  challenge   no confirmed `challenges` relation touches the problem        judged by code   -> derived
  cause       every cause step the fix rests on is `seen` or `inferred`     judged by the agent (decision
              (a guessed step leaves the condition unassessed)                035 default) -> asserted

Consequence class `exploratory` (floor: asserted): an adopted rule stays revocable, and S5 adds the
observed effect; a recurrence after enforcement sets `revoked` (effects.py).
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

METAMODEL = Path(os.environ.get("O2A_METAMODEL", Path.home() / "code/observation-to-action-metamodel"))
CONSEQUENCE_CLASS = "exploratory"


def fixture_for(problem: dict, fix: dict, challenged: bool, revoked: bool = False) -> dict:
    """One licence and its conditions as a metamodel record (nodes + hyperedges)."""
    rests = set(fix.get("rests_on") or [])
    causes = [c for c in (problem.get("analysis") or {}).get("cause_chain", []) if rests & set(c.get("rests_on") or [])]
    cause_ok = bool(causes) and all(c["basis"] in ("seen", "inferred") for c in causes)
    label = {"satisfied": "n-sat", "unassessed": "n-unassessed", "unsatisfied": "n-unsat"}
    nodes = [{"id": i, "kind": "element", "label": l} for i, l in [
        ("n-claim", fix["text"]), ("n-subjects", problem["id"]), ("n-class", CONSEQUENCE_CLASS),
        ("n-sat", "satisfied"), ("n-unassessed", "unassessed"), ("n-unsat", "unsatisfied"),
        ("n-derived", "derived"), ("n-asserted", "asserted"), ("n-true", "true"),
        ("n-basis-code", "computed by scripts/learning_loop/problems.py"),
        ("n-basis-agent", "judged by the analysis (agent judge, decision 035)")]]
    lic_roles = {"result": "n-claim", "subjects": "n-subjects", "consequenceClass": "n-class"}
    if revoked:
        lic_roles["revoked"] = "n-true"
    edges = [{"id": "lic", "type": "sci:LicenseRelation", "roles": lic_roles}]
    for cid, status, establishment, basis in [
            ("c-sightings", "satisfied" if problem["sightings"] >= 2 else "unassessed", "n-derived", "n-basis-code"),
            ("c-challenge", "unsatisfied" if challenged else "satisfied", "n-derived", "n-basis-code"),
            ("c-cause", "satisfied" if cause_ok else "unassessed", "n-asserted", "n-basis-agent")]:
        edges.append({"id": cid, "type": "sci:LicenseConditionRelation",
                      "roles": {"licence": "lic", "status": label[status], "establishment": establishment,
                                "basis": basis}})
    return {"nodes": nodes, "hyperedges": edges, "provenance": {"problem": problem["id"], "fix": fix["text"]}}


def derive(fixture: dict) -> str:
    """R-401 status from the metamodel's evaluator (imported from its checkout, not reimplemented)."""
    sys.path.insert(0, str(METAMODEL))
    import evaluate as ev  # noqa: E402  (the metamodel's own module)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(fixture, fh)
    try:
        fx = ev.load(fh.name)
        return ev.derive_licence_status(fx, next(iter(ev.edges(fx, "sci:LicenseRelation"))))
    finally:
        os.unlink(fh.name)


def licences_for(problem: dict, challenged: bool) -> list[dict]:
    out = []
    for fix in (problem.get("analysis") or {}).get("fixes", []):
        if fix["intent"] not in ("Prevent", "Detect"):
            continue
        fx = fixture_for(problem, fix, challenged)
        out.append({"problem": problem["id"], "intent": fix["intent"], "text": fix["text"],
                    "status": derive(fx), "conditions": {e["id"]: e["roles"]["status"] for e in fx["hyperedges"][1:]}})
    return out
