"""Python AST characterization provider (`RU-AES-CHARACTERIZE`, `SC-GF-006`).

Reads source text with `ast` only. Consumer code is never imported or executed,
so a module that raises at import time characterizes like any other.

Per file: the module name, top-level public symbols (functions with a
signature string, classes, assigned names), and the intra-repository import
edges resolved to governed file paths. Imports that resolve to no governed
file (stdlib, third-party) are not edges.

Module names follow the `src/` layout: `src/pkg/mod.py` is `pkg.mod`; any other
path is its dotted path (`tests/test_x.py` is `tests.test_x`). An absolute
import that does not resolve as written is retried relative to the importing
file's directory when that directory is not a package, which is where
pytest's default rootdir insertion finds a sibling helper module.

Import edges are taken from the whole file, not only the module top level: an
import inside a function is still code the test can reach. Importing
`pkg.sub.mod` executes `pkg/__init__.py` and `pkg/sub/__init__.py`, so those
governed files are edges too.
"""

from __future__ import annotations

import ast
from typing import Literal

from .records import StrictModel

SymbolKind = Literal["function", "class", "variable"]


class Symbol(StrictModel):
    name: str
    kind: SymbolKind
    signature: str | None = None  # functions only: "(args) -> return"


class PythonFacts(StrictModel):
    module: str
    symbols: list[Symbol]
    imports: list[str]  # governed paths, sorted
    parse_error: str | None = None


def module_name(path: str) -> str:
    """Dotted module name for a repository path ending in `.py`."""
    if not path.endswith(".py"):
        raise ValueError(f"not a Python path: {path!r}")
    rel = path.removeprefix("src/")[: -len(".py")]
    parts = rel.split("/")
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def render_signature(args: ast.arguments, returns: ast.expr | None) -> str:
    sig = f"({ast.unparse(args)})"
    return f"{sig} -> {ast.unparse(returns)}" if returns is not None else sig


def parse_export(entry: str) -> tuple[str, str | None]:
    """Split a symbol commitment into (name, normalized signature or None).

    `name` commits only that the symbol exists. `name(args) -> ret` also commits
    the signature; it is parsed as a function header and re-rendered, so spacing
    and quoting differences do not count as drift. Raises ValueError if the
    entry is neither form.
    """
    if "(" not in entry:
        if not entry.isidentifier():
            raise ValueError(f"export {entry!r} is not a Python identifier")
        return entry, None
    name = entry.split("(", 1)[0].strip()
    if not name.isidentifier():
        raise ValueError(f"export {entry!r} does not start with a Python identifier")
    try:
        node = ast.parse(f"def {entry.strip()}:\n    pass\n").body[0]
    except SyntaxError as exc:
        raise ValueError(f"export {entry!r} is not a function header: {exc.msg}") from exc
    assert isinstance(node, ast.FunctionDef)
    return name, render_signature(node.args, node.returns)


def _public_symbols(tree: ast.Module) -> list[Symbol]:
    found: dict[str, Symbol] = {}  # later bindings win, as at runtime

    def add(name: str, kind: SymbolKind, signature: str | None = None) -> None:
        if not name.startswith("_"):
            found[name] = Symbol(name=name, kind=kind, signature=signature)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add(node.name, "function", render_signature(node.args, node.returns))
        elif isinstance(node, ast.ClassDef):
            add(node.name, "class")
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for t in targets:
                for n in ([t] if isinstance(t, ast.Name) else getattr(t, "elts", [])):
                    if isinstance(n, ast.Name):
                        add(n.id, "variable")
    return list(found.values())


def _resolve(dotted: str, modules: dict[str, str]) -> list[str]:
    """Governed paths executed by importing `dotted`: the module and its packages."""
    parts = dotted.split(".")
    return [modules[p] for p in (".".join(parts[: i + 1]) for i in range(len(parts))) if p in modules]


def _imports(tree: ast.Module, path: str, module: str, modules: dict[str, str]) -> list[str]:
    is_package = path.endswith("/__init__.py")
    package = module if is_package else module.rpartition(".")[0]
    # The importing file's directory, when it is not a package: pytest puts such a
    # directory on sys.path, so a sibling module imports by its bare name there.
    local_dir = module_name(path).rpartition(".")[0]
    if local_dir in modules:
        local_dir = ""

    def absolute(dotted: str) -> list[str]:
        hit = _resolve(dotted, modules)
        if dotted in modules or not local_dir:
            return hit
        return hit or _resolve(f"{local_dir}.{dotted}", modules)

    edges: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                edges.update(absolute(alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base_parts = package.split(".") if package else []
                if node.level - 1 > len(base_parts):
                    continue  # beyond the top-level package; Python would refuse it too
                base = ".".join(base_parts[: len(base_parts) - (node.level - 1)])
                target = f"{base}.{node.module}" if base and node.module else (node.module or base)
                resolve = lambda d: _resolve(d, modules)
            else:
                target = node.module or ""
                resolve = absolute
            if not target:
                continue
            edges.update(resolve(target))
            for alias in node.names:  # `from pkg import mod` imports a submodule
                sub = f"{target}.{alias.name}"
                if sub in modules:
                    edges.update(resolve(sub))
    edges.discard(path)
    return sorted(edges)


def analyze(path: str, source: str, modules: dict[str, str]) -> PythonFacts:
    """Characterize one file. `modules` maps every governed module name to its path."""
    module = module_name(path)
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as exc:
        return PythonFacts(
            module=module, symbols=[], imports=[],
            parse_error=f"SyntaxError line {exc.lineno}: {exc.msg}",
        )
    return PythonFacts(
        module=module,
        symbols=_public_symbols(tree),
        imports=_imports(tree, path, module, modules),
    )


def import_closure(start: str, facts: dict[str, PythonFacts]) -> list[str]:
    """Every governed path reachable from `start` through import edges, `start` excluded."""
    if start not in facts:
        raise KeyError(start)
    seen: set[str] = set()
    stack = [start]
    while stack:
        for dep in facts[stack.pop()].imports:
            if dep not in seen and dep != start:
                seen.add(dep)
                stack.append(dep)
    return sorted(seen)
