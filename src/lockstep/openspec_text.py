"""Read the OpenSpec requirement a file implements, so the edit hook hands the agent that text instead of the AES plan text (behavior 3.7, issue #54).

OpenSpec is the approved single store of requirement text. A file says which requirement it implements with an
`Implements: <capability>/<requirement>` line in a docstring (the code2 repository format), where the requirement
is the heading `### Requirement: <name>` in `openspec/specs/<capability>/spec.md` and its ID is
`<capability>/<name as lowercase words joined by hyphens>`. The hook hands the agent that requirement's block of the
spec word for word (its statement, `Source:` line and scenarios), because agents read what is put in front of them
and do not follow references (wiki/behavior-layout.md).

The ID rule and the `Implements:` line are the ones code2check reads (`code2check.spec.slug`,
`code2check.markers`). They are copied here, about forty lines, instead of imported: code2check is a floating
private git dependency whose `show` also runs the test report, which a hook that runs before every edit must not.
Like code2check, requirements in an active change (`openspec/changes/<name>/specs/`, not the archive) are read
too and win over the spec, since that is where the requirement a file is being written to implement lives until
the change is archived.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:openspec_text.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-guard/agents-get-requirement-text-from-the-shell-too, lockstep-plan-format/the-plan-is-openspec-plus-layout-rows

### Requirement: Agents get requirement text from the shell too

In a repository with OpenSpec specs and no layout plan, the edit hook SHALL answer a shell command that names or writes a file whose docstrings carry `Implements:` lines with those requirements' text, without a `permissionDecision`, and SHALL log the call as `openspec_text` with the requirement IDs; a command naming no such file and no file a decision governs SHALL get no answer.

Source: inferred by agent from the 2026-11-23 linked-chain acceptance run (Claude edited only through Bash, so the text never arrived); plan docs/planning/linked-chain-core-2026-11-23.md

#### Scenario: A shell command on an implementing file gets its requirement text

- **GIVEN** a file whose docstring says `Implements: ship/<requirement>`
- **WHEN** the agent runs `cat` on it, writes it with a heredoc, or edits it with `sed -i`
- **THEN** the hook's answer holds that requirement's text and no decision

### Requirement: The plan is OpenSpec plus layout rows

In a repository whose `lockstep.yaml` has a `layout:` list and which has no `.aes/target.yaml`, Lockstep SHALL take the
planned files from the `layout:` rows (path, purpose, the OpenSpec requirements it implements, its tests, optionally
its typed exports), the governed folders from `governed:`, and the requirement text from OpenSpec. A repository with
`.aes/target.yaml` SHALL be read as before.

Source: Brian, 2026-11-11, approving the one-tool design as written ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 2: "Lockstep reads requirements from OpenSpec ... and layout from `lockstep.yaml`. `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it").

#### Scenario: The layout is laid out with first docstrings

- **GIVEN** a layout row for `src/greeter/__init__.py` implementing `greeting/greet-by-name`, tested by `tests/test_greet.py`
- **WHEN** `lockstep layout` runs
- **THEN** the file is created with a docstring holding its `Implements:` line, the requirement and its scenarios word for word, the test names and its declared signature, and an existing file is left as it is

#### Scenario: An unplanned file is refused against the layout

- **GIVEN** `governed: [src/]` and no row for `src/greeter/extra.py`
- **WHEN** an agent writes that file under `PCW_MODE=block`
- **THEN** the edit hook refuses it and names `lockstep.yaml` as where the file must be planned

#### Scenario: A planned file's edit hands over its requirement

- **GIVEN** a laid-out planned file
- **WHEN** an agent edits it
- **THEN** the edit is allowed and the agent is handed the OpenSpec requirement text

#### Scenario: The whole-tree check reads the layout

- **GIVEN** a laid-out, committed layout repository
- **WHEN** `lockstep check` runs, and again after an unplanned file is added under `src/`
- **THEN** the first allows and the second blocks with that file as `unplanned`

#### Scenario: A layout row must name real requirements

- **GIVEN** a row whose `implements` names a requirement no spec defines, and a row with no purpose
- **WHEN** the layout is checked
- **THEN** both are reported, naming the row's path

#### Scenario: An AES plan is still read

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** Lockstep reads its plan
- **THEN** the planned files come from `.aes/target.yaml` exactly as before
[[[end]]]
"""

from __future__ import annotations

import ast
from pathlib import Path
import re

_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*$")
_REQUIREMENT = re.compile(r"^#{3,4}[ \t]+Requirement:[ \t]*(.+?)[ \t]*$")
_SCENARIO = re.compile(r"^#{3,4}[ \t]+Scenario:")
_FENCE = re.compile(r"^[ \t]*(?:```|~~~)")
_IMPLEMENTS = re.compile(r"^[ \t]*Implements:[ \t]*(.*)$")


