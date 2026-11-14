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
