---
schema_version: "1.0"
artifact_type: design_plan
id: doc-reach-new-docs
status: proposed
method_conformance_receipt: proposals/doc-reach-new-docs/PLAN.receipt.json
goal:
  outcome: "In Brian's repositories, a commit that adds a document a reader is meant to open is refused unless wiki/index.md reaches it within two links, and the refusal names the exact link line to add; documents that already exist are left to the per-repository cleanup."
  canonical_example: "An agent commits docs/notes/why-agents.md to graph-retrieval with no link to it; the commit is refused with: add '- [why-agents](../docs/notes/why-agents.md)' to wiki/index.md. With that line added in the same commit, it is accepted."
  forbidden_substitutes: "a check of all documents (old ones too); a daily report standing in for the commit-time check; a generated list of every file appended to the wiki; tests alone without the replay over real commits"
  boundaries: "AES canonical commit rule (src/agentic_engineering_system/commit_rule.py), its tests, this plan folder; repositories owned by BrianMills2718 or brianmills-spec only; [Auto] commits are logged, never refused; switch off with doc_reach: observe in ~/.config/aes/commit_rule.yaml"
  done_when: "the replay over every commit since 2026-10-07 that added .md files (proposals/doc-reach-new-docs/replay.py, output replay-after.txt) shows the commit rule's verdict matching the daily check's reachability for each added file, read commit by commit; a real commit in a scratch clone of a Brian-owned repository is refused for an unlinked new document and accepted once the printed line is added, with both commit-msg outputs saved in check.txt; make check passes"
  do_not_gate_on: "Brian's review of this plan; the per-repository cleanup of existing documents (aes-brownfield-docs M4)"
---

# New documents are linked from the wiki when they are committed

## Actor and result

> **CORE-ACTOR-RESULT-EXAMPLE** (blocking): The plan names the actor it serves, the desired result, and one stable, concrete, user-visible example of that result.

**Actor:** every agent (and Brian) who commits a new document in one of Brian's repositories, and the next reader who looks for it.

**Request (verbatim):** Brian, 2026-10-08: "cant we just do it for new docuemtnts while we work on getting the rest of the repos aligned" (the rule being: every reader document reachable from `wiki/index.md` within two links).

**Result:** a commit that adds a reader document the wiki does not reach is refused with the exact line to add; once added, it passes. Existing documents are not checked.

**Stable example:** in graph-retrieval, committing `docs/notes/why-agents.md` alone is refused with "add `- [why-agents](../docs/notes/why-agents.md)` to wiki/index.md"; the same commit with that line in `wiki/index.md` is accepted.

## Success and disproof

> **CORE-SUCCESS-DISPROOF** (blocking): The plan defines the evidence that would show success and a concrete condition that would disprove the approach.

> **CORE-TRACE-REVIEW** (blocking): Every success or acceptance criterion in the plan is judged from the full trace of a run, not only its final outcome: it names the run whose full trace is examined (for example the session, its tool and LLM calls, commits, check output, or messages), where that trace lives, and what must be seen in that trace beyond the final outcome. A criterion that names only an outcome, such as tests passing, a PR merged, a test fixture reproducing the journey, or a status reading succeeded, fails this item. A criterion for which no run exists, such as a pure document edit, passes only when the plan states that exemption and its reason explicitly.

**Success evidence:** (1) the replay over every commit since 2026-10-07 that added `.md` files in Brian's repositories (78 commits on 2026-10-08) gives, for each added file, the same reachable/unreachable answer from the commit rule as from the daily check (`project-meta/scripts/md_file_cap.py` reachability at that commit); (2) a real commit in a scratch clone is refused for an unlinked new document and accepted once the printed line is added; (3) `make check` passes.

**Disproof:** the approach is wrong if, in the first enforced day's commit-rule logs, a refused commit's new document was in fact reachable (the rule and the daily check disagree), or if agents answer the refusal by appending unrelated catch-all link lists rather than the printed line (seen by reading the wiki diffs of the next commits in those repositories).

