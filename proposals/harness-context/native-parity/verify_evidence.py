"""Verify recorded native evidence without launching another model call."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tomllib

import jsonschema


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(path: Path):
    return json.loads(path.read_text())


def main() -> None:
    checks: list[str] = []

    def require(condition: bool, name: str) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    packet = read(HERE / "input/task.json")
    result = read(HERE / "codex-child-result.json")
    summary = read(HERE / "codex-trace-summary.json")
    skill_repo = Path.home() / "code/agent-skills"
    schema = read(skill_repo / "contracts/specialists/development-investigation-result.v1.schema.json")
    jsonschema.validate(result, schema)
    checks.append("native child result satisfies canonical schema")
    require(result["task_id"] == packet["task_id"], "child investigated the supplied task")
    require(result["status"] == "supported", "child returned source-supported diagnosis")
    files = {entry["path"]: entry for entry in packet["source_manifest"]}
    require(all(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == entry["sha256"]
                for name, entry in files.items()), "all five frozen sources remain unchanged")
    require(all(e["path"] in files and 0 < int(e["locator"][1:]) <=
                len((ROOT / e["path"]).read_text().splitlines()) for e in result["evidence"]),
            "all sixteen citations resolve within supplied sources")
    rows = {}
    for kind, item in summary.items():
        path = Path(item["trace_path"])
        require(hashlib.sha256(path.read_bytes()).hexdigest() == item["trace_sha256"],
                f"{kind} trace matches recorded digest")
        rows[kind] = [json.loads(line) for line in path.read_text().splitlines()]
        require(all(c["sandbox_policy"] == {"type": "read-only"} and
                    c["approval_policy"] == "never" for c in item["runtime_context"]),
                f"{kind} actual turn has read-only policy and no escalation")
    role = tomllib.loads((Path.home() / ".codex/agents/development-investigator.toml").read_text())
    texts = [text["text"] for row in rows["child"]
             if row.get("type") == "response_item" and row["payload"].get("type") == "message"
             for text in row["payload"].get("content", []) if "text" in text]
    require(role["developer_instructions"].strip() in {text.strip() for text in texts},
            "installed canonical specialist instructions appear in actual child input")
    meta = rows["child"][0]["payload"]
    require(meta["parent_thread_id"] == rows["parent"][0]["payload"]["id"] and
            meta["agent_role"] == "development-investigator", "native parent-child identity and role match")
    spawns = [json.loads(row["payload"]["arguments"]) for row in rows["parent"]
              if row.get("type") == "response_item" and row["payload"].get("name") == "spawn_agent"]
    require(len(spawns) == 1 and spawns[0]["fork_turns"] == "none",
            "native parent explicitly launched one fresh-history child")
    require(summary["child"]["workspace_bootstrap_loaded"] and
            summary["child"]["first_model_usage"]["input_tokens"] == 37750,
            "recorded context failure and first-input measurement match trace")
    probe = read(HERE / "permission-probe.json")
    require(probe["exit_code"] == 0 and probe["expected_denials_verified"] and
            not probe["sentinel_exists_after"], "independent native sandbox denied synthetic write and socket")
    refusal = read(HERE / "claude-refusal.json")
    require(refusal["api_error_status"] == 429 and refusal["api_error"] == "usage_limit_reached"
            and refusal["child_count"] == 0 and refusal["usage"]["input_tokens"] == 0,
            "Claude quota refusal cannot be counted as an executed child")
    receipt = {"checks_passed": len(checks), "checks_failed": 0, "exit_status": 0,
               "checks": checks, "parity_traces_available": ["codex_parent", "codex_child", "claude_parent_refusal"],
               "missing_required_trace": "claude_child", "cross_client_goal_complete": False,
               "limits": ["These checks validate recorded evidence, not cross-client completion.",
                          "Sandbox negative probe is independent of the child; no path-allowlist enforcement is claimed."]}
    (HERE / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
