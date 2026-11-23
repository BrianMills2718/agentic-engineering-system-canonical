import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import hub_page as h  # noqa: E402
import workspace_map as wm  # noqa: E402

NOW = dt.datetime(2026, 1, 2, 12, 0, tzinfo=dt.timezone.utc)
CFG = {
    "ssh_host_alias": "github-test",
    "github_accounts": {"someone": "gh-someone"},
    "git_identity": {"name": "Test", "email": "t@example.invalid"},
    "hub_page": {
        "repo": "someone/private-data", "data_branch": "shaping/hub-data",
        "site_url": "https://plans.example.invalid/hub/", "waiting_owners": ["someone"],
        "concern_repo": "someone/aes", "needs_human_label": "owner:person",
        "approvals_file": "/nonexistent/requirements.json",
        "quiet_units": {"pace.service": "owner said not a concern"},
        "quiet_issue_labels": {"source:pace": "owner said not a concern"},
        "quiet_concern_keys": {"pace": "owner said not a concern"},
        "fyi_rules": [{"name": "Records updates", "label": "source:records", "concern_key_prefix": "records-",
                       "title_prefix": "Records request "}],
        "shared_causes": [{"name": "Model credit used up", "why": "The model account is empty.",
                           "units": ["review.service", "page.service"], "issues": ["someone/meta#40"],
                           "concern_keys": ["credit-low"]}],
        "failures_file": "/nonexistent/failures.json",
        "links": [{"name": "Oversight page", "url": "https://plans.example.invalid/oversight/", "what": "rules"},
                  {"name": "Old front page", "url": "https://plans.example.invalid/front/", "what": "everything"}],
    },
}


def issue(number, title, labels=(), repo="someone/meta", key=""):
    return {"number": number, "title": title, "url": f"https://example.invalid/{repo}/{number}",
            "body": f"Text.\n\n<!-- concern-key: {key} -->\n" if key else "Text.",
            "updatedAt": f"2026-01-02T{number % 24:02d}:00:00Z", "repository": {"nameWithOwner": repo},
            "labels": [{"name": n} for n in ("waiting:person", *labels)]}


WAITING = [issue(7, "Pick a plan", repo="someone/proj"),
           issue(20, "Records request r1: records provided", ["source:records"]),
           issue(21, "Records request r2: denied", ["source:records"]),
           issue(22, "Records requests: 2 need you", ["source:other-records"]),  # an ask, not a status notice
           issue(23, "Records request r3: other", ["source:records"], repo="someone/root"),
           issue(30, "Timer job failed: backup.service", ["source:unit-watch"]),
           issue(40, "Model credit is used up", ["source:spend"]),
           issue(41, "Usage off track", ["source:pace"])]
FAILED = ("backup.service loaded failed failed Copy data to storage\n"
          "review.service loaded failed failed Review skills\n"
          "page.service   loaded failed failed Rebuild a page\n"
          "pace.service   loaded failed failed Weekly usage\n")
FAILURES = {"checked": "2026-01-02T11:00:00Z", "jobs": {
    "backup.service": {"unit": "backup.service", "reason": "The source folder was missing.", "first_failed": "2026-01-01",
                       "issue_url": "https://example.invalid/someone/meta/30"},
    "review.service": {"unit": "review.service", "reason": "The request needed more credits.", "first_failed": "2026-01-02",
                       "issue_url": ""}}}
CONCERNS = [{"number": 3, "title": "Gate is red", "url": "https://example.invalid/a/3", "updatedAt": "2026-01-01T00:00:00Z"}]
MERGED = [{"number": 9, "title": "Slice one", "url": "https://example.invalid/p/9", "mergedAt": "2026-01-02T09:00:00Z"}]
APPROVALS = {"generated": "2026-01-01T00:00:00Z", "repos": [
    {"repo": "proj", "items": [{"id": "a/one", "title": "One", "source": "inferred"},
                               {"id": "a/two", "title": "Two", "source": "brian"}]},
    {"repo": "proj-copy", "items": [{"id": "a/one", "title": "One", "source": "inferred"}]}]}


