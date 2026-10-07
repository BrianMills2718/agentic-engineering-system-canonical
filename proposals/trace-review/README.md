---
plan_id: trace-review
status: shaping
selected_path: repair
planning_path_decision: proposals/trace-review/planning-path-decision.json
method_conformance_receipt: proposals/trace-review/method-conformance-receipt.json
goal:
  outcome: every AES plan says whether its work runs a model, agent or pipeline, and work that runs is judged by an independent reading of its full trace, not by its final output
  canonical_example: a plan for an interview-coding run that declares trace_review runs_traced_work true but adds no trace_review evidence requirement is refused by aes plan validate; its trace_review observation cannot SUPPORT while 4 of 6 calls are unread or a checked label is wrong
  forbidden_substitutes: a protocol paragraph with no validator; a check that the word "trace" appears in the plan; a review written by the run's own author
  boundaries: AES canonical governed roots only; plans accepted before 2026-10-07 keep loading; no other repository changed in this plan
  done_when: aes plan validate refuses a proposal with no trace_review declaration and one that declares traced work without a trace_review requirement, and accepts the declared and routed case; observation loading refuses a trace_review assessment without a record, SUPPORTS with unread steps or a wrong decision, and an author reviewing their own run (tests with counts); make aes passes
  do_not_gate_on: other repositories adopting the rule; Brian reading this page
  owner: claude-code:vision-review-trace
---

# Plans require trace reviews

## Who it serves, the result, one example

**Actor:** Brian, and every agent planning work in a repository AES governs.

**Result:** a plan cannot be accepted without saying whether its work runs a model, an agent or a pipeline. If it does, the plan must contain a check that someone other than the author reads that run's full trace: what each step was shown, which model and settings it used, every output with its reason, and a sample of decisions followed back to their sources.

**Example (the case that started this, 2026-10-06):** in vision milestone 4, an interview coder (the `qualitative_coding` repository, run 4, trace `qualitative_coding/project/0cbd41e8`) labelled a woman's complaint about a prejudiced supervisor, and another's about heavy boxes, as "no lasting gain in work or earnings". Two rounds of review read the coder's output and amended rules; nobody opened the trace. The trace shows the cause: each passage was coded with one neighbouring line of context, the label's definition had no exclusions, and the model returned bare labels with no reasons. Under this plan the run's plan must carry a `trace_review` requirement, and its observation cannot SUPPORT until all six coding calls are read and the checked labels are right.

## Brian's direction (authority)

- 2026-10-07: "ok the first thing is that we need aes plans to require trace reviews as part of its planning."
- 2026-10-06: "my general principle of maximum observability (although there should be filters/views) and always reviewing full e2e traces of stuff not just the final output."

## Authority and non-goals

Authority: Brian's direction above; AES canonical is his repository and its governed roots change only through an accepted AES plan, which this is.

Non-goals: changing any other repository's plans or targets; checking whether a declared `false` is true against what actually ran (left to the running-system scan); choosing a trace store (the shared LLM client's call log already exists); requiring a human reviewer (an independent agent counts).

## Irreversible actions and spend

This plan proposes zero irreversible actions and zero spend. Every change is code, tests and documents in AES canonical, merged by pull request; containment is `git revert` of that merge, which restores the previous validator, and no record written under the old rules is rewritten. No model call, deployment, data deletion or outbound message is part of the work, so no authorizer beyond Brian's direction above is required.

## Design

1. **Declaration on every proposal.** `trace_review: {runs_traced_work: true}` or `{runs_traced_work: false, reason: ...}`. Missing is a validation violation; `false` without a reason fails to load. Plans accepted earlier load unchanged (the field is optional when loading, required when validating).
2. **Requirement when work runs.** With `runs_traced_work: true`, at least one success criterion the delta adds or changes has an evidence requirement of the new kind `trace_review`. Routing rules are unchanged, so it still needs a verification subject or an external boundary.
3. **Structured review record.** An observation that assesses a `trace_review` requirement carries `trace_review`: trace ids, author, reviewer (not the author), steps total and steps read, models and settings, context per step, outputs and reasons, decisions checked against their sources (correct, wrong or unclear), findings. SUPPORTS needs every step read and no checked decision wrong; REFUTES and INCONCLUSIVE stay open.

