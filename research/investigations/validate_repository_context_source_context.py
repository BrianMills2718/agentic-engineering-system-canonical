#!/usr/bin/env python3
"""Bounded checker for the repository-context source-local normative-context pilot.

This validates exact-text preservation, blueprint-declared applicability, and named
Python symbols/checks against caller-supplied source files. It is research tooling,
not a production AES schema and not evidence of behavioral conformance.
"""
from __future__ import annotations

import argparse
import ast
import copy
import json
import re
from pathlib import Path

import yaml


class ValidationError(ValueError):
    pass


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: expected mapping")
    return value


def extract_clause(markdown: str, clause_id: str) -> str:
    match = re.search(rf"^## {re.escape(clause_id)} — .+$", markdown, re.MULTILINE)
    if not match:
        raise ValidationError(f"missing clause {clause_id}")
    start = match.end()
    next_heading = re.search(r"^## ", markdown[start:], re.MULTILINE)
    end = start + (next_heading.start() if next_heading else len(markdown[start:]))
    paragraph = markdown[start:end].strip().split("\n\n", 1)[0].strip()
    if not paragraph:
        raise ValidationError(f"empty clause {clause_id}")
    return paragraph


def python_symbols(source: str) -> set[str]:
    tree = ast.parse(source)
    found: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            found.add(node.name)
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    found.add(f"{node.name}.{child.name}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found.add(node.name)
    return found


def component_blueprint(blueprint: dict, component_id: str) -> dict:
    for component in blueprint.get("components", []):
        if component.get("id") == component_id:
            return component
    raise ValidationError(f"blueprint missing component {component_id}")


def validate(
    record: dict,
    blueprint: dict,
    system_markdown: str,
    plan_markdown: str,
    resolver_source: str,
    resolver_tests: str,
    manifest_tests: str,
) -> dict:
    if record.get("status") != "generated_pilot":
        raise ValidationError("record is not generated_pilot")
    component = component_blueprint(blueprint, record["component_id"])
    local = component.get("local_context")
    if not isinstance(local, dict):
        raise ValidationError("blueprint lacks local_context declaration")

    expected_groups = {
        "direct_component": list(local.get("direct_clauses", [])),
        "context_delivery": list(local.get("context_delivery_clauses", [])),
        "outcome_context": list(local.get("outcome_clauses", [])),
    }
    normative = record["normative_context"]
    for group, expected in expected_groups.items():
        actual = [item["id"] for item in normative.get(group, [])]
        if actual != expected:
            raise ValidationError(
                f"{group} mismatch expected={expected} actual={actual}"
            )
        for item in normative.get(group, []):
            authoritative = extract_clause(system_markdown, item["id"])
            if item["verbatim"] != authoritative:
                raise ValidationError(f"non-verbatim text for {item['id']}")

    expected_conditional = [
        (item["clause"], item["when"]) for item in local.get("conditional_clauses", [])
    ]
    actual_conditional = [
        (item["id"], item["trigger"]) for item in normative.get("conditional", [])
    ]
    if actual_conditional != expected_conditional:
        raise ValidationError(
            f"conditional context mismatch expected={expected_conditional} "
            f"actual={actual_conditional}"
        )

    criteria = record["plan_context"]
    expected_ids = [f"AC-{index:03d}" for index in range(1, 12)]
    if criteria.get("component_acceptance_ids") != expected_ids:
        raise ValidationError("component acceptance set is incomplete or reordered")

    expanded = (
        criteria["primary_symbol_direct"]["criteria"]
        + criteria["relevant_criteria_verbatim"]
    )
    for item in expanded:
        if item["verbatim_source_line"] not in plan_markdown:
            raise ValidationError(
                f"criterion {item['id']} is absent or not verbatim in the plan"
            )

    primary = record["implementation_context"]["primary_symbol"]["symbol"]
    if primary not in python_symbols(resolver_source):
        raise ValidationError(f"missing implementation symbol {primary}")

    available_checks = python_symbols(resolver_tests) | python_symbols(manifest_tests)
    for item in record["implementation_context"]["native_checks"]:
        if item["symbol"] not in available_checks:
            raise ValidationError(f"missing native check {item['symbol']}")

    if (
        record["current"]["runtime_verification_at_exact_pinned_revision"]
        != "not_freshly_observed_in_this_pilot"
    ):
        raise ValidationError("pilot falsely promotes fresh runtime verification")
    if record["gap"]["closes_nothing_by_itself"] is not True:
        raise ValidationError("pilot falsely claims gap closure")

    return {
        "component": record["component_id"],
        "direct_clauses": len(normative["direct_component"]),
        "context_delivery_clauses": len(normative["context_delivery"]),
        "outcome_clauses": len(normative["outcome_context"]),
        "conditional_triggers": len(normative["conditional"]),
        "expanded_plan_criteria": len(expanded),
        "primary_symbol": primary,
        "native_checks": [item["symbol"] for item in record["implementation_context"]["native_checks"]],
        "status": "accepted_by_bounded_probe",
    }


def self_test(record: dict, *args) -> dict:
    mutations = {}

    candidate = copy.deepcopy(record)
    candidate["normative_context"]["direct_component"][0]["verbatim"] += " paraphrase"
    mutations["paraphrased_clause"] = candidate

    candidate = copy.deepcopy(record)
    candidate["normative_context"]["direct_component"].pop()
    mutations["omitted_direct_clause"] = candidate

    candidate = copy.deepcopy(record)
    candidate["normative_context"]["conditional"][0]["trigger"] = "always"
    mutations["changed_conditional_trigger"] = candidate

    candidate = copy.deepcopy(record)
    candidate["plan_context"]["primary_symbol_direct"]["criteria"][0][
        "verbatim_source_line"
    ] = "- AC-001 — changed"
    mutations["changed_plan_criterion"] = candidate

    candidate = copy.deepcopy(record)
    candidate["implementation_context"]["primary_symbol"]["symbol"] = (
        "RepositoryContextResolver.missing"
    )
    mutations["missing_code_symbol"] = candidate

    candidate = copy.deepcopy(record)
    candidate["implementation_context"]["native_checks"][0]["symbol"] = "test_missing"
    mutations["missing_native_check"] = candidate

    candidate = copy.deepcopy(record)
    candidate["current"]["runtime_verification_at_exact_pinned_revision"] = "verified"
    mutations["false_fresh_verification"] = candidate

    candidate = copy.deepcopy(record)
    candidate["gap"]["closes_nothing_by_itself"] = False
    mutations["false_gap_closure"] = candidate

    results = {}
    for name, altered in mutations.items():
        try:
            validate(altered, *args)
        except ValidationError as error:
            results[name] = {"rejected": True, "reason": str(error)}
        else:
            results[name] = {"rejected": False, "reason": "unexpectedly accepted"}
    if not all(result["rejected"] for result in results.values()):
        raise ValidationError(f"negative control failed: {results}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--blueprint", type=Path, required=True)
    parser.add_argument("--system", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--resolver", type=Path, required=True)
    parser.add_argument("--resolver-tests", type=Path, required=True)
    parser.add_argument("--manifest-tests", type=Path, required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    record = load_yaml(args.record)
    blueprint = load_yaml(args.blueprint)
    values = (
        blueprint,
        args.system.read_text(encoding="utf-8"),
        args.plan.read_text(encoding="utf-8"),
        args.resolver.read_text(encoding="utf-8"),
        args.resolver_tests.read_text(encoding="utf-8"),
        args.manifest_tests.read_text(encoding="utf-8"),
    )
    result = validate(record, *values)
    if args.self_test:
        result["negative_controls"] = self_test(record, *values)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
