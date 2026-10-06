# What goes to Brian

Status: proposed (hive-hardening plan, unit U1). One rule for every agent and script, replacing the Brian-facing sections now scattered across the workspace `AGENTS.md`, Claude memory, the hive roadmap and the three Paperclip agents' instructions, which contradict each other (listed at the end).

Every message to Brian carries one of two labels. Only a `needs-reply` message accepts an answer, and only an answer that really comes from Brian (his Telegram account or his dashboard login) counts.

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

## fyi: reaches him, no reply expected

- **Finished:** something he asked for is done, with where to look.
- **Stopped or stuck,** when no agent can unstick it, after the agent that owns it has tried.
- **A rule changed** that he set.

One plain sentence, once per change of state. Not: progress, routine failures (those go to an agent first, which fixes them; Brian, 2026-10-06), agent-to-agent traffic, "still waiting".

## How it is delivered

- At the moment it happens, on his Telegram thread (board BRI-2) and in the terminal session if one is open. (2026-10-03: "i want to know as soon as my agents try to send me a message and for them to get my response as soon as i respond.")
- Scripts post as the alert bot, never as Brian.
- No agent replies on a `needs-reply` message. An agent that acts on a reply checks its author first.

## Contradictions this replaces (found 2026-10-06)

- Brian Contact is "the only agent that messages Brian" ("one voice"), but Coordinator and Research and Code Review are told to post on BRI-2 directly, and the C: drive guard posts there under Brian's own login.
- Brian Contact (and Coordinator's line on `Decision:` tasks) still say "do not publish to Telegram — he answers in his Claude Code terminal" (2026-10-02), which Brian's 2026-10-03 rule above superseded.
- Brian Contact says to ask with an `ask_user_questions` card, and in another section "do not use question cards for him".
- Coordinator's goal line says work is "reviewed by him in his terminal, then merged", superseded by the 2026-10-04 merge rule.
- No message carries a label, so on 2026-10-06 the Coordinator treated the disk alert's question to Brian as one it could answer.
