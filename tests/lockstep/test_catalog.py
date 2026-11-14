"""Source identity and semantic-review boundaries for the complete-file catalog."""
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from lockstep.catalog import CatalogError, catalog_cli, inspect_catalog, refresh_catalog, review_catalog

pytestmark = pytest.mark.req('lockstep-catalog-upkeep/tracked-file-review-stays-bound-to-source')


def git(root, *args):
    subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)


def digest(root, name):
    return hashlib.sha256((root / name).read_bytes()).hexdigest()


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, 'init')
    (tmp_path / 'lockstep.yaml').write_text('catalog:\n  inventory: inventory.json\n  target: catalog.md\n')
    (tmp_path / 'catalog.md').write_text('---\nstatus: current\n---\nIntro\n**Coverage:** old\nExternal routes stay.\n\n## Browse by folder\nold\n')
    (tmp_path / 'source.txt').write_text('original source')
    entries = [{'path': name, 'summary': 'Reviewed purpose', 'sha256': None if name in ('inventory.json', 'catalog.md') else digest(tmp_path, name), 'custom': 7}
               for name in ('catalog.md', 'inventory.json', 'source.txt', 'lockstep.yaml')]
    (tmp_path / 'inventory.json').write_text(json.dumps({'entries': entries}))
    git(tmp_path, 'add', '.')
    return tmp_path


def review(root, name, **extra):
    return dict(path=name, sha256=digest(root, name), summary='Reviewed purpose', review_reason='Read complete file; existing purpose remains accurate', **extra)


def test_edit_and_explicit_retained_summary(repo):
    (repo / 'source.txt').write_text('changed')
    report = inspect_catalog(repo)
    assert report['pending'] == [{'path': 'source.txt', 'kind': 'changed', 'sha256': digest(repo, 'source.txt'), 'summary': 'Reviewed purpose'}]
    review_catalog(repo, [review(repo, 'source.txt')])
    assert inspect_catalog(repo)['pending'] == []
    row = next(r for r in json.loads((repo / 'inventory.json').read_text())['entries'] if r['path'] == 'source.txt')
    assert row['custom'] == 7
    assert list((repo / '.lockstep').glob('catalog-*.jsonl'))


def test_added_removed_and_private_untracked(repo):
    (repo / 'private.txt').write_text('ignored untracked')
    (repo / 'new.txt').write_text('new source')
    git(repo, 'add', 'new.txt')
    git(repo, 'rm', '-f', 'source.txt')
    assert [(r['path'], r['kind']) for r in inspect_catalog(repo)['pending']] == [('new.txt', 'added'), ('source.txt', 'removed')]
    review_catalog(repo, [review(repo, 'new.txt', role='source', disposition='keep', reason='Unique', source_locator='full file'), dict(path='source.txt', sha256=None, summary='Removed file', review_reason='Reviewed staged deletion')])
    assert inspect_catalog(repo)['pending'] == []


def test_wrong_hash_batch_refusal_is_atomic(repo):
    original = (repo / 'inventory.json').read_bytes()
    rows = [review(repo, 'lockstep.yaml'), {**review(repo, 'source.txt'), 'sha256': '0' * 64}]
    with pytest.raises(CatalogError):
        review_catalog(repo, rows)
    assert (repo / 'inventory.json').read_bytes() == original
    assert 'errors' in next((repo / '.lockstep').glob('*.jsonl')).read_text()


@pytest.mark.req('lockstep-catalog-upkeep/catalog-refresh-never-approves-meaning')
def test_refresh_preserves_review_and_prefix_and_is_idempotent(repo):
    (repo / 'source.txt').write_text('new meaning')
    before = (repo / 'inventory.json').read_bytes()
    assert refresh_catalog(repo) == ['catalog.md']
    text = (repo / 'catalog.md').read_text()
    assert text.startswith('---\nstatus: current\n---\nIntro\n')
    assert 'External routes stay.' in text
    assert 'Pending source review' in text
    assert 'Reviewed purpose' in text
    assert (repo / 'inventory.json').read_bytes() == before
    assert refresh_catalog(repo) == []


@pytest.mark.req('lockstep-catalog-upkeep/hooks-and-gates-expose-pending-review')
def test_check_is_read_only_and_rejects_stale(repo):
    before = (repo / 'catalog.md').read_bytes()
    assert catalog_cli(['check', '--repo', str(repo)]) == 1
    assert (repo / 'catalog.md').read_bytes() == before
    refresh_catalog(repo)
    assert catalog_cli(['check', '--repo', str(repo)]) == 0
    (repo / 'source.txt').write_text('changed')
    assert catalog_cli(['check', '--repo', str(repo)]) == 1


def test_escape_links_and_labels(repo):
    name = 'a [b](c)#%.txt'
    (repo / name).write_text('source')
    git(repo, 'add', name)
    review_catalog(repo, [review(repo, name, role='source', disposition='keep', reason='unique', source_locator='full file')])
    refresh_catalog(repo)
    text = (repo / 'catalog.md').read_text()
    assert 'a%20%5Bb%5D%28c%29%23%25.txt' in text
    assert r'a \[b\](c)#%.txt' in text


def test_no_config_noop(tmp_path):
    assert inspect_catalog(tmp_path) is None
    assert refresh_catalog(tmp_path) == []
    assert catalog_cli(['check', '--repo', str(tmp_path)]) == 0


@pytest.mark.parametrize('path', ['../outside', '/tmp/outside', './source.txt'])
def test_invalid_containment(repo, path):
    with pytest.raises(CatalogError):
        review_catalog(repo, [dict(path=path, sha256=None, summary='x', review_reason='x')])


def test_external_symlink_and_missing_tracked_source(repo, tmp_path_factory):
    outside = tmp_path_factory.mktemp('outside') / 'file'
    outside.write_text('outside')
    (repo / 'linked').symlink_to(outside)
    git(repo, 'add', 'linked')
    with pytest.raises(CatalogError):
        inspect_catalog(repo)
    git(repo, 'rm', '-f', 'linked')
    (repo / 'source.txt').unlink()
    with pytest.raises(CatalogError, match='missing'):
        inspect_catalog(repo)
