"""Tests for scripts/failed_unit_watch.py (pure parsing and planning; no systemd or gh)."""
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

os.environ.setdefault("PROJECT_GRAPH_OWNER", "BrianMills2718")  # the module reads its settings at import
os.environ.setdefault("CONCERN_REPO", "BrianMills2718/project-meta")

spec = importlib.util.spec_from_file_location(
    "failed_unit_watch", Path(__file__).resolve().parents[1] / "scripts/failed_unit_watch.py")
fuw = importlib.util.module_from_spec(spec)
sys.modules["failed_unit_watch"] = fuw
spec.loader.exec_module(fuw)


def test_parse_failed_reads_unit_names_with_and_without_bullet():
    listing = ("● me-hub-check.service loaded failed failed Daily check\n"
               "aes-audit.service      loaded failed failed AES audit\n\n")
    assert fuw.parse_failed(listing) == ["me-hub-check.service", "aes-audit.service"]


def test_parse_failed_empty_listing():
    assert fuw.parse_failed("") == []


def test_repo_from_remote_only_brians_repos():
    assert fuw.repo_from_remote("https://github.com/BrianMills2718/machine-coordination.git\n") == \
        "BrianMills2718/machine-coordination"
    assert fuw.repo_from_remote("git@github.com:BrianMills2718/project-meta.git") == "BrianMills2718/project-meta"
    assert fuw.repo_from_remote("https://github.com/Inside-Success/hive.git") is None


def test_exec_paths_pulls_script_after_interpreter():
    show = "{ path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /home/b/code/x/run.py ; ignore_errors=no }"
    assert "/home/b/code/x/run.py" in fuw.exec_paths(show)


def test_plan_reports_failing_and_closes_recovered_only():
    previous = {"a.service": "o/a", "b.service": "o/b"}
    to_open, to_close = fuw.plan(previous, {"b.service": "o/b", "c.service": "o/c"})
    assert set(to_open) == {"c.service"}  # b was already reported last run
    assert to_close == {"a.service": "o/a"}


def test_plan_reports_a_unit_once_not_on_every_run():
    """2026-10-13: every sweep re-commented on a still-failing unit; issue #2574 got 100 comments."""
    to_open, to_close = fuw.plan({"a.service": "o/a"}, {"a.service": "o/a", "b.service": "o/b"})
    assert to_open == {"b.service": "o/b"}
    assert to_close == {}


def test_a_reboot_does_not_count_as_recovery():
    """A cleared failed state with a failed last run stays failing; a later success does not."""
    outcomes = {"a.service": True, "b.service": False}
    assert fuw.failing_units([], outcomes, [], loaded=lambda u: True) == ["a.service"]
    assert fuw.failing_units([], outcomes, ["b.service"], loaded=lambda u: True) == ["a.service"]


def test_reported_unit_with_no_run_since_stays_until_it_is_removed():
    assert fuw.failing_units([], {}, ["old.service"], loaded=lambda u: True) == ["old.service"]
    assert fuw.failing_units([], {}, ["old.service"], loaded=lambda u: False) == []


def test_currently_failed_units_stay_even_when_the_journal_has_rolled_off():
    assert fuw.failing_units(["x.service"], {}, [], loaded=lambda u: False) == ["x.service"]


def test_read_outcomes_uses_the_last_message_for_each_unit():
    lines = [{"USER_UNIT": "a.service", "MESSAGE_ID": fuw.UNIT_FAILURE}, {"USER_UNIT": "a.service", "MESSAGE_ID": fuw.UNIT_STARTED},
             {"USER_UNIT": "b.service", "MESSAGE_ID": fuw.UNIT_SUCCESS}, {"USER_UNIT": "b.service", "MESSAGE_ID": fuw.UNIT_FAILURE},
             {"MESSAGE_ID": fuw.UNIT_FAILURE}]
    assert fuw.read_outcomes("\n".join(json.dumps(line) for line in lines)) == {"a.service": False, "b.service": True}


def test_a_switched_off_unit_nothing_starts_is_not_a_job():
    """Disabled with no timer (an old one-off) leaves the list; a disabled unit a timer starts stays on it."""
    assert not fuw.scheduled_from({"LoadState": "loaded", "UnitFileState": "disabled", "TriggeredBy": ""})
    assert fuw.scheduled_from({"LoadState": "loaded", "UnitFileState": "disabled", "TriggeredBy": "a.timer"})
    assert fuw.scheduled_from({"LoadState": "loaded", "UnitFileState": "static", "TriggeredBy": ""})
    assert not fuw.scheduled_from({"LoadState": "not-found", "UnitFileState": "", "TriggeredBy": "a.timer"})