## Prior art

Searched: existing ownership (this repository's `planning.py`, `records.py`, `evidence.py`; Company Planning's method profile and overlays), internal lineage (the workspace rule "review full traces" of 2026-10-06; the shared LLM client's trace logs; vision's milestone 4 record), and external prior art (Langfuse, LangSmith, OpenTelemetry GenAI tracing). Each candidate found, with one disposition:

| Candidate | What it does | Disposition |
| --- | --- | --- |
| Company Planning overlay `OV-LLM-CALL-BOUNDARY` | asks a plan to say how its model calls are traced | **extend**: it asks for tracing to exist; this plan requires the trace to be read by someone else before evidence supports the work |
| Company Planning activation facts and overlays | a declared fact switches checklist items on | **reuse**: `trace_review.runs_traced_work` is a declared fact that switches on a required evidence kind |
| AES evidence kind `human_review` | a person judges something; no structured record | **bounded exception**: kept unchanged; `trace_review` is a separate kind because its record (steps read, context, decisions checked) is what makes it checkable |
| Shared LLM client per-day call logs (`calls_<date>.jsonl`, keyed by `trace_id`) | stores every model call with prompt, model and response | **reuse** as the trace store; `trace_refs` point into it |
| Langfuse, LangSmith, OpenTelemetry GenAI traces | record traces and offer annotation queues | **compose**: a run traced there is cited the same way in `trace_refs`; none gates a plan's acceptance |
| Workspace rule "review full traces" (2026-10-06) | a written instruction to agents | **supersede**: AES now enforces it at plan acceptance and evidence loading; the written rule points here |

**Parallel-implementation check:** `git grep -n -i "trace_review" -- src/agentic_engineering_system` must show one evidence kind and one proposal field; a second trace field or kind is a parallel implementation. In Company Planning, if `OV-LLM-CALL-BOUNDARY` gains a "trace is reviewed" clause, that duplicates this check and one must point at the other.

## Uncertainties

These are the plan's material uncertainties: each could make the rule fail its purpose (missed reviews) or block real work (unreachable SUPPORTS). There are no others.

| Material uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Agents may declare `runs_traced_work: false` to avoid the requirement. | The AES coordinator session that owns `proposals/aes-planning` | The next five accepted AES plans in any repository: each one whose work in fact calls a model (its commits add or change llm_client calls) but declared `false` counts as a dodge; one or more means the declaration needs a check against what ran. |
| "Every step read" may be too heavy for runs of hundreds of calls. | This plan's owner (claude-code:vision-review-trace) until merged, then the AES coordinator | The first real `trace_review` observation (planned: vision milestone 4 retry, six coding calls): if a reviewer records INCONCLUSIVE only because of step count on a run whose sampled steps were all correct, the threshold moves into `.aes/planning.yaml`. |

## Success and what would disprove it

**Success is shown by:** `aes plan validate` refusing a proposal with no `trace_review` declaration and one that declares traced work without a `trace_review` evidence requirement, and accepting the declared and routed case; observation loading refusing a `trace_review` assessment without a record, SUPPORTS with unread steps, SUPPORTS with a checked decision marked wrong, and a review by the run's own author; all asserted in `tests/greenfield/test_trace_review.py` with counts, and `make aes` passing.

**Disproved if:** within the next five accepted plans that run models, one is accepted without a `trace_review` requirement, or a failure that its trace shows is found only after its `trace_review` evidence SUPPORTED it.

## Verification

`tests/greenfield/test_trace_review.py` (planning refusals and acceptance, observation refusals and the valid record), the updated `tests/greenfield/test_planning.py` and `test_plan_receipt.py`, and `make aes`.
