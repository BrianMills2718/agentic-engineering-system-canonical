"""Behavior 4.1: one page per requirement, its status from the code and the evidence, none typed."""

import re
from datetime import UTC, datetime, timedelta

import yaml
from agentic_engineering_system.planning import accept_proposal

from lockstep_support import sh
from lockstep.requirement_status import (BUILT, main, record_stale_evidence, requirement_pages, requirement_status,
                                    stale_pages, write_pages)

STATEMENT = """\
schema_version: aes.v0_2.proposal.probe0
proposal_id: PLAN-102-ANY-NAME
title: Greet any name
rationale: a normative change made by the test.
closes_gaps: []
trace_review:
  runs_traced_work: false
  reason: plain Python, judged by its tests.
target_delta:
  change:
    normative_items:
      - id: NI-001
        kind: behavior
        outcome_refs: [OUT-001]
        statement: greet(name) returns "Hello, <name>!" for any name it is given.
"""


def test_status_is_read_from_aes_at_the_current_commit(planned):
    status = requirement_status(planned)
    assert status["revision"] == sh("git rev-parse HEAD", planned).strip()
    assert not status["dirty"]
    assert set(status["criteria"]) == {"SC-001"}
    assert "standing" in status["criteria"]["SC-001"]
    assert status["artifacts"]["ART-GREET"]["status"]
    assert set(status["gaps"]) == {"CMP-GREETER"}  # every component is keyed, gaps or none


def test_a_drifted_export_shows_on_the_built_page_with_the_files_and_standing(proj):
    from lockstep.wiki import pages

    page = pages(proj, "greeter")["components/CMP-GREETER.md"]
    assert "**Drift between plan and code:** none" in page
    t = yaml.safe_load((proj / ".aes/target.yaml").read_text())
    next(a for a in t["planned_artifacts"] if a["id"] == "ART-GREET")["exports"] = ["greet(name: int) -> str"]
    (proj / ".aes/target.yaml").write_text(yaml.safe_dump(t, sort_keys=False))
    sh("git add -A && git commit -q -m 'plan says greet takes an int'", proj)  # AES characterizes the commit
    [d] = requirement_status(proj)["drift"]["ART-GREET"]
    assert (d["kind"], d["failing"]) == ("signature_changed", True)
    wiki = pages(proj, "greeter")
    page = wiki["components/CMP-GREETER.md"]
    src, test = ((proj / f).resolve().as_uri() for f in ("src/greeter/__init__.py", "tests/test_greet.py"))
    assert f"[src/greeter/__init__.py]({src}) (ART-GREET" in page and f"[tests/test_greet.py]({test}) (ART-TEST" in page
    assert "Standing now: **" in page
    assert (f"**Drift between plan and code:** [src/greeter/__init__.py]({src}) (ART-GREET) signature_changed: "
            "'greet' committed (name: int) -> str, found (name: str) -> str") in page
    assert "1 failing difference(s) at this commit" in wiki["index.md"]


def test_a_requirement_page_shows_its_text_then_each_result_with_commit_and_time_then_its_log(proj, tmp_path, monkeypatch):
    """ER-4.1-b."""
    path = tmp_path / "PLAN-102.yaml"
    path.write_text(STATEMENT)
    accept_proposal(proj, path, now=datetime.now(UTC) + timedelta(minutes=1))
    sh("make project && git add -A && git commit -q -m 'plan: greet any name'", proj)
    monkeypatch.setenv("PYTHONPATH", str(proj / "src"))  # the example's test imports greeter from src/
    assert record_stale_evidence(proj) == ["VS-GREET"]
    assert record_stale_evidence(proj) == []  # its result is now current
    head = sh("git rev-parse HEAD", proj).strip()
    wiki = requirement_pages(proj)
    page = wiki["requirements/OUT-001.md"]
    text = page.index("For someone: greet returns a greeting.")
    status = page.index("## Status")
    assert page.index("### NI-001\n\ngreet(name) returns") > status  # short heading, the behavior as text
    assert "Standing now: **SUPPORTED**" in page
    result = re.search(r"ER-001-01: \*\*supported\*\* — test passed at commit `(\w{12})`, "
                       r"\d{4}-\d\d-\d\d \d\d:\d\d UTC \(OBS-GREET-\w+\)", page)
    assert result and head.startswith(result[1])
    assert "- Files: `src/greeter/__init__.py` (ART-GREET, " in page and "- Drift between plan and code: none" in page
    log = page.index("## Change log")
    first, second = page.index("`PLAN-001-GREET`"), page.index("`PLAN-102-ANY-NAME`")
    assert text < status < result.start() < log < first < second  # text, status, then the log, newest last
    assert "On this requirement it changed behavior NI-001." in page  # plain words, not the plan's field names
    assert "- [OUT-001](requirements/OUT-001.md) — greet returns a greeting: 1 of 1 criteria supported" in wiki["index.md"]
    assert sum(line.startswith(BUILT) for line in page.splitlines()) == 1


def test_written_pages_pass_a_rebuild_and_are_reported_once_the_plan_changes(proj, tmp_path, capsys, monkeypatch):
    """ER-4.1-c."""
    monkeypatch.chdir(proj)  # the command finds its project from the working folder
    out = proj / "wiki/generated"
    assert sorted(write_pages(proj, out)) == ["change-log.md", "index.md", "requirements/OUT-001.md"]
    sh("git add -A && git commit -q -m 'write the pages'", proj)  # a new commit: only the built-at line differs
    assert stale_pages(proj, out) == [] and main(["--check", "wiki/generated"]) == 0
    assert write_pages(proj, out) == []  # a rebuild after the commit rewrites nothing, so a push can pass
    path = tmp_path / "PLAN-102.yaml"
    path.write_text(STATEMENT)
    accept_proposal(proj, path)
    problems = stale_pages(proj, out)
    assert f"{out}/requirements/OUT-001.md differs from a fresh build; run `make status` and commit it." in problems
    assert main(["--check", "wiki/generated"]) == 1
    assert "OUTCOME stale=3 recorded=0" in capsys.readouterr().out
