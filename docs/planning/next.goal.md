---
description: Next plan for AES canonical -- AES holds all four parts (Lockstep, planning, agent rules, the feedback loop), each configurable per repository in lockstep.yaml (adopted 2026-11-25); the earlier one-tool build and its proofs are done
---

# Plan: AES holds all four parts, each one configurable

Planning package: docs/planning/planning-package.json

Plan size: full

Full because Lockstep and `ship` are read by other repositories, and the `lockstep.yaml` sections are a contract
every repository carries. Slices 1 and 3 are planned in full (slice 3 on 2026-11-26); slice 2 is outlined; later slices are on the parking list below.

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
  skills: {mode: block, marketplace: OWNER/REPO}  # slice 3: write the plugin into .claude/settings.json
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

## Slice 3 (planned in full, 2026-11-26): `planning.skills` loads Company Planning per repository

Source: the settings model above ("Company Planning skills | per-person plugin install | slice 3"), adopted by Brian
2026-11-25; queue item 4 of the AES week (`~/projects/data/aes-week/WORKQUEUE.md`). Independent read: reviewer
subagent, 2026-11-26, verdict revise; its 11 findings are folded in below.

**What is true today (checked 2026-11-26).**

- Claude Code has two plugin keys in `settings.json`: `extraKnownMarketplaces` and `enabledPlugins`. The Company
  Planning marketplace is named `inside-success` and its plugin `company-planning`. The names are the same in
  `BrianMills2718/company-planning` and in the mirror `Inside-Success/company-planning`
  (`.claude-plugin/marketplace.json`). The exact shape, as in Company Planning's usage guide ("Staying current"), is:
  `{"extraKnownMarketplaces": {"inside-success": {"source": {"source": "github", "repo": "OWNER/REPO"}}},
  "enabledPlugins": {"company-planning@inside-success": true}}`.
- **What the keys do from a repository's own `.claude/settings.json`** (Claude Code docs, read 2026-11-26):
  - Once a person trusts the folder, the declared marketplace is cloned in the background
    (code.claude.com/docs/en/plugins/loading.md, and settings.md: the keys "apply only after each teammate trusts the
    folder").
  - The plugin itself is not downloaded. "Committing that entry turns the plugin on for your collaborators but doesn't
    download it to their machines. Each collaborator also runs `claude plugin install <name>@<marketplace> --scope
    project` once per clone" (plugins/install.md).
  - `claude -p` shows no trust dialog. It loads plugins only once they are installed and the folder is trusted
    (headless.md). Its `system/init` event lists the loaded plugins.
  - The docs do not say which wins when the person's own settings already declare `inside-success` with another source.
    Step 0 tests it.
- **Access.** Install clones the marketplace over HTTPS with the person's own git credentials (usage guide,
  "Install"). Anyone who cannot read the configured repository gets a failed install offer when they open the
  repository. Neither `lockstep init` nor the drift check can detect that, and init does not warn about it.
- **Codex 0.172 has no per-repository equivalent.** Probe, rerunnable in an empty git folder. Write a
  `.codex/config.toml` holding a `[marketplaces.probe-mkt]` table (`source`, `source_type = "git"`), and in a second run
  an `.agents/plugins/marketplace.json` naming `probe-repo-mkt`. Run `codex plugin marketplace list`, once plain and once
  with `-c 'projects."<folder>".trust_level="trusted"'`. All three runs exit 0 and list only the person's marketplaces,
  never the probe's. For Codex, Lockstep can only print what to run.

**The setting.**

```yaml
planning:
  skills: {mode: block, marketplace: OWNER/REPO}   # mode: block | warn | off (bare true/false as elsewhere)
```

- A missing key means `off`. That keeps today's behavior. It is deliberately not the `warn` default that `gate` and
  `one_page_plans` now have, because this switch writes files, and `warn` would put them in every repository.
