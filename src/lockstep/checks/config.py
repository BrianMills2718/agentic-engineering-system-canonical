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
    planning: {gate: block, one_page_plans: warn}         # ship's two planning gates; ship reads them from the
                                                          # default branch (ship/planning-gates-are-set-in-lockstep-yaml)

The file is data read with `yaml.safe_load`; nothing in it is executed.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:checks:config.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml, ship/planning-gates-are-set-in-lockstep-yaml, ship/add-on-gates-switch-off-from-the-copier-answers

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

### Requirement: Planning gates are set in lockstep.yaml

`ship` SHALL read `planning.gate` (the planning-package gate) and `planning.one_page_plans` (the one-page-plan check) from `lockstep.yaml` on the default branch at `origin`, never from the branch being shipped. Each SHALL be `block`, `warn` or `off`, a bare YAML `true` meaning `block` and `false` meaning `off`; an absent file, section or key SHALL mean `block`. A gate SHALL be off when either this setting or the `.copier-answers.yml` key says off, and the printed and logged line SHALL name the file that said so (`ship: planning gate: off (lockstep.yaml planning.gate: off)`). Under `warn`, a plan verdict (a validator rejection, a missing planning package, an incomplete one-page plan or a plan-list refusal) SHALL print and log `ship: warning: <gate>: <reason>; not refused (lockstep.yaml planning.<key>: warn)` and the merge SHALL go on, while a validator that cannot be fetched or cannot run SHALL still refuse. Any other value SHALL refuse the merge naming the value, with nothing pushed. The prior-art check has no switch.

Source: Brian, 2026-11-25: "yes it should hold all 4 parts btu the whole systm should be configurable so you can congfigure what is on or off or any other settings. for any piece" (docs/planning/next.goal.md, slice 1); the prior-art exception: Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search ... that needs to be ienforced".

#### Scenario: Off in lockstep.yaml on the default branch skips the gate

- **GIVEN** a new repository with no planning package whose default branch's `lockstep.yaml` says `planning: {gate: off}`
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints `ship: planning gate: off (lockstep.yaml planning.gate: off)`

#### Scenario: A branch cannot switch its own planning gate off in lockstep.yaml

- **GIVEN** a new repository with no planning package and a branch whose own `lockstep.yaml` says `planning: {gate: off}`
- **WHEN** ship runs
- **THEN** it is refused as before

#### Scenario: Warn passes a plan verdict

- **GIVEN** a new repository with no planning package whose default branch's `lockstep.yaml` says `planning: {gate: warn}`
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints a `ship: warning: planning gate:` line

#### Scenario: Warn still refuses a validator that cannot be fetched

- **GIVEN** a repository with a planning package, `planning: {gate: warn}` on the default branch and a company-planning source that cannot be fetched
- **WHEN** ship runs
- **THEN** it is refused and nothing is pushed

#### Scenario: A bad planning mode refuses

- **GIVEN** `planning: {gate: sometimes}` on the default branch
- **WHEN** ship runs
- **THEN** it exits 1 naming `sometimes`, with nothing pushed

### Requirement: Add-on gates switch off from the copier answers

`scripts/ship.py` SHALL read the keys `ship_planning_gate` and `ship_one_page_plans` from `.copier-answers.yml` on the default branch at `origin` (never from the branch being shipped, so a branch cannot turn its own gate off), reading each as a top-level `key: value` line. When a key's value is `false` (any letter case), ship SHALL skip that gate (the whole planning gate with its plan-repair and upkeep exceptions, or the one-page-plan check) and print and log `ship: planning gate: off (.copier-answers.yml ship_planning_gate: false)` or `ship: one-page plans: off (.copier-answers.yml ship_one_page_plans: false)`. A missing file, a missing key or any other value SHALL leave the gate on. The prior-art check is core and has no switch.

Source: Brian, 2026-11-20: "the whole thing should be configurable and shareable/protable. we shoudl start with the minimal core than add on other things as needed after the first minimal core milestone". The copier answers file as the one switch, and these two gates as add-ons, inferred by agent in docs/planning/minimal-core-2026-11-20.md sections 5 and 7.

#### Scenario: The planning gate is switched off

- **GIVEN** a new repository with no planning package whose `.copier-answers.yml` says `ship_planning_gate: false`
- **WHEN** ship runs with a passing check
- **THEN** it merges and prints `ship: planning gate: off (.copier-answers.yml ship_planning_gate: false)`

#### Scenario: The one-page-plan check is switched off

- **GIVEN** a branch adding an incomplete one-page plan, in a repository whose `.copier-answers.yml` says `ship_one_page_plans: false`
- **WHEN** ship runs with a passing check
- **THEN** it merges

#### Scenario: No answers file keeps every gate on

- **GIVEN** a new repository with no planning package and no `.copier-answers.yml` on the default branch, or one that only the branch being shipped adds
- **WHEN** ship runs
- **THEN** it is refused as before

Tested by: tests/lockstep/checks/test_lockstep_checks_config.py

Declares (typed signatures, from the plan):
  planning_modes(data: object) -> dict[str, str]
  planning_setting(repo: Path, key: str) -> str
  copier_answer_on(repo: Path, key: str) -> bool
  validator_source(repo: Path) -> tuple[str, str] | None
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
# ship's two planning gates (lockstep.yaml `planning:`), read by ship from the default branch: docs/planning/next.goal.md.
PLANNING_KEYS = ("gate", "one_page_plans")


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
    planning: dict[str, str] = field(default_factory=lambda: dict.fromkeys(PLANNING_KEYS, "block"))

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


