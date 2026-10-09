"""Check the actual native canary return against its frozen packet and result schema.

Usage: python verify_canary.py PACKET.json RESULT_SCHEMA.json < exact-result.json
This confirms honest inconclusive evidence, not successful parser diagnosis.
"""
import hashlib
import json
import sys
from pathlib import Path

import jsonschema

packet = json.loads(Path(sys.argv[1]).read_text())
schema = json.loads(Path(sys.argv[2]).read_text())
result = json.load(sys.stdin)
jsonschema.validate(result, schema)
assert result["task_id"] == packet["task_id"]
assert result["specialist_id"] == "development-investigator"
assert result["status"] == "inconclusive" and result["root_cause"] is None
assert result["causal_chain"] == []
assert all(v is False for v in result["mutation_declaration"].values())
for path, expected in packet["source_sha256"].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, path
authority = Path(packet["authority_paths"][1])
lines = authority.read_text().splitlines()
expected = {106: ("devices_list", "devices_ping", "process_start"),
            107: ("SESSION_TOOL_NOT_EXPOSED", "GitHub-only"),
            110: ("Only after the ping succeeds",)}
assert {(e["path"], e["locator"]) for e in result["evidence"]} == {
    (str(authority), f"L{n}") for n in expected}
for number, fragments in expected.items():
    assert all(fragment in lines[number - 1] for fragment in fragments), number
print("RESULT schema=passed task_identity=passed source_hashes=passed citation_membership=passed mutation_declaration=passed task_verdict=inconclusive exit=0")
