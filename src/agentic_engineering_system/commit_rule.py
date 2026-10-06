"""`aes commit check` / `aes commit replay`: the commit-tag rule (`RU-AES-COMMIT-RULE`, AP-REQ-001).

Real implementation work lands only under a plan Company Planning adopted; trivial
work still lands, decided by measured facts about the change, never by the tag
text alone. The first line of every commit message carries one tag:

- ``[Plan #N]`` / ``[Goal <id>]``: the named plan (``docs/plans/<N>_*.md``, or a
  Markdown plan whose front matter says ``plan_id: <id>``, in this repository or a
  configured plan root) declares ``method_conformance_receipt``; the adoption
  decision beside that receipt says ``adopted`` and its ``plan_sha256`` and
  ``receipt_sha256`` match the current bytes of the plan and the receipt.
- ``[Trivial]``: the change touches at most ``trivial_max_files`` files and
  ``trivial_max_lines`` added+deleted lines, adds no file under a governed root,
  and touches no running-thing file (Dockerfile, compose file, systemd unit,
  hook, deploy script, CI workflow, agent instructions).
- ``[Unplanned]``: an emergency; the message needs an ``Emergency: <reason>`` line.
- ``[Shaping <id>]``: drafting a plan; every changed file is under ``proposals/<id>/``.

Git's own merge, fixup, squash and amend messages are accepted. Paths and tags
are matched with regular expressions (identifiers, not prose); nothing judges
what a message means.

``.aes/commit_rule.yaml`` sets ``mode`` (``observe``: log every verdict, refuse
nothing, the default; ``enforce``: refuse), the trivial limits and extra
``plan_roots``. Every verdict appends one JSON line to
``<git-common-dir>/aes/commit-rule-<UTC date>.jsonl``.
"""

from __future__ import annotations

import datetime as dt
import fnmatch
import hashlib
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ruamel.yaml import YAML

from .records import load_project

_YAML = YAML(typ="safe")

CONFIG_PATH = Path(".aes") / "commit_rule.yaml"
TAG_RE = re.compile(
    r"^\[(?:Plan #(?P<plan>\d+)|Goal (?P<goal>[a-z0-9][a-z0-9._:-]*)|(?P<trivial>Trivial)"
    r"|(?P<unplanned>Unplanned)|Shaping (?P<shaping>[a-z0-9][a-z0-9._-]*))\]"
)
GIT_OWN_PREFIXES = ("Merge ", "fixup! ", "squash! ", "amend! ")
EMERGENCY_RE = re.compile(r"^Emergency:\s*\S", re.MULTILINE)
RUNNING_THING_NAMES = (
    "Dockerfile", "Dockerfile.*", "*.dockerfile", "compose.yaml", "compose.yml",
    "docker-compose*.yaml", "docker-compose*.yml", "*.service", "*.timer", "*.socket",
    "deploy.sh", "deploy-*.sh", "deploy_*.sh", "AGENTS.md", "CLAUDE.md", "*.AGENTS.md",
)
RUNNING_THING_DIRS = (".githooks/", "hooks/", ".github/workflows/", ".claude/", ".codex/")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True)
class FileChange:
    path: str
    status: str  # git name-status letter: A, M, D, R, C, T
    added: int
    deleted: int


@dataclass(frozen=True)
class RuleConfig:
    mode: str = "observe"
    trivial_max_files: int = 3
    trivial_max_lines: int = 60
    plan_roots: tuple[Path, ...] = ()


@dataclass
class Verdict:
    verdict: str  # accept | refuse
    tag: str
    reasons: list[str] = field(default_factory=list)
    files: int = 0
    lines: int = 0
    running_things: list[str] = field(default_factory=list)


def _git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {root}: {done.stderr.strip()}")
    return done.stdout


def load_rule_config(root: Path) -> RuleConfig:
    path = root / CONFIG_PATH
    if not path.is_file():
        return RuleConfig(plan_roots=(root,))
    data = _YAML.load(path.read_text(encoding="utf-8")) or {}
    mode = data.get("mode", "observe")
    if mode not in ("observe", "enforce"):
        raise ValueError(f"{path}: mode must be observe or enforce, not {mode!r}")
    extra = tuple((root / p).resolve() if not Path(p).is_absolute() else Path(p)
                  for p in data.get("plan_roots", []))
    return RuleConfig(
        mode=mode,
        trivial_max_files=int(data.get("trivial_max_files", 3)),
        trivial_max_lines=int(data.get("trivial_max_lines", 60)),
        plan_roots=(root, *extra),
    )


