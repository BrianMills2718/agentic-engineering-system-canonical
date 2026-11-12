"""Turn the LikeC4 diagram into import-linter contracts, and check the committed ones are current.

Implements: lockstep-checks/arch-diagram-becomes-import-contracts, lockstep-checks/arch-committed-contracts-match-the-diagram

Requirement text (generated):
    lockstep-checks/arch-diagram-becomes-import-contracts: `lockstep check arch gen` SHALL write one import-linter
        forbidden contract per diagram element that has `python` metadata, forbidding direct imports
        of every other mapped element it has no relation to. When LikeC4 reports the diagram
        invalid, it SHALL stop with LikeC4's errors and write no contracts.
    lockstep-checks/arch-committed-contracts-match-the-diagram: `lockstep check arch check` SHALL exit 1 when the
        committed contracts file differs from what the current diagram generates.
"""

import json
from pathlib import Path
import subprocess
import tempfile

LIKEC4 = "likec4@1.60.0"
CONTRACTS = ".importlinter"
HEADER = "# Generated from docs/architecture/*.c4 by `lockstep check arch gen`. Do not edit by hand.\n"


class DiagramInvalid(RuntimeError):
    """LikeC4 could not parse the diagram; its report is the message."""


def export_model(root: Path, likec4: str = LIKEC4) -> dict:
    """Export the LikeC4 model under docs/architecture as JSON.

    `likec4 export` exits 0 on a diagram it cannot parse and writes only what it parsed before the
    error, so the diagram is validated first.

    Args:
        root: Repository root.
        likec4: The pinned `likec4@<version>` package run through npx.

    Returns:
        The parsed LikeC4 JSON export.

    Raises:
        DiagramInvalid: LikeC4 reports the diagram invalid.
    """
    arch = str(root / "docs/architecture")
    checked = subprocess.run(["npx", "--yes", likec4, "validate", arch], capture_output=True, text=True)
    if checked.returncode != 0:
        raise DiagramInvalid(f"LikeC4 reports {arch} Invalid:\n{checked.stdout}{checked.stderr}")
    with tempfile.TemporaryDirectory() as out:
        subprocess.run(
            ["npx", "--yes", likec4, "export", "json", "-o", f"{out}/model.json", str(root / "docs/architecture")],
            check=True,
            capture_output=True,
        )
        return json.loads(Path(out, "model.json").read_text())


def contracts_from_model(model: dict) -> dict[str, list[str]]:
    """Map each Python-mapped element's module to the modules it may not import.

    An element may import another mapped element only when the diagram has a relation from it to that
    element. Elements without `python` metadata are ignored.

    Args:
        model: A LikeC4 JSON export.

    Returns:
        Module name to the sorted modules it is forbidden to import.
    """
    module = {
        eid: el["metadata"]["python"]
        for eid, el in model["elements"].items()
        if isinstance(el.get("metadata"), dict) and "python" in el["metadata"]
    }
    allowed = {(r["source"]["model"], r["target"]["model"]) for r in model["relations"].values()}
    return {
        module[a]: sorted(module[b] for b in module if b != a and (a, b) not in allowed)
        for a in sorted(module, key=lambda eid: module[eid])
    }


def render(forbidden: dict[str, list[str]], root: str | None = None) -> str:
    """Write the contracts as an import-linter INI file.

    Args:
        forbidden: Output of `contracts_from_model`.
        root: Root package; defaults to the first segment of every mapped module.

    Returns:
        The file text.
    """
    roots = [root] if root else sorted({m.split(".")[0] for m in forbidden})
    lines = [HEADER, "[importlinter]", "root_packages =", *[f"    {r}" for r in roots], ""]
    for source, targets in forbidden.items():
        if not targets:
            continue
        lines += [
            f"[importlinter:contract:{source}]",
            f"name = {source} imports only what the diagram allows",
            "type = forbidden",
            f"source_modules = {source}",
            "forbidden_modules =",
            *[f"    {t}" for t in targets],
            "allow_indirect_imports = True",
            "",
        ]
    return "\n".join(lines)


def generate(root: Path, likec4: str = LIKEC4) -> str:
    """Build the contracts file text from the repository's current diagram.

    Args:
        root: Repository root.
        likec4: The pinned `likec4@<version>` package.

    Returns:
        The file text `arch gen` writes.
    """
    return render(contracts_from_model(export_model(root, likec4)))
