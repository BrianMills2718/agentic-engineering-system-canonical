import json, os, signal, subprocess, sys, tempfile, time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
import md_file_cap as m


def make_repo(tmp, name, n_md, exception=None, untracked_md=0):
    path = tmp / name
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    for i in range(n_md):
        (path / f"doc{i}.md").write_text("x")
    (path / "code.py").write_text("x")
    if exception is not None:
        (path / m.EXCEPTION_FILE).write_text(exception)
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(path), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"], check=True)
    for i in range(untracked_md):  # untracked files must not count
        (path / f"loose{i}.md").write_text("x")
    return path


def run(tmp, entries, cap=5):
    graph = tmp / "graph.json"
    graph.write_text(json.dumps(entries))
    rows = m.evaluate(m.owned_checkouts(str(graph)), cap)
    return {r["repo"]: r for r in rows}


def test_cap_exceptions_and_scope(tmp_path):
    under = make_repo(tmp_path, "under", 5, untracked_md=10)  # exactly at cap; untracked ignored
    over = make_repo(tmp_path, "over", 6)
    excused = make_repo(tmp_path, "excused", 9, "limit: 20\nreason: document corpus\n")
    outgrown = make_repo(tmp_path, "outgrown", 9, "limit: 8\nreason: document corpus\n")
    no_reason = make_repo(tmp_path, "noreason", 3, "limit: 20\n")
    others = make_repo(tmp_path, "others", 50)
    rows = run(tmp_path, [
        {"github_repo": "BrianMills2718/under", "path": str(under)},
        {"github_repo": "BrianMills2718/under-alias", "path": str(under)},  # same checkout: counted once
        {"github_repo": "BrianMills2718/over", "path": str(over)},
        {"github_repo": "BrianMills2718/excused", "path": str(excused)},
        {"github_repo": "BrianMills2718/outgrown", "path": str(outgrown)},
        {"github_repo": "BrianMills2718/noreason", "path": str(no_reason)},
        {"github_repo": "Inside-Success/others", "path": str(others)},  # not Brian's: out of scope
        {"github_repo": "BrianMills2718/missing", "path": str(tmp_path / "nope")},
    ])
    assert set(rows) == {"BrianMills2718/under", "BrianMills2718/over", "BrianMills2718/excused",
                         "BrianMills2718/outgrown", "BrianMills2718/noreason"}
    assert (rows["BrianMills2718/under"]["md"], rows["BrianMills2718/under"]["status"]) == (5, "ok")
    assert rows["BrianMills2718/over"]["status"] == "over"
    assert rows["BrianMills2718/excused"]["status"] == "exception"
    assert rows["BrianMills2718/outgrown"]["status"] == "over"
    assert rows["BrianMills2718/noreason"]["status"] == "over"
    assert "reason" in rows["BrianMills2718/noreason"]["detail"]


def test_entry_without_github_repo_uses_origin_owner(tmp_path):
    mine = make_repo(tmp_path, "mine", 6)
    theirs = make_repo(tmp_path, "theirs", 6)
    subprocess.run(["git", "-C", str(mine), "remote", "add", "origin", "git@github-personal:BrianMills2718/mine.git"], check=True)
    subprocess.run(["git", "-C", str(theirs), "remote", "add", "origin", "https://github.com/Inside-Success/theirs.git"], check=True)
    rows = run(tmp_path, [{"id": "mine", "path": str(mine)}, {"id": "theirs", "path": str(theirs)}])
    assert set(rows) == {"BrianMills2718/mine"}
    assert rows["BrianMills2718/mine"]["status"] == "over"


def test_json_stdout_is_parseable(tmp_path, capsys):
    repo = make_repo(tmp_path, "one", 2)
    graph = tmp_path / "graph.json"
    graph.write_text(json.dumps([{"github_repo": "BrianMills2718/one", "path": str(repo)}]))
    assert m.main(["--graph", str(graph), "--json", "--cap", "5"]) == 1  # under the cap, but no wiki/index.md
    out = json.loads(capsys.readouterr().out)
    assert out["counts"]["ok"] == 1 and out["reach_counts"]["no-wiki"] == 1


