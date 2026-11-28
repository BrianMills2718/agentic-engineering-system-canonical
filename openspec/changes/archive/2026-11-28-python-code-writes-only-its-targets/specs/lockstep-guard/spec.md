## MODIFIED Requirements

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