**Trace review:**
- *Replay run* (`proposals/doc-reach-new-docs/replay.py`, output `replay-after.txt` committed here): the full per-commit trace lists each added file with both answers; it is read row by row for disagreements, not only the totals.
- *Scratch-commit run*: the two `git commit` outputs (refusal text, then acceptance) and the commit-rule log lines they write (`.git/aes/commit-rule-<date>.jsonl`, fields `verdict`, `check: doc-reach`, `reasons`) are saved in `check.txt`; the refusal must name the file and the exact link line.
- *make check*: its full output is saved verbatim in `check.txt` (every lint, governance and test step, with the per-test lines of `tests/greenfield/test_commit_rule.py`); it is read for the new doc-reach tests by name passing, for no skipped commit-rule test, and for the final counts and exit status.

## System model

> **CORE-SYSTEM-MODEL** (blocking): The plan links the project's system model (a path such as docs/model/ODD.md) or carries the one-line exemption `System model: `.aes/target.yaml` (AES canonical's model of its own system), element `RU-AES-COMMIT-RULE` ("judge a commit message's tag against facts about the staged change ... log every verdict"). Elements this work changes or relies on, and what the examined runs must show of each:
- *Process* — the commit-msg check (`aes commit check`): the scratch-commit run must show it reading the staged tree (a new document not on any earlier commit is judged).
- *Record* — the commit-rule log line (`.git/aes/commit-rule-<date>.jsonl`): the scratch-commit run must show a line with `check: doc-reach`, `verdict: refuse` and the new file named in `reasons`, then a later line with `verdict: accept`.
- *View* — the refusal message printed to the committer: the scratch-commit run must show it naming the file and the exact link line to add.
- *Relied on* — the daily check's reachability rule (project-meta `scripts/md_file_cap.py`): the replay run must show its answer beside the commit rule's for every added file.

## Authority and non-goals

> **CORE-AUTHORITY-NONGOALS** (blocking): The plan states who holds authority over the work and what it explicitly will not do (non-goals).

**Authority:** Brian, 2026-10-08 (quoted above), in his own repositories. AES canonical owns the commit rule; this session (code-83) is its writer.

