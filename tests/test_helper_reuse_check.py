"""Tests for scripts/helper_reuse_check.py: which functions count as new, the two calls, the cache and the input budget.

The model calls are replaced at the llm_client boundary (`_render`, `_ask`, `_resolve`), so these run offline.
"""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import helper_reuse_check as h

GIT = ["-c", "user.name=t", "-c", "user.email=t@t"]

SLUG = '''def slug(name):
    """Lowercase words joined by hyphens."""
    out = name.lower()
    return "-".join(out.split())
'''
REWRITE = '''def make_key(title):
    """Key for a heading."""
    words = title.lower().split()
    return "-".join(words)
'''
NEW_JOB = '''def roman(n):
    """Write a positive integer as a Roman numeral."""
    table = [(10, "X"), (5, "V"), (1, "I")]
    out = ""
    for v, s in table:
        while n >= v:
            out += s
            n -= v
    return out
'''
# Recorded call (trace aes/helper-reuse/0f882a1f8/candidates, 2026-11-24): 45,739 prompt tokens for a rendered
# prompt of 170,364 characters (1,280 indexed functions, 12 new ones), so 3.72 characters per token.
CHARS_PER_TOKEN = 3.72
INPUT_BUDGET_TOKENS = 60_000


def git(root, *args):
    subprocess.run(["git", "-C", str(root), *GIT, *args], check=True, capture_output=True)


def repo(tmp_path, files):
    root = tmp_path / "r"
    (root / "src").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    for name, text in files.items():
        (root / name).write_text(text)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    git(root, "checkout", "-qb", "work")
    return root


class Fake:
    """Stands in for the model: names candidates by a fixed map and judges by a fixed verdict."""

    def __init__(self, candidates, verdict="same_job", fail=False):
        self.candidates, self.verdict, self.fail, self.calls = candidates, verdict, fail, []

    def __call__(self, model, messages, response_model, trace_id):
        self.calls.append((trace_id, messages))
        if self.fail:
            raise RuntimeError("provider down")
        ctx = messages[0]["context"]
        if response_model is h._Candidates:
            return h._Candidates(items=[h._Candidate(new_id=f["id"], existing_ids=self.candidates.get(f["id"], []))
                                        for f in ctx["new_functions"]]), 0.01
        return h._Verdicts(items=[h._Verdict(new_id=p["id"], verdict=self.verdict,
                                             existing_id=p["candidates"][0]["id"], reason="same steps")
                                  for p in ctx["pairs"]]), 0.002


@pytest.fixture
def fake(monkeypatch):
    def install(candidates, **kw):
        f = Fake(candidates, **kw)
        monkeypatch.setattr(h, "_ask", f)
        monkeypatch.setattr(h, "_render", lambda template, **ctx: [{"role": "user", "content": template,
                                                                    "context": ctx}])
        monkeypatch.setattr(h, "_resolve", lambda model: "test/model")
        return f
    return install


def run(root, capsys):
    code = h.main(["--repo", str(root), "--base", "main"])
    return code, capsys.readouterr().out


def test_a_rewrite_under_a_new_name_is_flagged(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    f = fake({"src/b.py::make_key": ["src/a.py::slug"]})
    code, out = run(root, capsys)
    assert code == 1
    assert "same_job: src/b.py::make_key -> src/a.py::slug" in out
    assert "new_functions=1 flagged=1" in out
    index = f.calls[0][1][0]["context"]["index"]
    assert "src/a.py::slug(name) Lowercase words joined by hyphens." in index and "make_key" not in index


def test_a_function_with_a_new_job_passes(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(NEW_JOB)
    f = fake({})
    code, out = run(root, capsys)
    assert code == 0 and "new_functions=1 flagged=0" in out
    assert len(f.calls) == 1  # no candidates, so no judge call


def test_partial_overlap_is_reported_but_passes(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    fake({"src/b.py::make_key": ["src/a.py::slug"]}, verdict="partial_overlap")
    code, out = run(root, capsys)
    assert code == 0 and "partial_overlap: src/b.py::make_key" in out


def test_a_short_wrapper_is_still_read(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text("def run(cmd):\n    return cmd.split()\n")
    f = fake({})
    code, out = run(root, capsys)
    assert "new_functions=1" in out and len(f.calls) == 1


def test_moved_function_and_skipped_kinds_are_not_new(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/a.py").write_text("")
    method = "class K:\n    def __init__(self):\n        self.a = 1\n        self.b = 2\n        self.c = 3\n"
    tests = "def test_x():\n    a = 1\n    b = 2\n    assert a < b\n"
    (root / "src/moved.py").write_text(SLUG + "\n\n" + method + "\n\n" + tests)
    f = fake({})
    code, out = run(root, capsys)
    assert code == 0 and "new_functions=0" in out and f.calls == []


def test_methods_are_named_by_class(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text("class Box:\n" + "\n".join("    " + line for line in NEW_JOB.splitlines()) + "\n")
    f = fake({})
    run(root, capsys)
    assert [x["id"] for x in f.calls[0][1][0]["context"]["new_functions"]] == ["src/b.py::Box.roman"]


def test_a_failed_call_fails_closed(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    fake({}, fail=True)
    code, out = run(root, capsys)
    assert code == 2 and "RESULT helper-reuse tool-failed exit=2" in out


def test_a_missing_base_fails_closed(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    fake({})
    code = h.main(["--repo", str(root), "--base", "no-such-branch"])
    assert code == 2 and "tool-failed" in capsys.readouterr().out


def test_a_second_run_reads_the_cache(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    f = fake({"src/b.py::make_key": ["src/a.py::slug"]})
    run(root, capsys)
    assert len(f.calls) == 2
    code, out = run(root, capsys)
    assert len(f.calls) == 2 and code == 1 and "cost_usd=0.0000" in out


def test_a_damaged_cache_entry_is_asked_again(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    f = fake({"src/b.py::make_key": ["src/a.py::slug"]})
    run(root, capsys)
    for entry in (root / ".git" / "helper-reuse").glob("*.json"):
        entry.write_text("{not json")
    code, _ = run(root, capsys)
    assert len(f.calls) == 4 and code == 1


def test_a_candidate_not_in_the_index_is_dropped(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    f = fake({"src/b.py::make_key": ["src/a.py::invented"]})
    code, _ = run(root, capsys)
    assert code == 0 and len(f.calls) == 1


def test_head_revision_reads_a_commit_not_the_working_tree(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "rewrite")
    (root / "src/b.py").write_text("")
    fake({"src/b.py::make_key": ["src/a.py::slug"]})
    assert h.main(["--repo", str(root), "--base", "main", "--head", "HEAD"]) == 1


def test_candidates_prompt_for_the_largest_real_case_fits_the_input_budget():
    """This repository's whole index plus the largest recorded batch (slice 3's ratchet script) stays in budget."""
    old = {}
    for p in sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "scripts").rglob("*.py")):
        old.update(h._functions(str(p.relative_to(ROOT)), p.read_text()))
    new = list(h._functions("scripts/maintainability_ratchet.py",
                            (ROOT / "scripts" / "maintainability_ratchet.py").read_text()).values())
    ctx = h._candidates_context(old, new)
    chars = (len((h.PROMPTS / "candidates.yaml").read_text()) + len(ctx["index"])
             + sum(len(f["id"]) + len(f["source"]) for f in ctx["new_functions"]))
    assert chars / CHARS_PER_TOKEN <= INPUT_BUDGET_TOKENS
