# What goes to Brian

Status: adopted 2026-10-06 (Brian: "ok"), hive-hardening plan unit U1. One rule for every agent and script, replacing the Brian-facing sections now scattered across the workspace `AGENTS.md`, Claude memory, the hive roadmap and the three Paperclip agents' instructions, which contradict each other (listed at the end).

Every message to Brian starts with one of three labels: `needs-reply`, `review` or `fyi`. Only a `needs-reply` message waits for an answer, and only an answer that really comes from Brian (his Telegram account or his dashboard login) counts.

## needs-reply: only these

Each is Brian's own rule, quoted where it was set.

1. **Irreversible actions:** deleting data or history, a database migration. (2026-10-03: "i dont even want to answer merge for anything that isnt public facing and that is not irreversible.")
2. **Anything sent outward,** with the exact text: email, messages or posts to people, comments on other people's repositories, anything published. (Workspace rules; outbound email policy.)
3. **Restarting WSL** (and so compacting its disk). (2026-09-28: "please dont restart wsl without telling me.") Approving a fix is not approving the restart it needs.
4. **Spending money** beyond trivial API costs. (Hive roadmap, "Brian decides before it happens".)
5. **A merge or deploy to something he has said is out with people for review.** No other merge or deploy asks. (2026-10-04: "i only care about things that i have already sent out for people to review.")
6. **Access only he can give:** a login, credential, payment, device. Asked once, with literal steps; the credential is then stored so it never blocks twice. (2026-09-15.)
7. **A business, product or priority call that is both uncertain and high-impact,** sent as one recommendation with a default, never a list of questions. (2026-09-14, 2026-09-29.)

Never `needs-reply`: technical or correctness questions (decide, verify, report), "is this safe", "should I proceed" on reversible work, merges, deploys of his own tools with nothing private in them.

## review: something for him to open and judge

Brian, 2026-10-06: "on the reaches me would be stuff to review. the way this is supposed to work is that this is by default a working ui for me to examine during the implementation stage. or plans during the planning stage."

- **Planning stage:** the plan as a picture he can open (a review page served from git at hive.brianmills.dev/plans/, designed through Representation Router), not prose.
- **Implementation stage:** a working UI slice he can open and click, at a URL, showing the new behaviour on real data; not a report about it, not a diff.
- Before it is sent: the work's own checks pass and a cold reviewer (an agent that did not build it) has opened it and found it usable; the message says in one line what to look at and what changed since the last review.
- His feedback is welcome but the work does not stop to wait for it; anything he says becomes input to the next step. If the plan contains a call only he can make, that call goes separately as `needs-reply` (item 7).

## fyi: reaches him, no reply expected

- **Finished:** something he asked for is done, with where to look.
- **Stopped or stuck,** when no agent can unstick it, after the agent that owns it has tried.
- **A rule changed** that he set.

One plain sentence, once per change of state. Not: progress, routine failures (those go to an agent first, which fixes them; Brian, 2026-10-06), agent-to-agent traffic, "still waiting".

## How it is delivered

- `needs-reply` and `review`: at the moment it happens, posted by the agent that needs him on his Telegram thread (board BRI-2), first word the label, then one or two plain sentences and the link. (2026-10-03: "i want to know as soon as my agents try to send me a message and for them to get my response as soon as i respond.")
- `fyi`: gathered by Brian Contact into one short digest per cycle; nothing else goes to him.
- His answers: Brian Contact (or the waiting agent) copies his reply verbatim onto the waiting task.
- Scripts post as the alert bot, never as Brian.
- No agent replies on a `needs-reply` message. An agent that acts on a reply checks its author first.

## Contradictions this replaces (found 2026-10-06)

- Brian Contact is "the only agent that messages Brian" ("one voice"), but Coordinator and Research and Code Review are told to post on BRI-2 directly, and the C: drive guard posts there under Brian's own login.
- Brian Contact (and Coordinator's line on `Decision:` tasks) still say "do not publish to Telegram — he answers in his Claude Code terminal" (2026-10-02), which Brian's 2026-10-03 rule above superseded.
- Brian Contact says to ask with an `ask_user_questions` card, and in another section "do not use question cards for him".
- Coordinator's goal line says work is "reviewed by him in his terminal, then merged", superseded by the 2026-10-04 merge rule.
- No message carries a label, so on 2026-10-06 the Coordinator treated the disk alert's question to Brian as one it could answer.
