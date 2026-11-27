"""Projection: write each requirement's text into the docstrings that implement it, and each plan's coverage into the plan.

Implements: lockstep-projection/requirement-text-is-written-into-the-implementing-docstring,
    lockstep-projection/status-flows-back-into-the-plan

Requirement text (generated):
    lockstep-projection/requirement-text-is-written-into-the-implementing-docstring: `lockstep check
        project` SHALL write the text of each requirement a docstring implements, word for word, in
        a marked block under its `Implements:` line, and `lockstep check project --check` SHALL fail
        when a block differs from the spec, writing nothing. It SHALL print one `rewrote <path>`
        line per file it rewrote. It SHALL preserve unrelated Python source and remain idempotent.
        In a repository with a layout plan it SHALL also rewrite each planned file's cog plan copy
        from the plan, SHALL write no block inside that copy, and SHALL do both even when no
        requirement statement text was read.
    lockstep-projection/status-flows-back-into-the-plan: `lockstep check project` SHALL write a
        generated status block into each plan that has a `Closes:` line, listing each ID with its
        implementers and tests, and `--check` SHALL fail when the block is stale. A block written by
        code2check SHALL be replaced, not left beside the new one.


[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:project.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-projection/requirement-text-is-written-into-the-implementing-docstring, lockstep-projection/status-flows-back-into-the-plan, lockstep-projection/a-fixed-planned-file-without-a-plan-copy-is-reported, lockstep-plan-format/a-layout-repository-generates-one-wiki-page-per-capability, lockstep-plan-format/project-check-fails-on-stale-or-unreachable-wiki-pages

### Requirement: Requirement text is written into the implementing docstring

`lockstep check project` SHALL write the text of each requirement a docstring implements, word for word, in a marked block under its `Implements:` line, and `lockstep check project --check` SHALL fail when a block differs from the spec, writing nothing. It SHALL print one `rewrote <path>` line per file it rewrote. It SHALL preserve unrelated Python source and remain idempotent. In a repository with a layout plan it SHALL also rewrite each planned file's cog plan copy from the plan, SHALL write no block inside that copy, and SHALL do both even when no requirement statement text was read.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Opening quote line declarations receive canonical text

- **GIVEN** a docstring whose `Implements:` content starts on the opening quote line
- **WHEN** `project` runs
- **THEN** the text is written under it, other source is unchanged, and a second run changes nothing

#### Scenario: Projection rewrites the block

- **GIVEN** a spec requirement is reworded after its block was written
- **WHEN** `project` runs
- **THEN** the block holds the new wording once

#### Scenario: Stale requirement text fails the check

- **GIVEN** a block differs from the spec
- **WHEN** `project --check` runs
- **THEN** it exits 1, names the file and writes nothing

#### Scenario: A planned file's plan copy follows a reworded requirement

- **GIVEN** a layout repository whose planned file's cog plan copy is current, and its requirement is then reworded
- **WHEN** the edit hook judges the file, then `project` runs, then runs again
- **THEN** the hook finds it stale, `project` rewrites the copy with the new wording and no generated block inside it, and the second run changes nothing

### Requirement: Status flows back into the plan

`lockstep check project` SHALL write a generated status block into each plan that has a `Closes:` line, listing each ID with its implementers and tests, and `--check` SHALL fail when the block is stale. A block written by code2check SHALL be replaced, not left beside the new one.

Source: Brian, 2026-11-11: "i approve single tool desing re d4"; proposals/one-planning-tool/DESIGN.md, slice 6 ("Requirement text in docstrings" and "Status per requirement" rows)

#### Scenario: Plan block lists coverage

- **GIVEN** a plan with a `Closes:` line
- **WHEN** `project` runs
- **THEN** a block after the `Closes:` paragraph lists each ID's implementers and tests

#### Scenario: A plan block written by code2check is replaced not duplicated

- **GIVEN** a plan holds a code2check status block
- **WHEN** `project` runs
- **THEN** one lockstep block remains and no code2check marker

### Requirement: A fixed planned file without a plan copy is reported

`lockstep check project`, with or without `--check`, SHALL print `no-copy <path>` for each `layout:` row whose path
matches a `fixed:` glob in `lockstep.yaml`, names an existing Python file, and whose file holds no cog plan copy
naming that row's ID, and SHALL then exit 1. A row outside every `fixed:` glob SHALL NOT be reported.

Source: Brian, 2026-11-23: "i approve", to Q53 in `docs/planning/open-questions.json` ("Should `make check` fail
when a docstring's plan copy is stale or a `fixed:` file has no copy block?"; alignment cleanup item 14).

#### Scenario: A fixed file with no plan copy fails the check

- **GIVEN** `fixed: ["src/greeter/*"]` and a layout row for `src/greeter/__init__.py` whose file has a docstring with no cog plan copy
- **WHEN** `lockstep check project --check` runs
- **THEN** it prints `no-copy src/greeter/__init__.py` and exits 1, and once the file holds the copy that `lockstep layout` writes it reports nothing for that file

### Requirement: A layout repository generates one wiki page per capability

In a layout repository whose `lockstep.yaml` says `generated_wiki: true`, `lockstep check project` SHALL write `generated/wiki/index.md`, with one line per OpenSpec capability (its summary and a link to its page), and `generated/wiki/<capability>.md` for each capability. A capability page SHALL list each requirement's text, the symbols whose docstrings implement it with their `file:line`, each scenario with the tests tagged with its ID, and the requirement's coverage state (unimplemented, untested, or implemented and tested). The pages SHALL hold no commit hash and no pass or fail result, so they are the same in every checkout; `lockstep status` gives pass or fail. A page for a capability that no longer exists SHALL be removed.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 1 (restore the dropped wiki generator); told the agent to proceed without waiting. The `generated_wiki` switch, the coverage-only status and the page layout are inferred by agent.

#### Scenario: A capability page shows requirement, code and tests

- **GIVEN** a layout repository with `generated_wiki: true`, a requirement implemented by a function and a scenario with a tagged test
- **WHEN** `lockstep check project` runs
- **THEN** `generated/wiki/index.md` has one line for the capability and its page shows the requirement text, the function with its file and line, and the test

#### Scenario: A repository without the switch gets no pages

- **GIVEN** a layout repository without `generated_wiki`
- **WHEN** `lockstep check project` runs
- **THEN** no `generated/wiki/` folder is written

### Requirement: Project check fails on stale or unreachable wiki pages

`lockstep check project --check` SHALL name each `generated/wiki/` page that differs from what would be written, and SHALL exit 1. It SHALL also report each generated page that is more than two links from the index or whose link has no summary beside it, and exit 1.

Source: Brian, 2026-11-27, plan doc "AES next steps: plan for discussion", Milestone 1 step 1 (restore the dropped wiki generator); told the agent to proceed without waiting. Reusing the existing reachability rule inferred by agent.

#### Scenario: A stale page fails the check

- **GIVEN** committed generated pages and a test added after
- **WHEN** `lockstep check project --check` runs
- **THEN** it names the capability page and exits 1, and it writes nothing

Tested by: tests/lockstep/checks/test_lockstep_check_plugin.py, tests/lockstep/checks/test_lockstep_check_project.py, tests/lockstep/test_lockstep_layout_plan.py, tests/lockstep/test_lockstep_layout_wiki.py

Declares (typed signatures, from the plan):
  wiki_problems(root: Path) -> list[str]
[[[end]]]
"""

