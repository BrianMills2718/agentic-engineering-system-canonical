"""Thin AES binding to Company Planning's source-bound review provider.

No cached receipt or declared step count substitutes for opening retained bytes.
Provider configuration is machine-owned; missing configuration fails closed.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReviewCheck:
    status: str
    run_outcome: str | None
    reason: str


def _local(root: Path, ref: str) -> Path:
    relative = Path(ref)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("review evidence must be repository-relative")
    path = (root / relative).resolve()
    path.relative_to(root.resolve())
    return path


def _command() -> list[str]:
    configured = os.environ.get("AES_TRACE_REVIEW_COMMAND")
    if configured is None:
        config = Path.home() / ".config/aes/trace-review.json"
        command = json.loads(config.read_text())["command"]
    else:
        command = json.loads(configured)
    if not isinstance(command, list) or not command or any(
        not isinstance(item, str) or not item for item in command
    ):
        raise ValueError("trace review provider command must be a nonempty argv array")
    return command


def check_source_review(root: Path, observation: Any, criterion_id: str) -> ReviewCheck:
    """Validate retained reviews afresh, then bind them to native observation identity.

    Completeness and run correctness remain separate; callers must not promote
    a failed run simply because its review is complete.
    """
    tr = observation.trace_review
    refs = (observation.result or {}).get("trace_reviews")
    if tr is None or not isinstance(refs, list) or not refs:
        return ReviewCheck("unavailable", None, "retained source-bound trace_reviews are missing")
    try:
        command = _command()
        outcomes = []
        sources = set()
        steps = 0
        if len(set(refs)) != len(refs):
            raise ValueError("duplicate native review references")
        for ref in refs:
            if not isinstance(ref, str) or ref not in observation.retained_artifact_refs:
                raise ValueError("review reference is not a retained native artifact")
            path = _local(root, ref)
            before = path.read_bytes()
            completed = subprocess.run(
                [*command, ref, "--repo-root", str(root)], cwd=root,
                capture_output=True, text=True, check=False,
            )
            reply = json.loads(completed.stdout)
            if not isinstance(reply, dict):
                raise ValueError("provider response must be a JSON object")
            if completed.returncode != 0 or reply.get("valid") is not True or reply.get("exit_status") != 0:
                return ReviewCheck("incomplete", reply.get("run_outcome"),
                                   "provider refused full review: " + json.dumps(reply.get("errors", [])))
            if hashlib.sha256(before).digest() != hashlib.sha256(path.read_bytes()).digest():
                raise ValueError("review changed during provider validation")
            review = json.loads(before)
            for retained in (review["source"], *([review["assessment"]] if "assessment" in review else [])):
                if hashlib.sha256(_local(root, retained["path"]).read_bytes()).hexdigest() != retained["sha256"]:
                    raise ValueError("retained source or assessment changed during provider validation")
            if criterion_id not in review["criterion_ids"]:
                raise ValueError("review does not cover the native criterion")
            if observation.subject_revision is None or review["evidence_revision"] != observation.subject_revision:
                raise ValueError("review revision differs from the native observed revision")
            if review["reviewer"] != tr.reviewer:
                raise ValueError("reviewer identity differs from the native review")
            if review["run_id"] != (observation.result or {}).get("run_id"):
                raise ValueError("review run differs from the native retained run")
            source = review["source"]["path"]
            if source not in tr.trace_refs or source not in observation.retained_artifact_refs:
                raise ValueError("review source is not the native retained trace")
            if source in sources:
                raise ValueError("multiple reviews claim the same native source")
            sources.add(source)
            steps += len(review["reviewed_entries"])
            outcome = review["run_outcome"]
            if reply.get("review_status") != "complete" or reply.get("run_outcome") != outcome:
                raise ValueError("provider verdict disagrees with retained review")
            outcomes.append(outcome)
        if sources != set(tr.trace_refs) or len(sources) != len(tr.trace_refs):
            raise ValueError("native trace source membership differs from the reviewed sources")
        if steps != tr.steps_total or tr.steps_read != tr.steps_total:
            raise ValueError("native step membership differs from the validated full inventory")
        outcome = "fail" if "fail" in outcomes else "inconclusive" if "inconclusive" in outcomes else "pass"
        return ReviewCheck("complete", outcome, f"source-bound full review complete; run={outcome}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return ReviewCheck("unavailable", None, f"source-bound review unavailable: {exc}")
