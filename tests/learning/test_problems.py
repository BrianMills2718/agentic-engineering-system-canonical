"""S3 recurrence rule: independent observations with links; echoes of the same evidence count once."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import problems as PB  # noqa: E402


def rec(kind, session, links, basis=None):
    verified = [{"kind": k, "ref": r} for k, r in links]
    return {"kind": kind, "session": session, "day": "2026-10-08", "basis": basis, "unprovenanced": not links,
            "links": verified, "resolved_links": verified}


def test_two_sessions_seeing_different_evidence_are_two_sightings():
    m = [rec("observation", "s1", [("path", "a.log:3")]), rec("observation", "s2", [("path", "b.log:9")])]
    assert len(PB.sightings(m)) == 2


def test_a_second_session_citing_the_same_issue_is_an_echo():
    m = [rec("observation", "s1", [("issue", "o/r#316")]),
         rec("observation", "s2", [("url", "https://github.com/o/r/issues/316")])]
    assert len(PB.sightings(m)) == 1


def test_claims_actions_and_unlinked_observations_are_not_sightings():
    m = [rec("claim", "s1", [("path", "a.log:3")], "inferred"), rec("action", "s2", [("path", "b.log")]),
         rec("observation", "s3", []), rec("observation", "s4", [("path", "c.log:1")])]
    assert len(PB.sightings(m)) == 1


def test_group_joins_transitively():
    assert sorted(PB.group(5, [(0, 1), (1, 2), (3, 4)])) == [[0, 1, 2], [3, 4]]


def test_same_issue_number_in_different_repositories_is_independent():
    m = [rec("observation", "s1", [("issue", "o/one#316")]),
         rec("observation", "s2", [("url", "https://github.com/o/two/issues/316")])]
    assert len(PB.sightings(m)) == 2


def test_a_syntactic_but_unresolved_link_never_counts():
    r = rec("observation", "s1", [("issue", "o/r#999")])
    r["resolved_links"] = []
    assert PB.sightings([r]) == []


def test_effect_split_uses_sightings_after_enforcement(monkeypatch):
    before = rec("observation", "s1", [("path", "a.log:3")]); before["day"] = "2026-10-01"
    after = rec("observation", "s9", [("path", "z.log:1")]); after["day"] = "2026-10-20"
    members = [before, after]
    assert len(PB.sightings([r for r in members if r["day"] >= "2026-10-10"])) == 1
    assert len(PB.sightings([r for r in members if r["day"] < "2026-10-10"])) == 1
