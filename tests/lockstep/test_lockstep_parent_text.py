"""Behavior 7.1: a behavior's docstring carries its parent requirement in full, before its own text."""

from lockstep.parent_text import parent_lines


def test_docstring_carries_the_parent_requirement_in_full(planned):
    """A behavior's docstring repeats the requirement it belongs to (its AES outcome) word for word,
    because agents read what is in the file and do not follow references (wiki/behavior-layout.md)."""
    text = (planned / "src/greeter/__init__.py").read_text()
    assert "Part of OUT-001: greet returns a greeting." in text
    assert text.index("Part of OUT-001") < text.index("NI-001")


def test_every_parent_is_kept_whole_and_wrapped():
    long = "word " * 40
    lines = parent_lines({"outcomes": [{"id": "REQ-1", "statement": "short."},
                                       {"id": "REQ-2", "statement": long.strip()}]}, 40)
    assert lines[0] == "Part of REQ-1: short."
    assert all(len(line) <= 40 for line in lines)
    assert all(line.startswith("  ") for line in lines[2:])
    assert " ".join(line.strip() for line in lines[1:]) == f"Part of REQ-2: {long.strip()}"
