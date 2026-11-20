"""Lockstep's tests: the example projects and end-to-end scripts are inputs the tests copy, not tests."""

from lockstep_support import planned, proj  # noqa: F401  (shared fixtures)

import pytest


@pytest.fixture(autouse=True)
def _guard_log_in_tmp(tmp_path, monkeypatch):
    """The edit guard logs under $XDG_STATE_HOME (issue #974); keep each test's log out of the real home folder."""
    monkeypatch.delenv("LOCKSTEP_LOG_DIR", raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))


collect_ignore = ["example", "example-simple", "example-layout", "e2e", "lockstep-plan-sample"]
