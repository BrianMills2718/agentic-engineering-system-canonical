#!/usr/bin/env python3
"""Bounded structural probe for AES-BLUEPRINT-001, not a production AES schema.

Checks this draft's internal declarations against an exact SYSTEM_BOUNDARY blob.
Does not prove semantic applicability, provider compatibility, code behavior,
typed runtime integration, complete requirements, or stakeholder acceptance.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

import yaml


class UniqueKeysLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of accepting the last value."""


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeysLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def blob_id(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def validate(document, system_raw: bytes):
    require(document["status"] == "proposed", "this probe does not accept architecture")
    sources = document["sources"]
    for snapshot in document["snapshots"].values():
        require(bool(re.fullmatch(r"[0-9a-f]{40}", snapshot["revision"])),
                "source revision is not an exact commit")
    for source in sources.values():
        require(source["snapshot"] in document["snapshots"], "unknown source snapshot")
        path = PurePosixPath(source["path"])
        require(not path.is_absolute() and ".." not in path.parts, "unsafe source path")
    require(blob_id(system_raw) == sources["system"]["git_blob"],
            "SYSTEM_BOUNDARY bytes do not match the declared source blob")
    clauses = set(re.findall(r"^## (AES-[A-Z]+-\d+) ", system_raw.decode(), re.M))
    require(bool(clauses), "no source clauses")
    shared = document["normative_binding_proposal"]["shared_context"]["clauses"]
    require(set(shared) <= clauses, "unknown shared clause")
    components = document["components"]
    ids = [component["id"] for component in components]
    require(len(ids) == len(set(ids)), "duplicate component")
    homes = []
    seen = set(shared)
    for component in components:
        for field in ("purpose", "clauses", "origin_gaps", "local_role",
                      "provider_disposition", "code_home", "proposed_record",
                      "boundary", "checks", "open_questions"):
            require(bool(component.get(field)), f"{component['id']}: missing {field}")
        home = PurePosixPath(component["code_home"])
        require(str(home).startswith("src/agentic_engineering_system/"),
                "component outside the existing implementation root")
        require(".." not in home.parts, "unsafe code home")
        require(all(home != old and old not in home.parents and home not in old.parents
                    for old in homes), "overlapping code homes")
        homes.append(home)
        record = PurePosixPath(component["proposed_record"])
        require(home in record.parents, "record not colocated with declared code home")
        require(set(component["clauses"]) <= clauses, "unknown component clause")
        seen.update(component["clauses"])
        boundary = component["boundary"]
        require(boundary["state"] in ("unresolved", "observed_signature_not_executed_here"),
                "unsupported boundary verification claim")
        if boundary["state"] == "unresolved":
            require(bool(boundary.get("blocked_by")), "unresolved boundary lacks question")
        else:
            require(boundary["source"] in sources, "unknown boundary source")
            require(component.get("source_status") == "present_on_implementation_snapshot",
                    "signature presence cannot be inherited by a reserved component")
        require(bool(component["checks"].get("obligation")), "missing verification obligation")
        require(bool(component["checks"].get("disproof")), "missing disproof")
        if "source" in component["checks"]:
            require(component["checks"]["source"] in sources, "unknown check source")
    for seam in document["seams"]:
        require(set(seam["participants"]) <= set(ids), "unknown seam participant")
        require(set(seam["clauses"]) <= clauses, "unknown seam clause")
        seen.update(seam["clauses"])
    require(seen == clauses, "accepted system clause has no declared mapping")
    require(all(item["status"] == "proposed" for item in document["decision_sequence"]),
            "unaccepted design choice promoted")
    return {"components": len(components), "seams": len(document["seams"]),
            "system_clauses_referenced": len(seen)}


def self_test(document, system_raw):
    cases = {
        "duplicate_component": lambda x: x["components"].append(copy.deepcopy(x["components"][0])),
        "overlapping_home": lambda x: x["components"][1].update(code_home=x["components"][0]["code_home"]),
        "unknown_clause": lambda x: x["components"][0]["clauses"].append("AES-UNKNOWN-999"),
        "missing_disproof": lambda x: x["components"][0]["checks"].pop("disproof"),
        "mutable_revision": lambda x: x["snapshots"]["bootstrap"].update(revision="main"),
        "false_verified_boundary": lambda x: x["components"][1]["boundary"].update(state="verified"),
        "unknown_seam_participant": lambda x: x["seams"][0]["participants"].append("missing"),
    }
    results = {}
    for name, mutation in cases.items():
        altered = copy.deepcopy(document)
        mutation(altered)
        try:
            validate(altered, system_raw)
        except ValueError as error:
            results[name] = {"rejected": True, "reason": str(error)}
        else:
            raise ValueError(f"negative control incorrectly accepted: {name}")
    try:
        yaml.load("status: proposed\nstatus: accepted\n", Loader=UniqueKeysLoader)
    except ValueError as error:
        results["duplicate_yaml_key"] = {"rejected": True, "reason": str(error)}
    else:
        raise ValueError("duplicate YAML key accepted")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blueprint", type=Path)
    parser.add_argument("--system-boundary", required=True, type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        raw = args.blueprint.read_bytes()
        document = yaml.load(raw.decode(), Loader=UniqueKeysLoader)
        system_raw = args.system_boundary.read_bytes()
        result = validate(document, system_raw)
        result["blueprint_sha256"] = hashlib.sha256(raw).hexdigest()
        result["scope"] = "draft_structure_only"
        result["positive_fixture"] = "accepted_by_this_bounded_probe"
        if args.self_test:
            result["negative_controls"] = self_test(document, system_raw)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print(json.dumps({"scope": "draft_structure_only", "error": str(error)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
