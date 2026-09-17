# Human-observable delivery and attention economics

Status: accepted AES delivery constraint.

This document defines how canonical AES applies Company Planning, Representation Router lessons, and execution economics to project delivery. It is AES-specific: generic planning methodology remains owned by Company Planning and project-agnostic architecture remains owned by `wiki_methodology`. Friction discovered here should be proposed upstream rather than silently creating a second planning method.

## 1. Optimize for useful observation, not implementation inventory

AES should minimize the amount of speculative implementation that accumulates before the intended stakeholder can directly use enough of the system to judge whether the direction has value.

The relevant progress signal is not merely:

```text
commits
passing tests
backend completeness
closed tasks
```

It is:

```text
time / cost until the intended actor can say:
"I can use this enough to know whether I want more of it."
```

Call this **utility-discovery latency**. A technically productive project can still be badly sequenced when utility-discovery latency is high.

## 2. Default implementation-slice shape

An implementation slice should normally leave the intended actor with a small but authentic version of the accepted capability if work stops immediately afterward.

```text
accepted outcome
    ↓
implementation slice
    ↓
authentic human-usable surface
    ↓
direct use + engineering review
    ↓
observed utility / defect / uncertainty
    ↓
next slice or replan
```

"Human-usable surface" is intentionally broad. It may be:

- web or desktop UI;
- CLI;
- notebook;
- IDE interaction;
- API client or explorer;
- operator console;
- interactive report;
- rendered artifact;
- another authentic developer/user interaction boundary.

The requirement is not graphical polish. The requirement is that the actor can exercise and judge the real capability without first reconstructing it from code, tests, logs, plans, or agent dialogue.

**UI-first is therefore shorthand for actor-surface-first, not GUI-first.** Do not manufacture a graphical shell for a library, service, infrastructure capability, or developer tool when its authentic human boundary is another form. Conversely, do not use the existence of a CLI, JSON artifact, or test harness to claim human observability when the intended reviewer still has to mentally reconstruct the experience.

### Non-slice critical-path work

Not every necessary increment can produce standalone user value. Classify such work honestly:

- `boundary_probe` — resolves an architectural/integration uncertainty;
- `dependency_resolution` — answers a fact needed to freeze a later slice;
- `enabler` — supplies necessary infrastructure/capability with no standalone actor outcome;
- `regression_or_hardening` — protects already-visible behavior against an observed failure family.

Each such increment names the outcome-bearing slice it unlocks or protects. A plan containing many "slices" that are really infrastructure chores has lost the vertical boundary.

## 3. Design backward, implement forward

When the final interaction model is sufficiently knowable, maintain a **north-star experience** and derive earlier usable states backward from it.

```text
north-star experience
        ↑ reason backward
later usable slice
        ↑
earlier usable slice
        ↑
first authentic usable vertical

then implement forward:

Slice 1 -> Slice 2 -> Slice 3 -> north-star experience
```

Earlier surfaces should preferably preserve the same actor, job, semantic identity, major state transitions, and mental model while exposing less capability. Temporary scaffolding is acceptable when it has an explicit retirement trigger.

The north star may be a detailed UI when evidence supports that detail, or only an **interaction contract**:

- actor and recurring job;
- starting state;
- primary actions;
- information needed at each decision;
- important state transitions;
- failure/recovery behavior;
- progressive disclosure;
- authority boundaries;
- completion experience.

A north-star experience is a steering model, not an accepted implementation specification merely because it is vivid. It must remain revisable when stakeholder observation, feasibility evidence, or provider constraints invalidate its assumptions.

## 4. Maturity and epistemic certainty determine design depth

Delivery ambition and certainty are separate axes.

Delivery maturity may be `prototype | pilot | internal_product | external_release` or the current Company Planning equivalent. Epistemic certainty concerns how well the actor, job, interaction model, feasibility assumptions, and quality bar are actually known.

Use the following as heuristics, not a scoring formula:

| Situation | Planning behavior |
| --- | --- |
| high maturity + high experience certainty | design the north-star interaction substantially up front and slice backward aggressively |
| high maturity + medium certainty | fix jobs, states, major interactions, and high-fan-out boundaries; leave visual/detail choices flexible |
| prototype + high certainty | build a thin faithful subset of the known final experience |
| prototype + low product certainty | reach the cheapest authentic usable surface quickly and learn what the final experience should be |
| low technical certainty | run the narrowest feasibility probe that protects the next usable vertical, then return to that vertical |
| low product + low technical certainty | use a very small authentic experiment; avoid broad backend/platform commitments |

Distance from implementation is not itself a reason to stay vague. Conversely, imagined detail whose correctness depends on an unobserved upstream result is false precision.

## 5. Frontend ambition and backend feasibility co-design each other

The desired experience can reveal what the backend must make possible. Planning should work backward from that experience and identify **load-bearing feasibility assumptions** such as:

- latency;
- throughput or scale;
- data availability/quality;
- model capability;
- contract/API feasibility;
- provider behavior;
- persistence/state requirements;
- security or authority boundaries when actually activated;
- cost per interaction;
- integration fan-out.

Do not respond to uncertainty by building the whole backend first. Use the cheapest discriminating probe that preserves the phenomenon the final experience depends on.

Example:

```text
north-star:
whole-repository analysis in an interactive review surface

uncertain assumption:
required repository reasoning is affordable and sufficiently accurate

probe:
one authentic concern on one real repository

then:
return immediately to a usable vertical
```