def test_reads_default_branch_not_checked_out_work_branch(tmp_path):
    repo = make_repo(tmp_path, "vision", 9, "limit: 20\nreason: source corpus\n")
    git = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t"]
    # main (as fetched) carries the exception; a local work branch without it is checked out
    subprocess.run(git + ["update-ref", "refs/remotes/origin/main", "HEAD"], check=True)
    subprocess.run(git + ["checkout", "-qb", "work"], check=True)
    subprocess.run(git + ["rm", "-q", m.EXCEPTION_FILE], check=True)
    subprocess.run(git + ["commit", "-qm", "work"], check=True)
    rows = run(tmp_path, [{"github_repo": "BrianMills2718/vision", "path": str(repo)}])
    assert rows["BrianMills2718/vision"]["status"] == "exception"


def make_wiki_repo(tmp_path, files, exception=None):
    path = tmp_path / "wikirepo"
    for rel, text in files.items():
        f = path / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)
    if exception is not None:
        (path / m.EXCEPTION_FILE).write_text(exception)
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(path), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"], check=True)
    return str(path)


def test_reachability_classifies_unlinked_docs(tmp_path):
    repo = make_wiki_repo(tmp_path, {
        "wiki/index.md": "[a](../docs/a.md)",
        "docs/a.md": "[b](b.md)",
        "docs/b.md": "[c](c.md)",            # c is three links deep
        "docs/c.md": "deep",
        "docs/orphan.md": "nobody links me",
        "CLAUDE.md": "instructions", "tests/fixtures/x.md": "fixture", "docs/plans/TEMPLATE.md": "t",
        "docs/out.md": "generated",
        "scripts/gen.py": 'from pathlib import Path\nMARKDOWN_OUTPUT_PATH = Path("docs/out.md")\n',
        "raw/sources/s1.md": "source",
    })
    r = m.reachability(repo, "HEAD")
    assert r["status"] == "orphans"
    assert set(r["orphans"]) == {"docs/orphan.md", "raw/sources/s1.md"}
    assert r["beyond"] == ["docs/c.md"]


def test_unlinked_ok_needs_a_reason_and_exempts_its_folder(tmp_path):
    files = {"wiki/index.md": "[a](../docs/a.md)", "docs/a.md": "x", "raw/sources/s1.md": "s"}
    ok = m.reachability(make_wiki_repo(tmp_path / "ok", files, "limit: 5\nreason: r\nunlinked_ok:\n  - path: raw/sources/\n    reason: source material\n"), "HEAD")
    assert ok["status"] == "ok" and ok["orphans"] == []
    bad = m.reachability(make_wiki_repo(tmp_path / "bad", files, "limit: 5\nreason: r\nunlinked_ok:\n  - path: raw/sources/\n"), "HEAD")
    assert bad["status"] == "orphans" and "reason" in bad["detail"]


def test_no_wiki_is_reported(tmp_path):
    r = m.reachability(make_wiki_repo(tmp_path, {"README.md": "hi"}), "HEAD")
    assert r["status"] == "no-wiki"


def test_percent_encoded_link_to_a_name_with_spaces_counts_as_reached(tmp_path):
    repo = make_wiki_repo(tmp_path, {
        "wiki/index.md": "[meeting](../meetings/2026-07-10%20-%20Team%20Sync.md)",
        "meetings/2026-07-10 - Team Sync.md": "notes",
    })
    r = m.reachability(repo, "HEAD")
    assert r["status"] == "ok" and r["orphans"] == []


def test_root_relative_links_resolve_against_repo_root_then_wiki_folder(tmp_path):
    """Defect 2026-10-13: a link starting with "/" was joined onto the linking
    file's folder by os.path.join, which returns "/people/a.md" -- never a tracked
    path -- so personal-wiki (whose links are root-relative from wiki/) reported
    all 480 pages as orphans, including pages wiki/index.md links directly."""
    repo = make_wiki_repo(tmp_path, {
        "wiki/index.md": "[a](/people/a.md) [b](/docs/b.md) [gone](/nope.md)",
        "wiki/people/a.md": "resolves under wiki/",
        "docs/b.md": "resolves at the repository root",
        "docs/stray.md": "a real orphan",
    })
    r = m.reachability(repo, "HEAD")
    assert r["orphans"] == ["docs/stray.md"]
    assert r["reachable"] == 3  # index + a + b; /nope.md is not counted


