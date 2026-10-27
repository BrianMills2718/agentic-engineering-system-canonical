"""Build the planning-package review page's data file from the package itself.

Reads the manifest, the open-questions ledger, the domain graph, the open-questions map, the
Mermaid diagrams in docs/planning/SYSTEM_MODEL.md, the "Where the sources disagree" list in
docs/planning/DOMAIN.md and the next plan, and writes proposals/planning-package/review-page/data.js.
The page (index.html next to it) only renders that data, so it cannot say anything the package
files do not. Adapted from ecosystem-ops docs/planning/build_review_page.py (itself from greer).

The page must never carry secrets or personal data: it reads only the planning files above, none
of which holds credentials, spend rows or runtime state.

  python3 docs/planning/build_review_page.py
"""
import json
import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[2]
PAGE = REPO / "proposals" / "planning-package" / "review-page"
# The plan-page site copies only the page folder, so repository links must be absolute (public repository).
BLOB = "https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/"
LINK = re.compile(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)")


def _absolute_links(markdown: str, base: str) -> str:
    """Strip YAML front matter and point relative Markdown link targets at GitHub."""
    if markdown.startswith("---\n"):
        markdown = markdown.split("\n---\n", 1)[1]

    def repl(m: re.Match[str]) -> str:
        target, _, anchor = m.group(1).partition("#")
        path = (pathlib.PurePosixPath(base) / target).as_posix()
        parts: list[str] = []
        for piece in path.split("/"):
            if piece == "..":
                parts.pop()
            elif piece not in ("", "."):
                parts.append(piece)
        return "](" + BLOB + "/".join(parts) + ("#" + anchor if anchor else "") + ")"

    return LINK.sub(repl, markdown)


def _read(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8")


def _section(markdown: str, heading: str) -> str:
    start = markdown.index(heading)
    rest = markdown[start + len(heading):]
    nxt = re.search(r"^## ", rest, flags=re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def main() -> None:
    manifest = json.loads(_read("docs/planning/planning-package.json"))
    parts = manifest["parts"]
    ledger = json.loads(_read(parts["open_questions"]["path"]))
    domain = json.loads(_read(parts["domain_model"]["path"]))
    qmap = json.loads(_read("docs/planning/open-questions.graph.json"))
    architecture = _read(parts["system_model"]["path"])
    diagrams = re.findall(r"```mermaid\n(.*?)```", architecture, flags=re.DOTALL)
    section = _section(_read(parts["domain_model"]["glossary"]), "## Where the sources disagree")
    disagreements = [re.sub(r"\s+", " ", item).strip()
                     for item in re.split(r"^- ", section, flags=re.MULTILINE)[1:]]
    revision = manifest["subject_revision"][:7]
    data = {
        "manifest": manifest,
        "questions": ledger["questions"],
        "domain": domain,
        "question_map": qmap,
        "context_diagrams": diagrams,
        "disagreements": disagreements,
        "next_plan": _absolute_links(_read(parts["plan"]["path"]),
                                     str(pathlib.PurePosixPath(parts["plan"]["path"]).parent)),
        "cold_review": (_absolute_links(_read(parts["cold_review"]["path"]), "docs/planning")
                        if parts["cold_review"].get("path") else "The cold review has not run yet."),
        "evidence_links": {
            "checks.txt (full output of every check)": BLOB + parts["checks"]["path"],
            "cold-review.md (independent review)": BLOB + parts["cold_review"].get("path", "docs/planning/cold-review.md"),
            "planning-package.json (the manifest)": BLOB + "docs/planning/planning-package.json",
            "open-questions.json (the ledger)": BLOB + parts["open_questions"]["path"],
            "SYSTEM_MODEL.md (system model; checked loop in docs/model/ODD.md)": BLOB + parts["system_model"]["path"],
            "DOMAIN.md (domain glossary)": BLOB + parts["domain_model"]["glossary"],
            "next.goal.md (the next plan)": BLOB + parts["plan"]["path"],
        },
        "plan_questions": sorted(set(re.findall(r"\bQ\d+\b", _read(parts["plan"]["path"]))), key=lambda q: int(q[1:])),
        "built_from": revision,
        "checks_commit": (re.search(r"at commit ([0-9a-f]{7,40})", _read("docs/planning/checks.txt")) or [None, "unknown"])[1],
    }
    PAGE.mkdir(parents=True, exist_ok=True)
    (PAGE / "data.js").write_text("window.PAGE_DATA = " + json.dumps(data, ensure_ascii=False, indent=1)
                                  + ";\n", encoding="utf-8")
    print(f"questions={len(ledger['questions'])} concepts={len(domain['nodes'])} "
          f"context_diagrams={len(diagrams)} disagreements={len(disagreements)} built_from={revision}")


if __name__ == "__main__":
    main()
