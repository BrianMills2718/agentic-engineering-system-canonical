# Shared worktree lifecycle model

Scope: the existing EP/PM worktree control, a partial shared model rather than the full architectures of either repository. Git, claims and closeout retain their existing owners.

| Element | Kind / owner / representation | Required trace observation |
|---|---|---|
| Repository | Entity / PM graph, Git common directory | Canonical graph identity and actual common directory resolve to the same repo |
| Worktree | Entity / Git porcelain record | Exact path, HEAD, branch/detached, locked/missing state and before/after membership |
| Claim | Record / EP ClaimRecord | Native ID, owner, scope, freshness and target identity; competing update invalidates stale preflight |
| RuntimeDependency | Relationship / process and service configuration | Actual cwd/open files and configured paths, or explicit inspection failure; dependency prevents closure |
| DispositionReceipt | Record / EP closeout and recovery proof | Target, reason, remote readback/archive verification, mutation steps and final folder/claim state |
| SweepResult | Record / PM output and exit | Every repository outcome, retained/error distinction, child exits, totals and appropriate overall failure |
| Create admission | Process / EP creator and Make target | Resolved target checked before mutation; valid folder and claim together; refused target leaves neither |
| Discover | Process / PM graph plus Git enumeration | Exact standard, sibling-only, detached, missing and fixture members appear once |
| Preflight | Process / EP lifecycle owner | Fresh recovery, work, claim and dependency evidence leads to specified retain/close result |
| Close/reconcile | Process / EP session-close and safe remover | Recovery precedes removal; interrupted operations retry without false closure or data loss |
| Report | Process / PM sweep and existing concern | Partial error reaches output, exit and concern; deliberate retention stays visible |
| Inventory view | View / existing PM worktree/status surface | Every member exposes owner, evidence, disposition and next event; unknowns remain visible |

Relationships: Repository registers Worktree; Claim owns a lane at Worktree; RuntimeDependency requires Worktree; Preflight reads those identities plus recovery evidence; Close produces DispositionReceipt; Discover and Report produce Inventory view and SweepResult. PM invokes EP closeout instead of independently releasing managed claims.

Trace mapping: `placement-regressions` covers Repository, Worktree, Claim and Create admission; `inventory-regressions` covers Discover and Inventory view; `preservation-regressions` covers RuntimeDependency and Preflight; `closeout-regressions` covers DispositionReceipt and Close/reconcile; `sweep-failure-regressions` covers SweepResult and Report. `workspace-canary` connects these identities through the authentic lifecycle, while the service sentinel remains retained.

## Entry point, views and freshness

AES `wiki/index.md` remains the repository documentation entry point; the proposal index must link this partial model directly within two links. PM's own wiki entry point routes to the existing worktree/status surface. This model is discoverable there by its plan authority link, not a substitute whole-repository architecture.

The existing review page is a proposed lifecycle sequence sourced from this model; it omits live membership and dispositions because no runtime inventory is bound to it. PM's existing inventory/status view projects Git registrations joined to native claims and receipts; it must expose unavailable and partial states. Full EP/PM system architecture is outside this repair's partial model; no missing architecture is fabricated.

Before each slice, compare source/module revisions, canonical Git common directories, native claim identities and timer entrypoint with the model's named owners and contracts. Compare exact porcelain members with the inventory view and link each changed model element to its named acceptance run. A new producer, consumer, entity or close state without a mapped source, view and trace is model drift and blocks that slice's promotion. The source commit that changes such an element must update this model, affected view coverage and evidence links in the same change. All six named runs are planned; their later results are reported as observed only after full trace inspection. A successful source test cannot silently close missing installed evidence.
