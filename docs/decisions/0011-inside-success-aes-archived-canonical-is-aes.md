---
doc_role: active_authority
authority: canonical_if_merged
status: accepted
accepted_by: Brian Mills (2026-09-26, in conversation: "ok i agree with that ... archive the non canonical version")
date: 2026-09-26
reversible: true
amends:
  - docs/decisions/0001-canonical-convergence-boundary.md (item 3: the Inside Success repository moves from live capability source to archived capability source)
---

# Decision 0011 - This repository is the Agentic Engineering System; `Inside-Success/agentic-engineering-system` is archived

## Context

On 2026-09-26 four authority surfaces disagreed about which repository owns
the AES frontier: `project-meta/AGENTS.md` called this repository's
relationship to `Inside-Success/agentic-engineering-system` "an open question
for Brian"; the Inside Success weekly plan kept the team rollout on the old
repository and called this one "longer-horizon"; the old repository's roadmap
said its Plan 16 "owns the AES architecture-completion frontier"; and this
repository's roadmap recorded Brian's 2026-09-25 rule "AES canonical is the
goal".

State at the decision:

| | `Inside-Success/agentic-engineering-system` | this repository |
| --- | --- | --- |
| last commit | 2026-09-16 | 2026-09-25 |
| frontier | Plan 16 S0 (absorb Company Planning and Enforced Planning into one runtime), not delivered; branch `plan-16-unified-aes-runtime` 12 commits ahead of `main`, unmerged | Decision 0010: v0.2 accepted, `aes status` 9 supported / 0 insufficient / 0 refuted at `84bca46` |
| open PRs | 5 (#114, #122, #126, #158, #160; 2026-09-07 to 09-10) | 2 from the v0.1 line (#30, #32) |
| `docs/` | 96 files, 1.7 MB | 24 files, 234 KB |

Neither repository has shown that governing a project with AES improves an
outcome (old roadmap, "Gate 3 attribution gap"; Decision 0010, "Explicit
non-claims"). Plan 16's target, absorbing Company Planning and Enforced
Planning, is the work v0.2 already re-derived from a clean sheet.

## Decision

1. **This repository is the Agentic Engineering System.** Every ecosystem
   surface that names "AES" names it. Project Meta's "two routes, one
   outcome" statement now pairs Project Meta with this repository.
2. **`Inside-Success/agentic-engineering-system` is archived** on GitHub
   (read-only, still clonable and pip-installable at any pinned commit) and
   recorded `archived` in `project-meta/PROJECT_GRAPH.json` with
   `superseded_by` this repository. Its local checkout is not moved (Project
   Organization Policy: lifecycle changes do not move checkouts). Its five open
   PRs are closed with a pointer here; `plan-16-unified-aes-runtime` stays as a
   pushed branch. Plan 16 is not continued anywhere.
3. **Borrowable ideas are harvested, not ported.** The harvest is
   `research/synthesis/2026-09-26-inside-success-aes-harvest.md`. Each item
   carries the consumer trigger under which it would enter v0.2 through the
   donor re-entry rule (`proposals/aes-v0.2-greenfield/05-donor-reentry.md`)
   and `aes plan`. Nothing in the harvest is adopted by this decision.
4. **The Inside Success team rollout is paused**, not re-targeted yet. What a
   teammate could install from the old repository was one control (the
   assertion evidence gate, Claude Code only). The rollout resumes against
   this repository once whygame5 has produced its first result under AES
   governance (item 5).
5. **Next frontier is an outcome, not a mechanism:** whygame5 realizes
   `PLAN-WG5-RUNNER` and produces the result its README promises. During that
   work one pre-registered value measure is kept (see
   `docs/plans/README.md` entry for the whygame5 value probe once written):
   every time an agent reports done while `aes status` shows drift, an orphan
   or an INSUFFICIENT criterion, and every hand check a person still needed.
   No new v0.2 component is planned until that record exists.

## Consequences

- `README.md`, `wiki/index.md` and `.agentic/repo.yaml` here name this
  decision. `project-meta/AGENTS.md`, `project-meta/README.md`,
  `project-meta/PROJECT_GRAPH.json`, both weekly plans, and the old
  repository's `README.md`/`ROADMAP.md` are updated in the same change set.
- The old repository's evidence (Gates 1 to 2, Plans 8 to 15 receipts) stays
  citable at its pinned commits. Consumers that pinned it (whygame-reboot,
  static-pipeline-reboot, agent-ecology reboots) keep working; none is
  migrated by this decision.
- The two v0.1-line PRs here (#30, #32, Plan 002 offline replay) are closed as
  superseded; Plan 002's question re-enters only through the harvest trigger.

## Wrong when

- a teammate or consumer needs something only the old repository provides and
  the harvest has no trigger for it (then the harvest was too selective, and
  the item is planned through `aes plan`, not by reviving the old repository);
- the next three months of work here are again mechanism phases with no
  consumer outcome recorded, which is the pattern that stalled the old
  repository after 2026-08-24;
- whygame5's runner ships and the value record shows zero AES catches and
  zero saved hand checks (then AES is overhead on that consumer and the next
  decision is about scope, not more mechanism).
