"""Find `Implements:` docstring lines in source and `req` markers in tests, using the Python AST.

Implements: lockstep-checks/trace-source-folders-are-configurable, lockstep-checks/trace-test-folders-are-configurable

Requirement text (generated):
    lockstep-checks/trace-source-folders-are-configurable: The trace check SHALL search for
        `Implements:` lines in the folders listed under `[tool.lockstep] (or`[tool.code2check]`, its
        old name) source` in `pyproject.toml`, and in `src` when none are listed.
    lockstep-checks/trace-test-folders-are-configurable: The marker reader SHALL discover
        `@pytest.mark.req` in `test_*.py` files under the folders listed in `[tool.lockstep]
        (or`[tool.code2check]`, its old name) tests` in `pyproject.toml`, defaulting to `tests` when
        omitted. Trace, status, generated plan coverage and test-first SHALL use those same roots.
        Overlapping roots SHALL not duplicate a discovered test marker.
"""

import ast
from pathlib import Path
import re
import tomllib

_IMPLEMENTS = re.compile(r"^[ \t]*Implements:[ \t]*(.+(?:\n[ \t]+\S.*)*)", re.MULTILINE)


def _tool_table(root: Path) -> dict:
    """Return `[tool.lockstep]` from pyproject.toml, else `[tool.code2check]` (its old name), else {}."""
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return {}
    tool = tomllib.loads(pyproject.read_text()).get("tool", {})
    return tool.get("lockstep") or tool.get("code2check") or {}


def source_dirs(root: Path) -> list[Path]:
    """Return the folders searched for `Implements:` lines.

    Args:
        root: Repository root.

    Returns:
        The folders named by `[tool.lockstep] source` in pyproject.toml, or `src` when none are.
    """
    names = _tool_table(root).get("source", ["src"])
    return [root / name for name in names]


def test_dirs(root: Path) -> list[Path]:
    """Return configured test folders, defaulting to the repository's tests folder.

    Args:
        root: Repository root.

    Returns:
        The folders named by `[tool.lockstep] tests`, or `tests` when omitted.
    """
    names = _tool_table(root).get("tests", ["tests"])
    return [root / name for name in names]


def implementers(root: Path, only: Path | None = None) -> list[tuple[str, str, str]]:
    """List (requirement ID, file:line, symbol) for each `Implements:` line in source docstrings.

    Args:
        root: Repository root.
        only: Read just this file (absolute) instead of every file in the source folders.

    Returns:
        One entry per ID; a line may name several IDs separated by commas. The symbol is the dotted
        module path, plus the class and function names for a docstring inside one.
    """
    found = []
    for folder in source_dirs(root):
        if only is not None and not only.is_relative_to(folder):
            continue
        for path in [only] if only is not None else sorted(folder.rglob("*.py")):
            tree = ast.parse(path.read_text(), filename=str(path))
            parts = list(path.relative_to(folder).with_suffix("").parts)
            module = ".".join(parts[:-1] if parts[-1] == "__init__" else parts)
            for node, symbol in _documented(tree, module):
                doc = ast.get_docstring(node, clean=False)  # type: ignore[arg-type]
                if not doc:
                    continue
                line = getattr(node, "lineno", 1)
                for m in _IMPLEMENTS.finditer(doc):
                    for ident in m.group(1).replace("\n", " ").split(","):
                        if ident.strip():
                            found.append((ident.strip(), f"{path.relative_to(root)}:{line}", symbol))
    return found


def _documented(node: ast.AST, name: str) -> list[tuple[ast.AST, str]]:
    """Return node and every class or function inside it, at any depth, each with its dotted name."""
    found = [(node, name)]
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            found += _documented(child, f"{name}.{child.name}")
        else:
            found += [(n, s) for n, s in _documented(child, name)[1:]]
    return found


def implements(root: Path) -> list[tuple[str, str]]:
    """List (requirement ID, file:line) for each `Implements:` line in source docstrings.

    Args:
        root: Repository root.

    Returns:
        One entry per ID; a line may name several IDs separated by commas.
    """
    return [(ident, where) for ident, where, _ in implementers(root)]


def req_markers(root: Path, existing: bool | None = None) -> list[tuple[str, str, str]]:
    """List (scenario ID, file:line, test node ID) for each `@pytest.mark.req("...")` in tests.

    Args:
        root: Repository root.
        existing: When set, keep only markers whose `existing=True` flag equals it.

    Returns:
        One entry per marker on a test function.
    """
    found = []
    for path in sorted({path for folder in test_dirs(root) for path in folder.rglob("test_*.py")}):
        tree = ast.parse(path.read_text(), filename=str(path))
        rel = path.relative_to(root)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in node.decorator_list:
                if (
                    isinstance(dec, ast.Call)
                    and isinstance(dec.func, ast.Attribute)
                    and dec.func.attr == "req"
                    and dec.args
                    and isinstance(dec.args[0], ast.Constant)
                ):
                    flag = any(
                        k.arg == "existing" and isinstance(k.value, ast.Constant) and k.value.value is True
                        for k in dec.keywords
                    )
                    if existing is None or flag == existing:
                        found.append((str(dec.args[0].value), f"{rel}:{dec.lineno}", f"{rel}::{node.name}"))
    return found
