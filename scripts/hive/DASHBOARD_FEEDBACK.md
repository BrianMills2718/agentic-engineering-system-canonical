# Hive dashboard and planning visuals: Brian's critiques (living log)

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
| A diagram must show what a list cannot; a linear loop is a numbered list with "repeat" | "in this case the graph adss almsot nothign over a list with reapt at the end" | 2026-10-04 | `diagram-earns-its-space` (proposed; `structure-earned-not-imposed` covers tabs, not drawings) |
| Use diagrams with real semantics: port graphs (Zapier-style typed inputs and outputs), UML, and dynamic visualizations | "the port grpahs that are used in things like zapier are very helpful and uml diagrams and dynamic visualzaitons like ahve int he ai austronatus aritact and in my protfolio" | 2026-10-04 | router lacks `port-graph` and UML class/component representations (to add) |
| Planning requires generated static diagrams plus custom dynamic ones | "we can not only have requried satic uml type dagrams as aprt of company plannign that are requried and automatically genrated but also more custom dyanmic visualziations" | 2026-10-04 | AES plan gate (to build) |
| Phone first | "my goal is to move more or and more to my phone and off my computer" | 2026-10-03 | `whole-on-one-screen` at a phone viewport |
| Every box on the map opens its subject | "clicking on the brains doesnt show me anythgin or take me anywhere like i would want" | 2026-10-04 | `every-mark-opens-its-subject` (added, router PR #55) |
| Tooltips everywhere: every label explains itself (hover on a laptop, tap on a phone) | "i click it and it tells me nothign. ther should be tool tips everywehre" | 2026-10-04 | `every-label-explains-itself` (added, router PR #55) |
| A laptop gets a laptop layout | "it should detect when i am on my lptop and give me a laptop layout" | 2026-10-04 | `layout-fits-the-device` (added, router PR #55) |
| The page reloads itself | "why doesnt he page reload automatically?" | 2026-10-04 | `live-surface-refreshes-itself` (added, router PR #55) |

## Log

| Date | Version | Critique | What changed |
|---|---|---|---|
| 2026-10-03 | v1 (single list page) | "ok this is nto wha ti want" | Sketches requested from ChatGPT |
| 2026-10-03 | sketch prompt | the mockup "doesnt seem like you captured ... communciating through the optimal represantion" | Prompt rewritten around one form per question; v2 built from it |
| 2026-10-03 | v2 (five screens, hosted) | "it ist ill just text based" | `picture-before-prose` added to the router; Path, Live and Health redrawn as pictures (v3) |
| 2026-10-04 | plan-and-review loop diagram | "the graph adss almsot nothign over a list with reapt at the end" | Logged; diagram types with semantics (port graphs, UML) to be added to the router; generated diagrams become part of the AES plan gate |
| 2026-10-04 | v3 (hosted, five screens) | project cards "brain fresh" open nothing; no tooltips; no automatic reload; phone column on a laptop | AES #136: every map box opens a panel (project cards show the brain's now.md and links to its files), tooltips on hover and tap, self-reload except while typing, laptop columns, no cut-off text, VPS rebuild every minute. Four router heuristics added (router PR #55) |
