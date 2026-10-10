"""Seeded-defect tests for durable_docs_check.py (plan aes-durable-docs, M2).

Each test builds a clean repository that passes, plants one defect, and asserts the
specific finding for that element, so a pass is not the trivial answer.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import durable_docs_check as ddc  # noqa: E402

GOAL = """# Goal

## Introduction and Goals

### Requirements Overview
Plans complete only when the documents they change are current.

### Quality Goals
A fresh reader answers rule questions from the wiki.

### Stakeholders
not_applicable: solo maintainer, agents are the readers

## North star (AES extension)
A reader trusts the durable documents as current.

## Thesis (AES extension)
Declaring document updates at adoption and checking them at completion keeps documents current.

## Thesis disproof (AES extension)
Half of sampled plans declare none or make mechanical edits.

## Non-goals
Rewriting old plans.
"""

REQS = """# Requirements

## REQ-12 Members cannot hoard books
Success: a member with an overdue loan is refused at checkout.
Disproof: an overdue member completes a checkout.
"""

TRACE = {
    "entities": [{"id": "ENT-LOAN", "name": "Loan"}],
    "processes": [{"id": "PROC-CHECKOUT", "enforces": ["RULE-LOAN-OVERDUE"]}],
    "rules": [
        {
            "id": "RULE-LOAN-OVERDUE",
            "statement": "no borrowing while overdue",
            "owner": "src/loans.py",
            "checks": ["tests/test_loans.py::test_checkout_refused_when_overdue"],
            "decisions": ["docs/decisions/0031-fourteen-days.md"],
        }
    ],
}

ADR = """# 0031 Loans are overdue after 14 days

Governs: RULE-LOAN-OVERDUE