def requirement_slug(name: str) -> str:
    """The ID part of a requirement heading: lowercase words joined by hyphens (code2check's rule)."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def find_spec_root(start: Path) -> Path | None:
    """Nearest folder at or above `start` holding `openspec/specs/<capability>/spec.md`, else None."""
    start = start.resolve()
    for folder in [start, *start.parents]:
        if next((folder / "openspec" / "specs").glob("*/spec.md"), None) is not None:
            return folder
    return None


def _spec_files(root: Path) -> list[tuple[Path, bool]]:
    """Each spec file to read, with whether it is an active change's delta: the specs, then the active changes."""
    specs = sorted((root / "openspec" / "specs").glob("*/spec.md"))
    changes = sorted(f for f in (root / "openspec" / "changes").glob("*/specs/*/spec.md") if f.parts[-4] != "archive")
    return [(f, False) for f in specs] + [(f, True) for f in changes]


def _parse(spec: Path, root: Path, delta: bool) -> dict[str, tuple[str, str]]:
    """Requirement ID -> (spec path relative to root, the requirement's block word for word) for one spec file.

    A block runs from its `### Requirement:` heading to the next heading that is not one of its scenarios. A line
    inside a code fence is never a heading. In a change's delta, requirements under `## REMOVED` are not read.
    """
    capability = spec.parent.name
    rel = spec.relative_to(root).as_posix()
    found: dict[str, tuple[str, str]] = {}
    ident = ""
    block: list[str] | None = None
    fenced = False
    removed = False

    def close() -> None:
        if block is not None:
            found[ident] = (rel, "\n".join(block).rstrip())

    for line in spec.read_text(encoding="utf-8", errors="replace").splitlines():
        if _FENCE.match(line):
            fenced = not fenced
        elif not fenced and (heading := _HEADING.match(line)):
            requirement = _REQUIREMENT.match(line)
            if requirement or not (_SCENARIO.match(line) and block is not None):
                close()
                block = None
                if heading.group(1) == "##":
                    removed = delta and heading.group(2).upper().startswith("REMOVED")
                if requirement and not removed:
                    ident = f"{capability}/{requirement_slug(requirement.group(1))}"
                    block = []
        if block is not None:
            block.append(line)
    close()
    return found


def _read(root: Path) -> dict[str, tuple[str, str]]:
    found: dict[str, tuple[str, str]] = {}
    for spec, delta in _spec_files(root):
        found.update(_parse(spec, root, delta))
    return found


def read_requirements(root: Path) -> dict[str, str]:
    """Every requirement ID the specs and active changes under `root` define, with its block word for word."""
    return {ident: text for ident, (_, text) in _read(root).items()}


def implemented_ids(path: Path) -> list[str]:
    """The requirement IDs a Python file's docstrings name on `Implements:` lines, in order, without repeats.

    Module, class and function docstrings are read; a comment is not. An ID list continues on the next line
    while the line before ends in a comma. A file that is missing, is not Python or does not parse names none.
    """
    if path.suffix != ".py":
        return []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, ValueError):
        return []
    ids: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        lines = (ast.get_docstring(node, clean=False) or "").splitlines()
        for i, line in enumerate(lines):
            match = _IMPLEMENTS.match(line)
            if not match:
                continue
            text = match.group(1)
            while text.rstrip().endswith(",") and i + 1 < len(lines) and lines[i + 1].strip():
                i += 1
                text += " " + lines[i].strip()
            ids += [ident for part in text.split(",") if (ident := part.strip()) and ident not in ids]
    return ids


def requirement_packet(root: Path, path: Path) -> tuple[list[str], str]:
    """What the hook hands the agent before it edits `path`: (the IDs the file implements, the text to hand over).

    Each requirement is given word for word with the spec it came from; an ID that no spec or active change
    defines is named as missing, so a mistyped `Implements:` line is seen. A file that implements nothing gives
    ([], "") and the hook then falls back to the AES plan text.
    """
    ids = implemented_ids(path)
    if not ids:
        return [], ""
    found = _read(root)
    try:
        rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = str(path)
    blocks = []
    for ident in ids:
        if ident in found:
            source, text = found[ident]
            blocks.append(f"{ident} ({source}):\n{text}")
        else:
            blocks.append(f"{ident}: no requirement with this ID in openspec/specs/*/spec.md or an active change "
                          "under openspec/changes/; fix the `Implements:` line or add the requirement.")
    header = f"Requirement text for {rel}, from OpenSpec (its docstring says Implements: {', '.join(ids)}):"
    return ids, header + "\n\n" + "\n\n".join(blocks)
