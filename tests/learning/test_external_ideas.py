"""External idea intake: config, filtering, ranking, failure handling (fake fetcher, no network)."""
import json
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import external_ideas as E  # noqa: E402

NOW = 1_800_000_000.0


def post(pid, score, age_days, sub="a"):
    ts = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(NOW - age_days * 86400))
    return {"id": pid, "subreddit": sub, "title": f"t{pid}", "score": score, "replies": 1,
            "url": f"https://reddit.com/r/{sub}/{pid}", "body": "see https://github.com/x/y.", "created_at": ts}


def write_cfg(tmp_path, entries):
    p = tmp_path / "c.yaml"
    p.write_text(json.dumps({"subreddits": entries}))  # JSON is valid YAML
    return p


def entry(name="a", **kw):
    base = {"name": name, "reason": "r", "listing": "top", "window": "week", "limit": 10, "min_score": 5}
    base.update(kw)
    return base


@pytest.mark.req("external-idea-intake/invalid-config-refused")
@pytest.mark.parametrize("bad", [entry(listing="hot"), entry(reason=""), entry(limit=0), entry(min_score=-1)])
def test_invalid_config_refused_without_fetch(tmp_path, bad):
    calls = []
    rc = E.run(write_cfg(tmp_path, [bad]), tmp_path / "out", fetch=lambda *a: calls.append(a), now=NOW)
    assert rc != 0 and calls == []


@pytest.mark.req("external-idea-intake/invalid-config-refused")
def test_duplicate_name_refused(tmp_path):
    calls = []
    rc = E.run(write_cfg(tmp_path, [entry("a"), entry("A")]), tmp_path / "out", fetch=lambda *a: calls.append(a), now=NOW)
    assert rc != 0 and calls == []


@pytest.mark.req("external-idea-intake/digest-filters-and-ranks")
def test_filters_and_ranks_and_second_run_is_empty(tmp_path):
    posts = [post("seen", 99, 1), post("low", 1, 1), post("old", 99, 30), post("p1", 10, 2), post("p2", 40, 3)]
    out = tmp_path / "out"
    (out).mkdir()
    (out / "seen.json").write_text(json.dumps(["seen"]))
    fetch = lambda *a: {"subreddit": "a", "listing": "top", "count": len(posts), "results": posts}
    cfg = write_cfg(tmp_path, [entry()])
    assert E.run(cfg, out, fetch=fetch, now=NOW) == 0
    digest = next(out.glob("digest-*.md")).read_text()
    assert digest.index("tp2") < digest.index("tp1")
    for gone in ("tseen", "tlow", "told"):
        assert gone not in digest
    for f in out.glob("digest-*.md"):
        f.unlink()
    assert E.run(cfg, out, fetch=fetch, now=NOW) == 0
    assert "tp1" not in next(out.glob("digest-*.md")).read_text()


@pytest.mark.req("external-idea-intake/repeated-failure-is-down")
def test_repeated_failure_is_down_others_continue(tmp_path):
    def fetch(sub, listing, limit, window):
        if sub == "bad":
            raise RuntimeError("403")
        return {"subreddit": sub, "listing": listing, "count": 1, "results": [post("g", 10, 1, sub)]}
    out = tmp_path / "out"
    rc = E.run(write_cfg(tmp_path, [entry("bad"), entry("good")]), out, fetch=fetch, now=NOW)
    assert rc != 0
    assert "tg" in next(out.glob("digest-*.md")).read_text()
    log = [json.loads(line) for line in next(out.glob("runs-*.jsonl")).read_text().splitlines()]
    assert any(r.get("subreddit") == "bad" and r.get("status") == "down" for r in log)


@pytest.mark.req("external-idea-intake/output-outside-repo")
def test_all_files_under_out(tmp_path):
    out = tmp_path / "out"
    fetch = lambda sub, *a: {"subreddit": sub, "listing": "top", "count": 0, "results": []}
    cfg = write_cfg(tmp_path, [entry()])
    before = set(tmp_path.rglob("*"))
    E.run(cfg, out, fetch=fetch, now=NOW)
    new = set(tmp_path.rglob("*")) - before
    assert new and all(out in p.parents or p == out for p in new)


@pytest.mark.req("external-idea-intake/invalid-config-refused")
def test_shipped_config_is_valid_and_excludes_locallama():
    cfg = E.load_config(Path(E.__file__).with_name("external_sources.yaml"))
    names = [e["name"] for e in cfg]
    assert len(names) == 8 and "LocalLLaMA" not in names


@pytest.mark.req("external-idea-intake/digest-filters-and-ranks")
def test_malformed_post_is_skipped_not_fatal(tmp_path):
    posts = [{"id": "m", "title": "x"}, {**post("n", None, 1)}, post("ok", 10, 1)]
    out = tmp_path / "out"
    fetch = lambda *a: {"subreddit": "a", "listing": "top", "count": 3, "results": posts}
    assert E.run(write_cfg(tmp_path, [entry()]), out, fetch=fetch, now=NOW) == 0
    d = next(out.glob("digest-*.md")).read_text()
    assert "tok" in d and "tm" not in d.replace("tok", "")


@pytest.mark.req("external-idea-intake/repeated-failure-is-down")
def test_retry_success_and_different_errors(tmp_path):
    n = {"a": 0, "b": 0}
    def fetch(sub, *a):
        n[sub] += 1
        if sub == "a" and n[sub] == 1:
            raise RuntimeError("blip")
        if sub == "b":
            raise RuntimeError(f"err{n[sub]}")
        return {"subreddit": sub, "listing": "top", "count": 0, "results": []}
    out = tmp_path / "out"
    assert E.run(write_cfg(tmp_path, [entry("a"), entry("b")]), out, fetch=fetch, now=NOW) == 1
    log = [json.loads(l) for l in next(out.glob("runs-*.jsonl")).read_text().splitlines()]
    st = {r["subreddit"]: r["status"] for r in log if r["step"] == "fetch"}
    assert st == {"a": "ok", "b": "failed"}


@pytest.mark.req("external-idea-intake/invalid-config-refused")
def test_corrupt_seen_and_bad_yaml_refused(tmp_path):
    out = tmp_path / "out"; out.mkdir()
    (out / "seen.json").write_text("{trunc")
    fetch = lambda *a: pytest.fail("fetched")
    assert E.run(write_cfg(tmp_path, [entry()]), out, fetch=fetch, now=NOW) == 2
    bad = tmp_path / "b.yaml"; bad.write_text("subreddits: [a: b: c")
    assert E.run(bad, tmp_path / "o2", fetch=fetch, now=NOW) == 2
    assert E.run(write_cfg(tmp_path, [entry(limit=True)]), tmp_path / "o3", fetch=fetch, now=NOW) == 2