def test_docs_in_hidden_tool_folders_are_not_reader_docs(tmp_path):
    repo = make_wiki_repo(tmp_path, {
        "wiki/index.md": "[a](../docs/a.md)", "docs/a.md": "x",
        ".project-brain/now.md": "agent-loaded state", ".templates/claim.md": "template",
        "docs/stray.md": "a real orphan",
    })
    r = m.reachability(repo, "HEAD")
    assert r["orphans"] == ["docs/stray.md"]


def git_repo(tmp, name, files):
    path = tmp / name
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    for rel, text in files.items():
        (path / rel).parent.mkdir(parents=True, exist_ok=True)
        (path / rel).write_text(text)
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(path), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"], check=True)
    return path


REPO_YAML = ("authorities:\n  normative_roots: [docs/architecture/]\n  decision_roots: [docs/decisions/]\n"
             "  plan_roots: [docs/plans/]\n")
LAID_OUT = {".agentic/repo.yaml": REPO_YAML, "docs/architecture/design.md": "x", "docs/decisions/ADR-1-a.md": "x",
            "docs/plans/001_first.md": "x"}


def test_layout_undeclared_is_reported_not_passed(tmp_path):
    repo = git_repo(tmp_path, "r", {"README.md": "x"})
    assert m.layout(str(repo))["status"] == "undeclared"


def test_layout_ok_and_decision_outside_root(tmp_path):
    repo = git_repo(tmp_path, "r", dict(LAID_OUT))
    assert m.layout(str(repo)) == {"status": "ok", "findings": [], "detail": ""}
    misplaced = git_repo(tmp_path, "s", {**LAID_OUT, "plan/ADR-2-b.md": "x", "plan/002_second.md": "x",
                                          "notes/architecture/old.md": "x"})
    found = m.layout(str(misplaced))
    assert found["status"] == "findings"
    assert sorted(found["findings"]) == [("decision-outside", "plan/ADR-2-b.md"), ("design-outside", "notes/architecture/old.md"),
                                         ("plan-outside", "plan/002_second.md")]


def test_layout_generated_output_and_file_exception(tmp_path):
    files = {**LAID_OUT, "scripts/gen.py": 'from pathlib import Path\nREPORT_OUTPUT = Path("reports/out.json")\n',
             "reports/out.json": "{}", "ui/schema.json": "{}",
             "Makefile": "x:\n\tpython3 scripts/build.py --output ui/schema.json\n"}
    repo = git_repo(tmp_path, "r", files)
    assert sorted(m.layout(str(repo))["findings"]) == [("generated-outside", "reports/out.json"), ("generated-outside", "ui/schema.json")]
    kept = git_repo(tmp_path, "s", {**files, m.EXCEPTION_FILE: "layout_ok:\n  - path: ui/schema.json\n    reason: build input\n"})
    assert m.layout(str(kept))["findings"] == [("generated-outside", "reports/out.json")]


def test_reachability_exempts_generated_folder_outputs_anywhere_and_file_entries(tmp_path):
    repo = git_repo(tmp_path, "r", {
        "wiki/index.md": "[a](../docs/a.md)\n", "docs/a.md": "x",
        "generated/page.md": "x",                                   # under generated/
        "tools/gen.py": 'from pathlib import Path\nPAGE_OUTPUT = Path("out/page.md")\n', "out/page.md": "x",  # *OUTPUT* outside scripts/
        "notes/raw.md": "x", m.EXCEPTION_FILE: "unlinked_ok:\n  - path: notes/raw.md\n    reason: source material\n",
        "docs/orphan.md": "x"})
    r = m.reachability(str(repo))
    assert r["orphans"] == ["docs/orphan.md"] and r["beyond"] == []


