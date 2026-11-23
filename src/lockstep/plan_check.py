"""`lockstep plan check [--repo PATH] [--acceptance PATH] [--json]`: is the plan itself well formed?

Two checks, ported from Company Planning's package validator (company-planning at b8a53a0) so the plan format is
defined in one place (one-tool design, `proposals/one-planning-tool/DESIGN.md`, slice 5; spec
`openspec/specs/lockstep-plan-check/spec.md`):

  - the acceptance-criteria file, `docs/planning/acceptance-criteria.json` (or `--acceptance PATH`): one entry per
    user outcome with the seven fields, a unique id, the four statuses, and a judgment (`by`, `source`: the judge's
    own recorded words) before a judged status. Ported from `validate_planning_package._check_acceptance`
    (line 348) and `_citation` (line 691).
  - the plan's requirements: when the file carries Brian's words (`asked_by`) and the stored coverage judgment
    (`coverage`), each requirement is sourced (its quote is in his words) and covered (by criteria that exist, or
    by a deferral recorded in his own words), and the judgment is not stale. Ported from
    `coverage_check.check` and `_check` (lines 594 and 605), `quote_in_words` (294), `hashes` (326) and
    `staleness` (351), and the shape rules of `validate_judgment` (191).

The model call that makes a coverage judgment stays in Company Planning (`coverage_check.py`); this reads the
judgment it stored and calls no model. Nothing here reads a path outside the repository, so `lockstep.yaml` needs
no key for it.

Exit 0 the plan is well formed, 1 problems (each named), 2 the file is missing or is not JSON.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:plan_check.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-check/the-acceptance-criteria-file-is-validated, lockstep-plan-check/each-plan-requirement-is-sourced-in-brian-s-words-and-covered, lockstep-plan-check/the-command-is-reached-as-lockstep-plan-check

### Requirement: The acceptance-criteria file is validated

Source: Brian, 2026-10-27: "i am concerned that the success critiria and the demonstration of scucess cirtieria that are jdugemable by me and the represntations of these so tha ti can do this havent alreayd been worked out. i thoguth this was part of company planning ocmpliance" (Company Planning `package-contract.md`, "Acceptance criteria"); its move into Lockstep approved by Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 5).

`lockstep plan check` SHALL read `docs/planning/acceptance-criteria.json` (or the path given with `--acceptance`) and
exit 1, naming each problem, unless: the record type is `acceptance_criteria`; it lists at least one entry; each entry
has a unique `id` and the seven fields `criterion`, `demonstration`, `expected`, `failure_example`, `representation`,
`entrypoint` and `status`; `demonstration` is a list of non-empty steps; `representation` has a `view` and a
`router_record` naming an existing repository file (and an existing `variants` file when given); `entrypoint` is a
URL or `planned`; `status` is `not built`, `built`, `judged pass` or `judged fail`; a status other than `not built`
has a URL, not `planned`; and a judged status carries `judgment` with `by` and `source`, the judge's own recorded
words. It exits 2 when the file is missing or is not JSON.

#### Scenario: A complete acceptance file passes

- **GIVEN** an acceptance file with one entry that has all seven fields, a router record that exists and status `not built`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 0 and prints the count of criteria by status

#### Scenario: An entry missing a field fails

- **GIVEN** an entry without one of the seven fields
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and says `A1: no <field>`

#### Scenario: A malformed entry fails

- **GIVEN** an entry whose demonstration is not a list of steps, whose representation has no view or a router record that does not exist, whose entrypoint is neither a URL nor `planned`, or whose status is not one of the four
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and names that problem for that entry

#### Scenario: A built entry that still says planned fails

- **GIVEN** an entry with status `built` and entrypoint `planned`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and asks for the URL it opens at

#### Scenario: A judged status without the judge's words fails

- **GIVEN** an entry with status `judged pass` and no `judgment` with `by` and `source`
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1; with `judgment: {by, source}` it exits 0

#### Scenario: Duplicate ids and an empty list fail

- **GIVEN** two entries with the same id, or no entries
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and says `duplicate id` or `entries: none listed`

#### Scenario: A missing or unreadable file cannot be checked

- **GIVEN** no acceptance file, or one that is not JSON
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 2 and says what is wrong

### Requirement: Each plan requirement is sourced in Brian's words and covered

Source: Brian, 2026-10-27, the greer request "start the Greer whole-document graph view now: each hearing as one connected graph you can open and ask questions of" that a rewritten outcome dropped (Company Planning `coverage_check.py`, "Why", and `package-contract.md`, "Goal coverage"); Brian, 2026-11-06, "i approve" (three-call judgment); moved into Lockstep with the approval of 2026-11-11 above (slice 5).

When the acceptance file carries Brian's words (`asked_by`) and a stored coverage judgment (`coverage`, written by Company
Planning's `coverage_check.py`), `lockstep plan check` SHALL exit 1 unless: the judgment lists requirements with unique ids
and exactly one mapping each; each requirement's quote is found in the `asked_by` words it cites (exactly, or word for word
with a few of his typos re-spelled); each requirement not about the planning process is covered in full by criteria that
exist, or deferred by a `deferred` entry recorded as Brian's own words with date and source; an outcome requirement that was
not deferred is kept by the `outcome` line; and the judgment is not stale (Brian's words, the outcome, or a criterion or
deferral it relied on changed since it was judged). Criteria edited or added since are reported as pending, not failed. A
file with `asked_by` but no judgment fails; a file with neither skips this check and says so. Lockstep makes no model call.

#### Scenario: A covered requirement passes

- **GIVEN** a judgment whose one requirement quotes Brian's words and is fully covered by an existing criterion
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 0 and prints the count of requirements covered

#### Scenario: A gap in coverage fails

- **GIVEN** a requirement that is uncovered, only partly covered, covered by a criterion that does not exist, dropped from the outcome line, or deferred without a recorded deferral of Brian's
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 and names that requirement and gap

#### Scenario: An invented quote fails and a re-spelled typo passes

- **GIVEN** a requirement whose quote is not in Brian's words, or one that differs from them only by a near spelling of one of his typos
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 for the invented or changed quote and exits 0 for the re-spelled typo

#### Scenario: A deferral in Brian's words counts

- **GIVEN** a requirement mapped to a `deferred` entry with who `Brian`, words, date and source
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 0 and counts it as deferred

#### Scenario: A stale or missing judgment is reported

- **GIVEN** Brian's words changed after the judgment, or `asked_by` without any judgment, or a criterion edited after the judgment
- **WHEN** `lockstep plan check` runs
- **THEN** it exits 1 for the first two and exits 0 with a pending note for the third

#### Scenario: A file without Brian's words skips the requirement check

- **GIVEN** an acceptance file with no `asked_by` and no `coverage`
- **WHEN** `lockstep plan check` runs
- **THEN** it says the requirement check was skipped and the result depends on the acceptance check alone

### Requirement: The command is reached as `lockstep plan check`

Source: Brian, 2026-11-11: "i approve single tool desing re d4" (`proposals/one-planning-tool/DESIGN.md`, slice 5: "`lockstep plan check` validates it").

`lockstep plan check` SHALL accept `--repo PATH` (default the current directory), `--acceptance PATH` (default
`docs/planning/acceptance-criteria.json` under the repository) and `--json`, which prints the result as one object.

#### Scenario: The acceptance path can be overridden

- **GIVEN** an acceptance file at another path
- **WHEN** `lockstep plan check --acceptance that/path.json` runs
- **THEN** that file is the one checked
[[[end]]]
"""

