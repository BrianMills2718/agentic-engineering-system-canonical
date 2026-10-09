"""Native child lifecycle -> existing feedback reports; parent checks bind exact results.

No new store or child closeout requirement. Read native JSON structure, never infer
success or causes from prose. Unknown runtime/context fields remain unknown.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

import records as R
import transcripts as T

MARKER = "<!-- subagent-verification:v1 "


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


class Check(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    argv: list[str] = Field(min_length=1)
    exit_code: int
    stdout: str
    stderr: str


class Verification(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    contract: Literal["subagent-verification.v1"] = "subagent-verification.v1"
    parent_session_id: str = Field(min_length=1)
    call_id: str = Field(min_length=1)
    child_ref: str = Field(min_length=1)
    result_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    ts: str
    verdict: Literal["pass", "fail", "inconclusive"]
    feedback: str = ""
    checks: list[Check] = Field(min_length=1)


class Outcome(BaseModel):
    """Additive report-envelope contract; existing feedback records stay unchanged."""
    model_config = ConfigDict(extra="allow")
    contract: Literal["subagent-outcome.v1"]
    call_id: str
    parent_session_id: str
    child_ref: str
    role: str
    task_name: str
    packet_sha256: str
    result_sha256: str | None
    occurred_at: str
    outcome: Literal["assigned", "dispatch_unresolved", "interruption_requested", "completed_unverified",
                     "failed", "cancelled", "verified_pass", "verified_fail", "verified_inconclusive", "verification_failed"]
    runtime: dict
    verification: Verification | None


def rows(path: Path):
    """Stream complete native records with byte offsets; partial writes wait for reread."""
    with path.open("rb") as fh:
        while raw := fh.readline():
            if not raw.endswith(b"\n"):
                break
            try:
                value = json.loads(raw)
                if isinstance(value, dict):
                    yield fh.tell() - len(raw), value
            except ValueError:
                continue


def obj(value):
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            result = json.loads(value)
            return result if isinstance(result, dict) else {}
        except ValueError:
            pass
    return {}


def text_content(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", "") for b in content or []
                     if isinstance(b, dict) and b.get("type") in ("text", "output_text", "input_text"))


def messages_in(value):
    """Unwrap native code-tool output envelopes before reading fixed receipts."""
    if isinstance(value, str):
        parsed = obj(value)
        if parsed:
            yield from messages_in(parsed)
        else:
            yield value
    elif isinstance(value, list):
        for item in value:
            yield from messages_in(item)
    elif isinstance(value, dict):
        for key in ("text", "output", "content", "value"):
            if key in value:
                yield from messages_in(value[key])


def claude_children(parent: Path, session: str):
    """Index native child identities and exact initial packets, without reading prose meaning."""
    children = {}
    for path in (parent.parent / session / "subagents").glob("agent-*.jsonl"):
        for _, row in rows(path):
            if row.get("type") != "user":
                continue
            child = row.get("agentId")
            content = obj(row.get("message")).get("content")
            if (row.get("isSidechain") is True and row.get("sessionId") == session
                    and isinstance(child, str) and child and path.stem == "agent-" + child
                    and isinstance(content, str) and content):
                children[child] = (path, digest(content))
            break
    return children


def calls(path: Path, client: str):
    """Pair calls/results over the whole changed parent, not the collector's new tail."""
    pending, found, receipts, child_calls = {}, [], [], set()
    session, cwd = path.stem[-36:], ""
    for at, d in rows(path):
        p = obj(d.get("payload"))
        ts = str(d.get("timestamp") or "")
        if client == "codex" and d.get("type") == "session_meta":
            session, cwd = p.get("id", session), p.get("cwd", "")
        if client == "claude":
            session, cwd = d.get("sessionId", session), d.get("cwd", cwd)
        candidates, outputs, messages = [], [], []
        if client == "codex" and d.get("type") == "response_item":
            if p.get("type") == "function_call":
                candidates.append((p.get("call_id"), p.get("name", "").split(".")[-1], obj(p.get("arguments"))))
            elif p.get("type") == "function_call_output":
                outputs.append((p.get("call_id"), obj(p.get("output"))))
                if p.get("call_id") not in child_calls:
                    messages.append(str(p.get("output", "")))
            elif p.get("type") == "custom_tool_call_output":
                messages.extend(messages_in(p.get("output")))
        elif client == "claude" and not d.get("isSidechain"):
            for b in d.get("message", {}).get("content", []) if isinstance(d.get("message", {}).get("content"), list) else []:
                if b.get("type") == "tool_use":
                    candidates.append((b.get("id"), b.get("name"), obj(b.get("input"))))
                elif b.get("type") == "tool_result":
                    outputs.append((b.get("tool_use_id"), obj(d.get("toolUseResult"))))
                    if b.get("tool_use_id") not in child_calls:
                        messages.append(text_content(b.get("content")))
        for call_id, name, args in candidates:
            if name in ("spawn_agent", "followup_task", "Agent", "Task", "TaskOutput", "SendMessage"):
                child_calls.add(call_id)
            if name in ("spawn_agent", "followup_task", "Agent", "Task") and call_id:
                target = args.get("target")
                previous = next((r for r in reversed(found) if r["child_ref"] == target or
                                 r["child_ref"].endswith("/" + str(target))), {}) if target else {}
                run = {"call_id": call_id, "parent_session_id": session, "client": client,
                       "parent_trace": str(path), "cwd": cwd, "ts": ts, "offset": at,
                       "role": args.get("agent_type") or args.get("subagent_type") or previous.get("role", "unknown"),
                       "task_name": args.get("task_name") or args.get("description") or target or "unknown",
                       "requested_context_mode": args.get("fork_turns", "unspecified"),
                       "packet_sha256": digest(json.dumps(args, sort_keys=True)),
                       "requested_model": args.get("model"), "requested_effort": args.get("reasoning_effort"),
                       "child_ref": previous.get("child_ref", target or "unknown"), "terminal": "assigned", "result": "", "result_ts": ts,
                       "runtime": {}, "child_trace": None, "limitations": []}
                if client == "claude":
                    prompt = args.get("prompt")
                    run["native_task_prompt_sha256"] = digest(prompt) if isinstance(prompt, str) and prompt else None
                pending[call_id] = run
                found.append(run)
            elif name in ("interrupt_agent", "close_agent"):
                pending[call_id] = {"operation": name, "target": args.get("target") or args.get("id")}
        for call_id, output in outputs:
            run = pending.get(call_id)
            if run and "operation" not in run:
                run["child_ref"] = output.get("task_name") or output.get("agent_id") or output.get("agentId") or run["child_ref"]
                if output.get("status") in ("completed", "failed", "cancelled", "killed"):
                    run.update(terminal="cancelled" if output["status"] == "killed" else output["status"],
                               result=text_content(output.get("content")), result_ts=ts)
                if output.get("resolvedModel"):
                    run["runtime"]["model"] = output["resolvedModel"]
                if output.get("usage"):
                    run["runtime"]["usage"] = output["usage"]
                if output.get("harnessSectionHash"):
                    run["runtime"]["delivered_rules_sha256"] = output["harnessSectionHash"]
                if run["child_ref"] == "unknown":
                    run["terminal"] = "dispatch_unresolved"
            if run and "operation" in run:
                for child in found:
                    if child["child_ref"] == run["target"]:
                        if child["terminal"] not in ("completed", "failed", "cancelled"):
                            child.update(terminal="interruption_requested", result_ts=ts)
            for agent in output.get("agents", []):
                status = agent.get("agent_status")
                for child in reversed(found):
                    if child["child_ref"] == agent.get("agent_name") and isinstance(status, dict):
                        for key in ("completed", "failed", "cancelled"):
                            if key in status:
                                child.update(terminal=key, result=str(status[key]), result_ts=ts)
                        break
        for message in messages:
            # Fixed structural marker only; no interpretation of surrounding prose.
            start = message.find(MARKER)
            if start >= 0:
                end = message.find(" -->", start)
                if end >= 0:
                    try:
                        v = Verification.model_validate_json(message[start + len(MARKER):end])
                        if v.parent_session_id == session:
                            receipts.append(v)
                    except ValueError:
                        pass
    if client == "claude":
        children = claude_children(path, session)
        for run in found:
            prompt_hash = run.get("native_task_prompt_sha256")
            if run["child_ref"] in children:
                matches = [(run["child_ref"], children[run["child_ref"]])]
                identity_source = "native parent receipt"
            elif (run["child_ref"] == "unknown" and prompt_hash
                  and sum(r.get("native_task_prompt_sha256") == prompt_hash for r in found) == 1):
                matches = [(child, data) for child, data in children.items() if data[1] == prompt_hash]
                identity_source = "native identity and exact initial packet"
            else:
                matches = []
            if len(matches) == 1:
                child, (child_path, _) = matches[0]
                run.update(child_ref=child, child_session_id=child, child_trace=str(child_path))
                run["runtime"]["child_identity_source"] = identity_source
                if run["terminal"] == "dispatch_unresolved":
                    run["terminal"] = "assigned"
            else:
                run["limitations"].append("Claude child trace unavailable or ambiguous; no child result attributed")
    for i, run in enumerate(found):
        run["result_before"] = next((r["ts"] for r in found[i + 1:]
                                     if r["child_ref"] == run["child_ref"]), None)
    return found, receipts


