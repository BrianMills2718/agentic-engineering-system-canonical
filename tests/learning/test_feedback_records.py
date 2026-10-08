"""feedback-report.v1 parsing: the plan's canonical example and its negative controls
(proposals/aes-learning-loop/PLAN.md, "Fixtures")."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import records as R  # noqa: E402

PROV = R.Provenance(client="claude", session_id="3b596c23", turn_offset=1200, ts="2026-10-07T22:10:00Z")

STRANDED = """\
- obs: ten learnings lanes left their entries uncommitted [~/projects/data/learnings/file9.log:41] [BrianMills2718/project-meta#2431]  expected: each lane commits its entry
- obs (control): the commit rule refused the [Discovery] tag on every lane [`3f9c2ab`]
- claim (inferred, high, supported): the commit rule refusing the [Discovery] tag stranded the lanes  ← obs 1, obs 2
- action (Prevent, done): fall back to a detached append when a lane step fails → https://github.com/BrianMills2718/project-meta/pull/2442
"""


def test_canonical_example_parses_into_linked_records():
    recs, rest = R.parse_feedback(STRANDED, PROV)
    assert rest == []
    assert [r.kind for r in recs] == ["observation", "observation", "claim", "action"]
    o1, o2, claim, action = recs
    assert {lk.ref for lk in o1.links} == {"~/projects/data/learnings/file9.log:41", "BrianMills2718/project-meta#2431"}
    assert o1.expected == "each lane commits its entry"
    assert o1.text == "ten learnings lanes left their entries uncommitted"
    assert o2.text == "the commit rule refused the [Discovery] tag on every lane"
    assert o1.subject_kind == "work" and o2.subject_kind == "control"
    assert [lk.ref for lk in o2.links] == ["3f9c2ab"]
    assert (claim.basis, claim.confidence, claim.evidence_word) == ("inferred", "high", "supported")
    assert claim.supports == [o1.id, o2.id]
    assert not claim.unprovenanced  # provenanced through the observations it rests on
    assert (action.intent, action.status) == ("Prevent", "done")
    assert [lk.ref for lk in action.result] == ["https://github.com/BrianMills2718/project-meta/pull/2442"]
    assert all(not r.unprovenanced for r in recs)
    assert len({r.id for r in recs}) == 4
    assert all(r.provenance.session_id == "3b596c23" and r.provenance.line for r in recs)


def test_line_without_link_is_unprovenanced():
    recs, _ = R.parse_feedback("- obs: the build felt slow today", PROV)
    assert recs[0].unprovenanced and recs[0].links == []


def test_guessed_claim_keeps_its_basis():
    recs, _ = R.parse_feedback("- claim (guessed, low): my time limit caused it", PROV)
    assert recs[0].basis == "guessed" and recs[0].unprovenanced


def test_unmarked_lines_are_left_for_the_light_model():
    text = "Filed [#236](https://github.com/BrianMills2718/agentic-engineering-system-canonical/issues/236) (lanes).\n- obs: x [a/b.py:3]"
    recs, rest = R.parse_feedback(text, PROV)
    assert [r.kind for r in recs] == ["observation"]
    assert rest == [text.splitlines()[0]]


def test_link_finder_reads_identifiers_not_prose():
    links = R.find_links("see [the log](scripts/x.py:12), #44, owner/repo#9, `abcdef1` and https://e.com/a")
    assert [(lk.kind, lk.ref) for lk in links] == [
        ("path", "scripts/x.py:12"), ("url", "https://e.com/a"), ("issue", "#44"), ("issue", "owner/repo#9"),
        ("commit", "abcdef1")]
    assert R.find_links("nothing to see here, version 1.2 and e.g. this") == []
    assert [lk.ref for lk in R.find_links("refused at [Makefile:96] and README.md:12-14")] == ["Makefile:96", "README.md:12-14"]
    assert R.find_links("met at 12:30, ratio 3:1") == []
    md = R.find_links("Filed [#195](https://github.com/o/r/issues/195), a lesson")
    assert [lk.ref for lk in md] == ["https://github.com/o/r/issues/195"]


def test_record_ids_are_stable_and_distinct_per_session():
    a, _ = R.parse_feedback("- obs: same text [a/b.py]", PROV)
    b, _ = R.parse_feedback("- obs: same text [a/b.py]", PROV)
    c, _ = R.parse_feedback("- obs: same text [a/b.py]", PROV.model_copy(update={"session_id": "other"}))
    assert a[0].id == b[0].id != c[0].id


def test_free_text_records_take_the_nearest_link_in_their_sentence():
    import feedback_log as FL
    note = ("Filed [#236](https://github.com/o/r/issues/236) (one lane per session reopens lanes) and "
            "[#237](https://github.com/o/r/issues/237) (the goal text has no length check). Nothing else.")
    assert [lk.ref for lk in FL.sentence_links(note, "one lane per session reopens lanes")] == [
        "https://github.com/o/r/issues/236"]
    assert [lk.ref for lk in FL.sentence_links(note, "the goal text has no length check")] == [
        "https://github.com/o/r/issues/237"]
    assert FL.sentence_links(note, "Nothing else") == []


def test_published_schema_matches_the_model():
    import json
    path = Path(__file__).resolve().parents[2] / "contracts/learning-loop/feedback-report.v1.schema.json"
    assert json.loads(path.read_text()) == json.loads(json.dumps(R.Record.model_json_schema(), sort_keys=True)), \
        "regenerate contracts/learning-loop/feedback-report.v1.schema.json from records.Record"


def test_bare_issue_numbers_take_the_session_repo_and_url_duplicates_drop():
    links = R.find_links("tags [#300](https://github.com/o/r/issues/300) and #300, also #12")
    assert [lk.ref for lk in R.normalize_links(links, "o/r")] == ["https://github.com/o/r/issues/300", "o/r#12"]
    assert [lk.ref for lk in R.normalize_links(R.find_links("see #12"), "")] == ["#12"]
    recs, _ = R.parse_feedback("- obs: refused again [#7]", PROV, "BrianMills2718/aes")
    assert [lk.ref for lk in recs[0].links] == ["BrianMills2718/aes#7"]


def test_legacy_register_ids_are_links():
    links = R.find_links("recorded as `lrn-20261006T050845618039Z-ae28bc755c`")
    assert [(lk.kind, lk.ref) for lk in links] == [("entry", "lrn-20261006T050845618039Z-ae28bc755c")]


def test_transcript_turns_carry_the_session_folder(tmp_path):
    import json
    import transcripts as T
    p = tmp_path / "s.jsonl"
    p.write_text(json.dumps({"type": "assistant", "sessionId": "s1", "cwd": "/w/repo", "timestamp": "2026-10-08T00:00:00Z",
                             "message": {"content": [{"type": "text", "text": "hi"}]}}) + "\n")
    t = T.read_transcript(p, "claude")
    assert [(x.role, x.cwd) for x in t.turns] == [("agent", "/w/repo")]
