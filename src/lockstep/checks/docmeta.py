"""Docmeta check: the OKF front matter of every page under `wiki/` is complete, fresh and findable.

Fields (extra keys allowed, as OKF permits): `type` (required), `title`, `description`, `status`
(current | history | superseded; absent means current), `owner`, `successor` (required when
superseded), `last_checked` (YYYY-MM-DD, within 60 days on a current page), `source_of_truth_for`
(list of topics; one page per topic). Every current page sits at most two links from `wiki/index.md`.
`wiki/index.md` and `wiki/log.md` carry no front matter (OKF conventions) and are exempt from the
field rules. Federation homes (plan D10's second half) are not checked here.

Implements: lockstep-checks/docmeta-every-wiki-page-declares-its-type, lockstep-checks/docmeta-current-pages-are-checked-within-60-days,
    lockstep-checks/docmeta-superseded-pages-name-a-successor, lockstep-checks/docmeta-one-page-owns-each-topic,
    lockstep-checks/docmeta-every-current-page-is-within-two-links-of-the-index,
    lockstep-checks/docmeta-field-values-have-their-allowed-form, lockstep-checks/docmeta-count-line-and-exit-status

Requirement text (generated):
    lockstep-checks/docmeta-every-wiki-page-declares-its-type: The docmeta check SHALL report every
        Markdown page under `wiki/` whose OKF front matter is missing, unparseable or has no
        non-empty `type`. `wiki/index.md` and `wiki/log.md` are exempt, because the OKF conventions
        give the catalog and the chronicle no front matter.
    lockstep-checks/docmeta-current-pages-are-checked-within-60-days: The docmeta check SHALL report
        a page whose `status` is `current` (or absent, which means current) when its `last_checked`
        date (YYYY-MM-DD) is more than 60 days old or missing.
    lockstep-checks/docmeta-superseded-pages-name-a-successor: The docmeta check SHALL report a page
        whose `status` is `superseded` and which has no `successor`.
    lockstep-checks/docmeta-one-page-owns-each-topic: The docmeta check SHALL report every topic
        listed in the `source_of_truth_for` of two or more pages, naming the topic and each page.
    lockstep-checks/docmeta-every-current-page-is-within-two-links-of-the-index: The docmeta check
        SHALL report every current page under `wiki/` that cannot be reached from `wiki/index.md` by
        following at most two relative Markdown links.
    lockstep-checks/docmeta-field-values-have-their-allowed-form: The docmeta check SHALL report a
        `status` other than `current`, `history` or `superseded`, a `last_checked` that is not a
        YYYY-MM-DD date, and a `source_of_truth_for` that is not a list. Other keys are allowed, as
        OKF permits.
    lockstep-checks/docmeta-count-line-and-exit-status: The docmeta check SHALL print one count line
        `docmeta: pages=N missing_type=N stale=N superseded_without_successor=N
        topics_with_two_owners=N beyond_two_links=N invalid_field=N` then one line per finding (path
        and reason), and exit 0 when there is no finding and 1 otherwise. A repository with no
        `wiki/` folder prints the count line with `pages=0` and exits 0.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
from urllib.parse import unquote

import yaml

KINDS = ("missing_type", "stale", "superseded_without_successor", "topics_with_two_owners",
         "beyond_two_links", "invalid_field")
STATUSES = ("current", "history", "superseded")
MAX_AGE_DAYS = 60
MAX_LINKS = 2
EXEMPT = ("index.md", "log.md")
# Same link pattern as workspace/scripts/doc_reachability.py: [text](path) and [label]: path.
_LINK = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)|^\s*\[[^\]]+\]:\s*<?(\S+?)>?\s*$", re.M)
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class Finding:
    """One problem: its kind (one of KINDS), the page or pages it concerns, and why."""

    kind: str
    where: str
    reason: str


@dataclass
class Result:
    """The pages checked and the findings, in the order they were found."""

    pages: int
    findings: list[Finding]

    def count_line(self) -> str:
        """Return the one-line summary: page count, then a count per finding kind.

        Returns:
            `docmeta: pages=N missing_type=N ...`.
        """
        counts = " ".join(f"{k}={sum(f.kind == k for f in self.findings)}" for k in KINDS)
        return f"docmeta: pages={self.pages} {counts}"


def front_matter(text: str) -> dict | None:
    """Parse a page's leading YAML front matter.

    Args:
        text: The page's full text.

    Returns:
        The front matter as a dict; None when there is none or it does not parse to a mapping.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = next((i for i, ln in enumerate(lines[1:], 1) if ln.strip() in ("---", "...")), None)
    if end is None:
        return None
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def links(page: Path, wiki: Path) -> set[Path]:
    """Return the files a page links to; `/x.md` is relative to the wiki root (OKF bundle links).

    Args:
        page: The Markdown page.
        wiki: The wiki folder.

    Returns:
        Resolved paths of linked files (a folder link becomes its index.md or README.md).
    """
    found = set()
    for a, b in _LINK.findall(page.read_text(encoding="utf-8", errors="replace")):
        target = unquote((a or b).split("#", 1)[0].split("?", 1)[0])
        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
            continue  # same-page anchor, or an external URL / mailto
        base = wiki if target.startswith("/") else page.parent
        path = (base / target.lstrip("/")).resolve()
        if path.is_dir():
            path = next((path / n for n in ("index.md", "README.md") if (path / n).is_file()), path)
        found.add(path)
    return found


