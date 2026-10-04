# Vision coverage

Status: shaping
Role: non-binding proposed plan
Authority: proposed only; the owning repositories (`vision`, `inquiry-graph`) keep authority over their content
Review page: `review-page/vision-coverage-plan.html` (served at hive.brianmills.dev/plans/)

## Outcome

Brian's already-written vision material is covered: every document he authored about the program is found, captured in the Vision wiki as a source, and compiled into pages that quote him; and the positions and open questions in his conversations reach the hypotheses register with their conversation ids. Reason: on 2026-10-04 the three fullest statements of the vision turned out to sit in a Downloads folder and on Google Drive while agents reasoned from a thinner derivative (vision PR #40).

Brian, 2026-10-04: "maybe this implies that we need to do a better job covering the material i have already written and integrating it ... maybe we should use inquiry graph or something like it to more formally represent what has been done and what is open." Then: "proceed."

## Flow

Two stores with different jobs, meeting in the register:

- **Vision wiki** holds documents, compiled into readable pages: what the vision says.
- **Inquiry graph** holds conversations as positions with their history: what was concluded, changed, left open.
- **Register** (`vision/wiki/synthesis/hypotheses-and-evidence-register.md`): each belief row cites both.

Steps:

1. **Find.** Candidate documents from Google Drive (name and full-text matches on vision-related terms), the Windows Downloads folder, and Brian's own repositories. (Brian, 2026-10-04: "it is more than just the observation to action repo. i have been working through a bunch of different parts of the full infrastructure in kind of isolated pieces." The repositories are a source in their own right, and each one is a piece of the infrastructure.) A yes/no model (Jev) reads each name and opening text and scores a fixed set of questions; keywords only pick candidates, they never decide what a document is. Output: one inventory of what exists, where, and whether it is captured. Run 2026-10-04: 12,556 documents judged for $0.47 (4,018 on Drive and in Downloads, 8,538 across 146 repositories). 91 Drive and Downloads documents and 220 repository documents were flagged. Reading then confirmed 34 of the 91 as Brian's own vision writing; the model over-counted by almost three to one, so nothing is compiled without being read.
2. **Capture and compile.** Keepers become governed sources in the Vision wiki; one page per lineage quotes Brian. Done 2026-10-04 in two batches: of 311 flagged documents, 143 were read and confirmed as Brian's own vision writing (34 on Drive and in Downloads, 109 inside repositories); 61 lineage pages; and a piece-statements page recording what 58 repositories say they are and connect to, in their own words. Three drafts marked private and unapproved were left out. Alongside it, a piece map lays the repositories against the parts of the 2026-09-25 architecture; it names repositories, so it lives in the private `vision` repository. Precedent: the Evidence to Action lineage (2026-07-14, 2026-08-01, 2026-09-25), done 2026-10-04.
3. **Pull positions.** When the inquiry-graph archive extraction (another lane, already running) finishes, the vision-related clusters of its topic atlas become register rows for positions and open questions, each tied to its conversation.

## Not building

A new graph tool; a re-run of the extraction; hand-written positions.

## Proposed, not yet settled

Chat exports saved as files go through Find like any document; live ChatGPT conversations go only through the inquiry-graph lane.

## Review points

Each review point is a page Brian can open, not a report:

- Plan: `review-page/vision-coverage-plan.html`.
- After step 1: the inventory of likely vision documents. It lists private document names, so it lives in the private `vision` repository (`wiki/reference/owner-artifact-inventory-2026-10-04.md`), not in this public one; the plan page shows counts only.
- After step 2: the compiled lineage pages in the Vision wiki.
- After step 3: the register rows with links into the inquiry-graph atlas.
