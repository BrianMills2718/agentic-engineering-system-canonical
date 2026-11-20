"""Anchored citations in `lockstep plan check`: `path#:~:text=<text>` names the text a citation points at."""

import json
from pathlib import Path

import pytest

from lockstep.citation_anchor import anchor_problem
from test_lockstep_plan_check import ENTRY, acceptance, run

CASES = json.loads((Path(__file__).parent / "fixtures/citation_anchor_cases.json").read_text())["cases"]
WORDS = {"ok": None, "not_found": "not found", "ambiguous": "matches", "malformed": "malformed"}
RECORD = "docs/planning/router/a1.recommendation.json"


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_shared_cases(case):
    problem = anchor_problem(case["file"], case["fragment"])
    if case["expect"] == "ok":
        assert problem is None
    else:
        assert problem and WORDS[case["expect"]] in problem


def check_with(tmp_path: Path, capsys, router_text: str, ref: str):
    entry = {**ENTRY, "representation": {"view": "table", "router_record": ref}}
    acceptance(tmp_path, [entry])
    (tmp_path / RECORD).write_text(router_text, encoding="utf-8")
    return run(tmp_path, capsys)


@pytest.mark.req("lockstep-plan-check/an-anchored-citation-survives-a-line-move")
def test_an_anchored_citation_survives_a_line_move(tmp_path, capsys):
    code, out = check_with(tmp_path, capsys, '{"a": 1,\n"b": "costs $1.04 here"}\n', RECORD + "#:~:text=costs%20%241.04")
    assert code == 0, out


@pytest.mark.req("lockstep-plan-check/an-anchored-citation-whose-text-is-gone-fails")
def test_an_anchored_citation_whose_text_is_gone_fails(tmp_path, capsys):
    code, out = check_with(tmp_path, capsys, '{"b": "costs $0.52"}', RECORD + "#:~:text=costs%20%241.04")
    assert code == 1 and "#:~:text=costs%20%241.04" in out and "not found" in out


@pytest.mark.req("lockstep-plan-check/text-found-twice-fails")
def test_text_found_twice_fails(tmp_path, capsys):
    code, out = check_with(tmp_path, capsys, '{"a": "cost 1", "b": "cost 1"}', RECORD + "#:~:text=cost%201")
    assert code == 1 and "matches 2 places" in out


@pytest.mark.req("lockstep-plan-check/a-malformed-anchor-fails-instead-of-being-skipped")
def test_a_malformed_anchor_fails_instead_of_being_skipped(tmp_path, capsys):
    code, out = check_with(tmp_path, capsys, "{}", RECORD + "#:~:text=")
    assert code == 1 and "malformed" in out


@pytest.mark.req("lockstep-plan-check/an-anchored-citation-whose-text-is-gone-fails")
def test_text_containing_a_url_scheme_is_still_an_anchor(tmp_path, capsys):
    code, out = check_with(tmp_path, capsys, "see http://x here", RECORD + "#:~:text=http://gone")
    assert code == 1 and "not found" in out


@pytest.mark.req("lockstep-plan-check/a-malformed-anchor-fails-instead-of-being-skipped")
@pytest.mark.parametrize("fragment", ["#:~:selector=foo", "#:~:TEXT=ok", "#:~:"])
def test_a_wrong_directive_fails_instead_of_being_skipped(tmp_path, capsys, fragment):
    code, out = check_with(tmp_path, capsys, "{}", RECORD + fragment)
    assert code == 1 and "malformed" in out