import argparse
import hashlib
import json
import re
import string
import sys
from pathlib import Path
from typing import Any

from lockstep.citation_anchor import anchor_problem

DEFAULT_ACCEPTANCE = "docs/planning/acceptance-criteria.json"
ACCEPTANCE_FIELDS = ("criterion", "demonstration", "expected", "failure_example", "representation",
                     "entrypoint", "status")
ACCEPTANCE_STATUSES = ("not built", "built", "judged pass", "judged fail")
CITATION = re.compile(r"^(?P<path>[\w./-]+\.[\w]+|[\w./-]+/[\w.-]+)(?::(?P<line>\d+)(?:-(?P<end>\d+))?)?$")


class Unreadable(Exception):
    """The file cannot be checked at all (exit 2)."""


def _load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise Unreadable(f"{path}: not found") from exc
    except (OSError, UnicodeDecodeError) as exc:
        raise Unreadable(f"{path}: cannot read ({exc})") from exc
    except json.JSONDecodeError as exc:
        raise Unreadable(f"{path}: not JSON ({exc})") from exc


# --- the acceptance-criteria file -------------------------------------------------------------------------------

def _anchored(repo: Path, ref: str) -> tuple[bool, str | None]:
    """`path#:~:text=...`: the file exists in the repository and the quoted text is in it exactly once."""
    raw, _, fragment = ref.partition("#")
    if not re.fullmatch(r"[\w./-]+", raw or "") or raw.startswith("/") or ".." in Path(raw).parts:
        return True, f"{ref}: malformed anchor: the part before # is not a repository-relative file path"
    path = repo / raw
    if not path.is_file():
        return True, f"{ref}: {raw} does not exist"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return True, f"{ref}: cannot read ({exc})"
    problem = anchor_problem(text, fragment)
    return True, (f"{ref}: {problem}" if problem else None)