def _parse_changes(numstat: str, name_status: str) -> list[FileChange]:
    statuses: dict[str, str] = {}
    for line in name_status.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            statuses[parts[-1]] = parts[0][:1]
    changes = []
    for line in numstat.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added, deleted, path = parts[0], parts[1], parts[-1]
        if " => " in path:  # rename in numstat brace form; name-status holds the new path
            path = next((p for p in statuses if path.endswith(p.rsplit("/", 1)[-1])), path)
        changes.append(FileChange(path=path, status=statuses.get(path, "M"),
                                  added=int(added) if added.isdigit() else 0,
                                  deleted=int(deleted) if deleted.isdigit() else 0))
    return changes


def staged_changes(root: Path) -> list[FileChange]:
    return _parse_changes(_git(root, "diff", "--cached", "--numstat", "--no-renames"),
                          _git(root, "diff", "--cached", "--name-status", "--no-renames"))


def commit_changes(root: Path, rev: str) -> list[FileChange]:
    return _parse_changes(
        _git(root, "show", "--numstat", "--format=", "--no-renames", "--first-parent", "-m", rev),
        _git(root, "show", "--name-status", "--format=", "--no-renames", "--first-parent", "-m", rev),
    )


def running_thing(path: str) -> bool:
    name = path.rsplit("/", 1)[-1]
    if any(fnmatch.fnmatch(name, pattern) for pattern in RUNNING_THING_NAMES):
        return True
    return any(path.startswith(d) or f"/{d}" in f"/{path}" for d in RUNNING_THING_DIRS)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _plan_candidates(plan_root: Path, number: str | None, plan_id: str | None) -> list[Path]:
    if number is not None:
        return [p for p in sorted((plan_root / "docs" / "plans").glob("*.md"))
                if re.match(rf"0*{int(number)}_", p.name)]
    found = []
    for p in sorted(plan_root.glob("proposals/*/*.md")) + sorted(plan_root.glob("docs/plans/*.md")):
        match = FRONT_MATTER_RE.match(p.read_text(encoding="utf-8", errors="replace"))
        if match and (_YAML.load(match.group(1)) or {}).get("plan_id") == plan_id:
            found.append(p)
    return found


def plan_adoption(plan_root: Path, plan: Path) -> tuple[bool, str]:
    """Whether `plan` declares a Company Planning receipt whose adoption decision is `adopted`
    for the current bytes of both the plan and the receipt; the reason either way."""
    if not plan.is_file():
        return False, f"{plan}: plan file not found"
    match = FRONT_MATTER_RE.match(plan.read_text(encoding="utf-8", errors="replace"))
    meta = (_YAML.load(match.group(1)) or {}) if match else {}
    receipt_ref = meta.get("method_conformance_receipt")
    if not receipt_ref:
        return False, f"{plan}: no method_conformance_receipt in front matter (not adopted through Company Planning)"
    receipt = plan_root / receipt_ref
    decision = receipt.with_name(receipt.name.removesuffix(".json") + ".adoption-decision.json")
    if not (receipt.is_file() and decision.is_file()):
        return False, f"{plan}: receipt or adoption decision missing ({receipt_ref})"
    record = json.loads(decision.read_text(encoding="utf-8"))
    if record.get("decision") != "adopted":
        return False, f"{plan}: adoption decision is {record.get('decision')!r}, not adopted"
    if record.get("plan_sha256") != _sha256(plan):
        return False, f"{plan}: plan changed since adoption; re-adopt it"
    if record.get("receipt_sha256") != _sha256(receipt):
        return False, f"{plan}: receipt changed since adoption"
    return True, f"{plan.relative_to(plan_root) if plan.is_relative_to(plan_root) else plan} adopted"


def receipt_status(plan_roots: tuple[Path, ...], number: str | None, plan_id: str | None) -> tuple[bool, str]:
    """Whether the named plan has a current adopted Company Planning receipt, and why not."""
    label = f"#{number}" if number is not None else plan_id
    plans = [(r, p) for r in plan_roots for p in _plan_candidates(r, number, plan_id)]
    if not plans:
        return False, f"no plan {label} found under {', '.join(str(r) for r in plan_roots)}"
    reasons = []
    for plan_root, plan in plans:
        ok, why = plan_adoption(plan_root, plan)
        if ok:
            return True, f"plan {label} adopted ({plan.relative_to(plan_root)})"
        reasons.append(why)
    return False, "; ".join(reasons)


