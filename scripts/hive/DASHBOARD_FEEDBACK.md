# Hive dashboard: Brian's critiques (living log)

Every critique Brian gives on the hive-brain dashboard goes here in the same
turn: a rule row (his words, date, the router heuristic it maps to) and a dated
log row. Rules that apply beyond this page go into Representation Router
(`catalog/composition-heuristics.json`), per his 2026-10-03 rule.

## Rules

| Rule | Brian's words | Date | Router heuristic |
|---|---|---|---|
| Show each question in the form that answers it, not the same cards on every screen | "it doesnt seem like you captured the idea of stuff disucssed in the ai asotrnuats thing and represntaiton router of communciating through the optimal represantion" | 2026-10-03 | `form-matches-job` (existed; broken by v1) |
| Pictures first; text only where it is the best form | "i feel like it is still text based which is the main thing i am trying to get away from. text is often the best fromat but oftne not." | 2026-10-03 | `picture-before-prose` (added, router PR #50) |
| Answer from the page, in real time | "i want an actual real time communication system because i want to know as soon as my agents try to send me a message and for them to get my response as soon as i respond" | 2026-10-03 | n/a (function, not representation) |
| Phone first | "my goal is to move more or and more to my phone and off my computer" | 2026-10-03 | `whole-on-one-screen` at a phone viewport |

## Log

| Date | Version | Critique | What changed |
|---|---|---|---|
| 2026-10-03 | v1 (single list page) | "ok this is nto wha ti want" | Sketches requested from ChatGPT |
| 2026-10-03 | sketch prompt | the mockup "doesnt seem like you captured ... communciating through the optimal represantion" | Prompt rewritten around one form per question; v2 built from it |
| 2026-10-03 | v2 (five screens, hosted) | "it ist ill just text based" | `picture-before-prose` added to the router; Path, Live and Health redrawn as pictures (v3) |
