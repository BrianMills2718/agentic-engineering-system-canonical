---
schema_version: "1.0"
artifact_type: design_plan
id: meeting-claims-true
status: proposed
method_conformance_receipt: proposals/meeting-claims-true/PLAN.receipt.json
goal:
  outcome: "Every checkable claim Brian made in the 2026-10-08 SD - AI Astronaut meeting is true of the running systems, and the second brain answers Tyler's Slack-only positions correctly."
  canonical_example: "Dagim installs Company Planning from Inside-Success/company-planning by its README and gets the current version (the one with skeleton and check); a project brain's next scheduled run reads source code, searches GitHub for an off-the-shelf fix, and its run page lists every tool call; asking Brian's assistant gold question G003 in its own words retrieves Tyler's 'politics' message and the answer uses it."
  forbidden_substitutes: "a claim marked true from code reading or a passing unit test without a re-check run of the live system; a gold-set score without reading each item's trace; a changed prompt or config that no run has exercised; re-wording a claim so it becomes true without the system changing (allowed only for the three claims this plan lists as corrections, and only after Brian approves the corrected text)"
  boundaries: "Pull requests in the owning repositories; Team-Brains files in code-c1's lanes change only with code-c1's agreement; deploys use the transactional scripts under the shared lock, announced to code-c1; force-pushing Inside-Success/company-planning only after its old main is kept on a backup ref; no message to teammates without Brian approving the exact text"
  done_when: "The claim register in this plan shows each claim TRUE, each judged from the trace of its named re-check run, or CORRECTED with Brian's approved text; G003, G005 and G010 pass with traces showing the retrieved assertion used; the gold set is re-measured with every miss classified from its trace"
  do_not_gate_on: "teammates installing the plugin or answering brain proposals; Brian reviewing pull requests; the Sunday 2026-10-11 scheduled feedback run, which is checked when it happens"
---

# Make the 2026-10-08 meeting claims true

In the 2026-10-08 "SD - AI Astronaut" meeting (zoom:b5b26a4b0e7daf1a) Brian described his project brains, Company Planning, plan-to-code alignment, feedback system, positions map and ChatGPT backup to Tyler, Dagim, Jawad and Syed. Five read-only checks the same day found most claims partly true and several false. Brian, 2026-10-08: "we need to make all the claims i made true and improve the quality."

## Actor and result

**Actors:** Brian, who made the claims, and his teammates (Tyler, Dagim, Jawad, Syed), who will act on them: Dagim was told to install Company Planning, and Tyler weighed the project brains against his own design based on what Brian said they do.

**Desired result:** every claim in the register below is true of the running systems, judged from a trace of a real run. Where a claim cannot or should not be made true, it is corrected in writing, with Brian's approval. The second brain also answers Tyler's Slack-only positions correctly, which is the quality half of the request.

**Example:** Dagim types the install command from the Inside-Success/company-planning README and gets the build with `skeleton` and `check`, not the 2026-10-04 build he would get today. The Team-Brains project brain's next scheduled run opens `knowledge/mcp_server/server.py`, not only `.md` files, and runs a GitHub search for an existing tool, and its run page lists those calls. Asking Brian's assistant "someone from another department is trying to set up a meeting directly with one of our team members, what should we do?" returns Tyler's "add me to DMs ... there is politics in this stuff", and the answer uses it.

### Claim register

Verdicts are from the 2026-10-08 checks. Each row is closed by its re-check run (milestone in brackets).