def judge(message: str, changes: list[FileChange], governed_roots: list[str], config: RuleConfig) -> Verdict:
    first = message.lstrip().splitlines()[0] if message.strip() else ""
    files = len(changes)
    lines = sum(c.added + c.deleted for c in changes)
    running = sorted(c.path for c in changes if running_thing(c.path))

    def verdict(result: str, tag: str, reason: str) -> Verdict:
        return Verdict(result, tag, [reason], files, lines, running)

    if first.startswith(GIT_OWN_PREFIXES):
        return verdict("accept", "git", "git's own merge/fixup/squash message")
    match = TAG_RE.match(first)
    if not match:
        return verdict("refuse", "none",
                       "no tag: start the first line with [Plan #N], [Goal <id>], [Trivial], [Unplanned] or [Shaping <id>]")
    if match["plan"] is not None or match["goal"] is not None:
        tag = f"Plan #{match['plan']}" if match["plan"] is not None else f"Goal {match['goal']}"
        ok, why = receipt_status(config.plan_roots, match["plan"], match["goal"])
        return verdict("accept" if ok else "refuse", tag, why)
    if match["trivial"]:
        problems = []
        if files > config.trivial_max_files:
            problems.append(f"{files} files (trivial allows {config.trivial_max_files})")
        if lines > config.trivial_max_lines:
            problems.append(f"{lines} changed lines (trivial allows {config.trivial_max_lines})")
        added_governed = sorted(c.path for c in changes if c.status == "A"
                                and any(c.path.startswith(r) for r in governed_roots))
        if added_governed:
            problems.append(f"adds file(s) under a governed root: {', '.join(added_governed)}")
        if running:
            problems.append(f"touches running-thing file(s): {', '.join(running)}")
        if problems:
            return verdict("refuse", "Trivial", "not trivial: " + "; ".join(problems) + "; plan it ([Plan #N] or [Goal <id>])")
        return verdict("accept", "Trivial", f"trivial: {files} file(s), {lines} line(s), no running-thing file")
    if match["unplanned"]:
        if EMERGENCY_RE.search(message):
            return verdict("accept", "Unplanned", "emergency recorded (Emergency: line present); logged for review")
        why = "[Unplanned] is for emergencies: add an 'Emergency: <reason>' line"
        if running:
            why += f"; this change touches running-thing file(s) {', '.join(running)} and needs a plan ([Plan #N] or [Goal <id>])"
        return verdict("refuse", "Unplanned", why)
    plan_id = match["shaping"]
    outside = sorted(c.path for c in changes if not c.path.startswith(f"proposals/{plan_id}/"))
    if outside:
        return verdict("refuse", f"Shaping {plan_id}", f"[Shaping {plan_id}] may touch only proposals/{plan_id}/; also touches {', '.join(outside)}")
    return verdict("accept", f"Shaping {plan_id}", f"drafting plan {plan_id} inside proposals/{plan_id}/")


def _governed_roots(root: Path) -> list[str]:
    try:
        return list(load_project(root / ".aes" / "project.yaml").governed_roots)
    except (OSError, ValueError):
        return []


def _log(root: Path, entry: dict) -> Path:
    common = Path(_git(root, "rev-parse", "--git-common-dir").strip())
    log_dir = (common if common.is_absolute() else root / common) / "aes"
    log_dir.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    path = log_dir / f"commit-rule-{now.date().isoformat()}.jsonl"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"at": now.isoformat(timespec="seconds"), **entry}) + "\n")
    return path


def check_message(root: Path, message_file: Path) -> tuple[int, str]:
    """Judge the commit being made; return (exit status, report). Observe mode never refuses."""
    root = root.resolve()
    config = load_rule_config(root)
    message = "\n".join(l for l in message_file.read_text(encoding="utf-8").splitlines() if not l.startswith("#"))
    verdict = judge(message, staged_changes(root), _governed_roots(root), config)
    log = _log(root, {"mode": config.mode, "subject": message.strip().splitlines()[0] if message.strip() else "",
                      **asdict(verdict)})
    word = verdict.verdict if config.mode == "enforce" or verdict.verdict == "accept" else "would refuse (observe mode)"
    report = f"aes commit rule: {word} [{verdict.tag}] — {'; '.join(verdict.reasons)} (logged to {log})"
    blocked = config.mode == "enforce" and verdict.verdict == "refuse"
    return (1 if blocked else 0), report


def replay(root: Path, revisions: str = "HEAD", max_count: int = 300) -> tuple[list[tuple[str, str, Verdict]], dict[str, int]]:
    """Judge past commits (non-merge, first-parent order) with today's rule and today's receipts."""
    root = root.resolve()
    config = load_rule_config(root)
    governed = _governed_roots(root)
    out = _git(root, "log", "--no-merges", f"--max-count={max_count}", "--format=%H%x00%B%x01", revisions)
    rows = []
    for record in out.split("\x01"):
        if "\x00" not in record:
            continue
        sha, body = record.strip("\n").split("\x00", 1)
        verdict = judge(body, commit_changes(root, sha), governed, config)
        rows.append((sha, body.strip().splitlines()[0] if body.strip() else "", verdict))
    counts: dict[str, int] = {"commits": len(rows), "accept": 0, "refuse": 0}
    for _, _, v in rows:
        counts[v.verdict] += 1
        counts[f"tag:{v.tag.split(' ')[0]}"] = counts.get(f"tag:{v.tag.split(' ')[0]}", 0) + 1
    return rows, counts