# --- Healthchecks.io down checks (personal-file-infra#248) -----------------------------------------
# A job that never runs fails no systemd unit, so the sweep above never sees it; Healthchecks.io
# marks its check "down" and, until 2026-11-05, only emailed Brian (run-artifacts-pack was down
# 19 days unseen). The sweep now files one concern per down check, like a failed unit.

def _check(slug, status, uuid=None):
    return {"slug": slug, "name": slug, "status": status, "uuid": uuid or f"uuid-{slug}",
            "last_ping": "2026-11-05T00:00:00+00:00", "next_ping": None, "schedule": "0 3 * * *", "grace": 43200}


class FakeConcern:
    def __init__(self, close_reply="closed #1"):
        self.calls, self.close_reply = [], close_reply

    def __call__(self, action, repo, key, extra, dry):
        self.calls.append((action, repo, key))
        return self.close_reply if action == "close" else ""


def _sweep(tmp_path, checks, concern, **kw):
    return fuw.healthchecks_sweep(dry=False, state_path=tmp_path / "hc_state.json",
                                  fetch=lambda: checks, repo_for=lambda unit: f"o/{unit}",
                                  pings=lambda uuid: [], tail=lambda unit: "", concern_fn=concern, **kw)


def test_hc_api_key_reads_the_env_line_without_quotes_or_export():
    text = "FOO=1\nexport HEALTHCHECKS_API_KEY='abc123'\nHEALTHCHECKS_PING_KEY=zzz\n"
    assert fuw.hc_api_key(text) == "abc123"
    assert fuw.hc_api_key("FOO=1\n") == ""


def test_only_down_checks_count_not_paused_new_grace_or_up():
    checks = [_check("a", "down"), _check("b", "up"), _check("c", "paused"), _check("d", "new"), _check("e", "grace")]
    assert set(fuw.down_checks(checks)) == {"a"}


def test_each_down_check_gets_one_concern_in_the_jobs_repo(tmp_path):
    concern = FakeConcern()
    opened, recovered, errors = _sweep(tmp_path, [_check("offload-cold", "down"), _check("ok", "up")], concern)
    assert (opened, recovered, errors) == (1, 0, 0)
    assert concern.calls == [("open", "o/offload-cold.service", "healthcheck-down:offload-cold")]


def test_a_still_down_check_is_reported_once_not_every_run(tmp_path):
    """Same rule as failed units: #2574 got 100 comments when every sweep re-reported."""
    concern = FakeConcern()
    _sweep(tmp_path, [_check("a", "down")], concern)
    _sweep(tmp_path, [_check("a", "down")], concern)
    assert [c for c in concern.calls if c[0] == "open"] == [("open", "o/a.service", "healthcheck-down:a")]


def test_a_check_back_up_or_paused_closes_its_concern(tmp_path):
    concern = FakeConcern()
    _sweep(tmp_path, [_check("a", "down"), _check("b", "down")], concern)
    opened, recovered, errors = _sweep(tmp_path, [_check("a", "up"), _check("b", "paused")], concern)
    assert (opened, recovered, errors) == (0, 2, 0)
    assert ("close", "o/a.service", "healthcheck-down:a") in concern.calls
    assert ("close", "o/b.service", "healthcheck-down:b") in concern.calls
    assert fuw.load_state(tmp_path / "hc_state.json") == {"_close_tries": {}}


def test_a_close_that_cannot_find_the_new_issue_yet_is_retried(tmp_path):
    """GitHub search can miss an issue opened minutes ago; keep the check and retry, as for units."""
    _sweep(tmp_path, [_check("a", "down")], FakeConcern())
    concern = FakeConcern(close_reply="no open concern for key")
    _sweep(tmp_path, [_check("a", "up")], concern)
    state = fuw.load_state(tmp_path / "hc_state.json")
    assert "a" in state and state["_close_tries"] == {"a": 1}


def test_an_unreachable_api_is_a_sweep_error_and_keeps_the_state(tmp_path):
    _sweep(tmp_path, [_check("a", "down")], FakeConcern())
    before = (tmp_path / "hc_state.json").read_text()

    def broken():
        raise OSError("connection refused")
    concern = FakeConcern()
    result = fuw.healthchecks_sweep(dry=False, state_path=tmp_path / "hc_state.json", fetch=broken,
                                    repo_for=lambda u: "o/x", pings=lambda u: [], tail=lambda u: "", concern_fn=concern)
    assert result == (0, 0, 1)
    assert concern.calls == []
    assert (tmp_path / "hc_state.json").read_text() == before


