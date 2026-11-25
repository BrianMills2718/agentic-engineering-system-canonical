"""`lockstep check helper-reuse`: which functions count as new, the two calls, the cache and the input budget.

The model calls are replaced at the llm_client boundary (`_render`, `_ask`, `_resolve`), so these run offline.
"""
import subprocess
import sys
from pathlib import Path

import pytest

from lockstep.checks import helper_reuse as h
from lockstep.checks.cli import run as run_check

ROOT = Path(__file__).parents[3]
# These read the real repository's functions; mutmut's copy (mutants/) is not a git checkout, so they skip there.
IN_CHECKOUT = pytest.mark.skipif(not (ROOT / ".git").exists(), reason="needs the repository checkout")

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

    def __init__(self, candidates, verdict="same_job", fail=False, judge=None, drop=False):
        self.candidates, self.verdict, self.fail, self.calls = candidates, verdict, fail, []
        self.judge, self.drop = judge, drop

    def __call__(self, model, messages, response_model, trace_id):
        self.calls.append((trace_id, messages))
        if self.fail:
            raise RuntimeError("provider down")
        ctx = messages[0]["context"]
        if response_model is h._Candidates:
            items = [h._Candidate(new_id=f["id"], existing_ids=self.candidates.get(f["id"], []))
                     for f in ctx["new_functions"]]
            return h._Candidates(items=items[1:] if self.drop else items), 0.01
        if self.judge is not None:
            return h._Verdicts(items=self.judge), 0.002
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


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
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


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_function_with_a_new_job_passes(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(NEW_JOB)
    f = fake({})
    code, out = run(root, capsys)
    assert code == 0 and "new_functions=1 flagged=0" in out
    assert len(f.calls) == 1  # no candidates, so no judge call


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_partial_overlap_is_reported_but_passes(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    fake({"src/b.py::make_key": ["src/a.py::slug"]}, verdict="partial_overlap")
    code, out = run(root, capsys)
    assert code == 0 and "partial_overlap: src/b.py::make_key" in out


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_short_wrapper_is_still_read(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text("def run(cmd):\n    return cmd.split()\n")
    f = fake({})
    code, out = run(root, capsys)
    assert "new_functions=1" in out and len(f.calls) == 1


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_moved_function_and_skipped_kinds_are_not_new(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/a.py").write_text("")
    method = "class K:\n    def __init__(self):\n        self.a = 1\n        self.b = 2\n        self.c = 3\n"
    tests = "def test_x():\n    a = 1\n    b = 2\n    assert a < b\n"
    (root / "src/moved.py").write_text(SLUG + "\n\n" + method + "\n\n" + tests)
    f = fake({})
    code, out = run(root, capsys)
    assert code == 0 and "new_functions=0" in out and f.calls == []


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_methods_are_named_by_class(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text("class Box:\n" + "\n".join("    " + line for line in NEW_JOB.splitlines()) + "\n")
    f = fake({})
    run(root, capsys)
    assert [x["id"] for x in f.calls[0][1][0]["context"]["new_functions"]] == ["src/b.py::Box.roman"]


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_failed_call_fails_closed(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    fake({}, fail=True)
    code, out = run(root, capsys)
    assert code == 2 and "RESULT helper-reuse tool-failed exit=2" in out


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_missing_base_fails_closed(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    fake({})
    code = h.main(["--repo", str(root), "--base", "no-such-branch"])
    assert code == 2 and "tool-failed" in capsys.readouterr().out


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_second_run_reads_the_cache(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    f = fake({"src/b.py::make_key": ["src/a.py::slug"]})
    run(root, capsys)
    assert len(f.calls) == 2
    code, out = run(root, capsys)
    assert len(f.calls) == 2 and code == 1 and "cost_usd=0.0000" in out


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_damaged_cache_entry_is_asked_again(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    f = fake({"src/b.py::make_key": ["src/a.py::slug"]})
    run(root, capsys)
    for entry in (root / ".git" / "helper-reuse").glob("*.json"):
        entry.write_text("{not json")
    code, _ = run(root, capsys)
    assert len(f.calls) == 4 and code == 1


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_candidate_not_in_the_index_is_dropped(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    f = fake({"src/b.py::make_key": ["src/a.py::invented"]})
    code, _ = run(root, capsys)
    assert code == 0 and len(f.calls) == 1


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_head_revision_reads_a_commit_not_the_working_tree(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "rewrite")
    (root / "src/b.py").write_text("")
    fake({"src/b.py::make_key": ["src/a.py::slug"]})
    assert h.main(["--repo", str(root), "--base", "main", "--head", "HEAD"]) == 1


def _real_case():
    old = {}
    for p in sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "scripts").rglob("*.py")):
        old.update(h._functions(str(p.relative_to(ROOT)), p.read_text()))
    new = list(h._functions("src/lockstep/checks/maintainability.py",
                            (ROOT / "src" / "lockstep" / "checks" / "maintainability.py").read_text()).values())
    return old, new


def _template_chars(name):
    return len((h.PROMPTS / name).read_text())


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
@IN_CHECKOUT
def test_candidates_prompt_for_the_largest_real_case_fits_the_input_budget():
    """This repository's whole index plus the largest recorded batch (slice 3's ratchet script, 16 functions)."""
    old, new = _real_case()
    ctx = h._candidates_context(old, new)
    chars = (_template_chars("candidates.yaml") + len(ctx["index"])
             + sum(len(f["id"]) + len(f["source"]) for f in ctx["new_functions"]))
    assert chars / h.CHARS_PER_TOKEN <= h.INPUT_BUDGET_TOKENS


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
@IN_CHECKOUT
def test_judge_batches_for_the_worst_real_case_each_fit_the_input_budget():
    """The same batch, each new function paired with the three longest existing functions: split into calls that fit."""
    old, new = _real_case()
    longest = sorted(old.values(), key=lambda f: len(f["source"]))[-3:]
    pairs = [{"id": f["id"], "source": f["source"], "candidates": [{"id": c["id"], "source": c["source"]}
                                                                    for c in longest]} for f in new]
    batches = h._batches(pairs)
    assert len(batches) > 1 and sum(len(b) for b in batches) == len(pairs)
    for b in batches:
        chars = _template_chars("judge.yaml") + sum(h._pair_chars(p) for p in b)
        assert chars / h.CHARS_PER_TOKEN <= h.INPUT_BUDGET_TOKENS


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_prompt_over_the_budget_fails_before_any_call(tmp_path, capsys, fake, monkeypatch):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    f = fake({})
    monkeypatch.setattr(h, "INPUT_BUDGET_TOKENS", 1)
    monkeypatch.setattr(h, "_render", lambda template, **ctx: [{"role": "user", "content": "x" * 100, "context": ctx}])
    code, out = run(root, capsys)
    assert code == 2 and f.calls == []


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
@pytest.mark.parametrize("name", ["candidates.yaml", "judge.yaml"])
def test_templates_use_only_the_context_the_script_passes(name):
    """The templates are rendered by llm_client, which this repository's tests do not install; check their names."""
    import re

    text = (h.PROMPTS / name).read_text()
    used = set(re.findall(r"\{\{\s*([a-z_]+)", text)) | set(re.findall(r"\{%\s*for\s+\w+\s+in\s+([a-z_]+)", text))
    loops = set(re.findall(r"\{%\s*for\s+(\w+)\s+in", text))
    given = {"candidates.yaml": {"index", "new_functions"}, "judge.yaml": {"pairs"}}[name]
    assert used - loops == given
    if name == "candidates.yaml":  # the unchanging index comes before the per-branch part, for caching
        assert text.index("{{ index }}") < text.index("role: user")


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_missing_verdict_fails_closed(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    fake({"src/b.py::make_key": ["src/a.py::slug"]}, judge=[])
    code, out = run(root, capsys)
    assert code == 2 and "tool-failed" in out


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_verdict_naming_a_function_outside_its_candidates_fails_closed(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    bad = [h._Verdict(new_id="src/b.py::make_key", verdict="same_job", existing_id="src/x.py::other", reason="r")]
    fake({"src/b.py::make_key": ["src/a.py::slug"]}, judge=bad)
    code, _ = run(root, capsys)
    assert code == 2
    assert not list((root / ".git" / "helper-reuse").glob("*.json"))[1:]  # the rejected answer is not cached


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_candidates_answer_missing_a_function_fails_closed(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE + "\n\n" + NEW_JOB)
    fake({}, drop=True)
    code, _ = run(root, capsys)
    assert code == 2


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_file_that_does_not_parse_fails_closed(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text("def broken(:\n")
    fake({})
    code, _ = run(root, capsys)
    assert code == 2


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_function_renamed_in_place_is_not_new(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/a.py").write_text(SLUG.replace("def slug(", "def to_slug("))
    f = fake({})
    code, out = run(root, capsys)
    assert code == 0 and "new_functions=0" in out and f.calls == []


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_renamed_and_edited_file_keeps_its_functions(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG + "\n\n" + NEW_JOB})
    git(root, "mv", "src/a.py", "src/c.py")
    (root / "src/c.py").write_text(SLUG.replace("out = name.lower()", "out = name.lower().strip()") + "\n\n" + NEW_JOB)
    git(root, "add", "-A")
    f = fake({})
    code, out = run(root, capsys)
    assert code == 0 and "new_functions=0" in out and f.calls == []


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_verbatim_copy_in_another_file_is_still_judged(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(SLUG.replace("def slug(", "def make_key("))
    f = fake({"src/b.py::make_key": ["src/a.py::slug"]})
    code, out = run(root, capsys)
    assert code == 1 and "new_functions=1 flagged=1" in out and len(f.calls) == 2


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_function_moved_to_another_file_is_not_new(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG + "\n\n" + NEW_JOB})
    (root / "src/a.py").write_text(NEW_JOB)
    (root / "src/helpers.py").write_text(SLUG)
    f = fake({})
    code, out = run(root, capsys)
    assert code == 0 and "new_functions=0" in out and f.calls == []


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_recursive_function_renamed_in_place_is_not_new(tmp_path, capsys, fake):
    fact = "def fact(n):\n    if n < 2:\n        return 1\n    return n * fact(n - 1)\n"
    root = repo(tmp_path, {"src/a.py": fact})
    (root / "src/a.py").write_text(fact.replace("fact", "factorial"))
    f = fake({})
    code, out = run(root, capsys)
    assert "new_functions=0" in out and f.calls == []


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_ids_copied_with_their_arguments_are_cut_at_the_bracket():
    assert h._id("src/a.py::slug(name: str) -> str") == "src/a.py::slug"
    assert h._id("src/a (1).py::x") == "src/a (1).py::x"
    c = h._Candidate(new_id="src/b.py::k(t)", existing_ids=["src/a.py::slug(name)"])
    assert (c.new_id, c.existing_ids) == ("src/b.py::k", ["src/a.py::slug"])
    assert h._Verdict(new_id="x::y(z)", verdict="different", existing_id=None, reason="").existing_id is None


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_path_with_a_space_is_read(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/my helpers.py").write_text(NEW_JOB)
    f = fake({})
    code, out = run(root, capsys)
    assert "new_functions=1" in out and len(f.calls) == 1


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_a_changed_reasoning_setting_asks_again(tmp_path, capsys, fake, monkeypatch):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(NEW_JOB)
    f = fake({})
    run(root, capsys)
    monkeypatch.setattr(h, "REASONING", "xhigh")
    run(root, capsys)
    assert len(f.calls) == 2


@pytest.mark.req("lockstep-checks/helper-reuse-flags-a-rewrite-of-an-existing-function", existing=True)  # moved unchanged from scripts/helper_reuse_check.py
def test_same_job_with_no_existing_function_fails_closed(tmp_path, capsys, fake):
    root = repo(tmp_path, {"src/a.py": SLUG})
    (root / "src/b.py").write_text(REWRITE)
    bad = [h._Verdict(new_id="src/b.py::make_key", verdict="same_job", existing_id=None, reason="r")]
    fake({"src/b.py::make_key": ["src/a.py::slug"]}, judge=bad)
    assert run(root, capsys)[0] == 2


@pytest.mark.req("lockstep-checks/helper-reuse-off-unless-switched-on-and-needs-llm-client")
def test_off_unless_switched_on_and_needs_llm_client(tmp_path, capsys, monkeypatch):
    root = repo(tmp_path, {"src/a.py": SLUG})
    assert run_check(["helper-reuse", "--repo", str(root), "--base", "main"]) == 0
    assert "helper-reuse: skipped (off)" in capsys.readouterr().out
    (root / "lockstep.yaml").write_text("checks:\n  helper-reuse: block\n")
    monkeypatch.setitem(sys.modules, "llm_client", None)  # import fails
    assert run_check(["helper-reuse", "--repo", str(root), "--base", "main"]) == 2
    out = capsys.readouterr().out
    assert "needs llm_client" in out and "RESULT helper-reuse tool-failed=llm_client-missing exit=2" in out


@pytest.mark.req("lockstep-checks/helper-reuse-off-unless-switched-on-and-needs-llm-client")
def test_the_prompts_ship_inside_the_package():
    assert (h.PROMPTS / "candidates.yaml").is_file() and (h.PROMPTS / "judge.yaml").is_file()
    assert h.PROMPTS.parent.parent.name == "checks"
