"""SC-AP-001: the commit-tag rule, through the installed commit-msg hook on real commits.

Each test builds a real Git repository holding the frozen whygame5 records, runs
`aes hooks install`, stages real changes and runs `git commit`, so the verdict
comes from the hook git actually runs, not from calling the rule function.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from agentic_engineering_system.cli import main
from agentic_engineering_system.commit_rule import FileChange, RuleConfig, judge, replay

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"
WHYGAME5_AES = Path(__file__).parent / "fixtures" / "whygame5-54043e2" / ".aes"
ENV = {**os.environ, "PYTHONPATH": str(SRC)}


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", *args],
                          cwd=root, capture_output=True, text=True, check=False, env=ENV)


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _commits(root: Path) -> int:
    return int(_git(root, "rev-list", "--count", "HEAD").stdout)


def _set_mode(root: Path, mode: str) -> None:
    _write(root, ".aes/commit_rule.yaml", f"mode: {mode}\n")


def _adopted_plan(root: Path, plan_id: str = "demo") -> Path:
    """A plan with a Company Planning-shaped adoption decision bound to its bytes."""
    plan = root / "proposals" / plan_id / "README.md"
    _write(root, f"proposals/{plan_id}/README.md",
           f"---\nplan_id: {plan_id}\nmethod_conformance_receipt: proposals/{plan_id}/receipt.json\n---\n\n# Demo plan\n")
    _write(root, f"proposals/{plan_id}/receipt.json", json.dumps({"verdict": "pass"}) + "\n")
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    _write(root, f"proposals/{plan_id}/receipt.adoption-decision.json", json.dumps({
        "decision": "adopted", "plan_ref": f"proposals/{plan_id}/README.md",
        "plan_sha256": digest(plan), "receipt_sha256": digest(root / f"proposals/{plan_id}/receipt.json")}) + "\n")
    return plan


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "consumer"
    (root / ".aes").mkdir(parents=True)
    shutil.copyfile(WHYGAME5_AES / "project.yaml", root / ".aes" / "project.yaml")
    shutil.copyfile(WHYGAME5_AES / "target.yaml", root / ".aes" / "target.yaml")
    for rel in ("src/whygame5/__init__.py", "src/whygame5/contracts.py", "src/whygame5/evaluator.py",
                "src/whygame5/graph.py", "tests/test_evaluator.py", "tests/test_replay.py"):
        _write(root, rel, f"# {rel}\n")
    _write(root, "README.md", "# Consumer\n\nA line with a tpyo.\n")
    assert _git(root, "init", "-q").returncode == 0
    _git(root, "add", ".")
    assert _git(root, "commit", "-q", "-m", "fixture").returncode == 0
    assert main(["hooks", "install", "--root", str(root)]) == 0
    _adopted_plan(root)
    _set_mode(root, "enforce")
    _git(root, "add", ".")
    done = _git(root, "commit", "-m", "[Shaping demo] install hooks and draft plan\n\nEmergency: bootstrap")
    # the bootstrap touches files outside proposals/demo/, so even it is refused under enforce;
    # it lands as an emergency instead
    assert done.returncode != 0 and "Shaping demo" in done.stderr
    assert _git(root, "commit", "-m", "[Unplanned] install hooks and draft plan\n\nEmergency: bootstrap the rule").returncode == 0
    return root


def _stage_worker_tools(root: Path) -> None:
    _write(root, "Dockerfile", "FROM debian\nRUN apt-get install -y make\n")
    _write(root, "compose.yaml", "services:\n  app:\n    build: .\n")
    _git(root, "add", "Dockerfile", "compose.yaml")


def test_unplanned_running_thing_without_emergency_is_refused_naming_the_files(repo: Path) -> None:
    before = _commits(repo)
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Unplanned] add worker tools")
    assert done.returncode == 1
    assert "refuse [Unplanned]" in done.stderr
    assert "Dockerfile, compose.yaml" in done.stderr and "needs a plan" in done.stderr
    assert _commits(repo) == before


def test_same_change_under_an_adopted_plan_is_accepted(repo: Path) -> None:
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Goal demo] U2: worker tools")
    assert done.returncode == 0, done.stderr
    assert "accept [Goal demo]" in done.stderr and "plan demo adopted" in done.stderr


def test_one_line_readme_fix_is_trivial(repo: Path) -> None:
    _write(repo, "README.md", "# Consumer\n\nA line with a typo.\n")
    _git(repo, "add", "README.md")
    done = _git(repo, "commit", "-m", "[Trivial] fix typo")
    assert done.returncode == 0, done.stderr
    assert "accept [Trivial]" in done.stderr and "1 file(s), 2 line(s)" in done.stderr


def test_plan_changed_after_adoption_is_refused(repo: Path) -> None:
    plan = repo / "proposals" / "demo" / "README.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "\nEdited after adoption.\n", encoding="utf-8")
    _stage_worker_tools(repo)
    _git(repo, "add", str(plan))
    done = _git(repo, "commit", "-m", "[Goal demo] U2: worker tools")
    assert done.returncode == 1
    assert "plan changed since adoption; re-adopt it" in done.stderr


def test_plan_without_receipt_and_unknown_plan_are_refused(repo: Path) -> None:
    _write(repo, "docs/plans/7_old_plan.md", "# Plan 7, written before adoption existed\n")
    _git(repo, "add", "docs/plans/7_old_plan.md")
    done = _git(repo, "commit", "-m", "[Plan #7] old-style plan")
    assert done.returncode == 1 and "no method_conformance_receipt" in done.stderr
    done = _git(repo, "commit", "-m", "[Goal nosuch] work")
    assert done.returncode == 1 and "no plan nosuch found" in done.stderr


@pytest.mark.parametrize(("files", "reason"), [
    ({"hooks/pre-push": "#!/bin/sh\n"}, "touches running-thing file(s): hooks/pre-push"),
    ({"a.md": "a\n", "b.md": "b\n", "c.md": "c\n", "d.md": "d\n"}, "4 files (trivial allows 3)"),
    ({"notes.md": "x\n" * 61}, "61 changed lines (trivial allows 60)"),
    ({"src/whygame5/new.py": "x = 1\n"}, "adds file(s) under a governed root: src/whygame5/new.py"),
])
def test_trivial_is_measured_not_trusted(repo: Path, files: dict[str, str], reason: str) -> None:
    for rel, text in files.items():
        _write(repo, rel, text)
        _git(repo, "add", rel)
    # the same command the installed hook runs, on the staged change, before any commit
    msg = repo / ".git" / "MSG"
    msg.write_text("[Trivial] small thing\n", encoding="utf-8")
    checked = subprocess.run([sys.executable, "-m", "agentic_engineering_system.cli", "commit", "check",
                              str(msg), "--root", str(repo)], cwd=repo, capture_output=True, text=True, env=ENV)
    assert checked.returncode == 1
    assert reason in checked.stderr


def test_emergency_and_shaping(repo: Path) -> None:
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Unplanned] hotfix the worker image\n\nEmergency: workers down since 06:00")
    assert done.returncode == 0 and "emergency recorded" in done.stderr
    _write(repo, "proposals/next/README.md", "# Next plan draft\n")
    _git(repo, "add", "proposals/next/README.md")
    done = _git(repo, "commit", "-m", "[Shaping next] first draft")
    assert done.returncode == 0 and "accept [Shaping next]" in done.stderr
    _write(repo, "proposals/next/README.md", "# Next plan draft, v2\n")
    _write(repo, "README.md", "# Consumer\n\nAlso edited.\n")
    _git(repo, "add", "proposals/next/README.md", "README.md")
    done = _git(repo, "commit", "-m", "[Shaping next] second draft")
    assert done.returncode == 1 and "also touches README.md" in done.stderr


def test_plan_adopted_in_the_commit_being_made_is_found_in_the_index(repo: Path) -> None:
    # The plan and its adoption decision exist only in the commit being made (staged, not on disk),
    # as when a plan is adopted and committed together with its first work (code-15, 2026-10-08).
    _adopted_plan(repo, "fresh")
    _stage_worker_tools(repo)
    _git(repo, "add", "proposals/fresh")
    shutil.rmtree(repo / "proposals" / "fresh")
    done = _git(repo, "commit", "-m", "[Goal fresh] adopt the plan and add worker tools")
    assert done.returncode == 0, done.stderr
    assert "plan fresh adopted" in done.stderr and "commit being made" in done.stderr


def test_numbered_plan_adopted_in_the_commit_being_made_is_found(repo: Path) -> None:
    rel = "docs/plans/56_first_try.md"
    _write(repo, rel, "---\nmethod_conformance_receipt: docs/plans/56_first_try.receipt.json\n---\n\n# Plan 56\n")
    _write(repo, "docs/plans/56_first_try.receipt.json", json.dumps({"verdict": "pass"}) + "\n")
    digest = lambda p: hashlib.sha256((repo / p).read_bytes()).hexdigest()  # noqa: E731
    _write(repo, "docs/plans/56_first_try.adoption-decision.json", json.dumps({
        "decision": "adopted", "plan_sha256": digest(rel),
        "receipt_sha256": digest("docs/plans/56_first_try.receipt.json")}) + "\n")
    _stage_worker_tools(repo)
    _git(repo, "add", "docs/plans")
    shutil.rmtree(repo / "docs" / "plans")
    done = _git(repo, "commit", "-m", "[Plan #56] adopt plan 56 and add worker tools")
    assert done.returncode == 0, done.stderr
    assert "plan #56 adopted" in done.stderr


def test_plan_refusal_names_the_way_to_adopt_one(repo: Path) -> None:
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Goal no-such-plan] add worker tools")
    assert done.returncode == 1 and "no-such-plan" in done.stderr and "quick-adopt" in done.stderr


def test_unplanned_whose_emergency_line_says_none_is_refused(repo: Path) -> None:
    _stage_worker_tools(repo)
    for reason in ("none; [Unplanned] is the tag this repository accepts for unplanned maintenance (AES #189)",
                   "None.", "n/a", "NA - routine cleanup"):
        done = _git(repo, "commit", "-m", f"[Unplanned] add worker tools\n\nEmergency: {reason}")
        assert done.returncode == 1 and "says there is none" in done.stderr and "quick-adopt" in done.stderr, reason
    # A real reason that merely starts with the word is still an emergency.
    done = _git(repo, "commit", "-m", "[Unplanned] add worker tools\n\nEmergency: none of the backups ran since 06:00")
    assert done.returncode == 0 and "emergency recorded" in done.stderr


# Real commit messages that reached main tagged [Unplanned] for ordinary documentation work, copied verbatim
# from `git show -s --format=%B <sha>` (2026-10-10 audit; ROLLOUT.md "Placeholder Emergency lines are refused").
# vision 0df694a, 11f77bc, ef56e03, 607ddae; observation-to-action-metamodel d27d160, 54492b2, 4f62c97, 4f7f998.
_TRAILER = "\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>"
REAL_PLACEHOLDER_EMERGENCIES = {
    "vision 0df694a": "[Unplanned] Federation map: who owns each part of the agent, checked by the gate (#111)\n\n"
        "Emergency: not an emergency. Routine vision work has no fitting commit label (AES issue 190). "
        "PATH-vision-federation-map-2026-10-08.\n\n\n\n\nClaude-Session: "
        "https://claude.ai/code/session_01KPeBhZhkmToaDeoobYTVo4" + _TRAILER,
    "vision 11f77bc": "[Unplanned] Lineage pages for five relevant parts; parts index lists a part's own page first (#110)\n\n"
        "Emergency: not an emergency. Routine vision work has no fitting commit label (AES issue 190). Roadmap row 4, "
        "PATH-o2a-capture-relevant-parts-2026-10-08.\n\n\n\n\nClaude-Session: "
        "https://claude.ai/code/session_01KPeBhZhkmToaDeoobYTVo4" + _TRAILER,
    "vision ef56e03": "[Unplanned] The relevant parts, read for what each provides (#106)\n\n"
        "Emergency: not an emergency. Vision has no AES plans and no other commit label fits (AES issue 190). "
        "Within PATH-vision-entry-point-2026-10-08.\n\n\nClaude-Session: "
        "https://claude.ai/code/session_01KPeBhZhkmToaDeoobYTVo4" + _TRAILER,
    "vision 607ddae": "[Unplanned] Vision becomes the entry point to every part; generated parts index checked by the gate (#104)\n\n"
        "Emergency: not an emergency. Vision has no AES plans and no other commit label fits a routine change (see AES "
        "issue 190). Company-planning record: .company-planning/PATH-vision-entry-point-2026-10-08.json (durable_solo)."
        "\n\n\nClaude-Session: https://claude.ai/code/session_01KPeBhZhkmToaDeoobYTVo4" + _TRAILER,
    "metamodel d27d160": "[Unplanned] Roadmap rows 7a/7b and goal: system models for the four core owners first (#134)\n\n"
        "Emergency: not an emergency. Planning documents outside formal/ have no fitting label (AES issue 190)." + _TRAILER,
    "metamodel 54492b2": "[Unplanned] Roadmap row 7 and goal: system models for the 11 owners, composed through the "
        "federation map (#132)\n\n"
        "Emergency: not an emergency. Planning documents outside formal/ have no fitting label (AES issue 190)." + _TRAILER,
    "metamodel 4f62c97": "[Unplanned] Roadmap row 5a done (14 of 14 decompositions integrated); goal for row 5, the "
        "crosswalk (#128)\n\n"
        "Emergency: not an emergency. Planning documents outside formal/ have no fitting label (AES issue 190)." + _TRAILER,
    "metamodel 4f7f998": "[Unplanned] Roadmap row 5a (finish the 14 decompositions) and its goal (#127)\n\n"
        "Emergency: not an emergency. Planning documents outside formal/ have no fitting label (AES issue 190)." + _TRAILER,
}
# A real emergency, verbatim from second-brain-mega 48c5eb9 (a refresh failing every run).
REAL_EMERGENCY = ("[Unplanned] Repoint reader routes moved by the brians-2nd-brain-integration-work AES layout migration (#55)\n\n"
    "Emergency: server finder refresh has failed every run since 2026-10-08T10:17Z because catalog/systems.yaml routes "
    "to seven files that moved from plan/ and roadmap/ into docs/plans/ and docs/architecture/ (upstream PRs "
    "#932-#935). Every route now resolves at each repository's current main.\n\n"
    "Verified: every repos/<name>/<path> route in catalog/systems.yaml checked with git cat-file against origin/main "
    "of its submodule; 0 missing.\n\n\nClaude-Session: https://claude.ai/code/session_013Av3aoaEm5wQ7XqYhWhMkT" + _TRAILER)


def test_real_placeholder_emergency_messages_are_refused_and_a_real_emergency_is_accepted(repo: Path) -> None:
    _stage_worker_tools(repo)
    before = _commits(repo)
    for where, message in REAL_PLACEHOLDER_EMERGENCIES.items():
        done = _git(repo, "commit", "-m", message)
        assert done.returncode == 1 and "says there is none (or is a placeholder)" in done.stderr, where
        assert "quick-adopt" in done.stderr, where
    assert _commits(repo) == before
    done = _git(repo, "commit", "-m", REAL_EMERGENCY)
    assert done.returncode == 0 and "emergency recorded" in done.stderr, done.stderr
    assert _commits(repo) == before + 1


def test_placeholder_and_empty_emergency_values_are_refused(repo: Path) -> None:
    _stage_worker_tools(repo)
    for value in ("-", "--", "\u2014", "TBD", "todo.", "nothing", "no", "nil", "null", "No emergency",
                  "not applicable", "Non-emergency; docs only", "not urgent (routine)"):
        done = _git(repo, "commit", "-m", f"[Unplanned] add worker tools\n\nEmergency: {value}")
        assert done.returncode == 1 and "is a placeholder" in done.stderr, value
    # An empty Emergency: line is not a reason, even when a trailer follows it (\s* used to cross the line break).
    done = _git(repo, "commit", "-m", "[Unplanned] add worker tools\n\nEmergency:\nCo-authored-by: probe <p@example.invalid>")
    assert done.returncode == 1 and "add an 'Emergency: <reason>' line" in done.stderr, done.stderr
    # Reasons that merely start with a placeholder word are reasons.
    done = _git(repo, "commit", "-m", "[Unplanned] add worker tools\n\nEmergency: no deploy has succeeded since 06:00")
    assert done.returncode == 0 and "emergency recorded" in done.stderr, done.stderr


def test_observe_mode_logs_and_never_blocks(repo: Path) -> None:
    _set_mode(repo, "observe")
    _stage_worker_tools(repo)
    _git(repo, "add", ".aes/commit_rule.yaml")
    before = _commits(repo)
    done = _git(repo, "commit", "-m", "[Unplanned] add worker tools")
    assert done.returncode == 0
    assert "would refuse (observe mode) [Unplanned]" in done.stderr
    assert _commits(repo) == before + 1
    logs = sorted((repo / ".git" / "aes").glob("commit-rule-*.jsonl"))
    last = json.loads(logs[-1].read_text(encoding="utf-8").splitlines()[-1])
    assert last["mode"] == "observe" and last["verdict"] == "refuse" and last["tag"] == "Unplanned"
    assert last["running_things"] == ["Dockerfile", "compose.yaml"]


def test_no_tag_is_refused_and_git_messages_pass() -> None:
    config = RuleConfig()
    change = [FileChange("README.md", "M", 1, 1)]
    assert judge("fix things", change, [], config).verdict == "refuse"
    assert judge("Merge branch 'x' into main", change, [], config).verdict == "accept"
    assert judge("fixup! [Trivial] fix typo", change, [], config).verdict == "accept"


def test_replay_judges_history_with_counts(repo: Path) -> None:
    _write(repo, "README.md", "# Consumer\n\nA line with a typo.\n")
    _git(repo, "add", "README.md")
    assert _git(repo, "commit", "-m", "[Trivial] fix typo").returncode == 0
    rows, counts = replay(repo, "HEAD", 10)
    verdicts = {subject: v.verdict for _, subject, v in rows}
    assert verdicts["[Trivial] fix typo"] == "accept"
    assert verdicts["[Unplanned] install hooks and draft plan"] == "accept"  # emergency recorded
    assert verdicts["fixture"] == "refuse"  # no tag
    assert counts == {"commits": 3, "accept": 2, "refuse": 1, "tag:Trivial": 1, "tag:Unplanned": 1, "tag:none": 1}


def test_an_older_aes_without_the_rule_warns_and_does_not_block(repo: Path, tmp_path: Path) -> None:
    """A main checkout on an older branch must not stop every commit in every worktree."""
    old_aes = tmp_path / "old-python"
    old_aes.write_text("#!/bin/sh\necho 'aes: error: invalid choice: commit' >&2\nexit 2\n", encoding="utf-8")
    old_aes.chmod(0o755)
    assert _git(repo, "config", "--local", "aes.installer", str(old_aes)).returncode == 0
    _write(repo, "notes.md", "x\n")
    _git(repo, "add", "notes.md")
    done = _git(repo, "commit", "--no-verify", "-m", "placeholder")  # pre-commit would also use the old aes
    assert done.returncode == 0
    _git(repo, "reset", "--soft", "HEAD~1")
    hook = subprocess.run([str(repo / ".githooks" / "commit-msg"), str(repo / ".git" / "COMMIT_EDITMSG")],
                          cwd=repo, capture_output=True, text=True, env=ENV)
    assert hook.returncode == 0
    assert "WARNING: this AES has no 'commit' command, so the commit rule did not run" in hook.stderr


def test_in_aes_itself_the_hooks_run_the_working_copy_code() -> None:
    """Both hooks put `<root>/src` first when the repository is AES, so a worktree is checked
    by its own code, not by the branch the shared venv's editable install points at."""
    from agentic_engineering_system.hooks import render_commit_msg_hook, render_hook

    for body in (render_hook(), render_commit_msg_hook()):
        assert 'if [ -f "$root/src/agentic_engineering_system/cli.py" ]; then' in body
        assert 'PYTHONPATH="$root/src${PYTHONPATH:+:$PYTHONPATH}"; export PYTHONPATH' in body
    # this repository's tracked hooks are the rendered ones
    assert (REPO / ".githooks" / "pre-commit").read_text(encoding="utf-8") == render_hook()
    assert (REPO / ".githooks" / "commit-msg").read_text(encoding="utf-8") == render_commit_msg_hook()


