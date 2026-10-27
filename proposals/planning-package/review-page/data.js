window.PAGE_DATA = {
 "manifest": {
  "schema_version": "1.0",
  "record_type": "planning_package",
  "repository": "BrianMills2718/agentic-engineering-system-canonical",
  "subject_revision": "c1b3ee65040d0082863b4d4ef36e5d65dcb373c6",
  "request": "Workflow task 2026-10-27 \"Make the repository ... Company Planning compliant. It has no planning package yet: build one.\" (Brian's standing request, 2026-10-25: \"i have asked 100s of times to make ure that my proejcts are always company plannign complaint\"). The package describes commit c1b3ee6: origin/main at 30e9993 plus the commit that adds docs/planning/, the review page and one wiki/index.md link; later commits on the branch change package files only.",
  "parts": {
   "checks": {
    "status": "present",
    "path": "docs/planning/checks.txt",
    "results": [
     {
      "name": "durable documents (arc42)",
      "command": "python3 $HOME/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --repo . --arc42",
      "exit_status": 1,
      "counts": {
       "findings": 1,
       "catalog_stale": 1
      },
      "tracked_by": "Q3"
     },
     {
      "name": "project navigation",
      "command": "python3 $HOME/code2/company-planning/plugins/company-planning/scripts/validate_project_navigation.py .",
      "exit_status": 0,
      "counts": {
       "warnings": 2
      },
      "tracked_by": "Q8"
     },
     {
      "name": "plan adoption recheck",
      "command": "python3 $HOME/code2/company-planning/plugins/company-planning/scripts/method_conformance/cli.py lint --repo-root . --recheck",
      "exit_status": 1,
      "counts": {
       "current": 0,
       "stale": 23,
       "finished": 0
      },
      "tracked_by": "Q4"
     },
     {
      "name": "wiki rule (Markdown cap, reachability, layout, durable documents)",
      "command": "python3 $HOME/code/project-meta/scripts/md_file_cap.py --repo . --ref HEAD",
      "exit_status": 1,
      "counts": {
       "markdown_files": 213,
       "cap_limit": 140,
       "over": 1,
       "orphans": 0,
       "layout_findings": 0,
       "durable_findings": 1
      },
      "tracked_by": "Q7"
     },
     {
      "name": "repository's own AES gate (target validate, topology check, status)",
      "command": "make aes",
      "exit_status": 0,
      "counts": {
       "criteria_supported": 2,
       "criteria_insufficient": 10,
       "criteria_refuted": 0,
       "orphans": 0,
       "drifted": 0,
       "observations_current": 4,
       "observations_stale": 50,
       "plans_unreachable": 1
      },
      "tracked_by": "Q6"
     },
     {
      "name": "typed-graph/v1 schema (domain graph and open-questions map)",
      "command": "jsonschema against $HOME/code2/representation-router/schemas/typed-graph.schema.json (inline in checks.txt)",
      "exit_status": 0,
      "counts": {
       "graphs_valid": 2,
       "graphs_invalid": 0
      }
     }
    ]
   },
   "open_questions": {
    "status": "present",
    "path": "docs/planning/open-questions.json"
   },
   "system_model": {
    "status": "present",
    "path": "docs/planning/SYSTEM_MODEL.md",
    "executes_typed_rules": false,
    "basis": "src/agentic_engineering_system/evidence.py:447"
   },
   "domain_model": {
    "status": "present",
    "path": "docs/planning/domain.graph.json",
    "glossary": "docs/planning/DOMAIN.md",
    "implemented": {
     "target": "src/agentic_engineering_system/records.py:137",
     "outcome": "src/agentic_engineering_system/records.py:65",
     "normative-item": "src/agentic_engineering_system/records.py:73",
     "success-criterion": "src/agentic_engineering_system/records.py:86",
     "evidence-requirement": "src/agentic_engineering_system/records.py:80",
     "component": "src/agentic_engineering_system/records.py:94",
     "planned-artifact": "src/agentic_engineering_system/records.py:105",
     "verification-subject": "src/agentic_engineering_system/records.py:116",
     "external-boundary": "src/agentic_engineering_system/records.py:126",
     "governed-root": "src/agentic_engineering_system/records.py:198",
     "project-record": "src/agentic_engineering_system/records.py:194",
     "proposal": "src/agentic_engineering_system/planning.py:168",
     "target-delta": "src/agentic_engineering_system/planning.py:137",
     "accepted-plan": "src/agentic_engineering_system/planning.py:197",
     "trace-review-declaration": "src/agentic_engineering_system/planning.py:148",
     "observation": "src/agentic_engineering_system/evidence.py:176",
     "assessment": "src/agentic_engineering_system/evidence.py:96",
     "negative-control": "src/agentic_engineering_system/evidence.py:112",
     "freshness": "src/agentic_engineering_system/evidence.py:376",
     "standing": "src/agentic_engineering_system/evidence.py:426",
     "characterization": "src/agentic_engineering_system/characterize.py:59",
     "drift": "src/agentic_engineering_system/characterize.py:204",
     "orphan": "src/agentic_engineering_system/topology.py:73",
     "gap": "src/agentic_engineering_system/reconcile.py:113",
     "reconciliation": "src/agentic_engineering_system/reconcile.py:259",
     "legacy-baseline": "src/agentic_engineering_system/adopt.py:48",
     "working-context": "src/agentic_engineering_system/context.py:72",
     "pre-commit-hook": "src/agentic_engineering_system/hooks.py:83",
     "repository-context": "src/agentic_engineering_system/repository_context/models.py:87",
     "project-brain": "scripts/hive/brain_fresh.py:35"
    }
   },
   "diagrams": {
    "status": "present",
    "items": [
     {
      "path": "docs/planning/SYSTEM_MODEL.md",
      "question": "What is inside AES and what talks to it, and which part of the repository writes which .aes/ store? (context and container views)"
     },
     {
      "path": "docs/planning/domain.graph.json",
      "question": "What ideas does AES work with (target records, plans, evidence, state), which exist in code and which only in documents or history, and how do they relate?"
     },
     {
      "path": "docs/planning/open-questions.graph.json",
      "question": "Which questions are still open, whose call is each, what does each block, and which concepts does it bear on?"
     }
    ]
   },
   "plan": {
    "status": "present",
    "path": "docs/planning/next.goal.md",
    "relies_on": [
     "accepted-plan",
     "observation",
     "freshness",
     "standing",
     "success-criterion",
     "verification-subject",
     "thesis",
     "commit-rule",
     "project-brain"
    ]
   },
   "review_page": {
    "status": "present",
    "path": "proposals/planning-package/review-page/index.html",
    "url": "https://hive.brianmills.dev/plans/main/proposals/planning-package/review-page/index.html"
   },
   "cold_review": {
    "status": "missing"
   }
  }
 },
 "questions": [
  {
   "id": "Q1",
   "short": "Resume, hold or retire AES",
   "question": "AES canonical has been on hold since 2026-10-18 after the ~/code2 move to off-the-shelf tools. Should it stay on hold (kept as a working library two repositories still call), resume as a product, or be retired and archived?",
   "blocks": "whether any plan beyond keeping the repository's own checks honest is worth doing here, and whether dodaf and whygame5 should keep calling aes",
   "resolves_with": "Brian's priority call; no check settles it. The facts that bear on it are recorded: the value tally came back at 1 catch and 6 hand checks (Decision 0011), and 2 of 12 criteria are supported today (make aes).",
   "owner": "brian",
   "status": "open",
   "recommendation": "Keep it on hold. Run only the hygiene plan (docs/planning/next.goal.md) so the repository tells the truth about itself, and leave the aes CLI working for dodaf and whygame5.",
   "default": "AES stays on hold; agents run the hygiene plan and nothing else here.",
   "sources": [
    ".project-brain/now.md:3",
    "docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:76",
    "/home/brian/code2/dodaf/Makefile:57",
    "/home/brian/code2/whygame5/Makefile:9"
   ],
   "touches": [
    "thesis",
    "value-tally",
    "north-star"
   ]
  },
  {
   "id": "Q2",
   "short": "Inside Success rollout",
   "question": "Decision 0011 paused the Inside Success team rollout until whygame5 produced a result under AES; that condition was met on 2026-09-26 and the call to resume was never made. Resume it, or close it?",
   "blocks": "whether Decision 0011 item 4 stays open or is closed in a follow-up decision record",
   "resolves_with": "Brian's business call; no check settles it.",
   "owner": "brian",
   "status": "open",
   "recommendation": "Close it: AES is on hold, so there is no product to roll out. Record the closure as a short follow-up decision in the hygiene plan.",
   "default": "The rollout stays paused and Decision 0011 item 4 stays as written.",
   "sources": [
    "docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:59",
    "docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:80"
   ],
   "touches": [
    "value-tally"
   ]
  },
  {
   "id": "Q3",
   "short": "Stale docstring wiki",
   "question": "The durable-documents check fails with CATALOG-STALE because generated/docstring_wiki.md was not regenerated after later commits. Is regenerating it all that is needed?",
   "blocks": "the durable-documents check and the wiki-compliance check's durable column passing",
   "resolves_with": "An argument already settles the cause: regenerating in a scratch copy changes the counts from 1102 to 1098 tracked artifacts and 1061 to 1010 missing docstrings, so the file is simply behind the code. The fix is `make docstring-wiki` and a commit, then rerun the check; it is open only because this package touches docs/planning/ alone.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "Makefile:632",
    "docs/planning/checks.txt:1"
   ],
   "touches": [
    "project-brain"
   ]
  },
  {
   "id": "Q4",
   "short": "23 plans adopted, none continuing",
   "question": "23 plan receipts were adopted under older bounded-design revisions (4 to 13; current 18), and none of those plans carries a finished status, while the project brain says none of that work continues. Which are finished, which superseded by the 2026-10-13 redirect, and which (if any) still in progress?",
   "blocks": "the plan-adoption recheck passing, and which plan this package may treat as current",
   "resolves_with": "Reading each plan against what merged settles it (an argument per plan, no test): plans about the commit rule are superseded by its removal on 2026-10-14; the rest get done or superseded from their own records. Then set each plan's front-matter status.",
   "owner": "agent",
   "status": "open",
   "sources": [
    ".project-brain/now.md:3",
    "docs/planning/checks.txt:1"
   ],
   "touches": [
    "accepted-plan",
    "commit-rule"
   ]
  },
  {
   "id": "Q5",
   "short": "Thesis still names the commit rule",
   "question": "GOAL.md's thesis and disproof still cite the commit rule (\"a commit refused without an adopted plan\"; agents routing around it), which was removed on 2026-10-14. What do the thesis and disproof say without it?",
   "blocks": "whether the goal document can be used to judge AES at all, and the wording of the hygiene plan's goal edit",
   "resolves_with": "An argument settles it: the two remaining checked boundaries (fresh revision-bound evidence; truth where it is edited) carry the thesis, and the disproof's third clause is dropped or rewritten against the pre-commit orphan check. A doc edit, no test.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/architecture/GOAL.md:45",
    "docs/architecture/GOAL.md:56",
    "docs/model/ODD.md:55"
   ],
   "touches": [
    "thesis",
    "commit-rule",
    "pre-commit-hook"
   ]
  },
  {
   "id": "Q6",
   "short": "Evidence went stale: 2 of 12 supported",
   "question": "Decision 0010 accepted v0.2 at 9 supported criteria; `make aes` at 30e9993 reports 2 supported, 10 insufficient, 50 stale observations and one unreachable accepted plan. Is the product still what Decision 0010 accepted, or did a change break it?",
   "blocks": "whether `aes status` can be quoted as the product's state, and whether Decision 0010's acceptance still stands",
   "resolves_with": "Running the existing verification subjects settles it, no new evaluation: `aes evidence record <VS-ID>` for each of the 14 subjects re-runs its named tests at HEAD. All passing means the evidence was only stale; any failure is a regression with a named test. The unreachable plan PLAN-AES-SELF-GOVERN gets superseded_by.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/decisions/0010-greenfield-v0.2-accepted.md:63",
    "docs/planning/checks.txt:1"
   ],
   "touches": [
    "observation",
    "freshness",
    "standing",
    "success-criterion",
    "verification-subject",
    "accepted-plan"
   ]
  },
  {
   "id": "Q7",
   "short": "213 Markdown files, cap 140",
   "question": "The repository holds 213 tracked Markdown files at c1b3ee6 (210 on main plus this package's three; its cold review adds a fourth) against its own 140-file exception (written 2026-10-07 at about 130, 146 a day later). Archive history out of the repository, or raise the limit with a new reason?",
   "blocks": "the wiki-compliance check passing",
   "resolves_with": "An argument settles it: the growth is proposals/ and docs/plans/ records of the commit-rule and enforcement work that the 2026-10-13 redirect ended, and the exception's own reason says limit growth should trip the check. Move the superseded plan bundles to ~/archive (after a content check, restore steps recorded) only where nothing cites them; raise the limit, with the count of cited files as its reason, for the rest.",
   "owner": "agent",
   "status": "open",
   "sources": [
    ".md-file-cap.yaml:1",
    ".md-file-cap.yaml:6",
    "docs/planning/checks.txt:1"
   ],
   "touches": [
    "commit-rule"
   ]
  },
  {
   "id": "Q8",
   "short": "No roadmap front door",
   "question": "The navigation check warns that no roadmap front door exists (no roadmap/README.md, docs/ROADMAP.md or ROADMAP.md, none linked from wiki/index.md), although .agentic/repo.yaml names one. Link it or add one?",
   "blocks": "the navigation check's two warnings",
   "resolves_with": "Prior art in the repository settles it: .agentic/repo.yaml already names active_roadmap proposals/aes-v0.2-greenfield/25-roadmap-to-mvp-acceptance.md; link that file from wiki/index.md under a Roadmap line, noting the on-hold status.",
   "owner": "agent",
   "status": "open",
   "sources": [
    ".agentic/repo.yaml:34",
    "docs/planning/checks.txt:1"
   ],
   "touches": []
  },
  {
   "id": "Q10",
   "short": "Vendored claims machinery",
   "question": "enforced_planning/ (44,556 lines of claims, sessions and worktree lanes) and the scripts/meta coordination scripts that import it are still in the repository, but ~/code2 replaced claims with claude -w worktrees. Keep, or retire them?",
   "blocks": "how much of the repository the system model must describe, and the size of the hygiene plan",
   "resolves_with": "Depends on Q1. If AES stays on hold, an argument settles it: leave them in place, unmodelled and labelled as retired by the ~/code2 redirect, because removing 44k lines of code another session may own is not hygiene. If AES resumes, a separate plan.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "/home/brian/code2/AGENTS.md:19",
    "scripts/meta/session_finish.py:18"
   ],
   "touches": []
  },
  {
   "id": "Q9",
   "short": "Does AES execute typed rules?",
   "question": "Does AES evaluate typed rules (relations with named roles whose effects run), which would need a type-level metamodel mapped onto the shared kernel?",
   "blocks": "whether the system model needs a metamodel",
   "resolves_with": "Reading the code settles it.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "No. Its rules are fixed Python functions over typed records, for example assess (src/agentic_engineering_system/evidence.py:447) and reconcile (reconcile.py:259); no target record defines a rule whose effect AES evaluates.",
   "sources": [
    "src/agentic_engineering_system/evidence.py:447",
    "src/agentic_engineering_system/reconcile.py:259"
   ],
   "touches": [
    "standing",
    "reconciliation"
   ]
  },
  {
   "id": "Q11",
   "short": "AES commit replay check",
   "question": "Does the `aes commit replay` check apply to this repository?",
   "blocks": "which checks the package lists",
   "resolves_with": "Reading the record settles it.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "No. The commit rule and `aes commit` were removed on 2026-10-14 (ODD.md line 55), and the planning-compliance skill retires AES commit rules in ~/code2 from 2026-10-13.",
   "sources": [
    "docs/model/ODD.md:55",
    ".project-brain/now.md:3"
   ],
   "touches": [
    "commit-rule"
   ]
  },
  {
   "id": "Q12",
   "short": "Who still depends on aes",
   "question": "Ten repositories under ~/code2 carry an .aes/ folder. Which still run the aes CLI, so that a retirement would break them?",
   "blocks": "the cost side of Q1",
   "resolves_with": "Searching their Makefiles and hooks settles it.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Two: dodaf (Makefile aes-gate, line 57, installs aes from this repository) and whygame5 (Makefile lines 6-10). The other eight carry .aes/ records but no hook or make target names aes (grep of .git/hooks/pre-commit, lefthook.yml and Makefile, 2026-10-27).",
   "sources": [
    "/home/brian/code2/dodaf/Makefile:57",
    "/home/brian/code2/whygame5/Makefile:9"
   ],
   "touches": [
    "project-record"
   ]
  },
  {
   "id": "Q13",
   "short": "Is the aes gate healthy",
   "question": "Do the repository's own AES gates (target validate, topology check, status) still pass at HEAD?",
   "blocks": "whether the plan must repair the CLI before anything else",
   "resolves_with": "Running make aes settles it.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Yes: make aes exits 0 at 30e9993: target valid (2 outcomes, 12 criteria, 44 planned artifacts, 14 verification subjects), 42 governed files and 0 orphans, 44 artifacts realized and 0 drifted. Its evidence counts are Q6.",
   "sources": [
    "Makefile:571",
    "docs/planning/checks.txt:1"
   ],
   "touches": [
    "reconciliation",
    "orphan",
    "drift"
   ]
  },
  {
   "id": "Q14",
   "short": "Leftover commit-rule config",
   "question": ".aes/commit_rule.yaml still sets the commit rule to observe mode. Does anything read it?",
   "blocks": "whether the hygiene plan deletes it",
   "resolves_with": "Searching the code settles it.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Nothing reads it: a search for commit_rule under src/ and scripts/ finds only a comment in topology.py line 18. The hygiene plan removes the file (it is in git history).",
   "sources": [
    ".aes/commit_rule.yaml:5",
    "src/agentic_engineering_system/topology.py:18"
   ],
   "touches": [
    "commit-rule"
   ]
  }
 ],
 "domain": {
  "schema": "typed-graph/v1",
  "kinds": {
   "Target": {
    "label": "Plan records (in code)",
    "color": "#1f5f99",
    "explain": "What .aes/target.yaml declares: outcomes, rules, criteria, components and the files planned for them."
   },
   "Change": {
    "label": "Changing the plan (in code)",
    "color": "#5f8fc2",
    "explain": "How the target changes: a proposal with a delta, accepted into a plan record."
   },
   "Evidence": {
    "label": "Evidence (in code)",
    "color": "#3b78b8",
    "explain": "Observations bound to a commit, their freshness, and the standing they give each criterion."
   },
   "State": {
    "label": "Current state (in code)",
    "color": "#2b4c6f",
    "explain": "What HEAD contains, how it differs from the plan, and the gaps that remain."
   },
   "Context": {
    "label": "Context and project records (in code)",
    "color": "#7a8fa6",
    "explain": "Project settings, the working-context packet, the v0.1 repository context, and the project brain."
   },
   "DocOnly": {
    "label": "Only in documents",
    "color": "#d9822b",
    "explain": "Named in the goal, decisions or plans, with no code here that implements it.",
    "dashed": true
   },
   "Retired": {
    "label": "Retired (history)",
    "color": "#9aa3ad",
    "explain": "Removed on 2026-10-14; documents still describe it.",
    "dashed": true
   }
  },
  "layout": {
   "direction": "RIGHT",
   "algorithm": "layered"
  },
  "nodes": [
   {
    "id": "target",
    "label": "Target",
    "kind": "Target",
    "explain": "The plan of record, .aes/target.yaml: outcomes, normative items, success criteria, components, planned artifacts and verification subjects. Defined in docs/model/ODD.md:33. Code: src/agentic_engineering_system/records.py:137."
   },
   {
    "id": "outcome",
    "label": "Outcome",
    "kind": "Target",
    "explain": "What an actor or consumer gets (OUT-GF-001, OUT-AP-001), with its non-goals. Defined in docs/architecture/GOAL.md:12. Code: src/agentic_engineering_system/records.py:65."
   },
   {
    "id": "normative-item",
    "label": "Normative item",
    "kind": "Target",
    "explain": "A constraint, behavior, invariant or quality the system must hold, tied to outcomes. Defined in docs/architecture/GOAL.md:11. Code: src/agentic_engineering_system/records.py:73."
   },
   {
    "id": "success-criterion",
    "label": "Success criterion",
    "kind": "Target",
    "explain": "A checkable statement with a disproof and one or more evidence requirements; its standing decides whether it is a gap. Defined in docs/architecture/GOAL.md:11. Code: src/agentic_engineering_system/records.py:86."
   },
   {
    "id": "evidence-requirement",
    "label": "Evidence requirement",
    "kind": "Target",
    "explain": "One kind of evidence a criterion needs (deterministic test, runtime observation, human review or trace review); assessed one at a time, never per criterion. Defined in src/agentic_engineering_system/evidence.py:5. Code: src/agentic_engineering_system/records.py:80."
   },
   {
    "id": "component",
    "label": "Component",
    "kind": "Target",
    "explain": "A responsibility (RU-AES-*) that owns planned artifacts; `aes status` reports the first open gap per component. Defined in docs/model/ODD.md:33. Code: src/agentic_engineering_system/records.py:94."
   },
   {
    "id": "planned-artifact",
    "label": "Planned artifact",
    "kind": "Target",
    "explain": "A file at an exact path that the target plans; every file under a governed root must be one. Defined in src/agentic_engineering_system/topology.py:3. Code: src/agentic_engineering_system/records.py:105."
   },
   {
    "id": "verification-subject",
    "label": "Verification subject",
    "kind": "Target",
    "explain": "The test or check (with its proof role, direct or negative control) that routes evidence to a criterion's requirements. Defined in docs/model/ODD.md:33. Code: src/agentic_engineering_system/records.py:116."
   },
   {
    "id": "external-boundary",
    "label": "External boundary",
    "kind": "Target",
    "explain": "An evidence requirement routed outside the repository (a human review, an outside system) instead of to a local test. Defined in docs/model/ODD.md:33. Code: src/agentic_engineering_system/records.py:126."
   },
   {
    "id": "governed-root",
    "label": "Governed root",
    "kind": "Context",
    "explain": "A folder AES governs (src/agentic_engineering_system/, tests/greenfield/); only files there must be planned. Defined in AGENTS.md:33. Code: src/agentic_engineering_system/records.py:198."
   },
   {
    "id": "project-record",
    "label": "Project record",
    "kind": "Context",
    "explain": ".aes/project.yaml: project id, governed roots and where target, plans and observations live. Defined in src/agentic_engineering_system/topology.py:3. Code: src/agentic_engineering_system/records.py:194."
   },
   {
    "id": "proposal",
    "label": "Proposal",
    "kind": "Change",
    "explain": "A target delta plus the gaps it claims to close, checked by `aes plan validate` before it is accepted. Defined in docs/model/ODD.md:34. Code: src/agentic_engineering_system/planning.py:168."
   },
   {
    "id": "target-delta",
    "label": "Target delta",
    "kind": "Change",
    "explain": "The entries a proposal adds, replaces or removes in the target. Defined in docs/model/ODD.md:34. Code: src/agentic_engineering_system/planning.py:137."
   },
   {
    "id": "accepted-plan",
    "label": "Accepted plan",
    "kind": "Change",
    "explain": "A proposal applied by `aes plan accept`, kept in .aes/plans/ with the revision it was accepted at. Defined in AGENTS.md:39. Code: src/agentic_engineering_system/planning.py:197."
   },
   {
    "id": "trace-review-declaration",
    "label": "Trace-review declaration",
    "kind": "Change",
    "explain": "A proposal's statement of whether its work runs; work that runs needs a trace-review requirement (RULE-TRACE-REVIEW-DECLARED). Defined in docs/model/ODD.md:27. Code: src/agentic_engineering_system/planning.py:148."
   },
   {
    "id": "observation",
    "label": "Observation",
    "kind": "Evidence",
    "explain": "An append-only evidence record in .aes/observations/, bound to the commit it observed and the paths and target entries it depends on. Defined in docs/model/ODD.md:35. Code: src/agentic_engineering_system/evidence.py:176."
   },
   {
    "id": "assessment",
    "label": "Assessment",
    "kind": "Evidence",
    "explain": "An observation's verdict on one evidence requirement: SUPPORTS, REFUTES or INCONCLUSIVE. Defined in src/agentic_engineering_system/evidence.py:5. Code: src/agentic_engineering_system/evidence.py:96."
   },
   {
    "id": "negative-control",
    "label": "Negative control",
    "kind": "Evidence",
    "explain": "A case a control should refuse, recorded with whether it was detected; controls must prove they can fail (AES-POL-004). Defined in docs/architecture/GOAL.md:23. Code: src/agentic_engineering_system/evidence.py:112."
   },
   {
    "id": "freshness",
    "label": "Freshness",
    "kind": "Evidence",
    "explain": "CURRENT, STALE, UNKNOWN or UNREACHABLE, computed from Git: an observation is stale once a path or entry it depends on changes after its commit. Defined in src/agentic_engineering_system/evidence.py:9. Code: src/agentic_engineering_system/evidence.py:376."
   },
   {
    "id": "standing",
    "label": "Criterion standing",
    "kind": "Evidence",
    "explain": "SUPPORTED, REFUTED or INSUFFICIENT for each criterion; only current assessments count, and ignorance never renders green. Defined in docs/architecture/GOAL.md:21. Code: src/agentic_engineering_system/evidence.py:426."
   },
   {
    "id": "characterization",
    "label": "Characterization",
    "kind": "State",
    "explain": "What HEAD contains under the governed roots: each file's blob and its Python symbols. Defined in docs/model/ODD.md:36. Code: src/agentic_engineering_system/characterize.py:59."
   },
   {
    "id": "drift",
    "label": "Drift",
    "kind": "State",
    "explain": "A planned artifact whose committed symbols or signatures no longer match the target (formatting alone is not drift). Defined in docs/model/ODD.md:18. Code: src/agentic_engineering_system/characterize.py:204."
   },
   {
    "id": "orphan",
    "label": "Orphan",
    "kind": "State",
    "explain": "A tracked file under a governed root that the target does not plan; `aes topology check` fails on it. Defined in src/agentic_engineering_system/topology.py:3. Code: src/agentic_engineering_system/topology.py:73."
   },
   {
    "id": "gap",
    "label": "Gap",
    "kind": "State",
    "explain": "An unmet criterion or requirement that stays open until fresh evidence supports it. Defined in docs/model/ODD.md:22. Code: src/agentic_engineering_system/reconcile.py:113."
   },
   {
    "id": "reconciliation",
    "label": "Reconciliation",
    "kind": "State",
    "explain": "`aes status` / `aes reconcile`: artifacts, criteria, observations and plans composed into current state and first gap per component. Defined in docs/model/ODD.md:43. Code: src/agentic_engineering_system/reconcile.py:259."
   },
   {
    "id": "legacy-baseline",
    "label": "Legacy baseline",
    "kind": "State",
    "explain": "`aes adopt`: today's governed files in an existing repository accepted as legacy, without claiming conformance. Defined in docs/architecture/GOAL.md:61. Code: src/agentic_engineering_system/adopt.py:48."
   },
   {
    "id": "working-context",
    "label": "Working context",
    "kind": "Context",
    "explain": "`aes context <subject>`: the smallest complete packet of full-text rules and criteria for one subject, with what was left out listed. Defined in src/agentic_engineering_system/context.py:1. Code: src/agentic_engineering_system/context.py:72."
   },
   {
    "id": "pre-commit-hook",
    "label": "Pre-commit hook",
    "kind": "Context",
    "explain": "The hook `aes hooks install` writes; it refuses a commit that leaves an orphan under a governed root. Defined in AGENTS.md:39. Code: src/agentic_engineering_system/hooks.py:83."
   },
   {
    "id": "repository-context",
    "label": "Repository context (v0.1)",
    "kind": "Context",
    "explain": "The v0.1 Plan 001 artifact: authority surfaces and concern roots resolved from a checkout, with unresolved surfaces kept visible. Defined in docs/plans/001_repository_context_resolution_vertical.md:1. Code: src/agentic_engineering_system/repository_context/models.py:87."
   },
   {
    "id": "project-brain",
    "label": "Project brain",
    "kind": "Context",
    "explain": "The .project-brain/ files (now, state, truth, project) an agent reads first; a script reports when they are older than the work since. Defined in CLAUDE.md:5. Code: scripts/hive/brain_fresh.py:35."
   },
   {
    "id": "thesis",
    "label": "Checked-boundary thesis",
    "kind": "DocOnly",
    "explain": "The bet that agent-built software stays true to intent when every claim is checked against something an agent cannot talk past; with its disproof, still unmeasured. Defined in docs/architecture/GOAL.md:42. No code.",
    "dashed": true
   },
   {
    "id": "north-star",
    "label": "Colleague starts a new project",
    "kind": "DocOnly",
    "explain": "OUT-GF-001's north star: a colleague without private repositories takes a new project from intent to evidence-backed state. Defined in docs/architecture/GOAL.md:37. No code.",
    "dashed": true
   },
   {
    "id": "value-tally",
    "label": "Value tally",
    "kind": "DocOnly",
    "explain": "Decision 0011's pre-registered measure: AES catches versus hand checks a person still needed (whygame5: 1 catch, 6 hand checks). Defined in docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:64. No code.",
    "dashed": true
   },
   {
    "id": "offline-policy-replay",
    "label": "Offline policy-decision replay (v0.1)",
    "kind": "DocOnly",
    "explain": "Plan 002, the v0.1 frontier, stopped at its provider-access step; no code here implements it. Defined in docs/plans/002_offline_policy_decision_replay.md:3. No code.",
    "dashed": true
   },
   {
    "id": "commit-rule",
    "label": "Commit rule",
    "kind": "Retired",
    "explain": "Commit tags and plan adoption per commit; removed on 2026-10-14 at Brian's request. .aes/commit_rule.yaml remains, read by no code. Defined in docs/model/ODD.md:55. No code.",
    "dashed": true
   }
  ],
  "edges": [
   {
    "id": "e0",
    "source": "target",
    "target": "outcome",
    "label": "declares"
   },
   {
    "id": "e1",
    "source": "target",
    "target": "normative-item",
    "label": "declares"
   },
   {
    "id": "e2",
    "source": "target",
    "target": "success-criterion",
    "label": "declares"
   },
   {
    "id": "e3",
    "source": "target",
    "target": "component",
    "label": "declares"
   },
   {
    "id": "e4",
    "source": "target",
    "target": "planned-artifact",
    "label": "declares"
   },
   {
    "id": "e5",
    "source": "target",
    "target": "verification-subject",
    "label": "declares"
   },
   {
    "id": "e6",
    "source": "target",
    "target": "external-boundary",
    "label": "declares"
   },
   {
    "id": "e7",
    "source": "normative-item",
    "target": "outcome",
    "label": "serves"
   },
   {
    "id": "e8",
    "source": "success-criterion",
    "target": "normative-item",
    "label": "checks"
   },
   {
    "id": "e9",
    "source": "success-criterion",
    "target": "evidence-requirement",
    "label": "needs"
   },
   {
    "id": "e10",
    "source": "component",
    "target": "planned-artifact",
    "label": "owns"
   },
   {
    "id": "e11",
    "source": "verification-subject",
    "target": "evidence-requirement",
    "label": "routes evidence to"
   },
   {
    "id": "e12",
    "source": "external-boundary",
    "target": "evidence-requirement",
    "label": "routes evidence to"
   },
   {
    "id": "e13",
    "source": "project-record",
    "target": "governed-root",
    "label": "names"
   },
   {
    "id": "e14",
    "source": "project-record",
    "target": "target",
    "label": "locates"
   },
   {
    "id": "e15",
    "source": "planned-artifact",
    "target": "governed-root",
    "label": "lives under"
   },
   {
    "id": "e16",
    "source": "proposal",
    "target": "target-delta",
    "label": "carries"
   },
   {
    "id": "e17",
    "source": "proposal",
    "target": "gap",
    "label": "claims to close"
   },
   {
    "id": "e18",
    "source": "proposal",
    "target": "trace-review-declaration",
    "label": "carries"
   },
   {
    "id": "e19",
    "source": "accepted-plan",
    "target": "proposal",
    "label": "is an accepted"
   },
   {
    "id": "e20",
    "source": "target-delta",
    "target": "target",
    "label": "changes"
   },
   {
    "id": "e21",
    "source": "verification-subject",
    "target": "observation",
    "label": "produces"
   },
   {
    "id": "e22",
    "source": "observation",
    "target": "assessment",
    "label": "holds one per requirement"
   },
   {
    "id": "e23",
    "source": "assessment",
    "target": "evidence-requirement",
    "label": "judges"
   },
   {
    "id": "e24",
    "source": "observation",
    "target": "freshness",
    "label": "has"
   },
   {
    "id": "e25",
    "source": "observation",
    "target": "negative-control",
    "label": "may record"
   },
   {
    "id": "e26",
    "source": "standing",
    "target": "success-criterion",
    "label": "is the standing of"
   },
   {
    "id": "e27",
    "source": "assessment",
    "target": "standing",
    "label": "counts toward, when current"
   },
   {
    "id": "e28",
    "source": "characterization",
    "target": "planned-artifact",
    "label": "describes"
   },
   {
    "id": "e29",
    "source": "drift",
    "target": "planned-artifact",
    "label": "found in"
   },
   {
    "id": "e30",
    "source": "orphan",
    "target": "governed-root",
    "label": "found under"
   },
   {
    "id": "e31",
    "source": "reconciliation",
    "target": "characterization",
    "label": "reads"
   },
   {
    "id": "e32",
    "source": "reconciliation",
    "target": "standing",
    "label": "reads"
   },
   {
    "id": "e33",
    "source": "reconciliation",
    "target": "gap",
    "label": "reports"
   },
   {
    "id": "e34",
    "source": "reconciliation",
    "target": "drift",
    "label": "reports"
   },
   {
    "id": "e35",
    "source": "legacy-baseline",
    "target": "governed-root",
    "label": "accepts files under"
   },
   {
    "id": "e36",
    "source": "working-context",
    "target": "component",
    "label": "compiled for"
   },
   {
    "id": "e37",
    "source": "pre-commit-hook",
    "target": "orphan",
    "label": "refuses"
   },
   {
    "id": "e38",
    "source": "thesis",
    "target": "standing",
    "label": "rests on"
   },
   {
    "id": "e39",
    "source": "north-star",
    "target": "outcome",
    "label": "is the aim of"
   },
   {
    "id": "e40",
    "source": "value-tally",
    "target": "thesis",
    "label": "measures"
   },
   {
    "id": "e41",
    "source": "commit-rule",
    "target": "accepted-plan",
    "label": "required, per commit"
   },
   {
    "id": "e42",
    "source": "offline-policy-replay",
    "target": "repository-context",
    "label": "builds on"
   }
  ]
 },
 "question_map": {
  "schema": "typed-graph/v1",
  "kinds": {
   "AgentQuestion": {
    "label": "Agent question (checking can settle it)",
    "color": "#3b6fa8",
    "explain": "An open question an agent settles by argument, prior art or a run."
   },
   "BrianQuestion": {
    "label": "Brian's call",
    "color": "#d9822b",
    "explain": "An open question only Brian can decide; it carries a recommendation and a default."
   },
   "Decision": {
    "label": "Decision it blocks",
    "color": "#4a525c",
    "explain": "The decision or next step that waits on the question."
   },
   "Concept": {
    "label": "Domain concept",
    "color": "#9aa3ad",
    "explain": "A concept from docs/planning/domain.graph.json that the question bears on."
   }
  },
  "layout": {
   "direction": "RIGHT",
   "algorithm": "layered"
  },
  "nodes": [
   {
    "id": "Q1",
    "label": "Q1: Resume, hold or retire AES",
    "kind": "BrianQuestion",
    "explain": "AES canonical has been on hold since 2026-10-18 after the ~/code2 move to off-the-shelf tools. Should it stay on hold (kept as a working library two repositories still call), resume as a product, or be retired and archived? Recommendation: Keep it on hold. Run only the hygiene plan (docs/planning/next.goal.md) so the repository tells the truth about itself, and leave the aes CLI working for dodaf and whygame5. Default: AES stays on hold; agents run the hygiene plan and nothing else here."
   },
   {
    "id": "Q1-blocks",
    "label": "whether any plan beyond keeping the repository's own checks honest is worth doing here …",
    "kind": "Decision",
    "explain": "whether any plan beyond keeping the repository's own checks honest is worth doing here, and whether dodaf and whygame5 should keep calling aes"
   },
   {
    "id": "thesis",
    "label": "Checked-boundary thesis",
    "kind": "Concept",
    "dashed": true,
    "explain": "The bet that agent-built software stays true to intent when every claim is checked against something an agent cannot talk past; with its disproof, still unmeasured. Defined in docs/architecture/GOAL.md:42. No code."
   },
   {
    "id": "value-tally",
    "label": "Value tally",
    "kind": "Concept",
    "dashed": true,
    "explain": "Decision 0011's pre-registered measure: AES catches versus hand checks a person still needed (whygame5: 1 catch, 6 hand checks). Defined in docs/decisions/0011-inside-success-aes-archived-canonical-is-aes.md:64. No code."
   },
   {
    "id": "north-star",
    "label": "Colleague starts a new project",
    "kind": "Concept",
    "dashed": true,
    "explain": "OUT-GF-001's north star: a colleague without private repositories takes a new project from intent to evidence-backed state. Defined in docs/architecture/GOAL.md:37. No code."
   },
   {
    "id": "Q2",
    "label": "Q2: Inside Success rollout",
    "kind": "BrianQuestion",
    "explain": "Decision 0011 paused the Inside Success team rollout until whygame5 produced a result under AES; that condition was met on 2026-09-26 and the call to resume was never made. Resume it, or close it? Recommendation: Close it: AES is on hold, so there is no product to roll out. Record the closure as a short follow-up decision in the hygiene plan. Default: The rollout stays paused and Decision 0011 item 4 stays as written."
   },
   {
    "id": "Q2-blocks",
    "label": "whether Decision 0011 item 4 stays open or is closed in a follow-up decision record",
    "kind": "Decision",
    "explain": "whether Decision 0011 item 4 stays open or is closed in a follow-up decision record"
   },
   {
    "id": "Q3",
    "label": "Q3: Stale docstring wiki",
    "kind": "AgentQuestion",
    "explain": "The durable-documents check fails with CATALOG-STALE because generated/docstring_wiki.md was not regenerated after later commits. Is regenerating it all that is needed? Settled by: An argument already settles the cause: regenerating in a scratch copy changes the counts from 1102 to 1098 tracked artifacts and 1061 to 1010 missing docstrings, so the file is simply behind the code. The fix is `make docstring-wiki` and a commit, then rerun the check; it is open only because this package touches docs/planning/ alone."
   },
   {
    "id": "Q3-blocks",
    "label": "the durable-documents check and the wiki-compliance check's durable column passing",
    "kind": "Decision",
    "explain": "the durable-documents check and the wiki-compliance check's durable column passing"
   },
   {
    "id": "project-brain",
    "label": "Project brain",
    "kind": "Concept",
    "dashed": false,
    "explain": "The .project-brain/ files (now, state, truth, project) an agent reads first; a script reports when they are older than the work since. Defined in CLAUDE.md:5. Code: scripts/hive/brain_fresh.py:35."
   },
   {
    "id": "Q4",
    "label": "Q4: 23 plans adopted, none continuing",
    "kind": "AgentQuestion",
    "explain": "23 plan receipts were adopted under older bounded-design revisions (4 to 13; current 18), and none of those plans carries a finished status, while the project brain says none of that work continues. Which are finished, which superseded by the 2026-10-13 redirect, and which (if any) still in progress? Settled by: Reading each plan against what merged settles it (an argument per plan, no test): plans about the commit rule are superseded by its removal on 2026-10-14; the rest get done or superseded from their own records. Then set each plan's front-matter status."
   },
   {
    "id": "Q4-blocks",
    "label": "the plan-adoption recheck passing, and which plan this package may treat as current",
    "kind": "Decision",
    "explain": "the plan-adoption recheck passing, and which plan this package may treat as current"
   },
   {
    "id": "accepted-plan",
    "label": "Accepted plan",
    "kind": "Concept",
    "dashed": false,
    "explain": "A proposal applied by `aes plan accept`, kept in .aes/plans/ with the revision it was accepted at. Defined in AGENTS.md:39. Code: src/agentic_engineering_system/planning.py:197."
   },
   {
    "id": "commit-rule",
    "label": "Commit rule",
    "kind": "Concept",
    "dashed": true,
    "explain": "Commit tags and plan adoption per commit; removed on 2026-10-14 at Brian's request. .aes/commit_rule.yaml remains, read by no code. Defined in docs/model/ODD.md:55. No code."
   },
   {
    "id": "Q5",
    "label": "Q5: Thesis still names the commit rule",
    "kind": "AgentQuestion",
    "explain": "GOAL.md's thesis and disproof still cite the commit rule (\"a commit refused without an adopted plan\"; agents routing around it), which was removed on 2026-10-14. What do the thesis and disproof say without it? Settled by: An argument settles it: the two remaining checked boundaries (fresh revision-bound evidence; truth where it is edited) carry the thesis, and the disproof's third clause is dropped or rewritten against the pre-commit orphan check. A doc edit, no test."
   },
   {
    "id": "Q5-blocks",
    "label": "whether the goal document can be used to judge AES at all, and the wording of the hygiene …",
    "kind": "Decision",
    "explain": "whether the goal document can be used to judge AES at all, and the wording of the hygiene plan's goal edit"
   },
   {
    "id": "pre-commit-hook",
    "label": "Pre-commit hook",
    "kind": "Concept",
    "dashed": false,
    "explain": "The hook `aes hooks install` writes; it refuses a commit that leaves an orphan under a governed root. Defined in AGENTS.md:39. Code: src/agentic_engineering_system/hooks.py:83."
   },
   {
    "id": "Q6",
    "label": "Q6: Evidence went stale: 2 of 12 supported",
    "kind": "AgentQuestion",
    "explain": "Decision 0010 accepted v0.2 at 9 supported criteria; `make aes` at 30e9993 reports 2 supported, 10 insufficient, 50 stale observations and one unreachable accepted plan. Is the product still what Decision 0010 accepted, or did a change break it? Settled by: Running the existing verification subjects settles it, no new evaluation: `aes evidence record <VS-ID>` for each of the 14 subjects re-runs its named tests at HEAD. All passing means the evidence was only stale; any failure is a regression with a named test. The unreachable plan PLAN-AES-SELF-GOVERN gets superseded_by."
   },
   {
    "id": "Q6-blocks",
    "label": "whether `aes status` can be quoted as the product's state, and whether Decision 0010's …",
    "kind": "Decision",
    "explain": "whether `aes status` can be quoted as the product's state, and whether Decision 0010's acceptance still stands"
   },
   {
    "id": "observation",
    "label": "Observation",
    "kind": "Concept",
    "dashed": false,
    "explain": "An append-only evidence record in .aes/observations/, bound to the commit it observed and the paths and target entries it depends on. Defined in docs/model/ODD.md:35. Code: src/agentic_engineering_system/evidence.py:176."
   },
   {
    "id": "freshness",
    "label": "Freshness",
    "kind": "Concept",
    "dashed": false,
    "explain": "CURRENT, STALE, UNKNOWN or UNREACHABLE, computed from Git: an observation is stale once a path or entry it depends on changes after its commit. Defined in src/agentic_engineering_system/evidence.py:9. Code: src/agentic_engineering_system/evidence.py:376."
   },
   {
    "id": "standing",
    "label": "Criterion standing",
    "kind": "Concept",
    "dashed": false,
    "explain": "SUPPORTED, REFUTED or INSUFFICIENT for each criterion; only current assessments count, and ignorance never renders green. Defined in docs/architecture/GOAL.md:21. Code: src/agentic_engineering_system/evidence.py:426."
   },
   {
    "id": "success-criterion",
    "label": "Success criterion",
    "kind": "Concept",
    "dashed": false,
    "explain": "A checkable statement with a disproof and one or more evidence requirements; its standing decides whether it is a gap. Defined in docs/architecture/GOAL.md:11. Code: src/agentic_engineering_system/records.py:86."
   },
   {
    "id": "verification-subject",
    "label": "Verification subject",
    "kind": "Concept",
    "dashed": false,
    "explain": "The test or check (with its proof role, direct or negative control) that routes evidence to a criterion's requirements. Defined in docs/model/ODD.md:33. Code: src/agentic_engineering_system/records.py:116."
   },
   {
    "id": "Q7",
    "label": "Q7: 213 Markdown files, cap 140",
    "kind": "AgentQuestion",
    "explain": "The repository holds 213 tracked Markdown files at c1b3ee6 (210 on main plus this package's three; its cold review adds a fourth) against its own 140-file exception (written 2026-10-07 at about 130, 146 a day later). Archive history out of the repository, or raise the limit with a new reason? Settled by: An argument settles it: the growth is proposals/ and docs/plans/ records of the commit-rule and enforcement work that the 2026-10-13 redirect ended, and the exception's own reason says limit growth should trip the check. Move the superseded plan bundles to ~/archive (after a content check, restore steps recorded) only where nothing cites them; raise the limit, with the count of cited files as its reason, for the rest."
   },
   {
    "id": "Q7-blocks",
    "label": "the wiki-compliance check passing",
    "kind": "Decision",
    "explain": "the wiki-compliance check passing"
   },
   {
    "id": "Q8",
    "label": "Q8: No roadmap front door",
    "kind": "AgentQuestion",
    "explain": "The navigation check warns that no roadmap front door exists (no roadmap/README.md, docs/ROADMAP.md or ROADMAP.md, none linked from wiki/index.md), although .agentic/repo.yaml names one. Link it or add one? Settled by: Prior art in the repository settles it: .agentic/repo.yaml already names active_roadmap proposals/aes-v0.2-greenfield/25-roadmap-to-mvp-acceptance.md; link that file from wiki/index.md under a Roadmap line, noting the on-hold status."
   },
   {
    "id": "Q8-blocks",
    "label": "the navigation check's two warnings",
    "kind": "Decision",
    "explain": "the navigation check's two warnings"
   },
   {
    "id": "Q10",
    "label": "Q10: Vendored claims machinery",
    "kind": "AgentQuestion",
    "explain": "enforced_planning/ (44,556 lines of claims, sessions and worktree lanes) and the scripts/meta coordination scripts that import it are still in the repository, but ~/code2 replaced claims with claude -w worktrees. Keep, or retire them? Settled by: Depends on Q1. If AES stays on hold, an argument settles it: leave them in place, unmodelled and labelled as retired by the ~/code2 redirect, because removing 44k lines of code another session may own is not hygiene. If AES resumes, a separate plan."
   },
   {
    "id": "Q10-blocks",
    "label": "how much of the repository the system model must describe, and the size of the hygiene …",
    "kind": "Decision",
    "explain": "how much of the repository the system model must describe, and the size of the hygiene plan"
   }
  ],
  "edges": [
   {
    "id": "Q1-to-decision",
    "source": "Q1",
    "target": "Q1-blocks",
    "label": "blocks"
   },
   {
    "id": "Q1-thesis",
    "source": "Q1",
    "target": "thesis",
    "label": "bears on"
   },
   {
    "id": "Q1-value-tally",
    "source": "Q1",
    "target": "value-tally",
    "label": "bears on"
   },
   {
    "id": "Q1-north-star",
    "source": "Q1",
    "target": "north-star",
    "label": "bears on"
   },
   {
    "id": "Q2-to-decision",
    "source": "Q2",
    "target": "Q2-blocks",
    "label": "blocks"
   },
   {
    "id": "Q2-value-tally",
    "source": "Q2",
    "target": "value-tally",
    "label": "bears on"
   },
   {
    "id": "Q3-to-decision",
    "source": "Q3",
    "target": "Q3-blocks",
    "label": "blocks"
   },
   {
    "id": "Q3-project-brain",
    "source": "Q3",
    "target": "project-brain",
    "label": "bears on"
   },
   {
    "id": "Q4-to-decision",
    "source": "Q4",
    "target": "Q4-blocks",
    "label": "blocks"
   },
   {
    "id": "Q4-accepted-plan",
    "source": "Q4",
    "target": "accepted-plan",
    "label": "bears on"
   },
   {
    "id": "Q4-commit-rule",
    "source": "Q4",
    "target": "commit-rule",
    "label": "bears on"
   },
   {
    "id": "Q5-to-decision",
    "source": "Q5",
    "target": "Q5-blocks",
    "label": "blocks"
   },
   {
    "id": "Q5-thesis",
    "source": "Q5",
    "target": "thesis",
    "label": "bears on"
   },
   {
    "id": "Q5-commit-rule",
    "source": "Q5",
    "target": "commit-rule",
    "label": "bears on"
   },
   {
    "id": "Q5-pre-commit-hook",
    "source": "Q5",
    "target": "pre-commit-hook",
    "label": "bears on"
   },
   {
    "id": "Q6-to-decision",
    "source": "Q6",
    "target": "Q6-blocks",
    "label": "blocks"
   },
   {
    "id": "Q6-observation",
    "source": "Q6",
    "target": "observation",
    "label": "bears on"
   },
   {
    "id": "Q6-freshness",
    "source": "Q6",
    "target": "freshness",
    "label": "bears on"
   },
   {
    "id": "Q6-standing",
    "source": "Q6",
    "target": "standing",
    "label": "bears on"
   },
   {
    "id": "Q6-success-criterion",
    "source": "Q6",
    "target": "success-criterion",
    "label": "bears on"
   },
   {
    "id": "Q6-verification-subject",
    "source": "Q6",
    "target": "verification-subject",
    "label": "bears on"
   },
   {
    "id": "Q6-accepted-plan",
    "source": "Q6",
    "target": "accepted-plan",
    "label": "bears on"
   },
   {
    "id": "Q7-to-decision",
    "source": "Q7",
    "target": "Q7-blocks",
    "label": "blocks"
   },
   {
    "id": "Q7-commit-rule",
    "source": "Q7",
    "target": "commit-rule",
    "label": "bears on"
   },
   {
    "id": "Q8-to-decision",
    "source": "Q8",
    "target": "Q8-blocks",
    "label": "blocks"
   },
   {
    "id": "Q10-to-decision",
    "source": "Q10",
    "target": "Q10-blocks",
    "label": "blocks"
   }
  ]
 },
 "context_diagrams": [
  "flowchart LR\n  brian([Brian: planning authority])\n  agent([Coding agents: Claude Code, Codex])\n  aes[AES canonical<br/>the aes CLI and .aes records]\n  git[(Git: commits, blobs, history)]\n  consumers[Other repositories with .aes/<br/>dodaf and whygame5 run aes from make]\n  cp[Company Planning plugin<br/>design method, durable-docs check]\n  vps[personal-vps hive dashboard<br/>serves plan pages]\n  brian -->|decides scope, reads status and plan pages| aes\n  agent -->|aes plan / evidence record / status| aes\n  aes -->|reads commits and diffs for freshness and drift| git\n  consumers -->|install aes from this repository| aes\n  aes -->|v0.1 line names it as design provider| cp\n  vps -->|copies proposals/*/review-page/ every 15 minutes| aes\n",
  "flowchart TB\n  subgraph v02[v0.2 product: governed roots]\n    cli[aes CLI<br/>src/agentic_engineering_system/cli.py]\n    plan[planning.py<br/>proposals and accepted plans]\n    ev[evidence.py<br/>observations, freshness, standing]\n    rec[reconcile.py + characterize.py + topology.py<br/>state, drift, orphans, gaps]\n    ctx[context.py<br/>working-context packets]\n    hk[hooks.py<br/>pre-commit hook]\n  end\n  v01[repository_context/<br/>v0.1 Plan 001 resolver]\n  ep[enforced_planning/<br/>vendored claims, sessions, worktrees<br/>44,556 lines; retired in ~/code2]\n  scr[scripts/<br/>meta, hive, rules, catalogue, learning_loop]\n  docs[docs/, proposals/, research/, wiki/<br/>213 Markdown files]\n  t[(.aes/target.yaml)]\n  o[(.aes/observations/)]\n  p[(.aes/plans/)]\n  g[(.githooks/pre-commit)]\n  cli --> plan --> t\n  plan --> p\n  cli --> ev --> o\n  cli --> rec\n  rec -->|reads| t\n  rec -->|reads| o\n  cli --> ctx\n  cli --> hk --> g\n  scr -->|generate pages| docs\n"
 ],
 "disagreements": [
  "**The thesis still names the commit rule.** [GOAL.md](../architecture/GOAL.md) lines 44-46 and 55-57 describe \"a commit refused without an adopted plan\" as a checked boundary and its bypass as the disproof; the commit rule was removed on 2026-10-14 ([ODD.md](../model/ODD.md) line 55). Open question Q5.",
  "**Decision 0010 says accepted with 9 supported criteria; `aes status` now says 2 of 12.** The acceptance record ([0010](../decisions/0010-greenfield-v0.2-accepted.md) line 63) ended at 9 supported, 0 insufficient; at 30e9993, `make aes` reports 2 supported, 10 insufficient and 50 stale observations, because later commits changed the files that evidence depends on. Open question Q6.",
  "**The plan-receipt files say 23 plans are adopted and in progress; the project brain says nothing is being continued.** [now.md](../../.project-brain/now.md) line 3 (on hold since 2026-10-18). Open question Q4."
 ],
 "next_plan": "\n# Goal: AES on hold, checks honest\n\nPlanning package: docs/planning/planning-package.json\n\nStatus: proposed 2026-10-27, waiting on Brian's call Q1 (default: this goal runs).\n\n## Why this goal\n\nAES canonical is on hold ([now.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/.project-brain/now.md) line 3), but its own checks\nnow say things that are false or stale: three checks fail, `aes status` reports 2 of 12\ncriteria supported where Decision 0010 recorded 9, and the goal document's thesis still\nrests on the commit rule that was removed on 2026-10-14. While it stays on hold (the\nrecommended answer to Q1), the useful work is to make every check and document here true,\nand to keep the `aes` CLI working for dodaf and whygame5 (Q12). No new product work.\n\n## Done when\n\nEach line is checked by the command beside it; the package is rebuilt at the end.\n\n1. **Evidence re-recorded (Q6).** `aes evidence record <VS-ID>` run for each of the 14\n   verification subjects at HEAD; `make aes` shows the supported count, and any criterion that\n   does not return to SUPPORTED names the failing test. PLAN-AES-SELF-GOVERN carries\n   `superseded_by` so it is no longer reported unreachable.\n2. **Plan statuses true (Q4).** Each of the 23 plans in the recheck list has a front-matter\n   status of `done` or `superseded` (with the merge or decision that settled it), or stays\n   adopted with a reason; `cli.py lint --repo-root . --recheck` exits 0 or lists only those kept.\n3. **Docstring wiki current (Q3).** `make docstring-wiki` committed; `durable_docs_check.py --repo .\n   --arc42` exits 0.\n4. **Markdown count inside the cap (Q7).** Superseded plan bundles nothing cites moved to\n   `~/archive/agentic-engineering-system-canonical/<timestamp>/` after a content comparison, with\n   restore commands; `.md-file-cap.yaml` limit and reason updated for the rest;\n   `md_file_cap.py --repo .` exits 0.\n5. **Goal without the commit rule (Q5, Q14).** GOAL.md's thesis and disproof rewritten on the two\n   boundaries that remain; `.aes/commit_rule.yaml` removed.\n6. **Roadmap linked (Q8).** wiki/index.md links the roadmap named in `.agentic/repo.yaml`, marked\n   on hold; `validate_project_navigation.py .` reports 0 warnings.\n7. **Decision 0011 item 4 closed or kept (Q2)** as Brian answers; by default it is left as written.\n8. **Package rebuilt** from the final revision; `validate_planning_package.py` exits 0.\n\n## Out of scope\n\n- New v0.2 components, the v0.1 Plan 002 line, and the vendored `enforced_planning/` package\n  (Q10: left in place while on hold).\n- Anything in the other repositories that carry `.aes/`.\n\n## Domain concepts this plan relies on\n\nAccepted plan, observation, freshness, criterion standing, success criterion, verification\nsubject, the checked-boundary thesis, the commit rule (retired) and the project brain, as defined in\n[DOMAIN.md](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/docs/planning/DOMAIN.md).\n\n## Trace and evidence\n\nEvery `aes evidence record` run writes its observation under `.aes/observations/` with the\ncommand, revision and result; the agent reads each failing one in full, and a sample of passing\nones, before reporting the count. Each check's command, exit status and counts go into\n`docs/planning/checks.txt` when the package is rebuilt.\n",
 "cold_review": "The cold review has not run yet.",
 "evidence_links": {
  "checks.txt (full output of every check)": "https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/docs/planning/checks.txt",
  "cold-review.md (independent review)": "https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/docs/planning/cold-review.md",
  "planning-package.json (the manifest)": "https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/docs/planning/planning-package.json",
  "open-questions.json (the ledger)": "https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/docs/planning/open-questions.json",
  "SYSTEM_MODEL.md (system model; checked loop in docs/model/ODD.md)": "https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/docs/planning/SYSTEM_MODEL.md",
  "DOMAIN.md (domain glossary)": "https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/docs/planning/DOMAIN.md",
  "next.goal.md (the next plan)": "https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/main/docs/planning/next.goal.md"
 },
 "plan_questions": [
  "Q1",
  "Q2",
  "Q3",
  "Q4",
  "Q5",
  "Q6",
  "Q7",
  "Q8",
  "Q10",
  "Q12",
  "Q14"
 ],
 "built_from": "c1b3ee6",
 "checks_commit": "c1b3ee65040d0082863b4d4ef36e5d65dcb373c6"
};
