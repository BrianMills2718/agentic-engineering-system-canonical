from __future__ import annotations

import re
import tomllib

from .git_source import GitSource
from .models import AuthorityRole, AuthoritySurfaceObservation, ConcernRootObservation, EpistemicState, EvidenceRef


ROOT_DOCS = ("README.md", "CLAUDE.md", "AGENTS.md")
LOCAL_WIKI_REFERENCE = re.compile(r"(?:\]\(|[`'\"])(?:\./)?wiki/index\.md(?:[)`'\"]|$)")


def _evidence(source: GitSource, path: str, note: str) -> EvidenceRef:
    return EvidenceRef(
        evidence_id=f"{source.revision[:12]}:{path}",
        repository_id=source.repository_id,
        revision=source.revision,
        path=path,
        source_url=source.source_url(path),
        note=note,
    )


def _normalize_package_name(name: str) -> str:
    return re.sub(r"[-.]+", "_", name.strip())


def _contract_ownership_is_explicit(text: str, project_name: str, package_name: str) -> bool:
    lowered = text.lower()
    subjects = {project_name.lower(), package_name.lower()}
    owns_language = " owns" in lowered or "ownership" in lowered or "source of record" in lowered
    return "contract" in lowered and owns_language and any(subject in lowered for subject in subjects)


