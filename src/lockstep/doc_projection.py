"""Project declared source-local facts into Markdown; never execute source or repository code.

Implements: lockstep-doc-facts/declared-source-facts-have-one-authority,
    lockstep-doc-facts/invalid-input-is-not-a-pass,
    lockstep-doc-facts/installed-edit-and-merge-paths-maintain-facts

Requirement text (generated):
    lockstep-doc-facts/declared-source-facts-have-one-authority: `lockstep check project` SHALL
        generate Markdown fact blocks declared by `projections` in `lockstep.yaml`, each with id,
        source, target and fields, with an optional Python symbol. It SHALL read Markdown YAML front
        matter, JSON/YAML mapping fields and Python AST descriptions and signatures without
        importing or executing source. `--check` SHALL report stale target paths and exit 1 without
        writing. Generation SHALL preserve unrelated target content, include a relative source link
        (or an HTTP(S) source_base_url link when configured), escape HTML and table delimiters in
        projected scalar values, and remain idempotent. Consumers with no recognized OpenSpec
        requirement text SHALL project only declared facts, without creating an empty coverage page
        or rewriting historical plans.
    lockstep-doc-facts/invalid-input-is-not-a-pass: Projection SHALL reject missing sources or
        fields, invalid or duplicate marker pairs and paths escaping the repository, including
        symlinks. It SHALL validate all declared fact projections before any projection write and
        report invalid input with exit 2. Targets SHALL NOT also be sources.
    lockstep-doc-facts/installed-edit-and-merge-paths-maintain-facts: `lockstep refresh` SHALL
        refresh only declared source-local fact blocks without regenerating requirement docstrings
        or coverage. `lockstep init` SHALL install it as a PostToolUse hook for Claude Code and
        Codex while preserving existing hooks. It SHALL include `lockstep check project --check` in
        the pre-commit command so edits bypassing hooks are still checked. Refresh SHALL append one
        trace per run to a daily projection log with source/target hashes and rewritten paths. No
        declarations SHALL be a no-op.


Current assessment (agent-authored):
    Static source extraction, declared target fan-out, refresh traces and read-only
    comparison are implemented. AES declares this module as the source for its
    architecture and wiki assessment blocks. This narrative is an assessment,
    not a substitute for measured test or native-host evidence.

Gap G-NATIVE:
    Closed for the retained API-authenticated Claude path: one native Edit
    invoked the installed hook and refreshed both targets. Codex host execution
    and blanket default-session loading remain unobserved.

Plan P-NATIVE (addresses G-NATIVE):
    Completed for the retained Claude path: host transcript and trace identify
    one source Edit and both target writes; bypass refusal and recovery passed.

Gap G-CONCISE:
    The first adoption projects the full docstring; a compact wiki narrative and
    typed gap/plan relationship validation remain separate improvements.

Evidence:
    See evidence/runs/projection-worked-20261113.json for the earlier disposable
    CLI example. See evidence/runs/projection-self-adoption-20261113.json and
    evidence/runs/projection-native-20261113.jsonl for the bounded native run.

Native edit marker: observed-host-edit
"""
from __future__ import annotations

import argparse
import ast
from datetime import date, datetime, timezone
import hashlib
from html import escape
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from urllib.parse import quote, urlsplit

import yaml


class ProjectionError(ValueError):
    """A declared source or target cannot be projected; never silently skip it."""


def _path(root: Path, value: object) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '..' in Path(value).parts:
        raise ProjectionError(f'projection path must be repository-relative without traversal: {value!r}')
    path = root/value
    if not path.resolve().is_relative_to(root.resolve()):
        raise ProjectionError(f'projection path escapes repository: {value}')
    if not path.is_file():
        raise ProjectionError(f'projection file does not exist: {value}')
    return path


