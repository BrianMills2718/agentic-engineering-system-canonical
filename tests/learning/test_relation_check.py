"""S2 scoring rules: acceptable answers fixed with the labels, and the parity rule."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import relation_check as RC  # noqa: E402

PAIRS = [{"pair_id": "p1", "label": "supports", "acceptable": ["supports", "same_problem"]},
         {"pair_id": "p2", "label": "unrelated", "acceptable": ["unrelated"]},
         {"pair_id": "p3", "label": "same_problem"}]


def test_score_counts_any_acceptable_answer_and_reports_the_misses():
    r = RC.score(PAIRS, [{"pair_id": "p1", "relation": "same_problem"}, {"pair_id": "p2", "relation": "supports"},
                         {"pair_id": "p3", "relation": "same_problem"}])
    assert (r["correct"], r["n"], r["meets_bar"]) == (2, 3, False)
    assert [w["pair_id"] for w in r["wrong"]] == ["p2"]


def test_a_judge_that_fails_any_pair_is_out_not_scored():
    r = RC.score(PAIRS, [{"pair_id": "p1", "relation": "supports"}, {"pair_id": "p2", "relation": None},
                         {"pair_id": "p3", "relation": "same_problem"}])
    assert r["status"].startswith("out")
