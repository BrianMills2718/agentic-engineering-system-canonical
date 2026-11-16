"""The daily timer runs the intake command with the project profile (reads the unit files; starts nothing)."""
from pathlib import Path

import pytest

SYSTEMD = Path(__file__).resolve().parents[2] / "scripts" / "learning_loop" / "systemd"


@pytest.mark.req("external-idea-intake/daily-timer-runs-intake")
def test_timer_is_daily_and_service_runs_intake_with_profile():
    timer = (SYSTEMD / "external-ideas.timer").read_text()
    service = (SYSTEMD / "external-ideas.service").read_text()
    assert "OnCalendar=*-*-* " in timer and "Persistent=true" in timer
    exec_line = next(l for l in service.splitlines() if l.startswith("ExecStart="))
    assert "scripts/learning_loop/external_ideas.py" in exec_line and "--profile" in exec_line
    assert "WorkingDirectory=%h/.hive-brain/aes" in service
    assert "EXTERNAL_IDEAS_OUT=%h/projects/data/external-ideas" in service