def declarations(root: Path) -> list[dict]:
    """Read the optional projections list from the existing Lockstep configuration."""
    config = root/'lockstep.yaml'
    if not config.is_file():
        return []
    data = yaml.safe_load(config.read_text()) or {}
    if not isinstance(data, dict):
        raise ProjectionError('lockstep.yaml must hold a mapping')
    rows = data.get('projections', [])
    if not isinstance(rows, list):
        raise ProjectionError('projections must be a list')
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row)-{'id', 'source', 'target', 'fields', 'symbol'}:
            raise ProjectionError('each projection holds only id, source, target, fields and optional symbol')
        ident = row.get('id')
        if not isinstance(ident, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', ident) or ident in seen:
            raise ProjectionError(f'projection id is invalid or repeated: {ident!r}')
        seen.add(ident)
        _path(root, row.get('source'))
        _path(root, row.get('target'))
        if row['source'] == row['target']:
            raise ProjectionError(f'projection {ident}: source and target must differ')
        fields = row.get('fields')
        if not isinstance(fields, list) or not fields or any(not isinstance(f, str) or not f for f in fields) or len(set(fields)) != len(fields):
            raise ProjectionError(f'projection {ident}: fields must be distinct nonempty names')
        symbol = row.get('symbol')
        if symbol is not None and (not isinstance(symbol, str) or not symbol):
            raise ProjectionError(f'projection {ident}: symbol must be a nonempty name')
    return rows


def _symbol(tree: ast.AST, name: str | None) -> ast.AST:
    node = tree
    for part in name.split('.') if name else []:
        found = [n for n in getattr(node, 'body', [])
                 if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == part]
        if len(found) != 1:
            raise ProjectionError(f'Python symbol is missing or ambiguous: {name}')
        node = found[0]
    return node


def _facts(path: Path, fields: list[str], symbol: str | None, text: str | None = None) -> dict:
    text = path.read_text() if text is None else text
    if path.suffix == '.py':
        node = _symbol(ast.parse(text, filename=str(path)), symbol)
        description = ast.get_docstring(node) or ''  # type: ignore[arg-type]
        data: dict = {'description': description.split('\n\n', 1)[0], 'docstring': description} if description else {}
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            prefix = 'async ' if isinstance(node, ast.AsyncFunctionDef) else ''
            returns = f' -> {ast.unparse(node.returns)}' if node.returns else ''
            data['signature'] = f'{prefix}{node.name}({ast.unparse(node.args)}){returns}'
        elif isinstance(node, ast.ClassDef):
            data['signature'] = f'class {node.name}(' + ', '.join(ast.unparse(b) for b in [*node.bases, *node.keywords]) + ')'
    else:
        if symbol is not None:
            raise ProjectionError(f'symbol applies only to Python: {path.name}')
        if path.suffix.lower() == '.md':
            lines = text.splitlines()
            if not lines or lines[0] != '---':
                raise ProjectionError(f'Markdown source needs YAML front matter: {path.name}')
            try:
                end = lines.index('---', 1)
            except ValueError as exc:
                raise ProjectionError(f'unclosed YAML front matter: {path.name}') from exc
            data = yaml.safe_load('\n'.join(lines[1:end])) or {}
        elif path.suffix.lower() == '.json':
            data = json.loads(text)
        elif path.suffix.lower() in ('.yaml', '.yml'):
            data = yaml.safe_load(text) or {}
        else:
            raise ProjectionError(f'unsupported projection source: {path.name}')
        if not isinstance(data, dict):
            raise ProjectionError(f'projection source must hold a mapping: {path.name}')
    missing = [f for f in fields if f not in data or data[f] is None]
    if missing:
        raise ProjectionError(f'{path.name}: missing source field(s): {", ".join(missing)}')
    return {f: data[f] for f in fields}


def _json_default(value: object) -> str:
    if isinstance(value, date):
        return value.isoformat()
    raise ProjectionError(f'unsupported source field type: {type(value).__name__}')


def _cell(value: object) -> str:
    if not isinstance(value, str):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True, default=_json_default)
    return escape(value, quote=False).replace('|', '&#124;').replace('\r\n', '\n').replace('\n', '<br>')


def render(root: Path, contents: dict[Path, str] | None = None) -> dict[Path, str]:
    """Compose facts with already rendered contents, validating all inputs before writes."""
    rows = declarations(root)
    config = root/'lockstep.yaml'
    data = yaml.safe_load(config.read_text()) if config.is_file() else {}
    base = (data or {}).get('source_base_url')
    if base is not None:
        if not isinstance(base, str):
            raise ProjectionError('source_base_url must be an HTTP(S) base URL')
        parsed = urlsplit(base)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ProjectionError('source_base_url must be an HTTP(S) base URL without credentials, query or fragment')
    sources = {_path(root, row['source']).resolve() for row in rows}
    if any(_path(root, row['target']).resolve() in sources for row in rows):
        raise ProjectionError('a projection target cannot also be a projection source')
    rendered: dict[Path, str] = dict(contents or {})
    for row in rows:
        source, target = _path(root, row['source']), _path(root, row['target'])
        ident = row['id']
        start, end = f'<!-- lockstep facts: {ident} -->', f'<!-- /lockstep facts: {ident} -->'
        text = rendered.get(target, target.read_text())
        if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
            raise ProjectionError(f'{row["target"]}: projection {ident} needs exactly one ordered marker pair')
        # Markers are syntax, not prose interpretation. Nested generated blocks are invalid.
        middle = text[text.index(start)+len(start):text.index(end)]
        if '<!-- lockstep facts:' in middle or '<!-- /lockstep facts:' in middle:
            raise ProjectionError(f'{row["target"]}: nested projection markers')
        facts = _facts(source, row['fields'], row.get('symbol'), rendered.get(source))
        link = base.rstrip('/') + '/' + quote(row['source'], safe='/') if base else quote(os.path.relpath(source, target.parent).replace(os.sep, '/'), safe='/.')
        block = [start, '', f'Generated from [{row["source"]}]({link}); edit the source, not this block.', '',
                 '| Field | Value |', '| --- | --- |']
        block += [f'| {_cell(f)} | {_cell(value)} |' for f, value in facts.items()]
        new = '\n'.join(block)+f'\n\n{end}'
        rendered[target] = text[:text.index(start)] + new + text[text.index(end)+len(end):]
    return rendered