class FakeRun:
    """Answers each command by its step name; a name in `fail` exits 1."""

    def __init__(self, fail=(), labels=("owner:person",)):
        self.fail, self.labels, self.calls = set(fail), labels, []

    def log(self, text):
        pass

    def __call__(self, name, cmd, cwd=None, timeout=120):
        self.calls.append((name, cmd))
        if name in self.fail or any(name.startswith(f) for f in self.fail):
            return subprocess.CompletedProcess(cmd, 1, "", "boom")
        out = {"failed-units": FAILED, "concerns": json.dumps(CONCERNS), "merged": json.dumps(MERGED),
               "concern-labels": json.dumps([{"name": n} for n in self.labels])}.get(name)
        if name.startswith("waiting-"):
            out = json.dumps(WAITING)
        return subprocess.CompletedProcess(cmd, 0, out or "", "")


def approvals(_s):
    rec = h.parse_approvals(APPROVALS)
    return rec, h.source("Approvals waiting (oversight data)", True, count=rec["count"])


def failures(_s):
    return {"checked": FAILURES["checked"], "jobs": FAILURES["jobs"]}, h.source("Failure reasons (failing-jobs page)", True, count=2)


def failures_unread(_s):
    return None, h.source("Failure reasons (failing-jobs page)", False, "failures.json could not be read")


def build(run=None, previous=None, read_failures_=failures):
    return h.build_record(h.settings(CFG), run or FakeRun(), NOW, previous, read_approvals_=approvals,
                          read_failures_=read_failures_)


def needs_keys(rec):
    return sorted(i["key"] for g in rec["needs_you"].values() for i in g or [])


@pytest.mark.req("hub-page/needs-you-comes-first")
def test_needs_you_is_the_first_section_and_lists_only_what_waits():
    rec = build()
    page = h.render(rec, h.settings(CFG))
    assert page.index('id="needs"') < page.index('id="broken"') < page.index('id="fyi"') < page.index('id="changed"') \
        < page.index('id="sources"') < page.index('id="approvals"')
    # one decision, the records ask (no fyi rule matches it), one concern; nothing else
    assert needs_keys(rec) == ["issue:someone/aes#3", "issue:someone/meta#22", "issue:someone/proj#7"]
    assert rec["needs_you_total"] == 3
    needs = page[page.index('id="needs"'):page.index('id="broken"')]
    assert "Pick a plan" in needs and "Gate is red" in needs and "Records requests: 2 need you" in needs
    assert "backup.service" not in needs and "Records request r1" not in needs
    assert "someone/meta#41</a> (owner said not a concern)" in needs  # a quiet label: shown with its reason, not counted
    assert "Rebuilt only when someone runs it." in page
    assert "Rebuilt every hour." in h.render(rec, {**h.settings(CFG), "refresh": "every hour"})


@pytest.mark.req("hub-page/needs-you-comes-first")
def test_every_colour_comes_with_a_word_and_the_page_fits_a_phone():
    page = h.render(build(), h.settings(CFG))
    assert 'name="viewport"' in page and "max-width:760px" in page
    assert "green" not in page.lower() and "red" not in h.STYLE
    for tag in ('<span class="tag orange">Waiting</span>', '<span class="tag blue">Read</span>',
                '<span class="tag orange">Failing</span>', '<span class="tag grey">FYI</span>', '<span class="tag grey">Count only</span>'):
        assert tag in page


