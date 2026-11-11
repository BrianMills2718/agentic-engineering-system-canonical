# One planning-and-checking tool (design proposal)

Status: proposed, not adopted. Owner: the Lockstep session. Date: 2026-11-11.

Source: Brian, 2026-11-11, on the Lockstep session's Decision 4 (code2-workspace decision 0009, amendment 3,
part 2): "on dcision 4 it seems liek youa re poitn otu that htis should be combined into one single thing not a
bunch of differnt things which i agree with. and it should preusmably be part of aes canonicale which is
configurable and protable/sharebale". Issues: BrianMills2718/lockstep#111, BrianMills2718/code2-template#27.

## In one paragraph

Today three things do overlapping jobs. Lockstep (`pcw`) plans the files and guards edits, code2check runs
commit checks, and Company Planning checks plan packages. They use three plan formats: `.aes/target.yaml`,
OpenSpec markdown, and a markdown plan with a requirements table. This proposal makes them one tool, named
**Lockstep**, shipped from this repository as one installable package with one config file. It has one plan
format: OpenSpec for what the code must do, plus a small layout file for which files exist and why. One edit
guard and one commit check read it. Any repository, personal or Inside Success, installs it with one command.

## A concrete example of the finished tool

1. In a fresh repository: `uvx --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical lockstep init`.
   This writes `lockstep.yaml` and the Claude Code, Codex and lefthook hook entries. It writes no absolute paths.
2. An agent proposes the plan: an OpenSpec change (requirements and scenarios), plus layout rows in `lockstep.yaml`
   (file, purpose, which requirements it implements, which tests prove it). Brian (or the repository's approver)
   accepts it.
3. `lockstep layout` creates the planned files. Each starts with a docstring holding the requirement text, the
   success criteria and the test names. This is amendment 3 part 1, "it also writes the first doc strings".
4. An agent tries `cat > src/extra.py` for a file the plan does not name. It is refused, and the refusal shows the
   plan. `cp src/a.py /tmp/x` (only reading a planned file) is allowed. Lockstep today gets both of these wrong;
   the code2check guard gets them right, and its parser is carried over.
5. A commit whose new scenario test passes on the base revision is refused (test first). So is an import the
   architecture diagram forbids, or a requirement with no `Source:` line.

## What goes where

| Job | Today | In the one tool |
| --- | --- | --- |
| What the code must do | `.aes/target.yaml` (Lockstep), OpenSpec (code2check), plan requirements table (Company Planning) | OpenSpec specs and changes, the format already adopted for behavior changes (code2-workspace AGENTS.md, 2026-10-13) |
| Which files exist and why | `.aes/target.yaml` `planned_artifacts`; `lockstep.yaml` side file; `[tool.code2check] planned` | `lockstep.yaml` `layout:` rows: path, purpose, implements, tests |
| Acceptance Brian judges by hand | Company Planning `acceptance-criteria.json` | the same schema, read from `docs/planning/acceptance-criteria.json`; `lockstep plan check` validates it |
| Requirement text in docstrings | `pcw` cog projection; `code2check project` | one projector (Lockstep's), fed from OpenSpec |
| Edit-time guard | `pcw-hook`; code2check `hook.py` and `guard.py` | one hook; shell-target parsing taken from code2check `guard.py` (#25, #26) |
| Docstring edit drafts a plan change | `pcw docstring_up` | kept |
| Commit checks | code2check `trace`, `arch`, `test-first`, `sources`, `docmeta`; `pcw check`; `aes topology check` | `lockstep check` with named checks; each can be switched on or off in `lockstep.yaml` |
| Status per requirement | `pcw requirement_status`; `code2check status`; `aes evidence status` | one `lockstep status`, written to the wiki |
| Hook log | `.pcw/` in the repository; `~/.local/state/code2check/` | `.lockstep/` in the repository |

Company Planning's other skills (landscape review, roadmaps, the review page) stay in the Company Planning plugin.
Only its plan and acceptance format check moves, so the format is defined in one place.

## Configurable and shareable

- One config file, `lockstep.yaml`, has `checks:` (each `block`, `warn` or `off`), `governed:` and `fixed:` paths,
  `layout:` rows, `sources.human_pattern` (today hardcoded as `Source: Brian`), and `owner` (today hardcoded as
  `BrianMills2718` in code2-template `copier.yml` and Company Planning `PERSONAL_OWNER`). It also pins the
  `likec4` version.
- Nothing names Brian's machine. The paths Company Planning reads today (`~/code2/representation-router`,
  `~/code2/<name>`) become config keys with no default.
- It installs from this repository's git URL with `uv`. `lockstep init` and the code2 template both use it. Inside
  Success repositories install it the same way.

## Slices (each merges when it works)

1. **Move.** `pcw` moves into this repository as package `lockstep`, with tests. `pcw` and `pcw-hook` stay as alias
   entry points so lifelike and Team-Brains' vendored runner keep working. The lockstep repository then points here.
2. **Plan format.** Lockstep reads requirements from OpenSpec (it already reads OpenSpec text, lockstep#54) and
   layout from `lockstep.yaml`. `.aes/target.yaml` stays readable until lifelike and Team-Brains move off it.
3. **Guard.** Port code2check's shell-target parsing. Done when lifelike replays the four cases from lockstep#111
   (`cat >`, `echo >`, `python -c` refused; read-only `cp` allowed).
4. **Commit checks.** Port code2check's `trace`, `arch`, `test-first`, `sources` and `docmeta` with their tests,
   as `lockstep check <name>`.
5. **Plan check.** Port the acceptance-criteria and plan-requirement checks from Company Planning's validator.
6. **Switch users.** code2-template installs `lockstep` instead of `code2check` (11 repositories adopt it when
   next changed, under the existing adopt-when-changed rule). lifelike, plan-code-wiki and Team-Brains' runner
   move to the new package.

## What this does not decide

- How fast `.aes/target.yaml` retires. CLAUDE.md already says it retires one repository at a time.
- Whether Company Planning's adoption gate (`method_conformance adopt`) calls `lockstep plan check` or keeps its
  own copy for the Inside Success team. That is a question for slice 5.

Inferred by agent (the format choice, the name, the slices), from Brian's direction above and the inventory of
the three tools at lockstep 1476871, code2-template 03ce414, company-planning b8a53a0 and this repository
3b1c153.