def codex_index(root: Path):
    """Metadata-only index, once per collection; includes parents and children."""
    index = {}
    for path in root.glob("**/rollout-*.jsonl"):
        try:
            with path.open("rb") as fh:
                meta = obj(json.loads(fh.readline()).get("payload"))
            index[meta.get("id")] = (path, meta)
        except (OSError, ValueError):
            continue
    return index


def enrich(run: dict, index: dict):
    if run["client"] == "claude":
        if not run.get("child_trace"):
            return
        for _, d in rows(Path(run["child_trace"])):
            ts = str(d.get("timestamp") or "")
            if (d.get("sessionId") != run["parent_session_id"] or d.get("agentId") != run["child_ref"]
                    or d.get("isSidechain") is not True
                    or (ts and (ts < run["ts"] or (run.get("result_before") and ts >= run["result_before"])))):
                continue
            message = obj(d.get("message"))
            if d.get("type") != "assistant" or d.get("isApiErrorMessage"):
                continue
            if message.get("model") and message["model"] != "<synthetic>":
                run["runtime"]["model"] = message["model"]
            if d.get("perTurnEffort") is not None:
                run["runtime"]["effort"] = d["perTurnEffort"]
            if message.get("usage"):
                run["runtime"]["usage"] = message["usage"]
            content = text_content(message.get("content"))
            if (message.get("stop_reason") == "end_turn" and content
                    and run["terminal"] not in ("failed", "cancelled")):
                run.update(terminal="completed", result=content, result_ts=ts)
        return
    if run["client"] != "codex":
        return
    matches = []
    for path, meta in index.values():
        spawn = obj(obj(obj(meta.get("source")).get("subagent")).get("thread_spawn"))
        if spawn.get("parent_thread_id") == run["parent_session_id"] and (
            spawn.get("agent_path") == run["child_ref"] or meta.get("id") == run["child_ref"]
        ):
            matches.append((path, meta))
    if len(matches) != 1:
        run["limitations"].append("child trace unavailable or ambiguous; runtime attribution unknown")
        return
    path, meta = matches[0]
    run["child_trace"], run["child_session_id"] = str(path), meta["id"]
    run["runtime"]["role"] = meta.get("agent_role")
    run["runtime"]["role_definition_revision"] = None
    run["limitations"].append("role definition revision not observed; delivered instruction digests identify snapshots only")
    for _, d in rows(path):
        p = obj(d.get("payload"))
        ts = str(d.get("timestamp") or "")
        if ts and (ts < run["ts"] or (run.get("result_before") and ts >= run["result_before"])):
            continue
        if d.get("type") == "turn_context":
            run["runtime"].update(model=p.get("model"), effort=p.get("effort"))
        if d.get("type") == "response_item" and p.get("type") == "message":
            if p.get("role") in ("system", "developer"):
                content = text_content(p.get("content"))
                if content:
                    run["runtime"].setdefault("instruction_digests", []).append(digest(content))
            if (p.get("role") == "assistant" and p.get("phase") == "final_answer"
                    and run["terminal"] not in ("failed", "cancelled")):
                run.update(terminal="completed", result=text_content(p.get("content")),
                           result_ts=str(d.get("timestamp") or ""))
        if d.get("type") == "event_msg" and p.get("type") == "token_count":
            run["runtime"]["usage"] = p.get("info")


