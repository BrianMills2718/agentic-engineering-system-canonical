---
description: Next plan for AES canonical -- AES holds all four parts (Lockstep, planning, agent rules, the feedback loop), each configurable per repository in lockstep.yaml (adopted 2026-11-25); the earlier one-tool build and its proofs are done
---

# Plan: AES holds all four parts, each one configurable

Planning package: docs/planning/planning-package.json

Plan size: full

Full because Lockstep and `ship` are read by other repositories, and the `lockstep.yaml` sections are a contract
every repository carries. Only slice 1 is planned in full; later slices are on the parking list below.

Previous plan, done: the one planning-and-checking tool, built in six slices (merged 2026-11-11 and 2026-11-12), then
its retrofit, from-scratch and plan-fidelity proofs (adopted 2026-11-20, all passed by 2026-11-22). Rolling Lockstep
out to Project Brains still waits on Brian's call. Its full text, including the steps that specification
`Source:` lines cite as "next.goal.md, step 3": [next.goal.md at 613b0ec7](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/613b0ec7461a7e3fa838a9d5ba1dfe11f793fcf7/docs/planning/next.goal.md).

Source: Brian, 2026-11-25, answering Decision a and Decision b: "on Decision a, yes it should hold all 4 parts btu
the whole systm should be configurable so you can congfigure what is on or off or any other settings. for any piece.
on b yes but we need to make sure that it isnt jsut causing friction". Before that, also 2026-11-25: "i thought that
the wayt his would owkr is that all of this stuff was in aes canoncial so that it was proable an docnfiurabl and then
basically you could pikc some dir or repo and turn on aes conaincial for it".

This plan amends the adopted [one-tool design](../../proposals/one-planning-tool/DESIGN.md) (2026-11-11) rather than replacing it.
It extends three of that design's points:

- the config row: `lockstep.yaml` stays the one settings file and gains one section per part;
- the open slice-5 question about Company Planning: answered below;
- "Company Planning's other skills stay in the plugin": they still do, but whether a repository loads them becomes a
  setting AES writes.

Independent read: reviewer subagent, 2026-11-25, verdict revise. Its 11 findings are folded in below.

## The four parts today

| Part | Where it lives | Switchable per repository today? |
| --- | --- | --- |
| Lockstep (edit guard, commit checks, layout, docstrings) | AES `src/lockstep/` | Commit checks: yes, `lockstep.yaml` `checks:` (block, warn or off). Edit guard strictness: only through the `PCW_MODE` environment variable, which the installed hook command hardcodes (`src/lockstep/init_repo.py:133`). |
| Planning (Company Planning skills and package validator) | `BrianMills2718/company-planning` (private); Inside Success installs it from the private mirror `Inside-Success/company-planning` | Partly, and in a second file. `.copier-answers.yml` keys `ship_planning_gate` and `ship_one_page_plans` switch `ship`'s two planning gates off, read from the default branch so a branch cannot turn its own gate off (`copier_answer_on` in `src/lockstep/checks/config.py`). The validator's source is hardcoded as `~/code2/company-planning` (`src/lockstep/plan_check.py:113`). The skills are installed per person, not per repository. |
| Agent rules | code2-workspace `agents/`, loaded machine-wide by `~/.claude/CLAUDE.md` | No. One person and one machine only. |
| Feedback loop | AES `scripts/learning_loop/` and its systemd user timers on Brian's PC. A second, older sweep lives in `~/code/ecosystem-ops` (`ecosystem-feedback-worker` and `-watchdog`). | No. The loop runs per machine. Of 8 timers, 5 are disabled: the 3 AES analysis jobs and the 2 ecosystem-ops jobs. |

So settings sit in three places today: `lockstep.yaml`, `.copier-answers.yml` and environment variables.

## The settings model

**One file.** `lockstep.yaml` holds one section per part.

**One vocabulary.** Every switch is `block`, `warn` or `off`. A bare YAML `true` or `on` means `block`, and a bare
`false` means `off`, the same normalization `checks:` already has (`src/lockstep/checks/config.py:182`).

**Defaults.** A missing section or key keeps today's behavior, so no repository changes on the day this lands.

