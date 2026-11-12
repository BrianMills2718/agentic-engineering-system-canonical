"""Behavior 1.2: a top-level function or class the plan does not declare with its types is reported."""

import yaml

from lockstep_support import REPO
from lockstep.aes_bridge import target
from lockstep.unplanned_symbols import main, symbol_problems

CODE = '''"""A module."""


def greet(name: str) -> str:
    return f"Hello, {name}!"


def shout(name):
    return greet(name).upper()


class Greeter:
    pass


def _helper() -> None:
    pass
'''


def _plan(*exports):
    return {"planned_artifacts": [{"id": "ART-G", "kind": "source", "locator": {"exact_path": "src/g.py"},
                                   "exports": list(exports)}]}


def _write(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src/g.py").write_text(CODE)
    return tmp_path


def test_declared_typed_symbols_are_not_reported(tmp_path):
    root = _write(tmp_path)
    assert symbol_problems(root, _plan("greet(name: str) -> str", "shout(name: str) -> str", "Greeter")) == []


def test_an_undeclared_function_or_class_is_reported_and_a_private_one_is_not(tmp_path):
    root = _write(tmp_path)
    problems = symbol_problems(root, _plan("greet(name: str) -> str"))
    assert [p.split(", which")[0] for p in problems] == [
        "src/g.py defines the function shout(name)", "src/g.py defines the class Greeter"]
    assert problems[0].endswith("add it to ART-G's exports with its types, through "
                                "`aes plan prepare/validate/accept`, or make it private (a name starting with _).")
    assert not any("_helper" in p for p in problems)


def test_an_export_without_types_is_reported(tmp_path):
    root = _write(tmp_path)
    assert symbol_problems(root, _plan("greet", "shout(name: str) -> str", "Greeter")) == [
        "ART-G (src/g.py) declares the function greet by name only: declare it with its types, "
        "as greet(name: str) -> str."]
    assert symbol_problems(root, _plan("greet(name) -> str", "shout(name: str)", "Greeter")) == [
        "ART-G (src/g.py) declares 'greet(name) -> str' without types for name: give every parameter and "
        "the return a type.",
        "ART-G (src/g.py) declares 'shout(name: str)' without types for return: give every parameter and "
        "the return a type."]


def test_an_unwritten_file_is_checked_from_the_plan_alone(tmp_path):
    assert symbol_problems(tmp_path, _plan("greet(name: str) -> str")) == []
    assert len(symbol_problems(tmp_path, _plan("greet(name)"))) == 1


def test_make_check_reports_an_undeclared_function_in_a_project(proj, capsys):
    t = yaml.safe_load((proj / ".aes/target.yaml").read_text())
    art = next(a for a in t["planned_artifacts"] if a["id"] == "ART-GREET")
    assert main(["--root", str(proj)]) == 1  # the example declares no exports, so greet is undeclared
    assert "src/greeter/__init__.py defines the function greet(name: str) -> str" in capsys.readouterr().out
    art["exports"] = ["greet(name: str) -> str"]
    (proj / ".aes/target.yaml").write_text(yaml.safe_dump(t, sort_keys=False))
    assert main(["--root", str(proj)]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == "unplanned_symbols: files=1 written=1 problems=0"
