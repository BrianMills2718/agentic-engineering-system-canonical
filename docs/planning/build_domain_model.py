"""Write the AES canonical domain model: docs/planning/domain.graph.json and docs/planning/DOMAIN.md.

One list of concepts below is the single source for both outputs, so the graph and the glossary
cannot disagree. Each concept carries its definition, the document that defines it (file:line) and
where the code implements it. Concepts named only in documents, or retired, are dashed (kinds
DocOnly and Retired) and cite no code. The graph is typed-graph/v1
(representation-router/schemas/typed-graph.schema.json), drawn by representation-router/graph-viewer
on the planning review page. Adapted from ecosystem-ops docs/planning/build_domain_model.py.

    python3 docs/planning/build_domain_model.py   # rewrites both files

Source revision read: origin/main 30e9993 (2026-10-27).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
GRAPH = HERE / "domain.graph.json"
GLOSSARY = HERE / "DOMAIN.md"
IMPLEMENTED = HERE / "domain.implemented.json"

KINDS = {
    "Target": ("Plan records (in code)", "#1f5f99",
               "What .aes/target.yaml declares: outcomes, rules, criteria, components and the files planned for them."),
    "Change": ("Changing the plan (in code)", "#5f8fc2",
               "How the target changes: a proposal with a delta, accepted into a plan record."),
    "Evidence": ("Evidence (in code)", "#3b78b8",
                 "Observations bound to a commit, their freshness, and the standing they give each criterion."),
    "State": ("Current state (in code)", "#2b4c6f",
              "What HEAD contains, how it differs from the plan, and the gaps that remain."),
    "Context": ("Context and project records (in code)", "#7a8fa6",
                "Project settings, the working-context packet, the v0.1 repository context, and the project brain."),
    "DocOnly": ("Only in documents", "#d9822b",
                "Named in the goal, decisions or plans, with no code here that implements it."),
    "External": ("Written by another tool", "#b8860b",
                 "Records stored here that another tool (Company Planning) writes and reads; no AES code reads them."),
    "Retired": ("Retired (history)", "#9aa3ad",
                "Removed on 2026-10-14; documents still describe it."),
}
DASHED_KINDS = {"DocOnly", "External", "Retired"}

S = "src/agentic_engineering_system/"
# id, label, kind, definition, defined in (file:line), code (file:line or None)
CONCEPTS = [
    ("target", "Target", "Target",
     "The plan of record, .aes/target.yaml: outcomes, normative items, success criteria, components, planned artifacts and verification subjects.",
     "docs/model/ODD.md:33", S + "records.py:137"),
    ("outcome", "Outcome", "Target",
     "What an actor or consumer gets (OUT-GF-001, OUT-AP-001), with its non-goals.",
     "docs/architecture/GOAL.md:12", S + "records.py:65"),
    ("normative-item", "Normative item", "Target",
     "A constraint, behavior, invariant or quality the system must hold, tied to outcomes.",
     "docs/architecture/GOAL.md:11", S + "records.py:73"),
    ("success-criterion", "Success criterion", "Target",
     "A checkable statement with a disproof and one or more evidence requirements; its standing decides whether it is a gap.",
     "docs/architecture/GOAL.md:11", S + "records.py:86"),
    ("evidence-requirement", "Evidence requirement", "Target",
     "One kind of evidence a criterion needs (deterministic test, runtime observation, human review or trace review); assessed one at a time, never per criterion.",
     S + "evidence.py:5", S + "records.py:80"),
    ("component", "Component", "Target",
     "A responsibility (RU-AES-*) that owns planned artifacts; `aes status` reports the first open gap per component.",
     "docs/model/ODD.md:33", S + "records.py:94"),
    ("planned-artifact", "Planned artifact", "Target",
     "A file at an exact path that the target plans; every file under a governed root must be one.",
     S + "topology.py:3", S + "records.py:105"),
    ("verification-subject", "Verification subject", "Target",
     "The test or check (with its proof role, direct or negative control) that routes evidence to a criterion's requirements.",
     "docs/model/ODD.md:33", S + "records.py:116"),
    ("external-boundary", "External boundary", "Target",
     "An evidence requirement routed outside the repository (a human review, an outside system) instead of to a local test.",
     "docs/model/ODD.md:33", S + "records.py:126"),
    ("governed-root", "Governed root", "Context",
     "A folder AES governs (src/agentic_engineering_system/, tests/greenfield/); only files there must be planned.",
     "AGENTS.md:33", S + "records.py:198"),
    ("project-record", "Project record", "Context",
     ".aes/project.yaml: project id, governed roots and where target, plans and observations live.",
     S + "topology.py:3", S + "records.py:194"),
    ("proposal", "Proposal", "Change",
     "A target delta plus the gaps it claims to close, checked by `aes plan validate` before it is accepted.",
     "docs/model/ODD.md:34", S + "planning.py:168"),
    ("target-delta", "Target delta", "Change",
     "The entries a proposal adds, replaces or removes in the target.",
     "docs/model/ODD.md:34", S + "planning.py:137"),
    ("accepted-plan", "Accepted plan", "Change",
     "A proposal applied by `aes plan accept`, kept in .aes/plans/ with the revision it was accepted at.",
     "AGENTS.md:39", S + "planning.py:197"),
    ("trace-review-declaration", "Trace-review declaration", "Change",
     "A proposal's statement of whether its work runs; work that runs needs a trace-review requirement (RULE-TRACE-REVIEW-DECLARED).",
     "docs/model/ODD.md:27", S + "planning.py:148"),
    ("observation", "Observation", "Evidence",
     "An append-only evidence record in .aes/observations/, bound to the commit it observed and the paths and target entries it depends on.",
     "docs/model/ODD.md:35", S + "evidence.py:176"),
    ("assessment", "Assessment", "Evidence",
     "An observation's verdict on one evidence requirement: SUPPORTS, REFUTES or INCONCLUSIVE.",
     S + "evidence.py:5", S + "evidence.py:96"),
    ("negative-control", "Negative control", "Evidence",
     "A case a control should refuse, recorded with whether it was detected; controls must prove they can fail (AES-POL-004).",
     "docs/architecture/GOAL.md:23", S + "evidence.py:112"),
    ("freshness", "Freshness", "Evidence",
     "CURRENT, STALE, UNKNOWN or UNREACHABLE, computed from Git: an observation is stale once a path or entry it depends on changes after its commit.",
     S + "evidence.py:9", S + "evidence.py:376"),
    ("standing", "Criterion standing", "Evidence",
     "SUPPORTED, REFUTED or INSUFFICIENT for each criterion; only current assessments count, and ignorance never renders green.",
     "docs/architecture/GOAL.md:21", S + "evidence.py:426"),
    ("characterization", "Characterization", "State",
     "What HEAD contains under the governed roots: each file's blob and its Python symbols.",
     "docs/model/ODD.md:36", S + "characterize.py:59"),
    ("drift", "Drift", "State",
     "A planned artifact whose committed symbols or signatures no longer match the target (formatting alone is not drift).",
     "docs/model/ODD.md:18", S + "characterize.py:204"),
    ("orphan", "Orphan", "State",
     "A tracked file under a governed root that the target does not plan; `aes topology check` fails on it.",
     S + "topology.py:3", S + "topology.py:73"),
    ("gap", "Gap", "State",
     "An unmet criterion or requirement that stays open until fresh evidence supports it.",
     "docs/model/ODD.md:22", S + "reconcile.py:113"),
    ("reconciliation", "Reconciliation", "State",
     "`aes status` / `aes reconcile`: artifacts, criteria, observations and plans composed into current state and first gap per component.",
     "docs/model/ODD.md:43", S + "reconcile.py:259"),
    ("legacy-baseline", "Legacy baseline", "State",
     "`aes adopt`: today's governed files in an existing repository accepted as legacy, without claiming conformance.",
     "docs/architecture/GOAL.md:61", S + "adopt.py:48"),
    ("working-context", "Working context", "Context",
     "`aes context <subject>`: the smallest complete packet of full-text rules and criteria for one subject, with what was left out listed.",
     S + "context.py:1", S + "context.py:72"),
    ("pre-commit-hook", "Pre-commit hook", "Context",
     "The hook `aes hooks install` writes; it refuses a commit that leaves an orphan under a governed root. Not running in this checkout since 2026-10-13: core.hooksPath runs lefthook, which never calls aes (Q16).",
     "AGENTS.md:39", S + "hooks.py:83"),
    ("repository-context", "Repository context (v0.1)", "Context",
     "The v0.1 Plan 001 artifact: authority surfaces and concern roots resolved from a checkout, with unresolved surfaces kept visible.",
     "docs/plans/001_repository_context_resolution_vertical.md:1", S + "repository_context/models.py:87"),
    ("project-brain", "Project brain", "Context",
     "The .project-brain/ files (now, state, truth, project) an agent reads first; a script reports when they are older than the work since.",
     "CLAUDE.md:5", "scripts/hive/brain_fresh.py:35"),
    ("thesis", "Checked-boundary thesis", "DocOnly",
     "The bet that agent-built software stays true to intent when every claim is checked against something an agent cannot talk past; with its disproof, still unmeasured.",
     "docs/architecture/GOAL.md:42", None),
    ("north-star", "Colleague starts a new project", "DocOnly",
     "OUT-GF-001's north star: a colleague without private repositories takes a new project from intent to evidence-backed state.",
     "docs/architecture/GOAL.md:37", None),
    ("value-tally", "Value tally", "DocOnly",
     "Decision 0011's pre-registered measure: AES catches versus hand checks a person still needed (whygame5: 1 catch, 6 hand checks).",
     "docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:64", None),
    ("offline-policy-replay", "Offline policy-decision replay (v0.1)", "DocOnly",
     "Plan 002, the v0.1 frontier, stopped at its provider-access step; no code here implements it.",
     "docs/plans/002_offline_policy_decision_replay.md:3", None),
    ("plan-receipt", "Plan adoption receipt", "External",
     "A Company Planning adoption record (*.receipt.json next to a plan in docs/plans/ or proposals/), naming the bounded-design profile revision the plan was adopted under; distinct from an AES accepted plan.",
     "docs/plans/adoption-progress-fields.receipt.json:1", None),
    ("commit-rule", "Commit rule", "Retired",
     "Commit tags and plan adoption per commit; removed on 2026-10-14 at Brian's request. .aes/commit_rule.yaml remains, read by no code.",
     "docs/model/ODD.md:55", None),
]

# source, target, label
EDGES = [
    ("target", "outcome", "declares"),
    ("target", "normative-item", "declares"),
    ("target", "success-criterion", "declares"),
    ("target", "component", "declares"),
    ("target", "planned-artifact", "declares"),
    ("target", "verification-subject", "declares"),
    ("target", "external-boundary", "declares"),
    ("normative-item", "outcome", "serves"),
    ("success-criterion", "normative-item", "checks"),
    ("success-criterion", "evidence-requirement", "needs"),
    ("component", "planned-artifact", "owns"),
    ("verification-subject", "evidence-requirement", "routes evidence to"),
    ("external-boundary", "evidence-requirement", "routes evidence to"),
    ("project-record", "governed-root", "names"),
    ("project-record", "target", "locates"),
    ("planned-artifact", "governed-root", "lives under"),
    ("proposal", "target-delta", "carries"),
    ("proposal", "gap", "claims to close"),
    ("proposal", "trace-review-declaration", "carries"),
    ("accepted-plan", "proposal", "is an accepted"),
    ("target-delta", "target", "changes"),
    ("verification-subject", "observation", "produces"),
    ("observation", "assessment", "holds one per requirement"),
    ("assessment", "evidence-requirement", "judges"),
    ("observation", "freshness", "has"),
    ("observation", "negative-control", "may record"),
    ("standing", "success-criterion", "is the standing of"),
    ("assessment", "standing", "counts toward, when current"),
    ("characterization", "planned-artifact", "describes"),
    ("drift", "planned-artifact", "found in"),
    ("orphan", "governed-root", "found under"),
    ("reconciliation", "characterization", "reads"),
    ("reconciliation", "standing", "reads"),
    ("reconciliation", "gap", "reports"),
    ("reconciliation", "drift", "reports"),
    ("legacy-baseline", "governed-root", "accepts files under"),
    ("working-context", "component", "compiled for"),
    ("pre-commit-hook", "orphan", "would refuse (dormant here)"),
    ("thesis", "standing", "rests on"),
    ("north-star", "outcome", "is the aim of"),
    ("value-tally", "thesis", "measures"),
    ("commit-rule", "plan-receipt", "required, per commit"),
    ("offline-policy-replay", "repository-context", "builds on"),
]


def main() -> None:
    nodes = []
    implemented = {}
    for cid, label, kind, definition, source, code in CONCEPTS:
        node = {"id": cid, "label": label, "kind": kind,
                "explain": f"{definition} Defined in {source}." + (f" Code: {code}." if code else " No code.")}
        if kind in DASHED_KINDS:
            node["dashed"] = True
        else:
            implemented[cid] = code
        nodes.append(node)
    ids = {n["id"] for n in nodes}
    edges = []
    for i, (s, t, label) in enumerate(EDGES):
        assert s in ids and t in ids, (s, t)
        edges.append({"id": f"e{i}", "source": s, "target": t, "label": label})
    graph = {
        "schema": "typed-graph/v1",
        "kinds": {k: {"label": v[0], "color": v[1], "explain": v[2], **({"dashed": True} if k in DASHED_KINDS else {})}
                  for k, v in KINDS.items()},
        "layout": {"direction": "RIGHT", "algorithm": "layered"},
        "nodes": nodes,
        "edges": edges,
    }
    GRAPH.write_text(json.dumps(graph, indent=1) + "\n", encoding="utf-8")
    IMPLEMENTED.write_text(json.dumps(implemented, indent=1) + "\n", encoding="utf-8")

    lines = [
        "---",
        "description: AES canonical's domain glossary -- every concept, its definition, where it is defined and where the code implements it",
        "---",
        "",
        "# AES canonical: domain glossary",
        "",
        "Generated by `docs/planning/build_domain_model.py` together with",
        "[domain.graph.json](domain.graph.json) (typed-graph/v1); edit the script, not this file.",
        "Project-local: these are the ideas this repository works with, not a company-wide ontology.",
        "Concepts marked *documents only*, *written by another tool* or *retired* have no code here.",
        "",
        "| Concept | Area | Definition | Defined in | Code |",
        "|---|---|---|---|---|",
    ]
    for cid, label, kind, definition, source, code in CONCEPTS:
        area = KINDS[kind][0]
        lines.append(f"| {label} (`{cid}`) | {area} | {definition} | `{source}` | {('`' + code + '`') if code else 'none'} |")
    lines += [
        "",
        "## Where the sources disagree",
        "",
        "- **The thesis still names the commit rule.** [GOAL.md](../architecture/GOAL.md) lines 44-46 and 55-57 describe",
        "  \"a commit refused without an adopted plan\" as a checked boundary and its bypass as the disproof; the commit rule",
        "  was removed on 2026-10-14 ([ODD.md](../model/ODD.md) line 55). Open question Q5.",
        "- **Decision 0010 says accepted with its 9 criteria supported; `aes status` now says 2 of 12.** The two counts cover",
        "  different sets: three criteria were added after the acceptance ([0010](../decisions/0010-greenfield-v0.2-accepted.md)",
        "  line 63; `.aes/target.yaml` lines 271, 289, 307), and 15 of 82 observations depend on `commit_rule.py`, deleted",
        "  in a06e963. Open question Q6.",
        "- **The target still holds the commit rule's outcome.** OUT-AP-001 (`.aes/target.yaml` line 12) says real work",
        "  lands only under an adopted plan; the rule that enforced it was removed. Open question Q15.",
        "- **AGENTS.md says the pre-commit hook refuses unplanned files; the hook does not run in this checkout.** Open question Q16.",
        "- **The adoption receipts say 23 plans are adopted and in progress; the project brain says nothing is being",
        "  continued.** [now.md](../../.project-brain/now.md) line 3 (on hold since 2026-10-18). Open question Q4.",
        "",
    ]
    GLOSSARY.write_text("\n".join(lines), encoding="utf-8")
    print(f"concepts={len(nodes)} implemented={len(implemented)} dashed={len(nodes) - len(implemented)} edges={len(edges)}")


if __name__ == "__main__":
    main()
