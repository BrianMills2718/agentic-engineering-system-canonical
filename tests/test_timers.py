import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import timers as t  # noqa: E402

JOB = {
    "name": "demo", "description": "Demo job", "why": "to prove the renderer",
    "exec_start": "/usr/bin/true", "environment": {"A": "1"}, "exec_pre": ["/usr/bin/true"],
    "schedule": {"on_calendar": "*-*-* 03:00:00", "persistent": True, "randomized_delay": "5m"},
}


def write(tmp_path, jobs):
    import yaml
    path = tmp_path / "timers.yaml"
    path.write_text(yaml.safe_dump({"timers": jobs}))
    return path


@pytest.mark.req("timer-config/jobs-become-units")
def test_job_becomes_a_oneshot_service_and_a_scheduled_timer(tmp_path):
    files = t.render(t.load(write(tmp_path, [JOB])))
    assert set(files) == {"demo.service", "demo.timer"}
    assert "Type=oneshot" in files["demo.service"] and "ExecStart=/usr/bin/true" in files["demo.service"]
    assert '"A=1"' in files["demo.service"] and "# Why: to prove the renderer" in files["demo.service"]
    assert "OnCalendar=*-*-* 03:00:00" in files["demo.timer"] and "RandomizedDelaySec=5m" in files["demo.timer"]


@pytest.mark.req("timer-config/incomplete-job-is-refused")
@pytest.mark.parametrize("change", [{"why": ""}, {"name": "Bad Name"}, {"surprise": 1}, {"exec_start": None}])
def test_incomplete_or_unknown_job_is_refused(tmp_path, change):
    with pytest.raises(ValueError):
        t.load(write(tmp_path, [{**JOB, **change}]))


@pytest.mark.req("timer-config/incomplete-job-is-refused")
def test_repeated_name_is_refused(tmp_path):
    with pytest.raises(ValueError, match="twice"):
        t.load(write(tmp_path, [JOB, JOB]))


@pytest.mark.req("timer-config/install-backs-up-first")
def test_install_backs_up_the_old_file_then_writes_then_reloads(tmp_path):
    files = t.render(t.load(write(tmp_path, [JOB])))
    live, backup = tmp_path / "live", tmp_path / "backup"
    live.mkdir()
    (live / "demo.service").write_text("old content")
    calls = []
    changed = t.install(files, live, backup, run=lambda argv, check: calls.append(argv) or SimpleNamespace(returncode=0))
    assert sorted(changed) == ["demo.service", "demo.timer"]
    assert (live / "demo.service").read_text() == files["demo.service"]
    saved = list(backup.rglob("demo.service"))
    assert len(saved) == 1 and saved[0].read_text() == "old content"
    assert calls == [["systemctl", "--user", "daemon-reload"]]
    assert t.install(files, live, backup, run=lambda *a, **k: calls.append("again")) == [] and calls == [["systemctl", "--user", "daemon-reload"]]
