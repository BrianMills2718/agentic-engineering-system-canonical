from __future__ import annotations

import re
from pathlib import Path

from .git_source import GitSource
from .models import AuthorityRole, AuthoritySurfaceObservation, ConcernRootObservation, EpistemicState, EvidenceRef


ROOT_DOCS = ("README.md", "CLAUDE.md", "AGENTS.md")


def _evidence(source: GitSource, path: str, note: str) -> EvidenceRef:
    return EvidenceRef(
        evidence_id=f"{source.revision[:12]}:{path}",
        repository_id=source.repository_id,
        revision=source.revision,
        path=path,
        source_url=source.source_url(path),
        note=note,
    )


class LegacyRepositoryAdapter:
    """Resolve only explicit, bounded repository evidence; never infer authority from names."""

    def __init__(self, source: GitSource):
        self.source = source
        self.evidence: list[EvidenceRef] = []

    def _root_docs(self) -> list[tuple[str, str]]:
        result = []
        for path in ROOT_DOCS:
            if self.source.exists(path):
                result.append((path, self.source.read_text(path)))
        return result

    def navigation(self) -> tuple[AuthoritySurfaceObservation, list[EvidenceRef]]:
        docs = self._root_docs()
        if not docs:
            return AuthoritySurfaceObservation(
                role=AuthorityRole.NAVIGATION,
                state=EpistemicState.NONE,
                summary="No bounded root navigation document was observed.",
            ), []
        path, text = docs[0]
        ev = _evidence(self.source, path, "root navigation/context document")
        self.evidence.append(ev)
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

        if self.source.exists("pyproject.toml"):
            ev = _evidence(self.source, "pyproject.toml", "packaging metadata")
            evidence.append(ev)
            text = self.source.read_text("pyproject.toml")
            if re.search(r"where\s*=\s*\[\s*[\"']src[\"']\s*\]", text):
                observations.append(AuthoritySurfaceObservation(
                    role=AuthorityRole.IMPLEMENTATION,
                    state=EpistemicState.OBSERVED,
                    locations=("src/",),
                    summary="Packaging metadata explicitly identifies src/ as the package root.",
                    evidence_refs=(ev.evidence_id,),
                ))

        cap_match = re.search(r"(?:\]\()?((?:docs/ops/)?CAPABILITY_DECOMPOSITION\.md)", joined)
        if cap_match and self.source.exists(cap_match.group(1)):
            path = cap_match.group(1)
            ev = _evidence(self.source, path, "directly referenced capability-ownership document")
            evidence.append(ev)
            observations.append(AuthoritySurfaceObservation(
                role=AuthorityRole.OWNERSHIP,
                state=EpistemicState.OBSERVED,
                locations=(path,),
                summary="Root context directly routes capability ownership to this document.",
                evidence_refs=(ev.evidence_id,),
            ))

        wiki = "wiki/index.md"
        if self.source.exists(wiki):
            ev = _evidence(self.source, wiki, "existing local wiki entrypoint")
            evidence.append(ev)
            observations.append(AuthoritySurfaceObservation(
                role=AuthorityRole.NAVIGATION,
                state=EpistemicState.OBSERVED,
                locations=(wiki,),
                summary="A repository-local wiki entrypoint exists.",
                evidence_refs=(ev.evidence_id,),
            ))
        else:
            concerns.append(ConcernRootObservation(
                concern="wiki",
                state=EpistemicState.NONE,
                path=None,
                evidence_refs=(),
            ))

        # A directory named contracts/ is deliberately recorded only as a warning.
        if self.source.exists("contracts") or (self.source.repo / "contracts").is_dir():
            concerns.append(ConcernRootObservation(
                concern="contracts-root",
                state=EpistemicState.NONE,
                path="contracts/",
                evidence_refs=(),
            ))

        return observations, concerns, evidence