def report(run: dict, verification: Verification | None = None) -> dict:
    result_hash = digest(run["result"]) if run["result"] else None
    state = run["terminal"]
    valid = verification and run["terminal"] == "completed" and result_hash and (
        verification.parent_session_id == run["parent_session_id"] and
        verification.call_id == run["call_id"] and verification.child_ref == run["child_ref"] and
        verification.result_sha256 == result_hash)
    if valid:
        state = "verified_" + verification.verdict if all(c.exit_code == 0 for c in verification.checks) else "verification_failed"
    elif state == "completed":
        state = "completed_unverified"
    # A later check describes the original child event. Only a checker failure
    # is a new event at check time; unknown native event times remain unknown.
    occurred_at = verification.ts if valid and state == "verification_failed" else run["result_ts"]
    metadata = {k: v for k, v in run.items() if k != "result"}
    metadata.update(contract="subagent-outcome.v1", outcome=state, result_sha256=result_hash,
                    occurred_at=occurred_at,
                    result_task_id=obj(run["result"]).get("task_id"),
                    child_reported_status=obj(run["result"]).get("status"),
                    verification=verification.model_dump() if valid else None,
                    attribution="observed lifecycle and checks; cause not established")
    metadata = Outcome.model_validate(metadata).model_dump()
    # Stable event IDs make whole-parent rereads and resumed collection idempotent.
    rid = "rep-subagent-" + digest(json.dumps([run["parent_session_id"], run["call_id"], state,
                                              result_hash, occurred_at, metadata["verification"]], sort_keys=True))[:16]
    sentence = f"Subagent {run['role']} task {run['task_name']} outcome {state}; root cause and preventive target require trace analysis."
    prov = R.Provenance(client=run["client"], session_id=run["parent_session_id"],
                        turn_offset=run["offset"], ts=occurred_at,
                        cwd=run["cwd"], line=sentence)
    links = [R.Link(kind="path", ref=run["parent_trace"])]
    if run.get("child_trace"):
        links.append(R.Link(kind="path", ref=run["child_trace"]))
    rec = R.Record(kind="observation", text=sentence, subject_kind="control", links=links,
                   expected="Parent checks the exact returned result before treating completion as success.", provenance=prov)
    rec.id = "rec-subagent-" + rid.removeprefix("rep-subagent-")
    records, rest = [rec.model_dump()], []
    if valid and verification.feedback:
        notes, rest = R.parse_feedback(verification.feedback, prov)
        records.extend(r.model_dump() for r in notes)
    return {"id": rid, "field": "Subagent outcome", "transcript": run["parent_trace"],
            "provenance": prov.model_dump(), "value": sentence, "records": records,
            "rest": rest, "subagent": metadata}


