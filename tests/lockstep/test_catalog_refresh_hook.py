"""Native refresh delivers pending semantic review beyond declared fact sources."""
import hashlib
import io
import json
import subprocess

import pytest

from lockstep.doc_projection import refresh_cli


@pytest.mark.req('lockstep-catalog-upkeep/hooks-and-gates-expose-pending-review')
@pytest.mark.parametrize('client', ['claude', 'codex'])
def test_unrelated_edit_delivers_catalog_review_and_preserves_reviewed_hash(tmp_path, monkeypatch, capsys, client):
    subprocess.run(['git', 'init', str(tmp_path)], check=True, capture_output=True)
    (tmp_path/'lockstep.yaml').write_text('catalog:\n  inventory: inventory.json\n  target: catalog.md\n')
    (tmp_path/'catalog.md').write_text('# Catalog\n\n## Browse by folder\n')
    (tmp_path/'source.py').write_text('"""Search once."""\ndef search(): return []\n')
    entries = []
    for name in ['lockstep.yaml', 'catalog.md', 'source.py', 'inventory.json']:
        entries.append(dict(path=name, summary='Reviewed purpose', role='source', disposition='keep',
                            reason='Distinct source', source_locator='Whole file',
                            sha256=None if name in ['catalog.md', 'inventory.json'] else
                            hashlib.sha256((tmp_path/name).read_bytes()).hexdigest()))
    (tmp_path/'inventory.json').write_text(json.dumps(dict(entries=entries)))
    subprocess.run(['git', '-C', str(tmp_path), 'add', '.'], check=True, capture_output=True)
    before = (tmp_path/'inventory.json').read_bytes()
    (tmp_path/'source.py').write_text('"""Search in a loop."""\ndef search():\n    while True: yield []\n')
    call = dict(cwd=str(tmp_path), tool_name='Edit', tool_input={'file_path': str(tmp_path/'source.py')})
    monkeypatch.setattr('sys.stdin', io.StringIO(json.dumps(call)))
    assert refresh_cli(['--client', client]) == 0
    output = json.loads(capsys.readouterr().out)
    context = output['hookSpecificOutput']['additionalContext']
    assert output['hookSpecificOutput']['hookEventName'] == 'PostToolUse'
    assert 'source.py' in context and 'Read each complete changed source' in context
    assert 'review_reason' in context and 'blindly replacing hashes' in context
    assert (tmp_path/'inventory.json').read_bytes() == before
    assert 'Pending source review' in (tmp_path/'catalog.md').read_text()
    events = [json.loads(line) for p in (tmp_path/'.lockstep').glob('projection-*.jsonl') for line in p.read_text().splitlines()]
    assert len(events) == 1 and events[0]['catalog']['pending'][0]['path'] == 'source.py'


def _two_catalog_roots(tmp_path):
    roots = [tmp_path/'launch', tmp_path/'edited']
    for root in roots:
        root.mkdir()
        subprocess.run(['git', 'init', str(root)], check=True, capture_output=True)
        (root/'lockstep.yaml').write_text('catalog:\n  inventory: inventory.json\n  target: catalog.md\n')
        (root/'catalog.md').write_text('# Catalog\n\n## Browse by folder\n')
        (root/'source.py').write_text('"""Own source."""\n')
        entries = [dict(path=name, summary='Reviewed purpose', role='source', disposition='keep', reason='Distinct', source_locator='Whole file', sha256=None if name in ['catalog.md', 'inventory.json'] else hashlib.sha256((root/name).read_bytes()).hexdigest()) for name in ['lockstep.yaml', 'catalog.md', 'source.py', 'inventory.json']]
        (root/'inventory.json').write_text(json.dumps(dict(entries=entries)))
        subprocess.run(['git', '-C', str(root), 'add', '.'], check=True, capture_output=True)
    return roots


@pytest.mark.req('lockstep-catalog-upkeep/hooks-and-gates-expose-pending-review')
@pytest.mark.parametrize('absolute', [True, False])
def test_edit_routes_to_owning_worktree_instead_of_launch_repository(tmp_path, monkeypatch, capsys, absolute):
    launch, edited = _two_catalog_roots(tmp_path)
    launch_before = (launch/'catalog.md').read_bytes()
    (edited/'source.py').write_text('"""Changed source."""\n')
    call = dict(cwd=str(launch), tool_name='Edit', tool_input={'file_path': str(edited/'source.py') if absolute else 'source.py', 'workdir': str(edited)})
    monkeypatch.setattr('sys.stdin', io.StringIO(json.dumps(call)))
    assert refresh_cli(['--client', 'claude']) == 0
    context = json.loads(capsys.readouterr().out)['hookSpecificOutput']['additionalContext']
    assert '--repo ' + str(edited) in context
    assert (launch/'catalog.md').read_bytes() == launch_before
    assert not (launch/'.lockstep').exists()
    assert 'Pending source review' in (edited/'catalog.md').read_text()
    assert list((edited/'.lockstep').glob('projection-*.jsonl'))


@pytest.mark.req('lockstep-catalog-upkeep/hooks-and-gates-expose-pending-review')
def test_one_patch_across_configured_roots_refuses_without_wrong_target_writes(tmp_path, monkeypatch, capsys):
    launch, edited = _two_catalog_roots(tmp_path)
    before = [(p/'catalog.md').read_bytes() for p in [launch, edited]]
    call = dict(cwd=str(launch), tool_name='apply_patch', tool_input={'input': f'*** Update File: {launch}/source.py\n*** Update File: {edited}/source.py\n'})
    monkeypatch.setattr('sys.stdin', io.StringIO(json.dumps(call)))
    assert refresh_cli(['--client', 'codex']) == 2
    assert 'multiple configured repositories' in capsys.readouterr().err
    assert [(p/'catalog.md').read_bytes() for p in [launch, edited]] == before
