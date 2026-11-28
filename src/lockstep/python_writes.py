"""Which paths Python code writes, read from the parsed code (Python's `ast`), for `lockstep.shell_targets`.

The shell rule counts every path a writing script names, which counts the paths in the text a script writes
(a proposal that mentions `src/x/core.py`). Here only the targets of writing calls count: `open(p, "w")`,
`p.write_text(...)`, `shutil.copy(src, dst)` and the like, with `p` worked out from string literals, simple
assignments, `for` loops over a literal list, `Path(...)`, `/` joins and `os.path.join`. `None` means the code did
not parse or a write target could not be worked out; the caller then keeps the old rule.

Implements: lockstep-guard/shell-commands-are-judged-by-the-paths-they-write

Requirement text (generated):
    lockstep-guard/shell-commands-are-judged-by-the-paths-they-write: The edit hook SHALL find the
        files a shell command writes the way code2check's guard does: redirect and tee targets read
        as shell words, the files `mv`, `touch`, `sed -i` and the like write, only the destination
        of a copy (`cp`, `install`, `rsync`), and the paths named by code in the command (a `python
        -c`, a heredoc script) only when that code calls something that writes; for Python code that
        parses, only the paths its writing calls target (worked out from string literals, simple
        assignments and `Path` joins) SHALL count, and Python code whose write target cannot be
        worked out, or other code, SHALL count every path it names; a `cd` in the command SHALL be
        followed. In block mode it SHALL refuse a command that writes a file under a governed folder
        that the plan does not declare, and it SHALL NOT refuse a command that only reads a planned
        file.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:python_writes.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-guard/shell-commands-are-judged-by-the-paths-they-write

### Requirement: Shell commands are judged by the paths they write

The edit hook SHALL find the files a shell command writes the way code2check's guard does: redirect and tee
targets read as shell words, the files `mv`, `touch`, `sed -i` and the like write, only the destination of a
copy (`cp`, `install`, `rsync`), and the paths named by code in the command (a `python -c`, a heredoc script)
only when that code calls something that writes; for Python code that parses, only the paths its writing calls
target (worked out from string literals, simple assignments and `Path` joins) SHALL count, and Python code whose
write target cannot be worked out, or other code, SHALL count every path it names; a `cd` in the command SHALL be followed. In block mode it
SHALL refuse a command that writes a file under a governed folder that the plan does not declare, and it
SHALL NOT refuse a command that only reads a planned file.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md, slice 3: "Port code2check's shell-target parsing. Done when lifelike replays the four cases from lockstep#111").
The Python narrowing is inferred by agent from the 2026-11-28 Sonnet end-to-end run, where a script writing
only an OpenSpec proposal was refused because the proposal text named two planned files.

#### Scenario: A heredoc creating an unplanned file is refused

- **GIVEN** a governed root whose plan does not declare `newfile.py` and PCW_MODE=block
- **WHEN** a shell command is `cat > <governed>/newfile.py <<'EOF' ... EOF`
- **THEN** the hook denies it

#### Scenario: An echo redirect creating an unplanned file is refused

- **GIVEN** the same project
- **WHEN** a shell command is `echo 'x = 1' > <governed>/newfile.py`
- **THEN** the hook denies it

#### Scenario: A python one-liner creating an unplanned file is refused

- **GIVEN** the same project
- **WHEN** a shell command is `python -c "open('<governed>/newfile.py','w').write('x')"`
- **THEN** the hook denies it

#### Scenario: Copying a planned file out is allowed

- **GIVEN** the same project, with a planned file `<governed>/rule.py`
- **WHEN** a shell command is `cp <governed>/rule.py /tmp/x`
- **THEN** the hook allows it and hands over the plan text

#### Scenario: A Python script whose written text names a planned file is not refused

- **GIVEN** the same project, with a planned file `<governed>/rule.py`
- **WHEN** a shell command is `python3 - <<'EOF'` with a script that writes `openspec/changes/x/proposal.md`
  through `pathlib.Path` and whose written text names `<governed>/rule.py` and `<governed>/newfile.py`
- **THEN** the hook does not deny it

Tested by: tests/lockstep/test_lockstep_shell_targets.py

Declares (typed signatures, from the plan):
  python_code
  python_write_paths
[[[end]]]
"""

from __future__ import annotations

import ast
import itertools
import os
import re
import shlex

_PYTHON = re.compile(r"(?:^|/)python(?:\d+(?:\.\d+)?)?$")
# Path methods that write their receiver; `rename(target)` and `replace(target)` write both (a
# `replace` with two arguments is `str.replace`).
_WRITES_SELF = {"write_text", "write_bytes", "touch", "unlink", "rmdir", "symlink_to", "hardlink_to"}
_MOVES = {"rename", "replace"}
# os functions by which arguments they write.
_OS = {"remove": (0,), "unlink": (0,), "rmdir": (0,), "truncate": (0,), "rename": (0, 1), "replace": (0, 1),
       "link": (1,), "symlink": (1,), "open": (0,)}
_SHUTIL_DEST = {"copy", "copy2", "copyfile", "copytree", "copymode", "copystat"}
_PATH_CALLS = {"Path", "PurePath", "PosixPath", "join"}
_SAME_PATH = {"resolve", "absolute", "expanduser"}
# Calls that run other programs or code: what they write cannot be read from here, so the old rule applies.
_RUNS_OTHERS = {"system", "popen", "execv", "execvp", "execl", "execlp", "spawnl", "spawnv"}


