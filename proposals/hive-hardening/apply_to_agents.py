"""Put WHAT_GOES_TO_BRIAN.md into the three Paperclip agents' AGENTS.md and remove the lines it supersedes.

Usage: python3 apply_to_agents.py <dir>   # reads <dir>/{coordinator,contact,research}.live.md,
                                          # writes <dir>/{name}.new.md; fails if any expected text is missing.
Uploading (with a dated backup) is done separately through scripts/hive/board.sh.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
BRI2 = "BRI-2 (Brian's Telegram thread, issue id `519c6831-6967-4177-aef5-5aaea5d91850`)"
MARK_START, MARK_END = "<!-- what-goes-to-brian:start -->", "<!-- what-goes-to-brian:end -->"


def section() -> str:
    text = (HERE / "WHAT_GOES_TO_BRIAN.md").read_text()
    body = text.split("## needs-reply: only these", 1)[1].split("## Contradictions this replaces", 1)[0]
    return (f"{MARK_START}\n## What goes to Brian (adopted 2026-10-06; overrides every other line here about contacting or asking Brian)\n\n"
            "Every message to Brian starts with one of three labels: `needs-reply`, `review` or `fyi`. Only a `needs-reply` message waits for "
            "an answer, and only an answer that really comes from Brian (his Telegram account or his dashboard login, never an agent) counts. "
            f"Post `needs-reply` and `review` items on {BRI2}.\n\n### needs-reply: only these" + body.rstrip()
            + "\n\nSource: `BrianMills2718/agentic-engineering-system-canonical` `proposals/hive-hardening/WHAT_GOES_TO_BRIAN.md`.\n"
            + MARK_END + "\n").replace("\n## ", "\n### ")


def sub(s: str, old: str, new: str) -> str:
    assert old in s, f"expected text not found: {old[:80]!r}"
    return s.replace(old, new, 1)


def line_starting(s: str, prefix: str) -> str:
    m = re.search(r"^" + re.escape(prefix) + r".*$", s, re.M)
    assert m, f"no line starts with {prefix!r}"
    return m.group(0)


def insert(s: str) -> str:
    if MARK_START in s:
        return re.sub(re.escape(MARK_START) + ".*?" + re.escape(MARK_END) + "\n", section(), s, flags=re.S)
    first_break = s.index("\n\n") + 2
    return s[:first_break] + section() + "\n" + s[first_break:]


ASK = ("follow \"What goes to Brian\" above: only its seven `needs-reply` cases ask him. For one of those, create a task assigned to him "
       "(`assigneeUserId`) titled `Decision: <one line>` with the context, the options, your recommendation and what happens by default, "
       "block the waiting task on it, and at the same moment post the `needs-reply` line with the task link on BRI-2. His reply there is "
       "the answer: copy it verbatim onto the waiting task and act on it in the same heartbeat. Never post an answer on a `needs-reply` "
       "message yourself, and act on a reply only when Brian wrote it.")
MERGE = line_starting  # alias for readability below


def coordinator(s: str) -> str:
    s = sub(s, line_starting(s, "- When input is needed from Brian,"), "- When input is needed from Brian, " + ASK)
    s = sub(s, "built by agents unattended, reviewed by him in his terminal, then merged.",
            "built by agents unattended, checked by the repository's own checks and merged by the agents, with a `review` item "
            "(a working UI during implementation, a plan picture during planning) sent to him at each review point.")
    s = sub(s, line_starting(s, "- Reaching Brian in real time"),
            "- Reaching Brian in real time: see \"What goes to Brian\" above (Brian, 2026-10-03: \"i want to know as soon as my agents try "
            "to send me a message and for them to get my response as soon as i respond\").")
    return insert(s)


def contact(s: str) -> str:
    s = sub(s, "You are agent Brian Contact (the only agent that messages Brian) at Brian.",
            "You are agent Brian Contact (the agent that sends Brian his news digest and relays his answers) at Brian.")
    s = sub(s, "Brian hears from the agent team through you and nobody else.",
            "Brian hears the team's news (`fyi`) through you; `needs-reply` and `review` items reach him directly from the agent that needs him, per \"What goes to Brian\".")
    s = sub(s, line_starting(s, "- When Brian must decide,"),
            "- When Brian must decide (only the `needs-reply` cases in \"What goes to Brian\" above), make sure a `Decision:` task "
            "assigned to him exists on the blocked work, set the blocked task to `in_review`, and make sure its `needs-reply` line is on BRI-2.")
    s = sub(s, line_starting(s, "- **One voice**"),
            "- **One voice for news** — `fyi` items (finished, stuck, a rule of his changed) reach Brian only through your digest. "
            "`needs-reply` and `review` items are posted at the moment by the agent that needs him, labelled, per \"What goes to Brian\"; "
            "you relay his answers.")
    s = sub(s, "a question asked in prose with no interaction card behind it", "a question for Brian with no `Decision:` task behind it")
    s = sub(s, "any question for Brian exists as an interaction card and not only as prose",
            "any question for Brian exists as a `Decision:` task and not only as prose")
    s = sub(s, "Use `in_review` only when a real card is pending Brian's answer.",
            "Use `in_review` only when a `Decision:` task is pending Brian's answer.")
    start = s.index("## Where Brian answers (Brian, 2026-10-02)")
    end = s.index("## Reaching Brian (Brian, 2026-10-03")
    s = s[:start] + s[end:]
    s = sub(s, line_starting(s, "Brian: \"i want to know as soon as my agents try to send me a message"),
            line_starting(s, "Brian: \"i want to know as soon as my agents try to send me a message")
            .split(" Merge rule (Brian, 2026-10-04", 1)[0].split("Brian: ", 1)[0]
            + "See \"What goes to Brian\" above. Merge rule (Brian, 2026-10-04"
            + line_starting(s, "Brian: \"i want to know as soon as my agents try to send me a message").split(" Merge rule (Brian, 2026-10-04", 1)[1])
    s = sub(s, "## Reaching Brian (Brian, 2026-10-03, supersedes the 2026-10-02 'Telegram unused' note)", "## Reaching Brian")
    return insert(s)


def research(s: str) -> str:
    old = line_starting(s, "Brian: \"i want to know as soon as my agents try to send me a message")
    s = sub(s, old, "Only for a `needs-reply` case or a `review` item in \"What goes to Brian\" above: post the labelled line with the task "
            "link on BRI-2 at the moment it happens; everything else bound for Brian goes to Brian Contact. Merge rule (Brian, 2026-10-04"
            + old.split(" Merge rule (Brian, 2026-10-04", 1)[1])
    s = sub(s, "- Everything bound for Brian → [Brian Contact](/BRI/agents/brian-contact). You never contact him directly.",
            "- `fyi` news for Brian → [Brian Contact](/BRI/agents/brian-contact). `needs-reply` and `review` items go on BRI-2 as \"What goes to Brian\" says; nothing else goes to him directly.")
    s = sub(s, "- **Needs Brian's approval, requested through Coordinator and Brian Contact, before you act:** merging to a default branch; deploying or releasing; deleting",
            "- **Needs Brian's approval (a `needs-reply` case in \"What goes to Brian\") before you act:** deleting")
    return insert(s)


def main() -> None:
    d = Path(sys.argv[1])
    for name, fn in (("coordinator", coordinator), ("contact", contact), ("research", research)):
        new = fn((d / f"{name}.live.md").read_text())
        (d / f"{name}.new.md").write_text(new)
        print(f"{name}: {len(new)} chars")


if __name__ == "__main__":
    main()
