"""Tests for the docmeta check over a repository's wiki/ folder."""

from datetime import date, timedelta

import pytest

from lockstep.checks.cli import run as run_check
from lockstep_checks_support import write, repo  # noqa: F401  (fixture)

TODAY = date.today()


def page(name: str, links: tuple[str, ...] = (), **fields: str) -> str:
    """Build a wiki page with front matter and links to other pages."""
    meta = {"type": "Concept", "title": name, "status": "current", "last_checked": TODAY.isoformat()}
    meta.update(fields)
    head = "".join(f"{k}: {v}\n" for k, v in meta.items() if v is not None and v != "")
    body = "".join(f"- [{t}]({t}.md)\n" for t in links)
    return f"---\n{head}---\n\n# {name}\n\n{body}"


def wiki(root, pages: dict[str, str], index_links: tuple[str, ...]) -> None:
    """Write wiki/index.md (no front matter), wiki/log.md and the given pages."""
    write(root, "wiki/index.md", "# Index\n\n" + "".join(f"* [{t}]({t}.md)\n" for t in index_links))
    write(root, "wiki/log.md", "# Update Log\n\n## 2026-11-05\n* **Creation** | start\n")
    for name, text in pages.items():
        write(root, f"wiki/{name}.md", text)


def run(root, capsys) -> tuple[int, str]:
    """Run the check through the command line and return the exit status and output."""
    code = run_check(["docmeta", "--repo", str(root)])
    return code, capsys.readouterr().out


@pytest.mark.req("lockstep-checks/docmeta-page-without-type-fails")
def test_page_without_type_fails(tmp_path, capsys):
    wiki(tmp_path, {"a": page("a", type="")}, ("a",))
    code, out = run(tmp_path, capsys)
    assert code == 1
    assert "missing_type=1" in out
    assert "wiki/a.md" in out


@pytest.mark.req("lockstep-checks/docmeta-index-and-log-need-no-front-matter")
def test_index_and_log_need_no_front_matter(tmp_path, capsys):
    wiki(tmp_path, {"a": page("a")}, ("a",))
    code, out = run(tmp_path, capsys)
    assert code == 0, out
    assert "pages=1 missing_type=0" in out


@pytest.mark.req("lockstep-checks/docmeta-stale-current-page-fails")
def test_stale_current_page_fails(tmp_path, capsys):
    old = (TODAY - timedelta(days=61)).isoformat()
    ok = (TODAY - timedelta(days=60)).isoformat()
    wiki(tmp_path, {"a": page("a", last_checked=old), "b": page("b", last_checked=ok)}, ("a", "b"))
    code, out = run(tmp_path, capsys)
    assert code == 1
    assert "stale=1" in out
    assert "wiki/a.md" in out and "wiki/b.md" not in out


@pytest.mark.req("lockstep-checks/docmeta-superseded-page-without-successor-fails")
def test_superseded_page_without_successor_fails(tmp_path, capsys):
    wiki(tmp_path, {"a": page("a", status="superseded"), "b": page("b", status="superseded", successor="wiki/a.md")}, ("a", "b"))
    code, out = run(tmp_path, capsys)
    assert code == 1
    assert "superseded_without_successor=1" in out
    assert "wiki/a.md" in out and "wiki/b.md" not in out


@pytest.mark.req("lockstep-checks/docmeta-two-owners-of-one-topic-fail")
def test_two_owners_of_one_topic_fail(tmp_path, capsys):
    wiki(tmp_path, {"a": page("a", source_of_truth_for="[system-model, names]"),
                    "b": page("b", source_of_truth_for="[system-model]")}, ("a", "b"))
    code, out = run(tmp_path, capsys)
    assert code == 1
    assert "topics_with_two_owners=1" in out
    line = next(ln for ln in out.splitlines() if "system-model" in ln)
    assert "wiki/a.md" in line and "wiki/b.md" in line


@pytest.mark.req("lockstep-checks/docmeta-page-three-links-away-fails")
def test_page_three_links_away_fails(tmp_path, capsys):
    wiki(tmp_path, {"a": page("a", ("b",)), "b": page("b", ("c",)), "c": page("c")}, ("a",))
    code, out = run(tmp_path, capsys)
    assert code == 1
    assert "beyond_two_links=1" in out
    findings = [ln for ln in out.splitlines() if not ln.startswith("docmeta:")]
    assert findings and all("wiki/c.md" in ln for ln in findings)


@pytest.mark.req("lockstep-checks/docmeta-unknown-status-fails")
def test_unknown_status_fails(tmp_path, capsys):
    wiki(tmp_path, {"a": page("a", status="draft")}, ("a",))
    code, out = run(tmp_path, capsys)
    assert code == 1
    assert "invalid_field=1" in out


@pytest.mark.req("lockstep-checks/docmeta-clean-wiki-passes")
def test_clean_wiki_passes(tmp_path, capsys):
    write(tmp_path, "wiki/sub/deep.md", page("deep", extra_key="kept"))
    wiki(tmp_path, {"a": page("a", source_of_truth_for="[system-model]") + "- [deep](/sub/deep.md)\n",
                    "old": page("old", status="history", last_checked="2020-01-01")}, ("a",))
    code, out = run(tmp_path, capsys)
    assert code == 0, out
    assert out.splitlines()[0] == ("docmeta: pages=3 missing_type=0 stale=0 superseded_without_successor=0 "
                                   "topics_with_two_owners=0 beyond_two_links=0 invalid_field=0")


@pytest.mark.req("lockstep-checks/docmeta-repository-without-wiki-passes")
def test_repository_without_wiki_passes(tmp_path, capsys):
    code, out = run(tmp_path, capsys)
    assert code == 0
    assert out.startswith("docmeta: pages=0 ")
