---
description: First add-on after the linked chain - links.json reads the link lines repositories already write (Closes, Source, quote markers, decision Governs and supersession), and the edit hook hands over the decisions that govern a file
---
# Plan: links from lines that already exist

Plan size: full (the template and the package are read by every copy). Source: Brian, 2026-11-23: "i approve"
(to: "Step 1 puts the `Closes:`, `Source:` and quote links into `links.json`, with no new lines. Step 2 searches
your past chats and decision 0004 first, then adds decision -> requirement or code links that the hook hands
over."). Test for each link (agreed in the same exchange): it earns its place only if it gives an agent context at
edit time, triggers a check when one end changes, or gives a person a view.

## Facts (survey 2026-11-23, origin/main `4274c69`)

- `docs/links.json` today holds capability, requirement, scenario, test, symbol and file nodes
  (`checks/status.py:286`), built from `Implements:` and `req()` markers.
- `Closes:` lines: `plan_files()` (`checks/status.py:153`) reads `docs/plans/*.md` and active change proposals;
  `report()` and `project()` use it for plan status blocks. In AES all six `Closes:` lines are in archived
  proposals (`openspec/changes/archive/*/proposal.md`), which `plan_files()` skips on purpose.
- `Source:` lines: `checks/sources.py:_spec_items` and `_decision_item` read them for every requirement and
  decision and classify them (brian, inferred, other, missing). They point at a person's words, not at a file in
  the repository.
- Quote markers: `checks/quotes.py:check` returns each `<!-- lockstep quote: <id> -->` passage with file, line
  and state (current, stale, unknown, unclosed).
- Decisions: all fifteen AES decision records already carry a `Governs:` line (`docs/decisions/0001`-`0015`),
  naming paths (`copier.yml, template/`), path anchors (`SYSTEM_BOUNDARY.md#aes-cap-003...`) and rule IDs
  (`RULE-DEPENDENCY-CHANGE-STALES`). Nothing reads them. Supersession is written as front matter
  `status: superseded` / `superseded_by:` (decision 0007) or a MADR bullet `- Status: superseded by ...`.
  AES decision 0004 section 5 keeps decisions as their own record type with their own supersession.
- Search of Brian's chats and sessions (2026-11-23, brian-positions) found no earlier rule on decision-to-code
  links; his 2026-11-23 question asked for one file linking capabilities, files, success criteria and decisions.
  No quotes are copied here (private archive).

## Slice 1 (pull request 1): links.json reads Closes, Source and quote lines; page columns

1. `links(result, root)` adds, when given the repository root:
   - `plan` nodes, one per proposal or plan with a `Closes:` line: active ones from `plan_files()`, plus archived
     change proposals (field `state`: `active` or `archived`). `links`: the closed requirement/scenario IDs.
     `plan_files()` itself is unchanged, so plan status blocks are unchanged.
   - `quote` nodes, one per marker (`id` `<file>:<line>`, `state` from the quotes check), linking to the ID.
   - a `source` field (the `Source:` text) and `source_kind` on requirement nodes. `Source:` is a field, not a
     node: its other end is a person's words.
   - Node shape and `version: 1` stay; `links` stays the only edge list (sphinx-needs `needs.json` shape).
2. The page (`linked-chain.html` in the acceptance folder) draws plan, decision and quote | capability |
   requirement | scenario | test | symbol | file as separate columns.

## Slice 2 (pull request 2): decisions in links.json and in the hook

1. New module `lockstep/decisions.py` reads `docs/decisions/[0-9]*.md`: title, status, `superseded_by`, the
   decision paragraph (`sources._decision_item`), and `Governs:` targets (`Governs:` or `- Governs:`, comma
   separated). A target resolves to a path if it exists in the repository (anchor dropped; a folder covers what
   is under it), else to a requirement or capability ID if the plan defines it; anything else stays as a raw
   string in `governs`, and no check fails on it.
2. `links.json` gets `decision` nodes: `links` to the resolved targets, fields `status`, `superseded_by`,
   `source`, `source_kind`, `governs` (raw).
3. The edit hook (edit and shell routes, repositories with OpenSpec specs) appends, after the requirement text,
   each decision that governs the file being edited: by path, by folder, or through a requirement or capability
   the file implements. It hands over the title, status, file and decision paragraph, not the whole record. A
   superseded decision is flagged: "superseded by X; check this code still follows X". A file only a decision
   governs (no `Implements:`) gets the decision text alone. `requirement_packet` keeps its contract.
4. Template: decision 0001 gains `- Governs: docs/architecture/model.c4`; README gains one line on `Governs:`.

## Settled after the cold read (2026-11-23, verdict revise; each finding answered)

- Signature: `links(result, root: Path | None = None)`; `project()` passes its root. Without a root, output is as
  today. `source_kind` uses `checks.config.load(root).human_pattern` (falls back to `brian` if the config errors).
- OpenSpec: slice 1 is change `link-file-reads-existing-lines` (MODIFIED
  `lockstep-projection/status-links-each-requirement-to-its-code-and-tests`, node types now include `plan`,
  `quote`, `decision`; new scenario `the-link-file-reads-plans-sources-and-quotes`). Slice 2 is change
  `hook-hands-over-governing-decisions` (new requirement in `lockstep-guard`, scenario for links decisions).
- Edges only to nodes in the file. An ID a plan or quote names that no node has goes in that node's `unknown`
  list, not `links` (archived plans often name since-renamed requirements). A decision's path target becomes a
  `file` node (a folder too, with its trailing `/`).
- Node IDs: plan = its path; quote = `<path>:<line>`; decision = `decision/<file stem>` (as the sources check). If a
  plan path is also a decision target, the one node keeps type `plan` and gains no second entry.
- `Governs:` parsing: first line starting `Governs:` or `- Governs:` (bold allowed); split on commas; strip spaces
  and a trailing period; resolve against the repository root; anchor dropped for the path test, raw text kept in
  `governs`. Supersession: front matter `superseded_by:`, else the text after `superseded by` in a `Status` line.
- Hook text bound: at most 3 decisions per file, ordered direct path, then requirement or capability, then
  folder; the rest named by ID only ("also governed by: ..."). Each gives title, status, file and the decision
  paragraph cut at 600 characters. Places: `decide()` root-None branch and `art is None` branch (now continue only
  when there is neither requirement nor decision text), the layout branch's packet (appended after the
  requirement or plan text; refusal logic unchanged), and `_shell_spec_text`. Log field `decisions` (IDs) is added
  to the existing `openspec_text` record and named in the requirement.
- No check changes its exit code. A repository with no `docs/decisions/` gets no decision nodes and no hook text.
- Template: `tests/test_template_portable.py` gets a case that a rendered copy's `links.json` resolves decision
  0001's `docs/architecture/model.c4` target to a file node.
- Acceptance counts are measured in AES after the build and written into the pull request, not guessed here.

## Not doing

Generated files, evidence and wiki pages as nodes (existing checks cover them); symbol-level decision targets
(requirements and decisions are component-shaped); a failing check for an unresolved or superseded `Governs:`
target (no gate was approved).

## Acceptance (judged from the run trace)

- AES: `make check` exit 0; `docs/links.json` has 6 archived plan nodes, the quote nodes the quotes check
  lists, and 15 decision nodes, 0007 with `status: superseded`.
- chain-test (fresh lock, clean-home Claude): a plan with a live `Closes:` line, a quote marker and a decision
  with `Governs:` all appear in `links.json`; Claude, editing a governed file through `run-plan`, gets the
  decision text (hook log `decisions` field) and the page draws the new columns.