Decision: 14 days, not 21. Wrong when: more than 10% of loans are renewed once.
"""

BLOCK = {
    "schema_version": "0.1",
    "goal": "docs/architecture/GOAL.md",
    "requirements": "docs/architecture/REQUIREMENTS.md",
    "system_model": {"prose": "docs/model/ODD.md", "trace": "docs/model/trace.yaml"},
    "decisions": "docs/decisions/",
    "glossary": {"not_applicable": "small fixture, no vocabulary questions"},
    "plans": "docs/plans/",
}


def run(repo: Path, *args: str) -> None:
    # Fixture repositories are throwaway; the workspace's global commit-rule hooks do not apply.
    subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-C", str(repo), *args], check=True, capture_output=True)


def write(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit(repo: Path, msg: str) -> str:
    run(repo, "add", "-A")
    run(repo, "commit", "-q", "-m", msg)
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    run(tmp_path, "init", "-q")
    run(tmp_path, "config", "user.email", "t@example.invalid")
    run(tmp_path, "config", "user.name", "t")
    write(tmp_path, ".agentic/repo.yaml", yaml.safe_dump({"durable_documents": BLOCK}))
    write(tmp_path, "docs/architecture/GOAL.md", GOAL)
    write(tmp_path, "docs/architecture/REQUIREMENTS.md", REQS)
    write(tmp_path, "docs/model/ODD.md", "# System model\n\nLoans and checkout.\n")
    write(tmp_path, "docs/model/trace.yaml", yaml.safe_dump(TRACE))
    write(tmp_path, "docs/decisions/0031-fourteen-days.md", ADR)
    write(tmp_path, "docs/plans/README.md", "# Plans\n")
    write(tmp_path, "src/loans.py", "def checkout():\n    pass\n")
    write(tmp_path, "tests/test_loans.py", "def test_checkout_refused_when_overdue():\n    pass\n")
    commit(tmp_path, "clean")
    return tmp_path


def codes(findings: list[ddc.Finding]) -> list[tuple[str, str]]:
    return [(f.code, f.ident) for f in findings]


def test_clean_repository_has_no_findings(repo: Path) -> None:
    assert ddc.check_repo(repo, arc42=True) == []


def test_invalid_block_is_reported(repo: Path) -> None:
    block = dict(BLOCK, goal={"not_applicable": "short"})
    write(repo, ".agentic/repo.yaml", yaml.safe_dump({"durable_documents": block}))
    assert ("BLOCK-INVALID", "-") in codes(ddc.check_repo(repo, arc42=False))


def test_missing_block_is_invalid_input(repo: Path) -> None:
    write(repo, ".agentic/repo.yaml", "other: 1\n")
    assert ddc.main(["--repo", str(repo)]) == 2


def test_goal_placeholder_thesis(repo: Path) -> None:
    write(repo, "docs/architecture/GOAL.md", GOAL.replace(
        "Declaring document updates at adoption and checking them at completion keeps documents current.", "TODO"))
    assert ("GOAL-FIELD", "Thesis") in codes(ddc.check_repo(repo, arc42=False))


def test_requirement_without_disproof(repo: Path) -> None:
    write(repo, "docs/architecture/REQUIREMENTS.md", REQS.replace("Disproof: an overdue member completes a checkout.\n", ""))
    assert ("REQ-NO-DISPROOF", "REQ-12") in codes(ddc.check_repo(repo, arc42=False))


def test_owner_path_missing(repo: Path) -> None:
    trace = yaml.safe_load(yaml.safe_dump(TRACE))
    trace["rules"][0]["owner"] = "src/gone.py"
    write(repo, "docs/model/trace.yaml", yaml.safe_dump(trace))
    assert ("RULE-OWNER-MISSING", "RULE-LOAN-OVERDUE") in codes(ddc.check_repo(repo, arc42=False))


def test_two_owners_refused(repo: Path) -> None:
    trace = yaml.safe_load(yaml.safe_dump(TRACE))
    trace["rules"][0]["owner"] = ["src/loans.py", "src/other.py"]
    write(repo, "docs/model/trace.yaml", yaml.safe_dump(trace))
    assert ("RULE-OWNER", "RULE-LOAN-OVERDUE") in codes(ddc.check_repo(repo, arc42=False))


def test_check_path_missing(repo: Path) -> None:
    trace = yaml.safe_load(yaml.safe_dump(TRACE))
    trace["rules"][0]["checks"] = ["tests/test_gone.py::test_x"]
    write(repo, "docs/model/trace.yaml", yaml.safe_dump(trace))
    assert ("RULE-CHECK-MISSING", "RULE-LOAN-OVERDUE") in codes(ddc.check_repo(repo, arc42=False))


def test_rule_without_check(repo: Path) -> None:
    trace = yaml.safe_load(yaml.safe_dump(TRACE))
    trace["rules"][0]["checks"] = []
    write(repo, "docs/model/trace.yaml", yaml.safe_dump(trace))
    assert ("RULE-NO-CHECK", "RULE-LOAN-OVERDUE") in codes(ddc.check_repo(repo, arc42=False))


def test_process_enforcing_unknown_rule(repo: Path) -> None:
    trace = yaml.safe_load(yaml.safe_dump(TRACE))
    trace["processes"][0]["enforces"] = ["RULE-NOPE"]
    write(repo, "docs/model/trace.yaml", yaml.safe_dump(trace))
    assert ("PROC-UNKNOWN-RULE", "PROC-CHECKOUT") in codes(ddc.check_repo(repo, arc42=False))


def test_unresolvable_decision_link(repo: Path) -> None:
    write(repo, "docs/decisions/0031-fourteen-days.md", ADR.replace("Governs: RULE-LOAN-OVERDUE", "Governs: RULE-DOES-NOT-EXIST"))
    assert ("DECISION-UNRESOLVED", "0031-fourteen-days") in codes(ddc.check_repo(repo, arc42=False))


def test_decision_without_governs(repo: Path) -> None:
    write(repo, "docs/decisions/0031-fourteen-days.md", ADR.replace("Governs: RULE-LOAN-OVERDUE\n", ""))
    assert ("DECISION-NO-GOVERNS", "0031-fourteen-days") in codes(ddc.check_repo(repo, arc42=False))


def test_stale_rule_after_owner_change(repo: Path) -> None:
    write(repo, "src/loans.py", "def checkout():\n    return 'changed'\n")
    commit(repo, "change owner only")
    assert ("STALE", "RULE-LOAN-OVERDUE") in codes(ddc.check_repo(repo, arc42=False))


def test_reviewed_at_clears_staleness(repo: Path) -> None:
    write(repo, "src/loans.py", "def checkout():\n    return 'changed'\n")
    head = commit(repo, "change owner")
    trace = yaml.safe_load(yaml.safe_dump(TRACE))
    trace["rules"][0]["reviewed_at"] = head
    write(repo, "docs/model/trace.yaml", yaml.safe_dump(trace))
    commit(repo, "review rule")
    assert ("STALE", "RULE-LOAN-OVERDUE") not in codes(ddc.check_repo(repo, arc42=False))


def test_parallel_requirements_document(repo: Path) -> None:
    write(repo, "notes/PRD.md", "# old prd\n")
    commit(repo, "parallel prd")
    assert ("PARALLEL", "-") in codes(ddc.check_repo(repo, arc42=False))


def test_arc42_missing_heading(repo: Path) -> None:
    write(repo, "docs/architecture/GOAL.md", GOAL.replace("### Quality Goals", "### Qualities"))
    assert ("ARC42-HEADING", "Quality Goals") in codes(ddc.check_repo(repo, arc42=True))


def test_arc42_wrong_number(repo: Path) -> None:
    write(repo, "docs/architecture/GOAL.md", GOAL.replace("## Introduction and Goals", "## 2. Introduction and Goals"))
    assert ("ARC42-NUMBER", "Introduction and Goals") in codes(ddc.check_repo(repo, arc42=True))


def test_arc42_unlabelled_extension(repo: Path) -> None:
    write(repo, "docs/architecture/GOAL.md", GOAL.replace("## Thesis (AES extension)", "## Thesis"))
    assert ("ARC42-EXTENSION-LABEL", "Thesis") in codes(ddc.check_repo(repo, arc42=True))


# Completion check (R8): negative control B and its fixed re-run.

def plan_text(line: str) -> str:
    return f"# Plan x\n\n{line}\n"


def test_plan_without_declaration_refused(repo: Path) -> None:
    write(repo, "docs/plans/x.md", plan_text("No declaration here."))
    base = commit(repo, "plan")
    assert ("PLAN-NO-DECLARATION", "-") in codes(ddc.check_plan(repo, repo / "docs/plans/x.md", f"{base}~1..{base}"))


def test_plan_declared_document_unchanged_refused(repo: Path) -> None:
    base = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    write(repo, "docs/plans/x.md", plan_text("Durable documents: system_model#RULE-LOAN-OVERDUE, decisions"))
    write(repo, "src/loans.py", "def checkout():\n    return 'new'\n")
    head = commit(repo, "work without doc update")
    found = codes(ddc.check_plan(repo, repo / "docs/plans/x.md", f"{base}..{head}"))
    assert ("PLAN-UNCHANGED", "RULE-LOAN-OVERDUE") in found
    assert ("PLAN-UNCHANGED", "-") in found


def test_plan_declared_document_changed_passes(repo: Path) -> None:
    base = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    write(repo, "docs/plans/x.md", plan_text("Durable documents: system_model#RULE-LOAN-OVERDUE, decisions"))
    trace = yaml.safe_load(yaml.safe_dump(TRACE))
    trace["rules"][0]["statement"] = "no borrowing while any loan is overdue"
    write(repo, "docs/model/trace.yaml", yaml.safe_dump(trace))
    write(repo, "docs/decisions/0032-any-loan.md", "# 0032 Any overdue loan blocks\n\nGoverns: RULE-LOAN-OVERDUE\n")
    head = commit(repo, "work with doc update")
    assert ddc.check_plan(repo, repo / "docs/plans/x.md", f"{base}..{head}") == []


def test_plan_unknown_id_refused(repo: Path) -> None:
    base = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    write(repo, "docs/plans/x.md", plan_text("Durable documents: system_model#RULE-NOPE"))
    write(repo, "docs/model/ODD.md", "# System model\n\nchanged\n")
    head = commit(repo, "w")
    assert ("PLAN-UNKNOWN-ID", "RULE-NOPE") in codes(ddc.check_plan(repo, repo / "docs/plans/x.md", f"{base}..{head}"))


def test_plan_none_needs_reason(repo: Path) -> None:
    write(repo, "docs/plans/x.md", plan_text("Durable documents: none"))
    head = commit(repo, "p")
    assert ("PLAN-NONE-NO-REASON", "-") in codes(ddc.check_plan(repo, repo / "docs/plans/x.md", f"{head}~1..{head}"))


def test_plan_none_with_reason_passes(repo: Path) -> None:
    write(repo, "docs/plans/x.md", plan_text("Durable documents: none -- typo fix in a log message changes no rule"))
    head = commit(repo, "p")
    assert ddc.check_plan(repo, repo / "docs/plans/x.md", f"{head}~1..{head}") == []


def test_cli_exit_codes_and_summary(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert ddc.main(["--repo", str(repo), "--arc42"]) == 0
    out = capsys.readouterr().out
    assert "findings=0 (none), exit 0" in out
    write(repo, "docs/decisions/0031-fourteen-days.md", ADR.replace("Governs: RULE-LOAN-OVERDUE\n", ""))
    assert ddc.main(["--repo", str(repo)]) == 1
    out = capsys.readouterr().out
    assert "FINDING DECISION-NO-GOVERNS role=decisions id=0031-fourteen-days" in out
    assert "exit 1" in out