def test_repo_option_checks_a_given_checkout_at_a_ref(tmp_path, capsys):
    repo = git_repo(tmp_path, "r", dict(LAID_OUT, **{"wiki/index.md": "[d](../docs/architecture/design.md) [a](../docs/decisions/ADR-1-a.md) [p](../docs/plans/001_first.md)\n"}))
    assert m.main(["--repo", str(repo), "--ref", "HEAD"]) == 0
    out = capsys.readouterr().out
    assert "layout=ok(0)" in out and "1 given repos checked" in out and "exit 0" in out


def test_repo_option_on_someone_elses_repo_reports_cap_out_of_scope(tmp_path, capsys):
    files = {f"d{i}.md": "x" for i in range(8)}
    repo = git_repo(tmp_path, "r", files)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", "https://github.com/Other-Org/r.git"], check=True)
    assert m.main(["--repo", str(repo), "--ref", "HEAD", "--cap", "5"]) == 1  # no wiki/index.md is still a finding
    out = capsys.readouterr().out
    assert "cap=out-of-scope" in out and "over=0" in out and "out-of-scope=1" in out


def test_layout_does_not_judge_generator_output_files_as_records(tmp_path):
    repo = git_repo(tmp_path, "r", {**LAID_OUT,
        "scripts/readout.py": 'from pathlib import Path\nMARKDOWN_OUTPUT_PATH = Path("generated/plans/007_readout.md")\n',
        "generated/plans/007_readout.md": "x", "generated/other/008_note.md": "x"})
    assert m.layout(str(repo))["findings"] == []


FAKE_CHECKER = '''import sys, pathlib
repo = pathlib.Path(sys.argv[sys.argv.index("--repo") + 1])
assert "--arc42" in sys.argv
verdict = (repo / "verdict.txt").read_text().strip()
if verdict == "bad":
    print("FINDING TRACE-NO-CHECK role=system_model id=T1 file=docs/model/trace.yaml: rule has no check")
    sys.exit(1)
if verdict == "invalid":
    print("durable-docs: invalid input: no durable_documents block", file=sys.stderr)
    sys.exit(2)
'''


def test_durable_undeclared_ok_findings_and_invalid(tmp_path):
    checker = tmp_path / "fake_check.py"
    checker.write_text(FAKE_CHECKER)
    plain = git_repo(tmp_path, "plain", {".agentic/repo.yaml": REPO_YAML, "verdict.txt": "bad"})
    assert m.durable(str(plain), checker=str(checker))["status"] == "undeclared"  # no block: never run, never failing
    declared = {".agentic/repo.yaml": REPO_YAML + "durable_documents:\n  schema_version: '0.1'\n"}
    good = git_repo(tmp_path, "good", {**declared, "verdict.txt": "good"})
    assert m.durable(str(good), checker=str(checker)) == {"status": "ok", "findings": [], "detail": ""}
    bad = m.durable(str(git_repo(tmp_path, "bad", {**declared, "verdict.txt": "bad"})), checker=str(checker))
    assert bad["status"] == "findings" and bad["findings"] == [
        "FINDING TRACE-NO-CHECK role=system_model id=T1 file=docs/model/trace.yaml: rule has no check"]
    invalid = m.durable(str(git_repo(tmp_path, "inv", {**declared, "verdict.txt": "invalid"})), checker=str(checker))
    assert invalid["status"] == "findings" and "exit 2" in invalid["detail"] and "no durable_documents block" in invalid["detail"]


def test_durable_checks_the_ref_and_leaves_no_worktree(tmp_path, monkeypatch):
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path / "t"))
    checker = tmp_path / "fake_check.py"
    checker.write_text(FAKE_CHECKER)
    declared = {".agentic/repo.yaml": REPO_YAML + "durable_documents:\n  schema_version: '0.1'\n"}
    repo = git_repo(tmp_path, "r", {**declared, "verdict.txt": "good"})
    (repo / "verdict.txt").write_text("bad")  # uncommitted edit: the check reads the ref, not the working tree
    assert m.durable(str(repo), "HEAD", checker=str(checker))["status"] == "ok"
    listed = subprocess.run(["git", "-C", str(repo), "worktree", "list"], capture_output=True, text=True).stdout
    assert len(listed.strip().splitlines()) == 1
    assert list((tmp_path / "t" / "md-file-cap").iterdir()) == []  # its clone is gone after a normal run


