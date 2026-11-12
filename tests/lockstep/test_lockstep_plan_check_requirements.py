"""`lockstep plan check`, requirement coverage: the offline checks of a stored judgment.

Ported from company-planning at b8a53a0: tests/test_goal_coverage.py (`_judged`, the gap table, the quote tests,
the deferral test, the stale and pending tests).
"""

import json
from pathlib import Path

import pytest

from lockstep.plan_check import plan_cli, quote_in_words, requirement_problems
from test_lockstep_plan_check import ENTRY, acceptance, run


def judged(**mapping: object) -> dict:
    """An acceptance record whose one requirement ("map") is mapped as given."""
    m = {"requirement_id": "R1", "covered_by": ["A1"], "coverage_reason": "why", "extent": "full",
         "missing": "", "deferral": 0, "in_outcome": True, "outcome_reason": "why"}
    m.update(mapping)
    return {"outcome": "staff look up any store",
            "asked_by": [{"who": "Brian", "date": "2026-10-28", "words": "a shared map of every store", "source": "s"}],
            "coverage": {"requirements": [{"id": "R1", "requirement": "map", "quote": "map", "asked_by_index": 1,
                                           "kind": "outcome"}], "mappings": [m]}}


def stamped(record: dict) -> dict:
    """Give the stored judgment the hashes it would carry, so it is current."""
    from lockstep.plan_check import hashes
    record["coverage"].update(hashes({**record, "entries": [ENTRY]}))
    return record


def problems_of(record: dict) -> list[str]:
    record = stamped(record) if "asked_by_sha256" not in record.get("coverage", {}) else record
    return requirement_problems({**record, "entries": [ENTRY]})[0]


@pytest.mark.req("lockstep-plan-check/a-covered-requirement-passes")
def test_a_covered_requirement_passes(tmp_path, capsys):
    acceptance(tmp_path, [ENTRY], **stamped(judged()))
    code, out = run(tmp_path, capsys)
    assert code == 0, out
    assert "1 requirements: 1 covered, 0 deferred, 0 about the planning process" in out


@pytest.mark.req("lockstep-plan-check/a-gap-in-coverage-fails")
@pytest.mark.parametrize("mapping, expected", [
    ({"covered_by": [], "extent": "none"}, 'R1 "map": uncovered'),
    ({"covered_by": ["A9"]}, "criteria that do not exist: A9"),
    ({"extent": "partial", "missing": "printing"}, "only partly covered by A1; no criterion asks for printing"),
    ({"in_outcome": False, "outcome_reason": "says look up"}, "the outcome line drops it (says look up)"),
    ({"covered_by": [], "extent": "none", "deferral": 1}, "not a recorded deferral in Brian's own words"),
])
def test_a_gap_in_coverage_fails(mapping, expected):
    assert any(expected in p for p in problems_of(judged(**mapping))), problems_of(judged(**mapping))


def test_an_unmapped_or_duplicated_requirement_fails():
    record = judged()
    record["coverage"]["mappings"] = []
    assert any("exactly one mapping" in p for p in problems_of(record))
    record = judged()
    record["coverage"]["requirements"].append(dict(record["coverage"]["requirements"][0]))
    assert any("unique" in p for p in problems_of(record))


def test_a_process_requirement_needs_no_criterion():
    record = judged(covered_by=[], extent="none")
    record["coverage"]["requirements"][0]["kind"] = "process"
    assert problems_of(stamped(record)) == []


def test_a_malformed_judgment_is_a_problem_not_a_crash(tmp_path, capsys):
    acceptance(tmp_path, [ENTRY], **{**judged(), "coverage": "yes"})
    code, out = run(tmp_path, capsys)
    assert code == 1 and "coverage must be an object" in out, out
    record = judged()
    record["coverage"]["requirements"] = [3]
    assert any("not an object" in p for p in problems_of(record))


@pytest.mark.req("lockstep-plan-check/an-invented-quote-fails-and-a-re-spelled-typo-passes")
def test_an_invented_quote_fails():
    record = judged()
    record["coverage"]["requirements"][0]["quote"] = "a map with filters"
    assert any("not in Brian's words" in p for p in problems_of(record))


