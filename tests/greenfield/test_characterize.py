"""`aes characterize`: revision-bound facts, Python AST extraction, symbol drift
(SC-GF-006) and dependency discovery for recorded evidence.

The repository under test is a temp Git repo holding the frozen whygame5
records plus small stand-in sources, so every fact is checked against a
revision the test made.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

import pytest

from agentic_engineering_system.characterize import (
    CharacterizeError,
    characterize,
    check,
    drift,
    render_report,
    running_version,
)
from agentic_engineering_system.characterize_python import (
    analyze,
    import_closure,
    module_name,
    parse_export,
)
from agentic_engineering_system.cli import main
from agentic_engineering_system.evidence import record
from agentic_engineering_system.records import TargetValidationError, load_target

REPO = Path(__file__).resolve().parents[2]
WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"
PASS = [sys.executable, "-c", "print('1 passed')"]

SOURCES = {
    "src/whygame5/__init__.py": '"""pkg"""\n__version__ = "0"\n',
    "src/whygame5/contracts.py": "from pydantic import BaseModel\n\nclass Proposal(BaseModel):\n    text: str\n",
    "src/whygame5/prompts.py": (
        "from __future__ import annotations\n\n"
        "from whygame5.contracts import Proposal\n\n"
        "PROMPT = 'why?'\n_PRIVATE = 1\n\n"
        "def render(topic: str, *, depth: int = 1) -> str:\n    return PROMPT + topic\n"
    ),
    "src/whygame5/graph.py": "import re\n\ndef normalize(s):\n    return re.sub(' ', '', s)\n",
    "src/whygame5/evaluator.py": "from . import graph\nfrom .contracts import Proposal\n",
    "tests/test_prompts.py": "from whygame5 import prompts\n\ndef test_ok():\n    assert prompts.PROMPT\n",
}


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
        cwd=root, capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _commit(root: Path, message: str) -> None:
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", message)


@pytest.fixture
def root(tmp_path: Path) -> Path:
    (tmp_path / ".aes").mkdir()
    shutil.copy(WHYGAME5_AES / "project.yaml", tmp_path / ".aes" / "project.yaml")
    shutil.copy(WHYGAME5_AES / "target.yaml", tmp_path / ".aes" / "target.yaml")
    for rel, text in SOURCES.items():
        _write(tmp_path, rel, text)
    _git(tmp_path, "init", "-q")
    _commit(tmp_path, "base")
    return tmp_path


def _add_exports(root: Path, artifact_id: str, exports: list[str]) -> None:
    path = root / ".aes" / "target.yaml"
    text = path.read_text(encoding="utf-8")
    anchor = f"  - id: {artifact_id}\n"
    assert anchor in text
    head, tail = text.split(anchor, 1)
    block, rest = tail.split("\n  - id: ", 1)
    items = ", ".join(f'"{e}"' for e in exports)
    path.write_text(f"{head}{anchor}{block}\n    exports: [{items}]\n  - id: {rest}", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Revision binding and determinism (ER-SC-GF-006-02, exit gate)
# --------------------------------------------------------------------------- #


def test_output_is_deterministic_apart_from_produced_at(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    a, b = characterize(root), characterize(root)
    assert a.model_dump(exclude={"produced_at"}) == b.model_dump(exclude={"produced_at"})
    assert [f.path for f in a.files] == sorted(f.path for f in a.files)

    assert main(["characterize", "--root", str(root)]) == 0
    first = capsys.readouterr().out
    assert main(["characterize", "--root", str(root)]) == 0
    assert capsys.readouterr().out == first
    assert "produced_at" not in first


def test_every_fact_is_bound_to_head_and_producer(root: Path) -> None:
    c = characterize(root)
    assert c.subject_revision == _git(root, "rev-parse", "HEAD")
    # The tests import this checkout's src/ (pytest pythonpath), so the producer names it.
    running = subprocess.run(["git", "describe", "--always", "--dirty"], cwd=REPO, capture_output=True,
                             text=True, check=True).stdout.strip()
    assert (c.producer.identity, c.producer.version) == (
        "aes", f"{version('agentic-engineering-system')} (running: {running})")
    assert c.dirty is False
    assert [f.path for f in c.files] == sorted(SOURCES)  # governed roots only: no .aes/, no pyproject
    prompts = next(f for f in c.files if f.path == "src/whygame5/prompts.py")
    assert prompts.blob_sha == _git(root, "rev-parse", "HEAD:src/whygame5/prompts.py")
    assert prompts.size == len(SOURCES["src/whygame5/prompts.py"].encode())

    # An uncommitted edit makes it dirty, but the facts stay those of HEAD.
    _write(root, "src/whygame5/prompts.py", "EDITED = 1\n")
    dirty = characterize(root)
    assert dirty.dirty is True
    assert dirty.subject_revision == c.subject_revision
    assert next(f for f in dirty.files if f.path == "src/whygame5/prompts.py") == prompts


# --------------------------------------------------------------------------- #
# Python AST facts
# --------------------------------------------------------------------------- #


def test_public_symbols_and_signatures(root: Path) -> None:
    facts = characterize(root).python_facts()["src/whygame5/prompts.py"]
    assert facts.module == "whygame5.prompts"
    assert [(s.name, s.kind, s.signature) for s in facts.symbols] == [
        ("PROMPT", "variable", None),
        ("render", "function", "(topic: str, *, depth: int=1) -> str"),
    ]


def test_import_edges_absolute_from_and_relative() -> None:
    modules = {module_name(p): p for p in [
        "src/pkg/__init__.py", "src/pkg/a.py", "src/pkg/b.py", "src/pkg/c.py",
        "src/pkg/sub/__init__.py", "src/pkg/sub/d.py", "src/pkg/sub/e.py",
        "tests/test_x.py", "tests/helpers.py",
    ]}
    assert modules["pkg"] == "src/pkg/__init__.py" and modules["tests.test_x"] == "tests/test_x.py"

    top = analyze("src/pkg/a.py", "import json\nimport pkg.b\nfrom pkg.c import thing\n", modules)
    assert top.imports == ["src/pkg/__init__.py", "src/pkg/b.py", "src/pkg/c.py"]  # json is not an edge

    sub = analyze("src/pkg/sub/d.py", "from . import e\nfrom .. import a\nfrom ..b import x\n", modules)
    assert sub.imports == ["src/pkg/__init__.py", "src/pkg/a.py", "src/pkg/b.py", "src/pkg/sub/__init__.py",
                           "src/pkg/sub/e.py"]

    init = analyze("src/pkg/sub/__init__.py", "from .d import y\n", modules)
    assert init.imports == ["src/pkg/__init__.py", "src/pkg/sub/d.py"]

    # A test directory without __init__.py sits on sys.path under pytest: bare sibling names resolve.
    test = analyze("tests/test_x.py", "import helpers\nfrom pkg.sub import d\n", modules)
    assert test.imports == ["src/pkg/__init__.py", "src/pkg/sub/__init__.py", "src/pkg/sub/d.py",
                            "tests/helpers.py"]
    # Inside a package there is no implicit relative import: `import a` is not pkg/a.py.
    assert analyze("src/pkg/b.py", "import a\n", modules).imports == []


def test_characterization_never_executes_consumer_code(root: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
    sentinel = tmp_path_factory.mktemp("sentinel") / "executed"
    _write(root, "src/whygame5/graph.py",
           f"open({str(sentinel)!r}, 'w').write('ran')\nraise SystemExit('imported')\n\ndef normalize(s):\n    return s\n")
    _write(root, "src/whygame5/evaluator.py", "def broken(:\n")
    _commit(root, "hostile sources")
    facts = characterize(root).python_facts()
    assert not sentinel.exists()
    assert [s.name for s in facts["src/whygame5/graph.py"].symbols] == ["normalize"]
    assert facts["src/whygame5/evaluator.py"].parse_error == "SyntaxError line 1: invalid syntax"


# --------------------------------------------------------------------------- #
# Symbol commitments and drift (ER-SC-GF-006-01)
# --------------------------------------------------------------------------- #


def test_renamed_committed_symbol_is_drift(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _add_exports(root, "ART-WG5-PROMPTS", ["PROMPT", "render(topic: str, *, depth: int = 1) -> str"])
    _commit(root, "commit exports")
    report = check(root)
    assert report.ok, render_report(report)
    assert [(d.kind, d.path) for d in report.drift] == [  # planned files this repo does not write
        ("unrealized", p) for p in ["src/whygame5/cli.py", "src/whygame5/report.py", "src/whygame5/runner.py",
                                    "tests/test_evaluator.py", "tests/test_replay.py"]
    ]

    _write(root, "src/whygame5/prompts.py", SOURCES["src/whygame5/prompts.py"].replace("PROMPT", "QUESTION"))
    _commit(root, "scratch: rename PROMPT")
    report = check(root)
    assert not report.ok
    failing = [(d.kind, d.path, d.artifact_id, d.detail) for d in report.drift if d.failing]
    assert failing == [("missing_export", "src/whygame5/prompts.py", "ART-WG5-PROMPTS",
                        "committed export 'PROMPT' is not a top-level public symbol")]
    assert main(["characterize", "--root", str(root)]) == 1
    assert "missing_export: src/whygame5/prompts.py (ART-WG5-PROMPTS)" in capsys.readouterr().err


def test_changed_signature_is_drift_and_formatting_is_not(root: Path) -> None:
    _add_exports(root, "ART-WG5-PROMPTS", ["render(topic:str,*,depth:int=1)->str"])
    _commit(root, "commit exports")
    assert check(root).ok

    _write(root, "src/whygame5/prompts.py",
           SOURCES["src/whygame5/prompts.py"].replace("depth: int = 1", "depth: int = 2"))
    _commit(root, "change default")
    (d,) = [d for d in check(root).drift if d.failing]
    assert (d.kind, d.detail) == (
        "signature_changed",
        "'render' committed (topic: str, *, depth: int=1) -> str, found (topic: str, *, depth: int=2) -> str",
    )


def test_orphans_come_from_the_characterized_revision(root: Path) -> None:
    _write(root, "src/whygame5/extra.py", "X = 1\n")
    _commit(root, "unplanned file")
    target = load_target(root / ".aes" / "target.yaml")
    orphans = [d for d in drift(target, characterize(root)) if d.kind == "orphan"]
    assert [(d.path, d.failing) for d in orphans] == [("src/whygame5/extra.py", True)]


def test_exports_only_on_python_source_artifacts(root: Path) -> None:
    _add_exports(root, "ART-WG5-TEST-PROMPTS", ["test_ok"])
    _add_exports(root, "ART-WG5-GRAPH", ["normalize", "normalize", "bad name"])
    with pytest.raises(TargetValidationError) as exc:
        load_target(root / ".aes" / "target.yaml")
    assert len(exc.value.violations) == 3
    text = "\n".join(exc.value.violations)
    assert "duplicate export 'normalize' at planned_artifacts[2] (ART-WG5-GRAPH).exports[1]" in text
    assert "export 'bad name' is not a Python identifier at planned_artifacts[2] (ART-WG5-GRAPH).exports[2]" in text
    assert ("exports at planned_artifacts[8] (ART-WG5-TEST-PROMPTS) require kind 'source' and a .py exact_path "
            "(got kind 'test', path 'tests/test_prompts.py')") in text


def test_parse_export_forms() -> None:
    assert parse_export("PROMPT") == ("PROMPT", None)
    assert parse_export("f(a, b: int = 3) -> None") == ("f", "(a, b: int=3) -> None")
    with pytest.raises(ValueError, match="not a function header"):
        parse_export("f(a,")


# --------------------------------------------------------------------------- #
# Dependency discovery for recorded evidence
# --------------------------------------------------------------------------- #


def test_closure_of_the_fixture_test_file(root: Path) -> None:
    facts = characterize(root).python_facts()
    assert import_closure("tests/test_prompts.py", facts) == [
        "src/whygame5/__init__.py", "src/whygame5/contracts.py", "src/whygame5/prompts.py",
    ]


def test_record_discovers_dependencies_and_keeps_declared_ones(root: Path) -> None:
    obs = record(root, "VS-WG5-PROMPTS", ["src/whygame5/graph.py"], command=PASS).observation
    assert obs.dependency_basis is not None
    assert obs.dependency_basis.model_dump() == {
        "locator": "tests/test_prompts.py",
        "discovered": ["src/whygame5/__init__.py", "src/whygame5/contracts.py", "src/whygame5/prompts.py"],
        "declared": ["src/whygame5/graph.py"],
    }
    assert obs.dependency_paths == [
        "src/whygame5/__init__.py", "src/whygame5/contracts.py", "src/whygame5/graph.py",
        "src/whygame5/prompts.py", "tests/test_prompts.py",
    ]


# --------------------------------------------------------------------------- #
# Producer version names the running code, not only the install (§13 note)
# --------------------------------------------------------------------------- #


def _checkout_with_module(tmp_path: Path) -> tuple[Path, Path]:
    """A main checkout tracking pkg/mod.py and a linked worktree one commit ahead:
    the layout in which an editable install reports the main checkout's version."""
    main_co = tmp_path / "main"
    _write(main_co, "pkg/mod.py", "X = 1\n")
    _git(main_co, "init", "-q")
    _commit(main_co, "base")
    _git(main_co, "worktree", "add", "-q", "-b", "lane", str(tmp_path / "lane"))
    lane = tmp_path / "lane"
    _write(lane, "pkg/mod.py", "X = 2\n")
    _commit(lane, "lane change")
    return main_co, lane