def _depths(index: Path, pages: set[Path], wiki: Path) -> dict[Path, int]:
    """Return each page's link distance from the index, for pages within MAX_LINKS links."""
    depth = {index: 0}
    frontier = [index]
    for d in range(1, MAX_LINKS + 1):
        nxt = []
        for p in frontier:
            for t in links(p, wiki):
                if t in pages and t not in depth:
                    depth[t] = d
                    nxt.append(t)
        frontier = nxt
    return depth


def _as_date(value: object) -> date | None:
    """Return a YYYY-MM-DD value as a date, else None."""
    if isinstance(value, date):
        return value
    if isinstance(value, str) and _DATE.match(value.strip()):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def _page_findings(rel: str, meta: dict | None, today: date) -> tuple[list[Finding], str]:
    """Check one page's fields; return its findings and its status (absent or invalid means current)."""
    out: list[Finding] = []
    if meta is None:
        return [Finding("missing_type", rel, "no parseable front matter")], "current"
    if not str(meta.get("type") or "").strip():
        out.append(Finding("missing_type", rel, "front matter has no type"))
    status = meta.get("status", "current")
    if status not in STATUSES:
        out.append(Finding("invalid_field", rel, f"status {status!r} is not one of {', '.join(STATUSES)}"))
        status = "current"
    checked = meta.get("last_checked")
    when = _as_date(checked)
    if checked is not None and when is None:
        out.append(Finding("invalid_field", rel, f"last_checked {checked!r} is not a YYYY-MM-DD date"))
    if "source_of_truth_for" in meta and not isinstance(meta["source_of_truth_for"], list):
        out.append(Finding("invalid_field", rel, "source_of_truth_for is not a list"))
    if status == "current":
        if when is None:
            out.append(Finding("stale", rel, "current page has no valid last_checked"))
        elif (today - when).days > MAX_AGE_DAYS:
            out.append(Finding("stale", rel, f"last_checked {when.isoformat()} is {(today - when).days} days old (limit {MAX_AGE_DAYS})"))
    if status == "superseded" and not str(meta.get("successor") or "").strip():
        out.append(Finding("superseded_without_successor", rel, "superseded page names no successor"))
    return out, status


def check(root: Path, today: date | None = None) -> Result:
    """Check every Markdown page under `root/wiki/`.

    Args:
        root: Repository (or any folder) holding `wiki/`.
        today: The date staleness is measured from; defaults to today.

    Returns:
        The page count (exempt index and log excluded) and every finding.
    """
    today = today or date.today()
    wiki = (root / "wiki").resolve()
    if not wiki.is_dir():
        return Result(0, [])
    all_md = {p.resolve() for p in wiki.rglob("*.md") if p.is_file()}
    exempt = {(wiki / n).resolve() for n in EXEMPT}
    findings: list[Finding] = []
    owners: dict[str, list[str]] = defaultdict(list)
    current: list[Path] = []
    for path in sorted(all_md - exempt):
        rel = str(path.relative_to(root.resolve())) if path.is_relative_to(root.resolve()) else str(path)
        meta = front_matter(path.read_text(encoding="utf-8", errors="replace"))
        found, status = _page_findings(rel, meta, today)
        findings.extend(found)
        if status == "current":
            current.append(path)
        topics = (meta or {}).get("source_of_truth_for")
        if isinstance(topics, list):
            for topic in dict.fromkeys(str(t) for t in topics):
                owners[topic].append(rel)
    for topic, pages in sorted(owners.items()):
        if len(pages) > 1:
            findings.append(Finding("topics_with_two_owners", ", ".join(pages),
                                    f"topic {topic!r} is claimed by {len(pages)} pages"))
    index = (wiki / "index.md").resolve()
    depth = _depths(index, all_md, wiki) if index in all_md else {}
    for path in current:
        if path not in depth:
            rel = str(path.relative_to(root.resolve()))
            why = "wiki/index.md is missing" if index not in all_md else f"more than {MAX_LINKS} links from wiki/index.md"
            findings.append(Finding("beyond_two_links", rel, why))
    return Result(len(all_md - exempt), findings)