def test_down_body_names_the_unit_and_the_last_pings():
    body = fuw.hc_down_body(_check("offload-cold", "down"),
                            [{"type": "fail", "date": "2026-11-06T01:03:40+00:00"}], "journal line")
    assert "offload-cold.service" in body and "fail" in body and "2026-11-06T01:03:40" in body
    assert "journal line" in body and "```" not in body and "journalctl --user -u offload-cold.service" in body


def test_repo_from_remote_reads_ssh_host_aliases():
    """2026-11-05: remotes use the `github-personal` SSH alias, so offload-cold (personal-file-infra) was filed in
    project-meta, the fallback, instead of its own repository."""
    assert fuw.repo_from_remote("git@github-personal:BrianMills2718/personal-file-infra.git\n") == \
        "BrianMills2718/personal-file-infra"
    assert fuw.repo_from_remote("git@github-personal:Inside-Success/hive.git") is None


def test_transient_run_units_get_no_issue():
    """run-u2958/3422/3644 were an agent's systemd-run scratch repro that sat in the failed list (2026-11-07)."""
    listing = ("● run-u2958.service loaded failed failed /usr/bin/python3 repro.py\n"
               "run-r3f2a.scope loaded failed failed run-r3f2a.scope\n"
               "brent-us-sources.service loaded failed failed Fetch Brent sources\n")
    assert fuw.parse_failed(listing) == ["brent-us-sources.service"]
    assert fuw.failing_units([], {"run-u3422.service": True}, [], loaded=lambda u: True) == []


_REAL_LOAD_STATE = fuw.load_state


def _sweep_units(monkeypatch, tmp_path, *, failed, repo, scheduled=True, outcomes=None, issues=None, expect=0):
    """One run of main() with systemd, GitHub and the journal stubbed; returns the concern calls it made."""
    calls = []
    state_file = tmp_path / "state.json"
    monkeypatch.setattr(fuw, "STATE", state_file)
    monkeypatch.setattr(fuw, "load_state", lambda: _REAL_LOAD_STATE(state_file))  # its default path was bound at import
    monkeypatch.setattr(fuw, "failed_units", lambda: failed)
    monkeypatch.setattr(fuw, "last_outcomes", lambda: outcomes or {})  # default: a rebooted laptop, the journal has no earlier run
    monkeypatch.setattr(fuw, "open_concerns", lambda: issues or [])  # the open issues GitHub holds for this watch
    monkeypatch.setattr(fuw, "owning_repo", lambda unit: repo)
    monkeypatch.setattr(fuw, "journal_line", lambda unit: "journal line")
    monkeypatch.setattr(fuw, "healthchecks_sweep", lambda dry: (0, 0, 0))
    monkeypatch.setattr(fuw, "run", lambda cmd: f"LoadState={'loaded' if scheduled else 'not-found'}\nUnitFileState=static\nTriggeredBy=\n")
    monkeypatch.setattr(fuw, "concern", lambda action, repo, key, extra, dry: calls.append((action, repo, key)) or "")
    assert fuw.main([]) == expect
    return calls


def test_a_reported_unit_is_closed_in_the_repo_that_holds_its_issue(monkeypatch, tmp_path):
    """2026-11-05..08, project-meta#2599: ecosystem-ops-daily was filed in project-meta (its `github-personal` remote
    was not yet recognised, so the owner fell back). The remote fix then made the owner ecosystem-ops; each sweep
    re-derived the owner and rewrote the state, so the close went to ecosystem-ops, found nothing, gave up after four
    tries, and the project-meta issue stayed open for good."""
    key = "failed-unit:a.service"
    opened = _sweep_units(monkeypatch, tmp_path, failed=["a.service"], repo="o/project-meta")
    assert opened == [("open", "o/project-meta", key)]
    # The unit stays reported with no run since (a reboot emptied the journal); its owner is now worked out differently.
    still = _sweep_units(monkeypatch, tmp_path, failed=[], repo="o/ecosystem-ops")
    assert still == []
    assert _REAL_LOAD_STATE(tmp_path / "state.json")["a.service"] == "o/project-meta"
    closed = _sweep_units(monkeypatch, tmp_path, failed=[], repo="o/ecosystem-ops", scheduled=False)
    assert closed == [("close", "o/project-meta", key)]