A probe is justified when the expected rework or lock-in it protects exceeds the cost of learning earlier. A probe that grows into a generalized subsystem without returning to a human-observable outcome is planning drift.

## 6. Human attention is scarce planning capital

AES distinguishes at least these economic quantities conceptually:

- stakeholder/human attention;
- AI/model/tool spend;
- elapsed time;
- expected rework and architectural lock-in;
- opportunity cost of occupying an active project slot;
- expected outcome value;
- value of information from the next observation.

These need not be assigned fake precise numbers. Strong agents should make contextual decisions from the accepted outcome, constraints, uncertainty, and current evidence.

A useful qualitative comparison for a candidate next increment is:

```text
expected stakeholder value
+ value of information
+ options unlocked
+ material risk retired

versus

human attention required
+ AI/tool cost
+ elapsed time
+ rework / lock-in exposure
```

Human attention may have a high shadow price. Spending substantially more AI effort can be rational when it reduces human reconstruction work, produces a better decision surface, or reaches useful observation sooner.

But cheap AI can also create **unreviewed inventory**: many projects with weeks of accumulated implementation that all suddenly require expensive human comprehension. AES should not optimize human attention by postponing stakeholder observation until its leverage has disappeared.

## 7. Attention checkpoints are information-value checkpoints

An attention checkpoint is not a routine approval gate.

The agent should normally continue autonomously while the expected value of another reversible in-scope increment exceeds the expected value of direct stakeholder observation.

Surface a human-usable outcome when:

- product usefulness or interaction quality is materially uncertain;
- the next autonomous increment would create substantial rework/lock-in if the direction is wrong;
- a real human preference/judgment is the missing authority;
- the current slice has reached its authentic observation boundary;
- observed evidence materially changes the expected value of continuing;
- portfolio priority may change after seeing the result.

The preferred checkpoint is usually:

```text
"Use this and judge it"
```

not:

```text
"Read these files and reconstruct what I built"
```

Representation/context tooling should prepare the smallest source-bound review surface needed to make that judgment cheap.

A checkpoint disposition such as `continue | change | pause | stop | scale` is planning/utility evidence. It is not, by itself, technical conformance, plan acceptance, deployment approval, or authority to mutate another system.

## 8. Product surface and engineering-review surface are complementary

At the end of a meaningful slice, the stakeholder should normally have access to:

```text
PRODUCT / ACTOR SURFACE
Can I actually use the capability?

+

ENGINEERING REVIEW SURFACE
What was intended?
What changed?
What evidence ran?
What remains unsupported or stale?
Which gaps remain?
What decision, if any, belongs to me?
```

These surfaces may be one coordinated experience or separate artifacts. Neither becomes authority merely by rendering authoritative facts. Representation Router is a relevant donor/provider candidate for making these concern-specific surfaces tractable; Company Planning, Enforced Planning, repositories, policy systems, and other native owners retain their state and effect authority.

The product surface should make **holistic quality** observable where relevant: usefulness, coherence, interaction cost, latency, failure/recovery behavior, trust/legibility, and whether the feature fits the actor's real workflow. Automated evidence usually cannot establish all of these dimensions by itself.

## 9. Utility and conformance are orthogonal

Direct stakeholder use and technical/evidence conformance answer different questions and must remain separately visible.

```text
technical/evidence state      stakeholder utility state
------------------------      -------------------------
conformant                    useful
nonconformant                 promising but not acceptable yet
unknown / stale / error       useful-looking but unproven
conformant                    low-value / wrong direction
```

Consequences:

- automated green cannot override a stakeholder observation that the capability is low-value or badly shaped;
- stakeholder enthusiasm cannot convert missing, failed, stale, or insufficient required evidence into conformance;
- a low-utility but technically conformant result is planning evidence for `change | pause | stop`, not merely a polish backlog;
- a high-utility but nonconformant result may justify repair or another slice, but not a false closure claim.

The system should preserve both dimensions through review, gap reconciliation, and continuation decisions.

## 10. Portfolio economics

When a portfolio authority exists, project scheduling should compare the **next increments** available across projects rather than rewarding local completion percentages.

Useful signals include:

- expected project/outcome value;
- product uncertainty;
- technical uncertainty;
- maturity;
- human-attention demand of the next checkpoint;
- AI/tool spend and runtime;
- time until the next useful observation;
- rework/lock-in exposure;
- whether the next increment produces value, information, or only inventory.

A project-local AES executor does not invent portfolio priority. It should expose enough evidence for a portfolio authority to choose `continue | change | pause | stop | scale`.

Stopping or killing a project can be a high-value outcome when a cheap vertical plus brief human use reveals that the project is not worth further investment.

## 11. Learning from late-utility failures

A stakeholder reaction such as "this is technically complete but useless" is not merely a UI defect. It may indicate:

- the actor/job was misunderstood;
- utility was observed too late;
- slices were horizontal rather than outcome-bearing;
- the north-star experience was missing or wrong;
- backend work accumulated before product uncertainty was retired;
- human attention was saved locally but spent catastrophically at the end;
- agent review optimized internal consistency rather than stakeholder value.

Record and disposition that failure family so future planning shortens the stakeholder-observation interval for similar uncertainty.

## 12. Operating principle

> **Use AI autonomy to multiply human judgment, not to postpone human judgment until after its leverage has disappeared.**

The practical consequence is contextual rather than formulaic: design to the level justified by maturity and certainty, spend automation where it buys value or information cheaply, surface authentic usable outcomes early enough for high-leverage human judgment, and let observed utility reshape the plan.
