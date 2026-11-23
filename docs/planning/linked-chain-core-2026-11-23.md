---
description: Put AES's linked chain (requirement -> scenario -> test -> file -> symbol) back into the minimal core and the template
---
# Plan: the linked chain is core

Status: built (#1011, #1012; acceptance recorded in #1013). The planned file layout it left optional is put back by
`back-on-design-2026-11-23.md`.

Plan size: full (the template is read by every copy through `copier update`, so the small-plan test fails). Source:
Brian, 2026-11-23: "isnt this the whole thing that makes the whle systme work?"; AES `docs/architecture/GOAL.md:88`,
`docs/architecture/LOCKSTEP.md:26`. The minimal-core list (C1-C11) left the chain out; the milestone is reopened.
Revised after a cold review (2026-11-23, verdict revise; findings folded in below).

## Facts (survey and review 2026-11-23, origin/main)

- Links in a copy today: `Implements:` docstring lines (requirement -> symbol) and `req()` test markers
  (scenario -> test). `lockstep status --json` already emits these edges (`checks/status.py:49,85-91,202,205`),
  but drops the implementer's `file:line` that `checks/markers.py:59-87` computes, and writes no file.
- The edit hook hands an agent the OpenSpec requirement text when it edits a file with an `Implements:` block. With
  no layout plan in the repository (`aes_bridge.find_root` is None) it only hands over text: the edit path returns
  context (`hook.py:395-402`), the shell path returns nothing (`hook.py:335-337`), and without `PCW_MODE=block` it
  never refuses. It is installed only by `lockstep init` (`init_repo.py:66-98`), which also rewrites `lefthook.yml`,
  writes `lockstep.yaml` and runs the hook through `uvx` from unpinned `main`; the template does not call it.
- `lockstep check` is a diff check against HEAD (`check.py:122-131`), not a whole-tree scan, and errors when a
  repository has no commits (`check.py:390-396`). Refusing an undeclared file needs `governed:` plus a `layout:` row
  for every file (`unplanned_files.py`), which repeats file lists the markers do not need.

## Decision: the markers are the one home of each link

`Implements:` and `req()` stay the authority (truth where it is edited, K8 one home). The link file is generated
from them and is never edited by hand. Refusing undeclared files is a separate feature and is parked (below).

## Slice 1 (this plan)

1. **Template ships the edit hook, text only.** Two template files, `.claude/settings.json` and `.codex/hooks.json`,
   run `uv run lockstep-hook` (the copy's own locked Lockstep, no network) on edits. No `PCW_MODE=block`, no
   `lockstep.yaml`. Fix in the hook: for Claude, a text-only answer carries `additionalContext` without
   `permissionDecision: allow` (an `allow` skips the agent's own permission prompt; Codex already drops it,
   `hook.py:~575`). Probe 2026-11-23: Claude Code injects `additionalContext` with no `permissionDecision`
   (scratch `claude -p` run read the hook's text). Headless `run-plan` already bypasses permissions
   (`plan_run.py:105,110`), so it does not depend on the `allow`. This changes the existing hook requirement, so it
   goes in the OpenSpec delta and the 16 `allow` assertions in the hook tests are updated.
   Codex: hooks are a feature that is off by default (`codex features list`: `hooks stable false`) and each project
   hook needs trusting, so the copy's README says how to turn it on; Codex delivery is tried in the rerun, not a
   pass condition.
   Hook logs already go outside the checkout (`hook.py:201-210`), so nothing is added to `.gitignore` for them.
2. **One link file.** `lockstep check project` writes `docs/links.json` (git-ignored, like `docs/status.md`):
   `version`, and `nodes` with `id`, `type` (capability, requirement, scenario, test, symbol), `title`, `file`,
   `line`, `links`. Built from the existing `status` report, keeping `file:line`. Node shape follows sphinx-needs
   `needs.json` so other tools can read it; new types (decision, goal) can be added later. Prior art: build on the
   existing parsers (StrictDoc, Doorstop, sphinx-needs, OpenFastTrace, LOBSTER, reqif checked and rejected; record in
   the change's `prior-art.json`). `file` is also a node, so "what links to greeting.py" is one lookup. The status
   page's requirement table gains the `file:line` it now drops (`status.py:202`), so a person can read the links
   without opening JSON. This extends `lockstep-projection/status-links-each-requirement-to-its-code-and-tests`.
3. **Correct the record** in the same pull request: minimal-core section 1 (the chain is core), section 4 (the edit
   hook's text hand-over is now default-on; refusal stays an add-on), section 8 (milestone reopened);
   `second-user.goal.md` roadmap; `.project-brain/now.md`.

Old copies: `copier update` adds the two hook files and the ignore line. A copy that already has its own
`.claude/settings.json` gets a copier conflict to resolve; the hook never refuses an edit, so a copy that takes it
loses nothing.

## Acceptance (judged from the run trace, in a fresh copy with clean agent logins)

First plan as in the second-user run (greeting requirement, `greeting/greets-a-person-by-name`); then a second
plan that changes it (e.g. greet a list of names). Pass when:

- the copy's `.lockstep/` hook log has a line `why: openspec_text` naming that requirement for the `greeting.py`
  edit, and the Claude implementer transcript shows the text arriving (log copied out before `ship` removes it);
- `docs/links.json`, regenerated by `make check` in the run, lists the changed scenario, its test, `greeting.py`
  with a line number, and the symbol; a script compares it to the markers;
- the agent was still asked for permission as its settings require (no auto-approval from the hook);
- hidden tests pass and `ship` merges. Hidden tests passing alone is not enough.
- Brian is shown the generated status page's link table from the acceptance copy.

## Parked

Refusing undeclared files (`governed:` + layout rows, a whole-tree scan, the no-commit case, copy-only copier
guard); decision and goal nodes (open item 2, Brian's call); layout `exports:` signatures; AES's own repository
adopting the link file in its checks.
