"""Read the commit checks' settings from `lockstep.yaml` at the repository root.

Implements: lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml

Requirement text (generated):
    lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml: `lockstep check
        <name>` (`trace`, `arch`, `test-first`, `sources`, `docmeta` and the others) SHALL read
        `checks:` in `lockstep.yaml` at the repository root, where each check is `block` (the
        default when absent or when there is no file), `warn` or `off`; `maintainability`,
        `helper-reuse` and `mutation` SHALL instead be `off` when absent, and a bare YAML `on` SHALL
        mean `block`. A failing `block` check SHALL exit 1; a failing `warn` check SHALL print a
        `warning:` line and exit 0; an `off` check SHALL not run, SHALL print `skipped (off)` and
        exit 0. A value other than those three, or an unknown check name, SHALL exit 2 naming it.
        The file's `sources.human_pattern` (default `brian`), `owner` (no default) and `likec4`
        (default `1.60.0`) settings SHALL be read from the same file. `lockstep check` with no name,
        or only `--repo`, `--base` and `--json`, SHALL keep running the whole-tree plan check.

Keys (all optional; a missing file means every default):

    checks:   {trace: block, arch: warn, docmeta: off}   # name -> block | warn | off; default block (off for DEFAULT_OFF)
    mutation: {issue_repo: OWNER/NAME, name: AES}         # `check mutation --issue`'s issue repository (default
                                                          # origin) and the name in its title (default origin's name)
    sources:  {human_pattern: "brian"}                    # regex a `Source:` line must start with to count as human
    owner:    SomeGitHubOwner                             # no default; no commit check reads it yet
    likec4:   "1.60.0"                                    # LikeC4 version `arch` runs through npx

The file is data read with `yaml.safe_load`; nothing in it is executed.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:config.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml

### Requirement: Each check can be set to block, warn or off in lockstep.yaml

`lockstep check <name>` (`trace`, `arch`, `test-first`, `sources`, `docmeta` and the others) SHALL read `checks:` in
`lockstep.yaml` at the repository root, where each check is `block` (the default when absent or when there
is no file), `warn` or `off`; `maintainability`, `helper-reuse` and `mutation` SHALL instead be `off` when absent,
and a bare YAML `on` SHALL mean `block`. A failing `block` check SHALL exit 1; a failing `warn` check SHALL print a
`warning:` line and exit 0; an `off` check SHALL not run, SHALL print `skipped (off)` and exit 0. A value
other than those three, or an unknown check name, SHALL exit 2 naming it. The file's `sources.human_pattern`
(default `brian`), `owner` (no default) and `likec4` (default `1.60.0`) settings SHALL be read from the
same file. `lockstep check` with no name, or only `--repo`, `--base` and `--json`, SHALL keep running the
whole-tree plan check.

Source: Brian, 2026-11-25: "ia prpove yourr ecommednations" (the three checks become Lockstep checks each repository switches on itself, off by default); earlier Brian, 2026-11-11, approving the one-tool design ("i approve single tool desing re d4"; `proposals/one-planning-tool/DESIGN.md`, slice 4: the checks are Lockstep's, each switchable so another repository can adopt them one at a time).

#### Scenario: A missing lockstep.yaml means every check blocks

- **GIVEN** a repository with no `lockstep.yaml` and a spec requirement with no implementer
- **WHEN** `lockstep check trace` runs
- **THEN** it exits 1 and prints `RESULT trace findings=2 exit=1`

#### Scenario: Warn prints a warning and exits zero

- **GIVEN** `checks: {trace: warn}` and a failing trace check
- **WHEN** `lockstep check trace` runs
- **THEN** it prints `warning: trace failed` and exits 0

#### Scenario: Off skips the check and exits zero

- **GIVEN** `checks: {trace: off}`
- **WHEN** `lockstep check trace` runs
- **THEN** it prints `skipped (off)`, runs nothing and exits 0

#### Scenario: Block set explicitly exits one and other checks keep their own mode

- **GIVEN** `checks: {trace: block, docmeta: off}`
- **WHEN** `lockstep check trace` and `lockstep check docmeta` run
- **THEN** trace exits 1 and docmeta is skipped with exit 0

#### Scenario: A bad mode or unknown check is an error

- **GIVEN** `checks: {trace: sometimes}`, or `checks: {nonsense: warn}`
- **WHEN** the settings are read
- **THEN** reading fails naming the value, and `lockstep check trace` exits 2

#### Scenario: Defaults when keys are absent

- **GIVEN** a `lockstep.yaml` with none of `checks`, `sources`, `owner`, `likec4`
- **WHEN** the settings are read
- **THEN** the human pattern is `brian`, the owner is unset and LikeC4 is `likec4@1.60.0`

#### Scenario: LikeC4 pin and owner are read

- **GIVEN** `likec4: 1.70.0` and `owner: Acme`
- **WHEN** the settings are read
- **THEN** LikeC4 is `likec4@1.70.0` and the owner is `Acme`

#### Scenario: Lockstep check without a name still runs the tree check

- **GIVEN** `lockstep check --repo PATH`
- **WHEN** the command runs
- **THEN** the whole-tree plan check runs, as before

#### Scenario: The lockstep command runs a named check

- **GIVEN** an installed Lockstep and a repository failing the trace check
- **WHEN** `lockstep check trace --repo PATH` runs as a process
- **THEN** it prints the trace RESULT line and exits 1

#### Scenario: The three switched-on checks are off when absent

- **GIVEN** a `lockstep.yaml` that does not name `maintainability`, `helper-reuse` or `mutation`
- **WHEN** the settings are read
- **THEN** those three are `off` and `trace` is `block`; `mutation: on` reads as `block`, and `mutation.issue_repo` and
  `mutation.name` are read (an `issue_repo` that is not `OWNER/NAME` is an error)

Tested by: tests/lockstep/checks/test_lockstep_checks_config.py
[[[end]]]
"""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from lockstep.checks.arch import LIKEC4
from lockstep.checks.sources import DEFAULT_HUMAN_PATTERN

