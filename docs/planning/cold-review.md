<!-- Cold review by the company-planning planning-compliance-reviewer subagent (claude -p --agent), run 2 of 2, 2026-10-27. Run 1 (verdict revise, 6 blocking findings) is quoted as its previous report in the prompt and summarized under 'Previous findings'. The reviewer's note about uv.lock refers to a working-tree side effect of its own render; it was restored before commit (git show HEAD:uv.lock > uv.lock). -->

# Re-review: AES canonical planning package (`docs/planning/planning-package.json`)

**Verdict: pass.** All six blocking findings in the content from my first review are fixed. The seventh is the missing cold review, which this verdict clears. Nothing new is blocking, but some notes remain.

**My side effect, which needs your attention.** To render the page I ran `uv run --with playwright` from inside the worktree. That did two things:

- It created `.venv/`. Git ignores this folder.
- It re-locked `uv.lock`: 24 lines added for `pytest-xdist`.

I tried to restore `uv.lock` with `git checkout -- uv.lock`, but the safety hook blocked it, so the change is still in the working tree. Nothing I reviewed depends on it, because the review reads committed revisions only. Before anyone commits, run `git restore uv.lock` (or `git diff uv.lock` to look first). One more uncommitted file, `proposals/planning-package/review-page/index.html`, was already changed when I started (a one-line CSS change to `.lede`). That change is not mine.

## 1. Validator

`validate_planning_package.py --repo . docs/planning/planning-package.json` exits **1**.

- **Parts:** 7 of 8 ok. 7 check results, 4 of them found problems. 17 questions (12 open, 5 resolved). 36 concepts, 43 relations, 3 diagrams.
- **Substance:** 4 of 4 checks ok, 0 pending. 43 file citations and 2 other sources. 30 concepts are marked implemented and 6 dashed. 12 concepts are named in `relies_on`. No typed rules.
- **Freshness:** ok, built from 8b732aa with 0 commits of work since. The commit after it, f7241b7, changes 5 package files only.
- **Only failure:** `cold_review: missing`. It clears once this verdict is saved.

## 2. Checks rerun (read-only, at f7241b7)

Both match the manifest:

- **`make aes`** exits 0: 2 supported, 10 insufficient, 0 refuted; 4 current, 50 stale, 1 unknown observations; 8 accepted plans, 1 unreachable; 0 orphans; 0 drifted.
- **`repo_format.py .`** exits 1: 0 of 1 compliant, 5 items missing.

## Previous findings

1. **`superseded_by` on an accepted plan: fixed.** Step 2 now keeps PLAN-AES-SELF-GOVERN as a warning by design and cites `reconcile.py:18-20`.
2. **9-versus-12 comparison: fixed.** Q6 and step 2 now cover only the nine accepted criteria. The later criteria are listed with the evidence each needs (SC-TR-SOURCE-001 a trace review, SC-GF-001 a clean-user run). a06e963 and bb6818a are cited as the cause.
3. **Commit-rule outcome still in the target: fixed.** Q15 and step 1 now handle it. `target` and `outcome` are in `relies_on`. I checked that the plan route can actually do this: `planning.py:122-140` supports `remove:` for outcomes, and validation flags any reference left dangling (`planning.py:330-346`).
4. **Dormant orphan hook: fixed.** I confirmed the facts:
   - `core.hooksPath` points at the lefthook hook, and `lefthook.yml` loads only `code2-workspace hooks/base.yml`.
   - `~/.config/git/repo-hooks.off` exists.
   - Q16 covers it, Q5's answer is revised, the diagram marks the hook dormant, and the domain node says it does not run here.
   - Step 6 names a sync check that exists (`scripts/meta/check_agents_sync.py`).
5. **code2 format: fixed.** Q17 adds the question and step 8 does the quick parts. The check is in the manifest and reproduces.
6. **Plan receipt: fixed.** A `plan-receipt` node was added, citing a real receipt file. Q4 now touches it, the edge is now `commit-rule → plan-receipt` (e41), and it is in `relies_on`.
7. **Cold review missing: fixed by saving this verdict.**

**Notes from the first review:**

- **Weak `checks.txt:1` anchors: fixed.** The cited lines :6, :11, :45, :49, :68 and :88 now each carry the finding they are cited for.
- **Q3 touching `project-brain`: fixed.** Q3 touches nothing now.
- **Q12 evidence: fixed.**
- **Q14 evidence: fixed.**
- **Missing helper types in the system model: fixed.** They are now in one row.
- **Missing stores in the container diagram: fixed.** `.aes/project.yaml` and `.aes/legacy_baseline.json` are now drawn.
- **Domain model gaps: not fixed.** `RULE-*` and TraceReview still have no nodes.
- **`make check`, Plan 002 and the v0.1 frontier: not fixed.** They still get no question.

All of these remain notes.

## Findings (new, all notes)

- **Plan, `next.goal.md` step 1; Q15 at `open-questions.json` (resolves_with).** "TR-REQ-001 … withdrawn with it" would cascade: TR-REQ-001 is referenced at `.aes/target.yaml:278, 310, 348, 384, 861`. Those references include SC-TR-001 and SC-TR-SOURCE-001, so the criteria Q6 counts would change. Validation would catch the dangling references. **Fix:** pick re-pointing at OUT-GF-001 and say why. **Weight:** note.
- **Page, `index.html:338`.** The page still reads "verdict: undefined" because the cold-review part has no verdict yet. Saving this review fixes it. **Weight:** note.
- **Page, working tree.** The uncommitted `.lede` CSS change in `index.html` should be committed or dropped before merge. **Weight:** note.
- **Plan, `next.goal.md` steps.** The plan changes where the project stands, but it never says to update `.project-brain/now.md`. CLAUDE.md asks for that, and `brain_fresh.py` exits 1 when the brain is stale. **Fix:** add the brain update to step 10. **Weight:** note.
- **Repository, outside the package.** At the subject revision `uv.lock` is out of date: `pyproject.toml` declares `pytest-xdist`, but the lock does not include it. My `uv run` exposed this. **Weight:** note.

## Page

I rendered it with Playwright: 5 tabs, 0 console errors.

- **Data:** the page data matches the manifest, the ledger, the open-questions map and the domain graph exactly.
- **Content:** Q15, Q16 and Q17 appear on the Open questions and Next plan tabs, the plan-receipt node is shown, and the diagram labels the hook dormant.
- **Header:** it now says "commit 8b732aa", which is correct.
- **Links:** they still go to `blob/main`, so they resolve only after merge (note, as before).

## What I was unsure about

- **Q17's weight** still depends on the code2 format rule, which is an agent-inferred default (decision 0002) that you have not confirmed.
- **Q6's regression question** is unsettled. I did not rerun `tests/greenfield` this time. The plan's step 2 settles it with the tests already in the repository, so leaving it open is correct.

Reviewed revision: 8b732aaca497a5e4b55bfa0dad0585d0663299f5

Verdict: pass