import ast
import json
from pathlib import Path
import re
import textwrap

from lockstep.doc_projection import ProjectionError, declarations, render, project_facts
from lockstep.checks.markers import source_dirs
from lockstep.checks.spec import read_plan
from lockstep.checks.status import CLOSES, LINKS_FILE, STATUS_PAGE, Report, links, markdown, plan_files, report

HEADER = "Requirement text (generated):"
START = "<!-- lockstep status: generated by `lockstep check project`; do not edit -->"
END = "<!-- /lockstep status -->"
# Only a block directly after the Closes paragraph is replaced; markers quoted in prose are left alone.
# A block written by code2check (the tool this replaces) is replaced too, not left beside the new one.
_BLOCK = re.compile(r"\A\n*<!-- (?:lockstep|code2check) status:[^\n]*-->\n.*?\n<!-- /(?:lockstep|code2check) status -->\n*", re.DOTALL)
_WIDTH = 100
COG_OPEN = "[[[" + "cog"  # cog's markers, split so cog run over this source does not read them
COG_END = "[[[" + "end" + "]]]"


def _docstring_spans(tree: ast.Module) -> list[tuple[int, int, int, int, str]]:
    """Return AST docstring line/byte-column spans and decoded values, last first."""
    spans = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                value = first.value
                assert value.end_lineno is not None and value.end_col_offset is not None
                spans.append((value.lineno - 1, value.end_lineno - 1,
                              value.col_offset, value.end_col_offset, str(value.value)))
    return sorted(spans, reverse=True)