def project_facts(root: Path, check: bool = False, rendered: dict[Path, str] | None = None) -> list[str]:
    """Bring declared fact blocks up to date or return stale paths without writing."""
    contents = render(root) if rendered is None else rendered
    changed = []
    for path, text in contents.items():
        if not path.exists() or path.read_text() != text:
            changed.append(path.relative_to(root).as_posix())
            if not check:
                mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
                with tempfile.NamedTemporaryFile('w', dir=path.parent, prefix='.lockstep-', delete=False) as f:
                    f.write(text)
                    temporary = f.name
                os.chmod(temporary, mode)
                os.replace(temporary, path)
    return changed


def _root(start: Path) -> Path | None:
    start = start.resolve()
    return next((p for p in (start, *start.parents) if (p/'lockstep.yaml').is_file()), None)


def _trace_path(root: Path) -> Path:
    folder = root/'.lockstep'
    trace = folder/f'projection-{datetime.now(timezone.utc):%Y-%m-%d}.jsonl'
    if not folder.resolve().is_relative_to(root) or not trace.resolve().is_relative_to(root):
        raise ProjectionError('projection trace path escapes repository')
    return trace


def _append_trace(root: Path, event: dict) -> None:
    trace = _trace_path(root)
    trace.parent.mkdir(exist_ok=True)
    with trace.open('a') as f:
        f.write(json.dumps(event, default=_json_default)+'\n')


def _declared_inputs(root: Path) -> list[dict]:
    """Keep source identity on invalid-input traces, never copy source/tool payloads."""
    try:
        config = yaml.safe_load((root/'lockstep.yaml').read_text())
        rows = config.get('projections', []) if isinstance(config, dict) else []
        return [{'source': row['source'], 'fields': row.get('fields', [])}
                for row in rows if isinstance(row, dict) and isinstance(row.get('source'), str)
                and isinstance(row.get('fields', []), list)
                and all(isinstance(f, str) for f in row.get('fields', []))]
    except (OSError, ValueError, TypeError, yaml.YAMLError):
        return []


def refresh_cli(argv: list[str]) -> int:
    """PostToolUse refresh of declared facts only; no declarations is a fast no-op."""
    parser = argparse.ArgumentParser(prog='lockstep refresh')
    parser.add_argument('--repo', type=Path)
    parser.add_argument('--client', choices=('claude', 'codex'))
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)
    call = {}
    root = None
    try:
        if args.client:
            call = json.load(sys.stdin)
            if not isinstance(call, dict):
                raise ProjectionError('hook input must be a JSON object')
        root = args.repo or _root(Path(call.get('cwd') or os.getcwd()))
        if root is None:
            return 0
        root = root.resolve()
        rows = declarations(root)
        if not rows:
            return 0
        if args.client:
            from lockstep.hook import paths_from_call
            paths = paths_from_call(call)
            if paths:
                cwd = Path(call.get('cwd') or os.getcwd())
                edited = {(Path(p) if Path(p).is_absolute() else cwd/p).resolve() for p in paths}
                applicable = {(root/row[k]).resolve() for row in rows for k in ('source', 'target')}
                if not edited.intersection(applicable) and (root/'lockstep.yaml').resolve() not in edited:
                    return 0
            # Shell writes can be dynamic. With no concrete edit path, compare declared
            # facts conservatively; no arbitrary command from the configuration runs.
        _trace_path(root)  # Validate the append path before any projection write.
        changed = project_facts(root)
        # One append-only daily trace; source bytes and generated output can be opened at these paths.
        inputs = [{'source': row['source'], 'fields': row['fields'],
                   'sha256': hashlib.sha256((root/row['source']).read_bytes()).hexdigest(),
                   'facts': _facts(root/row['source'], row['fields'], row.get('symbol'))} for row in rows]
        outputs = [{'target': row['target'], 'sha256': hashlib.sha256((root/row['target']).read_bytes()).hexdigest()} for row in rows]
        event = {'tool': call.get('tool_name'), 'inputs': inputs, 'outputs': outputs, 'rewrote': changed, 'exit_status': 0}
        _append_trace(root, event)
        for rel in changed:
            print(f'rewrote {rel}')
        print(f'RESULT refresh rewrote={len(changed)} exit=0')
        return 0
    except (OSError, ValueError, TypeError, SyntaxError, yaml.YAMLError) as exc:
        # YAML/SyntaxError formatting can include the source line; keep the actual
        # error message without embedding source or raw tool content in the log.
        message = getattr(exc, 'problem', None) or getattr(exc, 'msg', None) or str(exc)
        print(f'error: {message}', file=sys.stderr)
        print('RESULT refresh errors=1 exit=2', file=sys.stderr)
        if root is not None:
            try:
                _append_trace(root, {'tool': call.get('tool_name'), 'inputs': _declared_inputs(root),
                                     'error': message, 'exit_status': 2})
            except (OSError, ValueError, TypeError):
                # A missing/uncontained/unwritable trace location cannot become an escape.
                pass
        return 2