**Non-goals:** no check of documents that already exist; no change to which documents count as reader documents (the daily check's rules are reused as they are, including `.md-file-cap.yaml` `unlinked_ok`); no repositories owned by others (Inside-Success and other owners are skipped); no automatic editing of anyone's wiki; [Auto] scheduled jobs are never refused.

## Irreversible actions and spend

> **CORE-IRREVERSIBLE-SPEND** (blocking): For each irreversible action or spend the plan proposes, it names the boundary, who must authorize it, and how it is contained.

No irreversible action and no spend: a refused commit is simply not made, and `doc_reach: observe` (or a revert) switches the check back to logging only.

## Uncertainties

> **CORE-UNCERTAINTIES** (blocking): The plan lists its material uncertainties, and each one has an owner or the evidence that would resolve it.

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the commit-time answer matches the daily check's on real commits | code-83; resolved by the replay comparison, row by row |
| How much friction it adds: 72 of 78 recent commits that added documents would have been refused | code-83; first enforced day's logs read for repeat refusals and for catch-all link dumps (disproof above) |
| Repositories with no `wiki/index.md` (25 of the 72): the refusal asks for one | code-83; the refusal text says to add `wiki/index.md` with the link, and the logs show whether agents do |

## Activation facts

> **CORE-ACTIVATION-FACTS** (blocking): No activation fact that the plan triggers is declared false. Declaring a fact true when the plan does not strictly need it is acceptable, because it only adds checks; judge only facts declared false. empirical_comparison_proposed is triggered when the plan proposes an A/B test, benchmark, bake-off, or other experiment comparing alternative designs, models, or candidates to choose among them; checking the built result against an expected outcome (an acceptance test, fixture replay, or regression check) is verification and does not trigger it. shared_mechanism is triggered by a new shared mechanism, contract, or algorithm; llm_central by behavior that centrally depends on LLM calls; irreversible_or_spend_action by a proposed irreversible action or spend.

`shared_mechanism` is declared true (the commit rule runs in every repository). `empirical_comparison_proposed` is false: the replay checks the built rule against the daily check's expected answer, which is verification, not a comparison of alternatives. `llm_central` is false: no model call. `irreversible_or_spend_action` is false: nothing irreversible, no spend.

## Prior art and ownership

> **OV-PRIOR-ART-DISPOSITION** (blocking): Existing ownership, internal lineage, and relevant external prior art were searched, and each candidate found is dispositioned as reuse, extend, compose, supersede, or bounded exception.

> **OV-PRIOR-ART-PARALLEL-CHECK** (advisory): The plan names one concrete structural check or consumer-path observation that would detect a silent parallel implementation of the same concern.

- **project-meta `scripts/md_file_cap.py` `reachability()`** (the daily check, same rule): *reuse* its rules (wiki entry, two links, link syntax, exemptions, `unlinked_ok`, generated outputs) by porting them into the commit rule over the staged tree, citing it as the source; the daily check stays the report for existing documents.
- **`aes-brownfield-docs` (AES proposal, another session)**: *compose* — it moves existing repositories into the layout (M4 rollout); this plan only guards new documents, so the two do not overlap.
- **External, each dispositioned:** markdown-link-check — *bounded exception*: it verifies that links resolve, not that a page is reachable from an entry page. lychee — *bounded exception*, same reason. pre-commit (the framework) — *bounded exception*: it needs per-repository installation, while the commit rule already runs as commit-msg in every repository; no hook in its registry checks reachability from an index page.
- **Ownership records searched:** `~/projects/.claude/AUTHORITIES.md` routes documentation and wiki questions to project-meta `docs/ops/DOCUMENTATION_PLANNING_LINKAGE_SYSTEM.md`. Its guardrails (`check_doc_coupling.py` staged source-to-doc coupling, `check_markdown_links.py` link resolution, plan-status sync) run in governed repositories' pre-commit hooks; none checks that a new document is reachable from `wiki/index.md`. Disposition: *compose* — those hooks keep running where installed; this check covers reachability in every Brian-owned repository through the commit rule, which already runs everywhere. project-meta `policy/registry.yaml` holds the `md-file-cap` policy whose daily check this reuses.
- **Search done:** project-meta `wiki/tool_and_capability_index.md` and `scripts/` (found `md_file_cap.py`), AES canonical `proposals/` (found `aes-brownfield-docs`), and the commit rule's own module; no other commit-time documentation check exists.

The replay compares the commit rule's answer with the daily check's for every added file; any disagreement row is a sign the two implementations have drifted apart.

## Coordination

> **OV-COORD-OWNERSHIP** (blocking): The plan names exact ownership, dependencies, conflict surfaces, the integration owner, and the work-unit evidence for each concurrent writer.

- **Owner and integration owner:** code-83 (this session), claim `agentic-engineering-system-canonical:doc-reach-new-docs`, branch `doc-reach-new-docs`.
- **Conflict surfaces:** `src/agentic_engineering_system/commit_rule.py` and `tests/greenfield/test_commit_rule.py`; no other live claim writes them (checked with `check_coordination_claims.py --list`).
- **Dependencies:** the daily check's rules in project-meta (read-only); the hook runtime checkout `worktrees/hook-runtime`, moved to main after merge.
- **Concurrent writers of these files:** only code-83. Work-unit evidence: the claim above and the commits on branch `doc-reach-new-docs`. The one other live AES claim (`plan-in-index`, also code-83) is merged and its worktree removed. The `aes-brownfield-docs` session writes only its own plan folder and the integration repository, not these files; it is told when this lands.
- **Writers affected but not editing:** every agent that commits documents in Brian's repositories; their evidence is each commit's log line (`check: doc-reach`), read on the first enforced day.
