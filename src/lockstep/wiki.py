"""Build wiki pages from the plan, the evidence standing and the code docstrings.

Called from a mkdocs-gen-files script, so pages exist only at build time and
cannot drift from the plan: there is no hand-written copy to go stale. Code
pages use mkdocstrings, which renders the same docstrings `cog` projected.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:wiki.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/old-route-checks-stay-while-a-repository-runs-them

### Requirement: Old-route checks stay while a repository runs them

For a repository with `.aes/target.yaml`, Lockstep SHALL keep the checks that plan route uses, each importable as
`lockstep.<name>` and `pcw.<name>`, and runnable as `python -m` under both names where it has a command line:
`action_check`, `behavior_check`, `change_list`, `change_log`, `criterion_checks`, `declared_reason`,
`docstring_up`, `linked_tests`, `plan_edit`, `plan_to_code`, `requirement_status`, `unplanned_symbols`, `wiki` and
`wiki_reach`. One SHALL be retired, with a dated record under
`docs/retired/`, only once no repository in `~/code2` runs it (code2-workspace decision 0009: `.aes/target.yaml`
retires one repository at a time).

Source: Brian, 2026-11-23: "i approve", to Q54 in `docs/planning/open-questions.json` ("write one requirement for
the ones the core calls; retire the rest"); the 2026-11-23 search found all 14 still run, so none retired (inferred by
agent from that search).

#### Scenario: An AES-plan repository's checks still run

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** its Makefile or edit hook runs one of the 14 checks
- **THEN** the check runs as before, as each module's own tests show

Tested by: tests/lockstep/test_lockstep_wiki_reach.py
[[[end]]] (sum: HR42zobiWc)
"""

from __future__ import annotations

from pathlib import Path

from lockstep.aes_bridge import target
from lockstep.change_log import entries, render
from lockstep.requirement_status import requirement_pages, requirement_status


def _source_base(root: Path, revision: str) -> str | None:
    """Where a repository file is linked to: `repo_url` in mkdocs.yml, else the GitHub `origin`, at this commit; None if neither."""
    import re
    import subprocess

    url = None
    mk = root / "mkdocs.yml"
    if mk.exists():
        m = re.search(r"^repo_url:\s*['\"]?([^'\"\s]+)", mk.read_text(encoding="utf-8"), re.M)  # a YAML key, not prose
        url = m.group(1) if m else None
    if url is None:
        try:
            origin = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"],
                                    capture_output=True, text=True, timeout=10).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            origin = ""
        m = re.match(r"^(?:https://|git@)github\.com[:/]([^/]+/[^/]+?)(?:\.git)?/?$", origin)
        url = f"https://github.com/{m.group(1)}" if m else None
    return f"{url.rstrip('/')}/blob/{revision or 'HEAD'}/" if url else None


def _file_link(root: Path, base: str | None, path: str) -> str:
    """A repository file as a Markdown link named by its path: to the hosted copy at this commit, or to the file on disk."""
    if not path:
        return "(no path)"
    return f"[{path}]({base + path if base else (root / path).resolve().as_uri()})"


