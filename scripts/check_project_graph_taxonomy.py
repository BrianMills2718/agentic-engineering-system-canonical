#!/usr/bin/env python3
"""Validate PROJECT_GRAPH.json metadata for browsing and agent routing.

The path validator checks whether records point at real files. This checker
guards the descriptive layer: concise one-liners, controlled portfolio areas,
utility tags, duplicate ids/paths, and GitHub remotes for git-backed projects.

Implements: project-graph-taxonomy/graph-path-is-configured
Implements: project-graph-taxonomy/records-are-validated
Implements: project-graph-taxonomy/hard-errors-block
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from branch_policy import BRANCH_POLICY_SCOPES  # noqa: E402

# Copied from Project Meta scripts/check_project_graph_taxonomy.py (retirement plan step 4). The project graph is one
# person's own data: the PROJECT_GRAPH environment variable names it, else it is read from the private `aes-config`
# repository (Decision 20).
GRAPH_DEFAULT = os.environ.get("PROJECT_GRAPH") or os.path.expanduser("~/code2/aes-config/PROJECT_GRAPH.json")


ALLOWED_PORTFOLIO_AREAS = {
    "agent-platform",
    "application",
    "code-generation",
    "data-reference",
    "knowledge-graph",
    "operations",
    "research-system",
    "shared-infrastructure",
}
ALLOWED_SOURCES = {
    "archive-import",
    "brian-built",
    "external-reference",
    "local-brian",
    "pointer",
}
ALLOWED_ORGANIZATION_STATUSES = {
    "canonical",
    "do-not-move",
    "needs-move",
    "pointer-only",
}
ALLOWED_PORTFOLIO_TIERS = {
    "background",
    "core",
    "none",
    "supporting",
}
ALLOWED_RECORD_KINDS = {
    "container",
    "data",
    "nested-project",
    "pointer",
    "project",
    "repository",
}
ALLOWED_WORKSPACE_HOMES = {
    "central-archive",
    "code-active",
    "code-inactive",
    "code-template",
}
ALLOWED_REPOSITORY_OWNER_CLASSES = {"archived", "brian", "employer", "external", "organization"}
ALLOWED_MUTATION_AUTHORITIES = {"feature_branch_only", "normal_push", "read_only"}
ALLOWED_PUBLICATION_AUTHORITIES = {"recoverable_git", "separate_approval"}
ALLOWED_REPOSITORY_TOPOLOGY_MODES = {"contained"}
ALLOWED_PHYSICAL_BUCKETS = {
    "agent-platform",
    "analysis-methods",
    "applications",
    "archives/agent-platform",
    "archives/analysis-methods",
    "archives/applications",
    "archives/code-generation",
    "archives/data-reference",
    "archives/knowledge-graph",
    "archives/operations",
    "archives/research-systems",
    "archives/shared-infrastructure",
    "code-generation",
    "data-reference",
    "external",
    "knowledge-graph",
    "operations",
    "research-systems",
    "scratch",
    "shared-infrastructure",
}

NULL_PATH_ALLOWED_STATUSES = {"deleted", "merged"}
MAX_ONE_LINER_LENGTH = 220
MIN_ONE_LINER_LENGTH = 90
SPARSE_CHECK_STATUSES = {"active", "dormant", "complete"}
MIN_CAPABILITIES = 3
MIN_TAGS = 3
SAFE_WORKSPACE_SLUG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")


# Mojibake = UTF-8 bytes that were decoded as cp1252/latin-1 and re-saved
# (an em dash becomes "\u00e2\u20ac\u201d"). The lead characters are the UTF-8
# lead bytes 0xC2/0xC3/0xE2/0xF0 read as cp1252; the follower is any cp1252
# rendering of a continuation byte. A hit only counts when the string actually
# round-trips back to valid UTF-8, which keeps ordinary accented text clean.
MOJIBAKE_SEQUENCE = re.compile(
    "[\u00c2\u00c3\u00e2\u00f0][\u0080-\u00bf\u0152\u0153\u0160\u0161\u0178\u017d\u017e"
    "\u0192\u02c6\u02dc\u2013\u2014\u2018-\u201e\u2020-\u2022\u2026\u2030\u2039\u203a"
    "\u20ac\u2122]"
)


def repair_mojibake(value: str) -> str | None:
    """Return the correctly decoded text if `value` is cp1252-garbled UTF-8, else None."""
    if not MOJIBAKE_SEQUENCE.search(value):
        return None
    raw = bytearray()
    for char in value:
        try:
            raw += char.encode("cp1252")
        except UnicodeEncodeError:
            raw += char.encode("utf-8")
    try:
        repaired = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    return repaired if repaired != value else None


def find_mojibake(value: object, location: str = "") -> list[tuple[str, str]]:
    """Walk a JSON value; return (location, repaired text) for each garbled string."""
    if isinstance(value, str):
        repaired = repair_mojibake(value)
        return [(location, repaired)] if repaired is not None else []
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            found += find_mojibake(child, f"{location}.{key}" if location else str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found += find_mojibake(child, f"{location}[{index}]")
    return found


def is_hard_error(error: str) -> bool:
    """Return whether an error is deterministic enough to block `make check`."""
    hard_prefixes = (
        "duplicate id:",
        "duplicate existing path:",
        "duplicate portable destination:",
        "record missing non-empty id",
    )
    hard_fragments = (
        ": null path only allowed for deleted/merged records",
        ": path must be a non-empty string or null",
        ": one_liner must be non-empty",
        ": mojibake in ",
        ": unknown portfolio_area ",
        ": branch_policy",
        ": unknown branch_policy scope",
        ": repository_governance",
        ": unknown repository_governance.",
        ": repository_topology",
        ": unknown repository_topology.",
        ": project record",
        ": membership_manifest",
        ": workspace_slug",
        ": default_branch",
        ": utility_tags must be a non-empty list",
        ": utility_tags missing ",
        ": domains must be a list",
        ": tech must be a list",
        ": capabilities must be a list",
        ": tags must be a list",
        ": depends_on must be a list",
        ": supersedes must be a list",
        ": depends_on references unknown id",
        ": supersedes references unknown id",
        ": superseded_by must be a string or null",
        ": superseded_by references unknown id",
        ": github_repo does not match origin remote",
    )
    return error.startswith(hard_prefixes) or any(fragment in error for fragment in hard_fragments)


def normalize_github_repo(value: object) -> str | None:
    """Normalize GitHub remote syntaxes to owner/repo for comparison."""
    if not isinstance(value, str) or not value.strip():
        return None
    repo = value.strip()
    if repo.startswith("https://github.com/"):
        return repo.removeprefix("https://github.com/").removesuffix(".git")
    if repo.startswith("git@github"):
        return repo.split(":", 1)[1].removesuffix(".git")
    if repo.startswith("ssh://git@github"):
        # ssh://git@github-personal/owner/repo.git: an SSH host alias for a second account.
        return "/".join(repo.removesuffix(".git").split("/")[-2:])
    return repo.removesuffix(".git")


def load_records(path: Path) -> list[dict]:
    """Load a list-shaped PROJECT_GRAPH.json file."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("PROJECT_GRAPH.json must be a list of project records")
    records = [record for record in payload if isinstance(record, dict)]
    if len(records) != len(payload):
        raise ValueError("PROJECT_GRAPH.json contains non-object records")
    return records