@pytest.mark.req("hub-page/an-unread-source-is-not-checked")
def test_a_source_that_cannot_be_read_is_not_checked_never_zero():
    rec = build(FakeRun(fail={"failed-units", "waiting-"}))
    page = h.render(rec, h.settings(CFG))
    assert rec["broken"] is None and rec["needs_you"]["decisions"] is None and rec["fyi"] is None
    assert "Not checked</span> Broken services" in page and "Broken services (0" not in page
    assert "Not checked</span> FYI: records updates" in page
    assert "1 source not checked" in page  # of Needs you's two sources, the issue search


@pytest.mark.req("hub-page/an-unread-source-is-not-checked")
def test_unread_failure_reasons_are_not_checked_and_the_services_still_show():
    rec = build(read_failures_=failures_unread)
    page = h.render(rec, h.settings(CFG))
    assert rec["broken_total"] == 3
    assert "Reason not checked: the failing-jobs page was not read." in page


@pytest.mark.req("hub-page/an-unread-source-is-not-checked")
def test_a_missing_label_is_reported_not_read_as_none():
    rec = build(FakeRun(labels=("owner:agent",)))
    src = next(x for x in rec["sources"] if x["name"].startswith("AES concerns"))
    assert not src["ok"] and "does not exist" in src["error"]
    assert rec["needs_you"]["concerns"] is None


@pytest.mark.req("hub-page/what-changed-since-the-last-run")
def test_what_changed_names_new_and_cleared_items():
    previous = build()
    previous["tracked"] = [i for i in previous["tracked"] if i["key"] != "unit:backup.service"]
    previous["tracked"].append({"key": "unit:old.service", "title": "old.service", "where": "", "url": "", "updated": "",
                                "group": "failed", "source": "Failed services (systemctl)"})
    previous["seen"] = [i["key"] for i in previous["tracked"]]
    rec = build(previous=json.loads(json.dumps(previous)))
    assert [i["key"] for i in rec["changed"]["new"]] == ["unit:backup.service"]
    assert [i["key"] for i in rec["changed"]["cleared"]] == ["unit:old.service"]
    page = h.render(rec, h.settings(CFG))
    assert "Cleared items (1)" in page and "#9 Slice one" in page


@pytest.mark.req("hub-page/what-changed-since-the-last-run")
def test_an_unread_source_is_never_shown_as_cleared():
    previous = build()
    rec = build(FakeRun(fail={"failed-units"}), previous=json.loads(json.dumps(previous)))
    assert rec["changed"]["cleared"] == []
    assert h.changes(None, rec, {})["compared"] is False


@pytest.mark.req("hub-page/links-to-each-source-page")
def test_each_configured_source_page_is_linked():
    page = h.render(build(), h.settings(CFG))
    for link in CFG["hub_page"]["links"]:
        assert f'href="{link["url"]}"' in page


@pytest.mark.req("hub-page/page-goes-to-a-private-data-branch")
def test_settings_name_the_private_branch_and_a_missing_one_stops():
    s = h.settings(CFG)
    assert s["remote"] == "git@github-test:someone/private-data.git" and s["data_branch"] == "shaping/hub-data"
    broken = {**CFG, "hub_page": {k: v for k, v in CFG["hub_page"].items() if k != "repo"}}
    with pytest.raises(wm.ConfigMissing, match="repo"):
        h.settings(broken)


@pytest.mark.req("hub-page/page-goes-to-a-private-data-branch")
def test_publish_pushes_only_to_the_data_branch(tmp_path):
    run = FakeRun()
    run_diff_changed = run.__call__

    def fake(name, cmd, cwd=None, timeout=120):
        out = run_diff_changed(name, cmd, cwd, timeout)
        return subprocess.CompletedProcess(cmd, 1, "", "") if name == "diff-data" else out

    fake.log = run.log
    assert h.publish(fake, tmp_path, h.settings(CFG), "2026-01-02 12:00")
    push = next(cmd for name, cmd in run.calls if name == "push-data")
    assert push[-1] == "HEAD:refs/heads/shaping/hub-data"
    assert not any("main" in str(c) for _, cmd in run.calls for c in cmd)