CHECK_NAMES = ("trace", "arch", "test-first", "sources", "docmeta", "project", "instructions", "changed", "suppressions",
               "maintainability", "helper-reuse", "mutation")
# Checks a repository switches on itself: absent from `checks:` means off, not block.
DEFAULT_OFF = ("maintainability", "helper-reuse", "mutation")
MODES = ("block", "warn", "off")
SIDE_FILE = "lockstep.yaml"


class ConfigError(ValueError):
    """`lockstep.yaml` holds a value the commit checks cannot use."""


@dataclass(frozen=True)
class Config:
    """The commit checks' settings with defaults filled in."""

    modes: dict[str, str] = field(default_factory=dict)
    human_pattern: str = DEFAULT_HUMAN_PATTERN
    owner: str | None = None
    likec4: str = LIKEC4
    mutation_issue_repo: str | None = None
    mutation_name: str | None = None

    def mode(self, name: str) -> str:
        """Return `block`, `warn` or `off` for a check (`off` when not set for a DEFAULT_OFF check, else `block`)."""
        return self.modes.get(name, "off" if name in DEFAULT_OFF else "block")


def _mutation_settings(data: dict) -> tuple[str | None, object]:
    """(mutation.issue_repo, mutation.name) from lockstep.yaml's `mutation:` mapping; raises ConfigError when malformed."""
    mutation = data.get("mutation") or {}
    if not isinstance(mutation, dict):
        raise ConfigError(f"{SIDE_FILE}: mutation must be a mapping")
    issue_repo = mutation.get("issue_repo")
    if issue_repo is not None and (not isinstance(issue_repo, str) or "/" not in issue_repo):
        raise ConfigError(f"{SIDE_FILE}: mutation.issue_repo must be OWNER/NAME")
    return issue_repo, mutation.get("name")


def load(root: Path) -> Config:
    """Read the commit-check settings from `root/lockstep.yaml`.

    Args:
        root: Repository root.

    Returns:
        The settings; all defaults when the file or a key is absent.

    Raises:
        ConfigError: A mode is not block, warn or off, a check name is unknown, or a value has the wrong type.
    """
    path = root / SIDE_FILE
    if not path.is_file():
        return Config()
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"{SIDE_FILE} must hold a mapping")
    modes = data.get("checks") or {}
    if not isinstance(modes, dict):
        raise ConfigError(f"{SIDE_FILE}: checks must map a check name to block, warn or off")
    # YAML reads a bare `off` as False and a bare `on` as True
    modes = {name: ("off" if mode is False else "block" if mode is True else mode) for name, mode in modes.items()}
    for name, mode in modes.items():
        if name not in CHECK_NAMES:
            raise ConfigError(f"{SIDE_FILE}: checks names unknown check {name!r}; known: {', '.join(CHECK_NAMES)}")
        if mode not in MODES:
            raise ConfigError(f"{SIDE_FILE}: check {name} is {mode!r}; it must be one of {', '.join(MODES)}")
    sources = data.get("sources") or {}
    if not isinstance(sources, dict):
        raise ConfigError(f"{SIDE_FILE}: sources must be a mapping")
    pattern = sources.get("human_pattern", DEFAULT_HUMAN_PATTERN)
    if not isinstance(pattern, str) or not pattern:
        raise ConfigError(f"{SIDE_FILE}: sources.human_pattern must be a non-empty regex string")
    owner = data.get("owner")
    likec4 = data.get("likec4")
    issue_repo, mutation_name = _mutation_settings(data)
    return Config(
        modes=dict(modes),
        human_pattern=pattern,
        owner=str(owner) if owner is not None else None,
        likec4=(str(likec4) if str(likec4).startswith("likec4@") else f"likec4@{likec4}") if likec4 is not None else LIKEC4,
        mutation_issue_repo=issue_repo,
        mutation_name=str(mutation_name) if mutation_name is not None else None,
    )
