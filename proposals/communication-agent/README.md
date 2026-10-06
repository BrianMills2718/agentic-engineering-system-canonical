# Communication agent: first slice (shaping)

**Question for Brian:** is this the right first step toward the hive-brain communication agent, and does the phone card feel right?

Review page: `review-page/communication-agent.html`, served at
https://hive.brianmills.dev/plans/ from branch `shaping/communication-agent`.

## The slice

When any agent is waiting (a hive worker in Paperclip, or a local Claude Code / Codex session in Agent Deck):

1. Jev triage (exists, `llm_client.call_decisions`) asks whether it is stuck on Brian or just done.
2. A **communication agent (new)** reads its recent work and writes one decision request: the question, the real options, one line of context each.
3. The **Representation Router (extended)** picks the form: choice buttons, a small picture, or plain text when text is clearest (Brian, 2026-10-03 and 2026-10-06: "text is often the best format but often not").
4. The **hive dashboard (extended)** shows it as a card and alerts his phone through the Telegram relay.
5. Brian taps or speaks an answer; the **reply route (extended)** sends it into the exact agent that asked (Paperclip task thread or `agent-deck session send`).

Source design: ai-astronauts `brian/HIVE-BRAIN-ARCHITECTURE.md` (communication agent and dashboard), glossary "Communicating responsibility", requirement R4.

## Open before building

- Where the communication agent runs: a Paperclip worker replacing "Brian Contact", or a small local service.
- The router call it needs: one decision request in, one form plus reason out.

## Status

Shaping only: diagram and clickable mock, no code. Built and checked 2026-10-06 (`review-page/communication-agent.disposition.json`).