def _citation(repo: Path, ref: object) -> tuple[bool, str | None]:
    """(is a file citation, problem). A string that is not `path[:line]` (a URL, a quote) is not a citation.

    Company Planning also accepts absolute and `~` paths; here a citation is repository-relative, so the check
    gives the same answer on every machine.
    """
    if not isinstance(ref, str):
        return False, None
    if "#:~:" in ref and "://" not in ref.partition("#")[0]:
        return _anchored(repo, ref.strip())
    m = CITATION.match(ref.strip())
    if not m or "://" in ref:
        return False, None
    raw = m.group("path")
    if raw.startswith("/") or ".." in Path(raw).parts:
        return False, None
    path = repo / raw
    if not path.is_file():
        return True, f"{ref}: {raw} does not exist"
    if m.group("line"):
        try:
            n = sum(1 for _ in path.open("rb"))
        except OSError as exc:
            return True, f"{ref}: cannot read ({exc})"
        last = int(m.group("end") or m.group("line"))
        if int(m.group("line")) < 1 or last > n:
            return True, f"{ref}: line {last} is past the end of {raw} ({n} lines)"
    return True, None


def acceptance_problems(repo: Path, record: Any) -> tuple[list[str], str]:
    """(problems, summary) for one acceptance-criteria record. One entry per user outcome."""
    problems: list[str] = []
    if not isinstance(record, dict) or record.get("record_type") != "acceptance_criteria":
        return ["record_type is not acceptance_criteria"], ""
    entries = record.get("entries")
    if not isinstance(entries, list) or not entries:
        return ["entries: none listed"], ""
    seen: set[str] = set()
    counts = {s: 0 for s in ACCEPTANCE_STATUSES}
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            problems.append(f"entry {i + 1}: not an object")
            continue
        eid = e.get("id") or f"entry {i + 1}"
        if not e.get("id"):
            problems.append(f"{eid}: no id")
        elif eid in seen:
            problems.append(f"{eid}: duplicate id")
        seen.add(eid)
        for field in ACCEPTANCE_FIELDS:
            if not e.get(field):
                problems.append(f"{eid}: no {field}")
        for field in ("criterion", "expected", "failure_example"):
            if e.get(field) and not isinstance(e[field], str):
                problems.append(f"{eid}: {field} must be text")
        steps = e.get("demonstration")
        if steps and (not isinstance(steps, list) or not all(isinstance(s, str) and s.strip() for s in steps)):
            problems.append(f"{eid}: demonstration must be a list of steps, each a non-empty string")
        rep = e.get("representation")
        if rep and not isinstance(rep, dict):
            problems.append(f"{eid}: representation must be {{view, router_record}}")
        elif rep:
            if not rep.get("view"):
                problems.append(f"{eid}: representation has no view")
            is_cite, problem = _citation(repo, rep.get("router_record"))
            if not is_cite:
                problems.append(f"{eid}: representation.router_record must be the repository path of the "
                                "Representation Router record (recommendation or disposition) that chose the view")
            elif problem:
                problems.append(f"{eid}: representation.router_record {problem}")
            if rep.get("variants") is not None:
                is_cite, problem = _citation(repo, rep.get("variants"))
                if not is_cite or problem:
                    problems.append(f"{eid}: representation.variants must name an existing sketch-set file"
                                    + (f" ({problem})" if problem else ""))
        entry = e.get("entrypoint")
        if entry and entry != "planned" and not (isinstance(entry, str) and entry.startswith(("https://", "http://"))):
            problems.append(f"{eid}: entrypoint must be a URL or planned")
        status = e.get("status")
        if status and status not in ACCEPTANCE_STATUSES:
            problems.append(f"{eid}: status must be one of {', '.join(ACCEPTANCE_STATUSES)}")
            continue
        if status:
            counts[status] += 1
        if status and status != "not built" and entry == "planned":
            problems.append(f"{eid}: status {status} but entrypoint is planned (give the URL it opens at)")
        if status in ("judged pass", "judged fail"):
            judgment = e.get("judgment")
            if not isinstance(judgment, dict) or not judgment.get("by") or not judgment.get("source"):
                problems.append(f"{eid}: {status} needs judgment {{by, source}}: who judged it on the "
                                "working interface and where their verdict is recorded")
    return problems, f"{len(entries)} criteria: " + ", ".join(f"{n} {s}" for s, n in counts.items())