def test_machine_config_reaches_repositories_without_their_own(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A plain repository takes the machine-wide mode; a per-repository entry overrides it; a repo file wins."""
    from agentic_engineering_system.commit_rule import load_rule_config

    machine = tmp_path / "machine.yaml"
    machine.write_text("mode: enforce\ntrivial_max_lines: 40\nrepos:\n  quiet:\n    mode: observe\n", encoding="utf-8")
    monkeypatch.setenv("AES_COMMIT_RULE_MACHINE_CONFIG", str(machine))
    plain, quiet, own = tmp_path / "plain", tmp_path / "quiet", tmp_path / "own"
    for root in (plain, quiet, own):
        root.mkdir()
    _write(own, ".aes/commit_rule.yaml", "mode: observe\n")
    assert (load_rule_config(plain).mode, load_rule_config(plain).trivial_max_lines) == ("enforce", 40)
    assert load_rule_config(plain).source == str(machine)
    assert load_rule_config(quiet).mode == "observe"
    assert load_rule_config(own).mode == "observe" and load_rule_config(own).source.endswith(".aes/commit_rule.yaml")
    monkeypatch.setenv("AES_COMMIT_RULE_MACHINE_CONFIG", str(tmp_path / "absent.yaml"))
    assert load_rule_config(plain).mode == "observe" and load_rule_config(plain).source == "default"


def test_machine_skip_roots_exempt_throwaway_repositories_and_nothing_else(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Issue #488: a repository under a machine-wide skip root commits untagged with a logged skip;
    one outside it is still refused; a repository's own file can neither name nor inherit a skip."""
    throwaway, real = tmp_path / "tmp", tmp_path / "code"
    machine = tmp_path / "machine.yaml"
    machine.write_text(f"mode: enforce\nskip_roots: [$AES_TEST_SKIP_ROOT, $AES_TEST_UNSET_VAR]\n", encoding="utf-8")
    monkeypatch.setenv("AES_COMMIT_RULE_MACHINE_CONFIG", str(machine))
    monkeypatch.setenv("AES_TEST_SKIP_ROOT", str(throwaway))
    monkeypatch.delenv("AES_TEST_UNSET_VAR", raising=False)
    env = {**ENV, "AES_COMMIT_RULE_MACHINE_CONFIG": str(machine), "AES_TEST_SKIP_ROOT": str(throwaway)}
    env.pop("AES_TEST_UNSET_VAR", None)

    def commit(root: Path, message: str) -> subprocess.CompletedProcess[str]:
        _write(root, "a.txt", message + "\n")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True, env=env)
        # the machine-wide hook a plain repository gets: `aes commit check` on the message
        hook = root / ".git" / "hooks" / "commit-msg"
        hook.write_text(f'#!/bin/sh\nexec "{sys.executable}" -m agentic_engineering_system.cli commit check '
                        f'--root "$(git rev-parse --show-toplevel)" "$1"\n', encoding="utf-8")
        hook.chmod(0o755)
        subprocess.run(["git", "add", "."], cwd=root, check=True, env=env)
        return subprocess.run(["git", "-c", f"core.hooksPath={hook.parent}", "-c", "user.name=probe",
                               "-c", "user.email=probe@example.invalid", "commit", "-m", message],
                              cwd=root, capture_output=True, text=True, check=False, env=env)

    skipped = commit(throwaway / "fixture-repo", "fixture")
    assert skipped.returncode == 0, skipped.stderr
    assert "aes commit rule: skip" in skipped.stderr and str(throwaway.resolve()) in skipped.stderr
    log = next((throwaway / "fixture-repo" / ".git" / "aes").glob("commit-rule-*.jsonl"))
    entry = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
    assert (entry["verdict"], entry["subject"], entry["skip_root"]) == ("skip", "fixture", str(throwaway.resolve()))

    refused = commit(real / "project", "fixture")
    assert refused.returncode != 0 and "refuse" in refused.stderr

    own = throwaway / "own-rule"
    _write(own, ".aes/commit_rule.yaml", f"mode: enforce\nskip_roots: [{tmp_path}]\n")
    judged = commit(own, "fixture")
    assert judged.returncode != 0 and "refuse" in judged.stderr

    from agentic_engineering_system.commit_rule import load_rule_config
    assert load_rule_config(own).skip_roots == ()
    assert load_rule_config(real / "project").skip_roots == (throwaway.resolve(),)


