"""Judge a proposed non-code action against the actions Lockstep's side file declares (behavior 5.4).

A Project Brain may propose something other than a pull request: a board update, a comment on a
tracking issue. Acceptance entry A14 asks that such an action name the plan it follows, be carried
out when it matches that plan, and be held when it names none or goes against it. The AES plan has
no place for an action, so actions are declared in Lockstep's side file, `lockstep.yaml`:

    actions:
      - id: ACT-BOARD-STATUS            # what a proposal names as the plan it follows
        kind: board_update              # the kind of action allowed
        target: Inside-Success/Team-Brains#900   # what it may act on, compared exactly
        purpose: post the weekly status line on the tracking issue
        refs: [OUT-001]                 # the plan items it serves

A proposal is a JSON object `{"plan": ..., "kind": ..., "target": ..., "body": ...}`. With a base
revision the side file is read as committed there, never from the working tree, so a change cannot
rewrite the rules it is judged by (issue #67). `python -m lockstep.action_check --proposal FILE` prints the
decision as JSON and exits 0 on allow, 1 on hold, 2 when it could not judge.

[[[cog import lockstep.cogtext as c; c.docstring("src:lockstep:action_check.py", indent=0)]]]
Plan (generated from lockstep.yaml layout and OpenSpec; edit the spec or the layout row, not this text):

Implements: lockstep-plan-format/old-route-checks-stay-while-a-repository-runs-them

### Requirement: Old-route checks stay while a repository runs them

For a repository with `.aes/target.yaml`, Lockstep SHALL keep the checks that plan route uses, each importable as
`lockstep.<name>` and `pcw.<name>`, and runnable as `python -m` under both names where it has a command line:
`action_check`, `behavior_check`, `change_list`, `change_log`, `criterion_checks`, `declared_reason`,
`docstring_up`, `linked_tests`, `plan_edit`, `plan_to_code`, `requirement_status`, `unplanned_symbols`, `wiki` and
`wiki_reach`. One SHALL be retired, with a dated record under
`docs/retired/`, only once no repository in `~/code2` runs it (code2-workspace decision 0009: `.aes/target.yaml`
retires one repository at a time).

Source: Brian, 2026-11-23: "i approve", to Q54 in `docs/planning/open-questions.json` ("write one requirement for
the ones the core calls; retire the rest"); the 2026-11-23 search found all 14 still run, so none retired (inferred by
agent from that search).

#### Scenario: An AES-plan repository's checks still run

- **GIVEN** a repository with `.aes/target.yaml`
- **WHEN** its Makefile or edit hook runs one of the 14 checks
- **THEN** the check runs as before, as each module's own tests show

Tested by: tests/lockstep/test_lockstep_action_check.py
[[[end]]]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from lockstep.aes_bridge import committed_text
from lockstep.side_file import SIDE_FILE

_FIELDS = ("id", "kind", "target", "purpose")


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def declared_actions(root: Path, base: str | None = None) -> dict[str, dict]:
    """Action id -> {kind, target, purpose, refs} from the side file's `actions` section.

    Only well-formed entries count (an id, kind, target and purpose, each non-empty text); the first
    of two entries with one id wins. A project with no side file, or none with an actions section,
    declares no actions, so every proposal is held.
    """
    if base is not None:
        text = committed_text(root, base, SIDE_FILE)
    else:
        path = root / SIDE_FILE
        text = path.read_text(encoding="utf-8") if path.is_file() else None
    data = yaml.safe_load(text) if text else None
    entries = data.get("actions") if isinstance(data, dict) else None
    actions: dict[str, dict] = {}
    for entry in entries if isinstance(entries, list) else []:
        if not isinstance(entry, dict) or not all(_text(entry.get(k)) for k in _FIELDS):
            continue
        refs = entry.get("refs")
        actions.setdefault(_text(entry["id"]), {
            "kind": _text(entry["kind"]), "target": _text(entry["target"]), "purpose": _text(entry["purpose"]),
            "refs": [r for r in refs if _text(r)] if isinstance(refs, list) else []})
    return actions


def action_decision(root: Path, proposal: dict, base: str | None = None) -> dict:
    """Allow a proposal that matches the declared action it names; hold it, with the reason, otherwise."""
    plan, kind, target = (_text(proposal.get(k)) for k in ("plan", "kind", "target"))
    decision = {"plan": plan, "kind": kind, "target": target}

    def held(reason: str) -> dict:
        return {**decision, "decision": "block", "reason": reason, "summary": f"Held: {reason}."}

    if not plan:
        return held("the proposed action names no plan it follows, and every action must name one "
                    f"declared in {SIDE_FILE}")
    actions = declared_actions(root, base)
    action = actions.get(plan)
    if action is None:
        return held(f"the proposed action names {plan}, which is not an action declared in {SIDE_FILE} "
                    f"(declared: {', '.join(sorted(actions)) or 'none'})")
    if kind != action["kind"]:
        return held(f"the proposed action goes against {plan}: the plan allows kind {action['kind']}, "
                    f"and this proposal is kind {kind or '(none)'}")
    if target != action["target"]:
        return held(f"the proposed action goes against {plan}: the plan allows it on {action['target']}, "
                    f"and this proposal acts on {target or 'no target'}")
    return {**decision, "decision": "allow", "purpose": action["purpose"], "refs": action["refs"],
            "reason": f"matches {plan}: a {kind} on {target} ({action['purpose']})",
            "summary": f"Lockstep: the action follows {plan} and matches it ({kind} on {target})."}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=".", help="project root holding lockstep.yaml")
    ap.add_argument("--proposal", required=True, help="the proposal, a JSON file")
    ap.add_argument("--base", help="read the side file as committed at this revision")
    a = ap.parse_args(argv)
    try:
        proposal = json.loads(Path(a.proposal).read_text(encoding="utf-8"))
        if not isinstance(proposal, dict):
            raise ValueError("the proposal must be a JSON object")
        result = action_decision(Path(a.repo), proposal, a.base)
    except (OSError, ValueError, yaml.YAMLError, RuntimeError) as exc:
        print(json.dumps({"decision": "error", "error": f"{type(exc).__name__}: {str(exc)[:300]}"}))
        return 2
    print(json.dumps(result))
    return 0 if result["decision"] == "allow" else 1


if __name__ == "__main__":
    sys.exit(main())
