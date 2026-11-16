#!/usr/bin/env python3
"""External idea intake: watch the subreddits named in external_sources.yaml, write a ranked digest.

Implements: external-idea-intake/* (openspec/specs/external-idea-intake/spec.md).
Ranks by score and age only; it never judges relevance (that is prose meaning and would need an approved
light model as a separate, measured stage). Output, seen list and run log go outside the repository.
Run on request:
  uv run --with-editable ~/code2/mcp-servers/social-media python scripts/learning_loop/external_ideas.py
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


class ConfigError(ValueError):
    pass


def load_config(path: Path) -> list[dict]:
    """Return the validated subreddit entries; raise ConfigError naming the first bad entry."""
    data = YAML(typ="safe").load(Path(path).read_text()) or {}
    entries = data.get("subreddits")
    if not isinstance(entries, list) or not entries:
        raise ConfigError("`subreddits` must be a non-empty list")
    seen: set[str] = set()
    for e in entries:
        name = str(e.get("name", "")).strip() if isinstance(e, dict) else ""
        if not name:
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
        if not (isinstance(e.get("limit"), int) and 1 <= e["limit"] <= 100):
            raise ConfigError(f"{name}: limit must be an integer 1..100")
        if not (isinstance(e.get("min_score"), int) and e["min_score"] >= 0):
            raise ConfigError(f"{name}: min_score must be an integer >= 0")
    return entries


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


def _age_days(created_at: str, now: float) -> float:
    ts = timegm(time.strptime(created_at[:19], "%Y-%m-%dT%H:%M:%S"))
    return (now - ts) / 86400


def _links(body: str) -> list[str]:
    return [u.rstrip(".,)") for u in re.findall(r"https?://\S+", body or "")]


def _log(path: Path, rec: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(rec, default=str) + "\n")


def run(config: Path, out: Path, fetch: Fetch | None = None, now: float | None = None) -> int:
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
    seen = set(json.loads(seen_file.read_text())) if seen_file.exists() else set()
    _log(log, {"step": "config", "path": str(config), "subreddits": [e["name"] for e in entries], "seen": len(seen)})
    fetch = fetch or social_media_fetch()
    candidates: list[dict] = []
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
        posts = result.get("results", [])
        kept, counts = [], {"seen": 0, "low_score": 0, "too_old": 0}
        for p in posts:
            if p["id"] in seen:
                counts["seen"] += 1
            elif p["score"] < e["min_score"]:
                counts["low_score"] += 1
            elif _age_days(p["created_at"], now) > WINDOW_DAYS[e["window"]]:
                counts["too_old"] += 1
            else:
                kept.append({**p, "age_days": round(_age_days(p["created_at"], now), 1), "reason": e["reason"]})
        candidates += kept
        _log(log, {"step": "fetch", "subreddit": e["name"], "status": "ok", "count": len(posts),
                   "kept": len(kept), "dropped": counts, "seconds": round(time.time() - t0, 2)})
    candidates.sort(key=lambda p: (-p["score"], p["age_days"]))
    digest = out / f"digest-{time.strftime('%Y%m%dT%H%M%S', time.gmtime(now))}.md"
    lines = [f"# External idea digest {day}", "",
             f"{len(candidates)} new posts, ranked by score then age. No relevance judgement.", ""]
    for p in candidates:
        links = ", ".join(_links(p.get("body", ""))[:5]) or "none in the first 500 characters"
        lines += [f"- **{p['title']}** (r/{p['subreddit']}, score {p['score']}, {p['age_days']} days old, "
                  f"{p['replies']} comments)", f"  {p['url']}", f"  Why watched: {p['reason']}. Links in body: {links}"]
    digest.write_text("\n".join(lines) + "\n")
    seen |= {p["id"] for p in candidates}
    seen_file.write_text(json.dumps(sorted(seen)))
    _log(log, {"step": "digest", "path": str(digest), "candidates": len(candidates), "down": down})
    return 1 if down else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=CONFIG)
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    a = ap.parse_args()
    return run(a.config, a.out)


if __name__ == "__main__":
    raise SystemExit(main())