def _project_docstring(lines: list[str], start: int, end: int, text: dict[str, str], raw: bool = False) -> None:
    """Rewrite the generated block after the `Implements:` paragraph of one docstring, in place.

    The lines are written for the literal they go into: backslashes doubled unless it is a raw string,
    so requirement text such as `C:\\Microsoft\\` decodes to itself and is no invalid escape.
    """
    inside, outside = False, []
    for i in range(start, end):  # an `Implements:` line inside a cog plan copy belongs to that copy, not to this block
        inside = (inside or COG_OPEN in lines[i]) and COG_END not in lines[i]
        if not inside and COG_END not in lines[i]:
            outside.append(i)
    at = next((i for i in outside if lines[i].lstrip().startswith("Implements:")), None)
    if at is None:
        return
    stop = at + 1
    while stop < end and lines[stop].strip():
        stop += 1
    ids = [i.strip() for i in " ".join(lines[at:stop]).split("Implements:", 1)[1].split(",") if i.strip()]
    look = stop
    while look < end and not lines[look].strip():
        look += 1
    if look < end and lines[look].strip() == HEADER:
        last = look + 1
        while last < end and lines[last].strip():
            last += 1
        del lines[stop:last]
    indent = lines[at][: len(lines[at]) - len(lines[at].lstrip())]
    known = [i for i in ids if i in text]
    if not known:
        return
    block = ["", indent + HEADER]
    for ident in known:
        entry = f"{ident}: {text[ident]}"
        block += textwrap.wrap(
            entry if raw else entry.replace("\\", "\\\\"),
            width=_WIDTH,
            initial_indent=indent + "    ",
            subsequent_indent=indent + "        ",
            break_long_words=False,
            break_on_hyphens=False,
        )
    lines[stop:stop] = block


def _plan_copies(root: Path, source: str) -> str:
    """Return source with each cog plan copy re-rendered from the plan, in a repository with a layout.

    The edit hook judges a planned file stale when its copy differs from the plan; this is the rewrite its refusal
    names. A copy whose ID the plan does not have is left alone.
    """
    from lockstep.aes_bridge import context
    from lockstep.check import COG_CALL
    from lockstep.cogtext import render as render_copy
    from lockstep.layout_plan import has_layout

    if not has_layout(root) or COG_OPEN not in source:
        return source
    lines, i = source.split("\n"), 0
    while i < len(lines):
        m = COG_CALL.fullmatch(lines[i]) if COG_OPEN in lines[i] else None
        end = next((k for k in range(i + 1, len(lines)) if COG_END in lines[k]), None) if m else None
        if m is None or end is None:
            i += 1
            continue
        try:
            ctx = context(root, m["id"])
        except RuntimeError:
            i = end + 1
            continue
        pad = " " * int(m["indent"] or 4)
        body = [(pad + line).rstrip() for line in render_copy(ctx)]
        lines[i + 1:end] = body
        i += len(body) + 2
    return "\n".join(lines)