def planning_modes(data: object) -> dict[str, str]:
    """`block`, `warn` or `off` for each of PLANNING_KEYS from a parsed lockstep.yaml; `block` when absent.

    Implements: ship/planning-gates-are-set-in-lockstep-yaml

    Requirement text (generated):
        ship/planning-gates-are-set-in-lockstep-yaml: `ship` SHALL read `planning.gate` (the
            planning-package gate) and `planning.one_page_plans` (the one-page-plan check) from
            `lockstep.yaml` on the default branch at `origin`, never from the branch being shipped.
            Each SHALL be `block`, `warn` or `off`, a bare YAML `true` meaning `block` and `false`
            meaning `off`; an absent file, section or key SHALL mean `block`. A gate SHALL be off
            when either this setting or the `.copier-answers.yml` key says off, and the printed and
            logged line SHALL name the file that said so (`ship: planning gate: off (lockstep.yaml
            planning.gate: off)`). Under `warn`, a plan verdict (a validator rejection, a missing
            planning package, an incomplete one-page plan or a plan-list refusal) SHALL print and
            log `ship: warning: <gate>: <reason>; not refused (lockstep.yaml planning.<key>: warn)`
            and the merge SHALL go on, while a validator that cannot be fetched or cannot run SHALL
            still refuse. Any other value SHALL refuse the merge naming the value, with nothing
            pushed. The prior-art check has no switch.

    Raises:
        ConfigError: The file or its `planning:` section is not a mapping, a key is unknown, or a mode is not one of MODES.
    """
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ConfigError(f"{SIDE_FILE} must hold a mapping")
    planning = data.get("planning") or {}
    if not isinstance(planning, dict):
        raise ConfigError(f"{SIDE_FILE}: planning must be a mapping")
    modes = {}
    for key in PLANNING_KEYS:
        mode = planning.get(key, "block")
        mode = "off" if mode is False else "block" if mode is True else mode  # YAML reads bare on/off as booleans
        if mode not in MODES:
            raise ConfigError(f"{SIDE_FILE}: planning.{key} is {mode!r}; it must be one of {', '.join(MODES)}")
        modes[key] = mode
    unknown = sorted(str(k) for k in set(planning) - set(PLANNING_KEYS) - {"validator", "skills"})  # slice 2 and 3 keys
    if unknown:
        raise ConfigError(f"{SIDE_FILE}: planning has unknown key {unknown[0]!r}; known: {', '.join(PLANNING_KEYS)}, validator, skills")
    return modes


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
    planning = planning_modes(data)
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
        planning=planning,
    )


def planning_setting(repo: Path, key: str) -> str:
    """`planning.<key>` from `lockstep.yaml` on the default branch at origin, never the branch being shipped, so a
    branch cannot turn its own gate off; see planning_modes.

    Raises:
        ConfigError: That file is not YAML, or its `planning:` section is wrong (planning_modes).
    """
    try:
        data = yaml.safe_load(_on_default_branch(repo, SIDE_FILE))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{SIDE_FILE} on the default branch is not YAML ({exc})") from exc
    return planning_modes(data)[key]


def _on_default_branch(repo: Path, name: str) -> str:
    """The text of file `name` on the default branch at origin; empty when it or the branch is missing."""
    import subprocess

    def read(*args: str) -> str:
        done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, errors="replace")
        return done.stdout if done.returncode == 0 else ""
    default = read("symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD").strip() or "origin/main"
    return read("show", f"{default}:{name}")


def copier_answer_on(repo: Path, key: str) -> bool:
    """False only when `.copier-answers.yml` on the default branch at origin says `key: false`; else True.

    Read from the default branch, never the branch being shipped, so a branch cannot turn its own gate off.

    Implements: ship/add-on-gates-switch-off-from-the-copier-answers

    Requirement text (generated):
        ship/add-on-gates-switch-off-from-the-copier-answers: `scripts/ship.py` SHALL read the keys
            `ship_planning_gate` and `ship_one_page_plans` from `.copier-answers.yml` on the default
            branch at `origin` (never from the branch being shipped, so a branch cannot turn its own
            gate off), reading each as a top-level `key: value` line. When a key's value is `false`
            (any letter case), ship SHALL skip that gate (the whole planning gate with its
            plan-repair and upkeep exceptions, or the one-page-plan check) and print and log `ship:
            planning gate: off (.copier-answers.yml ship_planning_gate: false)` or `ship: one-page
            plans: off (.copier-answers.yml ship_one_page_plans: false)`. A missing file, a missing
            key or any other value SHALL leave the gate on. The prior-art check is core and has no
            switch.
    """
    import re
    found = re.search(rf"^{re.escape(key)}:[ \t]*(\S+)[ \t]*$", _on_default_branch(repo, ".copier-answers.yml"), re.M)
    return not (found and found.group(1).strip("'\"").lower() == "false")


def validator_source(repo: Path) -> tuple[str, str] | None:
    """(address, branch) from `planning.validator` in lockstep.yaml on the default branch at origin, else None.

    Raises:
        ConfigError: That file is not YAML, or `planning.validator` is not a mapping of a text `repo` and optional `ref`.
    """
    try:
        data = yaml.safe_load(_on_default_branch(repo, SIDE_FILE)) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(f"{SIDE_FILE} on the default branch is not YAML ({exc})") from exc
    planning = data.get("planning") if isinstance(data, dict) else None
    setting = planning.get("validator") if isinstance(planning, dict) else None
    if setting is None:
        return None
    if (not isinstance(setting, dict) or set(setting) - {"repo", "ref"} or not isinstance(setting.get("repo"), str)
            or not isinstance(setting.get("ref", "main"), str)):
        raise ConfigError(f"{SIDE_FILE}: planning.validator must be a mapping of a text repo and an optional text ref "
                          f"(a branch), not {setting!r}")
    return setting["repo"], setting.get("ref", "main")
