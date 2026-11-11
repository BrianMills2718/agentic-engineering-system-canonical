<!-- Cold review by the company-planning planning-compliance-reviewer subagent, 2026-11-11, refresh of the package for the one-tool plan. Round 1 read 493e155e1 (verdict revise, 4 blocking findings, 5 notes; quoted in full below). Round 2 read 09326db81 (verdict pass). After round 2, the agent fixed its notes on stale anchors only (planning-package.json domain anchors and evidence.py:510 in the manifest and Q9), which change no plan content. -->

# Cold review: AES planning package (one-tool plan), round 2

Reviewed revision: 09326db81cb6491389cfd360cd71cf27ca2e6b86

I did not render the page in a browser. I read the committed HTML and grepped its links. I did not rerun `run_checks.sh`.

**Validator:** all substance checks ok, 0 failing. The only FAIL is freshness (`reviewed at 8b732aaca497`, 9 plan files changed since), as expected. Coverage reports 13 of 14 requirements covered, the 14th being about the planning process.

## Round-1 findings

1. **Navigation warnings count (blocking): fixed.** `checks.txt` has 14 `WARNING` lines, `planning-package.json:137` now says 14, and I found no "10 warnings" text left in the manifest or Q8.
2. **Review page links and footer (blocking): fixed.**
   - There are no `blob/main/https` links in any of the 8 HTML files.
   - Every file link is a clean repository-relative `blob/main/<path>` URL, and the only other targets are the decision, `core.md`, issue-filter and hive links.
   - The footer reads `c44c408fd34c`, which is the subject revision I was told about, not the 8b732aa revision. It is not the HEAD I reviewed, but the commits since touch no plan content.
3. **System model by type (blocking): fixed.** `SYSTEM_MODEL.md` now has rows for the feedback-loop and policy-layer types, each with a writer and a store.
   - Feedback loop: `Record`, `Link`, `Provenance`, `Turn`, `Transcript`, `Check`, `Verification`, `Outcome` and `_Step`/`_Fix`/`_Analysis`.
   - Policy layer: the agent router contracts and `Disposition`.
   - The "Outside this model" section now points back at the table. The "does AES execute typed rules" answer (no) is unchanged.
4. **Q18 owner and slice (blocking): fixed.** `next.goal.md:58-62` adds a step 0 with an owner (an agent in `scripts/learning_loop/`, not the Lockstep session), a proof (a correction from the day before appears as a `source:human` issue after the next nightly run) and acceptance entry A6, which fails today.
5. **A1, A2 and A5 jargon (blocking, I was unsure): fixed enough.** Each `expected` now starts "In plain words". A1 explains the hook entries, A2 explains `cat >`, `echo >`, `python -c` and read-only `cp`, and A5 explains machine paths. The failure examples still name concrete strings, but they are glossed.

Round-1 notes:

- **Domain-model anchors:** fixed in `domain.graph.json`. For example, `observation` points at `evidence.py:184`, `assessment` at `:104`, `negative-control` at `:120` and `freshness` at `:384`. The manifest and Q9 are not fixed (see the first new note below).
- **Q3, Q5, Q7, Q8 and the other work-item questions marked open:** not changed. They stay open as labelled work items, and the status wording is still only a note.
- **Diagram question mapping, Q12 and Q13 evidence age, and the other round-1 notes:** I did not recheck them. They were notes and are not blocking.

## New findings

- **Note, `planning-package.json:143-148`:** the manifest's domain-concept anchors are stale.
  - `observation` is at `evidence.py:176` (should be `:184`), `assessment` at `:96` (should be `:104`), `negative-control` at `:112` (should be `:120`) and `freshness` at `:376` (should be `:384`).
  - `characterization` is at `characterize.py:59`, a blank line.
  - The rebuilt `domain.graph.json` is right, but the manifest copy and the page links (`review.html` `#L96`, `#L112`, `#L176`, `#L376`) were not regenerated.
  - Fix: rebuild the manifest from the graph.