| # | Claim (Brian's words, abridged) | Today | Re-check run that closes it |
|---|---|---|---|
| P1 | a brain per project, woken by commits and on a schedule | TRUE | none needed |
| P2 | it makes proposals and codes up PRs on its own | PARTLY: 2 PRs from 19 runner attempts, 16 failed on missing credentials | [M3] next 10 runner builds: PRs opened, none failing on credentials |
| P3 | it knows the owner from commit history and docs, and sends to them | PARTLY: owner list is hand-written | [M3] owner list regenerated from git history; a proposal reaches that owner |
| P4 | it reads the repo, including code and other branches | FALSE for scheduled brains (1,704 of 1,724 reads were .md) | [M3] next scheduled run's trace shows source-file reads |
| P5 | owners can mark its PRs helpful or not | PARTLY: no PR rating | [M3] a rating on a brain PR shows on the Brain value page |
| P6 | it has the same sources as personal brains (Slack, Zoom) | PARTLY: no Slack tool | [M3] a run trace shows a Slack search |
| P7 | it searches GitHub for off-the-shelf tools and hunts bugs | FALSE | [M3] a run trace shows a GitHub search and a bug-scan step |
| P8 | observability of what it does (Brian: "I need to add more") | PARTLY: tool calls exist but are not joined to runs | [M3] `brain_runs` shows each run's tool calls |
| K1 | a router for task types | mostly TRUE; two of six routes have no checklist | [M1] probe and reset routes get a checklist or a stated exemption |
| K2 | plans require reasoning, work units, design, schemas, contracts, dependencies, deployment | PARTLY: schemas, contracts, deploy not gated | [M1] a plan crossing a boundary is refused without them |
| K3 | a skill plus hooks for enforcement | PARTLY: commit refusal is the AES rule, not this plugin | [M1] Codex `hooks/list` run; wording in the plugin README matches what refuses what |
| K4 | teammates get it from the Inside Success account | FALSE: Inside-Success copy is 4 days stale, separate history | [M1] fresh install from the Inside-Success README reports the current build |
| K5 | used on other projects, working well | PARTLY: 41 plans in 13 repos, 3 days old; refusals overwritten | [M1] each adoption attempt is appended, so refusals are countable |
| K6 | planning asks "is this route optimal?" and logs it | PARTLY: generic skill feedback; nothing reads it back | [M1] adopt asks route fit; a reader opens a concern on a repeat mismatch |
| A1 | plans name the files they govern | TRUE in AES-target repos | none needed |
| A2 | plans inject intent into each file and function | FALSE | [M4] markers in planned files from the plan, by an adopted tool |
| A3 | status from code flows back into plans | PARTLY: report only | [M4] status file updated by the commit hook |
| A4 | a wiki layer tells agents where to look | TRUE but stale in places | [M4] wiki links the target; llm_client codebase-wiki check passes |
| A5 | an enforcement mechanism keeps code and plan aligned | TRUE in 3 repos | [M4] hook also in Digimon once it has planned paths |
| A6 | "this doesn't really exist out there" | FALSE: StrictDoc, Spec Kit, OpenSpec cover parts | [M7] CORRECTED, text approved by Brian |
| F1 | friction is logged automatically | PARTLY: only 69 of 429 records come from agent closeouts | [M5] collector warns on zero closeout lines; a week of runs |
| F2 | grouped into failure modes | PARTLY: noisy groups | [M5] groups titled by agent-written lines |
| F3 | an audit skill checks those failure modes | PARTLY: list is hand-written | [M5] taxonomy pass reads the new log and proposes list changes |
| F4 | feedback goes into planning or policy | PARTLY: once for policy, never for planning | [M5] a planning-type problem opens a company-planning issue |
| F5 | periodically categorized | PARTLY: first scheduled run Sunday | [M5] the 2026-10-11 run is checked |
| F6 | never delete from the log | TRUE | none needed |
| F7 | everybody's feedback in one place | FALSE: only Brian's local sessions | [M5] one teammate-origin record arrives through a supported intake |
| W1 | project wiki that pulls in Slack; "we already have" ingestion | PARTLY: pages carry no Slack | [M6] project pages show recent Slack |
| W2 | his repos hold reasoning, roadmaps, capability ladders | PARTLY: ladders 1 of 5 | [M6] the five sampled repos carry a ladder |
| W3 | positions map over all his chats, changing over time | PARTLY: no Codex/Claude Code; manual rebuild | [M6] scheduled rebuild includes Codex and Claude Code sessions |
| W4 | could build this for everyone | FALSE for Codex | [M6] author setting configurable; Codex importer exists |
| W5 | ChatGPT bridge backs up history | PARTLY: extension disconnected since about 10-02 | [M6] backups resume; zero connections raise an alert |
| W6 | his reply format | TRUE | none needed |
| Q1 | the second brain finds people's stated positions | FALSE for G003, G010; G005 found and unused | [M2] three traces show retrieval and use; gold set re-measured |

