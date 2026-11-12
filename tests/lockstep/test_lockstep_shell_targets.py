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
