"""AES's `lockstep.yaml` plans every tracked file, governs every top-level entry and shows the plan as a page."""

from pathlib import Path
import subprocess

import pytest
import yaml

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
    top = {p.split("/", 1)[0] + ("/" if "/" in p else "") for p in tracked}
    assert not top - set(side.get("governed") or []), f"top-level entries not governed: {sorted(top - set(side.get('governed') or []))}"
    catalog = [r for r in side.get("projections") or [] if r.get("target") == "generated/files.md"]
    assert catalog and catalog[0].get("items") == "layout" and catalog[0].get("key") == "path"
    assert "generated/files.md" not in project.project(ROOT, check=True), "generated/files.md is stale; run lockstep project"
    assert "generated/files.md" in (ROOT / "wiki/index.md").read_text()