def test_running_version_names_the_checkout_that_is_executing(tmp_path: Path,
                                                              monkeypatch: pytest.MonkeyPatch) -> None:
    import agentic_engineering_system.characterize as ch

    monkeypatch.setattr(ch, "version", lambda _: "0.1.dev9+gabc")
    main_co, lane = _checkout_with_module(tmp_path)
    main_sha = _git(main_co, "rev-parse", "--short", "HEAD")
    lane_sha = _git(lane, "rev-parse", "--short", "HEAD")
    assert main_sha != lane_sha
    # Same installed version, but each names the tree its module file sits in.
    assert running_version(main_co / "pkg" / "mod.py") == f"0.1.dev9+gabc (running: {main_sha})"
    lane_version = running_version(lane / "pkg" / "mod.py")
    assert lane_version.startswith("0.1.dev9+gabc (running: ") and lane_version.endswith(")")
    assert _git(lane, "rev-parse", "HEAD").startswith(lane_version.split("running: ")[1].rstrip(")"))
    _write(lane, "pkg/mod.py", "X = 3\n")
    assert running_version(lane / "pkg" / "mod.py").endswith("-dirty)")


def test_running_version_is_the_install_alone_outside_a_tracking_checkout(tmp_path: Path,
                                                                          monkeypatch: pytest.MonkeyPatch) -> None:
    """A venv's site-packages inside a consumer checkout is not tracked by it: the
    consumer's commit must not be reported as the AES code's."""
    import agentic_engineering_system.characterize as ch

    monkeypatch.setattr(ch, "version", lambda _: "0.1.dev9+gabc")
    consumer = tmp_path / "consumer"
    _write(consumer, "README", "x\n")
    _git(consumer, "init", "-q")
    _commit(consumer, "base")
    _write(consumer, ".venv/lib/site-packages/pkg/mod.py", "X = 1\n")
    assert running_version(consumer / ".venv/lib/site-packages/pkg/mod.py") == "0.1.dev9+gabc"
    _write(tmp_path / "plain", "pkg/mod.py", "X = 1\n")
    assert running_version(tmp_path / "plain" / "pkg" / "mod.py") == "0.1.dev9+gabc"


def test_running_version_fails_when_neither_is_determinable(tmp_path: Path,
                                                            monkeypatch: pytest.MonkeyPatch) -> None:
    import agentic_engineering_system.characterize as ch
    from importlib.metadata import PackageNotFoundError

    def missing(name: str) -> str:
        raise PackageNotFoundError(name)

    monkeypatch.setattr(ch, "version", missing)
    _write(tmp_path / "plain", "pkg/mod.py", "X = 1\n")
    with pytest.raises(CharacterizeError, match="no producer version"):
        running_version(tmp_path / "plain" / "pkg" / "mod.py")
    main_co, _ = _checkout_with_module(tmp_path / "co")
    assert running_version(main_co / "pkg" / "mod.py").startswith("not installed (running: ")
