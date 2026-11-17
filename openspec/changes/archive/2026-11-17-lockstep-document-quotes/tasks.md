## 1. Tests first (each marked `@pytest.mark.req("<capability>/<scenario-slug>")`)

- [x] 1.1 `tests/lockstep/checks/test_lockstep_check_quotes.py`: one test per scenario of "Trace: A marked quote matches its requirement" (six), on throwaway repositories built with `lockstep_checks_support`
- [x] 1.2 `tests/lockstep/checks/test_lockstep_check_changed.py`: the scenario "Changed: A document quoting a changed requirement is listed as stale", text and `--json` output
- [x] 1.3 Run them; every new test fails for the right reason before any source changes

## 2. Source

- [x] 2.1 `checks/quotes.py`: list tracked Markdown outside `openspec/` (`git ls-files`; outside a git repository, every Markdown file outside `openspec/` and dot folders); find each start marker and its end marker; compare the passage with the requirement's and its scenarios' text, whitespace runs as one space
- [x] 2.2 `checks/trace.py`: add `stale-quote`, `unknown` and `unclosed-quote` findings, each with `<path>:<line>`
- [x] 2.3 `checks/changed.py`: a `documents` list per listed requirement (text block and JSON)
- [x] 2.4 `Implements:` lines in the docstrings; `lockstep check project` to write the requirement text

## 3. Finish

- [x] 3.1 `make check` exits 0
- [x] 3.2 `openspec archive lockstep-document-quotes --yes`; `openspec validate --all --strict --no-interactive`
- [x] 3.3 `wiki/lockstep.md` and `.project-brain/now.md` say how to mark a quote and that unmarked copies are not checked
