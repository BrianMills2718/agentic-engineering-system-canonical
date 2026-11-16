"""Depth-aware usefulness judge for external ideas.

Implements: external-idea-intake/depth-judge-reads-more-when-asked.
Round 1: the model sees each post's title and opening text plus the project list and, per post, decides
useful / not useful / need more (comments, linked pages, or both). Round 2: this code reads exactly what
was asked for (the model never fetches anything itself, so a hostile page cannot steer a tool) and the model
gives a final verdict on those posts. Posts are judged by a Claude model through the subscription route.
"""
from __future__ import annotations

import json
import re
import time
import urllib.request
from typing import Callable, Literal

from pydantic import BaseModel

JUDGE_MODEL = "claude-code/sonnet"
PAGE_CHARS = 5000
COMMENT_CHARS = 4000
MAX_LINKS = 2

PROMPT = (
    "You help one person decide which outside posts are worth reading. Below are their projects, then new "
    "posts from one subreddit. For each post decide:\n"
    "- useful: it could concretely help at least one project (a technique, tool, finding, design or "
    "warning they could adopt or must know about). Name at most two projects, the best fits, exactly as "
    "written in the list, and give a reason that names the specific thing to adopt or learn and where it "
    "would be used. No generic phrases like 'directly applicable'.\n"
    "- not_useful: you can already tell it has no concrete use (pure entertainment, news, hype, off-topic).\n"
    "- need_more: you cannot tell from the title and opening text. A question's value comes from its "
    "answers, so ask for the comments. A demo or announcement may rest on a repository or article, so ask "
    "for the linked pages. Say which: comments, links or both. Prefer need_more to guessing, but do not "
    "ask for more when the post is clearly useful or clearly not.\n"
    "Return one entry for every post id.\n\n")
FINAL = (
    "Here is the extra material you asked for. Give a final verdict for each post: useful or not_useful "
    "(need_more is no longer allowed). Same rules for projects and reason.\n\n")


class Verdict(BaseModel):
    id: str
    decision: Literal["useful", "not_useful", "need_more"]
    projects: list[str] = []
    reason: str = ""
    want: Literal["comments", "links", "both", "none"] = "none"


class Verdicts(BaseModel):
    verdicts: list[Verdict]


def read_page(url: str) -> str:
    """Plain text of a linked page (tags stripped, capped); empty string on any failure."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (idea-intake reader)"})
        with urllib.request.urlopen(req, timeout=15) as r:  # noqa: S310 - http(s) links from posts, read-only GET
            if not url.startswith(("http://", "https://")):
                return ""
            raw = r.read(400_000).decode("utf-8", "replace")
    except Exception:  # noqa: BLE001 - an unreadable page is just no extra material
        return ""
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    return re.sub(r"\s+", " ", re.sub(r"(?s)<[^>]+>", " ", raw)).strip()[:PAGE_CHARS]


def links_in(text: str) -> list[str]:
    seen: list[str] = []
    for u in re.findall(r"https?://[^\s)\]>*]+", text or ""):
        u = u.rstrip(".,")
        if "reddit.com" in u or "redd.it" in u or u in seen:
            continue
        seen.append(u)
    return seen


def make_reader(fetch_post: Callable[[str], dict], page: Callable[[str], str] = read_page):
    """read_more(post_id, want) -> text. `fetch_post` returns the social-media `reddit_post` dict."""
    def read_more(post_id: str, want: str) -> str:
        data = fetch_post(post_id)
        parts: list[str] = []
        if want in ("comments", "both"):
            cs = "\n".join(f"{'  ' * int(c.get('depth', 0))}- {c.get('text', '')}" for c in data.get("comments", []))
            parts.append("COMMENTS:\n" + cs[:COMMENT_CHARS])
        if want in ("links", "both"):
            for u in links_in(data.get("text", ""))[:MAX_LINKS]:
                body = page(u)
                parts.append(f"LINKED PAGE {u}:\n{body}" if body else f"LINKED PAGE {u}: (could not be read)")
        return "\n\n".join(parts) or "(nothing more could be read)"
    return read_more


def build_judge(projects: list[dict], call: Callable[[str], Verdicts],
                read_more: Callable[[str, str], str]):
    """`call(prompt) -> Verdicts` runs the model; `read_more` does the reading. Returns a Judge."""
    plist = "\n".join(f"- {p['name']}: {p['goal']}" for p in projects)

    def judge(sub: str, posts: list) -> dict:
        t0 = time.time()
        body = "\n\n".join(f"id: {p['id']}\ntitle: {p['title']}\ntext: {p.get('body', '')}" for p in posts)
        by_id = {p["id"]: p for p in posts}
        r1 = {v.id: v for v in call(f"{PROMPT}Projects:\n{plist}\n\nPosts from r/{sub}:\n\n{body}").verdicts if v.id in by_id}
        out: dict = {}
        asked: dict[str, str] = {}
        for pid, v in r1.items():
            if v.decision == "useful":
                out[pid] = (v.projects, v.reason, "title")
            elif v.decision == "need_more":
                asked[pid] = v.want if v.want != "none" else "both"
        if asked:
            extra = "\n\n".join(
                f"id: {pid}\ntitle: {by_id[pid]['title']}\ntext: {by_id[pid].get('body', '')}\n"
                f"You asked for: {want}\n{read_more(pid, want)}" for pid, want in asked.items())
            for v in call(f"{FINAL}Projects:\n{plist}\n\n{extra}").verdicts:
                if v.id in asked and v.decision == "useful":
                    out[v.id] = (v.projects, v.reason, f"read {asked[v.id]}")
        judge.log({"step": "judge-depth", "subreddit": sub, "posts": len(posts), "round1_useful": sum(
            1 for v in r1.values() if v.decision == "useful"), "asked_more": len(asked),
            "asked": dict(asked), "final_useful": len(out), "seconds": round(time.time() - t0, 1)})
        return out
    judge.log = lambda r: None  # type: ignore[attr-defined]  # run() points this at the run log
    judge.names = [p["name"] for p in projects]  # type: ignore[attr-defined]
    judge.cost = 0.0  # type: ignore[attr-defined]
    return judge
