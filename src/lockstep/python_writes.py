"""Which paths Python code writes, read from the parsed code (Python's `ast`), for `lockstep.shell_targets`.

The shell rule counts every path a writing script names, which counts the paths in the text a script writes
(a proposal that mentions `src/x/core.py`). Narrowing that to the targets of the script's writing calls is the
exception, taken only when every import, name, call and keyword in the code is on the known lists below and
every write target is worked out from string literals, simple assignments, `for` loops over a literal list,
`with ... as`, `Path(...)`, `/`, `+` and `os.path.join`. Anything else (an alias, an unknown call, code that runs
another program, a binding not followed, a self-reference, more than `_LIMIT` paths, shell expansion, a crash)
returns `None`, and the caller keeps the every-path rule.

Implements: lockstep-guard/shell-commands-are-judged-by-the-paths-they-write

Requirement text (generated):
    lockstep-guard/shell-commands-are-judged-by-the-paths-they-write: The edit hook SHALL find the
        files a shell command writes the way code2check's guard does: redirect and tee targets read
        as shell words, the files `mv`, `touch`, `sed -i` and the like write, only the destination
        of a copy (`cp`, `install`, `rsync`), and, when code in the command (a `python -c`, a
        heredoc script) calls something that writes, every path that code names; a `cd` in the
        command SHALL be followed. As the one exception, Python code SHALL count only the paths its
        writing calls target when the hook can vouch for all of it: Python reads it as its program
        (`-c`, or a heredoc on standard input with no script argument), the shell expands nothing in
        it, it parses, every import, name, call and keyword in it is on the hook's known lists, and
        every write target is worked out from string literals, simple assignments and `Path` joins.
        Anything else SHALL keep the every-path rule, including code that runs other programs
        (`subprocess`, `os.system`, `exec`, `__import__` and the like), an alias, a binding the hook
        does not follow, and a crash or a slow answer while reading the code. In block mode it SHALL
        refuse a command that writes a file under a governed folder that the plan does not declare,
        and it SHALL NOT refuse a command that only reads a planned file.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:python_writes.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-guard/shell-commands-are-judged-by-the-paths-they-write

### Requirement: Shell commands are judged by the paths they write

The edit hook SHALL find the files a shell command writes the way code2check's guard does: redirect and tee
targets read as shell words, the files `mv`, `touch`, `sed -i` and the like write, only the destination of a
copy (`cp`, `install`, `rsync`), and, when code in the command (a `python -c`, a heredoc script) calls something
that writes, every path that code names; a `cd` in the command SHALL be followed. As the one exception, Python
code SHALL count only the paths its writing calls target when the hook can vouch for all of it: Python reads it
as its program (`-c`, or a heredoc on standard input with no script argument), the shell expands nothing in it,
it parses, every import, name, call and keyword in it is on the hook's known lists, and every write target is
worked out from string literals, simple assignments and `Path` joins. Anything else SHALL keep the every-path
rule, including code that runs other programs (`subprocess`, `os.system`, `exec`, `__import__` and the like), an
alias, a binding the hook does not follow, and a crash or a slow answer while reading the code. In block mode it
SHALL refuse a command that writes a file under a governed folder that the plan does not declare, and it SHALL
NOT refuse a command that only reads a planned file.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md, slice 3: "Port code2check's shell-target parsing. Done when lifelike replays the four cases from lockstep#111").
The Python exception, and its fallback to the every-path rule for anything the hook cannot vouch for, are
inferred by agent from the 2026-11-28 Sonnet end-to-end run (a script writing only an OpenSpec proposal was
refused because the proposal text named two planned files) and the independent review of the first fix
(42 of 70 probes missed a write the every-path rule caught).

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

#### Scenario: Python code the parser cannot vouch for keeps the every-path rule

- **GIVEN** the same project
- **WHEN** a Python heredoc writes `log.txt` and also writes `<governed>/b.py` by a call the hook does not know
  (`os.posix_spawnp`, `gzip.open`, `from shutil import copy`, a function parameter)
- **THEN** the hook counts every path the code names, and denies it

#### Scenario: An aliased writer keeps the every-path rule

- **GIVEN** the same project
- **WHEN** a Python heredoc runs `import os as o; o.remove('<governed>/newfile.py')`
- **THEN** the hook denies it

#### Scenario: A keyword argument target is counted

- **GIVEN** the same project
- **WHEN** a Python heredoc runs `shutil.copy('/tmp/x', dst='<governed>/newfile.py')`
- **THEN** the hook denies it

#### Scenario: Shell expansion in Python text keeps the every-path rule

- **GIVEN** the same project
- **WHEN** an unquoted heredoc or a double-quoted `python -c` holds `$(cp /tmp/x <governed>/newfile.py)`
- **THEN** the hook denies it

#### Scenario: A parser crash keeps the every-path rule

- **GIVEN** a Python heredoc too deeply nested for Python's parser that names `<governed>/b.py`
- **WHEN** the hook reads it
- **THEN** it counts every path the code names

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
from collections.abc import Sequence

_PYTHON = re.compile(r"(?:^|/)python(?:\d+(?:\.\d+)?)?$")
_LIMIT = 64  # most paths one write target may stand for; more and the old rule applies

# Modules whose plain `import` is understood, and per module the calls that are known: a tuple names the
# argument positions the call writes, () a call that writes nothing. Any other call on a module is unknown.
_MODULE_CALLS: dict[str, dict[str, tuple[int, ...]]] = {
    "os": {"remove": (0,), "unlink": (0,), "rmdir": (0,), "truncate": (0,), "makedirs": (0,), "mkdir": (0,),
           "rename": (0, 1), "replace": (0, 1), "link": (0, 1), "symlink": (0, 1), "open": (0,),
           "getcwd": (), "listdir": (), "walk": (), "stat": (), "getenv": (), "write": (), "close": (),
           "fspath": ()},
    "os.path": {name: () for name in ("join", "exists", "isfile", "isdir", "basename", "dirname", "abspath",
                                       "relpath", "splitext", "normpath", "expanduser", "getsize", "split")},
    "shutil": {"copy": (1,), "copy2": (1,), "copyfile": (1,), "copytree": (1,), "move": (0, 1), "rmtree": (0,),
               "copyfileobj": (), "which": ()},
    "json": {"dump": (), "dumps": (), "load": (), "loads": ()},
    "re": {name: () for name in ("compile", "sub", "subn", "match", "search", "findall", "finditer", "split",
                                  "escape", "fullmatch")},
    "sys": {"exit": ()},
    "textwrap": {"dedent": (), "indent": (), "fill": (), "wrap": ()},
    "glob": {"glob": (), "iglob": ()},
    "io": {"open": (0,), "StringIO": (), "BytesIO": ()},
    "pathlib": {"Path": (), "PurePath": (), "PurePosixPath": (), "PosixPath": ()},
}
_MODULE_ATTRS = {"os": {"path", "sep", "environ", "linesep", "curdir", "pardir"},
                 "sys": {"argv", "stdout", "stderr", "stdin", "version_info"}}
_PATH_CLASSES = {"Path", "PurePath", "PurePosixPath", "PosixPath"}
_SAFE_BUILTINS = {
    "print", "len", "str", "int", "float", "bool", "list", "dict", "set", "tuple", "frozenset", "sorted",
    "reversed", "range", "enumerate", "zip", "isinstance", "repr", "min", "max", "sum", "any", "all", "abs",
    "round", "format", "chr", "ord", "hex", "bytes", "hash", "divmod", "Exception", "ValueError", "TypeError",
    "KeyError", "RuntimeError", "SystemExit", "AssertionError", "FileNotFoundError", "OSError", "IndexError",
    "NotImplementedError", "__name__", "__file__",
}
# Methods on values (strings, lists, dicts, paths, open files) that write nothing.
_SAFE_METHODS = {
    "read_text", "read_bytes", "exists", "is_file", "is_dir", "iterdir", "glob", "rglob", "resolve", "absolute",
    "expanduser", "with_suffix", "with_name", "with_stem", "relative_to", "joinpath", "as_posix", "is_absolute",
    "split", "rsplit", "strip", "lstrip", "rstrip", "join", "format", "startswith", "endswith", "lower", "upper",
    "title", "splitlines", "encode", "decode", "count", "find", "rfind", "index", "partition", "rpartition",
    "zfill", "ljust", "rjust", "center", "items", "keys", "values", "get", "setdefault", "pop", "append",
    "extend", "insert", "update", "add", "discard", "sort", "reverse", "write", "writelines", "read",
    "readline", "readlines", "close", "flush", "group", "groups", "isdigit", "isalpha", "isspace", "casefold",
}
# Methods that write their receiver (a path); `rename`/`replace` with one argument write it too.
_SELF_WRITERS = {"write_text", "write_bytes", "touch", "unlink", "rmdir", "mkdir", "symlink_to", "hardlink_to"}
_KNOWN_KEYWORDS = {"mode", "encoding", "errors", "newline", "buffering", "parents", "exist_ok", "indent",
                   "sort_keys", "ensure_ascii", "end", "sep", "flush", "missing_ok", "key", "reverse",
                   "default", "flags", "count", "maxsplit", "file"}
_WRITERS_BY_NAME = set(_SELF_WRITERS) | {"rename", "replace", "open", "remove", "copy", "move", "dump"}


class _Unknown(Exception):
    """The code does something this module cannot vouch for; the caller keeps the every-path rule."""


def python_code(segment: str) -> str | None:
    """The program Python runs in a simple shell command: its `-c` argument, or the heredoc body when Python
    reads its program from stdin. None when it runs no such program, or when the shell would expand `$` or a
    backtick inside it first."""
    first, _, body = segment.partition("\n")
    heredoc = re.search(r"(?<!<)<<-?\s*(['\"]?)[A-Za-z_][\w-]*\1", first)
    head = first if heredoc else segment
    words = shlex.split(head)
    if words[:2] == ["uv", "run"]:
        words = words[2:]
    if not words or not _PYTHON.search(words[0]):
        return None
    args = iter(words[1:])
    for word in args:
        if word == "-c":
            code = next(args, None)
            return None if code is None or _expands(head) else code
        if word in {"-", "/dev/stdin"} or word.startswith("<<"):
            break
        if word in {"-W", "-X"}:
            next(args, None)
        elif not word.startswith("-") or word.startswith(("-m", "--")) or (len(word) > 2 and "c" in word[1:]):
            return None
    if heredoc is None or first.count("<<") > 1 or re.search(r"(?<![<\d>&])<(?!<)", first):
        return None
    return None if not heredoc.group(1) and re.search(r"[$`\\]", body) else body


def _expands(text: str) -> bool:
    """True when the shell would expand `$` or a backtick in `text` (anywhere outside single quotes)."""
    quote = ""
    for c in text:
        if c == "'" and quote != '"':
            quote = "" if quote else "'"
        elif c == '"' and quote != "'":
            quote = "" if quote else '"'
        elif c in "$`" and quote != "'":
            return True
    return False


def python_write_paths(segment: str) -> list[str] | None:
    """The paths the Python code in `segment` writes; None when the code holds anything this module cannot
    vouch for (see the module docstring), and the caller keeps the every-path rule."""
    try:
        code = python_code(segment)
        return None if code is None else _Reader(ast.parse(code)).written()
    except Exception:  # noqa: BLE001  # an unreadable script (RecursionError and the like) keeps the old rule
        return None


class _Reader:
    def __init__(self, tree: ast.Module) -> None:
        self.tree = tree
        self.modules: dict[str, str] = {}
        self.functions: set[str] = set()
        self.values: dict[str, list[ast.expr]] = {}
        self.untracked: set[str] = set()
        self.memo: dict[int, list[str] | None] = {}
        self.busy: set[int] = set()
        self.tracked: set[int] = set()  # name nodes bound by a form whose value is recorded
        self.called = {id(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)}
        self.attr_values = {id(n.value) for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        for node in ast.walk(tree):
            self._learn(node)
        clash = (set(self.values) | self.untracked) & (set(self.modules) | self.functions | {"open"} | _SAFE_BUILTINS)
        if clash:
            raise _Unknown(f"rebinds {sorted(clash)}")

    def written(self) -> list[str]:
        out: list[str] = []
        for node in ast.walk(self.tree):
            self._vouch(node)
            for target in self._targets(node) if isinstance(node, ast.Call) else []:
                paths = self._resolve(target)
                if paths is None:
                    raise _Unknown("a write target cannot be worked out")
                out += [p for p in paths if p not in out]
        return out

    def _learn(self, node: ast.AST) -> None:
        """Record imports and bindings; any binding form other than `name = value`, `for name in ...` and
        `with ... as name` leaves the name unknown."""
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname or alias.name not in _MODULE_CALLS:
                    raise _Unknown(f"import {alias.name}")
                self.modules[alias.name.split(".")[0]] = alias.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom):
            self._learn_from(node)
        elif isinstance(node, (ast.ClassDef, ast.AsyncFunctionDef, ast.Await)):
            raise _Unknown(type(node).__name__)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            self.untracked |= set(node.names)  # bound in another scope: never worked out
        elif isinstance(node, ast.FunctionDef):
            self.functions.add(node.name)
            self.untracked |= {a.arg for a in ast.walk(node.args) if isinstance(a, ast.arg)}
        elif isinstance(node, ast.Lambda):
            self.untracked |= {a.arg for a in ast.walk(node.args) if isinstance(a, ast.arg)}
        else:
            self._learn_binding(node)

    def _learn_from(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            known = node.module == "pathlib" and alias.name in _PATH_CLASSES or node.module == "__future__"
            if alias.asname or not known:
                raise _Unknown(f"from {node.module} import {alias.name}")
            self.modules[alias.name] = "pathlib." + alias.name

    def _learn_binding(self, node: ast.AST) -> None:
        if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Attribute) for n in targets for t in ast.walk(n)):
                raise _Unknown("assignment to an attribute")
            if isinstance(node, ast.Assign):
                self._bind([t for t in targets if isinstance(t, ast.Name)], [node.value])
        elif isinstance(node, (ast.For, ast.comprehension)) and isinstance(node.target, ast.Name):
            items = node.iter.elts if isinstance(node.iter, (ast.List, ast.Tuple)) and node.iter.elts else [node.iter]
            self._bind([node.target], items)
        elif isinstance(node, ast.withitem) and isinstance(node.optional_vars, ast.Name):
            self._bind([node.optional_vars], [node.context_expr])
        else:
            self._learn_untracked(node)

    def _bind(self, names: list[ast.Name], values: list[ast.expr]) -> None:
        for name in names:
            self.tracked.add(id(name))
            self.values.setdefault(name.id, []).extend(values)

    def _learn_untracked(self, node: ast.AST) -> None:
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)) and id(node) not in self.tracked:
            self.untracked.add(node.id)  # every other way a name gets bound: tuple, walrus, +=, except as, del
        elif isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name:
            self.untracked.add(node.name)
        elif isinstance(node, ast.MatchMapping) and node.rest:
            self.untracked.add(node.rest)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            self.untracked.add(node.name)

    def _vouch(self, node: ast.AST) -> None:
        """Raise unless every name, attribute and call in the code is one this module knows."""
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            self._vouch_name(node)
        elif isinstance(node, ast.Attribute) and id(node) not in self.called:
            module = self._module_of(node.value)
            if module and node.attr not in _MODULE_ATTRS.get(module, set()):
                raise _Unknown(f"{module}.{node.attr} used as a value")
            if not module and node.attr in _WRITERS_BY_NAME:
                raise _Unknown(f".{node.attr} used as a value")
        elif isinstance(node, ast.Call):
            self._vouch_call(node)

    def _vouch_name(self, node: ast.Name) -> None:
        name = node.id
        if name in self.modules:
            if id(node) not in self.attr_values and not self.modules[name].startswith("pathlib."):
                raise _Unknown(f"module {name} used as a value")
            if self.modules[name].startswith("pathlib.") and id(node) not in self.called:
                raise _Unknown(f"{name} used as a value")
        elif name == "open" or name in self.functions:
            if id(node) not in self.called:
                raise _Unknown(f"{name} used as a value")
        elif name not in _SAFE_BUILTINS and name not in self.values and name not in self.untracked:
            raise _Unknown(f"unknown name {name}")

    def _vouch_call(self, call: ast.Call) -> None:
        if any(isinstance(a, ast.Starred) for a in call.args) or any(k.arg is None for k in call.keywords):
            raise _Unknown("star arguments")
        if any(k.arg not in _KNOWN_KEYWORDS for k in call.keywords):
            raise _Unknown("an unknown keyword argument")
        key = next((k.value for k in call.keywords if k.arg == "key"), None)
        if key is not None and not isinstance(key, ast.Lambda):
            raise _Unknown("a function passed as key")
        func = call.func
        if isinstance(func, ast.Name):
            if func.id not in self.functions | _SAFE_BUILTINS | {"open"} and func.id not in self.modules:
                raise _Unknown(f"call of {func.id}")
        elif isinstance(func, ast.Attribute):
            module = self._module_of(func.value)
            if module and func.attr not in _MODULE_CALLS.get(module, {}):
                raise _Unknown(f"{module}.{func.attr}")
            if not module and not self._known_method(func.attr, call):
                raise _Unknown(f".{func.attr}")
        elif not isinstance(func, ast.Lambda):
            raise _Unknown("a call of a computed function")

    @staticmethod
    def _known_method(name: str, call: ast.Call) -> bool:
        if name in {"rename", "replace"}:
            return len(call.args) == 1 and not call.keywords or name == "replace" and len(call.args) >= 2
        if name == "copy":
            return not call.args and not call.keywords  # dict.copy(); Path.copy(target) writes
        return name in _SAFE_METHODS or name in _SELF_WRITERS or name == "open"

    def _module_of(self, node: ast.expr) -> str | None:
        """`os` for the name `os`, `os.path` for `os.path`; None for anything that is not an imported module."""
        if isinstance(node, ast.Name) and node.id in self.modules and not self.modules[node.id].startswith("pathlib."):
            return self.modules[node.id]
        if isinstance(node, ast.Attribute) and node.attr == "path" and self._module_of(node.value) == "os":
            return "os.path"
        return None

    def _targets(self, call: ast.Call) -> list[ast.expr]:
        """The expressions a known call writes."""
        func, keywords = call.func, {k.arg: k.value for k in call.keywords}
        if isinstance(func, ast.Name) and func.id == "open":
            return self._open(call.args[:1] or [keywords.get("file")], call.args[1:2], keywords)
        if not isinstance(func, ast.Attribute):
            return []
        module = self._module_of(func.value)
        if module:
            if module == "io" and func.attr == "open":
                return self._open(call.args[:1] or [keywords.get("file")], call.args[1:2], keywords)
            return [call.args[i] for i in _MODULE_CALLS[module][func.attr] if i < len(call.args)] if func.attr != "open" or module == "os" else []
        if func.attr == "open":
            return self._open([func.value], call.args[:1], keywords)
        if func.attr in _SELF_WRITERS:
            return [func.value]
        if func.attr in {"rename", "replace"} and len(call.args) == 1:
            return [func.value, call.args[0]]
        return []

    @staticmethod
    def _open(path: Sequence[ast.expr | None], mode_args: list[ast.expr], keywords: dict) -> list[ast.expr]:
        mode = keywords.get("mode", mode_args[0] if mode_args else None)
        reads = mode is None or (isinstance(mode, ast.Constant) and isinstance(mode.value, str)
                                 and not set(mode.value) & set("wax+"))
        if reads:
            return []
        if path[0] is None:
            raise _Unknown("open without a path")
        return [path[0]]

    def _resolve(self, node: ast.expr) -> list[str] | None:
        """The paths `node` can be; None when one cannot be worked out, the name refers to itself, or there
        are more than `_LIMIT`. Each node is worked out once."""
        if id(node) in self.memo:
            return self.memo[id(node)]
        if id(node) in self.busy:
            return None
        self.busy.add(id(node))
        try:
            result = self._resolve_new(node)
        finally:
            self.busy.discard(id(node))
        if result is not None and len(result) > _LIMIT:
            result = None
        self.memo[id(node)] = result
        return result

    def _resolve_new(self, node: ast.expr) -> list[str] | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return [node.value]
        if isinstance(node, ast.Name):
            if node.id in self.untracked or node.id not in self.values:
                return None
            return self._union([self._resolve(v) for v in self.values[node.id]])
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.Add)):
            glue = os.path.join if isinstance(node.op, ast.Div) else (lambda *s: "".join(s))
            return self._product([node.left, node.right], glue)
        if isinstance(node, ast.Call):
            return self._resolve_call(node)
        return None

    def _resolve_call(self, node: ast.Call) -> list[str] | None:
        func = node.func
        if node.keywords:
            return None
        if isinstance(func, ast.Name) and self.modules.get(func.id, "").startswith("pathlib."):
            return self._product(node.args, os.path.join) if node.args else ["."]
        if not isinstance(func, ast.Attribute):
            return None
        module = self._module_of(func.value)
        if (module, func.attr) in {("pathlib", c) for c in _PATH_CLASSES} | {("os.path", "join")}:
            return self._product(node.args, os.path.join) if node.args else ["."]
        if module is None and func.attr in {"resolve", "absolute", "expanduser"} and not node.args:
            return self._resolve(func.value)
        if module is None and func.attr == "joinpath":
            return self._product([func.value, *node.args], os.path.join)
        return None

    def _product(self, parts: list[ast.expr], glue) -> list[str] | None:
        maybe = [self._resolve(p) for p in parts]
        resolved = [r for r in maybe if r is not None]
        if len(resolved) < len(maybe) or _size(resolved) > _LIMIT:
            return None
        return list(dict.fromkeys(glue(*combo) for combo in itertools.product(*resolved)))

    @staticmethod
    def _union(options: list[list[str] | None]) -> list[str] | None:
        known = [o for o in options if o is not None]
        if not options or len(known) < len(options):
            return None
        return list(dict.fromkeys(p for o in known for p in o))


def _size(resolved: list) -> int:
    total = 1
    for r in resolved:
        total *= len(r)
    return total