SLOW_CHECKER = '''import os, pathlib, time
pathlib.Path(os.environ["SLOW_STARTED"]).write_text(str(os.getpid()))
time.sleep(60)
'''


@pytest.mark.parametrize("how", ["SIGTERM", "SIGKILL"])
def test_killed_run_registers_no_worktree_and_its_leftover_is_swept(tmp_path, monkeypatch, how):
    """A hook timeout killed runs mid-check and left registered worktrees on lockstep (2026-11-07)."""
    declared = {".agentic/repo.yaml": REPO_YAML + "durable_documents:\n  schema_version: '0.1'\n", "verdict.txt": "good"}
    repo = git_repo(tmp_path, "r", declared)
    slow, started, t = tmp_path / "slow_check.py", tmp_path / "started", tmp_path / "t"
    slow.write_text(SLOW_CHECKER)
    t.mkdir()
    env = {**os.environ, "DURABLE_DOCS_CHECK": str(slow), "SLOW_STARTED": str(started), "TMPDIR": str(t)}
    proc = subprocess.Popen([sys.executable, m.__file__, "--repo", str(repo), "--ref", "HEAD"], env=env,
                            start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + 30
    while not started.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    assert started.exists(), "the checker never started"
    if how == "SIGTERM":
        proc.send_signal(signal.SIGTERM)  # what a caller's timeout sends
    else:
        os.killpg(proc.pid, signal.SIGKILL)  # the whole process group, with no chance to clean up
    assert proc.wait(timeout=30) == (128 + signal.SIGTERM if how == "SIGTERM" else -signal.SIGKILL)
    listed = subprocess.run(["git", "-C", str(repo), "worktree", "list"], capture_output=True, text=True).stdout
    assert len(listed.strip().splitlines()) == 1  # nothing registered on the checked repository either way
    left = list((t / "md-file-cap").iterdir())
    if how == "SIGTERM":
        assert left == []  # the signal unwound into durable()'s finally
        return
    assert len(left) == 1
    fast = tmp_path / "fake_check.py"
    fast.write_text(FAKE_CHECKER)
    monkeypatch.setattr(tempfile, "tempdir", str(t))
    assert m.durable(str(repo), "HEAD", checker=str(fast))["status"] == "ok"
    assert list((t / "md-file-cap").iterdir()) == left  # too young to be a leftover: a run may still be using it
    old = time.time() - m.STALE_SECONDS - 60
    os.utime(left[0], (old, old))
    assert m.durable(str(repo), "HEAD", checker=str(fast))["status"] == "ok"
    assert list((t / "md-file-cap").iterdir()) == []  # the next run swept the killed run's clone


ORIGIN_CHECKER = '''import os, pathlib, subprocess, sys
repo = sys.argv[sys.argv.index("--repo") + 1]
seen = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "--quiet", "refs/remotes/origin/main"],
                      capture_output=True, text=True).stdout.strip()
pathlib.Path(os.environ["SEEN_ORIGIN_MAIN"]).write_text(seen)
'''


def rev(path, ref):
    return subprocess.run(["git", "-C", str(path), "rev-parse", ref], capture_output=True, text=True, check=True).stdout.strip()


def test_durable_clone_origin_main_is_the_sources_github_main_not_its_local_main(tmp_path, monkeypatch):
    """plan-code-wiki's local main sat at 581d610 for weeks while its origin/main moved on. In the shared clone
    origin/main was that stale local main, so lockstep's `make check` (`pcw check --base $(git merge-base
    origin/main HEAD)`) blocked on 102 files the checked revision never changed (2026-11-07)."""
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path / "t"))
    checker, seen = tmp_path / "origin_check.py", tmp_path / "seen"
    checker.write_text(ORIGIN_CHECKER)
    monkeypatch.setenv("SEEN_ORIGIN_MAIN", str(seen))
    declared = {".agentic/repo.yaml": REPO_YAML + "durable_documents:\n  schema_version: '0.1'\n"}
    github = git_repo(tmp_path, "github", {**declared, "a.txt": "1"})
    subprocess.run(["git", "-C", str(github), "branch", "-M", "main"], check=True)
    src = tmp_path / "src"
    subprocess.run(["git", "clone", "-q", str(github), str(src)], check=True)
    (github / "a.txt").write_text("2")
    subprocess.run(["git", "-C", str(github), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "b"], check=True)
    subprocess.run(["git", "-C", str(src), "fetch", "-q", "origin"], check=True)  # local main now lags origin/main
    assert rev(src, "refs/heads/main") != rev(src, "refs/remotes/origin/main")
    assert m.durable(str(src), "HEAD", checker=str(checker))["status"] == "ok"
    assert seen.read_text() == rev(src, "refs/remotes/origin/main")