def python_code(segment: str) -> str | None:
    """The Python code a simple shell command runs: its `-c` argument or its heredoc body; None if it runs none."""
    first, _, body = segment.partition("\n")
    try:
        words = shlex.split(first)
    except ValueError:
        return None
    if not any(_PYTHON.search(w) for w in words[:4]):
        return None
    if "-c" in words:
        i = words.index("-c") + 1
        return words[i] if i < len(words) else None
    return body if "<<" in first else None


def python_write_paths(segment: str) -> list[str] | None:
    """The paths the Python code in `segment` writes, or None when it cannot tell (see the module docstring)."""
    code = python_code(segment)
    if code is None:
        return None
    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError):
        return None
    env = _bindings(tree)
    out: list[str] = []
    for node in ast.walk(tree):
        if _runs_others(node):
            return None
        for target in _write_args(node) if isinstance(node, ast.Call) else []:
            paths = _resolve(target, env, 0)
            if paths is None:
                return None
            out += [p for p in paths if p not in out]
    return out


def _runs_others(node: ast.AST) -> bool:
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        names = [a.name for a in node.names] + ([node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
        return any(n.split(".")[0] == "subprocess" for n in names)
    func = node.func if isinstance(node, ast.Call) else None
    return (isinstance(func, ast.Name) and func.id in {"exec", "eval"}) or (
        isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == "os"
        and func.attr in _RUNS_OTHERS)


def _bindings(tree: ast.AST) -> dict[str, list[ast.expr]]:
    """Every value each plain name is given: `n = expr`, each item of `for n in [a, b]`, `with x as n`."""
    env: dict[str, list[ast.expr]] = {}
    for node in ast.walk(tree):
        for name, value in _bound(node):
            env.setdefault(name, []).append(value)
    return env


def _bound(node: ast.AST) -> list[tuple[str, ast.expr]]:
    if isinstance(node, ast.Assign):
        return [(t.id, node.value) for t in node.targets if isinstance(t, ast.Name)]
    if isinstance(node, (ast.For, ast.comprehension)) and isinstance(node.target, ast.Name):
        literal = isinstance(node.iter, (ast.List, ast.Tuple, ast.Set)) and node.iter.elts
        return [(node.target.id, v) for v in (node.iter.elts if literal else [node.iter])]  # type: ignore[attr-defined]
    if isinstance(node, (ast.With, ast.AsyncWith)):
        return [(i.optional_vars.id, i.context_expr) for i in node.items if isinstance(i.optional_vars, ast.Name)]
    return []


def _write_args(call: ast.Call) -> list[ast.expr]:
    """The argument expressions (or receiver) a call writes; empty for a call that writes nothing."""
    func = call.func
    name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
    owner = func.value.id if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) else ""
    if owner == "os" and name in _OS:
        return [call.args[i] for i in _OS[name] if i < len(call.args)]
    if name == "open":
        return _open_target(call, func, owner)
    if owner == "shutil":
        return _shutil_args(call, name)
    if isinstance(func, ast.Attribute) and name in _WRITES_SELF:
        return [func.value]
    if isinstance(func, ast.Attribute) and name in _MOVES and len(call.args) == 1:  # str.replace takes two
        return [func.value, call.args[0]]
    return []


def _shutil_args(call: ast.Call, name: str) -> list[ast.expr]:
    if name in _SHUTIL_DEST:
        return call.args[1:2]
    if name == "move":
        return call.args[:2]
    return call.args[:1] if name == "rmtree" else list(call.args)


def _open_target(call: ast.Call, func: ast.expr, owner: str) -> list[ast.expr]:
    """`open(p, mode)`, `io.open(p, mode)` or `p.open(mode)`: `p` when the mode writes or is not a literal."""
    is_method = isinstance(func, ast.Attribute) and owner not in {"io", "codecs"}
    mode_args = call.args[0:1] if is_method else call.args[1:2]
    mode = next((k.value for k in call.keywords if k.arg == "mode"), mode_args[0] if mode_args else None)
    reads = mode is None or (isinstance(mode, ast.Constant) and isinstance(mode.value, str)
                             and not set(mode.value) & set("wax+"))
    if reads:
        return []
    return [func.value] if is_method else call.args[:1]  # type: ignore[attr-defined]


def _resolve(node: ast.expr, env: dict[str, list[ast.expr]], depth: int) -> list[str] | None:
    """The path strings `node` can be, or None when one of them cannot be worked out."""
    if depth > 20:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.Name):
        return _union([_resolve(v, env, depth + 1) for v in env.get(node.id, [])])
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return _joined([node.left, node.right], env, depth)
    if isinstance(node, ast.Call):
        return _resolve_call(node, env, depth)
    return None


def _resolve_call(node: ast.Call, env: dict[str, list[ast.expr]], depth: int) -> list[str] | None:
    func = node.func
    name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
    if name in _PATH_CALLS:
        return _joined(list(node.args), env, depth) if node.args else ["."]
    if name in _SAME_PATH and isinstance(func, ast.Attribute):
        return _resolve(func.value, env, depth + 1)
    if name == "open" and node.args:  # a handle bound by `with open(p) as f`
        return _resolve(node.args[0], env, depth + 1)
    return None


def _joined(parts: list[ast.expr], env: dict[str, list[ast.expr]], depth: int) -> list[str] | None:
    resolved = [_resolve(p, env, depth + 1) for p in parts]
    if any(r is None for r in resolved):
        return None
    return [os.path.join(*combo) for combo in itertools.product(*resolved)]  # type: ignore[arg-type]


def _union(options: list[list[str] | None]) -> list[str] | None:
    """Every value of a name; None when the name has no value here or one of them cannot be worked out."""
    if not options or any(o is None for o in options):
        return None
    return list(dict.fromkeys(p for o in options for p in o))  # type: ignore[union-attr]
