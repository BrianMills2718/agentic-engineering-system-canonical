"""Tests for scripts/public_text.py: text bound for an issue anyone may read."""
import importlib.util
import sys
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("public_text", Path(__file__).resolve().parents[1] / "scripts/public_text.py")
pt = importlib.util.module_from_spec(spec)
sys.modules["public_text"] = pt
spec.loader.exec_module(pt)


@pytest.mark.req("failed-unit-watch/issue-body-carries-one-line-not-the-log")
def test_redact_home_paths_windows_users_emails_and_ips():
    text = ("open /home/alice/code2/x.py and /Users/bob/notes, home=/srv/me/a\n"
            r"C:\Users\carol\AppData\x.ps1 and C:/Users/carol/y" "\n"
            "mail dave@example.com from 192.168.1.20")
    out = pt.redact(text, home="/srv/me")
    assert "alice" not in out and "bob" not in out and "carol" not in out
    assert "~/code2/x.py" in out and "~/notes" in out and "home=~/a" in out
    assert r"C:\Users\<you>\AppData" in out and "C:/Users/<you>/y" in out
    assert "<email>" in out and "dave@" not in out
    assert "<ip>" in out and "192.168" not in out


def test_redact_leaves_versions_and_plain_text_alone():
    assert pt.redact("python 3.12.1 exited status=1/FAILURE", home="/srv/me") == "python 3.12.1 exited status=1/FAILURE"


def test_first_line_is_the_first_non_empty_line_cut_short_and_redacted():
    assert pt.first_line("\n  \nboom at /srv/me/x\nsecond", home="/srv/me") == "boom at ~/x"
    assert len(pt.first_line("x" * 1000)) <= 300
    assert pt.first_line("") == "(no output)"