# A git hook exports these for the committing repository; inherited by a child
# `git -C <other checkout>` they make it read the committing repository instead,
# so every checkout would report the committing repository's own origin.
_INHERITED_GIT_REPO_VARS = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_PREFIX",
)


def remote_for(path: Path) -> str | None:
    """Return the normalized origin remote for a local git repo path."""
    if not (path / ".git").exists():
        return None
    env = {key: value for key, value in os.environ.items() if key not in _INHERITED_GIT_REPO_VARS}
    try:
        remote = subprocess.check_output(
            ["git", "-C", str(path), "remote", "get-url", "origin"],
            text=True,
            stderr=subprocess.DEVNULL,
            env=env,
        ).strip()
    except subprocess.CalledProcessError:
        return None
    return normalize_github_repo(remote)


def validate_records(records: list[dict]) -> list[str]:
    """Return human-readable validation errors for project graph records."""
    errors: list[str] = []
    ids = [record.get("id") for record in records]
    for duplicate, count in Counter(ids).items():
        if duplicate is None:
            continue
        if count > 1:
            errors.append(f"duplicate id: {duplicate}")

    valid_ids: set[str] = {
        r["id"] for r in records if isinstance(r.get("id"), str) and r["id"].strip()
    }

    existing_paths: list[str] = []
    portable_destinations: list[tuple[str, str]] = []
    for record in records:
        record_id = record.get("id", "<missing-id>")
        if not isinstance(record_id, str) or not record_id.strip():
            errors.append("record missing non-empty id")
            continue

        for location, repaired in find_mojibake(record):
            errors.append(
                f"{record_id}: mojibake in {location} (cp1252-garbled UTF-8); "
                f"decoded text would be {repaired[:80]!r}"
            )

        status = str(record.get("status", "")).strip().lower()
        record_kind = record.get("record_kind")
        path_value = record.get("path")
        if path_value is None:
            if status not in NULL_PATH_ALLOWED_STATUSES and record_kind != "project":
                errors.append(f"{record_id}: null path only allowed for deleted/merged records")
        elif not isinstance(path_value, str) or not path_value.strip():
            errors.append(f"{record_id}: path must be a non-empty string or null")
        else:
            path = Path(path_value).expanduser()
            if path.exists():
                existing_paths.append(str(path.resolve()))
                remote = remote_for(path)
                if remote and normalize_github_repo(record.get("github_repo")) != remote:
                    errors.append(
                        f"{record_id}: github_repo does not match origin remote "
                        f"({record.get('github_repo')!r} != {remote!r})"
                    )

        one_liner = record.get("one_liner")
        if not isinstance(one_liner, str) or not one_liner.strip():
            errors.append(f"{record_id}: one_liner must be non-empty")
        elif len(one_liner) > MAX_ONE_LINER_LENGTH:
            errors.append(f"{record_id}: one_liner exceeds {MAX_ONE_LINER_LENGTH} chars")

        area = record.get("portfolio_area")
        if area not in ALLOWED_PORTFOLIO_AREAS:
            errors.append(f"{record_id}: unknown portfolio_area {area!r}")

        source = record.get("source")
        if source is not None and source not in ALLOWED_SOURCES:
            errors.append(f"{record_id}: unknown source {source!r}")

        physical_bucket = record.get("physical_bucket")
        if (
            physical_bucket is not None
            and (
                path_value is None
                or record.get("source") == "pointer"
                or record.get("organization_status") == "pointer-only"
            )
        ):
            errors.append(f"{record_id}: pointer-only/null-path record must omit physical_bucket")
        elif physical_bucket is not None and physical_bucket not in ALLOWED_PHYSICAL_BUCKETS:
            errors.append(f"{record_id}: unknown physical_bucket {physical_bucket!r}")

        organization_status = record.get("organization_status")
        if organization_status is not None and organization_status not in ALLOWED_ORGANIZATION_STATUSES:
            errors.append(f"{record_id}: unknown organization_status {organization_status!r}")

        visibility = record.get("visibility")
        if visibility is not None and visibility not in ("public", "private"):
            errors.append(f"{record_id}: unknown visibility {visibility!r} (use 'public' or 'private')")

        workspace_home = record.get("workspace_home")
        workspace_slug = record.get("workspace_slug")
        default_branch = record.get("default_branch")
        if record_kind is not None and record_kind not in ALLOWED_RECORD_KINDS:
            errors.append(f"{record_id}: unknown record_kind {record_kind!r}")
        if workspace_home is not None and workspace_home not in ALLOWED_WORKSPACE_HOMES:
            errors.append(f"{record_id}: unknown workspace_home {workspace_home!r}")

        is_pointer = (
            (path_value is None and record_kind != "project")
            or source == "pointer"
            or organization_status == "pointer-only"
        )
        if record_kind is not None and is_pointer and record_kind != "pointer":
            errors.append(f"{record_id}: pointer-only/null-path record_kind must be 'pointer'")
        if record_kind == "pointer" and workspace_home is not None:
            errors.append(f"{record_id}: pointer record must omit workspace_home")
        if workspace_home is not None and record_kind is None:
            errors.append(f"{record_id}: workspace_home requires explicit record_kind")
        if isinstance(workspace_home, str) and workspace_home.startswith("code-") and record_kind != "repository":
            errors.append(f"{record_id}: code workspace_home requires record_kind 'repository'")
        if record_kind == "nested-project" and workspace_home is not None:
            errors.append(f"{record_id}: nested-project record must inherit its parent workspace home")
        if record_kind == "project":
            if path_value is not None:
                errors.append(f"{record_id}: project record path must be null")
            if workspace_home is not None:
                errors.append(f"{record_id}: project record must omit workspace_home")
            pointer = record.get("membership_manifest")
            if not isinstance(pointer, dict):
                errors.append(f"{record_id}: project record requires membership_manifest")
            else:
                if set(pointer) != {"repository_id", "path"}:
                    errors.append(
                        f"{record_id}: membership_manifest must contain only repository_id and path"
                    )
                owner_id = pointer.get("repository_id")
                manifest_path = pointer.get("path")
                if not isinstance(owner_id, str) or owner_id not in valid_ids:
                    errors.append(f"{record_id}: membership_manifest references unknown repository id")
                elif next(
                    (candidate.get("record_kind") for candidate in records if candidate.get("id") == owner_id),
                    None,
                ) != "repository":
                    errors.append(f"{record_id}: membership_manifest owner must be a repository")
                if (
                    not isinstance(manifest_path, str)
                    or not manifest_path
                    or manifest_path.startswith("/")
                    or "\\" in manifest_path
                    or ".." in PurePosixPath(manifest_path).parts
                ):
                    errors.append(f"{record_id}: membership_manifest path must be repository-relative")
        if organization_status == "needs-move" and record_kind is None:
            errors.append(f"{record_id}: needs-move requires explicit record_kind")
        if organization_status == "needs-move" and record_kind == "repository" and workspace_home is None:
            errors.append(f"{record_id}: needs-move repository requires workspace_home")
        if workspace_slug is not None:
            if not isinstance(workspace_slug, str) or not SAFE_WORKSPACE_SLUG.fullmatch(workspace_slug):
                errors.append(f"{record_id}: workspace_slug must be a portable POSIX-safe basename")
            if record_kind not in {"project", "repository"}:
                errors.append(f"{record_id}: workspace_slug requires record_kind 'project' or 'repository'")
            if workspace_home is None and record_kind != "project":
                errors.append(f"{record_id}: workspace_slug requires workspace_home")
            if isinstance(workspace_home, str) and isinstance(workspace_slug, str):
                portable_destinations.append((f"{workspace_home}/{workspace_slug}", record_id))
        if default_branch is not None:
            invalid_branch = (
                not isinstance(default_branch, str)
                or not default_branch
                or len(default_branch) > 240
                or default_branch.startswith("-")
                or default_branch.endswith(("/", ".", ".lock"))
                or any(token in default_branch for token in ("..", "//", "@{"))
                or any(char.isspace() or ord(char) < 32 for char in default_branch)
                or any(char in default_branch for char in "~^:?*[\\")
            )
            if invalid_branch:
                errors.append(f"{record_id}: default_branch must be a valid branch name")

        repository_governance = record.get("repository_governance")
        if repository_governance is not None:
            if not isinstance(repository_governance, dict):
                errors.append(f"{record_id}: repository_governance must be an object")
            else:
                owner_class = repository_governance.get("owner_class")
                remote_owners = repository_governance.get("approved_remote_owners")
                mutation_authority = repository_governance.get("mutation_authority")
                publication_authority = repository_governance.get("publication_authority")
                review = repository_governance.get("review")
                if owner_class not in ALLOWED_REPOSITORY_OWNER_CLASSES:
                    errors.append(f"{record_id}: unknown repository_governance.owner_class {owner_class!r}")
                if not isinstance(remote_owners, list) or not all(
                    isinstance(owner, str) and owner.strip() for owner in remote_owners
                ):
                    errors.append(
                        f"{record_id}: repository_governance.approved_remote_owners must be a list of non-empty strings"
                    )
                if mutation_authority not in ALLOWED_MUTATION_AUTHORITIES:
                    errors.append(
                        f"{record_id}: unknown repository_governance.mutation_authority {mutation_authority!r}"
                    )
                if publication_authority not in ALLOWED_PUBLICATION_AUTHORITIES:
                    errors.append(
                        f"{record_id}: unknown repository_governance.publication_authority {publication_authority!r}"
                    )
                if owner_class != "brian" and mutation_authority == "normal_push":
                    errors.append(
                        f"{record_id}: normal_push requires repository_governance.owner_class 'brian'"
                    )
                if not isinstance(review, dict):
                    errors.append(f"{record_id}: repository_governance.review must be an object")
                else:
                    reviewed_by = review.get("reviewed_by")
                    reviewed_at = review.get("reviewed_at")
                    evidence = review.get("evidence")
                    if not isinstance(reviewed_by, str) or not reviewed_by.strip():
                        errors.append(
                            f"{record_id}: repository_governance.review.reviewed_by must be a non-empty string"
                        )
                    if not isinstance(reviewed_at, str):
                        errors.append(
                            f"{record_id}: repository_governance.review.reviewed_at must be an ISO date"
                        )
                    else:
                        try:
                            parsed_reviewed_at = date.fromisoformat(reviewed_at)
                        except ValueError:
                            errors.append(
                                f"{record_id}: repository_governance.review.reviewed_at must be an ISO date"
                            )
                        else:
                            if parsed_reviewed_at.isoformat() != reviewed_at:
                                errors.append(
                                    f"{record_id}: repository_governance.review.reviewed_at must be an ISO date"
                                )
                    if not isinstance(evidence, list) or not evidence or not all(
                        isinstance(item, str) and item.strip() for item in evidence
                    ):
                        errors.append(
                            f"{record_id}: repository_governance.review.evidence must be a non-empty list of non-empty strings"
                        )

        repository_topology = record.get("repository_topology")
        if repository_topology is not None:
            if not isinstance(repository_topology, dict):
                errors.append(f"{record_id}: repository_topology must be an object")
            else:
                for field in sorted(set(repository_topology) - {"mode"}):
                    errors.append(f"{record_id}: unknown repository_topology.{field}")
                topology_mode = repository_topology.get("mode")
                if topology_mode not in ALLOWED_REPOSITORY_TOPOLOGY_MODES:
                    errors.append(
                        f"{record_id}: unknown repository_topology.mode {topology_mode!r}"
                    )

        portfolio_tier = record.get("portfolio_tier")
        if portfolio_tier is not None and portfolio_tier not in ALLOWED_PORTFOLIO_TIERS:
            errors.append(f"{record_id}: unknown portfolio_tier {portfolio_tier!r}")

        branch_policy = record.get("branch_policy")
        if branch_policy is not None:
            if not isinstance(branch_policy, dict):
                errors.append(f"{record_id}: branch_policy must be an object")
            else:
                for scope, exception in branch_policy.items():
                    if scope not in BRANCH_POLICY_SCOPES:
                        errors.append(f"{record_id}: unknown branch_policy scope {scope!r}")
                        continue
                    if not isinstance(exception, dict):
                        errors.append(f"{record_id}: branch_policy.{scope} must be an object")
                        continue
                    branch = exception.get("branch")
                    reason = exception.get("reason")
                    if not isinstance(branch, str) or not branch.strip():
                        errors.append(f"{record_id}: branch_policy.{scope}.branch must be non-empty")
                    if not isinstance(reason, str) or not reason.strip():
                        errors.append(f"{record_id}: branch_policy.{scope}.reason must be non-empty")

        utility_tags = record.get("utility_tags")
        if not isinstance(utility_tags, list) or not utility_tags:
            errors.append(f"{record_id}: utility_tags must be a non-empty list")
        else:
            expected = {f"area:{area}", f"status:{status}"}
            actual = {tag for tag in utility_tags if isinstance(tag, str)}
            missing = sorted(expected - actual)
            if missing:
                errors.append(f"{record_id}: utility_tags missing {', '.join(missing)}")

        for list_field in ["domains", "tech", "capabilities", "tags", "depends_on", "supersedes"]:
            value = record.get(list_field)
            if not isinstance(value, list):
                errors.append(f"{record_id}: {list_field} must be a list")

        # Dangling relation checks
        depends_on = record.get("depends_on")
        if isinstance(depends_on, list):
            for ref in depends_on:
                if isinstance(ref, str) and ref.strip() and ref not in valid_ids:
                    errors.append(f"{record_id}: depends_on references unknown id {ref!r}")

        supersedes_list = record.get("supersedes")
        if isinstance(supersedes_list, list):
            for ref in supersedes_list:
                if isinstance(ref, str) and ref.strip() and ref not in valid_ids:
                    errors.append(f"{record_id}: supersedes references unknown id {ref!r}")

        superseded_by = record.get("superseded_by")
        if superseded_by is not None:
            if not isinstance(superseded_by, str):
                errors.append(f"{record_id}: superseded_by must be a string or null")
            elif superseded_by.strip() and superseded_by not in valid_ids:
                errors.append(f"{record_id}: superseded_by references unknown id {superseded_by!r}")

        # Sparse-record checks for active/dormant/complete
        if status in SPARSE_CHECK_STATUSES:
            tags_val = record.get("tags")
            caps_val = record.get("capabilities")
            is_exempt = (
                record.get("minimal_record_ok") is True
                or (
                    isinstance(tags_val, list)
                    and "minimal-record-ok" in tags_val
                )
            )
            if not is_exempt:
                if isinstance(caps_val, list) and len(caps_val) < MIN_CAPABILITIES:
                    errors.append(
                        f"{record_id}: active/dormant/complete record has only {len(caps_val)} "
                        f"capabilities (need {MIN_CAPABILITIES}); add minimal-record-ok tag to exempt"
                    )
                if isinstance(tags_val, list) and len(tags_val) < MIN_TAGS:
                    errors.append(
                        f"{record_id}: active/dormant/complete record has only {len(tags_val)} "
                        f"tags (need {MIN_TAGS}); add minimal-record-ok tag to exempt"
                    )
                if isinstance(one_liner, str) and one_liner.strip() and len(one_liner) < MIN_ONE_LINER_LENGTH:
                    errors.append(
                        f"{record_id}: active/dormant/complete record one_liner is {len(one_liner)} chars "
                        f"(need {MIN_ONE_LINER_LENGTH}+); add minimal-record-ok tag to exempt"
                    )

    for duplicate_path, count in Counter(existing_paths).items():
        if count > 1:
            errors.append(f"duplicate existing path: {duplicate_path}")

    destination_counts = Counter(destination for destination, _ in portable_destinations)
    for destination, count in sorted(destination_counts.items()):
        if count > 1:
            record_ids = sorted(
                record_id for value, record_id in portable_destinations if value == destination
            )
            errors.append(
                f"duplicate portable destination: {destination} ({', '.join(record_ids)})"
            )

    return errors


