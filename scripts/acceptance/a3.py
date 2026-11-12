"""A3 run: the commit checks, on four real commits in a throwaway git repository.

Writes docs/planning/runs/lockstep-acceptance/a3.json. Each commit is made on its own branch from the same base
commit; the matching `lockstep check <name>` is run on it (test-first compares with the base, `--base main`).
"""

import shutil
import tempfile
import textwrap
from pathlib import Path

from _common import BIN, Trace, git, tree

SPEC = '''
# core Specification

## Purpose
Example.

## Requirements
### Requirement: Greet

The tool SHALL greet.

Source: inferred by agent, the acceptance run's fixture.

#### Scenario: It greets
- **WHEN** called
- **THEN** it says hello
'''
SPEC_NEW_SCENARIO = SPEC + '''
#### Scenario: It also greets politely
- **WHEN** called politely
- **THEN** it says hello
'''
SPEC_NO_SOURCE = SPEC + '''
### Requirement: Say goodbye

The tool SHALL say goodbye.

#### Scenario: It says goodbye
- **WHEN** called
- **THEN** it says goodbye
'''
SPEC_CLEAN = SPEC + '''
### Requirement: Say goodbye

The tool SHALL say goodbye.

Source: inferred by agent, the acceptance run's fixture.

#### Scenario: It says goodbye
- **WHEN** called
- **THEN** it says goodbye
'''
MODEL = '''
specification { element component }
model {
  cli = component 'CLI' { metadata { python 'app.cli' } }
  detect = component 'Detect' { metadata { python 'app.detect' } }
  cli -> detect 'calls'
}
views { view index { include * } }
'''
GREET_TEST = '''
import pytest
from app.detect import greet


@pytest.mark.req("core/it-also-greets-politely")
def test_greets_politely():
    assert greet() == "hello"
'''
BASE = {
    "openspec/specs/core/spec.md": SPEC,
    "docs/architecture/model.c4": MODEL,
    "src/app/__init__.py": "",
    "src/app/detect.py": 'def greet():\n    return "hello"\n',
    "src/app/cli.py": "from app.detect import greet\n\n\ndef main():\n    return greet()\n",
    "tests/test_core.py": ('import pytest\nfrom app.cli import main\n\n\n@pytest.mark.req("core/it-greets")\n'
                           'def test_greets():\n    assert main() == "hello"\n'),
    ".gitignore": "__pycache__/\n.pytest_cache/\n",
}


def put(repo: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def main() -> int:
    t = Trace("A3", "The commit checks refuse a commit that breaks the plan's rules")
    t.extra["pytest_in_lockstep_env"] = t.run("pytest version in Lockstep's environment (test-first runs pytest)",
                                              [str(BIN / "python"), "-m", "pytest", "--version"], Path.cwd())["stdout"]["text"]
    repo = Path(tempfile.mkdtemp(prefix="a3-repo-")) / "demo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    put(repo, BASE)
    lock = lambda *a, cwd=repo: t.run(" ".join(["lockstep", "check", *a]), [str(BIN / "lockstep"), "check", *a], cwd)
    lock_arch_gen = lock("arch", "gen")  # the base commit carries the import contracts the diagram generates
    t.extra["base_arch_gen"] = {"exit_code": lock_arch_gen["exit_code"]}
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    base = git(repo, "rev-parse", "HEAD").strip()
    t.extra["base_commit"] = base
    t.extra["files_at_base"] = tree(repo)

    def branch(name: str, files: dict[str, str], message: str) -> str:
        git(repo, "checkout", "-q", "-b", name, "main")
        put(repo, files)
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", message)
        return git(repo, "rev-parse", "--short", "HEAD").strip()

    def verdict(step: dict) -> str:
        return "refused" if step["exit_code"] != 0 else "accepted"

    def output(step: dict) -> str:
        return step["stdout"]["text"] + step["stderr"]["text"]

    cases = [
        ("test-first", "A new test that already passed before the change",
         {"openspec/specs/core/spec.md": SPEC_NEW_SCENARIO, "tests/test_greet.py": GREET_TEST},
         "add a test for a new scenario; the code already does it", ["test-first", "--base", "main"],
         "tests/test_greet.py::test_greets_politely"),
        ("arch", "An import the architecture diagram forbids",
         {"src/app/detect.py": 'from app.cli import main\n\n\ndef greet():\n    return "hello"\n'},
         "detect imports cli (the diagram has no arrow from detect to cli)", ["arch", "check"], "app.detect"),
        ("sources", "A requirement with no Source line",
         {"openspec/specs/core/spec.md": SPEC_NO_SOURCE}, "add a requirement without a Source line",
         ["sources"], "core/say-goodbye"),
    ]
    for name, label, files, message, argv, token in cases:
        sha = branch(f"bad-{name}", files, message)
        changed = git(repo, "diff", "--name-only", "main", "HEAD").split()
        step = lock(*argv)
        refused = step["exit_code"] != 0
        named = token in output(step)
        should = f"refused by {name}, message names {token}"
        did = (f"refused by {name}, message names {token}" if refused and named else
               f"refused by {name}, message does not name {token}" if refused else f"accepted by {name}")
        t.row(name, label, should, did, step["name"],
              {"commit": sha, "commit_message": message, "files_changed": changed, "check": step["command"],
               "exit_code": step["exit_code"], "message": output(step)})
        if name == "arch":  # extra evidence, outside the verdict: does import-linter itself see the forbidden import?
            t.extra["arch_import_linter_probe"] = t.run(
                "probe: uvx --from import-linter lint-imports (not part of `lockstep check`)",
                "PYTHONPATH=src uvx --quiet --from import-linter lint-imports", repo)
    # the clean commit: all three checks accept it
    sha = branch("clean", {"openspec/specs/core/spec.md": SPEC_CLEAN, "src/app/detect.py":
                           'def greet():\n    return "hello"\n\n\ndef goodbye():\n    return "bye"\n',
                           "tests/test_bye.py": 'import pytest\nfrom app.detect import goodbye\n\n\n'
                           '@pytest.mark.req("core/it-says-goodbye")\ndef test_bye():\n    assert goodbye() == "bye"\n'},
                "add goodbye, with its requirement, source and test")
    steps = [lock("test-first", "--base", "main"), lock("arch", "check"), lock("sources")]
    done = [verdict(s) for s in steps]
    # test-first on this commit: the new test fails on the base (goodbye does not exist there), as it should.
    t.row("clean", "A clean commit: a real new test that fails on the base, an allowed import, a Source line",
          "accepted by all three checks", "accepted by all three checks" if set(done) == {"accepted"} else
          "refused by " + ", ".join(n for n, d in zip(("test-first", "arch", "sources"), done) if d == "refused"),
          steps[0]["name"] + " + arch check + sources",
          {"commit": sha, "commit_message": "add goodbye, with its requirement, source and test",
           "files_changed": git(repo, "diff", "--name-only", "main", "HEAD").split(),
           "check": " ; ".join(s["command"] for s in steps), "exit_code": [s["exit_code"] for s in steps],
           "message": "\n".join(output(s) for s in steps)})
    t.write()
    shutil.rmtree(repo.parent, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
