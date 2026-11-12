"""Show what one source file must keep true: the requirements its docstrings implement, with their text and scenarios.

Implements: lockstep-projection/show-prints-what-a-file-must-keep-true

Requirement text (generated):
    lockstep-projection/show-prints-what-a-file-must-keep-true: `lockstep show FILE` SHALL print
        each requirement the file's docstrings implement, with its text, its scenarios and their
        status.

"""

from pathlib import Path

from lockstep.checks.markers import implementers
from lockstep.checks.spec import read_plan
from lockstep.checks.status import report


def show(root: Path, file: Path | str) -> str:
    """Return the requirements a file implements, each with its text, symbols, scenarios and state.

    Args:
        root: Repository root.
        file: The source file, absolute or relative to root.

    Returns:
        The text to print; empty when the file implements no requirement.
    """
    root = root.resolve()
    path = Path(file) if Path(file).is_absolute() else root / file
    rel = str(path.resolve().relative_to(root))
    symbols: dict[str, list[str]] = {}
    for ident, _, symbol in implementers(root, only=path.resolve()):
        symbols.setdefault(ident, []).append(symbol)
    if not symbols:
        return ""
    result = report(root)
    text = {**read_plan(root).text, **read_plan(root, changes=True).text}
    lines = [f"{rel} implements {len(symbols)} requirement(s); test results: {result.results_note}"]
    for ident, syms in symbols.items():
        row = result.requirements.get(ident)
        lines.append(f"{ident} [{row.state if row else 'unknown ID'}] in {', '.join(syms)}")
        if ident in text:
            lines.append(f"    {text[ident]}")
        for sid, sc in result.scenarios.items():
            if sc.requirement == ident:
                lines.append(f"    scenario {sid} [{sc.state}]: {', '.join(sc.links) or 'no tests'}")
    return "\n".join(lines) + "\n"
