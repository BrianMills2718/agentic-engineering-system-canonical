"""AES canonical governs itself (roadmap phase 6b, `SC-GF-003`, `SC-GF-004`).

Unlike every other file in this directory, these tests read the live
repository they are part of, not a fixture or a temporary clone: the subject
is AES's own `.aes/` target at the checked-out revision. That is intended. The
repository governing itself is the claim, so the check has to run against it.

ER-SC-GF-003-02: the unchanged planned topology is accepted at HEAD (every
governed file, the retained v0.1 files included, is a planned artifact).
ER-SC-GF-004-01: every evidence requirement in the live target has a route.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ruamel.yaml import YAML

from agentic_engineering_system.cli import main
from agentic_engineering_system.planning import route_violations
from agentic_engineering_system.records import load_project, load_target
from agentic_engineering_system.topology import compare_topology, normalized_roots

REPO = Path(__file__).resolve().parents[2]
# The accepted copy (Decision 0010), not the proposal lineage file it was copied from.
SEMANTIC_INSTANCE = REPO / "docs" / "architecture" / "greenfield-v0.2" / "12-greenfield-mvp-semantic-instance.yaml"
V01_RETAINED = ("repository_context",)  # real v0.1 code: console script aes-repo-context
V01_ARCHIVED = (  # empty placeholders, moved to archive/v0.1-placeholders/ in phase 7a
    "capability_sourcing", "evidence_assessment", "execution", "gap_reconciliation", "learning",
    "normative_context", "planning", "policy_control",
)


def _target():
    project = load_project(REPO / ".aes" / "project.yaml")
    return project, load_target(REPO / project.materialization.target_path)


def _words(text: str) -> str:
    return " ".join(str(text).split())


def test_own_target_loads_strictly_with_the_greenfield_criteria_verbatim():
    _, target = _target()
    source = YAML(typ="safe").load(SEMANTIC_INSTANCE.read_text(encoding="utf-8"))
    want = {c["id"]: c for c in source["success_criteria"]}
    # the greenfield criteria, verbatim; later outcomes (SC-AP-*, PLAN-AES-COMMIT-RULE) add their own
    got = {c.id: c for c in target.success_criteria if c.id.startswith("SC-GF-")}
    assert sorted(got) == sorted(want) == [f"SC-GF-00{i}" for i in range(1, 10)]
    for sc_id, c in want.items():
        assert _words(got[sc_id].statement) == _words(c["statement"]), sc_id
        assert _words(got[sc_id].disproof) == _words(c["disproof"]), sc_id
        assert got[sc_id].target_refs == c["target_refs"], sc_id
        assert [(e.id, _words(e.requirement)) for e in got[sc_id].evidence_requirements] == [
            (e["id"], _words(e["requirement"])) for e in c["evidence_requirements"]
        ], sc_id
    items = {n.id: n for n in target.normative_items}
    for n in source["normative_items"]:
        assert _words(items[n["id"]].statement) == _words(n["statement"]), n["id"]


def test_topology_at_head_has_no_orphan_and_plans_the_v01_files_as_history():
    project, target = _target()
    governed = normalized_roots(project.governed_roots)
    listed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "-z", "HEAD", "--", *governed],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout
    files = tuple(p for p in listed.split("\0") if p)
    report = compare_topology(governed, files, target)
    assert report.orphans == ()
    by_path = {a.locator.exact_path: a for a in target.planned_artifacts}
    v01 = [p for p in files if p.split("/")[2] in V01_RETAINED]
    assert v01 and "src/agentic_engineering_system/repository_context/cli.py" in v01
    for path in [*v01, "src/agentic_engineering_system/__init__.py"]:
        assert by_path[path].semantic_justification_refs == ["NI-AES-HIST"], path
    # the archived placeholders left the governed root and the target, and kept their history
    gone = tuple(f"src/agentic_engineering_system/{pkg}/" for pkg in V01_ARCHIVED)
    assert not [p for p in [*files, *by_path] if p.startswith(gone)]
    archived = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "--", "archive/v0.1-placeholders/"],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout.split()
    assert sorted(archived) == sorted(
        [f"archive/v0.1-placeholders/{pkg}/component.placeholder.yaml" for pkg in V01_ARCHIVED]
        + ["archive/v0.1-placeholders/README.md"]
    )
    assert "tests/greenfield/test_self_governance.py" in by_path


def test_every_greenfield_evidence_requirement_has_a_route():
    _, target = _target()
    assert route_violations(target) == []
    external = {b.evidence_requirement_ref for b in target.external_boundaries}
    assert {e for e in external if e.startswith("ER-SC-GF-")} == {"ER-SC-GF-001-01", "ER-SC-GF-005-02", "ER-SC-GF-009-01"}
    assert external - {"ER-SC-GF-001-01", "ER-SC-GF-005-02", "ER-SC-GF-009-01"} == {"ER-AP-001-02"}


def test_aes_status_on_this_repository_exits_zero(capsys):
    assert main(["status", "--root", str(REPO)]) == 0
    out = capsys.readouterr().out
    assert "agentic-engineering-system-canonical-target" in out
    assert "0 orphan(s)" in out