@pytest.mark.req("hub-page/what-changed-since-the-last-run")
def test_an_item_that_only_moved_section_is_neither_new_nor_cleared():
    # a record from before the split: every failed unit and every waiting issue sat under Needs you
    rec_now = build()
    gs = rec_now["group_sources"]
    old = {"built": "2026-01-02T11:00+00:00", "sources": rec_now["sources"],
           "group_sources": {"decisions": gs["decisions"], "failed": gs["failed"], "concerns": gs["concerns"]},
           "needs_you": {"decisions": h.parse_issues(json.dumps(WAITING)),
                         "failed": h.parse_failed_units(FAILED, CFG["hub_page"]["quiet_units"])[0],
                         "concerns": rec_now["needs_you"]["concerns"]}}
    rec = build(previous=json.loads(json.dumps(old)))
    assert rec["changed"]["compared"] and rec["changed"]["new"] == [] and rec["changed"]["cleared"] == []


@pytest.mark.req("hub-page/broken-services-grouped-by-cause")
def test_failed_services_are_grouped_by_cause_and_not_counted_under_needs_you():
    rec = build()
    page = h.render(rec, h.settings(CFG))
    assert rec["broken_total"] == 3  # the quiet unit is not counted here either
    causes = {c["name"]: c for c in rec["broken"]}
    shared = causes["Model credit used up"]
    assert [u["title"] for u in shared["units"]] == ["review.service", "page.service"]
    assert [i["where"] for i in shared["issues"]] == ["someone/meta#40"]
    assert [i["where"] for i in causes["backup.service"]["issues"]] == ["someone/meta#30"]
    broken = page[page.index('id="broken"'):page.index('id="fyi"')]
    assert "Broken services (3 services, 2 causes)" in broken
    assert "Model credit used up: 2 services share one cause" in broken
    assert "The source folder was missing. Failing since 2026-01-01." in broken
    assert "Reason not on the failing-jobs page yet." in broken  # page.service has no row there
    assert "pace.service (owner said not a concern)" in broken


@pytest.mark.req("hub-page/broken-services-grouped-by-cause")
def test_an_issue_that_belongs_to_a_service_is_listed_once():
    rec = build()
    page = h.render(rec, h.settings(CFG))
    assert "issue:someone/meta#30" not in needs_keys(rec) and "issue:someone/meta#40" not in needs_keys(rec)
    assert page.count('href="https://example.invalid/someone/meta/30"') == 1
    assert page.count('href="https://example.invalid/someone/meta/40"') == 1
    # a shared cause none of whose units or issues is present is not shown
    s = {**h.settings(CFG), "shared_causes": [{"name": "Gone", "units": ["none.service"], "issues": ["x/y#1"]}]}
    assert all(c["name"] != "Gone" for c in h.build_record(s, FakeRun(), NOW, None, approvals, failures)["broken"])


@pytest.mark.req("hub-page/records-updates-are-for-information")
def test_records_status_notices_go_to_fyi_by_label_and_title_prefix():
    rec = build()
    page = h.render(rec, h.settings(CFG))
    groups = {(g["label"], g["repo"]): [i["where"] for i in g["items"]] for g in rec["fyi"]}
    assert groups == {("source:records", "someone/meta"): ["someone/meta#21", "someone/meta#20"],
                      ("source:records", "someone/root"): ["someone/root#23"]}
    fyi = page[page.index('id="fyi"'):page.index('id="changed"')]
    assert "FYI: records updates (3)" in fyi and 'title starting &quot;Records request &quot;' in fyi
    assert "Records updates from someone/root, label source:records (1)" in fyi
    assert "Records requests: 2 need you" not in fyi


