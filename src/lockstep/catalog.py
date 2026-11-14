"""Maintain navigation without pretending deterministic generation reviews meaning.

Implements: lockstep-catalog-upkeep/tracked-file-review-stays-bound-to-source,
    lockstep-catalog-upkeep/catalog-refresh-never-approves-meaning,
    lockstep-catalog-upkeep/hooks-and-gates-expose-pending-review
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html import escape
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import quote

import yaml


class CatalogError(ValueError):
    """Catalog inputs cannot establish a valid review."""


def _path(root: Path, value: object) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '..' in Path(value).parts or Path(value).as_posix() != value:
        raise CatalogError('catalog path must be normalized and repository-relative')
    result = root / value
    if not result.resolve().is_relative_to(root.resolve()):
        raise CatalogError('catalog path escapes repository')
    return result


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(root: Path) -> tuple[dict, dict, bytes] | None:
    config = root / 'lockstep.yaml'
    if not config.exists():
        return None
    data = yaml.safe_load(config.read_text())
    if not isinstance(data, dict):
        raise CatalogError('lockstep.yaml must contain a mapping')
    if 'catalog' not in data:
        return None
    declaration = data['catalog']
    if not isinstance(declaration, dict) or set(declaration) != {'inventory', 'target'}:
        raise CatalogError('catalog requires inventory and target')
    inventory, target = (_path(root, declaration[k]) for k in ('inventory', 'target'))
    if inventory == target:
        raise CatalogError('catalog inventory and target must differ')
    raw = inventory.read_bytes()
    document = json.loads(raw)
    if not isinstance(document, dict) or not isinstance(document.get('entries'), list):
        raise CatalogError('inventory requires an entries list')
    seen = set()
    for row in document['entries']:
        if not isinstance(row, dict):
            raise CatalogError('inventory entry must be an object')
        _path(root, row.get('path'))
        if row['path'] in seen or not isinstance(row.get('summary'), str) or not row['summary'].strip():
            raise CatalogError('inventory paths must be distinct and summaries nonempty')
        digest = row.get('sha256')
        if digest is not None and (not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest)):
            raise CatalogError('inventory sha256 must be a digest or null')
        for key in ('role', 'disposition', 'reason', 'source_locator'):
            if key in row and (not isinstance(row[key], str) or not row[key].strip()):
                raise CatalogError(f'inventory {key} must be nonempty')
        seen.add(row['path'])
    if not target.is_file():
        raise CatalogError('catalog target does not exist')
    return declaration, document, raw


def _snapshot(root: Path, declaration: dict) -> dict[str, str | None]:
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '--cached', '-z'], capture_output=True, check=True)
    paths = sorted(set(os.fsdecode(p) for p in result.stdout.split(b'\0') if p))
    snapshot = {}
    for name in paths:
        path = _path(root, name)
        if not path.is_file():
            raise CatalogError(f'tracked source is missing or not a file: {name}')
        snapshot[name] = None if name in declaration.values() else _digest(path)
    return snapshot


def _pending(document: dict, snapshot: dict) -> list[dict]:
    entries = {row['path']: row for row in document['entries']}
    return [dict(path=name, kind='added' if name not in entries else 'removed' if name not in snapshot else 'changed',
                 sha256=snapshot.get(name), summary=entries.get(name, {}).get('summary'))
            for name in sorted(entries.keys() | snapshot.keys())
            if name not in entries or name not in snapshot or entries[name].get('sha256') != snapshot[name]]


def _label(value: str) -> str:
    return escape(value, quote=False).replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]').replace('_', '\\_').replace('*', '\\*').replace('|', '&#124;').replace('\n', '<br>').replace('\r', '')


def _render(root: Path, declaration: dict, document: dict, pending: list[dict]) -> str:
    original = _path(root, declaration['target']).read_text()
    marker = '## Browse by folder'
    if original.count(marker) != 1:
        raise CatalogError('catalog needs exactly one Browse by folder heading')
    prefix = original.split(marker)[0]
    coverage = f'**Coverage:** {len(document["entries"])} inventory files; {len(pending)} pending source reviews. Links and stored summaries do not establish current verification.'
    prefix = re.sub(r'^\*\*Coverage:\*\*[^\n]*', lambda _: coverage, prefix, flags=re.M)
    if '**Coverage:**' not in prefix:
        prefix += coverage + '\n\n'
    lines = [prefix.rstrip(), '', marker, '', f'Pending reviews: {len(pending)}. Refresh preserves reviewed summaries; a native coding agent must review complete changed files.', '']
    if pending:
        lines += ['### Pending source reviews', '']
        lines += [f'- {_label(row["path"])} — {row["kind"]}; review required.' for row in pending]
        lines.append('')
    groups: dict[str, list] = {}
    for row in sorted(document['entries'], key=lambda row: row['path']):
        groups.setdefault(str(Path(row['path']).parent), []).append(row)
    pending_names = {row['path'] for row in pending}
    for index, (folder, rows) in enumerate(sorted(groups.items())):
        title = folder if folder != '.' else 'Repository root'
        lines.append(f'- [{_label(title)}](#catalog-folder-{index}) ({len(rows)} files)')
    lines.append('')
    for index, (folder, rows) in enumerate(sorted(groups.items())):
        lines += [f'<a id="catalog-folder-{index}"></a>', f'### {_label(folder if folder != "." else "Repository root")}', '']
        for row in rows:
            link = quote(os.path.relpath(root / row['path'], (root / declaration['target']).parent), safe='/')
            status = ' **Pending source review.**' if row['path'] in pending_names else ''
            lines.append(f'- [{_label(row["path"])}]({link}) — {_label(row["summary"])} Role: {_label(row.get("role", "unspecified"))}; disposition: {_label(row.get("disposition", "unspecified"))}.{status}')
        lines.append('')
    return '\n'.join(lines)


def inspect_catalog(root: Path) -> dict | None:
    loaded = _load(root)
    if loaded is None:
        return None
    declaration, document, _ = loaded
    pending = _pending(document, _snapshot(root, declaration))
    return {'pending': pending, 'catalog_stale': _path(root, declaration['target']).read_text() != _render(root, declaration, document, pending)}


def _atomic(path: Path, content: bytes) -> None:
    mode = path.stat().st_mode & 0o777
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.lockstep-', delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(content)
    try:
        temporary.chmod(mode)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _refresh_catalog(root: Path) -> list[str]:
    loaded = _load(root)
    if loaded is None:
        return []
    declaration, document, raw = loaded
    snapshot = _snapshot(root, declaration)
    target = _path(root, declaration['target'])
    original = target.read_bytes()
    rendered = _render(root, declaration, document, _pending(document, snapshot)).encode()
    if _snapshot(root, declaration) != snapshot or _path(root, declaration['inventory']).read_bytes() != raw or target.read_bytes() != original:
        raise CatalogError('catalog inputs changed during refresh')
    changed = [] if original == rendered else [declaration['target']]
    _path(root, f'.lockstep/catalog-{datetime.now(timezone.utc):%Y-%m-%d}.jsonl')
    _trace(root, {'operation': 'refresh', 'phase': 'prepared' if changed else 'unchanged',
                  'inputs': snapshot, 'inventory_sha256': hashlib.sha256(raw).hexdigest(),
                  'output_sha256': hashlib.sha256(rendered).hexdigest(), 'rewritten': changed, 'errors': []})
    if changed:
        _atomic(target, rendered)
    return changed


def refresh_catalog(root: Path) -> list[str]:
    try:
        return _refresh_catalog(root)
    except (OSError, ValueError, TypeError, subprocess.SubprocessError, yaml.YAMLError):
        try:
            _trace(root, {'operation': 'refresh', 'errors': ['refresh rejected; validate configuration, tracked paths and source stability']})
        except (OSError, ValueError):
            pass
        raise


def _trace(root: Path, event: dict) -> None:
    trace = _path(root, f'.lockstep/catalog-{datetime.now(timezone.utc):%Y-%m-%d}.jsonl')
    trace.parent.mkdir(exist_ok=True)
    with trace.open('a') as stream:
        stream.write(json.dumps(event, sort_keys=True) + '\n')


def review_catalog(root: Path, reviews: list[dict]) -> dict:
    event: dict = {'operation': 'review', 'reviews': [], 'errors': []}
    try:
        loaded = _load(root)
        if loaded is None:
            raise CatalogError('catalog is not configured')
        declaration, document, raw = loaded
        snapshot = _snapshot(root, declaration)
        entries = {row['path']: dict(row) for row in document['entries']}
        if not isinstance(reviews, list) or not reviews:
            raise CatalogError('review input requires a nonempty list')
        seen = set()
        for row in reviews:
            if not isinstance(row, dict) or not {'path', 'sha256', 'summary', 'review_reason'} <= row.keys():
                raise CatalogError('review requires path, sha256, summary and review_reason')
            name = row['path']
            _path(root, name)
            if name in seen:
                raise CatalogError('duplicate review path')
            seen.add(name)
            for key in ('summary', 'review_reason'):
                if not isinstance(row[key], str) or not row[key].strip():
                    raise CatalogError(f'review {key} must be nonempty')
            event['reviews'].append({key: row[key] for key in ('path', 'sha256', 'summary', 'review_reason')})
            if name not in snapshot:
                if name not in entries or row['sha256'] is not None:
                    raise CatalogError('removal requires an existing entry absent from the git index')
                del entries[name]
                continue
            if row['sha256'] != snapshot[name]:
                raise CatalogError('review hash does not match current source bytes')
            if name not in entries:
                for key in ('role', 'disposition', 'reason', 'source_locator'):
                    if not isinstance(row.get(key), str) or not row[key].strip():
                        raise CatalogError(f'new entry requires {key}')
            entries[name] = {**entries.get(name, {}), **row}
        document['entries'] = [entries[name] for name in sorted(entries)]
        output = (json.dumps(document, indent=2, ensure_ascii=False) + '\n').encode()
        inventory = _path(root, declaration['inventory'])
        # Validate trace containment and all source identities before the first write.
        _path(root, f'.lockstep/catalog-{datetime.now(timezone.utc):%Y-%m-%d}.jsonl')
        if inventory.read_bytes() != raw or _snapshot(root, declaration) != snapshot:
            raise CatalogError('catalog inputs changed during review')
        event['phase'] = 'prepared'
        event['output_sha256'] = hashlib.sha256(output).hexdigest()
        event['reviewed'] = len(reviews)
        _trace(root, event)
        # The durable prepared receipt identifies the exact proposed output hash.
        # Append failure must occur before replacement, never after successful mutation.
        _atomic(inventory, output)
        event['phase'] = 'applied'
        return event
    except (OSError, ValueError, TypeError, subprocess.SubprocessError):
        event['errors'] = ['catalog review rejected; input validation or concurrent source change']
        try:
            _trace(root, event)
        except (OSError, ValueError):
            pass
        raise


def catalog_cli(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog='lockstep catalog')
    parser.add_argument('command', nargs='?', choices=('pending', 'refresh', 'check', 'review'), default='pending')
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--input', type=Path)
    try:
        args = parser.parse_args(argv)
        root = args.repo.resolve()
        if args.command == 'review':
            if args.input is None:
                raise CatalogError('review requires --input')
            result = review_catalog(root, json.loads(args.input.read_text()))
        elif args.command == 'refresh':
            result = {'rewritten': refresh_catalog(root)}
        else:
            result = inspect_catalog(root)
        print(json.dumps(result, sort_keys=True))
        return int(args.command == 'check' and bool(result) and bool(result['pending'] or result['catalog_stale']))
    except SystemExit as exc:
        return int(exc.code or 0)
    except (OSError, ValueError, TypeError, subprocess.SubprocessError, yaml.YAMLError) as exc:
        print(f'catalog error: {type(exc).__name__}; validate catalog configuration, tracked paths, review fields and current sha256 values, then retry.', file=sys.stderr)
        return 2
