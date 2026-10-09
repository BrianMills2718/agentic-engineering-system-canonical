"""Parent check for the bounded native/Remote MCP instruction regression.

This checks identity, schema, frozen source and citation membership. The parent
also reads the native tool trace and checks the meaning of the cited evidence;
this command does not treat a child's self-rating as behavioral proof.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import jsonschema


def verify(packet: dict, result: dict, expect: str) -> None:
    schema_path = Path(packet["result_schema_path"])
    assert hashlib.sha256(schema_path.read_bytes()).hexdigest() == packet["result_schema_sha256"]
    jsonschema.validate(result, json.loads(schema_path.read_text()))
    assert result["task_id"] == packet["task_id"], "wrong assignment"
    assert result["status"] == expect, "unexpected task outcome"
    allowed = set(packet["allowed_read_paths"])
    for source, digest in packet["source_sha256"].items():
        assert source in allowed
        assert hashlib.sha256(Path(source).read_bytes()).hexdigest() == digest, "source changed"
    citations = set()
    for item in result["evidence"]:
        assert item["path"] in allowed, "citation outside packet"
        line = int(item["locator"][1:])
        assert line <= len(Path(item["path"]).read_text().splitlines()), "invalid citation"
        citations.add((item["path"], item["locator"]))
    required = {(item["path"], item["locator"]) for item in packet["required_citations"]}
    assert required <= citations, "missing causal source citation"
    if expect == "supported":
        assert packet["execution_transport"] == "native_local"
        assert result["root_cause"] and result["causal_chain"]
    else:
        assert packet["execution_transport"] == "remote_mcp"
        assert result["root_cause"] is None and not result["causal_chain"]
        assert result["limitations"], "unavailable remote route must be explicit"
        assert all(item["path"] in packet["authority_paths"] for item in result["evidence"]), "remote stop read parser"


def self_test(packet: dict, result: dict, expect: str) -> None:
    verify(packet, result, expect)
    bad = copy.deepcopy(result)
    bad["task_id"] = "another-assignment"
    cases = [bad]
    bad = copy.deepcopy(result)
    bad["mutation_declaration"]["files_changed"] = True
    cases.append(bad)
    bad = copy.deepcopy(result)
    bad["evidence"] = []
    cases.append(bad)
    bad = copy.deepcopy(result)
    bad["status"] = "inconclusive" if expect == "supported" else "supported"
    cases.append(bad)
    for bad in cases:
        try:
            verify(packet, bad, expect)
        except (AssertionError, jsonschema.ValidationError):
            continue
        raise AssertionError("negative case accepted")
    print("self-test: 5 passed, 0 failed; exit=0")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--expect", choices=("supported", "inconclusive"), required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        packet = json.loads(args.packet.read_text())
        result = json.loads(args.result.read_text())
        if args.self_test:
            self_test(packet, result, args.expect)
        else:
            verify(packet, result, args.expect)
            print("parent case check: 1 passed, 0 failed; exit=0")
        return 0
    except (AssertionError, jsonschema.ValidationError, ValueError, KeyError, OSError) as error:
        print(f"parent case check: 0 passed, 1 failed; exit=1; {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