def test_skip_root_at_or_above_home_is_ignored(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A too-broad skip root ('/', '~') must not switch the rule off for every repository (issue #488)."""
    from agentic_engineering_system.commit_rule import RuleConfig, skipped_by

    home = tmp_path / "home"
    repo = home / "code" / "repo"
    repo.mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    assert skipped_by(repo, RuleConfig(skip_roots=(Path("/"), home.resolve()))) is None
    throwaway = (tmp_path / "throwaway").resolve()
    (throwaway / "r").mkdir(parents=True)
    assert skipped_by(throwaway / "r", RuleConfig(skip_roots=(Path("/"), throwaway))) == throwaway


def test_auto_tag_names_its_job_and_touches_no_running_thing() -> None:
    """[Auto] is for scheduled jobs: it must name the job and may not change anything that runs."""
    config = RuleConfig(plan_roots=())
    data = [FileChange("data/prices.csv", "M", 4000, 3900)]
    assert judge("[Auto] refresh prices", data, [], config).verdict == "refuse"
    ok = judge("[Auto] refresh prices\n\nAuto-job: price-sync.timer", data, [], config)
    assert ok.verdict == "accept" and "price-sync.timer" in ok.reasons[0]
    risky = judge("[Auto] refresh\n\nAuto-job: price-sync.timer", [FileChange("Dockerfile", "M", 1, 0)], [], config)
    assert risky.verdict == "refuse" and "Dockerfile" in risky.reasons[0]


def test_enforce_with_plan_adoption_observe_blocks_untagged_but_not_unadopted_plans(repo: Path) -> None:
    """Staged enforcement: tags and trivial size are refused; a plan that is not adopted is only logged."""
    _write(repo, ".aes/commit_rule.yaml", "mode: enforce\nplan_adoption: observe\n")
    _git(repo, "add", ".aes/commit_rule.yaml")
    assert _git(repo, "commit", "-m", "[Unplanned] stage config\n\nEmergency: test setup").returncode == 0
    _write(repo, "README.md", "# Consumer\n\nA line with a typo fixed.\n")
    _git(repo, "add", "README.md")
    untagged = _git(repo, "commit", "-m", "fix typo")
    assert untagged.returncode != 0 and "no tag" in untagged.stderr
    unadopted = _git(repo, "commit", "-m", "[Plan #999] fix typo under a plan that does not exist")
    assert unadopted.returncode == 0 and "plan adoption is observe-only" in unadopted.stderr


def test_goal_plan_owned_by_another_repository_resolves_through_the_workspace(repo: Path, tmp_path: Path) -> None:
    """Federated plans: the plan and its receipt live in the repository that owns them; a commit
    in another repository under the same workspace that names it is judged against it."""
    owner = tmp_path / "owner"
    owner.mkdir()
    assert _git(owner, "init", "-q").returncode == 0
    _adopted_plan(owner, "fed")
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Goal fed] U1: worker tools")
    assert done.returncode == 1 and "no plan fed found" in done.stderr
    _write(repo, ".aes/commit_rule.yaml", f"mode: enforce\nplan_workspace: {tmp_path}\n")
    _git(repo, "add", ".aes/commit_rule.yaml")
    done = _git(repo, "commit", "-m", "[Goal fed] U1: worker tools")
    assert done.returncode == 0, done.stderr
    assert "plan fed adopted (proposals/fed/README.md)" in done.stderr
    _write(repo, "notes.md", "x\n" * 70)
    _git(repo, "add", "notes.md")
    done = _git(repo, "commit", "-m", "[Goal nosuch] more work")
    assert done.returncode == 1 and f"every repository in {tmp_path}" in done.stderr


def test_goal_plan_on_another_repositorys_main_resolves_when_its_checkout_is_elsewhere(
        repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The owner repository's checkout sits on a branch without the plan; its main has it. The
    working-tree scan cannot see it; the plan index, read from main through git, can."""
    from agentic_engineering_system.commit_rule import build_plan_index

    index = tmp_path / "plan-index.json"
    monkeypatch.setenv("AES_PLAN_INDEX", str(index))
    monkeypatch.setenv("AES_PLAN_INDEX_REFRESH", "0")
    owner = tmp_path / "owner"
    owner.mkdir()
    assert _git(owner, "init", "-q", "-b", "main").returncode == 0
    _adopted_plan(owner, "onmain")
    _git(owner, "add", ".")
    assert _git(owner, "commit", "-q", "-m", "adopt onmain").returncode == 0
    _git(owner, "update-ref", "refs/remotes/origin/main", "main")
    assert _git(owner, "checkout", "-q", "--orphan", "other").returncode == 0
    _git(owner, "rm", "-rq", "--cached", ".")
    shutil.rmtree(owner / "proposals")
    assert not (owner / "proposals").exists()
    _write(repo, ".aes/commit_rule.yaml", f"mode: enforce\nplan_workspace: {tmp_path}\n")
    _git(repo, "add", ".aes/commit_rule.yaml")
    _stage_worker_tools(repo)
    env = {**ENV, "AES_PLAN_INDEX": str(index), "AES_PLAN_INDEX_REFRESH": "0"}
    refused = subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", "commit", "-m",
                              "[Goal onmain] U1: worker tools"], cwd=repo, capture_output=True, text=True, env=env)
    assert refused.returncode == 1 and "no plan onmain found" in refused.stderr, refused.stderr
    built = build_plan_index(tmp_path, index)
    assert built["repos"][str(owner.resolve())]["plans"] == {"onmain": ["proposals/onmain/README.md"]}
    done = subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", "commit", "-m",
                           "[Goal onmain] U1: worker tools"], cwd=repo, capture_output=True, text=True, env=env)
    assert done.returncode == 0, done.stderr
    assert "adopted on the default branch (owner origin/main:proposals/onmain/README.md)" in done.stderr


def test_foreign_plan_reads_preserve_repository_identity_under_hook_environment(
        repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """AES #483: Git's hook environment used PM objects for every foreign repo."""
    from agentic_engineering_system import commit_rule as cr

    owner = tmp_path / "owner"
    owner.mkdir()
    assert _git(owner, "init", "-q", "-b", "main").returncode == 0
    _adopted_plan(owner, "foreign")
    _git(owner, "add", ".")
    assert _git(owner, "commit", "-q", "-m", "adopt foreign").returncode == 0
    owner_sha = _git(owner, "rev-parse", "HEAD").stdout.strip()
    _git(owner, "update-ref", "refs/remotes/origin/main", owner_sha)
    _git(owner, "checkout", "-q", "--orphan", "other")
    _git(owner, "rm", "-rq", "--cached", ".")
    shutil.rmtree(owner / "proposals")

    index = tmp_path / "plan-index.json"
    monkeypatch.setenv("AES_PLAN_INDEX", str(index))
    monkeypatch.setenv("AES_PLAN_INDEX_REFRESH", "0")
    alternate = tmp_path / "consumer-alternate-index"
    shutil.copyfile(repo / ".git/index", alternate)
    _write(repo, "alternate-only.txt", "local staged evidence\n")
    hook_env = {**ENV, "GIT_DIR": str(repo / ".git"), "GIT_WORK_TREE": str(repo), "GIT_INDEX_FILE": str(alternate)}
    staged = subprocess.run(["git", "add", "alternate-only.txt"], cwd=repo, env=hook_env, capture_output=True, text=True)
    assert staged.returncode == 0, staged.stderr
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        monkeypatch.setenv(name, hook_env[name])

    built = cr.build_plan_index(tmp_path, index)
    assert built["repos"][str(owner.resolve())]["sha"] == owner_sha
    assert built["repos"][str(owner.resolve())]["plans"] == {"foreign": ["proposals/foreign/README.md"]}
    verdicts, stale = cr.indexed_adoption(tmp_path, "foreign")
    assert any(ok for ok, why, meta in verdicts), verdicts
    assert stale is False
    text = cr._plan_text(RuleConfig(plan_roots=(), plan_workspace=tmp_path), "foreign")
    assert text is not None and text[0] == owner
    assert "plan_id: foreign" in text[2]
    assert cr._git(repo, "show", ":alternate-only.txt") == "local staged evidence\n"
    assert _git(repo, "show", ":alternate-only.txt").returncode != 0
    _adopted_plan(repo, "local-alternate")
    staged = subprocess.run(["git", "add", "proposals/local-alternate"], cwd=repo,
                            env=hook_env, capture_output=True, text=True)
    assert staged.returncode == 0, staged.stderr
    local = cr.staged_adoption(repo, None, "local-alternate")
    assert local is not None and local[0] is True, local
    assert _git(repo, "show", ":proposals/local-alternate/README.md").returncode != 0


def test_background_plan_refresh_clears_only_git_local_environment(
        repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from agentic_engineering_system import commit_rule as cr

    monkeypatch.setenv("AES_PLAN_INDEX", str(tmp_path / "index.json"))
    monkeypatch.delenv("AES_PLAN_INDEX_REFRESH", raising=False)
    monkeypatch.setenv("GIT_DIR", str(repo / ".git"))
    monkeypatch.setenv("GIT_INDEX_FILE", str(repo / ".git/index"))
    monkeypatch.setenv("GIT_SSH_COMMAND", "ssh -o BatchMode=yes")
    local_names = cr._git_local_env_vars()
    calls = []
    monkeypatch.setattr(cr.subprocess, "Popen", lambda args, **kwargs: calls.append((args, kwargs)))
    cr._refresh_index_in_background(tmp_path)
    env = calls[0][1]["env"]
    assert set(local_names).isdisjoint(env)
    assert env["GIT_SSH_COMMAND"] == "ssh -o BatchMode=yes"
    assert env["PATH"] == os.environ["PATH"]


def test_conflict_surface_matching_and_repository_names(tmp_path: Path) -> None:
    """#218: the scope vocabulary is Company Planning's conflictSurface; only write/exclusive
    repository_path surfaces naming this repository grant edits."""
    from agentic_engineering_system.commit_rule import in_surface, repository_names, write_scope

    assert in_surface("tests/unit/test_x.py", "tests/unit/test_x.py")
    assert in_surface("tests/unit/test_x.py", "tests/unit") and in_surface("tests/unit/test_x.py", "tests/unit/")
    assert not in_surface("tests/unit_other/a.py", "tests/unit")
    assert in_surface("pkg/a/b/c.py", "pkg/**/*.py") and in_surface("pkg/c.py", "pkg/**/*.py")
    assert in_surface("pkg/c.py", "pkg/*.py") and not in_surface("pkg/a/c.py", "pkg/*.py")
    assert not in_surface("anything", "")

    meta = {"conflict_surfaces": [
        {"kind": "repository_path", "repository": "Owner/Repo", "target": "src/a.py", "access": "write"},
        {"kind": "repository_path", "repository": "repo", "target": "src/b", "access": "exclusive"},
        {"kind": "repository_path", "repository": "owner/repo", "target": "src/c.py", "access": "read"},
        {"kind": "repository_path", "repository": "other/repo2", "target": "src/d.py", "access": "write"},
        {"kind": "contract", "repository": "owner/repo", "target": "src/e.py", "access": "write"},
        "not a mapping",
    ]}
    assert write_scope(meta, ("owner/repo", "repo")) == ["src/a.py", "src/b"]
    assert write_scope({"conflict_surfaces": "src/"}, ("repo",)) == []

    root = tmp_path / "checkout-folder"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "remote", "add", "origin", "git@github-personal:Owner/Repo.git")
    assert repository_names(root) == ("owner/repo", "repo", "checkout-folder")


def test_asked_line_is_recorded_and_never_changes_the_verdict() -> None:
    """Asked: says who wanted the change, in their words; size and effect still decide the tag."""
    config = RuleConfig(plan_roots=())
    small = [FileChange("README.md", "M", 1, 1)]
    big = [FileChange(f"notes/{i}.md", "A", 30, 0) for i in range(5)]
    ok = judge('[Trivial] fix typo\n\nAsked: Brian 2026-10-07 "fix the typo"', small, [], config)
    assert ok.verdict == "accept" and ok.asked == 'Brian 2026-10-07 "fix the typo"'
    refused = judge('[Trivial] add notes\n\nAsked: Brian 2026-10-07 "write the notes"', big, [], config)
    assert refused.verdict == "refuse" and "not trivial" in refused.reasons[0]
    assert refused.asked.startswith("Brian")
    assert judge("[Trivial] fix typo", small, [], config).asked == ""


def test_plan_index_does_not_cache_a_failed_search_as_no_plans(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """git grep exits 1 for 'no match' and 2+ for an error; an error must not be recorded as 'this
    repository holds no plans', or the plan stays invisible until the repository's main moves."""
    import agentic_engineering_system.commit_rule as cr

    repo = tmp_path / "ws" / "owner"
    repo.mkdir(parents=True)
    assert _git(repo, "init", "-q", "-b", "main").returncode == 0
    _adopted_plan(repo, "solid")
    _git(repo, "add", ".")
    assert _git(repo, "commit", "-q", "-m", "plan").returncode == 0
    index = tmp_path / "idx.json"
    real_run = subprocess.run

    def failing_grep(cmd, *a, **k):
        if "grep" in cmd:
            return subprocess.CompletedProcess(cmd, 128, "", "fatal: simulated failure")
        return real_run(cmd, *a, **k)
    monkeypatch.setattr(cr.subprocess, "run", failing_grep)
    built = cr.build_plan_index(tmp_path / "ws", index)
    assert str(repo.resolve()) not in built["repos"], "a failed search was cached as an empty entry"
    assert built["errors"] and "simulated failure" in built["errors"][0]
    monkeypatch.setattr(cr.subprocess, "run", real_run)
    again = cr.build_plan_index(tmp_path / "ws", index)
    assert again["repos"][str(repo.resolve())]["plans"] == {"solid": ["proposals/solid/README.md"]}


def test_only_one_background_index_refresh_runs_at_a_time(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import agentic_engineering_system.commit_rule as cr

    monkeypatch.setenv("AES_PLAN_INDEX", str(tmp_path / "idx.json"))
    monkeypatch.delenv("AES_PLAN_INDEX_REFRESH", raising=False)
    started: list[list[str]] = []
    monkeypatch.setattr(cr.subprocess, "Popen", lambda cmd, **k: started.append(cmd))
    for _ in range(5):
        cr._refresh_index_in_background(tmp_path)
    assert len(started) == 1, f"{len(started)} rebuilds started for one stale index"


def _last_log(root: Path) -> dict:
    """The rule's own record of the commit just attempted (the hook writes one JSON line per verdict)."""
    logs = sorted((root / ".git" / "aes").glob("commit-rule-*.jsonl"))
    return json.loads(logs[-1].read_text(encoding="utf-8").splitlines()[-1])


def _quick_plan(root: Path, plan_id: str, files: list[str]) -> None:
    """A plan shaped like Company Planning's quick-adopt output, with an adoption decision bound to its bytes."""
    listing = "\n".join(f"- `{f}`" for f in files)
    _write(root, f"proposals/{plan_id}/{plan_id}.md",
           f"---\nplan_id: {plan_id}\nplanning_path: requested\n"
           f"method_conformance_receipt: proposals/{plan_id}/{plan_id}.receipt.json\n---\n\n# Quick plan\n\n"
           f"## Vertical and reset\n\nOne vertical over these files:\n\n{listing}\n\nReset: git revert.\n")
    _write(root, f"proposals/{plan_id}/{plan_id}.receipt.json", json.dumps({"verdict": "pass"}) + "\n")
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    _write(root, f"proposals/{plan_id}/{plan_id}.adoption-decision.json", json.dumps({
        "decision": "adopted", "plan_sha256": digest(root / f"proposals/{plan_id}/{plan_id}.md"),
        "receipt_sha256": digest(root / f"proposals/{plan_id}/{plan_id}.receipt.json")}) + "\n")


def test_quick_plan_commit_is_logged_for_its_check_output_and_file_list(repo: Path) -> None:
    """Plan commit-rule-followups: for a quick-adopt plan, the rule logs whether the commit adds the saved
    check output and stays inside the plan's file list. The notes never change the verdict."""
    _quick_plan(repo, "fix-label", ["README.md"])
    _git(repo, "add", "proposals/fix-label")
    assert _git(repo, "commit", "-q", "-m", "[Shaping fix-label] adopt the plan").returncode == 0
    # inside the list, with the check output: accepted, both notes clean
    _write(repo, "README.md", "# Consumer\n\nA line with a typo fixed.\n")
    _write(repo, "proposals/fix-label/fix-label.check.txt", "$ grep -c tpyo README.md\n0\nexit 1\n")
    _git(repo, "add", "README.md", "proposals/fix-label/fix-label.check.txt")
    done = _git(repo, "commit", "-q", "-m", '[Goal fix-label] fix the typo\n\nAsked: Brian 2026-10-07 "fix the typo"')
    assert done.returncode == 0, done.stderr
    entry = _last_log(repo)
    assert entry["verdict"] == "accept"
    assert entry["notes"] == ["quick plan fix-label: saved check output proposals/fix-label/fix-label.check.txt present",
                              "quick plan fix-label: every changed file is in the plan's list"]
    # a file outside the list: still accepted (notes only), the note names the file
    _write(repo, "notes.md", "unrelated\n")
    _git(repo, "add", "notes.md")
    done = _git(repo, "commit", "-q", "-m", "[Goal fix-label] also a note")
    assert done.returncode == 0, done.stderr
    entry = _last_log(repo)
    assert entry["verdict"] == "accept"
    assert "quick plan fix-label: files outside the plan's list: notes.md" in entry["notes"]
    assert "files outside the plan's list: notes.md" in done.stderr


def test_quick_plan_commit_without_its_check_output_is_logged_as_missing(repo: Path) -> None:
    _quick_plan(repo, "fix-label", ["README.md"])
    _git(repo, "add", "proposals/fix-label")
    assert _git(repo, "commit", "-q", "-m", "[Shaping fix-label] adopt the plan").returncode == 0
    _write(repo, "README.md", "# Consumer\n\nA line with a typo fixed.\n")
    _git(repo, "add", "README.md")
    done = _git(repo, "commit", "-q", "-m", "[Goal fix-label] fix the typo")
    assert done.returncode == 0, done.stderr
    entry = _last_log(repo)
    assert entry["verdict"] == "accept"
    assert entry["notes"][0] == "quick plan fix-label: saved check output proposals/fix-label/fix-label.check.txt missing"


def test_a_full_plan_gets_no_quick_plan_notes(repo: Path) -> None:
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-q", "-m", "[Goal demo] U2: worker tools")
    assert done.returncode == 0, done.stderr
    assert _last_log(repo)["notes"] == []


def _real_durable_check() -> Path | None:
    """Company Planning's durable_docs_check.py: $AES_DURABLE_DOCS_CHECK, or a company-planning checkout
    beside one of this checkout's parent folders."""
    if os.environ.get("AES_DURABLE_DOCS_CHECK"):
        return Path(os.environ["AES_DURABLE_DOCS_CHECK"])
    rel = Path("company-planning/plugins/company-planning/scripts/durable_docs_check.py")
    return next((d / rel for d in REPO.parents if (d / rel).is_file()), None)


def _durable_repo(repo: Path, script: Path, durable_line: str, mode: str = "enforce") -> None:
    """A repository declaring durable_documents whose trace names src/whygame5/graph.py as RULE-A's owner,
    and an adopted quick plan carrying quick-adopt's durable-documents completion command."""
    _write(repo, ".agentic/repo.yaml", "durable_documents:\n  schema_version: \"0.1\"\n"
           "  system_model: {prose: docs/model/ODD.md, trace: docs/model/trace.yaml}\n")
    _write(repo, "docs/model/ODD.md", "# Model\n\nRULE-A: graph edges are acyclic.\n")
    _write(repo, "docs/model/trace.yaml", "rules:\n  - id: RULE-A\n    statement: graph edges are acyclic\n"
           "    owner: src/whygame5/graph.py\n    checks: [tests/test_replay.py]\n")
    _write(repo, ".aes/commit_rule.yaml", f"mode: {mode}\ndoc_reach: observe\ndurable_check: {script}\n")
    _git(repo, "add", ".agentic", "docs", ".aes")
    assert _git(repo, "commit", "-q", "-m", "[Unplanned] declare durable documents\n\nEmergency: fixture").returncode == 0
    base = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _quick_plan(repo, "edit-graph", ["src/whygame5/graph.py", "docs/model/trace.yaml"])
    plan = repo / "proposals/edit-graph/edit-graph.md"
    plan.write_text(plan.read_text(encoding="utf-8") + f"\n## Durable documents\n\n{durable_line}\n\n"
                    f'At completion, `python3 "$SESSION_PLUGIN_ROOT/scripts/durable_docs_check.py" --repo . '
                    f"--plan proposals/edit-graph/edit-graph.md --range {base}..HEAD` must exit 0.\n", encoding="utf-8")
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    _write(repo, "proposals/edit-graph/edit-graph.adoption-decision.json", json.dumps({
        "decision": "adopted", "plan_sha256": digest(plan),
        "receipt_sha256": digest(repo / "proposals/edit-graph/edit-graph.receipt.json")}) + "\n")
    _git(repo, "add", "proposals/edit-graph")
    adopted = _git(repo, "commit", "-q", "-m", "[Shaping edit-graph] adopt the plan\n\nEmergency: fixture")
    assert adopted.returncode == 0, adopted.stderr


def test_durable_docs_check_refuses_unnamed_owner_and_accepts_named(repo: Path) -> None:
    """A [Goal] commit that edits a durable rule's owner file under a quick plan whose Durable documents
    line does not name the rule is refused (check durable-docs, PLAN-OWNER-UNNAMED); naming the rule and
    updating the trace in the same plan lets the same edit land. Runs Company Planning's real check."""
    script = _real_durable_check()
    if script is None:
        pytest.skip("Company Planning's durable_docs_check.py not found; set AES_DURABLE_DOCS_CHECK")
    _durable_repo(repo, script, "Durable documents: none -- tidy wording only here")
    _brian_owned(repo)  # so the new-document check applies
    _write(repo, "src/whygame5/graph.py", "# graph, edges now checked\n")
    _write(repo, "docs/edges.md", "# Edges\n\nAn unlinked page: the observe-only new-document check would refuse it.\n")
    _git(repo, "add", "src/whygame5/graph.py", "docs/edges.md")
    before = _commits(repo)
    done = _git(repo, "commit", "-q", "-m", "[Goal edit-graph] check edges")
    assert done.returncode == 1, done.stderr
    assert "PLAN-OWNER-UNNAMED" in done.stderr and "RULE-A" in done.stderr
    entry = _last_log(repo)
    assert entry["verdict"] == "refuse" and entry["check"] == "durable-docs"  # not hidden behind doc-reach
    assert "not reached from wiki/index.md" in done.stderr
    assert _commits(repo) == before

    # the plan names the rule (re-adopted), and the trace changes with the code: accepted
    _git(repo, "reset", "-q", "HEAD", "src/whygame5/graph.py", "docs/edges.md")
    (repo / "docs/edges.md").unlink()
    plan = repo / "proposals/edit-graph/edit-graph.md"
    plan.write_text(plan.read_text(encoding="utf-8").replace(
        "Durable documents: none -- tidy wording only here", "Durable documents: system_model#RULE-A"), encoding="utf-8")
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    _write(repo, "proposals/edit-graph/edit-graph.adoption-decision.json", json.dumps({
        "decision": "adopted", "plan_sha256": digest(plan),
        "receipt_sha256": digest(repo / "proposals/edit-graph/edit-graph.receipt.json")}) + "\n")
    _git(repo, "add", "proposals/edit-graph")
    assert _git(repo, "commit", "-q", "-m", "[Shaping edit-graph] name RULE-A\n\nEmergency: fixture").returncode == 0
    _write(repo, "docs/model/trace.yaml", "rules:\n  - id: RULE-A\n    statement: graph edges are acyclic, checked\n"
           "    owner: src/whygame5/graph.py\n    checks: [tests/test_replay.py]\n")
    _git(repo, "add", "src/whygame5/graph.py", "docs/model/trace.yaml")
    done = _git(repo, "commit", "-q", "-m", "[Goal edit-graph] check edges")
    assert done.returncode == 0, done.stderr
    entry = _last_log(repo)
    assert entry["verdict"] == "accept" and entry["check"] == "plan-adoption"
    assert any("durable-docs: mode=plan" in n and "exit 0" in n for n in entry["notes"]), entry["notes"]


def _fake_durable_check(tmp_path: Path, findings: str) -> Path:
    """A stand-in check script printing fixed findings (exit 1 when there are any), the real script's format."""
    script = tmp_path / "fake_durable_docs_check.py"
    lines = [f for f in findings.splitlines() if f]
    script.write_text("import sys\n" + "".join(f"print({f!r})\n" for f in lines)
                      + f"print('durable-docs: mode=plan repo=x findings={len(lines)} (fake), exit {1 if lines else 0}')\n"
                      + f"sys.exit({1 if lines else 0})\n", encoding="utf-8")
    return script


def test_durable_docs_check_observe_and_skips(repo: Path, tmp_path: Path) -> None:
    """durable: observe only logs a refusal; an unchanged declared document is a note, not a refusal; a missing
    check script leaves a note and never refuses; a quick plan without the completion command gets no check."""
    unnamed = "FINDING PLAN-OWNER-UNNAMED role=system_model id=RULE-A file=src/whygame5/graph.py: name it"
    script = _fake_durable_check(tmp_path, unnamed)
    _durable_repo(repo, script, "Durable documents: none -- tidy wording only here")
    _write(repo, ".aes/commit_rule.yaml", f"mode: enforce\ndurable: observe\ndurable_check: {script}\n")
    _git(repo, "add", ".aes/commit_rule.yaml")
    assert _git(repo, "commit", "-q", "-m", "[Unplanned] observe\n\nEmergency: fixture").returncode == 0
    _write(repo, "src/whygame5/graph.py", "# graph, edges now checked\n")
    _git(repo, "add", "src/whygame5/graph.py")
    done = _git(repo, "commit", "-q", "-m", "[Goal edit-graph] check edges")
    assert done.returncode == 0, done.stderr
    assert "would refuse (durable-docs check is observe-only)" in done.stderr
    assert _last_log(repo)["check"] == "durable-docs"

    # an unchanged declared document only: a note, accepted under enforce
    unchanged = "FINDING PLAN-UNCHANGED role=system_model id=RULE-A file=docs/model/ODD.md: declared document not changed"
    script = _fake_durable_check(tmp_path, unchanged)
    _write(repo, ".aes/commit_rule.yaml", f"mode: enforce\ndurable_check: {script}\n")
    _write(repo, "src/whygame5/graph.py", "# graph, edges checked twice\n")
    _git(repo, "add", ".aes/commit_rule.yaml", "src/whygame5/graph.py")
    done = _git(repo, "commit", "-q", "-m", "[Goal edit-graph] check edges again")
    assert done.returncode == 0, done.stderr
    entry = _last_log(repo)
    assert entry["verdict"] == "accept" and any("PLAN-UNCHANGED" in n for n in entry["notes"])

    # the check script is missing: a note, never a refusal
    _write(repo, ".aes/commit_rule.yaml", f"mode: enforce\ndurable_check: {tmp_path / 'absent.py'}\n")
    _write(repo, "src/whygame5/graph.py", "# graph, third pass\n")
    _git(repo, "add", ".aes/commit_rule.yaml", "src/whygame5/graph.py")
    env = {**ENV, "AES_DURABLE_DOCS_CHECK": "", "SESSION_PLUGIN_ROOT": ""}
    done = subprocess.run(["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", "commit", "-q",
                           "-m", "[Goal edit-graph] third pass"], cwd=repo, capture_output=True, text=True, env=env)
    assert done.returncode == 0, done.stderr
    assert any("durable_docs_check.py not found" in n for n in _last_log(repo)["notes"])

    # a quick plan without the completion command (an older plan): no durable check at all
    script = _fake_durable_check(tmp_path, unnamed)
    _write(repo, ".aes/commit_rule.yaml", f"mode: enforce\ndurable_check: {script}\n")
    _git(repo, "add", ".aes/commit_rule.yaml")
    assert _git(repo, "commit", "-q", "-m", "[Unplanned] config\n\nEmergency: fixture").returncode == 0
    _quick_plan(repo, "fix-label", ["README.md"])
    _git(repo, "add", "proposals/fix-label")
    assert _git(repo, "commit", "-q", "-m", "[Shaping fix-label] adopt the plan").returncode == 0
    _write(repo, "README.md", "# Consumer\n\nA line with a typo fixed.\n")
    _git(repo, "add", "README.md")
    done = _git(repo, "commit", "-q", "-m", "[Goal fix-label] fix the typo")
    assert done.returncode == 0, done.stderr
    assert not any("durable-docs" in n for n in _last_log(repo)["notes"])


def test_trivial_may_not_touch_test_setup_or_a_script_a_systemd_unit_runs(repo: Path) -> None:
    """conftest.py changes every test run; a script named in a tracked unit's ExecStart runs on a schedule."""
    _write(repo, "integration/conftest.py", "import os\n")
    _write(repo, "scripts/job.py", "print('job')\n")
    _write(repo, "deploy/job.service", "[Service]\nExecStart=/usr/bin/python3 %h/code/consumer/scripts/job.py\n")
    _git(repo, "add", "integration/conftest.py", "scripts/job.py", "deploy/job.service")
    assert _git(repo, "commit", "-q", "-m", "[Unplanned] add the job\n\nEmergency: test setup").returncode == 0
    _write(repo, "integration/conftest.py", "import os\nimport sys\n")
    _git(repo, "add", "integration/conftest.py")
    done = _git(repo, "commit", "-q", "-m", "[Trivial] tidy test setup")
    assert done.returncode == 1, done.stderr
    entry = _last_log(repo)
    assert entry["verdict"] == "refuse" and "touches running-thing file(s): integration/conftest.py" in entry["reasons"][0]
    _git(repo, "reset", "-q", "HEAD", "integration/conftest.py")
    _git(repo, "checkout", "-q", "--", "integration/conftest.py")
    _write(repo, "scripts/job.py", "print('job, now quieter')\n")
    _git(repo, "add", "scripts/job.py")
    done = _git(repo, "commit", "-q", "-m", "[Trivial] quieter job")
    assert done.returncode == 1, done.stderr
    entry = _last_log(repo)
    assert entry["verdict"] == "refuse" and "touches running-thing file(s): scripts/job.py" in entry["reasons"][0]


def test_plan_names_with_capital_letters_are_read_as_plan_tags(repo: Path) -> None:
    """#193: '[Goal PATH-brent-v1-2026-10-02]' was logged as 'no tag'. A plan id may contain capitals."""
    _write(repo, "notes.md", "a\n" * 70)
    _git(repo, "add", "notes.md")
    _git(repo, "commit", "-q", "-m", "[Goal Upper-Case-Plan] work under a plan named with capitals")
    entry = _last_log(repo)
    assert entry["tag"] == "Goal Upper-Case-Plan", entry
    assert "no tag" not in entry["reasons"][0]
    _git(repo, "reset", "-q", "HEAD", "notes.md")
    _write(repo, "proposals/Upper-Case-Plan/README.md", "# draft\n")
    _git(repo, "add", "proposals/Upper-Case-Plan/README.md")
    done = _git(repo, "commit", "-q", "-m", "[Shaping Upper-Case-Plan] draft")
    entry = _last_log(repo)
    assert entry["tag"] == "Shaping Upper-Case-Plan" and entry["verdict"] == "accept", entry
    assert done.returncode == 0, done.stderr


def _brian_owned(root: Path, owner: str = "BrianMills2718") -> None:
    _git(root, "remote", "add", "origin", f"git@github.com:{owner}/consumer.git")


def test_new_document_the_wiki_does_not_reach_is_refused_with_the_line_to_add(repo: Path) -> None:
    _brian_owned(repo)
    _write(repo, "wiki/index.md", "# Wiki\n\n- [Readme](../README.md)\n")
    _git(repo, "add", "wiki/index.md")
    assert _git(repo, "commit", "-m", "[Trivial] add the wiki entry page").returncode == 0
    _write(repo, "docs/notes/why-agents.md", "# Why agents\n")
    _git(repo, "add", "docs/notes/why-agents.md")
    done = _git(repo, "commit", "-m", "[Trivial] note why we use agents")
    assert done.returncode == 1, done.stderr
    assert "docs/notes/why-agents.md" in done.stderr and "- [why-agents](../docs/notes/why-agents.md)" in done.stderr
    log = _last_log(repo)
    assert log["verdict"] == "refuse" and log["check"] == "doc-reach"
    _write(repo, "wiki/index.md", "# Wiki\n\n- [Readme](../README.md)\n- [why-agents](../docs/notes/why-agents.md)\n")
    _git(repo, "add", "wiki/index.md")
    done = _git(repo, "commit", "-m", "[Trivial] note why we use agents")
    assert done.returncode == 0, done.stderr


def test_new_document_two_links_deep_is_accepted_three_is_not(repo: Path) -> None:
    _brian_owned(repo)
    _write(repo, "wiki/index.md", "# Wiki\n\n- [Docs](../docs/README.md)\n")
    _write(repo, "docs/README.md", "# Docs\n\n- [Deep](deep/README.md)\n- [Two](two.md)\n")
    _write(repo, "docs/deep/README.md", "# Deep\n\n- [Three](three.md)\n")
    _write(repo, "docs/two.md", "# Two\n")
    _git(repo, "add", "wiki", "docs/README.md", "docs/two.md")
    assert _git(repo, "commit", "-m", "[Trivial] wiki and a page two links deep").returncode == 0
    _write(repo, "docs/deep/three.md", "# Three\n")
    _git(repo, "add", "docs/deep")
    done = _git(repo, "commit", "-m", "[Trivial] a page three links deep")
    assert done.returncode == 1 and "docs/deep/three.md" in done.stderr
    assert "docs/deep/README.md" not in done.stderr.split("within")[1].split(";")[0]


def test_no_wiki_asks_for_one_and_a_new_wiki_linking_it_is_accepted(repo: Path) -> None:
    _brian_owned(repo)
    _write(repo, "docs/guide.md", "# Guide\n")
    _git(repo, "add", "docs/guide.md")
    done = _git(repo, "commit", "-m", "[Trivial] add a guide")
    assert done.returncode == 1 and "has no wiki/index.md" in done.stderr
    _write(repo, "wiki/index.md", "# Wiki\n\n- [guide](../docs/guide.md)\n")
    _git(repo, "add", "wiki/index.md")
    assert _git(repo, "commit", "-m", "[Trivial] add a guide").returncode == 0


def test_existing_documents_exempt_files_auto_jobs_and_other_owners_are_not_refused(repo: Path) -> None:
    _brian_owned(repo)
    _write(repo, "README.md", "# Consumer\n\nEdited, still unlinked; it existed before.\n")
    _git(repo, "add", "README.md")
    assert _git(repo, "commit", "-m", "[Trivial] edit an existing unlinked page").returncode == 0
    # exempt by the daily check's rules: a template, a hidden tool folder (AGENTS.md and tests/ are
    # exempt too, but those touch a running thing and a governed root here, which other checks judge)
    _write(repo, "docs/TEMPLATE.md", "# Template\n")
    _write(repo, ".templates/page.md", "# Page template\n")
    _git(repo, "add", "docs/TEMPLATE.md", ".templates/page.md")
    done = _git(repo, "commit", "-m", "[Trivial] a template and a hidden tool page")
    assert done.returncode == 0, done.stderr
    _write(repo, "pages/daily.md", "# Daily page\n")
    _git(repo, "add", "pages/daily.md")
    done = _git(repo, "commit", "-m", "[Auto] daily page\n\nAuto-job: daily-pages")
    assert done.returncode == 0, done.stderr
    assert "logged only for [Auto]" in done.stderr
    _git(repo, "remote", "set-url", "origin", "git@github.com:Inside-Success/consumer.git")
    _write(repo, "docs/theirs.md", "# Someone else's repository\n")
    _git(repo, "add", "docs/theirs.md")
    assert _git(repo, "commit", "-m", "[Trivial] a page in a repository Brian does not own").returncode == 0


def test_the_suggested_line_works_for_a_file_name_with_a_hash(repo: Path) -> None:
    _brian_owned(repo)
    _write(repo, "wiki/index.md", "# Wiki\n")
    _git(repo, "add", "wiki/index.md")
    assert _git(repo, "commit", "-m", "[Trivial] add the wiki entry page").returncode == 0
    rel = "docs/plans/repo#218.goal.md"
    _write(repo, rel, "# Goal 218\n")
    _git(repo, "add", rel)
    done = _git(repo, "commit", "-m", "[Trivial] goal document for plan 218")
    assert done.returncode == 1 and "trivial:" not in done.stderr.split(" — ", 1)[1]
    line = done.stderr.split("(or to a page it links): ", 1)[1].split("; or list", 1)[0]
    assert line == "- [repo#218.goal](../docs/plans/repo%23218.goal.md)"
    _write(repo, "wiki/index.md", "# Wiki\n\n" + line + "\n")
    _git(repo, "add", "wiki/index.md")
    assert _git(repo, "commit", "-m", "[Trivial] goal document for plan 218").returncode == 0


def test_a_skeleton_plan_named_by_id_is_found(repo: Path) -> None:
    # Company Planning's `skeleton` writes `id:` (artifact_type: design_plan), not `plan_id:`.
    rel = "proposals/built/PLAN.md"
    _write(repo, rel, "---\nartifact_type: design_plan\nid: built\n"
                      "method_conformance_receipt: proposals/built/PLAN.receipt.json\n---\n\n# Built plan\n")
    _write(repo, "proposals/built/PLAN.receipt.json", json.dumps({"verdict": "pass"}) + "\n")
    digest = lambda p: hashlib.sha256((repo / p).read_bytes()).hexdigest()  # noqa: E731
    _write(repo, "proposals/built/PLAN.adoption-decision.json", json.dumps({
        "decision": "adopted", "plan_sha256": digest(rel),
        "receipt_sha256": digest("proposals/built/PLAN.receipt.json")}) + "\n")
    _git(repo, "add", "proposals/built")
    assert _git(repo, "commit", "-m", "[Shaping built] adopt the plan").returncode == 0
    _stage_worker_tools(repo)
    done = _git(repo, "commit", "-m", "[Goal built] worker tools")
    assert done.returncode == 0, done.stderr
    assert "plan built adopted" in done.stderr


def test_a_plan_merged_on_the_remote_is_indexed_after_a_fetching_rebuild(
        tmp_path: Path, repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from agentic_engineering_system import commit_rule as cr
    remote, ws = tmp_path / "remote.git", tmp_path / "ws"
    assert subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)]).returncode == 0
    ws.mkdir()
    clone = ws / "owner"
    assert subprocess.run(["git", "clone", "-q", str(remote), str(clone)], capture_output=True).returncode == 0
    _write(clone, "README.md", "# Owner\n")
    _git(clone, "add", ".")
    _git(clone, "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "start")
    _git(clone, "push", "-q", "origin", "HEAD:main")
    # another machine (here: another clone) merges an adopted plan on the remote's main
    other = tmp_path / "other"
    subprocess.run(["git", "clone", "-q", str(remote), str(other)], capture_output=True)
    _adopted_plan(other, "merged")
    _git(other, "add", ".")
    _git(other, "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "plan")
    _git(other, "push", "-q", "origin", "HEAD:main")
    index = tmp_path / "index.json"
    before = cr.build_plan_index(ws, index)
    assert not any("merged" in e["plans"] for e in before["repos"].values())  # the clone has not fetched
    consumer_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()
    monkeypatch.setenv("GIT_DIR", str(repo / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(repo))
    monkeypatch.setenv("GIT_INDEX_FILE", str(repo / ".git/index"))
    assert cr.fetch_all(ws) == []
    after = cr.build_plan_index(ws, index)
    assert any("merged" in e["plans"] for e in after["repos"].values())
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == consumer_sha


@pytest.mark.parametrize(("first_line", "tag"), [
    ("[Goal Upper-Case-1] capitals in a plan id", "Goal Upper-Case-1"),
    ("[Plan #3] numbered plan", "Plan #3"),
    ("[Trivial] typo", "Trivial"),
    ("[Shaping some-plan] draft", "Shaping some-plan"),
    ("[Bogus] not a commit-rule tag", None),
    ("no tag at all", None),
])
def test_commit_tag_prints_the_rule_grammar_tag(tmp_path: Path, first_line: str, tag: str | None,
                                                capsys: pytest.CaptureFixture[str]) -> None:
    """#414: chained repository hooks ask `aes commit tag` instead of keeping their own grammar copy."""
    message = tmp_path / "COMMIT_EDITMSG"
    message.write_text(f"# git comment line\n{first_line}\n\nbody\n", encoding="utf-8")
    status = main(["commit", "tag", str(message)])
    out = capsys.readouterr().out.strip()
    assert (status, out or None) == ((0, tag) if tag else (1, None))
    entry_tag = judge(message.read_text(encoding="utf-8").split("\n", 1)[1], [], [],
                      RuleConfig(mode="observe")).tag
    assert (entry_tag != "none") == (tag is not None), entry_tag  # same split as the rule itself


def test_a_shaping_commit_may_carry_link_lines_into_its_own_proposal(repo: Path) -> None:
    """#476/#531: a new proposal and the wiki link that makes it reachable land in one [Shaping] commit;
    anything else outside proposals/<id>/ is still refused."""
    _brian_owned(repo)
    _write(repo, "wiki/index.md", "# Wiki\n\n- [Readme](../README.md)\n")
    _git(repo, "add", "wiki/index.md")
    assert _git(repo, "commit", "-m", "[Trivial] add the wiki entry page").returncode == 0
    _write(repo, "proposals/demo-nav/plan.md", "# Demo plan\n")
    _git(repo, "add", "proposals/demo-nav/plan.md")
    done = _git(repo, "commit", "-m", "[Shaping demo-nav] draft")
    assert done.returncode == 1 and "proposals/demo-nav/plan.md" in done.stderr  # unreached: doc-reach refuses
    # a deleted line, a non-link line, or a link to another proposal outside the folder is refused
    for readme in ("# Consumer\n\n- [demo plan](proposals/demo-nav/plan.md)\n",
                   "# Consumer\n\nA line with a tpyo.\nMore prose.\n- [demo plan](proposals/demo-nav/plan.md)\n",
                   "# Consumer\n\nA line with a tpyo.\n- [demo plan](proposals/demo-nav/plan.md)\n- [other](proposals/other/x.md)\n"):
        _write(repo, "README.md", readme)
        _git(repo, "add", "README.md")
        done = _git(repo, "commit", "-m", "[Shaping demo-nav] draft")
        assert done.returncode == 1, (readme, done.stderr)
        assert "may touch only proposals/demo-nav/" in done.stderr, done.stderr
    _write(repo, "README.md", "# Consumer\n\nA line with a tpyo.\n- [demo plan](proposals/demo-nav/plan.md)\n")
    _git(repo, "add", "README.md")
    done = _git(repo, "commit", "-m", "[Shaping demo-nav] draft")
    assert done.returncode == 0, done.stderr
    assert _last_log(repo)["verdict"] == "accept"


def test_a_shaping_commit_may_create_the_first_wiki_index(repo: Path) -> None:
    """#531: in a repository with no wiki/index.md, the first index can land with the first proposal."""
    _brian_owned(repo)
    _write(repo, "proposals/first/plan.md", "# First plan\n")
    _write(repo, "wiki/index.md", "# Wiki\n\n- [first plan](../proposals/first/plan.md)\n")
    _git(repo, "add", "proposals/first/plan.md", "wiki/index.md")
    done = _git(repo, "commit", "-m", "[Shaping first] draft")
    assert done.returncode == 0, done.stderr
    # a new page other than the index is not navigation
    _write(repo, "proposals/second/plan.md", "# Second plan\n")
    _write(repo, "docs/second.md", "# Second\n\n- [second plan](../proposals/second/plan.md)\n")
    _git(repo, "add", "proposals/second/plan.md", "docs/second.md")
    done = _git(repo, "commit", "-m", "[Shaping second] draft")
    assert done.returncode == 1 and "docs/second.md" in done.stderr, done.stderr


def test_preflight_reports_the_hooks_verdict_without_logging(repo: Path) -> None:
    """#532: `aes commit check --preflight -m` judges the staged change before a commit is attempted,
    exits 1 on a refusal in any mode, and writes nothing to the commit-rule log."""
    _brian_owned(repo)
    _write(repo, "wiki/index.md", "# Wiki\n\n- [Readme](../README.md)\n")
    _git(repo, "add", "wiki/index.md")
    assert _git(repo, "commit", "-m", "[Trivial] add the wiki entry page").returncode == 0
    logs = sorted((repo / ".git" / "aes").glob("commit-rule-*.jsonl"))
    before = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in logs)
    _write(repo, "proposals/pre/plan.md", "# Pre plan\n")
    _git(repo, "add", "proposals/pre/plan.md")
    cmd = [sys.executable, "-m", "agentic_engineering_system.cli", "commit", "check", "--preflight",
           "--root", str(repo), "-m", "[Shaping pre] draft"]
    done = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, env=ENV)
    assert done.returncode == 1 and "preflight" in done.stderr and "proposals/pre/plan.md" in done.stderr, done.stderr
    _write(repo, "wiki/index.md", "# Wiki\n\n- [Readme](../README.md)\n- [pre plan](../proposals/pre/plan.md)\n")
    _git(repo, "add", "wiki/index.md")
    done = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, env=ENV)
    assert done.returncode == 0 and "accept [Shaping pre]" in done.stderr, done.stderr
    logs = sorted((repo / ".git" / "aes").glob("commit-rule-*.jsonl"))
    assert sum(len(p.read_text(encoding="utf-8").splitlines()) for p in logs) == before
    assert _git(repo, "commit", "-m", "[Shaping pre] draft").returncode == 0  # the hook agrees
