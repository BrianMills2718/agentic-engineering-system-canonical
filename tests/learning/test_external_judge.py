"""Depth-aware judge: the model asks for more, code reads exactly that, final verdicts (fake model, no network)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "learning_loop"))
import external_judge as J  # noqa: E402

PROJECTS = [{"name": "aes", "goal": "g"}]
POSTS = [{"id": "a", "title": "ta", "body": "x"}, {"id": "q", "title": "a question", "body": ""},
         {"id": "n", "title": "tn", "body": ""}]


def V(**kw):
    return J.Verdict(**kw)


@pytest.mark.req("external-idea-intake/depth-judge-reads-more-when-asked")
def test_reads_only_what_was_asked_and_uses_final_verdict():
    prompts, reads = [], []
    def call(prompt):
        prompts.append(prompt)
        if len(prompts) == 1:
            return J.Verdicts(verdicts=[V(id="a", decision="useful", projects=["aes"], reason="adopt x"),
                                        V(id="q", decision="need_more", want="comments"),
                                        V(id="n", decision="not_useful")])
        return J.Verdicts(verdicts=[V(id="q", decision="useful", projects=["aes"], reason="answers name tool y")])
    def read_more(pid, want):
        reads.append((pid, want))
        return "COMMENTS: use tool y"
    judge = J.build_judge(PROJECTS, call, read_more)
    got = judge("sub", POSTS)
    assert reads == [("q", "comments")]
    assert got == {"a": (["aes"], "adopt x", "title"), "q": (["aes"], "answers name tool y", "read comments")}
    assert "use tool y" in prompts[1] and "id: a" not in prompts[1]


@pytest.mark.req("external-idea-intake/depth-judge-reads-more-when-asked")
def test_no_second_call_when_nothing_needs_more_and_unknown_ids_ignored():
    calls = []
    def call(prompt):
        calls.append(prompt)
        return J.Verdicts(verdicts=[V(id="ghost", decision="useful", projects=["aes"], reason="r"),
                                    V(id="a", decision="not_useful")])
    judge = J.build_judge(PROJECTS, call, lambda *a: pytest.fail("read"))
    assert judge("s", POSTS) == {} and len(calls) == 1


@pytest.mark.req("external-idea-intake/depth-judge-reads-more-when-asked")
def test_reader_gets_comments_and_links_and_skips_reddit_links():
    data = {"text": "see https://github.com/x/y and https://reddit.com/r/a/b.", "comments": [{"text": "great", "depth": 1}]}
    read = J.make_reader(lambda pid: data, page=lambda u: f"PAGE {u}")
    out = read("p", "both")
    assert "- great" in out and "PAGE https://github.com/x/y" in out and "reddit.com" not in out.split("COMMENTS")[1].split("LINKED")[1]
    assert "LINKED" not in read("p", "comments")