def _issue(unit, repo, number=1, updated="2026-11-05T18:10:47Z", key_prefix="failed-unit"):
    """An open issue as `gh search issues --json repository,number,body,updatedAt` returns it."""
    return {"repository": {"nameWithOwner": repo}, "number": number, "updatedAt": updated,
            "body": f"Body text\n\n<!-- concern-key: {key_prefix}:{unit} -->"}


def test_adoptable_takes_open_failed_unit_issues_the_state_does_not_know():
    issues = [_issue("a.service", "o/project-meta"), _issue("b.service", "o/other")]
    assert fuw.adoptable({"b.service": "o/ops"}, issues) == {"a.service": "o/project-meta"}  # b keeps the state's repo


def test_adoptable_ignores_other_keys_and_issues_without_one():
    issues = [_issue("c", "o/x", key_prefix="healthcheck-down"), {"repository": {"nameWithOwner": "o/y"}, "body": None}]
    assert fuw.adoptable({}, issues) == {}


def test_adoptable_picks_the_most_recently_updated_issue_for_one_unit():
    issues = [_issue("a.service", "o/new", updated="2026-11-08T00:00:00Z"), _issue("a.service", "o/old", updated="2026-10-01T00:00:00Z")]
    assert fuw.adoptable({}, issues) == {"a.service": "o/new"}


def test_a_stranded_issue_is_adopted_and_closed_once_a_later_run_succeeded(monkeypatch, tmp_path):
    """2026-11-05..09, project-meta#2664: local-data-backup.service's concern was opened in project-meta, the state then
    moved to personal-file-infra and the close gave up, so no state entry named the issue. It stayed open for four
    days while the unit ran green four times: nothing in the watch knew the issue existed."""
    issue = [_issue("a.service", "o/project-meta")]
    closed = _sweep_units(monkeypatch, tmp_path, failed=[], repo="o/personal-file-infra", issues=issue, outcomes={"a.service": False})
    assert closed == [("close", "o/project-meta", "failed-unit:a.service")]
    assert "a.service" not in _REAL_LOAD_STATE(tmp_path / "state.json")


def test_an_adopted_issue_stays_open_while_the_journal_has_no_run_since_a_reboot(monkeypatch, tmp_path):
    """The reboot guard applies to an adopted issue too: no recorded run is not a recovery (a cleared failed state
    once closed issues as verified green on jobs that were still broken)."""
    issue = [_issue("a.service", "o/project-meta")]
    assert _sweep_units(monkeypatch, tmp_path, failed=[], repo="o/personal-file-infra", issues=issue) == []
    assert _REAL_LOAD_STATE(tmp_path / "state.json")["a.service"] == "o/project-meta"
    # ... and a later success then closes it in the repository that holds the issue.
    later = _sweep_units(monkeypatch, tmp_path, failed=[], repo="o/personal-file-infra", outcomes={"a.service": False})
    assert later == [("close", "o/project-meta", "failed-unit:a.service")]


def test_an_adopted_issue_for_a_unit_still_failing_is_left_alone(monkeypatch, tmp_path):
    """Adopting must not comment again or close a unit whose last run failed."""
    issue = [_issue("a.service", "o/project-meta")]
    assert _sweep_units(monkeypatch, tmp_path, failed=[], repo="o/personal-file-infra", issues=issue, outcomes={"a.service": True}) == []
    assert _REAL_LOAD_STATE(tmp_path / "state.json")["a.service"] == "o/project-meta"


def test_a_failed_issue_search_is_a_sweep_error_but_the_sweep_still_runs(monkeypatch, tmp_path):
    def boom():
        raise fuw.subprocess.CalledProcessError(1, ["gh"])
    calls = []
    monkeypatch.setattr(fuw, "STATE", tmp_path / "state.json")
    monkeypatch.setattr(fuw, "load_state", lambda: {})
    monkeypatch.setattr(fuw, "failed_units", lambda: ["a.service"])
    monkeypatch.setattr(fuw, "last_outcomes", lambda: {})
    monkeypatch.setattr(fuw, "owning_repo", lambda unit: "o/project-meta")
    monkeypatch.setattr(fuw, "journal_line", lambda unit: "journal line")
    monkeypatch.setattr(fuw, "healthchecks_sweep", lambda dry: (0, 0, 0))
    monkeypatch.setattr(fuw, "run", lambda cmd: "LoadState=loaded\nUnitFileState=static\nTriggeredBy=\n")
    monkeypatch.setattr(fuw, "open_concerns", boom)
    monkeypatch.setattr(fuw, "concern", lambda action, repo, key, extra, dry: calls.append((action, repo, key)) or "")
    assert fuw.main([]) == 2  # loud: the watch could not look for stranded issues
    assert calls == [("open", "o/project-meta", "failed-unit:a.service")]  # the ordinary sweep still ran


