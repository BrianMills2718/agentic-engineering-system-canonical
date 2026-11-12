"""Behavior 3.2: after `make project`, every export the plan declares for a file is in its docstring as declared."""

import ast

import pytest

from lockstep_support import REPO
from lockstep.aes_bridge import target
from lockstep.signature_text import signature_lines


def test_signature_lines_copy_each_export_verbatim():
    ctx = {"subject": {"id": "ART-X", "exports": ["WIDTH", "render(ctx: dict, width: int = 76) -> list[str]"]}}
    assert signature_lines(ctx) == ["Declares (typed signatures, from the plan):", "  WIDTH",
                                    "  render(ctx: dict, width: int = 76) -> list[str]"]
    assert signature_lines({"subject": {"id": "TST-X"}}) == []


def test_an_export_that_cannot_sit_in_a_docstring_is_refused():
    with pytest.raises(ValueError, match="triple quote"):
        signature_lines({"subject": {"id": "ART-X", "exports": ['f(x: str = """) -> None']}})
