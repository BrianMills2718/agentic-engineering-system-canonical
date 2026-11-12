"""A4 run: `lockstep layout` on an approved plan, then each planned file's first docstring against the plan.

Writes docs/planning/runs/lockstep-acceptance/a4.json. The plan is OpenSpec requirements plus `layout:` rows in
lockstep.yaml, committed (the approval) before any planned file exists. Starts from Lockstep's own layout example
(tests/lockstep/example-layout) and adds a second requirement with two scenarios and a second planned file.
"""

import ast
import datetime as dt
import re
import shutil
import tempfile
from pathlib import Path

import yaml

from _common import BIN, ROOT, Trace, git, tree

EXAMPLE = ROOT / "tests/lockstep/example-layout"
SECOND_REQUIREMENT = '''
### Requirement: Greet politely

Source: inferred by agent, a second requirement so the run has two planned source files.

`greet_politely(name)` SHALL return `Good day, <name>.`.

#### Scenario: A name is greeted politely

- **GIVEN** the name `Ada`
- **WHEN** `greet_politely` is called with it
- **THEN** it returns `Good day, Ada.`

#### Scenario: An empty name is refused

- **GIVEN** the empty name
- **WHEN** `greet_politely` is called with it
- **THEN** it raises `ValueError`
'''
SECOND_ROWS = '''  - path: src/greeter/polite.py
    purpose: the polite greeting
    implements: [greeting/greet-politely]
    tests: [tests/test_polite.py]
    exports: ["greet_politely(name: str) -> str"]
  - path: tests/test_polite.py
    purpose: prove that greet_politely greets politely and refuses an empty name
    implements: [greeting/greet-politely]
'''


def requirements(spec: str) -> dict[str, dict]:
    """Each requirement of the spec: its statement (after the Source line) and its scenarios, as written."""
    out = {}
    for block in re.split(r"(?m)^### Requirement: ", spec)[1:]:
        title, _, rest = block.partition("\n")
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        statement = re.split(r"(?m)^#### Scenario:", rest)[0]
        statement = re.sub(r"(?m)^Source:.*\n", "", statement).strip()
        scenarios = ["#### Scenario:" + s.rstrip() for s in re.split(r"(?m)^#### Scenario:", rest)[1:]]
        out[f"greeting/{slug}"] = {"title": title, "statement": statement, "scenarios": scenarios}
    return out


def main() -> int:
    t = Trace("A4", "After approval, each planned file's first docstring carries the approved text word for word")
    repo = Path(tempfile.mkdtemp(prefix="a4-repo-")) / "greeter"
    shutil.copytree(EXAMPLE, repo)
    spec_path = repo / "openspec/specs/greeting/spec.md"
    spec_path.write_text(spec_path.read_text().rstrip() + "\n" + SECOND_REQUIREMENT)
    (repo / "lockstep.yaml").write_text((repo / "lockstep.yaml").read_text().rstrip() + "\n" + SECOND_ROWS)
    (repo / ".gitignore").write_text("__pycache__/\n.pcw/\n")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "approve the plan: OpenSpec requirements and layout rows")
    approved_at = git(repo, "log", "-1", "--format=%cI").strip()
    layout = yaml.safe_load((repo / "lockstep.yaml").read_text())["layout"]
    planned = [r["path"] for r in layout]
    t.extra["approval"] = {"commit": git(repo, "rev-parse", "HEAD").strip(), "committed_at": approved_at,
                           "files_in_the_approval_commit": git(repo, "ls-files").split()}
    t.extra["files_before_layout"] = tree(repo)
    t.extra["planned_files_existing_before_layout"] = {p: (repo / p).exists() for p in planned}
    step = t.run("lockstep layout", [str(BIN / "lockstep"), "layout"], repo)
    t.extra["files_after_layout"] = tree(repo)
    reqs = requirements(spec_path.read_text())
    t.extra["approved_requirements"] = reqs

    for row in layout:
        path = row["path"]
        file = repo / path
        mtime = dt.datetime.fromtimestamp(file.stat().st_mtime, dt.timezone.utc) if file.exists() else None
        doc = (ast.get_docstring(ast.parse(file.read_text()), clean=False) or "") if file.exists() else ""
        want = reqs[row["implements"][0]]
        parts = {"requirement text": [want["statement"]], "success criteria (scenarios)": want["scenarios"]}
        if row.get("tests"):
            parts["test names"] = row["tests"]
        # each piece must appear in the docstring exactly as written in the approved plan (no re-wording, no re-wrapping)
        found = {name: all(piece.strip() in doc for piece in pieces) for name, pieces in parts.items()}
        created = bool(mtime and mtime >= dt.datetime.fromisoformat(approved_at))
        if not created:
            found["file made after the approval"] = False
        missing = [n for n, ok in found.items() if not ok]
        should = "all present word for word: " + ", ".join(parts)
        did = should if not missing else "missing or changed: " + ", ".join(missing)
        t.row(path, f"{path} ({'test' if path.startswith('tests/') else 'source'} file)", should, did, step["name"], {
            "requirement_id": row["implements"][0], "requirement_title": want["title"],
            "requirement_text": want["statement"], "scenarios": want["scenarios"], "test_names": row.get("tests", []),
            "first_docstring": doc, "parts_found": found, "existed_before_layout": False,
            "created_after_approval": created})
    # the approval row: nothing was laid out before the approval
    pre = [p for p, here in t.extra["planned_files_existing_before_layout"].items() if here]
    t.row("approval", "No planned file existed before the plan was approved and the layout ran",
          "none of the planned files existed before", "none of the planned files existed before" if not pre else
          "already existed: " + ", ".join(pre), step["name"],
          {"files_before_layout": t.extra["files_before_layout"], "planned": planned})
    t.write()
    shutil.rmtree(repo.parent, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