- `marketplace` is a GitHub `owner/repo`, with no default address, for the same reason as slice 2. A fresh
  `lockstep init` writes the key commented out, with the mirror as the example. An existing `lockstep.yaml` (every
  adopting repository) is edited by hand, then `lockstep init` is run. There is no `--skills-from` option.
- **One switch.** `planning.skills.mode` is the only switch. The drift check below runs inside the existing `project`
  commit check, so it adds no `checks:` entry and no new name in `CHECK_NAMES`. That leaves the lefthook command that
  init generates unchanged in existing repositories (`init_repo.py` `_lefthook`).
- **Not a ship gate.** The drift check is advisory, runs at commit time and reads the working tree. `ship` does not run
  it, and `planning_modes` (`checks/config.py`) does not validate `skills`, so a typo there never stops a merge. Only
  `side_file.py` and the drift check report a bad `skills` value. This exception to "ship reads gates from the default
  branch" is deliberate: the check only keeps `.claude/settings.json` consistent; it protects nothing.

**Steps.**
0. **Proof first, no code.** In a skipper branch checkout:

- add the two keys by hand to `.claude/settings.json`, using the mirror;
- trust the folder;
- run `claude plugin install company-planning@inside-success --scope project`;
- then run `claude -p "list your skills" --output-format stream-json`.

   Expected: its `system/init` event lists `company-planning` in `plugins` and nothing in `plugin_errors`. Repeat once
   on a machine whose `~/.claude/settings.json` already declares `inside-success` from the other address, and record
   which source loads. Output goes to `~/projects/data/aes-week/slice3-proof/`. If the plugin does not load, stop the
   slice and record the result here.

   Result, second case (2026-11-26 22:15). This was run in a scratch repository rather than skipper, since the disk
   guard refused new worktrees. The repository declared the mirror, and the person's own settings already declare
   `inside-success` from `BrianMills2718/company-planning`. Results:
  - `claude -p` loaded `company-planning` from the existing install, with no `plugin_errors`;
  - `claude plugin marketplace list` still shows the person's own source.

   So the repository's keys are harmless for someone who already has the plugin, and their source wins.
   Files: `~/projects/data/aes-week/slice3-proof/conflict-case-*`. The first case (a person without the plugin) is
   still to run.

1. **`side_file.py`** validates `planning.skills` as a map with `mode` (the shared normalization) and `marketplace`
   (`owner/repo`). Problems are reported with their line.
2. **New module `src/lockstep/checks/plugin_settings.py`**, with a `layout:` row (ship.py is at its size cap). It has
   the marketplace and plugin names as constants. `wanted(config)` gives the keys above. `merge(path, config)`
   returns one of three results:
   - `wrote`: a key was missing, so it is added and every other key is kept, as `_merge_hooks` keeps them.
   - `skipped`: everything already matches.
   - `conflict`: an `inside-success` entry with a different source or repository, or an `enabledPlugins` value of
     `false`, is never overwritten. A `false` is a person opting out on purpose.

   Extra fields such as `autoUpdate: true` are tolerated.
3. **`lockstep init`** calls `merge` when `mode` is `block` or `warn` and prints its result. A `.claude/settings.json`
   that is not valid JSON exits 2, as for hooks. For Codex it prints the two commands from the usage guide with the
   configured address (`codex plugin marketplace add OWNER/REPO`, `codex plugin add company-planning@inside-success`).
   It reads and writes nothing in `~/.codex/`. For Claude Code it also prints the one step the docs say each person
   still runs once per clone: `claude plugin install company-planning@inside-success --scope project`. The same line
   goes in the repository's `AGENTS.md` setup notes, so a teammate who did not run init sees it too.
4. **Drift check, inside `lockstep check project`.** It needs no network. Its compare looks only at three things: the
   source is `github`, the repository matches, and the `enabledPlugins` entry is `true`. A missing or different
   value refuses under `block`, warns under `warn`, and is not looked at under `off`. A `conflict` (including an
   opt-out `false`) only warns, whatever the mode, and names the key. The fix the message names is `lockstep init`.
