import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import collect_feedback as CF  # noqa: E402


def _human(rid, quote):
    return {"id": rid, "field": "Human correction", "value": quote, "records": [{"id": "r-" + rid}]}


def test_human_corrections_file_once_per_distinct_quote(tmp_path):
    """The same instruction recurs across thousands of sessions; only one report per quote is filed,
    and a quote filed on an earlier night is not filed again."""
    (tmp_path / "reports-2026-11-09.jsonl").write_text(
        json.dumps(_human("rep-human-old", "Stop  and ask") | {"filing": "https://x/1"}) + "\n"
        + json.dumps(_human("rep-human-wait", "Use uv") | {"filing": "deferred_cap"}) + "\n")
    filed = CF.filed_human_quotes(tmp_path)
    assert filed == {"stop and ask"}  # a deferred report is not counted as filed
    reps = [_human("a", "Use uv"), _human("b", "use  UV"), _human("c", "stop and ask"), _human("d", "Merge it")]
    keep, dropped = CF.dedupe_human(reps, filed)
    assert [r["id"] for r in keep] == ["a", "d"]
    assert dropped == 2


class _Clock:
    def __init__(self):
        self.t = 0.0
        self.slept = []

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.slept.append(s)
        self.t += s


def test_pacer_holds_filing_to_the_hourly_limit():
    clock = _Clock()
    pacer = CF.HourlyPacer(3, clock=clock, sleep=clock.sleep)
    for _ in range(3):
        assert pacer.wait() == 0
        clock.t += 10  # each filing takes 10 s
    assert pacer.wait() == 3600 - 30  # the fourth waits for the hour that began at the first
    assert clock.slept == [3570]
    clock.t += 10
    assert pacer.wait() == 0  # a new window has room again


def test_pacer_never_waits_when_the_hour_has_passed_or_pacing_is_off():
    clock = _Clock()
    pacer = CF.HourlyPacer(2, clock=clock, sleep=clock.sleep)
    pacer.wait()
    pacer.wait()
    clock.t = 3600
    assert pacer.wait() == 0
    off = CF.HourlyPacer(0, clock=clock, sleep=clock.sleep)
    assert all(off.wait() == 0 for _ in range(1000))
    assert clock.slept == []


def test_default_cap_files_a_night_inside_the_unit_timeout():
    """900 reports at 450 an hour is two windows: about 71 minutes of filing at the measured 1.4 s an
    issue, inside the unit's 2-hour TimeoutStartSec, and never above GitHub's 500 an hour."""
    src = (Path(CF.__file__)).read_text()
    assert 'add_argument("--max-reports", type=int, default=900' in src
    assert 'add_argument("--reports-per-hour", type=int, default=450' in src
    per_hour, cap, secs_each = 450, 900, 1.4
    windows = -(-cap // per_hour)
    minutes = ((windows - 1) * 3600 + (cap - (windows - 1) * per_hour) * secs_each) / 60
    assert per_hour < 500 and minutes < 120


def test_human_corrections_file_before_other_reports_under_the_cap():
    """2026-11-11: 867 corrections were appended after 900 closeout and subagent reports, so the
    900-a-night cap deferred every one, every night (AES planning Q18, acceptance A6)."""
    other = [{"id": f"o{i}", "field": "Feedback"} for i in range(3)]
    human = [_human("h1", "Use uv"), _human("h2", "Merge it")]
    ordered = CF.filing_order(other + human)
    assert [r["id"] for r in ordered] == ["h1", "h2", "o0", "o1", "o2"]
    assert len(ordered[:2]) == 2 and all(r["field"] == "Human correction" for r in ordered[:2])
