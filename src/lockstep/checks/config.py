"""Read the commit checks' settings from `lockstep.yaml` at the repository root.

Implements: lockstep-checks/each-check-can-be-set-to-block-warn-or-off-in-lockstep-yaml

Keys (all optional; a missing file means every default):

    checks:   {trace: block, arch: warn, docmeta: off}   # name -> block | warn | off; default block
    sources:  {human_pattern: "brian"}                    # regex a `Source:` line must start with to count as human
    owner:    SomeGitHubOwner                             # no default; no commit check reads it yet
    likec4:   "1.60.0"                                    # LikeC4 version `arch` runs through npx

The file is data read with `yaml.safe_load`; nothing in it is executed.
"""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from lockstep.checks.arch import LIKEC4
from lockstep.checks.sources import DEFAULT_HUMAN_PATTERN

CHECK_NAMES = ("trace", "arch", "test-first", "sources", "docmeta", "project")
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

    def mode(self, name: str) -> str:
        """Return `block`, `warn` or `off` for a check (`block` when not set)."""
        return self.modes.get(name, "block")


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
    modes = {name: ("off" if mode is False else mode) for name, mode in modes.items()}  # YAML reads a bare `off` as False
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
    return Config(
        modes=dict(modes),
        human_pattern=pattern,
        owner=str(owner) if owner is not None else None,
        likec4=(str(likec4) if str(likec4).startswith("likec4@") else f"likec4@{likec4}") if likec4 is not None else LIKEC4,
    )