def _source_text(path: Path, text: dict[str, str], root: Path | None = None) -> str:
    """Return the file's content with every generated docstring block rewritten."""
    original = path.read_text()
    if root is not None:
        original = _plan_copies(root, original)
    lines = original.split("\n")
    for start, end, column, end_column, value in _docstring_spans(ast.parse(original, filename=str(path))):
        token = lines[start].encode("utf-8")[column:].decode("utf-8")
        raw = "r" in token[: len(token) - len(token.lstrip("rRbBuUfF"))].lower()
        if value.split("\n", 1)[0].lstrip().startswith("Implements:"):
            raw = False  # rewritten below as a plain `"""` literal, its backslashes doubled
            # Decode through the AST, then move opening-line content onto physical
            # lines the existing renderer handles. Preserve code/comments outside
            # the literal and preserve raw-string/backslash values without executing it.
            prefix = lines[start].encode("utf-8")[:column].decode("utf-8")
            suffix = lines[end].encode("utf-8")[end_column:].decode("utf-8")
            indent = " " * column
            body = value.replace("\\", "\\\\").replace('"""', '\\"""').split("\n")
            replacement = [prefix + '"""', indent + body[0], *body[1:], indent + '"""' + suffix]
            lines[start:end + 1] = replacement
            end = start + len(replacement) - 1
        _project_docstring(lines, start, end, text, raw)
    return "\n".join(lines)


def stale_copy(root: Path, path: Path) -> bool:
    """Say whether a source file's generated requirement text differs from what `project` would write.

    Args:
        root: Repository root.
        path: The file, absolute.

    Returns:
        True for an existing Python file under a source folder whose generated block is stale or missing.
    """
    root, path = root.resolve(), path.resolve()
    if path.suffix != ".py" or not path.is_file():
        return False
    if not any(path.is_relative_to(d.resolve()) for d in source_dirs(root)):
        return False
    text = {**read_plan(root).text, **read_plan(root, changes=True).text}
    try:
        return _source_text(path, text, root) != path.read_text()
    except SyntaxError:
        return False


def _coverage(ident: str, status: Report) -> str:
    """Return one plan block line: the ID's implementers and tests, from the status report."""
    if ident in status.requirements:
        impl = status.requirements[ident].links
        tests = [t for s in status.scenarios.values() if s.requirement == ident for t in s.links]
        parts = ["implemented by " + ", ".join(f"`{x}`" for x in impl) if impl else "not implemented"]
    elif ident in status.scenarios:
        tests, parts = status.scenarios[ident].links, []
    else:
        return f"- `{ident}`: unknown ID"
    tests = list(dict.fromkeys(tests))
    parts.append("tests " + ", ".join(f"`{t}`" for t in tests) if tests else "no tests")
    return f"- `{ident}`: " + "; ".join(parts)


def _plan_text(path: Path, ids: list[str], status: Report) -> str:
    """Return the plan's content with its status block rewritten after the `Closes:` paragraph."""
    original = path.read_text()
    m = CLOSES.search(original)
    assert m is not None  # plan_files listed only files with a Closes: line
    head, tail = original[: m.end()], _BLOCK.sub("", original[m.end() :], count=1).lstrip("\n")
    block = "\n".join([START, "", *(_coverage(i, status) for i in ids), "", END])
    return f"{head}\n\n{block}\n\n{tail}" if tail else f"{head}\n\n{block}\n"


def _ignored(root: Path, rel: Path) -> bool:
    """Whether git ignores rel in root: an ignored status page is build output, so --check does not report it."""
    import subprocess

    try:
        done = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", str(rel)], capture_output=True)
    except OSError:
        return False
    return done.returncode == 0