- **Note, `open-questions.json:226-228` and `planning-package.json:108` and `:303`:** `assess` is still cited at `evidence.py:447`, which is `EvidenceReport`. It is at `:510`. Q9's conclusion holds.
- **Note, `review.html`:** file links use `blob/main`. Files new on this branch, such as the slice-0 text, will not resolve on GitHub until the branch merges. Merge before Brian reads the page.
- **Note, `acceptance-criteria.json` A1, A2 and A5:** the demonstrations still contain `lockstep.yaml`, `cat >` and `/home/brian`. They are now glossed. Brian can judge the pass or fail from the "In plain words" lines.
- **Note, unsure:** R13 ("approve single tool design") was marked UNSURE by the stored coverage judge (1 of 3 runs found a gap). I read A1 and it does ask for the approved single-tool design, so I treat it as covered.

Verdict: pass

## Round 1 report (493e155e1)

**Cold review of the AES Company Planning package at 493e155e1: revise (four blocking findings, five notes).**

Reviewed revision: 493e155e1c6fdadf2ef2f0345dda6a0e5b0e1fce

I did not render the page in a browser. I read the committed HTML and its embedded data. I did not rerun `run_checks.sh`; I read `checks.txt` and spot-checked a few of its counts against the repository.

## Validator and checks

- **Validator:** all 10 parts present, 0 failing; 11 of 12 substance checks ok, 1 pending (the route check). Coverage reports 13 of 14 requirements covered, the 14th being about the planning process.
- **Freshness:** the validator's only failure is the stale cold review (`reviewed 8b732aaca497`, 9 plan files changed since). `cold-review.md` is still the 2026-10-27 file, so the manifest's `cold_review` (`planning-package.json:278`) must be replaced after this review.
- **Counts that reproduce:**
  - the 23 stale plan receipts
  - 108 of 140 Markdown files, 6 unreachable
  - 4 durable-document findings
  - `make aes` counts (2 supported, 10 insufficient, 2 current and 52 stale observations out of 55)
  - 4 repo-format findings
- **Spot-checked repository facts:**
  - the 867 human-correction reports deferred at the cap, plus 474 subagent and 426 closeout reports filed, match the 2026-11-11 reports file
  - the newest `source:human` issue is #1586, from 2026-11-03
  - AES canonical is public

## Quotes

Every quote I checked is in `history.jsonl` with the date, session and UTC time the package gives: the 08:14, 20:17, 20:40, 20:46, 21:10 and 22:23 messages, plus the 2026-10-13 stop. The quotes in the decision 0009 amendments match too. Inferred claims are marked "agent judgment" or "inferred by agent" where I looked. No finding here.

## Blocking findings

1. **Checks:** `planning-package.json:32` and `open-questions.json:134` (Q8) say the navigation check gives 10 warnings, from 8 README links. `checks.txt` shows 14 `WARNING` lines: 12 `NAV_ANCHOR_MISSING`, 1 `NAV_ROOT_LINK_MISSING` and 1 `NAV_DOCUMENT_MISSING`. The tool's own summary says "14 finding(s)". Fix by changing the counts in the manifest, Q8 and the review page.

2. **Review page** (`proposals/planning-package/review-page/index.html`, `review.html`, `open-questions.html`): many links are broken, and the page is stale.
   - Dozens of links have a doubled prefix, `…/blob/main/https://github.com/…/blob/main/docs/planning/…`. These include next.goal.md, planning-package.json, DOMAIN.md, SYSTEM_MODEL.md, acceptance-criteria.json, checks.txt, cold-review.md and investigation.json.
   - Several links are quote strings turned into URLs, such as `…/blob/main/https://…/blob/main/"it also writes the firs tdoc strings …"`. Fix by making the builder prefix only repository-relative paths.
   - The footer still says "Revision 8b732aaca497", not the reviewed revision.

3. **System model, by type:** `SYSTEM_MODEL.md:134` puts the feedback loop's and policy layer's records "outside this model", but the package now says AES is the whole system.
   - The code defines `scripts/learning_loop/records.py` (`Record`, `Provenance`, `Link`), `transcripts.py` (`Turn`, `Transcript`), `subagents.py` (`Outcome`, `Check`, `Verification`), `problems.py` (`_Analysis`, `_Step`, `_Fix`), `scripts/rules/agent_router.py` (profile and handoff contracts) and `sort_legacy.Disposition`.
   - Only the v0.2 engine's types are in the table. Add these to the table with what writes each.