**Where `ship` reads gates from.** `ship` reads every gate switch from the default branch at origin, never from the
branch being shipped, as `copier_answer_on` (formerly ship's `addon_on`) does. Diagnostic commands such as `lockstep plan check` read the working
tree and report the real verdict whatever the mode.

```yaml
checks: {trace: block, mutation: off}            # Lockstep commit checks: exists today
planning:                                        # slice 1 (gates) and slice 2 (source)
  gate: block                                    # ship's planning-package gate
  one_page_plans: block                          # ship's one-page-plan check
  validator: {repo: <git address>, ref: main}    # slice 2; no default address is written
  skills: block                                  # slice 3: write the plugin into .claude/settings.json
guard: {mode: warn}                              # parking: replaces the PCW_MODE hardcode
rules: {mode: block, source: {repo: <address>, ref: main, files: [agents/core.md]}}  # parking
feedback: {mode: block, issue_repo: OWNER/NAME}  # parking
```

**Switch-on command.** `lockstep init` stays the one command that turns AES on. The `aes` command already has an
unrelated `init`, which writes the retired `.aes/project.yaml` and which five old repositories still call, so the name
`aes init` is not reused. `lockstep init --parts planning,rules,feedback` writes each section. The default is every
part built so far.

### Every switch and where it lands

| Gate or setting | Today | In this plan |
| --- | --- | --- |
| Commit checks | `lockstep.yaml` `checks:` | unchanged |
| Planning-package gate | `.copier-answers.yml` `ship_planning_gate` | `planning.gate` (slice 1); the copier key is still read, and either one saying off turns the gate off |
| One-page-plan check | `.copier-answers.yml` `ship_one_page_plans` | `planning.one_page_plans` (slice 1), with the same fallback |
| Validator source | env `SHIP_COMPANY_PLANNING` or `~/code2/company-planning` | `planning.validator` (slice 2) |
| Plan-list graph | env `PROJECT_GRAPH` or `~/code2/aes-config/` (`ship.py:883`) | parking: a `planning.project_graph` key |
| Edit-guard strictness | `PCW_MODE` hardcoded in the hook command | parking: `guard.mode` |
| Company Planning skills | per-person plugin install | slice 3: `planning.skills` |
| Rules | machine-wide `~/.claude/CLAUDE.md` | parking: `rules:` |
| Feedback scope | machine-wide timers | parking: `feedback:` |
| Prior-art gate | no switch | **Deliberate exception**: Brian, 2026-11-17: "every cpaability/featuer shoul dhave a prior art search ... that needs to be ienforced". |

Two parts have boundaries that limit what a repository can switch:

- **Rules.** Brian's machine-wide load through `~/.claude/CLAUDE.md` must keep working. The per-repository setting
  serves a repository or a person without that global file.
- **Feedback.** The timers run per machine and never per repository. A repository only sets whether its sessions and
  records are in scope, and where its concerns are filed.

## Slice 1 (planned in full): the planning gates move into lockstep.yaml

What changes:

1. **`side_file.py` accepts the new sections.** Its top-level key list `_TOP` (`src/lockstep/side_file.py:55`) gains
   `planning`, `guard`, `rules`, `feedback` and `mutation`. `mutation` is already missing, so
   `lockstep.unplanned_files` reports AES's own `lockstep.yaml` as "has an unknown key 'mutation'". The message at
   `side_file.py:169`, which lists only five keys, is corrected. This lands first because every repository installs
   from the unpinned address.
2. **`checks/config.py` reads `planning.gate` and `planning.one_page_plans`.** Each is `block`, `warn` or `off`,
   normalized as above; a bad value refuses the merge with exit 1 and nothing pushed.
3. **`ship` reads the `planning:` section from `lockstep.yaml` on the default branch at origin.** It also keeps
   reading the `.copier-answers.yml` keys. Either one saying off turns the gate off, and the log line names which file
   said so. The three modes mean:
   - `off` skips the gate as a copier-answers `false` does.
   - `warn` downgrades a plan verdict (a validator rejection, a missing planning package, an incomplete one-page plan
     or a plan-list refusal) to a printed `warning:` line. A validator that cannot be fetched or cannot run still
     refuses the merge, because that failure is not a verdict on the plan (`_Unavailable` in `ship.py`).
   - `block` is today's behavior.
4. **`lockstep plan check` is not affected by the mode.** It always reports the validator's verdict with its own exit
   code.
5. **`lockstep init` writes `planning: {gate: block, one_page_plans: block}`** with a comment saying what each does.
   The comment contains no `~/` and no `/home/`, as the `lockstep-init` spec requires.
6. **OpenSpec change `planning-settings-in-lockstep-yaml`, with its `prior-art.json`.** The candidates are keeping the
   copier keys, and an `aes.yaml` file. Tests are written first. The change also edits:
   - the ship spec requirement `add-on-gates-switch-off-from-the-copier-answers`;
   - the `ship.py` docstrings at lines 37 and 457;
   - the `lockstep-init` spec.

Done when:

- **Tests:**
  - a branch that sets `planning.gate: off` in its own `lockstep.yaml` is still gated, because the setting is read
    from the default branch;
  - `off` on the default branch skips the gate and logs `lockstep.yaml`;
  - the copier key `false` still skips it;
  - `warn` passes a validator rejection with a warning but refuses an unfetchable validator;
  - a bad mode refuses with exit 1;
  - `side_file_problems` accepts the new keys and AES's own `lockstep.yaml`.
- **Real proof on another repository.** Edit only skipper's `lockstep.yaml` on a branch, setting
  `planning.gate: warn`. A `ship --dry-run` (or the gate function run against that checkout) still reads the default
  branch's setting. Once the setting is on main, a deliberately failing package warns and does not refuse.
- `make check` exits 0 in AES.

## Slice 2 (next, outline only): the validator's source is a setting

**The setting.** `planning.validator: {repo, ref}`. `lockstep init` writes it commented out, with a placeholder and no
address, because `company-planning` is private and a default address would fail for anyone without access.

**Which source wins.** The order is:

1. the environment variables `SHIP_PLANNING_VALIDATOR` and `SHIP_COMPANY_PLANNING`, which tests need;
2. the configured repository;
3. `~/code2/company-planning`.

Every run logs the winning source. When an environment variable overrides a configured repository, the run warns.

**The clone cache.** It lives under `$XDG_CACHE_HOME/lockstep/` (default `~/.cache/lockstep/`), keyed by a hash of the
address. Fetches take a `flock`. Git runs with `GIT_TERMINAL_PROMPT=0`, ssh with `BatchMode=yes`, and every fetch has a
timeout. Credentials come only from the user's own git or `gh` setup, and never from `lockstep.yaml`.

**The ref.** `ref` replaces the hardcoded `origin/main` at both places in `plan_check.py` (lines 120 and 126).

**The proof.** Point skipper at the `Inside-Success/company-planning` mirror with no environment variables set. The log
must name the mirror as the source.

## Feedback loop (Decision b), running alongside slice 1

These steps are zero-code and run before any timer is turned on:

1. **Dry run.** Run each of the 5 disabled jobs without side effects. Only `fix_owner.py` has `--dry-run`. For
   `problems.py`, run it without `--file` and with `--max-analyse` set low. Any job with no safe mode is read from its
   code and its last real outputs instead.

   For each job, count:
   - issues filed or updated;
   - agent sessions or pull requests started;
   - measured spend;
   - items that reach Brian directly.
2. **Judge the output.** The judge is a stronger model through `llm_client`, which reads every would-be item, up to
   20 per job. It marks each one actionable, duplicate or noise.
3. **Turn on only the jobs that pass, with caps.** Brian said "i dont get why we would want a cap?" on 2026-10-12. The
   recorded history and his 2026-11-25 words supersede that here:
   - the uncapped analysis opened 152 concerns at once;
   - `fix_owner.py` runs 10 items a day with a $20 budget each run.
4. **Friction measure, kept per job per week:**
   - items created;
   - items acted on;
   - items untriaged;
   - items closed as noise;
   - spend;
   - items that reached Brian.
5. **Stop rules:**
   - **Immediate stop:** any item that reaches Brian without his having asked, or a day's spend over $2. The job turns
     off at once.
   - **Weekly stop:** if under a third of a week's items are acted on, counting untriaged items as not acted on, the job
     turns off with that count as the reason.

   These join the "Wrong if" rules in the operator guide (`scripts/learning_loop/systemd/README.md`) rather than
   sitting beside them.
6. **The ecosystem-ops pair.**
   - The worker is a second home for "turn feedback into fixes", next to `fix_owner.py`. It stays off unless its dry
     run shows work `fix_owner.py` cannot do; in that case one home is chosen and the other retired.
   - The watchdog only watches the worker, so it goes wherever the worker goes.

Dry-run result, 2026-11-25 (steps 1 and 2; $1.48 measured from the `llm_client` call log, projects
`aes-feedback-dryrun` and `aes-feedback-dryrun-judge`; inputs, judge marks and traces in
`~/projects/data/aes-feedback-dryrun/`, outside git). Every job stays off, each for a stop rule:

| Job | Would do | Judge marks | Stop rule tripped |
| --- | --- | --- | --- |
| `problems.py` | file 7 issues, update 3, open 8 concerns, about 1,125 subscription Sonnet sessions (worked out from its strong-model setting) | 3 actionable, 12 duplicate, 3 noise | a Telegram digest reaches Brian; under a third useful |
| effects | revoke 6 of 17 rules, reopen 6 concerns | all 6 noise | 6 Telegram messages reach Brian |
| `fix_owner.py` | 10 comments, 1 bypass-permissions session that can merge | 2 actionable, 5 duplicate, 3 noise | under a third useful; all 192 open concerns are `on-hold` (its sessions run on the subscription, so their $0.49 to $17.59 is notional, not spend) |
| ecosystem-ops worker | no current work in its four registrations | not independent (judged from past actions) | none shown; kept off with no unique work today |
| watchdog | urgent push to Brian on failure | not run (restart is a side effect) | reaches Brian |

Spend is counted two ways (Brian, 2026-11-25: "shouldnt it use subscription usage which isnt modney anyways?"):
Claude Code sessions (`claude -p`, the `claude-code/` route) run on the subscription and count as a share of its
weekly limit, not dollars; only API calls (the labelling model, about $1.12 a cold run) count toward the $2-a-day
rule. Before any job is turned on again: its messages to Brian go to a digest he asked for or stop, it skips items
already open, and a rerun of this dry run passes the one-third acted-on rule.

## Parking list (later slices, not planned yet)

- Slice 3: `planning.skills`. `lockstep init` writes the Company Planning marketplace and plugin into the repository's
  `.claude/settings.json` (`extraKnownMarketplaces`, `enabledPlugins`), and writes the Codex equivalent.
- `guard.mode` replaces the `PCW_MODE` hardcode in the hook command.
- `planning.project_graph` replaces the `~/code2/aes-config` default.
- The rules part:
  - `rules.source` names the rule text;
  - `lockstep rules sync` fetches it into `.lockstep/rules/`, and `AGENTS.md` imports it;
  - `policies.py` reads the configured source.
- The feedback part's per-repository scope and `issue_repo`, read by the collector and the labels job.
- `lockstep status` prints each part's mode and last result. Built 2026-11-26 as `lockstep status --parts`
  (spec `lockstep-projection`, "Status lists each part with its mode and last gate result").
- Review the planning-gate records (since 2026-11-25, Brian: "i agree witht he warn but we should be recoridn these so
  we can review them afterwards"). An absent `planning:` setting now warns, and ship appends every gate run to
  `~/code2/.ship-logs/planning-verdicts/<date>.jsonl` (spec `ship`, "Every planning-gate run is recorded"). Review
  after 30 warn or refuse records, or on 2026-12-09, whichever comes first. For each record, follow its `head`:
  - Was the missing plan or package written within a week anyway?
  - Was the change reverted or fixed soon after?
  - Then keep, change or drop each check. The first data is the `aes_test` checks-on arm's refusals (2026-11-25).

## Authorized source-fact upkeep follow-on

Brian's 2026-11-12 Company Planning conversation asks for automatic wiki upkeep and
a finished consolidation demonstration ("ok proceed"). This bounded follow-on
extends existing Lockstep projection, configuration and hooks: selected source-owned
status, description, interface and evidence fields feed declared target blocks;
post-edit refresh maintains them and the read-only project check refuses stale
blocks. It adds no AI answer path or universal enforcement. The
[acceptance table](source-facts-acceptance.md) and A9 distinguish provider tests,
installed-command replay and native dispatch; consumer evidence is supplied by
Company Planning rather than inferred from a successful documentation build.
Specification: `openspec/specs/lockstep-doc-facts/spec.md`.