def missing_copies(root: Path) -> list[str]:
    """List the planned files under a `fixed:` glob that hold no cog plan copy naming their row.

    Implements: lockstep-projection/a-fixed-planned-file-without-a-plan-copy-is-reported

    Requirement text (generated):
        lockstep-projection/a-fixed-planned-file-without-a-plan-copy-is-reported: `lockstep check
            project`, with or without `--check`, SHALL print `no-copy <path>` for each `layout:` row
            whose path matches a `fixed:` glob in `lockstep.yaml`, names an existing Python file,
            and whose file holds no cog plan copy naming that row's ID, and SHALL then exit 1. A row
            outside every `fixed:` glob SHALL NOT be reported.

    Args:
        root: Repository root.

    Returns:
        Row paths, in layout order, of existing Python files matching a `fixed:` glob with no plan copy.
    """
    import fnmatch

    from lockstep.check import COG_CALL
    from lockstep.layout_plan import _data, artifact_id, has_layout, layout_rows

    if not has_layout(root):
        return []
    globs = [str(g) for g in _data(root).get("fixed") or [] if str(g).strip()]
    missing = []
    for row in layout_rows(root):
        rel, path = row["path"], root / row["path"]
        if not rel.endswith(".py") or not path.is_file() or not any(fnmatch.fnmatchcase(rel, g) for g in globs):
            continue
        ids = {m["id"] for line in path.read_text().split("\n") if COG_OPEN in line and (m := COG_CALL.fullmatch(line))}
        if artifact_id(rel) not in ids:
            missing.append(rel)
    return missing


def project(root: Path, check: bool = False) -> list[str]:
    """Bring every generated block up to date, or with check, only list the files that are stale.

    A rewritten docstring moves the lines below it, so when a source file was rewritten the status page and the
    link file are rendered once more from the new lines.

    Args:
        root: Repository root.
        check: Report stale files without writing them.

    Returns:
        Paths relative to root of the files rewritten (or stale), source files first, then plans, then `docs/status.md` and `docs/links.json`.
    """
    changed = _project_once(root, check)
    if not check and any(p.endswith(".py") for p in changed):
        changed += [p for p in _project_once(root, check) if p not in changed]
    return changed


def _project_once(root: Path, check: bool = False) -> list[str]:
    """Bring every generated block up to date, or with check, only list the files that are stale.

    Args:
        root: Repository root.
        check: Report stale files without writing them.

    Returns:
        Paths relative to root of the files rewritten (or stale), source files first, then plans, then `docs/status.md` and `docs/links.json`.
    """
    from lockstep.layout_plan import has_layout

    text = {**read_plan(root).text, **read_plan(root, changes=True).text}
    if not text and not has_layout(root):
        return project_facts(root, check=check)
    page = root / STATUS_PAGE
    if any((root / row['target']).resolve() == page.resolve() for row in declarations(root)):
        raise ProjectionError(f'{STATUS_PAGE} is a full-file coverage projection; choose another fact target')
    # Stage every renderer's output before writing so shared plan targets compose,
    # source docstring facts see the new requirement copy, and errors leave no partial output.
    contents: dict[Path, str] = {}
    for path in sorted(p for d in source_dirs(root) for p in d.rglob("*.py")):
        contents[path] = _source_text(path, text, root)
    status = report(root)
    for rel, ids in plan_files(root):
        path = root / rel
        contents[path] = _plan_text(path, ids, status)
    coverage = report(root, use_results=False)
    if page.parent.is_dir() and not (check and _ignored(root, STATUS_PAGE)):
        contents[page] = markdown(coverage)
    if page.parent.is_dir() and not (check and _ignored(root, LINKS_FILE)):
        contents[root / LINKS_FILE] = json.dumps(links(coverage, root), indent=1) + "\n"
    gone = _wiki(root, coverage, contents, check)
    _results_page(root, status, contents, check)
    facts = project_facts(root, check=check, rendered=render(root, contents))
    if not check:  # remove old pages only once every output rendered and was written
        for rel in gone:
            (root / rel).unlink()
    return facts + gone


