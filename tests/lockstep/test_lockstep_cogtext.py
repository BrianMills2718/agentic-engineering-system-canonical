"""Behavior 3.1: cog copies the plan's text into the docstring, word for word (7.1 is tests/test_parent_text.py)."""


def test_docstring_holds_the_plan_text_word_for_word(planned):
    text = (planned / "src/greeter/__init__.py").read_text()
    for piece in ['NI-001: greet(name) returns "Hello, <name>!".', "SC-001: greet greets the name it is given.",
                  'Disproved if: greet("Ada") returns anything other than "Hello, Ada!".',
                  "Proven by: VS-GREET (tests/test_greet.py)"]:
        assert piece in text, piece
