#!/usr/bin/env python3
"""Validate an AES architecture-realization YAML record with JSON Schema 2020-12.

JSON Schema owns structural validation. This small AES research checker adds only
cross-record constraints JSON Schema cannot express compactly here: unique
component/seam IDs, declared seam participants, and declared seam references.

It does not validate provider conformance, code behavior, normative applicability,
or verification adequacy.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def load_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_schema(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("schema must be an object")
    Draft202012Validator.check_schema(value)
    return value


def custom_errors(record: dict) -> list[str]:
    errors: list[str] = []
    components = record.get("components", [])
    seams = record.get("seams", [])
    component_ids = [item.get("id") for item in components if isinstance(item, dict)]
    seam_ids = [item.get("id") for item in seams if isinstance(item, dict)]

    if len(component_ids) != len(set(component_ids)):
        errors.append("duplicate component id")
    if len(seam_ids) != len(set(seam_ids)):
        errors.append("duplicate seam id")

    component_set = set(component_ids)
    seam_set = set(seam_ids)
    for seam in seams:
        for participant in seam.get("participants", []):
            if participant not in component_set:
                errors.append(f"seam {seam.get('id')} has undeclared participant {participant}")
    for component in components:
        for seam_ref in component.get("normative", {}).get("seams", []):
            if seam_ref not in seam_set:
                errors.append(f"component {component.get('id')} references undeclared seam {seam_ref}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    args = parser.parse_args()

    schema = load_schema(args.schema)
    record = load_yaml(args.record)
    if not isinstance(record, dict):
        print(json.dumps({"ok": False, "errors": ["record must be an object"]}))
        return 1

    validator = Draft202012Validator(schema)
    errors = [
        f"{'/'.join(str(x) for x in error.absolute_path)}: {error.message}"
        for error in validator.iter_errors(record)
    ]
    errors.extend(custom_errors(record))
    result = {"ok": not errors, "errors": errors}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
