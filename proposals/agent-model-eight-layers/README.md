# Agent model on the eight layers

Status: shaping (2026-10-12). Proposed only; not accepted.

**Question for Brian:** does the review page's right-hand column match the formal work already done in
epistemic-warrant? If a layer is missing something, name it.

**Review page:** [`review-page/agent-model-eight-layers.html`](review-page/agent-model-eight-layers.html), served at
hive.brianmills.dev/plans/ from the `shaping/agent-model-eight-layers` branch.

## What it shows

The o2a agent model (`observation-to-action-metamodel` `formal/SPEC.md`) placed against the eight layers of
epistemic-warrant's canonical factorization (metamodel §5): formal representation, candidate generation, support,
argument and defeat, warrant, licence, epistemic action and update, strategy and control. For each layer: which
agent-model sections touch it, and which epistemic-warrant decisions, documents and code already work it out,
marked used, partly used, not used, rebuilt locally, or conflicting.

At the pinned revisions (epistemic-warrant `9ca2c95e`, o2a `b58b6e1b`): 20 of 31 worked-out items are not used,
two warrant regimes are rebuilt locally (decisions 011 and 012), and the agent model's stakes-bar acceptance rule
conflicts with decision 010.

## Next

1. Brian confirms or corrects the mapping.
2. One company-planning plan rewrites `formal/SPEC.md` on the eight layers, adopting epistemic-warrant's interface,
   regimes and transition calculus; adds a decision-intake ledger with a gate so upstream decisions must each be
   marked used, not yet, or rejected; corrects the vision catch-up page; redraws the agent-model diagram.

## Files

- `review-page/layers.json` — the mapping data (edit this, then run `python3 review-page/build_page.py`).
- `review-page/build_page.py` — builds the page; fails if any agent-model section is in no layer.
- `review-page/*.usecase.json`, `*.recommendation.json`, `*.disposition.json` — Representation Router records.
- `review-page/*-1440.png`, `*-390.png` — rendered screenshots.