def reports(transcripts: list[T.Transcript], counts, sessions_root: Path | None = None) -> list[dict]:
    root = sessions_root or Path.home() / ".codex/sessions"
    index = codex_index(root) if any(t.client == "codex" for t in transcripts) else {}
    parents = {(t.path, t.client) for t in transcripts}
    for t in transcripts:
        meta = index.get(t.session_id, (None, {}))[1]
        spawn = obj(obj(obj(meta.get("source")).get("subagent")).get("thread_spawn"))
        if spawn.get("parent_thread_id") in index:
            parents.add((str(index[spawn["parent_thread_id"]][0]), "codex"))
    out = {}
    for path, client in sorted(parents):
        runs, receipts = calls(Path(path), client)
        for run in runs:
            enrich(run, index)
            candidates = [v for v in receipts if v.call_id == run["call_id"]]
            rep = report(run, candidates[-1] if candidates else None)
            out[rep["id"]] = rep
            counts["subagent_" + rep["subagent"]["outcome"]] += 1
    return list(out.values())


def verify(run: dict, commands: list[list[str]], verdict: Literal["pass", "fail", "inconclusive"] = "inconclusive", feedback: str = "") -> Verification:
    if run["terminal"] != "completed" or not run["result"] or not commands:
        raise ValueError("Verification requires an observed completed result and executable parent checks")
    checks = []
    for argv in commands:
        if not argv or any(not isinstance(a, str) for a in argv):
            raise ValueError("Each --check-argv must be a nonempty JSON string array")
        try:
            p = subprocess.run(argv, input=run["result"], capture_output=True, text=True, check=False)
            checks.append(Check(argv=argv, exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr))
        except OSError as exc:
            checks.append(Check(argv=argv, exit_code=127, stdout="", stderr=str(exc)))
    return Verification(parent_session_id=run["parent_session_id"], call_id=run["call_id"],
                        child_ref=run["child_ref"], result_sha256=digest(run["result"]),
                        ts=dt.datetime.now(dt.timezone.utc).isoformat(), verdict=verdict, feedback=feedback, checks=checks)


