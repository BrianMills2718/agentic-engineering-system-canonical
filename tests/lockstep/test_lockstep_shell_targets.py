"""Behavior 5.1 (lockstep-guard): the hook judges a shell command by the paths it writes, found the way
code2check's guard finds them (ported from code2-template `src/code2check/guard.py` at 6ce00a9).

The four cases of BrianMills2718/lockstep#111, on the greeter project (planned `src/greeter/__init__.py`,
governed root `src/`), under PCW_MODE=block.
"""

import pytest

from lockstep.hook import decide

NEW = "src/greeter/newfile.py"


def verdict(proj, command: str) -> str:
    out = decide({"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(proj)})
    return out["hookSpecificOutput"]["permissionDecision"] if out else "none"


@pytest.fixture
def block(monkeypatch):
    monkeypatch.setenv("PCW_MODE", "block")


@pytest.mark.req("lockstep-guard/a-heredoc-creating-an-unplanned-file-is-refused")
def test_heredoc_creating_an_unplanned_file_is_refused(proj, block):
    assert verdict(proj, f"cat > {NEW} <<'EOF'\nx = 1\nif a > b:\n    pass\nEOF") == "deny"


@pytest.mark.req("lockstep-guard/an-echo-redirect-creating-an-unplanned-file-is-refused")
def test_echo_redirect_creating_an_unplanned_file_is_refused(proj, block):
    assert verdict(proj, f"echo 'x = 1' > {NEW}") == "deny"


@pytest.mark.req("lockstep-guard/a-python-one-liner-creating-an-unplanned-file-is-refused")
def test_python_one_liner_creating_an_unplanned_file_is_refused(proj, block):
    assert verdict(proj, f"python -c \"open('{NEW}','w').write('x')\"") == "deny"


@pytest.mark.req("lockstep-guard/copying-a-planned-file-out-is-allowed")
def test_copying_a_planned_file_out_is_allowed(proj, block):
    assert verdict(proj, "cp src/greeter/__init__.py /tmp/x") == "allow"


@pytest.mark.parametrize("command", [
    "install src/greeter/__init__.py /tmp/y", "rsync -a src/greeter/__init__.py /tmp/y/",
    "python -c \"print(open('src/greeter/__init__.py').read())\"",
    "python -c \"open('src/greeter/__init__.py','r').read()\"",
    "python - <<'E'\nprint(open('src/greeter/__init__.py').read())\nE",
    "sudo cp src/greeter/__init__.py /tmp/y", "xargs -I{} cp {} /tmp/y < /dev/null",
    "cat src/greeter/__init__.py",
])
def test_reads_of_a_planned_file_are_not_refused(proj, block, command):
    assert verdict(proj, command) in ("allow", "none"), command


@pytest.mark.parametrize("command", [
    "cp /tmp/x src/greeter/__init__.py", "mv src/greeter/__init__.py /tmp/y", "mv /tmp/y src/greeter/__init__.py",
    "install /tmp/x src/greeter/__init__.py", "rsync /tmp/x src/greeter/__init__.py",
    "sed -i s/a/b/ src/greeter/__init__.py",
    "sudo cp /tmp/x src/greeter/__init__.py", "bash -c 'cp /tmp/x src/greeter/__init__.py'",
    "find src -name '*.py' -exec touch src/greeter/__init__.py \\;",
    "python -c \"import shutil; shutil.copy('/tmp/x','src/greeter/__init__.py')\"",
    "python - <<'E'\nopen('src/greeter/__init__.py', 'w').write('x')\nE",
    "dd if=/tmp/x of=src/greeter/__init__.py",
])
def test_writes_of_a_planned_file_are_refused(proj, block, command):
    assert verdict(proj, command) == "deny", command


def test_a_copy_writes_only_its_destination_and_a_move_both():
    from lockstep.shell_targets import shell_write_words
    assert shell_write_words("cp a b") == ["b"]
    assert shell_write_words("mv a b") == ["a", "b"]
    assert shell_write_words("python -c \"open('a').read()\"") == []


def test_segments_keep_quoted_separators_and_heredoc_bodies():
    from lockstep.shell_targets import segments
    assert segments("python -c \"a; b\" && ls") == ["python -c \"a; b\" ", " ls"]
    assert segments("cat > f <<E\nx > y\nE\nls") == ["cat > f <<E\nx > y", "ls"]


def test_code_that_writes_names_only_its_paths_not_its_keywords():
    from lockstep.shell_targets import shell_write_words
    assert shell_write_words("python -c \"import os; open('src/a.py','w').write(os.path.join('a','b'))\"") == ["src/a.py"]
    assert shell_write_words("python -c \"open('new.py','w').write('x')\"") == ["new.py"]


# The shape the edit hook refused in the 2026-11-28 Sonnet end-to-end run: a script that writes only an
# OpenSpec proposal, whose text names planned and unplanned source files.
SONNET_SCRIPT = (
    "python3 - <<'EOF'\nimport json, pathlib\nc = pathlib.Path(\"openspec/changes/add-greet\")\n"
    "(c/\"specs/core\").mkdir(parents=True, exist_ok=True)\n"
    "t = 'a'.replace('a', 'src/greeter/__init__.py')\n"
    "(c/\"proposal.md\").write_text(\"\"\"## Why\n\nTouches src/greeter/__init__.py and "
    f"{NEW}.\n\"\"\")\nEOF"
)


@pytest.mark.req("lockstep-guard/a-python-script-whose-written-text-names-a-planned-file-is-not-refused")
def test_a_python_script_whose_written_text_names_a_planned_file_is_not_refused(proj, block):
    assert verdict(proj, SONNET_SCRIPT) != "deny"


def test_python_code_writes_only_the_paths_its_write_calls_target():
    from lockstep.shell_targets import shell_write_words
    assert shell_write_words(SONNET_SCRIPT) == ["openspec/changes/add-greet/proposal.md"]
    assert shell_write_words(
        "python -c \"import shutil; shutil.copy('src/a.py', 'b/c.py')\"") == ["b/c.py"]


@pytest.mark.parametrize("command", [
    "python3 - <<'E'\nfrom pathlib import Path\np = Path('src/greeter') / '__init__.py'\np.write_text('x')\nE",
    "python3 - <<'E'\nimport pathlib\nfor n in ['__init__.py']:\n    (pathlib.Path('src/greeter')/n).write_text('x')\nE",
    "python3 - <<'E'\nn = input()\nopen(f'src/greeter/{n}', 'w').write('x  # src/greeter/__init__.py')\nE",
    "python3 - <<'E'\nimport subprocess\nsubprocess.run(['cp', '/tmp/x', 'src/greeter/__init__.py'])\nopen('log.txt', 'w').write('x')\nE",
    "python3 - <<'E'\nthis is not python, but it .write( src/greeter/__init__.py\nE",
])
def test_python_writes_of_a_planned_file_are_still_refused(proj, block, command):
    assert verdict(proj, command) == "deny", command


# Review probes of 2026-11-28 (fix/hook-heredoc-paths, first version): each pairs a write under `src/` with,
# where that write would not trigger the code-writes rule alone, a harmless `log.txt` write that does. Parsing
# must never miss a write the every-path rule catches.
T = "; open('log.txt','w').write('x')"
PROBES = {
 "append": "open('src/b.py','a').write('x')",
 "mode kw": "open('src/b.py', mode='w').write('x')",
 "file kw": "open(file='src/b.py', mode='w').write('x')",
 "star args": "open(*['src/b.py','w']).write('x')",
 "io.open": "import io; io.open('src/b.py','w').write('x')",
 "io alias": "import io as i; i.open('src/b.py','w').write('x')",
 "builtins.open": "import builtins; builtins.open('src/b.py','w').write('x')",
 "gzip.open": "import gzip; gzip.open('src/b.py','wt').write('x')",
 "open alias": "o = open; o('src/b.py','w').write('x')",
 "from io open": "from io import open as o; o('src/b.py','w').write('x')",
 "Path.open w": "import pathlib; pathlib.Path('src/b.py').open('w').write('x')",
 "Path.open mode kw": "import pathlib; pathlib.Path('src/b.py').open(mode='w').write('x')",
 "os.rename": "import os; os.rename('a','src/b.py')",
 "os.renames": "import os; os.renames('a','src/b.py')" + T,
 "os.makedirs": "import os; os.makedirs('src/newdir')" + T,
 "shutil.copy": "import shutil; shutil.copy('a','src/b.py')",
 "shutil.copy kw": "import shutil; shutil.copy('a', dst='src/b.py')",
 "from shutil copy": "from shutil import copy; copy('a','src/b.py')" + T,
 "shutil alias": "import shutil as sh; sh.copy('a','src/b.py')" + T,
 "os alias remove": "import os as o; o.remove('src/b.py')" + T,
 "from os remove": "from os import remove; remove('src/b.py')" + T,
 "getattr os": "import os; getattr(os,'remove')('src/b.py')" + T,
 "__import__ os": "__import__('os').remove('src/b.py')" + T,
 "__import__ subprocess": "__import__('subprocess').run(['cp','a','src/b.py'])" + T,
 "importlib subprocess": "import importlib; importlib.import_module('subprocess').run(['cp','a','src/b.py'])" + T,
 "os.system alias": "import os as o; o.system('cp a src/b.py')" + T,
 "os.execvpe": "import os; os.execvpe('cp',['cp','a','src/b.py'],{})" + T,
 "os.spawnvp": "import os; os.spawnvp(os.P_WAIT,'cp',['cp','a','src/b.py'])" + T,
 "os.posix_spawnp": "import os; os.posix_spawnp('cp',['cp','a','src/b.py'],{})" + T,
 "asyncio subprocess": "import asyncio; asyncio.run(asyncio.create_subprocess_exec('cp','a','src/b.py'))" + T,
 "pty.spawn": "import pty; pty.spawn(['cp','a','src/b.py'])" + T,
 "builtins.exec": "import builtins; builtins.exec(\"open('src/b.py','w')\")" + T,
 "eval": "eval(\"open('src/b.py','w')\")",
 "json.dump handle": "import json; json.dump({}, open('src/b.json','w'))",
 "np.save": "import numpy as np; np.save('src/b.npy',[1])" + T,
 "to_csv": "import pandas as pd; pd.DataFrame().to_csv('src/b.csv')" + T,
 "sqlite3": "import sqlite3; sqlite3.connect('src/b.db').execute('create table t(x)')" + T,
 "zip extract": "import zipfile; zipfile.ZipFile('/tmp/a.zip').extractall('src')" + T,
 "tar extract": "import tarfile; tarfile.open('/tmp/a.tar').extractall('src/x')" + T,
 "tempfile": "import tempfile; tempfile.NamedTemporaryFile(dir='src/x', delete=False)" + T,
 "urlretrieve": "import urllib.request as u; u.urlretrieve('http://x','src/b.py')" + T,
 "Path.write_bytes": "from pathlib import Path; Path('src/b.py').write_bytes(b'x')",
 "Path.mkdir": "from pathlib import Path; Path('src/newdir').mkdir()" + T,
 "Path.copy 3.14": "from pathlib import Path; Path('/tmp/a').copy('src/b.py')" + T,
 "Path.rename kw": "from pathlib import Path; Path('src/a.py').rename(target='/tmp/a')" + T,
 "os.open": "import os; os.write(os.open('src/b.py', os.O_WRONLY|os.O_CREAT), b'x')",
 "in function": "def f():\n    open('src/b.py','w').write('x')\nf()",
 "in lambda": "(lambda: open('src/b.py','w').write('x'))()",
 "in comprehension": "[open(p,'w').write('x') for p in ['src/b.py']]",
 "in class": "class C:\n    open('src/b.py','w').write('x')",
 "stdout redirect": "import sys; sys.stdout = open('src/b.py','w'); print('x')",
 "redirect_stdout": "import contextlib\nwith open('src/b.py','w') as f, contextlib.redirect_stdout(f): print(1)",
 "param shadow": "p = 'ok.md'\ndef w(p):\n    open(p,'w').write('x')\nw('src/b.py')",
 "augassign": "p = 'src/'\np += 'b.py'\nopen(p,'w').write('x')",
 "tuple unpack shadow": "p = 'ok.md'\na, p = 'x', 'src/b.py'\nopen(p,'w').write('x')",
 "annassign shadow": "p = 'ok.md'\np: str = 'src/b.py'\nopen(p,'w').write('x')",
 "walrus shadow": "p = 'ok.md'\nif (p := 'src/b.py'): open(p,'w').write('x')",
 "for tuple shadow": "p = 'ok.md'\nfor a, p in [('x','src/b.py')]: open(p,'w').write('x')",
 "except as shadow": "p = 'ok.md'\nopen(p,'w').write('x')",
 "chdir": "import os; os.chdir('src'); open('b.py','w').write('x')",
 "getattr write_text": "from pathlib import Path; getattr(Path('src/b.py'),'write_text')('x')",
 "bound method": "from pathlib import Path; w = Path('src/b.py').write_text; w('x')",
 "str.join trick": "open('/'.join(['src','b.py']),'w').write('x')",
 "fstring": "n='b.py'; open(f'src/{n}','w').write('x')",
 "concat": "open('src/' + 'b.py','w').write('x')",
 "logging FileHandler": "import logging; logging.FileHandler('src/b.log')" + T,
 "print file=": "print('x', file=open('src/b.py','w'))",
 "shutil.copyfileobj": "import shutil; shutil.copyfileobj(open('/tmp/a'), open('src/b.py','wb'))",
 "Path.write_text in with as": "from pathlib import Path\nwith Path('src/b.py') as p: pass\np.write_text('x')",
 "del rebind": "p='src/b.py'\ndel p\np='ok.md'\nopen(p,'w')",
}
GOVERNED = ("b.py", "b.json", "b.npy", "b.csv", "b.db", "src", "src/x", "newdir", "b.log", "src/a.py")


def _old_rule(command: str) -> list[str]:
    import lockstep.shell_targets as st
    real = st.python_write_paths
    st.python_write_paths = lambda segment: None
    try:
        return st.shell_write_words(command)
    finally:
        st.python_write_paths = real


def _h(code: str) -> str:
    return "python3 - <<'E'\n" + code + "\nE"


@pytest.mark.req("lockstep-guard/python-code-the-parser-cannot-vouch-for-keeps-the-every-path-rule")
@pytest.mark.parametrize("name", list(PROBES))
def test_parsing_never_misses_a_write_the_every_path_rule_catches(name):
    from lockstep.shell_targets import shell_write_words
    command = _h(PROBES[name])

    def hit(words):
        return any(w.endswith(GOVERNED) for w in words)
    if hit(_old_rule(command)):
        assert hit(shell_write_words(command)), (name, shell_write_words(command))


@pytest.mark.parametrize("command", [
    _h(f"open(file='{NEW}', mode='w').write('x')"),
    _h(f"import gzip; gzip.open('{NEW}','wt').write('x')"),
    _h(f"import shutil as sh; sh.copy('/tmp/x','{NEW}'); open('log.txt','w').write('done')"),
    _h(f"from shutil import copy; copy('/tmp/x','{NEW}'); open('log.txt','w').write('done')"),
    _h(f"import os; os.posix_spawnp('cp',['cp','/tmp/x','{NEW}'],{{}}); open('log.txt','w').write('d')"),
    _h(f"p = 'log.txt'\ndef w(p, t):\n    open(p,'w').write(t)\nw('{NEW}', 'x')\nw(p, 'done')"),
    _h(f"from pathlib import Path\nw = Path('{NEW}').write_text\nw('x')"),
    "python3 tools/gen.py <<'EOF'\nprint(file='" + NEW + "')\nEOF",
])
def test_code_the_parser_cannot_vouch_for_is_still_refused(proj, block, command):
    assert verdict(proj, command) == "deny", command


@pytest.mark.req("lockstep-guard/an-aliased-writer-keeps-the-every-path-rule")
def test_an_aliased_writer_keeps_the_every_path_rule(proj, block):
    assert verdict(proj, _h(f"import os as o; o.remove('{NEW}'); open('log.txt','w').write('x')")) == "deny"


@pytest.mark.req("lockstep-guard/a-keyword-argument-target-is-counted")
def test_a_keyword_argument_target_is_counted(proj, block):
    assert verdict(proj, _h(f"import shutil; shutil.copy('/tmp/x', dst='{NEW}')")) == "deny"


@pytest.mark.req("lockstep-guard/shell-expansion-in-python-text-keeps-the-every-path-rule")
@pytest.mark.parametrize("command", [
    "python3 - <<EOF\nopen('log.txt','w').write(\"$(cp /tmp/x " + NEW + ")\")\nEOF",
    "python3 -c \"open('log.txt','w').write('$(cp /tmp/x " + NEW + ")')\"",
    "python3 - <<EOF\nopen('log.txt','w').write(\"`cp /tmp/x " + NEW + "`\")\nEOF",
])
def test_shell_expansion_in_python_text_keeps_the_every_path_rule(proj, block, command):
    assert verdict(proj, command) == "deny", command


@pytest.mark.req("lockstep-guard/a-parser-crash-keeps-the-every-path-rule")
@pytest.mark.parametrize("code", [
    "x = " + "+".join(["1"] * 20000) + "\nopen('src/b.py','w')",
    "x = " + "(" * 300 + "1" + ")" * 300 + "\nopen('src/b.py','w')",
    "x = " + "[" * 1000 + "]" * 1000 + "\nopen('src/b.py','w')",
])
def test_a_parser_crash_keeps_the_every_path_rule(code):
    from lockstep.python_writes import python_write_paths
    from lockstep.shell_targets import shell_write_words
    assert python_write_paths(_h(code)) is None
    assert any(w.endswith("src/b.py") for w in shell_write_words(_h(code)))


def test_resolving_reassigned_paths_takes_milliseconds():
    import time
    from lockstep.shell_targets import shell_write_words
    reassigned = "from pathlib import Path\np = Path('src')\n" + "".join(f"p = p / 'd{i}'\n" for i in range(8))
    squared = "from pathlib import Path\na = Path('x')\na = Path('y')\n" + "".join(
        f"a{k} = {'a' if k == 1 else f'a{k - 1}'} / {'a' if k == 1 else f'a{k - 1}'}\n" for k in range(1, 7))
    loop = "from pathlib import Path\nfor n in [" + ",".join(f"'f{i}'" for i in range(30)) + "]:\n    (Path(n)/n/n/n/n)"
    for code in (reassigned + "p.write_text('z')", squared + "a6.write_text('z')", loop + ".write_text('z')"):
        started = time.perf_counter()
        shell_write_words(_h(code))
        assert time.perf_counter() - started < 0.1, code[:60]


@pytest.mark.parametrize("segment", [
    "python3 tools/gen.py <<'E'\nopen('a.md','w').write('src/greeter/x.py')",
    "echo python3 - <<'E'\nopen('a.md','w').write('src/greeter/x.py')",
    "python3 tools/gen.py -c \"open('a.md','w')\"",
    "python3 -m tool <<'E'\nopen('a.md','w')",
])
def test_only_a_program_python_reads_from_stdin_or_c_is_parsed(segment):
    from lockstep.python_writes import python_code
    assert python_code(segment) is None, segment
