"""Check every page of a generated wiki is within two links of its front page, each link with a summary (behavior 6.2).

The wiki here is the one Lockstep generates from the plan, the evidence standing and the
docstrings (`lockstep.wiki.pages`, behavior 6.1): normative pages per component, and the code page.
Walking it from the front page, this reports a page more than two links away (with the shortest
chain of links found to it) or never reached (no chain exists), a link to a page the wiki does not have, and a link with no summary beside it (other text on the
link's own line or table row). A hand-written wiki is held to the same rule by the workspace's
`md_file_cap.py`. `python -m lockstep.wiki_reach --package pcw` is part of `make check`.

[[[cog import lockstep.cogtext as c; c.docstring("ART-WIKI-REACH", indent=0)]]]
Plan (generated from .aes/target.yaml; edit the plan, not this text):

Part of REQ-6: The wiki gets an agent to the right document or code within
  two links: from the wiki's front page, an agent reaches the normative
  document or the code that answers its question within two links, and each
  link comes with a summary of what it leads to.
BEH-6.2: Every normative document and code page is reached from the wiki's
  front page within two links, and each link carries a summary; a page that
  is too far away is reported with the shortest chain of links found to it
  from the front page, or with a statement that no chain exists.
SC-6.2: A built wiki is walked from its front page: every normative document
  and code page is within two links, and every link has a summary; a page
  that is too far away is reported with the shortest chain of links to it,
  or with a statement that no chain exists.
  Disproved if: A normative document or code page needs three or more links,
  or a link has no summary, or a report of a page that is too far away
  leaves out the shortest chain of links to it (or leaves out that none
  exists).
Proven by: VS-6.2-a (tests/test_wiki_reach.py)
Declares (typed signatures, from the plan):
  reach_problems(pages: dict[str, str], front: str = 'index.md') -> list[str]
  main(argv: list[str] | None = None) -> int
[[[end]]] (sum: hE+kCOD6/c)
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
from pathlib import Path

from lockstep.aes_bridge import find_root

LINK = re.compile(r"\[([^\]\n]*)\]\(([^)\s]+)\)")  # Markdown link syntax, not prose
NOT_SUMMARY = " \t-*|:;,.()—–0123456789"


def _links(pages: dict[str, str]) -> list[tuple[str, str, bool]]:
    """(page, linked page, has a summary) for every link from one wiki page to another."""
    out = []
    for src, text in pages.items():
        for line in text.splitlines():
            for m in LINK.finditer(line):
                href = m.group(2).split("#", 1)[0]
                if not href or "://" in href or href.startswith("mailto:") or not href.endswith(".md"):
                    continue
                dest = posixpath.normpath(posixpath.join(posixpath.dirname(src), href))
                rest = LINK.sub("", line).strip(NOT_SUMMARY)
                out.append((src, dest, bool(rest)))
    return out


def reach_problems(pages: dict[str, str], front: str = "index.md") -> list[str]:
    """One plain-words problem per page too deep or unreached, broken link, and link with no summary."""
    links = _links(pages)
    problems = [f"{src} links to {dest}, which the wiki does not have." for src, dest, _ in links if dest not in pages]
    problems += [f"{src} links to {dest} with no summary beside the link: say what the page holds on the "
                 "link's own line." for src, dest, summary in links if not summary and dest in pages]
    depth = {front: 0} if front in pages else {}
    parent: dict[str, str] = {}  # the page each page was first reached from: walks back to the shortest chain
    frontier = list(depth)
    while frontier:
        nxt = []
        for page in frontier:
            for src, dest, _ in links:
                if src == page and dest in pages and dest not in depth:
                    depth[dest] = depth[page] + 1
                    parent[dest] = page
                    nxt.append(dest)
        frontier = nxt
    for page in sorted(pages):
        if page not in depth:
            problems.append(f"{page} is not reached from {front} by any chain of links. No chain of links exists.")
        elif depth[page] > 2:
            chain = [page]
            while chain[-1] != front:
                chain.append(parent[chain[-1]])
            problems.append(f"{page} is {depth[page]} links from {front}; every page must be within two. "
                            f"Shortest chain: {' -> '.join(reversed(chain))}.")
    return problems


def main(argv: list[str] | None = None) -> int:
    """`python -m lockstep.wiki_reach [--root DIR] [--package NAME]`: build the wiki pages, print each problem; exit 1 if any."""
    from lockstep.wiki import pages as wiki_pages  # lockstep.wiki runs AES; imported only when the check runs

    ap = argparse.ArgumentParser(prog="lockstep.wiki_reach", description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--package", default="src", help="the package the code page renders (default src)")
    args = ap.parse_args(argv)
    root = find_root(args.root)
    if root is None:
        print(f"no .aes/project.yaml at or above {args.root}", file=sys.stderr)
        return 2
    pages = wiki_pages(root, args.package)
    problems = reach_problems(pages)
    for p in problems:
        print(p)
    print(f"wiki_reach: pages={len(pages)} links={len(_links(pages))} problems={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
