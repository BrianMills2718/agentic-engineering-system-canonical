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
        "links": [{"name": "Oversight page", "url": "https://plans.example.invalid/oversight/", "what": "rules"},
                  {"name": "Old front page", "url": "https://plans.example.invalid/front/", "what": "everything"}],
    },
}
WAITING = [{"number": 7, "title": "Pick a plan", "url": "https://example.invalid/i/7", "updatedAt": "2026-01-02T10:00:00Z",
            "repository": {"name": "proj", "nameWithOwner": "someone/proj"}}]
FAILED = ("backup.service loaded failed failed Copy data to storage\n"
          "pace.service   loaded failed failed Weekly usage\n")
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


def build(run=None, previous=None):
    return h.build_record(h.settings(CFG), run or FakeRun(), NOW, previous, read_approvals_=approvals)


@pytest.mark.req("hub-page/needs-you-comes-first")
def test_needs_you_is_the_first_section_and_lists_only_what_waits():
    rec = build()
    page = h.render(rec, h.settings(CFG))
    assert page.index('id="needs"') < page.index('id="changed"') < page.index('id="sources"')
    assert rec["needs_you_total"] == 3  # one decision, one failed service (the quiet one is not counted), one concern
    assert "Pick a plan" in page and "backup.service" in page and "Gate is red" in page
    assert "pace.service (owner said not a concern)" in page
    assert "Approvals waiting (1)" in page  # a/one counted once across two checkouts; a/two has a source
    assert "Rebuilt only when someone runs it." in page
    assert "Rebuilt every hour." in h.render(rec, {**h.settings(CFG), "refresh": "every hour"})


@pytest.mark.req("hub-page/needs-you-comes-first")
def test_every_colour_comes_with_a_word_and_the_page_fits_a_phone():
    page = h.render(build(), h.settings(CFG))
    assert 'name="viewport"' in page and "max-width:760px" in page
    assert "green" not in page.lower() and "red" not in h.STYLE
    for tag in ('<span class="tag orange">Waiting</span>', '<span class="tag blue">Read</span>'):
        assert tag in page


@pytest.mark.req("hub-page/an-unread-source-is-not-checked")
def test_a_source_that_cannot_be_read_is_not_checked_never_zero():
    rec = build(FakeRun(fail={"failed-units", "waiting-"}))
    page = h.render(rec, h.settings(CFG))
    assert rec["needs_you"]["failed"] is None and rec["needs_you"]["decisions"] is None
    assert "Not checked</span> Failed services" in page and "Failed services (0)" not in page
    assert "2 sources not checked" in page


@pytest.mark.req("hub-page/an-unread-source-is-not-checked")
def test_a_missing_label_is_reported_not_read_as_none():
    rec = build(FakeRun(labels=("owner:agent",)))
    src = next(x for x in rec["sources"] if x["name"].startswith("AES concerns"))
    assert not src["ok"] and "does not exist" in src["error"]
    assert rec["needs_you"]["concerns"] is None


@pytest.mark.req("hub-page/what-changed-since-the-last-run")
def test_what_changed_names_new_and_cleared_items():
    previous = build()
    previous["needs_you"]["failed"] = [{"key": "unit:old.service", "title": "old.service", "where": "", "url": "", "updated": ""}]
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