def persist(rep: dict, out: Path, file: bool) -> dict:
    """Use exactly the collector's daily report log and report-dedup table."""
    import feedback_log as FL
    out.mkdir(parents=True, exist_ok=True)
    day = dt.datetime.now(dt.timezone.utc).date().isoformat()
    with sqlite3.connect(out / "state.sqlite") as db:
        db.execute("CREATE TABLE IF NOT EXISTS reports (id TEXT PRIMARY KEY, day TEXT, records INT, issue TEXT)")
        db.execute("BEGIN IMMEDIATE")
        old = db.execute("SELECT issue FROM reports WHERE id=?", (rep["id"],)).fetchone()
        if old and (old[0].startswith("http") or not file):
            return rep | {"filing": old[0], "deduplicated": True}
        rep = rep | {"filing": FL.file_report(rep) if file else "not_filed", "run_id": "subagent-parent-check"}
        with (out / f"reports-{day}.jsonl").open("a") as fh:
            fh.write(json.dumps(rep, ensure_ascii=False) + "\n")
        db.execute("INSERT OR REPLACE INTO reports VALUES (?,?,?,?)", (rep["id"], day, len(rep["records"]), rep["filing"]))
    return rep


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--parent-transcript", required=True, type=Path)
    ap.add_argument("--client", required=True, choices=("codex", "claude"))
    ap.add_argument("--call-id", required=True)
    ap.add_argument("--sessions-root", type=Path, default=Path.home() / ".codex/sessions")
    ap.add_argument("--check-argv", action="append", default=[], help="JSON argv; receives exact child result on stdin")
    ap.add_argument("--verdict", choices=("pass", "fail", "inconclusive"), default="inconclusive",
                    help="parent disposition; successful structural checks alone do not establish task success")
    ap.add_argument("--feedback", default="", help="parent's provenanced obs/claim/action lines; no child self-rating")
    ap.add_argument("--out", type=Path, default=Path.home() / "projects/data/feedback-collector")
    ap.add_argument("--file", action="store_true", help="file through existing feedback_log and deduplicate in state.sqlite")
    args = ap.parse_args()
    runs, _ = calls(args.parent_transcript, args.client)
    run = next(r for r in runs if r["call_id"] == args.call_id)
    enrich(run, codex_index(args.sessions_root) if args.client == "codex" else {})
    verification = verify(run, [json.loads(c) for c in args.check_argv], args.verdict, args.feedback) if args.check_argv else None
    if verification:
        print(MARKER + verification.model_dump_json() + " -->")
    rep = report(run, verification)
    if rep["rest"]:
        print("RESULT exit=2: immediate filing requires obs/claim/action feedback markers; "
              "the emitted receipt retains unmarked notes for the collector's existing splitter", file=sys.stderr)
        return 2
    rep = persist(rep, args.out, args.file)
    print(json.dumps({"report_id": rep["id"], "outcome": rep["subagent"]["outcome"], "filing": rep["filing"]}))
    code = int(rep["subagent"]["outcome"] in ("verified_fail", "verification_failed"))
    print(f"RESULT records={len(rep['records'])} checks={len(verification.checks) if verification else 0} exit={code}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