def absent_local_paths(records: list) -> list:
    """Records naming a path that does not exist on this machine.

    Never an error. ADR-2026-08-12 point 5: presence on one device is not
    lifecycle authority, so a repository simply not cloned here is normal. It is
    still worth printing, because the same signal covers the case that is a real
    defect -- a path the index still claims after the checkout was moved or
    deleted -- and nothing else surfaced it. Eight such records accumulated
    undetected before this was added.
    """
    absent = []
    for record in records:
        path = record.get("path")
        if not isinstance(path, str) or not path.strip():
            continue
        if not os.path.exists(os.path.expanduser(path)):
            absent.append((str(record.get("id")), path))
    return sorted(absent)


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-graph",
        default=GRAPH_DEFAULT,
        help=f"Path to PROJECT_GRAPH.json (default: $PROJECT_GRAPH, else {GRAPH_DEFAULT})",
    )
    parser.add_argument(
        "--fail-on",
        choices=("all", "hard"),
        default="all",
        help=(
            "Which finding class should make the command fail. "
            "`all` preserves the full taxonomy gate; `hard` fails only on "
            "deterministic structural errors and leaves descriptive taxonomy "
            "readiness measured/report-only."
        ),
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    try:
        records = load_records(Path(args.project_graph))
        errors = validate_records(records)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
        records = []

    hard_errors = [error for error in errors if is_hard_error(error)]
    measured_errors = [error for error in errors if not is_hard_error(error)]
    blocking_errors = errors if args.fail_on == "all" else hard_errors

    if args.json:
        print(
            json.dumps(
                {
                    "ok": not errors,
                    "blocking_ok": not blocking_errors,
                    "fail_on": args.fail_on,
                    "records": len(records),
                    "errors": errors,
                    "hard_errors": hard_errors,
                    "measured_errors": measured_errors,
                },
                indent=2,
            )
        )
    else:
        print(f"Validated {len(records)} project graph taxonomy records")
        print(f"Errors: {len(errors)}")
        if args.fail_on == "hard":
            print(f"Blocking hard errors: {len(hard_errors)}")
            print(f"Measured non-blocking findings: {len(measured_errors)}")
            if hard_errors:
                print("\n[BLOCKING ERRORS]")
                for error in hard_errors:
                    print(f"- {error}")
            if measured_errors:
                print("\nMeasured taxonomy readiness findings are report-only here.")
                print("Run `python scripts/check_project_graph_taxonomy.py --project-graph PROJECT_GRAPH.json` for details.")
        elif errors:
            print("\n[ERRORS]")
            for error in errors:
                print(f"- {error}")

        absent = absent_local_paths(records)
        if absent:
            print(f"\n[PATHS ABSENT ON THIS MACHINE: {len(absent)}] (not errors)")
            for record_id, path in absent:
                print(f"- {record_id}: {path}")
            print("Expected for repositories not cloned here. Investigate any you "
                  "believe should be present: the index may be naming a stale path.")

    return 1 if blocking_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