# Brian's recorded words with his typos (company-planning tests/test_goal_coverage.py, lockstep quotes 7 and 8).
WORDS = ["after we buildl lockstep we will get th eproject brains to use it as a consumer. lockstep is meant to be "
         "part of aes canonical. includes how the current status part from the code side is projected up itnto the "
         "normative docuemtnation and how everything needs to be linked together",
         "one other bet re lockstep that is improtant is that the key idea with drift is putting the docuemtnation "
         "next to what is edited."]


@pytest.mark.req("lockstep-plan-check/an-invented-quote-fails-and-a-re-spelled-typo-passes")
@pytest.mark.parametrize("quote, index", [
    ("the current status part from the code side is projected up itnto the normative docuemntation", 1),
    ("the current status part from the code side is projected up into the normative documentation", 1),
    ("the key idea with drift is putting the docuemtnation next to what is edited", 2),
    ("lockstep is meant to be part of aes canonical", 1),
])
def test_a_respelled_typo_passes(quote, index):
    assert quote_in_words(quote, WORDS[index - 1])


@pytest.mark.req("lockstep-plan-check/an-invented-quote-fails-and-a-re-spelled-typo-passes")
@pytest.mark.parametrize("quote, index", [
    ("the current status part from the code side is projected down into the normative docuemtnation", 1),
    ("the key idea with drift is putting the docuemtnation next to what is reviewed", 2),
    ("how everything needs to be unlinked together", 1),
    ("the key idea with drift is putting the docuemtnation right next to what is edited", 2),
    ("the key idea with drift is putting the docuemntation next to what is edited", 1),
    ("projected up itnto the normativ docuemntation", 1),
])
def test_a_changed_or_added_word_still_fails(quote, index):
    assert not quote_in_words(quote, WORDS[index - 1])


@pytest.mark.req("lockstep-plan-check/a-deferral-in-brian-s-words-counts")
def test_a_deferral_in_brians_words_counts(tmp_path, capsys):
    record = judged(covered_by=[], extent="none", deferral=1)
    record["deferred"] = [{"requirement": "map", "who": "Brian", "date": "2026-10-28",
                           "words": "skip the map for now", "source": "session"}]
    acceptance(tmp_path, [ENTRY], **stamped(record))
    code, out = run(tmp_path, capsys)
    assert code == 0 and "1 deferred" in out, out


@pytest.mark.req("lockstep-plan-check/a-stale-or-missing-judgment-is-reported")
def test_a_stale_or_missing_judgment_is_reported(tmp_path, capsys):
    record = stamped(judged())
    record["asked_by"][0]["words"] += " and print it"
    acceptance(tmp_path, [ENTRY], **record)
    code, out = run(tmp_path, capsys)
    assert code == 1 and "stale" in out and "asked_by words changed" in out, out

    record = stamped(judged())
    record["outcome"] = "staff look up one store"
    acceptance(tmp_path, [ENTRY], **record)
    code, out = run(tmp_path, capsys)
    assert code == 1 and "the outcome line changed" in out, out

    record = judged()
    del record["coverage"]
    acceptance(tmp_path, [ENTRY], **record)
    code, out = run(tmp_path, capsys)
    assert code == 1 and "no stored coverage judgment" in out, out

    record = stamped(judged())
    acceptance(tmp_path, [ENTRY, {**ENTRY, "id": "A2", "criterion": "I can see the invoices page."}], **record)
    code, out = run(tmp_path, capsys)
    assert code == 0 and "pending" in out and "re-judge" in out, out

    record = stamped(judged())
    acceptance(tmp_path, [{**ENTRY, "id": "A2"}], **record)   # A1, which the judgment relied on, was removed
    code, out = run(tmp_path, capsys)
    assert code == 1 and "criteria removed since it was judged: A1" in out, out


@pytest.mark.req("lockstep-plan-check/a-file-without-brian-s-words-skips-the-requirement-check")
def test_a_file_without_brians_words_skips_the_requirement_check(tmp_path, capsys):
    acceptance(tmp_path, [ENTRY])
    code, out = run(tmp_path, capsys)
    assert code == 0 and "requirements: skipped (no asked_by" in out, out
    data = json.loads(run(tmp_path, capsys, "--json")[1])
    assert data["requirements"]["checked"] is False


def test_needs_review_fails():
    record = judged()
    record["coverage"]["needs_review"] = True
    assert any("needs_review" in p for p in problems_of(record))
