"""Feedback records (contract feedback-report.v1): observations, claims and actions with links.

Plan: proposals/aes-learning-loop/PLAN.md ("Record model", "Report format"). An agent's closeout
Feedback field holds one record per line:

  - obs: <one sentence> [<link>] [<link>]  expected: <link or sentence>
  - claim (inferred, high, supported): <one sentence>  ← <obs N or link>
  - action (Investigate, done): <one sentence> → <result link>
  - action (Prevent, proposed): <one sentence>

This module parses those fixed markers with code (structure only; prose meaning is left to the
light model in collect_feedback.py, for lines without markers). Links are identifiers, not prose:
URLs, markdown links, issue/PR references, commits, and file paths with an optional line.
A record with no link is kept but marked `unprovenanced`; it can never support a licence.
Pure standard library plus Pydantic, so the tests run without llm_client.
"""
from __future__ import annotations

import hashlib
import re
from typing import Literal

from pydantic import BaseModel, Field

CONTRACT = "feedback-report.v1"
Basis = Literal["seen", "inferred", "guessed"]
Confidence = Literal["low", "medium", "high"]
Intent = Literal["Investigate", "Mitigate", "Repair", "Detect", "Prevent"]
# The vision register's evidence words (vision wiki hypotheses-and-evidence-register).
EVIDENCE_WORDS = ("implemented", "demonstrated", "supported", "current judgment", "forecast",
                  "hypothesis", "principle", "objective")


class Link(BaseModel):
    kind: Literal["url", "issue", "commit", "path", "entry"]  # entry: a legacy learnings-register id
    ref: str


class Provenance(BaseModel):
    """Who filed it, when, and from where (the nanopublication-style pubinfo)."""
    client: str = ""            # claude | codex | manual
    session_id: str = ""
    turn_offset: int = 0        # byte offset of the closeout turn in the transcript
    ts: str = ""
    cwd: str = ""
    line: str = ""              # the source line, verbatim


class Record(BaseModel):
    contract: str = CONTRACT
    id: str = ""
    kind: Literal["observation", "claim", "action"]
    text: str
    links: list[Link] = Field(default_factory=list)
    unprovenanced: bool = False
    parsed_by: Literal["markers", "light_model"] = "markers"
    # observation
    expected: str = ""
    subject_kind: Literal["work", "control", ""] = ""
    # claim
    basis: Basis | None = None
    confidence: Confidence | None = None
    evidence_word: str = ""
    supports: list[str] = Field(default_factory=list)   # record ids or link refs this claim rests on
    # action
    intent: Intent | None = None
    status: Literal["proposed", "done", ""] = ""
    result: list[Link] = Field(default_factory=list)
    provenance: Provenance = Field(default_factory=Provenance)


_MD_LINK = re.compile(r"\[[^\]]*\]\((\S+?)\)")
_URL = re.compile(r"https?://[^\s)\]>`'\"]+")
_ISSUE = re.compile(r"(?<![\w/])((?:[\w.-]+/)?[\w.-]+)?#(\d{1,6})\b")
_COMMIT = re.compile(r"`([0-9a-f]{7,40})`")
_PATH = re.compile(r"(?<![\w/.:])((?:~|\.{0,2})?/?(?:[\w.@-]+/)+[\w.@-]+\.[A-Za-z0-9]{1,8}(?::\d+(?:-\d+)?)?)")
_ENTRY = re.compile(r"\b(lrn-\d{8}T\d{6,12}Z-[0-9a-f]{6,12})\b")
_GH_ISSUE_URL = re.compile(r"github\.com/([\w.-]+/[\w.-]+)/(?:issues|pull)/(\d+)")
# a bare file name with a line number (Makefile:96, README.md:12); a letter first, so times are not read
_FILE_LINE = re.compile(r"(?<![\w/.:~-])([A-Za-z][\w.-]*:\d+(?:-\d+)?)\b")


def find_links(text: str) -> list[Link]:
    """Every resolvable reference in `text`, in order, without duplicates."""
    out: list[Link] = []
    seen: set[str] = set()

    def add(kind, ref):
        ref = ref.rstrip(".,;:")
        if ref and ref not in seen:
            seen.add(ref)
            out.append(Link(kind=kind, ref=ref))

    urls = [m.group(1) for m in _MD_LINK.finditer(text)] + _URL.findall(text)
    for u in urls:
        if u.startswith("http"):
            add("url", u)
        elif "/" in u or "." in u:
            add("path", u)
    scrub = _URL.sub(" ", _MD_LINK.sub(" ", text))  # markdown links first, so their text is not read twice
    for m in _ISSUE.finditer(scrub):
        add("issue", f"{m.group(1)}#{m.group(2)}" if m.group(1) else f"#{m.group(2)}")
    for m in _ENTRY.finditer(scrub):
        add("entry", m.group(1))
    for m in _COMMIT.finditer(scrub):
        add("commit", m.group(1))
    for m in _PATH.finditer(scrub):
        add("path", m.group(1))
    for m in _FILE_LINE.finditer(_PATH.sub(" ", scrub)):
        add("path", m.group(1))
    return out