## Milestones

**M1 Company Planning for the team** (company-planning, Inside-Success/company-planning). Keep the old Inside-Success main on `backup/pre-sync-2026-10-08`, then make Inside-Success main equal BrianMills2718 main and keep it synced on each release. Add probe/reset checklists or a stated exemption (K1); gate items for schemas, contracts and deploy behind activation facts (K2); README wording for what refuses what, and one Codex `hooks/list` run (K3); append every adoption attempt (K5); a route-fit question in `adopt` with a reader that opens a concern on repeats (K6).

**M2 Answer quality** (Digimon governed search, the assertion extractor, Brian's assistant instructions). Hybrid ranking with embeddings over governed assertions beside the current word-match ranking; assertion rewrites that keep the referent and the stated reason; an assistant instruction to use a retrieved stated position. Re-extract only the assertions whose sources changed in the extractor, starting with Slack.

**M3 Project brains** (Team-Brains; code-c1 agreement for its lanes). Scheduled brains may list and read source files and branches (P4); add a Slack search tool (P6); a GitHub search and bug-scan step (P7); a read-only GitHub token and scoped key file for the PR runner (P2); owner list regenerated from git history (P3, code-c1 lane); a helpful/not-helpful label read by `brain_value.py` (P5, code-c1 lane); `brain_runs` shows each run's tool calls, and a short system model for project brains at `Team-Brains/docs/model/ODD.md` (P8).

**M4 Plan-code alignment** (AES canonical). Short landscape review of StrictDoc, Spec Kit converge/analyze and OpenSpec; adopt the one that writes plan markers into code (A2); `aes reconcile --write` to a separate status file run from the commit hook (A3); wiki links and the llm_client codebase-wiki fix (A4); hook in Digimon when it has planned paths (A5).

**M5 Feedback loop** (AES learning loop, agent-skills). Warn on zero closeout lines (F1); agent-written group titles (F2); taxonomy pass reads the new log (F3); planning-type problems open company-planning issues (F4); check the Sunday run (F5); an intake teammates can use, with a source label (F7).

**M6 Wiki, repos, positions, backup.** Recent Slack on project pages (W1); capability ladders in the five sampled repos (W2); scheduled positions rebuild with Codex and Claude Code sources, configurable author (W3, W4); reconnect the ChatGPT extension and alert when connections drop to zero (W5).

**M7 Corrections.** A6 and any claim a milestone shows cannot be made true get corrected text for Brian to approve; nothing is sent to teammates without that approval.

Order: M1 first (a teammate was told to install it), then M2 and M3, then M4 to M7.

## Success and disproof

Every criterion below is judged from the full trace of a named run, not its outcome alone.

1. *Each register row closes by its re-check run.* Run: the run named in the row's last column. Trace: for brain rows, the Hermes `state.db` session of that run read with `plan/eval/brain_trace.py` (each tool call, arguments, result); for planning rows, the `adopt`/`check` output and receipt; for install rows, the install command's output and `claude plugin list`; for feedback rows, the collector's report line and journal entry. Must be seen: the behavior the claim names, in the trace (for P4, a `read_file` of a non-`.md` path; for P7, a GitHub search call).
2. *Answer quality.* Run: the gold set through `plan/eval/eval_runner.py` with `LLM_CLIENT_PLAN_ID=meeting-claims-true`. Trace: each item's session via `brain_trace.py`, searched by assertion id, not by original wording. Must be seen: G003, G005 and G010 each retrieve their assertion (`gassert2_48c5e7…`, `gassert2_7764757…`, `gassert2_3585ee5…`) and the answer cites it; every other miss is classified as never retrieved, retrieved and unused, or a wrong expected answer.
3. *Nothing regressed.* Runs: the "before" run is the 2026-10-08 gold-set run already recorded (its sessions are listed in the integration repo's `brain_answers.jsonl` for that date, including 20261008_105120_b52505, 20261008_105227_4d632b and 20261008_105513_31eb39); the "after" run is the first gold-set run after M2 deploys, run with `LLM_CLIENT_PLAN_ID=meeting-claims-true`, whose session ids land in the same `brain_answers.jsonl`. Trace: each item's Hermes session in the `2b-brian-mills-brain` profile's `state.db` on the server, read with `brain_trace.py`, for every item that passed before and fails after. Must be seen: none, or each explained from its trace.

**Disproof:** the approach is wrong if, after M2, G003 and G010 still never retrieve their assertion with meaning ranking in place (the trace shows no hit in any search result): the cause is then the extracted rewrite itself, and the fix moves to indexing the original message text. It is also wrong for M3 if the brains' next five scheduled runs, with code reading allowed, still read only `.md` files in their traces: the prompt, not the tool allowlist, is what limits them.

## System model

System model: the second brain's architecture at Inside-Success/brians-2nd-brain-integration-work `wiki/concepts/second-brain-architecture.md`, the planning gate's model at company-planning `docs/model/ODD.md`, and the project-brain model this plan writes at Team-Brains `docs/model/ODD.md` (M3). Elements this plan changes or relies on, and what the examined run must show: governed assertion search (ranking mode in its receipt), the assertion extractor (rewrites carrying referent and reason), scheduled brain runs (tool calls in the session), the PR runner (build ledger outcome), the plugin release sync (installed build number), the feedback collector (report line).

## Authority and non-goals

**Authority:** Brian, 2026-10-08: "we need to make all the claims i made true and improve the quality." The repositories are Brian's, or Inside Success repositories where his approval of the task is the mutation grant (workspace policy). Messages to teammates and corrections of claims need Brian's approval of the exact text.

**Non-goals:** building Tyler's bottom-up context hub (his design, not Brian's claim); deciding the top-down versus bottom-up question from the meeting; Syed's Claude startup application; posting on X; changing code-c1's lanes without its agreement; a new verifier or new planning profile beyond K1/K2.

## Irreversible actions and spend

- **Inside-Success/company-planning sync** (M1): replacing main with a different history. Boundary: Inside-Success/company-planning main. Authorized by Brian's request (policy: a reversible change in a repository he works in). Contained by first pushing the old main to `backup/pre-sync-2026-10-08` and confirming the backup ref resolves; the old state is restorable from it.
- **Deploys to the shared server** (M2, M3): authorized by Brian's request; contained by the transactional deploy scripts with rollback, run under the shared lock and announced to code-c1.
- **Spend:** model calls for re-extraction of changed Slack assertions, embeddings for about 12,400 assertions, brain re-check runs and gold-set runs. Boundary: about $25 in total for this plan, logged by plan id (`LLM_CLIENT_PLAN_ID=meeting-claims-true`) in the call logs. Authorized by Brian (agent spend approved 2026-10-07/08). Contained by re-extracting only changed sources and stopping a step whose cost passes twice its estimate.
- **Messages to teammates:** none sent without Brian approving the exact text.

## Uncertainties

These are the material uncertainties known on 2026-10-08; each can change whether the plan meets its goal.

| Uncertainty | Owner or resolving evidence |
|---|---|
| Whether meaning ranking alone recovers G003 and G010, or the rewrites must keep more of the original text | Owner: this plan's agent. Evidence: M2's traces (success criterion 2 and the disproof) |
| Whether code-c1 agrees to the P3 and P5 changes in its lanes, or does them itself | Owner: code-c1, asked before M3 starts |
| Whether scheduled brains read code once allowed, or the prompt keeps them on docs | Owner: this plan's agent. Evidence: the next five scheduled runs' traces |
| Whether the Digimon governed search accepts an embedding index without breaking its receipt contract | Owner: the Digimon repo session. Evidence: Digimon's tests and one live search receipt |
| Whether reconnecting the ChatGPT extension needs Brian at the browser | Owner: this plan's agent; evidence: the bridge's `/health` after a remote reconnect attempt |

## Activation facts

shared_mechanism true (changes to search, planning gate and feedback loop that every agent uses); llm_central true (re-extraction, embeddings, brain runs and the gold-set judge are model calls); irreversible_or_spend_action true (the plugin repository sync and model spend); empirical_comparison_proposed false (the gold set verifies outcomes against expected answers; no alternatives are compared to pick a winner).

## Prior art and ownership

Searched 2026-10-08 through five read-only checks, one per claim group, each told to find the owning code, earlier internal versions, and external tools for its group. **Search coverage:** ownership from `project-meta/PROJECT_GRAPH.json` and each repository's code; internal lineage by grepping the owning repositories and the AES ideas register (`vision/legacy/project-meta-vision/ARCHITECTURAL_IDEAS.md`); external prior art by web and GitHub search for spec-to-code traceability, drift detection, hybrid retrieval and multi-person feedback intake. Every candidate those searches found is in the table below with its disposition; none was left undecided. **Ownership:** Team-Brains owns project brains and the PR runner (code-c1 owns brain routing, `brain_value.py` and tracing); Digimon owns governed assertion search; company-planning owns the planning gate; AES canonical owns `aes` targets, hooks and the learning loop; inquiry-graph owns the positions map; chatgpt-conversation-manager owns the ChatGPT backup.

| Candidate | Category | Disposition |
|---|---|---|
| StrictDoc `@relation` markers, LOBSTER, OpenFastTrace | external | **compose** for A2 after the M4 landscape review |
| GitHub Spec Kit analyze/converge, OpenSpec, openlore drift | external | **bounded exception** for A3: not adopted, because `aes reconcile` already computes per-file drift from the plan (39 realized, 0 drifted on AES canonical) and only lacks a write-back; the M4 review re-opens this only if one of them also writes status back into its spec |
| hybrid lexical plus embedding ranking (BM25 with dense vectors) | external | **reuse** for M2 ranking |
| `aes reconcile`, `aes context` | internal | **extend** (A3 write-back, A2 context) |
| Team-Brains `brain_runs`, `brain_value.py` | internal | **extend** (P5, P8) |
| learning-loop `collect_feedback.py`, `problems.py`, `taxonomy_feedback_pass.py` | internal | **extend** (F1 to F7) |
| inquiry-graph importers | internal | **extend** (W3, W4) |
| older read-injection hook (`~/.claude/hooks/read_inject.py`, unwired since 2026-08-28) | internal lineage | **supersede** by the A2 markers plus `aes context` |
| Tessl spec-linked generation, Kiro task status | external | **bounded exception**: not adopted; they generate code from specs and do not mark or check existing code |
| ChatGPT bridge (chatgpt-conversation-manager) | internal | **reuse** (W5, reconnect only) |

**Parallel check:** after M2, `git grep -n "tfidf\|embedding" ` in the Digimon governed search package must show one ranking entry point that both modes go through, so no second search path exists; and after M3, `brain_runs` must be the only page that shows a run's tool calls.

## LLM call boundary

**Call graph:** (1) the assertion extractor: one call per changed source passage, structured output a list of assertions (subject, type, sentence, referent, stated reason); (2) embeddings: one call per assertion batch, returning vectors; (3) brain runs: the existing Hermes agent loop, whose result boundary is the run record Team-Brains stores per run (trigger, status, report text, sources, cost, Hermes session id) and, for PR-runner builds, the build-ledger line (`brain-pr-builds-<date>.jsonl`: outcome opened/no_change/error, PR URL, reason); (4) the gold-set judges in `eval_runner.py` (`eval_position_accuracy`, `eval_tyler_ness`), structured verdicts. **Tracing:** every call goes through `llm_client` with `LLM_CLIENT_PLAN_ID=meeting-claims-true`, so each call-log line carries the plan id and a trace id; brain runs keep their Hermes session ids, read with `brain_trace.py`. **Provider and spend authority:** OpenRouter for every call: chat and judge models by `openrouter/<provider>/<model>` id, and embeddings by `openrouter/openai/text-embedding-3-small`, the model Digimon's runtime config already names (`Option/Config2.runtime.yaml:11`); spend authorized by Brian within the $25 boundary above. **Authentic-run condition before promotion:** the new ranking and extraction are promoted only after one live gold-set run whose traces show G003, G005 and G010 retrieving and using their assertions.

## Coordination

**Owners and claimed paths:** this plan's agent (claude-code session code-15) for company-planning, the Inside-Success/company-planning sync, AES `aes` and learning-loop changes, the integration repo's eval, inquiry-graph and the ChatGPT bridge. code-c1 owns Team-Brains `brain_proposals.yaml`, the self_file path, `brain_value.py` and tracing; P3 and P5 go through it. The Digimon repo session owns Digimon; M2's search change is offered to it first. code-83 owns the AES commit rule.
**Dependencies:** M2 depends on Digimon's search package; M3 P3 and P5 depend on code-c1; M5 F4 depends on company-planning issues existing.
**Conflict surfaces:** Team-Brains `main`; Digimon `main`; the shared server's deploy lock; the `team-tools` and `shared-evidence` containers.
**Integration owner:** this plan's agent (`claude-code:meeting-claims-true`) integrates the plan end to end: it merges its pull requests after local checks, announces each deploy to code-c1 before taking the lock, and updates the claim register after each re-check run. code-c1 and the Digimon session integrate their own lanes.
**Work-unit evidence, per writer:** this plan's agent: one issue per milestone M1 to M7 in Inside-Success/2nd-brain-plan-repo, each listing its pull requests and the re-check trace that closes each register row. code-c1: the Team-Brains pull requests for P3 (owner list from git history) and P5 (PR rating in `brain_value.py`), linked from the M3 issue, or code-c1's reply declining them. Digimon repo session: the Digimon pull request for M2 hybrid ranking, linked from the M2 issue, or its reply handing the change back. code-83: no work unit in this plan; its commit rule is relied on, not changed.

<!-- goal-authority-reversion:v1:start -->
```yaml
schema_version: "1.1"
owner: "claude-code:meeting-claims-true"
receiver: "claude-code:recovery"
transfer:
  trigger: "explicit_handoff"
reporting:
  event: "register row closed with its re-check trace"
  deadline: "PT4H"
  one_probe_transition: "block"
non_gating_utility_review:
  broad_cycle_limit: 2
  on_limit: "compare_direct_route_and_merge_or_defer"
  later_review: "exact_counterexample_only_unless_scope_expands"
```
<!-- goal-authority-reversion:v1:end -->

## Boundaries

| Boundary | Owning authority | Rollback or containment | Disposition |
|---|---|---|---|
| Inside-Success/company-planning main replaced (deployment of the plugin to teammates) | Brian's request; the repository is in his Inside Success account | backup ref `backup/pre-sync-2026-10-08` pushed and resolved first | proceed |
| Deploys of search, extractor and brain changes to the shared server | Brian's request; server deploy scripts | transactional deploy with rollback, shared lock, announced to code-c1 | proceed |
| Slack and meeting content read during re-checks (sensitive data) | Inside Success access rules, enforced server-side | read through the governed tools only; nothing copied into public places | proceed |
| Corrections or messages sent to teammates (publication) | Brian | exact text approved by Brian before sending | deferred until approved |
