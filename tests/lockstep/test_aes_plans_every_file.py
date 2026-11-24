"""AES's `lockstep.yaml` plans every tracked file, governs every top-level entry and shows the plan as a page."""

from pathlib import Path
import subprocess

import pytest
import yaml

from lockstep.aes_bridge import is_governed, under_governed
from lockstep.checks import project

ROOT = Path(__file__).resolve().parents[2]


def _git(*args: str) -> list[str]:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout.splitlines()


@pytest.mark.req("lockstep-plan-format/every-tracked-file-has-a-planned-row-and-the-catalog-page-is-current")
def test_every_tracked_file_has_a_planned_row_and_the_catalog_page_is_current():
    side = yaml.safe_load((ROOT / "lockstep.yaml").read_text())
    tracked = set(_git("ls-files"))
    rows = {row["path"]: row for row in side.get("layout") or []}
    assert tracked
    assert not tracked - set(rows), f"tracked files with no layout row: {sorted(tracked - set(rows))[:20]}"
    assert not [p for p in tracked if not str(rows[p].get("purpose") or "").strip()], "layout rows without a purpose"
    assert "." in (side.get("governed") or []), "AES governs the whole repository"
    for new in ("brand-new-folder/a.py", "new-top-level-file.json", "docs/new-page.md"):
        assert is_governed(ROOT, new), f"a new {new} would not be reported"
    catalog = [r for r in side.get("projections") or [] if r.get("target") == "generated/files.md"]
    assert catalog and catalog[0].get("items") == "layout" and catalog[0].get("key") == "path"
    assert "generated/files.md" not in project.project(ROOT, check=True), "generated/files.md is stale; run lockstep project"
    assert "generated/files.md" in (ROOT / "wiki/index.md").read_text()


@pytest.mark.req("lockstep-plan-format/a-governed-entry-covers-what-it-names")
def test_a_governed_entry_covers_what_it_names():
    assert under_governed("src/a/b.py", "src/") and not under_governed("srcx/b.py", "src/")
    assert under_governed("anything/at/all.txt", ".") and under_governed("top.json", "./")
    assert under_governed("Makefile", "Makefile") and not under_governed("Makefile.bak", "Makefile")
    assert under_governed("src/lockstep/x.py", "src/lockstep") and not under_governed("src/lockstep_old.py", "src/lockstep")