def normalize_links(links: list[Link], default_repo: str = "") -> list[Link]:
    """Qualify a bare `#N` with the session's repository, and drop an issue reference that a GitHub URL in
    the same list already names (`#300` beside `.../issues/300`)."""
    urls = {(m.group(1).lower(), m.group(2)) for lk in links if lk.kind == "url"
            for m in [_GH_ISSUE_URL.search(lk.ref)] if m}
    url_nums = {n for _, n in urls}
    out: list[Link] = []
    for lk in links:
        if lk.kind == "issue":
            repo, _, num = lk.ref.partition("#")
            if (not repo and num in url_nums) or (repo.lower(), num) in urls:
                continue
            lk = Link(kind="issue", ref=f"{repo or default_repo}#{num}" if (repo or default_repo) else f"#{num}")
        if all(lk.ref != o.ref for o in out):
            out.append(lk)
    return out


_LINE = re.compile(r"^\s*[-*]?\s*(obs|observation|claim|action)\b\s*(?:\(([^)]*)\))?\s*:\s*(.+)$", re.I)
_SUPPORT = re.compile(r"\s*(?:←|<-)\s*(.+)$")
_RESULT = re.compile(r"\s*(?:→|->)\s*(.+)$")
_EXPECTED = re.compile(r"\s+expected:\s*(.+)$", re.I)
_OBS_REF = re.compile(r"\bobs(?:ervation)?\s*(\d+)\b", re.I)
_INTENTS = {i.lower(): i for i in ("Investigate", "Mitigate", "Repair", "Detect", "Prevent")}


def record_id(prov: Provenance, kind: str, text: str) -> str:
    h = hashlib.sha256(f"{prov.client}|{prov.session_id}|{prov.turn_offset}|{kind}|{text}".encode())
    return "rec-" + h.hexdigest()[:12]


def _qualifiers(raw: str | None) -> list[str]:
    return [q.strip().lower() for q in (raw or "").split(",") if q.strip()]


def _strip_links(text: str) -> str:
    """The sentence without its bracketed link references (kept in `links`); markdown link text stays."""
    text = _MD_LINK.sub(lambda m: m.group(0).split("](")[0][1:], text)
    for lk in find_links(text):
        for form in (f"[{lk.ref}]", f"[`{lk.ref}`]"):
            text = text.replace(form, " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_line(line: str, prov: Provenance, observations: list[Record], default_repo: str = "") -> Record | None:
    """One marked Feedback line -> a Record, or None when the line carries no marker."""
    m = _LINE.match(line)
    if not m:
        return None
    marker, quals, body = m.group(1).lower(), _qualifiers(m.group(2)), m.group(3).strip()
    p = prov.model_copy(update={"line": line.strip()})
    if marker in ("obs", "observation"):
        expected = ""
        e = _EXPECTED.search(body)
        if e:
            expected, body = e.group(1).strip(), body[: e.start()]
        links = find_links(body)
        rec = Record(kind="observation", text=_strip_links(body), links=links, expected=expected,
                     subject_kind="control" if "control" in quals else "work", provenance=p)
    elif marker == "claim":
        supports_raw = ""
        s = _SUPPORT.search(body)
        if s:
            supports_raw, body = s.group(1).strip(), body[: s.start()]
        supports = []
        for ref in _OBS_REF.findall(supports_raw):
            i = int(ref) - 1
            if 0 <= i < len(observations):
                supports.append(observations[i].id)
        links = find_links(body) + [lk for lk in find_links(supports_raw)]
        supports += [lk.ref for lk in find_links(supports_raw)]
        basis = next((q for q in quals if q in ("seen", "inferred", "guessed")), None)
        conf = next((q for q in quals if q in ("low", "medium", "high")), None)
        word = next((q for q in quals if q in EVIDENCE_WORDS), "")
        rec = Record(kind="claim", text=_strip_links(body), links=links, basis=basis, confidence=conf,
                     evidence_word=word, supports=supports, provenance=p)
        # a claim resting on a linked observation of the same report is provenanced through it
        if not rec.links and any(o.id in supports and o.links for o in observations):
            rec.links = [lk for o in observations if o.id in supports for lk in o.links]
    else:
        result_raw = ""
        r = _RESULT.search(body)
        if r:
            result_raw, body = r.group(1).strip(), body[: r.start()]
        intent = next((_INTENTS[q] for q in quals if q in _INTENTS), None)
        status = next((q for q in quals if q in ("proposed", "done")), "")
        rec = Record(kind="action", text=_strip_links(body), links=find_links(body), intent=intent,
                     status=status, result=find_links(result_raw), provenance=p)
    rec.links = normalize_links(rec.links, default_repo)
    rec.result = normalize_links(rec.result, default_repo)
    rec.unprovenanced = not (rec.links or rec.result)
    rec.id = record_id(prov, rec.kind, rec.text)
    return rec


def parse_feedback(value: str, prov: Provenance, default_repo: str = "") -> tuple[list[Record], list[str]]:
    """A Feedback field -> (records from marked lines, unmarked non-empty lines left for the light model)."""
    records: list[Record] = []
    rest: list[str] = []
    for line in value.splitlines():
        if not line.strip():
            continue
        rec = parse_line(line, prov, [r for r in records if r.kind == "observation"], default_repo)
        if rec is None:
            rest.append(line)
        else:
            records.append(rec)
    return records, rest