def pages(root: Path, package: str) -> dict[str, str]:
    tgt, status = target(root), requirement_status(root)
    by_id = {kind: {x["id"]: x for x in tgt.get(kind) or []}
             for kind in ("outcomes", "normative_items", "success_criteria", "components",
                          "planned_artifacts", "verification_subjects")}
    criteria, artifacts, gaps = status["criteria"], status["artifacts"], status["gaps"]  # behavior 4.1
    drift = status["drift"]
    failing = sum(d["failing"] for ds in drift.values() for d in ds)
    base = _source_base(root, status["revision"])
    link = lambda path: _file_link(root, base, path)  # noqa: E731

    # Behavior 6.1: each section is the question it answers; each entry links down to the page, plan or code.
    out: dict[str, str] = {}
    idx = [f"# {tgt.get('target_id', 'Project')}", "",
           f"Generated from `.aes/target.yaml` and `aes reconcile` at commit `{status['revision'][:12]}`"
           + (" (uncommitted changes present)" if status["dirty"] else "") + ". Edit the plan, not this page.",
           "Start from your question; each line links to the page that answers it, and each page links to the plan "
           f"({link('.aes/target.yaml')}) and the files.", "",
           "## What must this project do, and is each requirement met?", ""]
    for o in by_id["outcomes"].values():  # behavior 4.1: one page per requirement, with its status and change log
        idx += [f"- [{o['id']}](requirements/{o['id']}.md) — for {o['actor_or_consumer']}: {o['statement']}"]
    idx += ["", "## Which files do each part of the plan, and does their test prove it?", ""]
    for cid, c in by_id["components"].items():
        idx += [f"- [{cid}](components/{cid}.md) — {c['responsibility']} ({len(gaps.get(cid, []))} open gap(s))"]
    idx += ["", "## Does the code still match the plan?", "",
            f"{failing} failing difference(s) at this commit (AES `characterize`); each component page lists its own."]
    idx += [f"- {link(d['path'])}: {d['detail']}" for d in drift.get("", [])]
    idx += ["", "## What does the code say, file by file?", "",
            f"- [`{package}` reference](code.md) — rendered from the docstrings, which carry the projected plan text"]
    log = entries(root)  # behavior 4.2
    idx += ["", "## What changed in the plan, and when?", "",
            f"- [Change log](change-log.md) — every accepted change to the plan, newest first ({len(log)} entries)"]
    out["index.md"] = "\n".join(idx) + "\n"
    out["change-log.md"] = render(log)

    for cid, c in by_id["components"].items():
        p = [f"# {cid}: {c['responsibility']}", "", f"Plan: {link('.aes/target.yaml')} (component {cid}).", ""]
        for ref in c.get("target_refs", []):
            ni = by_id["normative_items"].get(ref)
            if ni:
                p += [f"**{ni['id']}** (requirement): {ni['statement'].strip()}", ""]
                for sc in by_id["success_criteria"].values():
                    if ref in sc.get("target_refs", []):
                        st = criteria.get(sc["id"], {})
                        p += [f"**{sc['id']}** — {sc['statement'].strip()}", "",
                              f"- Disproved if: {sc['disproof'].strip()}",
                              f"- Standing now: **{st.get('standing', 'unknown')}**"]
                        tests = [str(vs["locator"]).split("::")[0] for vs in by_id["verification_subjects"].values()
                                 if sc["id"] in vs.get("criterion_refs", []) and vs.get("locator")]
                        if tests:
                            p += ["- Proven by: " + ", ".join(link(t) for t in dict.fromkeys(tests))]
                        for m in st.get("missing", []):
                            p += [f"    - {m['er_id']}: {m['status']} — {m['detail']}"]
                        p += [""]
        files = []
        for aid in c.get("planned_artifact_refs", []):
            art, st = by_id["planned_artifacts"].get(aid, {}), artifacts.get(aid, {})
            files.append(f"{link((art.get('locator') or {}).get('exact_path', ''))} ({aid}, {st.get('status', '').lower()})")
        p += ["**Files:** " + "; ".join(files), ""]
        found = [f"{link(d['path'])} ({aid}) {d['kind']}: {d['detail']}"
                 for aid in c.get("planned_artifact_refs", []) for d in drift.get(aid, [])]
        p += ["**Drift between plan and code:** " + ("; ".join(found) if found else "none"), ""]
        open_gaps = [f"{g['kind']}: {g['detail']}" for g in gaps.get(cid, [])]
        p += ["**Open gaps:** " + ("; ".join(open_gaps) if open_gaps else "none")]
        out[f"components/{cid}.md"] = "\n".join(p) + "\n"

    out.update({k: v for k, v in requirement_pages(root, status).items() if k.startswith("requirements/")})
    out["code.md"] = f"# Code reference\n\nRendered from the docstrings in the code.\n\n::: {package}\n"
    return out


def main() -> int:
    """`python -m lockstep.wiki [PACKAGE]`: print the wiki pages as plain text (what an agent reads first)."""
    import sys

    from lockstep.aes_bridge import find_root

    root = find_root(Path.cwd())
    if root is None:
        print("no .aes/project.yaml here or above", file=sys.stderr)
        return 1
    package = sys.argv[1] if len(sys.argv) > 1 else "src"
    for name, text in pages(root, package).items():
        if name != "code.md":
            print(f"===== wiki/{name}\n{text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