# --- the plan's requirements: sourced in Brian's words, covered by criteria or his deferral ----------------------

def _norm(text: object) -> str:
    return " ".join(str(text).split()).casefold()


# A quote must be Brian's words. He types fast and his recorded words keep his typos; a judging model sometimes
# re-spells one when it copies it (lockstep, 2026-11-07: his "docuemtnation" quoted as "docuemntation"). So a quote
# passes when it is in his words exactly, or matches a run of them word for word, the same number of words, where
# each differing word is a near spelling of his and few differ (thresholds from Company Planning's coverage_check):
# a word under 5 letters must match exactly, the first letter must match, at most 1 edit (2 from 8 letters), and at
# most one differing word per five words of the quote.
_EDGE_PUNCTUATION = string.punctuation + "“”‘’…—–"
_SHORT = 5
_LONG = 8
_SHARE = 5


def _words(text: str) -> list[str]:
    return [w for w in (t.strip(_EDGE_PUNCTUATION) for t in _norm(text).split()) if w]


def _edits(a: str, b: str) -> int:
    """Damerau-Levenshtein distance (optimal string alignment)."""
    before, prev = [0] * (len(b) + 1), list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                cur[j] = min(cur[j], before[j - 2] + 1)
        before, prev = prev, cur
    return prev[-1]


def _respelled(said: str, quoted: str) -> bool:
    longer = max(len(said), len(quoted))
    if longer < _SHORT or min(len(said), len(quoted)) < _SHORT - 1 or said[0] != quoted[0]:
        return False
    return _edits(said, quoted) <= (1 if longer < _LONG else 2)