def _wiki(root: Path, coverage: Report, contents: dict[Path, str], check: bool) -> list[str]:
    """Add the generated wiki pages to `contents`; return the old pages it no longer writes (the caller removes them).

    Implements: lockstep-plan-format/a-layout-repository-generates-one-wiki-page-per-capability

    Requirement text (generated):
        lockstep-plan-format/a-layout-repository-generates-one-wiki-page-per-capability: In a layout
            repository whose `lockstep.yaml` says `generated_wiki: true`, `lockstep check project`
            SHALL write `generated/wiki/index.md`, with one line per OpenSpec capability (its
            summary and a link to its page), and `generated/wiki/<capability>.md` for each
            capability. A capability page SHALL list each requirement's text, the symbols whose
            docstrings implement it with their `file:line`, each scenario with the tests tagged with
            its ID, and the requirement's coverage state (unimplemented, untested, or implemented
            and tested). The pages SHALL hold no commit hash and no pass or fail result, so they are
            the same in every checkout; `lockstep status` gives pass or fail. A page for a
            capability that no longer exists SHALL be removed.

    Args:
        root: Repository root.
        coverage: The coverage-only report the pages are rendered from.
        contents: The staged outputs, extended in place.
        check: Report without writing or removing.

    Returns:
        Paths relative to root of the pages for capabilities that are gone (removed by `project` unless check).
    """
    from lockstep.layout_wiki import orphan_pages, wiki_contents

    pages = wiki_contents(root, coverage)
    contents.update(pages)
    if pages and not check:
        next(iter(pages)).parent.mkdir(parents=True, exist_ok=True)
    gone = orphan_pages(root, set(pages))
    return [p.relative_to(root).as_posix() for p in gone]


def _results_page(root: Path, status: Report, contents: dict[Path, str], check: bool) -> None:
    """Stage `generated/wiki/results.md` when the wiki is on and git ignores the page; never under --check.

    Implements: lockstep-plan-format/a-generated-wiki-shows-test-results-at-this-checkout

    Requirement text (generated):
        lockstep-plan-format/a-generated-wiki-shows-test-results-at-this-checkout: In a layout
            repository whose `lockstep.yaml` says `generated_wiki: true` and whose git ignores
            `generated/wiki/results.md`, `lockstep check project` SHALL write that page with every
            requirement and scenario and the state `lockstep status` gives them (passing, failing,
            skipped, not run at this revision, untested, unimplemented), a line naming the commit
            the test results are from or why no results were used, and each plan or change whose
            `Closes:` IDs are not all passing with those IDs. `--check` SHALL NOT report the page
            and a run SHALL NOT remove it. When git does not ignore the path the page SHALL NOT be
            written. The committed index SHALL name the page on one line without linking to it.

    Args:
        root: Repository root.
        status: The status report read with test results.
        contents: The staged outputs, extended in place.
        check: Report only; the page is build output, so nothing is staged.
    """
    from lockstep.layout_wiki import RESULTS_PAGE, enabled, results_page

    if not check and enabled(root) and _ignored(root, RESULTS_PAGE):
        (root / RESULTS_PAGE).parent.mkdir(parents=True, exist_ok=True)
        contents[root / RESULTS_PAGE] = results_page(status)


def wiki_problems(root: Path) -> list[str]:
    """List the ways the generated wiki breaks the two-link and summary rule.

    Implements: lockstep-plan-format/project-check-fails-on-stale-or-unreachable-wiki-pages

    Requirement text (generated):
        lockstep-plan-format/project-check-fails-on-stale-or-unreachable-wiki-pages: `lockstep check
            project --check` SHALL name each `generated/wiki/` page that differs from what would be
            written, and SHALL exit 1. It SHALL also report each generated page that is more than
            two links from the index or whose link has no summary beside it, and exit 1.

    Args:
        root: Repository root.

    Returns:
        Plain-words problems; empty when the repository has no generated wiki or it is sound.
    """
    from lockstep.layout_wiki import wiki_problems as problems

    return problems(root, report(root, use_results=False))