def test_durable_clone_of_a_repo_without_remote_tracking_refs_still_runs(tmp_path, monkeypatch):
    """The mirror fetch matches nothing here; that must not fail the check, and origin/main stays the local main."""
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path / "t"))
    checker, seen = tmp_path / "origin_check.py", tmp_path / "seen"
    checker.write_text(ORIGIN_CHECKER)
    monkeypatch.setenv("SEEN_ORIGIN_MAIN", str(seen))
    declared = {".agentic/repo.yaml": REPO_YAML + "durable_documents:\n  schema_version: '0.1'\n"}
    repo = git_repo(tmp_path, "r", declared)
    subprocess.run(["git", "-C", str(repo), "branch", "-M", "main"], check=True)
    assert subprocess.run(["git", "-C", str(repo), "for-each-ref", "refs/remotes"], capture_output=True, text=True).stdout == ""
    assert m.durable(str(repo), "HEAD", checker=str(checker)) == {"status": "ok", "findings": [], "detail": ""}
    assert seen.read_text() == rev(repo, "refs/heads/main")


def test_checker_copy_is_reused_by_content_hash(tmp_path, monkeypatch):
    """One cached copy per checker version, not one temp folder per run (160 leaked in a day, 2026-11-07)."""
    cp = git_repo(tmp_path, "cp", {m.CHECKER_REL: "print('v1')\n", m.SCHEMA_REL: "{}\n"})
    graph = tmp_path / "graph.json"
    graph.write_text(json.dumps([{"id": "company-planning", "path": str(cp)}]))
    (tmp_path / "t").mkdir()
    monkeypatch.delenv("DURABLE_DOCS_CHECK", raising=False)
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path / "t"))
    root = tmp_path / "cache" / "md-file-cap"
    unused = root / "durable-checker-0000000000000000"  # an older version nobody has used for a day
    unused.mkdir(parents=True)
    os.utime(unused, (time.time() - 86400, time.time() - 86400))
    recent = root / "durable-checker-1111111111111111"  # another version a concurrent run may be using
    recent.mkdir()
    monkeypatch.setattr(m, "_checker", {})
    first = m.resolve_checker(str(graph))
    monkeypatch.setattr(m, "_checker", {})
    assert m.resolve_checker(str(graph)) == first
    assert Path(first).read_text() == "print('v1')\n"
    assert (root / Path(first).relative_to(root).parts[0] / m.SCHEMA_REL).read_text() == "{}\n"
    assert sorted(p.name for p in root.iterdir()) == sorted([Path(first).relative_to(root).parts[0], recent.name])
    assert list((tmp_path / "t").iterdir()) == []  # nothing left in the temp folder


def test_repo_yaml_without_authorities_leaves_layout_undeclared(tmp_path):
    repo = git_repo(tmp_path, "r", {".agentic/repo.yaml": "durable_documents:\n  schema_version: '0.1'\n",
                                    "docs/decisions/ADR-1-a.md": "x"})
    assert m.layout(str(repo))["status"] == "undeclared"


