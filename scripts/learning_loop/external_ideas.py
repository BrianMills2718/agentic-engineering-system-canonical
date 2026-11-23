#!/usr/bin/env python3
"""External idea intake: watch the subreddits named in external_sources.yaml, write a ranked digest.

Spec: openspec/specs/external-idea-intake/spec.md. The daily timer is systemd/external-ideas.timer.

Implements: external-idea-intake/the-watch-list-is-configuration-and-an-invalid-one-is-refused
Implements: external-idea-intake/the-digest-ranks-new-posts-by-score-and-age-only
Implements: external-idea-intake/every-run-is-traced-and-a-repeated-failure-is-reported-as-down
Implements: external-idea-intake/output-stays-outside-the-repository-and-the-register-is-never-written
Implements: external-idea-intake/a-project-profile-makes-the-digest-rank-by-usefulness-to-brian-s-projects
Implements: external-idea-intake/posts-already-assessed-into-raw-sources-are-never-offered-again
Implements: external-idea-intake/a-daily-timer-runs-the-digest-with-the-project-profile
Implements: external-idea-intake/the-profile-may-list-interests-and-the-judge-treats-them-like-projects

Ranks by score and age only. With --profile, a light model also judges usefulness to the listed projects
(prose meaning is never judged by regex) and writes a second digest. Output, seen list and run log go outside the repository.
Run on request:
  uv run --with-editable ~/code2/mcp-servers/social-media [--with-editable '~/code2/llm_client[agents]' for --profile] python scripts/learning_loop/external_ideas.py
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
from calendar import timegm
from pathlib import Path
from typing import Callable

from ruamel.yaml import YAML

CONFIG = Path(__file__).with_name("external_sources.yaml")
OUT_DEFAULT = Path(os.environ.get("EXTERNAL_IDEAS_OUT", "~/projects/data/external-ideas")).expanduser()
SOCIAL_MEDIA = Path(os.environ.get("SOCIAL_MEDIA_MCP", "~/code2/mcp-servers/social-media")).expanduser()
LISTINGS = {"top", "new"}
WINDOW_DAYS = {"day": 1, "week": 7, "month": 31, "year": 366}
Fetch = Callable[[str, str, int, str], dict]
# judge(subreddit, posts) -> {post id: (project names, one-line reason)} for the posts judged useful
Judge = Callable[[str, list], dict]
JUDGE_MODEL = "claude-code/sonnet"  # shown in the digest header; the real default is external_judge.JUDGE_MODEL
RAW_SOURCES = Path(__file__).resolve().parents[2] / "raw" / "sources"


class ConfigError(ValueError):
    pass


def load_config(path: Path) -> list[dict]:
    """Return the validated subreddit entries; raise ConfigError naming the first bad entry."""
    try:
        data = YAML(typ="safe").load(Path(path).read_text()) or {}
    except Exception as exc:  # noqa: BLE001 - malformed YAML is a config error
        raise ConfigError(f"unreadable YAML: {exc}") from exc
    entries = data.get("subreddits") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ConfigError("`subreddits` must be a non-empty list")
    seen: set[str] = set()
    for e in entries:
        name = e.get("name") if isinstance(e, dict) else None
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_]+", name):
            raise ConfigError(f"entry without a name: {e!r}")
        if name.lower() in seen:
            raise ConfigError(f"{name}: duplicate name")
        seen.add(name.lower())
        if not str(e.get("reason", "")).strip():
            raise ConfigError(f"{name}: reason is required")
        if e.get("listing") not in LISTINGS:
            raise ConfigError(f"{name}: listing must be one of {sorted(LISTINGS)}")
        if e.get("window") not in WINDOW_DAYS:
            raise ConfigError(f"{name}: window must be one of {sorted(WINDOW_DAYS)}")
        if not (type(e.get("limit")) is int and 1 <= e["limit"] <= 100):
            raise ConfigError(f"{name}: limit must be an integer 1..100")
        if not (type(e.get("min_score")) is int and e["min_score"] >= 0):
            raise ConfigError(f"{name}: min_score must be an integer >= 0")
    return entries


def _social_media_tool(name: str):
    """A public async tool of the social-media server, with Reddit credentials loaded (values never printed)."""
    sys.path.insert(0, str(SOCIAL_MEDIA))
    import run_stdio  # type: ignore

    env, _, _ = run_stdio.build_child_environment(run_stdio.default_secrets_file(os.environ))
    os.environ.update({k: v for k, v in env.items() if k.startswith("REDDIT_")})
    import server  # type: ignore

    return getattr(getattr(server, name), "fn", getattr(server, name))


def social_media_fetch() -> Fetch:
    """Fetch through the social-media server's public `reddit_subreddit_posts` tool.

    Credentials come from the server's own launcher logic (named keys only, values never printed).
    """
    sys.path.insert(0, str(SOCIAL_MEDIA))
    import run_stdio  # type: ignore

    env, _, _ = run_stdio.build_child_environment(run_stdio.default_secrets_file(os.environ))
    os.environ.update({k: v for k, v in env.items() if k.startswith("REDDIT_")})
    import server  # type: ignore

    tool = getattr(server.reddit_subreddit_posts, "fn", server.reddit_subreddit_posts)

    def fetch(sub: str, listing: str, limit: int, window: str) -> dict:
        return json.loads(asyncio.run(tool(sub, listing, limit, window)))

    return fetch


def load_profile(path: Path) -> list[dict]:
    """Projects (and optional interests) to judge usefulness against: each needs a name and a one-line goal.

    Interest entries come back with kind "interest".

    Implements: external-idea-intake/the-profile-may-list-interests-and-the-judge-treats-them-like-projects

    Requirement text (generated):
        external-idea-intake/the-profile-may-list-interests-and-the-judge-treats-them-like-projects:
            The private profile MAY carry an `interests` list whose entries each need a name and a
            one-line goal. The judge SHALL list interests after projects, SHALL accept an interest
            name as a useful post's target, and the useful digest SHALL print projects and interests
            on separate lines. A profile without `interests` SHALL behave as before. An interest
            entry without a name or goal SHALL make the command refuse the profile.
    """
    try:
        data = YAML(typ="safe").load(Path(path).read_text()) or {}
    except Exception as exc:  # noqa: BLE001
        raise ConfigError(f"unreadable profile: {exc}") from exc
    projects = data.get("projects") if isinstance(data, dict) else None
    if not isinstance(projects, list) or not projects:
        raise ConfigError("profile needs a non-empty `projects` list")
    interests = data.get("interests") or []
    if not isinstance(interests, list):
        raise ConfigError("profile `interests` must be a list")
    entries = []
    for kind, group in (("project", projects), ("interest", interests)):
        for pr in group:
            if not (isinstance(pr, dict) and str(pr.get("name", "")).strip() and str(pr.get("goal", "")).strip()):
                raise ConfigError(f"profile entry needs name and goal: {pr!r}")
            entries.append({**pr, "kind": kind})
    return entries


def llm_judge(projects: list[dict]) -> Judge:
    """Depth-aware judge: a Claude model (subscription route) decides per post how much more to read."""
    import external_judge as J
    from llm_client import call_llm_structured  # type: ignore

    model = os.environ.get("EXTERNAL_IDEAS_JUDGE_MODEL", J.JUDGE_MODEL)
    tool = _social_media_tool("reddit_post")

    def fetch_post(pid: str) -> dict:
        return json.loads(asyncio.run(tool(pid, 15, True, 0)))

    def call(prompt: str) -> "J.Verdicts":
        res, meta = call_llm_structured(
            model, [{"role": "user", "content": prompt}], response_model=J.Verdicts, task="external-ideas.judge",
            model_justification="model judges whether a post helps a project (prose meaning; workspace rule)",
            agent_options={"tools": [], "setting_sources": [], "max_turns": 1},
            trace_id=f"external-ideas/judge/{int(time.time() * 1000)}", max_budget=0.5)
        judge.cost += float(meta.cost or 0)
        return res

    judge = J.build_judge(projects, call, J.make_reader(fetch_post))
    return judge


def assessed_ids(raw_dir: Path) -> set[str]:
    """Reddit post ids already captured and assessed: capture folders are named `<date>-reddit-<id>-<slug>`."""
    if not Path(raw_dir).is_dir():
        return set()
    parts = [d.name.split("-") for d in Path(raw_dir).iterdir()]
    return {p[4] for p in parts if len(p) > 4 and p[3] == "reddit"}


def _age_days(created_at: str, now: float) -> float:
    ts = timegm(time.strptime(created_at[:19], "%Y-%m-%dT%H:%M:%S"))
    return (now - ts) / 86400


def _links(body: str) -> list[str]:
    return [u.rstrip(".,)") for u in re.findall(r"https?://\S+", body or "")]


def _log(path: Path, rec: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(rec, default=str) + "\n")


def run(config: Path, out: Path, fetch: Fetch | None = None, now: float | None = None,
        judge: Judge | None = None, assessed_dir: Path | None = None) -> int:
    """Run once; return 0, or non-zero on a bad config or any subreddit reported down."""
    now = time.time() if now is None else now
    out = Path(out)
    try:
        entries = load_config(config)
    except (ConfigError, OSError) as exc:
        print(f"external_ideas: invalid config: {exc}", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    day = time.strftime("%Y-%m-%d", time.gmtime(now))
    log = out / f"runs-{day}.jsonl"
    seen_file = out / "seen.json"
    try:
        seen = set(json.loads(seen_file.read_text())) if seen_file.exists() else set()
    except (ValueError, OSError) as exc:
        print(f"external_ideas: seen list unreadable ({seen_file}): {exc}", file=sys.stderr)
        return 2
    assessed = assessed_ids(RAW_SOURCES if assessed_dir is None else assessed_dir)
    seen |= assessed
    if hasattr(judge, "log"):
        judge.log = lambda r: _log(log, r)  # type: ignore[union-attr]
    _log(log, {"step": "assessed", "already_assessed": len(assessed)})
    _log(log, {"step": "config", "path": str(config), "subreddits": [e["name"] for e in entries], "seen": len(seen)})
    if fetch is None:
        try:
            fetch = social_media_fetch()
        except Exception as exc:  # noqa: BLE001 - logged, then a clean non-zero exit
            _log(log, {"step": "setup", "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
            print(f"external_ideas: cannot load the social-media tool ({type(exc).__name__}: {exc}). "
                  "Run with: uv run --with-editable ~/code2/mcp-servers/social-media python "
                  "scripts/learning_loop/external_ideas.py", file=sys.stderr)
            return 2
    candidates: list[dict] = []
    useful: list[dict] = []
    skipped: list[str] = []
    unjudged: set[str] = set()
    known = set(getattr(judge, "names", ()))  # profile names; empty = no validation (custom judge)
    down = 0
    for e in entries:
        t0 = time.time()
        result, errors = None, []
        for _ in range(2):
            try:
                result = fetch(e["name"], e["listing"], e["limit"], e["window"])
                break
            except Exception as exc:  # noqa: BLE001 - any failure is recorded, then retried once
                errors.append(f"{type(exc).__name__}: {exc}")
        if result is None:
            same = len(errors) == 2 and errors[0] == errors[1]
            down += 1
            _log(log, {"step": "fetch", "subreddit": e["name"], "status": "down" if same else "failed",
                       "errors": errors, "seconds": round(time.time() - t0, 2)})
            continue
        posts = result.get("results", []) if isinstance(result, dict) else []
        kept, counts = [], {"seen": 0, "low_score": 0, "too_old": 0, "malformed": 0}
        for p in posts:
            try:
                bad = not (isinstance(p["score"], int) and p["id"] and p["title"] is not None
                           and _age_days(p["created_at"], now) is not None)
            except (KeyError, TypeError, ValueError):
                bad = True
            if bad:
                counts["malformed"] += 1
            elif p["id"] in seen:
                counts["seen"] += 1
            elif p["score"] < e["min_score"]:
                counts["low_score"] += 1
            elif _age_days(p["created_at"], now) > WINDOW_DAYS[e["window"]]:
                counts["too_old"] += 1
            else:
                kept.append({**p, "age_days": round(_age_days(p["created_at"], now), 1), "reason": e["reason"]})
        if judge is not None and kept:
            try:
                hits = judge(e["name"], kept)
            except Exception as exc:  # noqa: BLE001 - logged; posts stay unseen so a later run offers them again
                down += 1
                _log(log, {"step": "judge", "subreddit": e["name"], "status": "failed",
                           "error": f"{type(exc).__name__}: {str(exc)[:300]}"})
                skipped.append(e["name"])
                continue
            ids = {p["id"] for p in kept}
            unjudged |= set(getattr(judge, "unjudged", ()))
            by_id = {p["id"]: p for p in kept}
            for pid, hit in hits.items():
                names, why, depth = (list(hit) + ["title"])[:3] if len(hit) == 2 else hit
                if pid in by_id:
                    good = [n for n in names if not known or n in known]
                    if len(good) != len(names):
                        _log(log, {"step": "judge", "subreddit": e["name"], "dropped_project_names":
                                   [n for n in names if known and n not in known]})
                    useful.append({**by_id[pid], "projects": good, "why": why, "depth": depth})
            _log(log, {"step": "judge", "subreddit": e["name"], "status": "ok", "posts": len(kept),
                       "useful": sum(1 for h in hits if h in ids)})
        candidates += kept
        _log(log, {"step": "fetch", "subreddit": e["name"], "status": "ok", "count": len(posts),
                   "kept": len(kept), "dropped": counts, "seconds": round(time.time() - t0, 2)})
    candidates.sort(key=lambda p: (-p["score"], p["age_days"]))
    digest = out / f"digest-{time.strftime('%Y%m%dT%H%M%S', time.gmtime(now))}.md"
    lines = [f"# External idea digest {day}", "",
             f"{len(candidates)} new posts, ranked by score then age; this list does no relevance judgement.", ""]
    if skipped:
        lines += [f"Not shown: r/{n} (usefulness judge failed; its posts are offered again next run).".replace("r/r/", "r/") for n in skipped] + [""]
    for p in candidates:
        links = ", ".join(_links(p.get("body", ""))[:5]) or "none in the first 500 characters"
        lines += [f"- **{p['title']}** (r/{p['subreddit']}, score {p['score']}, {p['age_days']} days old, "
                  f"{p['replies']} comments)", f"  {p['url']}", f"  Why watched: {p['reason']}. Links in body: {links}"]
    digest.write_text("\n".join(lines) + "\n")
    if judge is not None:
        ul = [f"# Useful to your projects {day}", "",
              f"{len(useful)} of {len(candidates)} new posts judged useful by "
              f"{os.environ.get('EXTERNAL_IDEAS_JUDGE_MODEL', JUDGE_MODEL)}; each post listed once, "
              "score then age.", ""]
        for p in sorted(useful, key=lambda p: (-p["score"], p["age_days"])):
            ints = set(getattr(judge, "interests", ()))
            pj = [n for n in p["projects"] if n not in ints]
            it = [n for n in p["projects"] if n in ints]
            ul += [f"- **{p['title']}** (r/{p['subreddit']}, score {p['score']}, {p['age_days']} days old)"]
            if pj or not it:
                ul += [f"  Projects: {', '.join(pj) or '(unassigned)'}"]
            if it:
                ul += [f"  Interests: {', '.join(it)}"]
            ul += [f"  {p['url']}", f"  How (judged from: {p.get('depth', 'title')}): {p['why']}"]
        (out / digest.name.replace("digest-", "digest-useful-")).write_text("\n".join(ul) + "\n")
        _log(log, {"step": "useful-digest", "useful": len(useful), "of": len(candidates),
                   "model_cost_usd": round(getattr(judge, "cost", 0.0), 5)})
    seen |= {p["id"] for p in candidates} - unjudged
    tmp = seen_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(sorted(seen)))
    tmp.replace(seen_file)
    _log(log, {"step": "digest", "path": str(digest), "candidates": len(candidates), "down": down})
    return 1 if down else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=CONFIG)
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    ap.add_argument("--profile", type=Path, default=None,
                    help="projects.yaml (outside the repo): judge usefulness to these projects with a light model")
    a = ap.parse_args()
    judge = None
    if a.profile:
        try:
            judge = llm_judge(load_profile(a.profile))
        except (ConfigError, OSError, ImportError) as exc:
            print(f"external_ideas: profile/model unavailable: {exc}", file=sys.stderr)
            return 2
    return run(a.config, a.out, judge=judge)


if __name__ == "__main__":
    raise SystemExit(main())