@pytest.mark.req("failed-unit-watch/settings-come-from-config")
def test_missing_settings_stop_loudly(monkeypatch, tmp_path):
    monkeypatch.delenv("PROJECT_GRAPH_OWNER", raising=False)
    monkeypatch.setattr(fuw, "CONFIG", tmp_path / "graph-config.yaml")
    with pytest.raises(SystemExit, match="no owner named"):
        fuw.setting("owner", "PROJECT_GRAPH_OWNER")
    (tmp_path / "graph-config.yaml").write_text("owner: Someone\nconcern_repo: Someone/ops\n")
    assert fuw.setting("owner", "PROJECT_GRAPH_OWNER") == "Someone"
    assert fuw.setting("concern_repo", "CONCERN_REPO_UNSET") == "Someone/ops"


def _entry(ident, message, ts="1763370486000000", host="WINDOWS-HOST", pid="2295333"):
    return json.dumps({"SYSLOG_IDENTIFIER": ident, "MESSAGE": message, "__REALTIME_TIMESTAMP": ts,
                       "_HOSTNAME": host, "_PID": pid})


@pytest.mark.req("failed-unit-watch/issue-body-carries-one-line-not-the-log")
def test_the_line_is_the_newest_one_the_job_printed_without_host_or_pid():
    """AES #945 (2026-11-17) carried 14 journal lines with the host name; the one that said why was the job's own."""
    journal = "\n".join([
        _entry("systemd", "Starting brent-fdot-feed.service - Read FDOT's feed..."),
        _entry("bash", "could not read the Windows user name"),
        _entry("systemd", "brent-fdot-feed.service: Main process exited, code=exited, status=1/FAILURE"),
        _entry("systemd", "brent-fdot-feed.service: Failed with result 'exit-code'."),
    ])
    line = fuw.pick_line(journal)
    assert "could not read the Windows user name" in line
    assert "WINDOWS-HOST" not in line and "2295333" not in line and "systemd" not in line


def test_with_no_line_from_the_job_systemds_newest_line_is_used():
    journal = "\n".join([_entry("systemd", "x.service: Main process exited, status=1/FAILURE"),
                         _entry("systemd", "x.service: Failed with result 'exit-code'.")])
    assert "Failed with result" in fuw.pick_line(journal)
    assert fuw.pick_line("") == "(no journal lines)"


def test_a_line_printed_as_bytes_and_a_home_path_are_made_readable_and_redacted():
    raw = list(f"wrote {Path.home()}/projects/x.json".encode())
    assert fuw.pick_line(_entry("python3", raw)).endswith("wrote ~/projects/x.json")


@pytest.mark.req("failed-unit-watch/issue-body-carries-one-line-not-the-log")
def test_failed_unit_body_has_the_line_and_the_journalctl_pointer_and_no_log_block(monkeypatch, tmp_path):
    bodies = []
    state_file = tmp_path / "state.json"
    monkeypatch.setattr(fuw, "STATE", state_file)
    monkeypatch.setattr(fuw, "load_state", lambda: _REAL_LOAD_STATE(state_file))
    monkeypatch.setattr(fuw, "failed_units", lambda: ["x.service"])
    monkeypatch.setattr(fuw, "last_outcomes", lambda: {})
    monkeypatch.setattr(fuw, "open_concerns", lambda: [])
    monkeypatch.setattr(fuw, "owning_repo", lambda unit: "o/x")
    monkeypatch.setattr(fuw, "journal_line", lambda unit: "2026-11-17 09:48:06 bash: boom")
    monkeypatch.setattr(fuw, "healthchecks_sweep", lambda dry: (0, 0, 0))
    monkeypatch.setattr(fuw, "concern", lambda action, repo, key, extra, dry: bodies.append(extra[extra.index("--body") + 1]) or "")
    assert fuw.main([]) == 0
    assert "bash: boom" in bodies[0] and "journalctl --user -u x.service" in bodies[0]
    assert "```" not in bodies[0] and "Last journal lines" not in bodies[0]


@pytest.mark.req("failed-unit-watch/ssh-host-alias-remotes-find-their-repository")
def test_repo_from_remote_reads_the_github_com_host_alias():
    assert fuw.repo_from_remote("git@github.com-personal:BrianMills2718/brent-chatgpt.git\n") == "BrianMills2718/brent-chatgpt"