class LegacyRepositoryAdapter:
    """Resolve only explicit, bounded repository evidence; never infer authority from names."""

    def __init__(self, source: GitSource):
        self.source = source

    def _root_docs(self) -> list[tuple[str, str]]:
        result = []
        for path in ROOT_DOCS:
            if self.source.exists(path):
                result.append((path, self.source.read_text(path)))
        return result

    def _package_metadata(self) -> tuple[str | None, str | None, EvidenceRef | None]:
        if not self.source.exists("pyproject.toml"):
            return None, None, None
        text = self.source.read_text("pyproject.toml")
        try:
            value = tomllib.loads(text)
        except tomllib.TOMLDecodeError:
            return None, None, None

        project = value.get("project")
        project_name: str | None = None
        if isinstance(project, dict):
            candidate_name = project.get("name")
            if isinstance(candidate_name, str) and candidate_name.strip():
                project_name = candidate_name

        tool = value.get("tool")
        setuptools = tool.get("setuptools", {}) if isinstance(tool, dict) else {}
        if not isinstance(setuptools, dict):
            setuptools = {}
        packages = setuptools.get("packages", {})
        find = packages.get("find", {}) if isinstance(packages, dict) else {}
        where = find.get("where") if isinstance(find, dict) else None
        source_root: str | None = None
        if isinstance(where, list) and where and isinstance(where[0], str) and where[0]:
            source_root = where[0].rstrip("/")
        if source_root is None:
            package_dir = setuptools.get("package-dir")
            if isinstance(package_dir, dict):
                candidate = package_dir.get("")
                if isinstance(candidate, str) and candidate:
                    source_root = candidate.rstrip("/")
        package_evidence = _evidence(self.source, "pyproject.toml", "packaging metadata")
        if source_root is None:
            return project_name, None, package_evidence

        root_path = f"{source_root}/"
        package_path: str | None = root_path if self.source.exists(root_path) else None
        if project_name is not None:
            package_name = _normalize_package_name(project_name)
            candidate_path = f"{source_root}/{package_name}/"
            if self.source.exists(candidate_path):
                package_path = candidate_path
        return project_name, package_path, package_evidence

    def navigation(self) -> tuple[AuthoritySurfaceObservation, list[EvidenceRef]]:
        docs = self._root_docs()
        if not docs:
            return AuthoritySurfaceObservation(
                role=AuthorityRole.NAVIGATION,
                state=EpistemicState.NONE,
                summary="No bounded root navigation document was observed.",
            ), []
        path, _ = docs[0]
        ev = _evidence(self.source, path, "root navigation/context document")
        return AuthoritySurfaceObservation(
            role=AuthorityRole.NAVIGATION,
            state=EpistemicState.OBSERVED,
            locations=(path,),
            summary=f"Repository-local entrypoint is {path}.",
            evidence_refs=(ev.evidence_id,),
        ), [ev]

    def authorities(self) -> tuple[list[AuthoritySurfaceObservation], list[ConcernRootObservation], list[EvidenceRef]]:
        observations: list[AuthoritySurfaceObservation] = []
        concerns: list[ConcernRootObservation] = []
        evidence: list[EvidenceRef] = []
        docs = self._root_docs()
        joined = "\n".join(text for _, text in docs)

        project_name, package_path, package_evidence = self._package_metadata()
        if package_path is not None and package_evidence is not None:
            evidence.append(package_evidence)
            observations.append(AuthoritySurfaceObservation(
                role=AuthorityRole.IMPLEMENTATION,
                state=EpistemicState.OBSERVED,
                locations=(package_path,),
                summary="Packaging metadata positively identifies the implementation package root.",
                evidence_refs=(package_evidence.evidence_id,),
            ))

        capability_path: str | None = None
        capability_evidence: EvidenceRef | None = None
        capability_text: str | None = None
        cap_match = re.search(r"(?:\]\()?((?:docs/ops/)?CAPABILITY_DECOMPOSITION\.md)", joined)
        if cap_match and self.source.exists(cap_match.group(1)):
            capability_path = cap_match.group(1)
            capability_text = self.source.read_text(capability_path)
            capability_evidence = _evidence(
                self.source,
                capability_path,
                "directly referenced capability-ownership document",
            )
            evidence.append(capability_evidence)
            observations.append(AuthoritySurfaceObservation(
                role=AuthorityRole.OWNERSHIP,
                state=EpistemicState.OBSERVED,
                locations=(capability_path,),
                summary="Root context directly routes capability ownership to this document.",
                evidence_refs=(capability_evidence.evidence_id,),
            ))

        if (
            project_name is not None
            and package_path is not None
            and package_evidence is not None
            and capability_text is not None
            and capability_evidence is not None
            and _contract_ownership_is_explicit(
                capability_text,
                project_name,
                _normalize_package_name(project_name),
            )
        ):
            observations.append(AuthoritySurfaceObservation(
                role=AuthorityRole.CONTRACT,
                state=EpistemicState.OBSERVED,
                locations=(package_path,),
                summary="Packaging metadata plus the directly referenced ownership source identify this package as a contract authority surface.",
                evidence_refs=(package_evidence.evidence_id, capability_evidence.evidence_id),
            ))

        local_wiki_ref: tuple[str, str] | None = None
        for path, text in docs:
            if LOCAL_WIKI_REFERENCE.search(text):
                local_wiki_ref = (path, text)
                break
        if local_wiki_ref is None:
            concerns.append(ConcernRootObservation(
                concern="wiki-navigation",
                state=EpistemicState.NONE,
                path=None,
                evidence_refs=(),
            ))
        else:
            ref_path, _ = local_wiki_ref
            ref_evidence = _evidence(self.source, ref_path, "root context explicitly references local wiki navigation")
            evidence.append(ref_evidence)
            if self.source.exists("wiki/index.md"):
                concerns.append(ConcernRootObservation(
                    concern="wiki-navigation",
                    state=EpistemicState.OBSERVED,
                    path="wiki/index.md",
                    evidence_refs=(ref_evidence.evidence_id,),
                ))
            else:
                concerns.append(ConcernRootObservation(
                    concern="wiki-navigation",
                    state=EpistemicState.UNRESOLVED,
                    path="wiki/index.md",
                    evidence_refs=(ref_evidence.evidence_id,),
                ))

        # A directory named contracts/ is deliberately recorded only as a warning,
        # never promoted to authority by existence alone.
        if self.source.exists("contracts"):
            concerns.append(ConcernRootObservation(
                concern="contracts-root",
                state=EpistemicState.NONE,
                path="contracts/",
                evidence_refs=(),
            ))

        return observations, concerns, evidence