5. **`off` never removes keys** a person or another tool wrote.
6. **OpenSpec change `planning-skills-setting`**, with `prior-art.json`. Candidates:
   - Claude Code's own plugin keys in project settings, plus its documented per-clone install: **adopt**, if step 0 passes.
   - The copier template writing the keys statically: **reject**, because most repositories did not start from the
     template.
   - A Codex project config: **reject**, because the probe above shows none.

   The change edits the `lockstep-init` spec and the `project` check's spec. New tests go in
   `tests/test_plugin_settings.py`, with a layout row, written first.

**Done when.**

- **Tests:**
  - init with `block`, then `lockstep check project`, passes, and a second init reports `skipped`;
  - `warn` also writes the keys;
  - the keys merge into an existing `.claude/settings.json` without losing its hooks;
  - a malformed settings file exits 2;
  - `off` writes nothing, and leaves keys that already exist untouched;
  - the drift check refuses a deleted `enabledPlugins` entry under `block` and warns under `warn`;
  - a different `inside-success` source, and an opt-out `false`, are reported as `conflict` and left as they are;
  - `autoUpdate` passes;
  - a bad mode and a bad address are each reported with the line, and `ship`'s `planning_modes` ignores them;
  - init prints the two Codex commands with the configured address.
- **Real proof:** step 0's `system/init` event, saved and judged by the AES week run that records it. Then the same
  skipper branch with the keys removed, written back by `lockstep init`, and the printed install line run: the
  plugin loads again. Codex: in a scratch
  `CODEX_HOME`, the printed commands are run once, and `codex plugin list` shows `company-planning@inside-success`.
- `make check` exits 0 in AES.

**Out of this slice:** removing the per-person install from machines that already have it; a Codex per-repository
install (none exists); the rules and feedback parts.

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

## aes_test result (2026-11-25, one run per arm)

Next evaluation: [game benchmark plan](game-benchmark.md) (2026-11-26; Brian: the TinyDB test was too easy).

Brian approved the test on 2026-11-25 ("i approve your recommdnation"): TinyDB 4.8.0 rebuilt from its documentation
only, AES full planning by one Sonnet session, building by a second, judged by TinyDB's own 201 tests hidden from both.

| | checks on | checks off |
|---|---|---|
| Hidden tests using only documented names (179) | 156 passed | 144 passed |
| Builder wall time | 21 min | 21 min |
| Builder turns | 38 | 91 |
| Builder cost (notional: subscription session) | $3.66 | $5.72 |
| Check or hook refusals | 0 | 0 (hooks off) |

- The checks-on arm's failures are a subset of the checks-off arm's. The 12-test gap is one private name the tests
  read (`table._query_cache`), in neither the documentation nor the plan.
- Unadapted, both arms score 0: the tests' `conftest.py` imports `JSONStorage` from the package top level, which the
  documentation never shows. 22 more tests import undocumented helpers (`touch`, `freeze`).
- Planning took the whole 90-minute cap, ending in the second cold-review round. The planner read Lockstep's installed
  source to learn what the checks want.
- Reading: the build checks neither refused nor visibly changed the code. The cost is in planning paperwork. This
  is one run, so it is a lead rather than a measurement. The first planning-gate review (parking list) takes it as its
  first data.

## Parking list (later slices, not planned yet)

- `guard.mode` replaces the `PCW_MODE` hardcode in the hook command.
- `planning.project_graph` replaces the `~/code2/aes-config` default.
- The rules part:
  - `rules.source` names the rule text;
  - `lockstep rules sync` fetches it into `.lockstep/rules/`, and `AGENTS.md` imports it;
  - `policies.py` reads the configured source.
- The feedback part's per-repository scope and `issue_repo`, read by the collector and the labels job.
- `lockstep status` prints each part's mode and last result.
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
