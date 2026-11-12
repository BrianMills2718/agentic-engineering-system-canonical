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

[[[cog import lockstep.cogtext as c; c.docstring("ART-OPENSPEC-TEXT", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-3: A hook copies the normative text and typed signatures down
  into the code: a hook copies the full normative text, and the typed
  signatures, from the plan down into the code's docstrings automatically;
  nobody types the copy. For normative text the projection is two-way: the
  normative portion of a docstring can be edited where the agent is working,
  and the edit projects up into the plan; and when the normative text
  changes in the plan, every linked function, wherever it is, is marked for
  update and the agent is handed that list.
BEH-3.7: In a repository that has OpenSpec specs, the requirement text the
  hook hands the agent before an edit is the OpenSpec requirement the file
  implements, named by an `Implements: <capability>/<requirement>` line in
  the file's docstring, with its scenarios, word for word; a planned file
  that implements no OpenSpec requirement, and a repository without OpenSpec
  specs, keep the plan text from .aes/target.yaml.
SC-3.7: For an Edit or Write to a file whose docstring has an `Implements:
  <capability>/<requirement>` line, in a repository with
  `openspec/specs/<capability>/spec.md`, the hook's context holds that
  requirement's text and scenarios word for word from the spec (or from an
  active change), with or without an AES plan, and none of the plan's text;
  a planned file that implements no requirement, and a repository with no
  OpenSpec specs, still get the plan text.
  Disproved if: The hook hands plan text from .aes/target.yaml for a file
  that implements an OpenSpec requirement, shortens or alters the
  requirement text, hands nothing for a repository that has OpenSpec specs
  and no AES plan, or hands no plan text where there are no OpenSpec specs
  or the file implements no requirement.
Proven by: VS-3.7-a (tests/test_openspec_text.py)
Declares (typed signatures, from the plan):
  requirement_slug(name: str) -> str
  find_spec_root(start: Path) -> Path | None
  read_requirements(root: Path) -> dict[str, str]
  implemented_ids(path: Path) -> list[str]
  requirement_packet(root: Path, path: Path) -> tuple[list[str], str]
[[[end]]] (sum: 23k0ND7ufr)
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