def test_exception_file_with_only_unlinked_ok_raises_no_limit(tmp_path):
    """An exception file that only lists unlinked_ok entries is valid; the plain cap applies."""
    only_unlinked = "unlinked_ok:\n  - path: raw/sources/\n    reason: source material\n"
    fits = make_repo(tmp_path, "fits", 5, only_unlinked)
    grown = make_repo(tmp_path, "grown", 6, only_unlinked)
    rows = run(tmp_path, [
        {"github_repo": "BrianMills2718/fits", "path": str(fits)},
        {"github_repo": "BrianMills2718/grown", "path": str(grown)},
    ])
    assert (rows["BrianMills2718/fits"]["status"], rows["BrianMills2718/fits"]["detail"]) == ("ok", "")
    assert rows["BrianMills2718/grown"]["status"] == "over"
    assert "> cap 5" in rows["BrianMills2718/grown"]["detail"]


@pytest.fixture(autouse=True)
def _graph_owner(monkeypatch):
    """The checks cover one GitHub owner, named by the graph's settings; these tests use a temporary graph with none."""
    monkeypatch.setenv("PROJECT_GRAPH_OWNER", "BrianMills2718")


@pytest.mark.req("project-graph-config/owner-from-config")
def test_owner_is_read_from_the_settings_beside_the_graph(tmp_path, monkeypatch):
    monkeypatch.delenv("PROJECT_GRAPH_OWNER")
    (tmp_path / "graph-config.yaml").write_text("owner: someone\nother: x\n")
    assert m.graph_owner(str(tmp_path / "PROJECT_GRAPH.json")) == "someone"


@pytest.mark.req("project-graph-config/no-owner-fails-loudly")
def test_no_owner_named_fails_loudly(tmp_path, monkeypatch):
    monkeypatch.delenv("PROJECT_GRAPH_OWNER")
    with pytest.raises(SystemExit, match="PROJECT_GRAPH_OWNER"):
        m.graph_owner(str(tmp_path / "PROJECT_GRAPH.json"))


def test_generated_md_not_counted(tmp_path):
    """Generator output under generated/ is not counted; a docs/ file is (Brian, 2026-11-17)."""
    path = make_repo(tmp_path, "gen", 0)
    (path / "generated").mkdir()
    (path / "generated" / "x.md").write_text("x")
    (path / "docs").mkdir()
    (path / "docs" / "x.md").write_text("x")
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(path), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "more"], check=True)
    assert m.count_md(str(path)) == 1


def test_tool_generated_openspec_skill_copies_are_not_counted(tmp_path):
    # `openspec init --tools claude,codex` writes the same OpenSpec skills into .claude/ and .agents/;
    # they are generator output, like generated/ (Brian, 2026-11-17, "skip generated").
    repo = git_repo(tmp_path, "r", {
        "docs/a.md": "x",
        ".claude/skills/openspec-propose/SKILL.md": "x",
        ".agents/skills/openspec-propose/SKILL.md": "x",
        ".claude/commands/opsx/propose.md": "x",
        ".claude/skills/my-own-skill/SKILL.md": "a hand-written skill still counts",
        ".claude/commands/review.md": "a hand-written command still counts",
    })
    assert m.count_md(str(repo), "HEAD") == 3


def test_archived_openspec_change_is_not_counted(tmp_path):
    # The archived change stays only for the merge that archives it, then is removed; its specs are counted in
    # openspec/specs/ (inferred by agent, 2026-11-24).
    repo = git_repo(tmp_path, "r", {
        "docs/a.md": "x",
        "openspec/specs/core/spec.md": "x",
        "openspec/changes/archive/2026-11-24-x/proposal.md": "x",
        "openspec/changes/archive/2026-11-24-x/specs/core/spec.md": "x",
        "openspec/changes/live-change/proposal.md": "an unarchived change still counts",
    })
    assert m.count_md(str(repo), "HEAD") == 3


@pytest.mark.req("lockstep-wiki/generated-wiki-pages-need-no-layout-row")
def test_generated_wiki_pages_are_not_counted_and_other_generated_names_stay_narrow(tmp_path):
    """The generated wiki pages (`generated/wiki/`) are not counted; a Markdown file beside them under docs/ is."""
    repo = git_repo(tmp_path, "w", {"generated/wiki/index.md": "x", "generated/wiki/core.md": "x", "docs/generated/wiki/a.md": "x"})
    assert m.count_md(str(repo), "HEAD") == 1
