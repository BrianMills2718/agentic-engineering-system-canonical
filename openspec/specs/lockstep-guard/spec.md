# lockstep-guard Specification

## Purpose

Lockstep's edit hook judges a shell command by the paths it writes, found by code2check's shell-target parser (`src/lockstep/shell_targets.py`; `proposals/one-planning-tool/DESIGN.md`, slice 3).

## Requirements

### Requirement: Shell commands are judged by the paths they write

The edit hook SHALL find the files a shell command writes the way code2check's guard does: redirect and tee
targets read as shell words, the files `mv`, `touch`, `sed -i` and the like write, only the destination of a
copy (`cp`, `install`, `rsync`), and the paths named by code in the command (a `python -c`, a heredoc script)
only when that code calls something that writes; a `cd` in the command SHALL be followed. In block mode it
SHALL refuse a command that writes a file under a governed folder that the plan does not declare, and it
SHALL NOT refuse a command that only reads a planned file.

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md, slice 3: "Port code2check's shell-target parsing. Done when lifelike replays the four cases from lockstep#111").

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

### Requirement: A refusal lists the files the plan allows

When the edit hook refuses (or warns about) a write to a file the plan does not name, its message SHALL also list the files the plan does allow, read from whichever plan is in use (`lockstep.yaml` `layout:` rows or the planned artifacts of `.aes/target.yaml`): those in the refused file's folder first, at most 15, then "and N more".

Source: Brian, 2026-11-11, "i approve single tool desing re d4" (proposals/one-planning-tool/DESIGN.md); acceptance entries A2 and A3 in docs/planning/acceptance-criteria.json

#### Scenario: A refusal lists the files the plan allows

- **GIVEN** a plan that names `src/greeter/__init__.py` and PCW_MODE=block
- **WHEN** an agent writes `src/greeter/extra.py`, by an edit or by a shell command
- **THEN** the refusal message lists `src/greeter/__init__.py` under "The plan does allow these files" and no more than 15 paths, with "and N more" for the rest
