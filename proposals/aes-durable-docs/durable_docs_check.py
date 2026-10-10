#!/usr/bin/env python3
"""Check a repository's durable documents (plan aes-durable-docs, R1-R5, R8, R9, R11).

Modes:
  durable_docs_check.py --repo R              whole-repository check (R1-R5, R9, R11, parallel check)
  durable_docs_check.py --repo R --plan P --range BASE..HEAD
                                              completion check for one plan (R8)

Output: one ``FINDING <code> role=<role> id=<id> file=<file>: <message>`` line per
finding, then a summary line with the count per code and the exit status.
Exit codes: 0 clean, 1 findings, 2 invalid input (no block, unreadable file).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import jsonschema
import yaml

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE / "durable_documents.schema.json").read_text(encoding="utf-8"))

# Placeholder text that does not count as filling a field.
PLACEHOLDER = re.compile(r"^\s*(TODO|TBD|FIXME|\.\.\.|-)?\s*$", re.IGNORECASE)
GOAL_FIELDS = ("North star", "Thesis", "Thesis disproof", "Non-goals")
ARC42_GOAL_HEADING = "Introduction and Goals"
ARC42_GOAL_SUBHEADINGS = ("Requirements Overview", "Quality Goals", "Stakeholders")
ARC42_NUMBERS = {
    "Introduction and Goals": "1",
    "Architecture Constraints": "2",
    "Context and Scope": "3",
    "Solution Strategy": "4",
    "Building Block View": "5",
    "Runtime View": "6",
    "Deployment View": "7",
    "Cross-cutting Concepts": "8",
    "Architecture Decisions": "9",
    "Quality Requirements": "10",
    "Risks and Technical Debts": "11",
    "Glossary": "12",
}
EXTENSION_KEYS = ("Thesis", "Thesis disproof", "North star")
ID_RE = re.compile(r"\b(?:RULE|PROC|ENT|REC|VIEW|REQ)-[A-Z0-9][A-Z0-9-]*\b")
GOVERNS_RE = re.compile(r"^\s*(?:\*\*)?governs(?:\*\*)?\s*:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
DURABLE_LINE_RE = re.compile(r"^\s*(?:\*\*)?Durable documents(?:\*\*)?\s*:\s*(.+)$", re.IGNORECASE | re.MULTILINE)


@dataclass(frozen=True)
class Finding:
    code: str
    role: str
    ident: str
    file: str
    message: str

    def line(self) -> str:
        return f"FINDING {self.code} role={self.role} id={self.ident} file={self.file}: {self.message}"


class InvalidInput(Exception):
    pass


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise InvalidInput(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def load_block(repo: Path) -> dict:
    path = repo / ".agentic" / "repo.yaml"
    if not path.is_file():
        raise InvalidInput(f"{path} not found")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    block = data.get("durable_documents")
    if block is None:
        raise InvalidInput(".agentic/repo.yaml has no durable_documents block")
    return block


def role_path(block: dict, role: str) -> str | None:
    value = block.get(role)
    if isinstance(value, str):
        return value
    return None


def is_na(value: object) -> bool:
    return isinstance(value, dict) and "not_applicable" in value


def check_block(block: dict) -> list[Finding]:
    validator = jsonschema.Draft202012Validator(SCHEMA)
    findings = []
    for error in sorted(validator.iter_errors(block), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "(block)"
        findings.append(Finding("BLOCK-INVALID", where, "-", ".agentic/repo.yaml", error.message))
    return findings


def field_value(text: str, name: str) -> str | None:
    """Return the text after '<name>:' or under a heading named <name> (extension label allowed)."""
    label = re.escape(name) + r"(?:\s*\(AES extension\))?"
    inline = re.search(rf"^\s*(?:[-*]\s*)?(?:\*\*)?{label}(?:\*\*)?\s*:\s*(.*)$", text, re.MULTILINE | re.IGNORECASE)
    if inline and inline.group(1).strip():
        return inline.group(1).strip()
    heading = re.search(rf"^#+\s*{label}\s*$\n+(.+?)(?=^#|\Z)", text, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    if heading:
        return heading.group(1).strip()
    return None


def check_goal(repo: Path, rel: str, arc42: bool) -> list[Finding]:
    path = repo / rel
    if not path.is_file():
        return [Finding("MISSING-DOC", "goal", "-", rel, "declared goal document does not exist")]
    text = path.read_text(encoding="utf-8")
    findings = []
    for name in GOAL_FIELDS:
        value = field_value(text, name)
        if value is None or PLACEHOLDER.match(value):
            findings.append(Finding("GOAL-FIELD", "goal", name, rel, f"'{name}' is missing or placeholder"))
    if arc42:
        findings.extend(check_arc42_goal(text, rel))
    return findings


def headings(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^#+\s+(.+?)\s*$", text, re.MULTILINE)]


def check_arc42_goal(text: str, rel: str) -> list[Finding]:
    findings = []
    hs = headings(text)
    bare = [re.sub(r"^\d+(\.\d+)*\.?\s+", "", h) for h in hs]
    if ARC42_GOAL_HEADING not in bare:
        findings.append(Finding("ARC42-HEADING", "goal", ARC42_GOAL_HEADING, rel, "arc42 heading 'Introduction and Goals' missing"))
    for sub in ARC42_GOAL_SUBHEADINGS:
        if sub not in bare:
            findings.append(Finding("ARC42-HEADING", "goal", sub, rel, f"arc42 sub-heading '{sub}' missing (use not_applicable: <reason> under it if it does not apply)"))
    for h in hs:
        m = re.match(r"^(\d+)\.?\s+(.+)$", h)
        if m and m.group(2) in ARC42_NUMBERS and ARC42_NUMBERS[m.group(2)] != m.group(1):
            findings.append(Finding("ARC42-NUMBER", "goal", m.group(2), rel, f"numbered {m.group(1)}, arc42 numbers it {ARC42_NUMBERS[m.group(2)]}"))
    for key in EXTENSION_KEYS:
        for line in text.splitlines():
            if re.match(rf"^\s*(#+\s*|[-*]\s*)?(\*\*)?{re.escape(key)}(\*\*)?\s*(:|$)", line, re.IGNORECASE) and "(AES extension)" not in line:
                findings.append(Finding("ARC42-EXTENSION-LABEL", "goal", key, rel, f"'{key}' is an AES extension and must be labelled '(AES extension)'"))
                break
    return findings


def check_requirements(repo: Path, rel: str) -> list[Finding]:
    path = repo / rel
    if not path.is_file():
        return [Finding("MISSING-DOC", "requirements", "-", rel, "declared requirements document does not exist")]
    findings = []
    if path.suffix in (".yaml", ".yml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        criteria = data.get("success_criteria") or []
        if not criteria:
            findings.append(Finding("REQ-NO-CRITERIA", "requirements", "-", rel, "no success_criteria"))
        for c in criteria:
            if not str(c.get("disproof") or "").strip():
                findings.append(Finding("REQ-NO-DISPROOF", "requirements", str(c.get("id")), rel, "success criterion has no disproof"))
        return findings
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"^(?=#+\s+REQ-)", text, flags=re.MULTILINE)
    reqs = [b for b in blocks if re.match(r"^#+\s+REQ-", b)]
    if not reqs:
        findings.append(Finding("REQ-NONE", "requirements", "-", rel, "no '## REQ-<id>' headings"))
    for block in reqs:
        ident = ID_RE.search(block.splitlines()[0])
        rid = ident.group(0) if ident else block.splitlines()[0].strip("# ")
        for name, code in (("Success", "REQ-NO-SUCCESS"), ("Disproof", "REQ-NO-DISPROOF")):
            value = field_value(block, name)
            if value is None or PLACEHOLDER.match(value):
                findings.append(Finding(code, "requirements", rid, rel, f"requirement has no '{name}:' line"))
    return findings


def load_trace(repo: Path, rel: str) -> tuple[dict, list[Finding]]:
    path = repo / rel
    if not path.is_file():
        return {}, [Finding("MISSING-DOC", "system_model", "-", rel, "declared trace file does not exist")]
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data, []


def trace_ids(trace: dict) -> set[str]:
    ids = set()
    for kind in ("entities", "processes", "records", "views", "rules"):
        for item in trace.get(kind) or []:
            if item.get("id"):
                ids.add(item["id"])
    return ids


def check_system_model(repo: Path, model: dict) -> tuple[list[Finding], dict]:
    findings = []
    prose = model["prose"]
    if not (repo / prose).is_file():
        findings.append(Finding("MISSING-DOC", "system_model", "-", prose, "declared system-model prose does not exist"))
    trace, missing = load_trace(repo, model["trace"])
    findings.extend(missing)
    if missing:
        return findings, trace
    rel = model["trace"]
    rules = trace.get("rules") or []
    if not rules:
        findings.append(Finding("TRACE-NO-RULES", "system_model", "-", rel, "trace declares no rules"))
    seen: Counter[str] = Counter()
    for kind in ("entities", "processes", "records", "views", "rules"):
        for item in trace.get(kind) or []:
            ident = item.get("id")
            if not ident:
                findings.append(Finding("TRACE-NO-ID", "system_model", "-", rel, f"a {kind[:-1]} has no id"))
                continue
            seen[ident] += 1
    for ident, n in seen.items():
        if n > 1:
            findings.append(Finding("TRACE-DUPLICATE-ID", "system_model", ident, rel, f"id declared {n} times"))
    for rule in rules:
        rid = rule.get("id", "-")
        owner = rule.get("owner")
        if not owner or isinstance(owner, list):
            findings.append(Finding("RULE-OWNER", "system_model", rid, rel, "rule must name exactly one owner path"))
        elif not (repo / owner).exists():
            findings.append(Finding("RULE-OWNER-MISSING", "system_model", rid, owner, "owner path does not exist"))
        checks = rule.get("checks") or []
        if not checks:
            findings.append(Finding("RULE-NO-CHECK", "system_model", rid, rel, "rule names no check"))
        for c in checks:
            if not (repo / str(c).split("::")[0]).exists():
                findings.append(Finding("RULE-CHECK-MISSING", "system_model", rid, str(c), "check path does not exist"))
        for d in rule.get("decisions") or []:
            if not (repo / d).is_file():
                findings.append(Finding("RULE-DECISION-MISSING", "system_model", rid, d, "decision record does not exist"))
    rule_ids = {r.get("id") for r in rules}
    for proc in trace.get("processes") or []:
        enforces = proc.get("enforces")
        if enforces is None:
            findings.append(Finding("PROC-NO-RULES", "system_model", proc.get("id", "-"), rel, "process does not name the rules it enforces (use [] if none)"))
            continue
        for rid in enforces:
            if rid not in rule_ids:
                findings.append(Finding("PROC-UNKNOWN-RULE", "system_model", proc.get("id", "-"), rel, f"enforces unknown rule {rid}"))
    return findings, trace


def check_decisions(repo: Path, rel: str, known_ids: set[str], component_paths: set[str]) -> list[Finding]:
    root = repo / rel
    if not root.is_dir():
        return [Finding("MISSING-DOC", "decisions", "-", rel, "declared decisions directory does not exist")]
    findings = []
    for path in sorted(root.glob("*.md")):
        if path.name.lower() in ("readme.md", "index.md"):
            continue
        text = path.read_text(encoding="utf-8")
        relp = str(path.relative_to(repo))
        m = GOVERNS_RE.search(text)
        if not m:
            findings.append(Finding("DECISION-NO-GOVERNS", "decisions", path.stem, relp, "decision record has no 'Governs:' line naming rule or component IDs"))
            continue
        targets = [t.strip().strip("`") for t in m.group(1).split(",") if t.strip()]
        for t in targets:
            if t not in known_ids and t not in component_paths and not (repo / t).exists():
                findings.append(Finding("DECISION-UNRESOLVED", "decisions", path.stem, relp, f"'Governs:' target {t} resolves to no trace id or path"))
    return findings


def last_commit(repo: Path, rel: str) -> str | None:
    out = git(repo, "log", "-1", "--format=%H", "--", rel).strip()
    return out or None


def check_staleness(repo: Path, model: dict, trace: dict) -> list[Finding]:
    findings = []
    trace_rel = model["trace"]
    base_default = last_commit(repo, trace_rel)
    for rule in trace.get("rules") or []:
        owner = rule.get("owner")
        if not isinstance(owner, str) or not (repo / owner).exists():
            continue
        base = rule.get("reviewed_at") or base_default
        if not base:
            continue
        changed = git(repo, "log", "--format=%h", f"{base}..HEAD", "--", owner).split()
        if changed:
            findings.append(Finding("STALE", "system_model", rule.get("id", "-"), owner,
                                    f"owner changed in {len(changed)} commit(s) after the rule was last reviewed ({base[:9]}); re-read the rule and set reviewed_at"))
    return findings


def check_parallel(repo: Path, block: dict) -> list[Finding]:
    findings = []
    tracked = git(repo, "ls-files").splitlines()
    req = role_path(block, "requirements")
    if req:
        for f in tracked:
            name = f.rsplit("/", 1)[-1]
            if name in ("REQUIREMENTS.md", "PRD.md") and f != req:
                findings.append(Finding("PARALLEL", "requirements", "-", f, f"second requirements document beside declared {req}"))
    model = block.get("system_model")
    if isinstance(model, dict) and "prose" in model:
        for f in tracked:
            if f.endswith("/ODD.md") or f == "ODD.md":
                if f != model["prose"]:
                    findings.append(Finding("PARALLEL", "system_model", "-", f, f"second system model beside declared {model['prose']}"))
    goal = role_path(block, "goal")
    if goal:
        for f in tracked:
            if f.rsplit("/", 1)[-1] == "GOAL.md" and f != goal:
                findings.append(Finding("PARALLEL", "goal", "-", f, f"second goal document beside declared {goal}"))
    return findings


def check_repo(repo: Path, arc42: bool) -> list[Finding]:
    block = load_block(repo)
    findings = check_block(block)
    if findings:
        return findings
    goal = role_path(block, "goal")
    if goal:
        findings += check_goal(repo, goal, arc42)
    req = role_path(block, "requirements")
    if req:
        findings += check_requirements(repo, req)
    trace: dict = {}
    model = block["system_model"]
    if not is_na(model):
        model_findings, trace = check_system_model(repo, model)
        findings += model_findings
        if trace:
            findings += check_staleness(repo, model, trace)
    dec = role_path(block, "decisions")
    if dec:
        components = {r.get("owner") for r in trace.get("rules") or [] if isinstance(r.get("owner"), str)}
        findings += check_decisions(repo, dec, trace_ids(trace), components)
    plans = role_path(block, "plans")
    if plans and not (repo / plans).is_dir():
        findings.append(Finding("MISSING-DOC", "plans", "-", plans, "declared plans directory does not exist"))
    findings += check_parallel(repo, block)
    return findings


def parse_plan_line(text: str) -> tuple[list[str], str | None] | None:
    m = DURABLE_LINE_RE.search(text)
    if not m:
        return None
    value = m.group(1).strip()
    none = re.match(r"^none\s*(?:--|—|:)\s*(.*)$", value, re.IGNORECASE)
    if none:
        return [], none.group(1).strip()
    if value.lower() == "none":
        return [], ""
    entries = [e.strip().strip("`") for e in value.split(",") if e.strip()]
    return entries, None


def check_plan(repo: Path, plan: Path, rng: str) -> list[Finding]:
    block = load_block(repo)
    if not plan.is_file():
        raise InvalidInput(f"plan {plan} not found")
    parsed = parse_plan_line(plan.read_text(encoding="utf-8"))
    rel = str(plan.relative_to(repo)) if plan.is_relative_to(repo) else str(plan)
    if parsed is None:
        return [Finding("PLAN-NO-DECLARATION", "plan", "-", rel, "plan has no 'Durable documents:' line")]
    entries, reason = parsed
    if reason is not None:
        if len(reason.split()) < 3:
            return [Finding("PLAN-NONE-NO-REASON", "plan", "-", rel, "'none' needs a reason of at least three words")]
        return []
    changed = set(git(repo, "diff", "--name-only", rng).splitlines())
    findings = []
    model = block.get("system_model")
    for entry in entries:
        role, _, ident = entry.partition("#")
        role = role.strip()
        if role not in block or role == "schema_version":
            findings.append(Finding("PLAN-UNKNOWN-ROLE", role, ident or "-", rel, f"'{role}' is not a declared durable role"))
            continue
        if role == "system_model":
            if is_na(model):
                findings.append(Finding("PLAN-ROLE-NA", role, ident or "-", rel, "role is declared not_applicable"))
                continue
            paths = [model["prose"], model["trace"]]
            if ident:
                trace, _ = load_trace(repo, model["trace"])
                if ident not in trace_ids(trace):
                    findings.append(Finding("PLAN-UNKNOWN-ID", role, ident, model["trace"], "declared id not in the trace at HEAD"))
        else:
            value = block[role]
            if is_na(value):
                findings.append(Finding("PLAN-ROLE-NA", role, ident or "-", rel, "role is declared not_applicable"))
                continue
            paths = [value["generated"]] if isinstance(value, dict) else [value]
        hit = any(c == p or c.startswith(p.rstrip("/") + "/") for p in paths for c in changed)
        if not hit:
            findings.append(Finding("PLAN-UNCHANGED", role, ident or "-", ", ".join(paths), f"declared durable document not changed in {rng}"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--plan", type=Path, help="plan file for the completion check")
    parser.add_argument("--range", dest="rng", help="commit range BASE..HEAD for --plan")
    parser.add_argument("--arc42", action="store_true", help="also check arc42 section rules (R11)")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()
    mode = "plan" if args.plan else "repo"
    try:
        if args.plan:
            if not args.rng:
                raise InvalidInput("--plan needs --range BASE..HEAD")
            plan = args.plan if args.plan.is_absolute() else repo / args.plan
            findings = check_plan(repo, plan.resolve(), args.rng)
        else:
            findings = check_repo(repo, args.arc42)
    except InvalidInput as exc:
        print(f"INVALID: {exc}")
        print(f"durable-docs: mode={mode} repo={repo} invalid input, exit 2")
        return 2
    for f in findings:
        print(f.line())
    counts = Counter(f.code for f in findings)
    summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "none"
    status = 1 if findings else 0
    print(f"durable-docs: mode={mode} repo={repo} findings={len(findings)} ({summary}), exit {status}")
    return status


if __name__ == "__main__":
    sys.exit(main())
