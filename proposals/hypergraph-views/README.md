---
plan_id: hypergraph-views
status: shaping
selected_path: coordinated
planning_path_decision: proposals/hypergraph-views/planning-path-decision.json
review_page: proposals/hypergraph-views/review-page/hypergraph-views-plan.html
goal:
  outcome: any project whose facts join more than two things in named roles is drawn without breaking them into pairs, through the shared graph viewer and the Representation Router; the DoDAF demo shows its model and the whole DM2 metamodel that way, and a reader or the agent can build a custom view from a checked recipe
  canonical_example: the DoDAF fact "Matthew Perry transferred 45 pallets to Shiloh on 23 March near Hachinohe" is one hub with spokes to Matthew Perry, Shiloh, the pallets, Hachinohe and 23 March, so it connects to the Hachinohe port clearance; the whole DoDAF model drawn that way is 2 connected pieces or fewer, not 7
  forbidden_substitutes: a hand-rolled per-project viewer; a picture that draws hubs but drops place or date into edge notes; a custom view labelled with a standard DoDAF code; a recipe drawn without checking it against the model's types
  boundaries: shared viewer changes are additive to typed-graph/v1 (existing graphs render unchanged); DoDAF model changes only promote place, date and quantity that the cited passages already state; the DoDAF repository stays parked apart from the demo
  done_when: 'the shared viewer renders a typed-graph with hyperedges as hubs with role-labelled spokes (tests and a browser check); the router routes a hypergraph use case to relation-hub-graph and applies keep-n-ary-relations-whole (tests); the live DoDAF demo has a whole-model hub view whose piece count is measured and stated, a DM2 metamodel hub view built from onto-canon6''s dm2_complete pack, and an agent that answers a question with a recipe-built view labelled custom (live checks)'
  do_not_gate_on: Brian's review of the plan page; migrating other projects (scientific-hypergraph, onto-canon6) onto the shared viewer
  owner: claude-code session dd8590c4
---

# Hypergraph views: draw n-ary facts whole, everywhere

## Who it serves, the result, one example

**Actor:** Brian, readers of his public demos, and every agent that builds a graph view for one
of his projects.

**Result:** facts that join several things in named roles (who did what, to what, where, when,
from which source) are drawn as one mark with labelled spokes instead of being split into pairs.
The graph then stays connected where the facts connect.

**Example (measured 2026-10-07 on the DoDAF demo's published model, 131 relations):**

| Drawing | Disconnected pieces |
|---|---:|
| pairs (today) | 7 |
| one hub per relation, role spokes | 3 |
| hub plus a place participant | 2 (the remaining piece is the Sendai effort) |

## Brian's direction

- 2026-10-07: "i think we kind of do need n-ary role typed because the binary edges are causing what
  should be a unified graph to be broken up into isolated subgraphs"; "i was kind of expecting
  something more like what i have for scientific hypergraph repo".
- 2026-10-07: "on the interactive part i was thinking maybe like the user/ai could build views in
  real time?"; "this will probably be ai powered where the user asks questions and the ai delivers
  views for basic users".
- 2026-10-07: "ok can you see if represnetation router should be updated for general proejcts that
  need these capabiltiies" then "i approve".

## What exists, and what this plan does with it

| Existing piece | Where | Disposition |
|---|---|---|
| Hub layout: relation instance as a box with role-labelled spokes, layered columns | scientific-hypergraph `wiki/reference/metamodel/hypergraph-viewer-*.js` | **reuse the approach** inside the shared viewer; not a second viewer |
| Shared graph viewer (React Flow + ELK, typed-graph/v1: nodes, edges) | representation-router `graph-viewer/` | **extend**: add `hyperedges` (type, roles to node ids), drawn as hubs |
| Role-typed assertions (`roles: {role: [fillers]}`; 5 of 131 already have three roles) | dodaf semantic IR and surface payload | **reuse**; promote place, date and quantity from annotations to role fillers |
| DM2 2.02 as data: 193 entity types, 86 relation types, 173 roles with expected types, 204 subtype links | onto-canon6 `ontology_packs/dm2_complete/2.2.0/` | **reuse** as the metamodel hub view's input |
| View recipes (selection, grouping, shape) as a registry | dodaf `semantic_authority/projections.py` | **reuse** the shape for recipe-built views |
| Router catalog: 26 representations, none for hypergraphs | representation-router `catalog/` | **extend**: relation-hub-graph, paoh-hypergraph, upset-plot; hypergraph structure; three heuristics; recipe-built-views pattern (ready as a tested patch) |

**What was searched:** the two repositories above for hub and hypergraph rendering; the router catalog
for hypergraph, hyperedge, n-ary, incidence and bipartite entries (none); published methods:
Fischer et al. (2021, IEEE VIS, survey of hypergraph visualizations), Valdivia et al. (2021, IEEE
TVCG, PAOH), Lex et al. (2014, IEEE TVCG, UpSet), Shen et al. (2021, IEEE TVCG, natural-language
interfaces to visualization). Disposition: adopt these established forms; build only the hub
support the shared viewer lacks.

## Work units

| ID | Change | Where | Done when |
|---|---|---|---|
| H1 | Router catalog: hypergraph structure, three representations, three heuristics, recipe-built-views pattern | representation-router | router tests pass; a hypergraph use case routes to relation-hub-graph and lists keep-n-ary-relations-whole |
| H2 | Shared viewer draws `hyperedges` as hubs with role-labelled spokes; additive to typed-graph/v1 | representation-router `graph-viewer/` | existing graphs render unchanged (tests); a fixture with a three-role fact renders one hub and three labelled spokes in a real browser |
| H3 | DoDAF: place, date and quantity become role participants; whole-model hub view in the demo | dodaf | the published model has those participants; the live view states its piece count (target: 2 or fewer); release audited and recorded |
| H4 | DM2 metamodel hub view from onto-canon6's pack | dodaf demo (data from onto-canon6) | the live view shows the 86 relation types as hubs with their 173 typed roles, searchable |
| H5 | Recipe-built views: the agent answers a question with a view recipe, checked against the model's types, drawn, labelled custom | dodaf demo and its worker | three live questions each produce a checked custom view; an invalid recipe is refused with its reason |

Order: H1 and H2 first (they serve every project), then H3, H4, H5. Each lands and is checked on its own.

## Uncertainties

| Uncertainty | Evidence that resolves it |
|---|---|
| Whether a date participant joins the Sendai piece | H3's measured piece count with and without dates |
| Whether hubs stay readable at DM2's size (86 hubs, 193 types) | H4 in a real browser at 1440px and 390px; fall back to PAOH or a filtered start if not |
| How much the agent's recipes need constraining | H5's refused-recipe count over its live checks |

## Irreversible actions and spend

None irreversible: commits, an additive format change and redeploys of Brian's own demo, each
revertable. LLM spend is the demo agent's existing route (about $0.001 a question).