@pytest.mark.req("hub-page/approvals-are-a-footer-count")
def test_approvals_are_a_footer_count_with_no_significance_field():
    rec = build()
    page = h.render(rec, h.settings(CFG))
    footer = page[page.index('id="approvals"'):]
    assert "Approvals waiting: 1 requirements" in footer  # a/one counted once across two checkouts; a/two has a source
    assert "Not shown: no significance field" in footer
    assert "One</" not in page and "approval:" not in json.dumps(rec["needs_you"])
    assert 'href="https://plans.example.invalid/oversight/"' in footer


MOVED = [issue(50, "Records request r9: denied", repo="someone/new", key="records-r9"),
         issue(51, "Timer job failed: backup.service", repo="someone/new", key="failed-unit:backup.service"),
         issue(52, "Model credit is low", repo="someone/new", key="credit-low"),
         issue(53, "Usage off track", repo="someone/new", key="pace"),
         issue(54, "Records requests: 1 email matches none", repo="someone/new", key="records-unmatched")]


@pytest.mark.req("hub-page/broken-services-grouped-by-cause")
@pytest.mark.req("hub-page/records-updates-are-for-information")
@pytest.mark.req("hub-page/moved-issues-are-matched-by-concern-key")
def test_issues_moved_to_another_repository_are_sorted_by_their_concern_key():
    class Moved(FakeRun):
        def __call__(self, name, cmd, cwd=None, timeout=120):
            out = super().__call__(name, cmd, cwd, timeout)
            return subprocess.CompletedProcess(cmd, 0, json.dumps(MOVED), "") if name.startswith("waiting-") else out

    rec = build(Moved())
    assert needs_keys(rec) == ["issue:someone/aes#3", "issue:someone/new#54"]  # the ask stays: its title has no prefix
    assert [i["where"] for i in rec["quiet_issues"]] == ["someone/new#53"]
    assert [i["where"] for g in rec["fyi"] for i in g["items"]] == ["someone/new#50"]
    causes = {c["name"]: c for c in rec["broken"]}
    assert [i["where"] for i in causes["backup.service"]["issues"]] == ["someone/new#51"]
    assert [i["where"] for i in causes["Model credit used up"]["issues"]] == ["someone/new#52"]
    assert h.parse_issues(json.dumps([issue(1, "x")]))[0]["concern_key"] == ""


@pytest.mark.req("hub-page/agent-work-is-not-needs-you")
def test_an_issue_an_agent_owns_goes_to_agent_work_not_needs_you():
    agent = issue(60, "Wire the new check", ["owner:agent"], repo="someone/proj")

    class WithAgent(FakeRun):
        def __call__(self, name, cmd, cwd=None, timeout=120):
            out = super().__call__(name, cmd, cwd, timeout)
            return subprocess.CompletedProcess(cmd, 0, json.dumps(WAITING + [agent]), "") if name.startswith("waiting-") else out

    before = h.build_record(h.settings(CFG), WithAgent(), NOW, None, approvals, failures)
    assert "issue:someone/proj#60" in needs_keys(before)  # without the setting nothing changes
    cfg = {**CFG, "hub_page": {**CFG["hub_page"], "agent_labels": {"owner:agent": "an agent owns the next step"}}}
    s = h.settings(cfg)
    rec = h.build_record(s, WithAgent(), NOW, before, approvals, failures)
    assert "issue:someone/proj#60" not in needs_keys(rec)
    assert rec["needs_you_total"] == before["needs_you_total"] - 1
    assert [(i["where"], i["reason"]) for i in rec["agent_work"]] == [("someone/proj#60", "an agent owns the next step")]
    assert "issue:someone/proj#60" in rec["seen"] and rec["changed"]["cleared"] == []
    page = h.render(rec, s)
    assert page.index('id="broken"') < page.index('id="agent"') < page.index('id="fyi"')
    section = page[page.index('id="agent"'):page.index('id="fyi"')]
    assert "Agent work (1)" in section and "Wire the new check" in section and "an agent owns the next step" in section
    needs = page[page.index('id="needs"'):page.index('id="broken"')]
    assert "Wire the new check" not in needs
