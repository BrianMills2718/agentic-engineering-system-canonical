"""Behavior 6.2: every page of a generated wiki is within two links of its front page, each link with a summary."""

from lockstep_support import REPO
from lockstep.wiki import pages
from lockstep.wiki_reach import reach_problems


def test_a_built_wiki_reaches_every_page_within_two_links_with_summaries(planned):
    wiki = pages(planned, "greeter")
    assert set(wiki) == {"index.md", "components/CMP-GREETER.md", "requirements/OUT-001.md", "code.md", "change-log.md"}
    assert reach_problems(wiki) == []


def test_a_page_three_links_deep_is_reported():
    wiki = {"index.md": "- [A](a.md) the first page\n",
            "a.md": "- [B](sub/b.md) the second page\n",
            "sub/b.md": "- [C](../c.md) the third page\n",
            "c.md": "# C\n"}
    assert reach_problems(wiki) == ["c.md is 3 links from index.md; every page must be within two. "
                                    "Shortest chain: index.md -> a.md -> sub/b.md -> c.md."]


def test_the_chain_reported_is_the_shortest_one():
    wiki = {"index.md": "- [A](a.md) a\n- [D](d.md) d\n", "a.md": "- [B](b.md) b\n", "b.md": "- [X](x.md) x\n",
            "x.md": "- [C](c.md) c\n", "d.md": "- [E](e.md) e\n", "e.md": "- [C](c.md) c\n", "c.md": "# C\n"}
    assert reach_problems(wiki) == [
        "c.md is 3 links from index.md; every page must be within two. Shortest chain: index.md -> d.md -> e.md -> c.md.",
        "x.md is 3 links from index.md; every page must be within two. Shortest chain: index.md -> a.md -> b.md -> x.md."]


def test_a_page_no_link_reaches_is_reported_as_having_no_chain():
    wiki = {"index.md": "- [A](a.md) the first page\n", "a.md": "# A\n", "lost.md": "- [A](a.md) back\n"}
    assert reach_problems(wiki) == ["lost.md is not reached from index.md by any chain of links. No chain of links exists."]


def test_a_link_with_no_summary_an_unreached_page_and_a_broken_link_are_reported():
    wiki = {"index.md": "- [A](a.md)\n| [B](b.md) | the B page |\n- [Gone](gone.md) — not here\n",
            "a.md": "# A\n", "b.md": "# B\n", "lost.md": "# Lost\n"}
    assert reach_problems(wiki) == [
        "index.md links to gone.md, which the wiki does not have.",
        "index.md links to a.md with no summary beside the link: say what the page holds on the link's own line.",
        "lost.md is not reached from index.md by any chain of links. No chain of links exists."]
