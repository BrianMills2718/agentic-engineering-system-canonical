"""Helpers that build small throwaway repositories for the commit checks to run on (from code2check's conftest)."""

from pathlib import Path
import textwrap

import pytest


def write(root: Path, rel: str, text: str) -> Path:
    """Write dedented text to a file under root, creating parent folders."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip())
    return path


SPEC = """
    # core Specification

    ## Purpose
    Example.

    ## Requirements
    ### Requirement: Do the thing
    The tool SHALL do the thing.

    #### Scenario: It works
    - **WHEN** called
    - **THEN** it works
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repository with one spec and nothing else."""
    write(tmp_path, "openspec/specs/core/spec.md", SPEC)
    (tmp_path / "src/pkg").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    return tmp_path