4. **Plan, `next.goal.md:58`, against A6:** "Fix first … corrections are extracted but not filed (Q18)" has no owner, slice or step. "Done when" requires Brian to judge A1 to A8, and A6 fails today. Add an explicit step, or a slice 0, that fixes the filing order and says who does it and what shows it worked. Otherwise the plan does not follow from Q18.

5. **Acceptance, `acceptance-criteria.json:39-70` and `:114` (A1, A2, A5):** the demonstration, expected result and failure example rely on jargon a non-expert cannot judge. Examples are "hook entries for Claude Code, Codex and lefthook", `lockstep.yaml`, `cat >`, `echo >`, `python -c`, `cp src/a.py /tmp/x`, and "machine paths". Brian is mostly non-technical. Add a plain-words column to each row, for example "writes a new file: refused", and a "what this means" line.

   I am unsure whether this one is blocking, because the failure examples do state each row's expected word.

## Notes

- **Questions answered but marked open:** Q3, Q5, Q7, Q8, Q10, Q15, Q16 and Q17 each say in their own text "the answer is known" or give a settling argument, yet are `status: open`. They are labelled work items so that failing checks have an owner. A status such as "decided, work pending" would be clearer. Q6 and Q19 are also argued as settled.
- **Stale line anchors:**
  - The domain model anchors point 8 lines or more off in `evidence.py`.
  - `observation` at `:176` is inside `TraceReview`, while `ObservationRecord` is at `:184`. `assessment` at `:96` is `EvidenceError`'s docstring, while `ErAssessment` is at `:104`. `negative-control` at `:112` is at `:120`. `freshness` is at `:384`, not `:376`. `characterization` at `characterize.py:59` is a blank line.
  - `assess` is cited at `evidence.py:447` in SYSTEM_MODEL, Q9 and the spectrum, but it is at `:510`; `:447` is `EvidenceReport`. The same drift affects `SYSTEM_MODEL.md:110-111`.
  - Q9's conclusion still holds. The validator only checks that a line exists, so rebuild with current lines.
- **Possible missing questions** (unsure about all three):
  - After `.aes/` retires, does the thesis's own boundary ("fresh revision-bound evidence", standing) have a successor in `lockstep status`? `DESIGN.md` folds `aes evidence status` into one status command without saying.
  - Brian's "more opinionated and stack alongside lockstep" is the one requirement of his words that no acceptance entry or question carries.
  - Inside Success repositories would install work tooling from a repository in a personal account. Q2 asks only about the rollout, not the hosting. I did not weigh this against Brian's 2026-11-06 account-routing rule.
- **Diagram claim in the manifest:** both `context` and `cross_repo` point at `SYSTEM_MODEL.md`, and the second diagram in the file is the containers view. The cross-repository question is answered by the first diagram. The two manifest questions should say which diagram answers which.
- **Open-question evidence age:** the Q12 and Q13 evidence is dated 2026-10-27 or cites commit 30e9993, not refreshed for this revision.

## Judgments I am unsure about

- The Q18 hypothesis, "corrections sort last". The report list order in `collect_feedback.py:578` puts per-transcript reports before subagent reports, yet subagent reports were filed. So the cause is not simply list order. The question is legitimately open.
- Whether `domain.spectrum.json` terms and the goal fields in `review-page.json` fit their definitions. I read the thesis, disproof and north star on the page data and found them testable, but I did not audit the spectrum file term by term.

Files: `/home/brian/code2/worktrees/aes-planning-refresh-1111/docs/planning/` (manifest, open-questions.json, acceptance-criteria.json, SYSTEM_MODEL.md, next.goal.md, checks.txt) and `/home/brian/code2/worktrees/aes-planning-refresh-1111/proposals/planning-package/review-page/`.

Round 1 verdict: revise
