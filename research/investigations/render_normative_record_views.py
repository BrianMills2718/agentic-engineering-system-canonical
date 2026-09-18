#!/usr/bin/env python3
"""Validate and render conventional views from one structured AES normative projection.

Research-only pilot. Existing Markdown remains normative authority.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load(path: Path) -> dict:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected mapping")
    return value


def clause_body(markdown: str, clause_id: str) -> str:
    match = re.search(rf"^## {re.escape(clause_id)} — .+$", markdown, re.MULTILINE)
    if not match:
        raise ValueError(f"missing clause {clause_id}")
    start = match.end()
    nxt = re.search(r"^## ", markdown[start:], re.MULTILINE)
    end = start + (nxt.start() if nxt else len(markdown[start:]))
    return markdown[start:end].strip().split("\n\n", 1)[0].strip()


def section_body(markdown: str, heading: str, next_heading: str) -> str:
    start_marker = f"## {heading}"
    end_marker = f"## {next_heading}"
    start = markdown.index(start_marker) + len(start_marker)
    end = markdown.index(end_marker, start)
    return markdown[start:end].strip()


def journey_steps(markdown: str) -> list[str]:
    marker = "Directional north-star interaction:"
    start = markdown.index(marker)
    fence = markdown.index("```text", start)
    end = markdown.index("```", fence + 7)
    return [
        line.strip()
        for line in markdown[fence + 7:end].splitlines()
        if line.strip() and line.strip() != "↓"
    ]


def alignment_question(alignment: str, qid: str) -> str:
    marker = f"  - id: {qid}\n"
    start = alignment.index(marker)
    end = alignment.find("\n  - id: AQR-", start + len(marker))
    if end < 0:
        end = alignment.find("\nresearch_basis:", start)
    block = alignment[start:end]
    m = re.search(r"\n    question: >\n([\s\S]*?)(?=\n    status:)", block)
    if not m:
        raise ValueError(f"missing question {qid}")
    return " ".join(line.strip() for line in m.group(1).splitlines() if line.strip())


def validate(record: dict, system: str, plan: str, alignment: str) -> None:
    if record.get("status") != "generated_pilot" or record.get("authority") != "none":
        raise ValueError("pilot projection cannot claim authority")

    seen = set()
    entries = [record["north_star"], *record.get("requirements", []), *record.get("outcomes", [])]
    for item in entries:
        iid = item["id"]
        if iid in seen:
            raise ValueError(f"duplicate normative id: {iid}")
        seen.add(iid)

    if record["north_star"]["verbatim"] != clause_body(system, record["north_star"]["id"]):
        raise ValueError("north_star wording drift")

    for req in record.get("requirements", []):
        if req["verbatim"] != clause_body(system, req["id"]):
            raise ValueError(f"requirement wording drift: {req['id']}")
        if req.get("kind") not in {"behavior", "constraint", "invariant", "quality", "policy"}:
            raise ValueError(f"unsupported requirement kind: {req.get('kind')}")

    expected_outcome = section_body(plan, "User outcome", "Canonical behavioral example")
    if record["outcomes"][0]["verbatim"] != expected_outcome:
        raise ValueError("product outcome wording drift")

    if record["journeys"][0]["steps"] != journey_steps(plan):
        raise ValueError("journey drift")

    for question in record.get("questions", []):
        if question.get("status") == "resolved" and not question.get("decision_ref"):
            raise ValueError(f"resolved AQR lacks decision_ref: {question['id']}")
        if question["question"] != alignment_question(alignment, question["id"]):
            raise ValueError(f"AQR wording drift: {question['id']}")

    forbidden = {"current", "gap", "evidence", "native_contract_definition"}
    if forbidden & set(record):
        raise ValueError("derived/current/native-contract content placed in normative system record")


def render(record: dict) -> str:
    out = [
        "# Generated AES normative view bundle",
        "",
        "> Generated projection. Not normative authority.",
        "",
        "## PRD-style view",
        "",
        "### North star",
        record["north_star"]["verbatim"],
        "",
        "### Product outcome",
        record["outcomes"][0]["verbatim"],
        "",
        "### Actor",
        record["actors"][0]["label"],
        "",
        "## User journey view",
        "",
    ]
    out.extend(f"{i}. {step}" for i, step in enumerate(record["journeys"][0]["steps"], 1))
    out.extend(["", "## Requirements view", ""])
    for req in record["requirements"]:
        out.extend([f"### {req['id']} [{req['kind']}]", req["verbatim"], ""])
    out.extend(["## Architecture/component view", "", "Components:"])
    out.extend(f"- {item}" for item in record.get("component_refs", []))
    out.extend(["", "## AQR view", ""])
    for q in record.get("questions", []):
        out.extend([f"### {q['id']} [{q['status']}]", q["question"], ""])
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--system", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--alignment", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    record = load(args.record)
    validate(
        record,
        args.system.read_text(encoding="utf-8"),
        args.plan.read_text(encoding="utf-8"),
        args.alignment.read_text(encoding="utf-8"),
    )
    rendered = render(record)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(json.dumps({
        "status": "accepted_by_bounded_probe",
        "normative_records": 1 + len(record["requirements"]) + len(record["outcomes"]),
        "journeys": len(record["journeys"]),
        "aqrs": len(record["questions"]),
        "views": ["PRD", "USER_JOURNEY", "REQUIREMENTS", "ARCHITECTURE_COMPONENT", "AQR"],
        "output_bytes": len(rendered.encode("utf-8")),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