def quote_in_words(quote: str, words: str) -> bool:
    """Whether `quote` is Brian's `words`: exactly, or word for word with a few of his typos re-spelled."""
    if _norm(quote) in _norm(words):
        return True
    q, w = _words(quote), _words(words)
    if not q:
        return False
    allowed = max(1, len(q) // _SHARE)
    for start in range(len(w) - len(q) + 1):
        differing = [(s, t) for s, t in zip(w[start:start + len(q)], q) if s != t]
        if len(differing) <= allowed and all(_respelled(s, t) for s, t in differing):
            return True
    return False


def _sha(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _asked_by(record: dict) -> list[dict]:
    quotes = record.get("asked_by")
    if not isinstance(quotes, list):
        return []
    return [{k: q.get(k, "") for k in ("who", "date", "words", "source")} for q in quotes if isinstance(q, dict)]


def _criteria(record: dict) -> list[dict]:
    return [{"id": e.get("id", ""), "title": e.get("title", ""), "criterion": e.get("criterion", ""),
             "demonstration": e.get("demonstration") or [], "expected": e.get("expected", "")}
            for e in record.get("entries") or [] if isinstance(e, dict)]


def hashes(record: dict) -> dict:
    """What a judgment depends on (the keys `coverage_check.py` stores): Brian's words, the outcome and the criteria."""
    return {"asked_by_sha256": _sha([{k: q[k] for k in ("who", "date", "words")} for q in _asked_by(record)]),
            "criteria_sha256": _sha({"outcome": record.get("outcome", ""), "criteria": _criteria(record),
                                     "deferred": record.get("deferred") or []}),
            "outcome_sha256": _sha(record.get("outcome", "")),
            "criteria_judged": {c["id"]: _sha(c) for c in _criteria(record)},
            "deferrals_judged": [_sha(d) for d in record.get("deferred") or []]}


def staleness(record: dict, coverage: dict) -> tuple[str, str]:
    """("current" | "rejudge" | "pending", why). Only "pending" may wait for the next re-judgment."""
    current = hashes(record)
    if all(coverage.get(k) == current[k] for k in ("asked_by_sha256", "criteria_sha256")):
        return "current", ""
    stale = "the coverage record is stale: "
    if coverage.get("asked_by_sha256") != current["asked_by_sha256"]:
        return "rejudge", stale + "Brian's asked_by words changed since it was judged"
    if "outcome_sha256" in coverage and coverage["outcome_sha256"] != current["outcome_sha256"]:
        return "rejudge", stale + "the outcome line changed since it was judged"
    judged = coverage.get("criteria_judged")
    maps = [m for m in coverage.get("mappings") or [] if isinstance(m, dict)]
    named = {c for m in maps for c in m.get("covered_by") or []}
    removed = sorted(((set(judged) if isinstance(judged, dict) else set()) | named) - set(current["criteria_judged"]))
    if removed:
        return "rejudge", stale + f"criteria removed since it was judged: {', '.join(removed)}"
    judged_deferrals = coverage.get("deferrals_judged")
    gone = [d for d in judged_deferrals if d not in current["deferrals_judged"]] \
        if isinstance(judged_deferrals, list) else []
    highest = max((m.get("deferral") or 0 for m in maps), default=0)
    if gone or highest > len(current["deferrals_judged"]):
        return "rejudge", stale + "a deferral it relied on was removed or reworded"
    if isinstance(judged, dict):
        edited = sorted(i for i, sha in current["criteria_judged"].items() if judged.get(i) != sha)
        what = f"criteria edited or added: {', '.join(edited)}" if edited else "a deferral was added"
    else:
        what = "criteria or deferrals edited or added"
    return "pending", f"{what}; re-judge with Company Planning's coverage_check.py"


def _shape_problems(coverage: dict, asked_by: list[dict]) -> list[str]:
    """The shape rules a stored judgment must keep before its gaps can be read (`validate_judgment`)."""
    reqs = coverage.get("requirements")
    maps = coverage.get("mappings")
    if not isinstance(reqs, list) or not isinstance(maps, list):
        return ["coverage: requirements and mappings must both be lists"]
    problems = [f"coverage: requirement {i + 1} is not an object" for i, r in enumerate(reqs) if not isinstance(r, dict)]
    problems += [f"coverage: mapping {i + 1} is not an object" for i, m in enumerate(maps) if not isinstance(m, dict)]
    if problems:
        return problems
    if not reqs:
        return ["the coverage record lists no requirements"]
    ids = [str(r.get("id", "")) for r in reqs]
    if any(not i.strip() for i in ids) or len(set(ids)) != len(ids) \
            or any(not str(r.get("requirement", "")).strip() for r in reqs):
        problems.append("coverage: requirements must be named and have nonempty, unique ids")
    mapped = [m.get("requirement_id") for m in maps]
    if len(mapped) != len(ids) or len(set(mapped)) != len(mapped) or set(mapped) != set(ids):
        problems.append("coverage: exactly one mapping is required for every requirement, with no extra, "
                        "duplicate or missing mappings")
    return problems


def requirement_problems(record: dict) -> tuple[list[str], dict]:
    """(problems, info) for the plan's requirements. info: checked, summary, pending."""
    info: dict[str, Any] = {"checked": False, "summary": "", "pending": ""}
    asked_by = _asked_by(record)
    coverage = record.get("coverage")
    if not asked_by and coverage is None:
        info["summary"] = "skipped (no asked_by: record Brian's own words to check that the criteria keep them)"
        return [], info
    if not asked_by:
        return ["coverage: the file has a coverage record but no asked_by words for it to quote"], info
    if coverage is None:
        return ["asked_by is recorded but there is no stored coverage judgment; make one with Company Planning's "
                "coverage_check.py"], info
    if not isinstance(coverage, dict):
        return ["coverage must be an object (the stored judgment)"], info
    info["checked"] = True
    problems = _shape_problems(coverage, asked_by)
    if problems:
        return problems, info
    state, why = staleness(record, coverage)
    if state == "rejudge":
        problems.append(why)
    elif state == "pending":
        info["pending"] = why
    ids = {e["id"] for e in _criteria(record)}
    deferred = record.get("deferred") or []
    maps = {m["requirement_id"]: m for m in coverage["mappings"]}
    covered, deferred_n, process = [], [], []
    for r in coverage["requirements"]:
        rid = r.get("id", "?")
        label = f'{rid} "{r.get("requirement", "?")}"'
        idx = r.get("asked_by_index")
        if not isinstance(idx, int) or isinstance(idx, bool) or not 1 <= idx <= len(asked_by):
            problems.append(f"{label}: asked_by_index {idx!r} is not one of the {len(asked_by)} quotes")
        elif not str(r.get("quote", "")).strip() or not quote_in_words(r.get("quote", ""), asked_by[idx - 1]["words"]):
            problems.append(f"{label}: its quote is not in Brian's words (quote {idx}): {r.get('quote')!r}")
        m = maps[rid]
        if r.get("kind") == "process":
            process.append(rid)
        else:
            by = [c for c in m.get("covered_by") or []]
            unknown = [c for c in by if c not in ids]
            if unknown:
                problems.append(f"{label}: covered_by names criteria that do not exist: {', '.join(unknown)}")
            good = [c for c in by if c in ids]
            d = m.get("deferral") or 0
            extent = m.get("extent") or ("full" if good else "none")
            if good and extent == "full":
                covered.append(rid)
            elif good and not d:
                problems.append(f"{label}: only partly covered by {', '.join(good)}; no criterion asks for "
                                f"{m.get('missing') or 'the rest'}")
            elif d:
                entry = deferred[d - 1] if isinstance(d, int) and 1 <= d <= len(deferred) else None
                if not isinstance(entry, dict) or entry.get("who") != "Brian" or not all(
                        entry.get(k) for k in ("words", "date", "source")):
                    problems.append(f"{label}: deferral {d} is not a recorded deferral in Brian's own words "
                                    "(deferred[] needs who: Brian, words, date, source)")
                else:
                    deferred_n.append(rid)
            else:
                problems.append(f"{label}: uncovered: no criterion asks for it and Brian approved no deferral "
                                f"({m.get('coverage_reason', '')})")
        # A requirement Brian deferred in his own words is rightly absent from the line saying what is built now.
        if r.get("kind") == "outcome" and m.get("in_outcome") is False and rid not in deferred_n:
            problems.append(f"{label}: the outcome line drops it ({m.get('outcome_reason', '')})")
    if coverage.get("needs_review"):
        problems.append("needs_review: two independent judgments disagreed; re-judge with Company Planning's "
                        "coverage_check.py --force")
    info["summary"] = (f"{len(coverage['requirements'])} requirements: {len(covered)} covered, {len(deferred_n)} "
                       f"deferred, {len(process)} about the planning process")
    return problems, info


# --- the command -------------------------------------------------------------------------------------------------

def plan_cli(argv: list[str]) -> int:
    """`lockstep plan <command>`: today the only command is `check`."""
    if argv and argv[0] == "units":
        from lockstep.work_units import units_cli
        return units_cli(argv[1:])
    if not argv or argv[0] != "check":
        print("usage: lockstep plan check [--repo PATH] [--acceptance PATH] [--json] | lockstep plan units [--repo PATH] [--json]",
              file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(prog="lockstep plan check", description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo", type=Path, default=Path("."), help="the repository (default: the current directory)")
    parser.add_argument("--acceptance", type=Path, default=None,
                        help=f"the acceptance-criteria file (default: {DEFAULT_ACCEPTANCE} under --repo)")
    parser.add_argument("--json", action="store_true", help="print the result as one JSON object")
    args = parser.parse_args(argv[1:])
    repo: Path = args.repo
    path = repo / (args.acceptance or DEFAULT_ACCEPTANCE)
    try:
        record = _load(path)
    except Unreadable as exc:
        print(f"cannot check: {exc}", file=sys.stderr)
        return 2
    a_problems, a_summary = acceptance_problems(repo, record)
    r_problems, info = requirement_problems(record) if isinstance(record, dict) else ([], {
        "checked": False, "summary": "skipped", "pending": ""})
    problems = a_problems + r_problems
    units_file = repo / "docs/planning/work-units.json"
    if units_file.is_file():  # the work-unit DAG is checked here once a repository has one
        from lockstep.work_units import analyse
        try:
            problems += [f"work units: {p}" for p in analyse(_load(units_file))["problems"]]
        except Unreadable as exc:
            problems.append(f"work units: {exc}")
    if args.json:
        print(json.dumps({"ok": not problems, "acceptance": {"path": str(path), "summary": a_summary},
                          "requirements": info, "problems": problems}, indent=2))
    else:
        print(f"{'ok  ' if not a_problems else 'FAIL'} acceptance: {a_summary or str(path)}")
        print(f"{'ok  ' if not r_problems else 'FAIL'} requirements: {info['summary'] or 'not judged'}")
        if info["pending"]:
            print(f"pending: {info['pending']}")
        for p in problems:
            print(f"  {p}")
        print(f"OUTCOME {'ok' if not problems else 'fail'}: {len(problems)} problems")
    return 0 if not problems else 1
