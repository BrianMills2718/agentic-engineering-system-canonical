"""Source-owned facts reach wiki blocks; stale copies fail without executing source."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from lockstep.checks import project
from lockstep.checks.cli import run


def _repo(root: Path, source='docs/plan.md', fields=None, symbol=None):
    row = {'id': 'example', 'source': source, 'target': 'wiki/index.md',
           'fields': fields or ['description', 'status']}
    if symbol:
        row['symbol'] = symbol
    (root/'wiki').mkdir(parents=True)
    (root/'docs').mkdir(exist_ok=True)
    (root/'wiki/index.md').write_text('# Wiki\n\n<!-- lockstep facts: example -->\nold\n<!-- /lockstep facts: example -->\n\nKeep this narrative.\n')
    (root/'lockstep.yaml').write_text(yaml.safe_dump({'projections': [row]}))
    (root/'docs/plan.md').write_text('---\ndescription: Own description\nstatus: active\n---\n# Plan\n')
    return root


@pytest.mark.req('lockstep-doc-facts/markdown-facts-regenerate-and-stale-check-is-read-only')
def test_markdown_facts_regenerate_and_stale_check_is_read_only(tmp_path):
    root = _repo(tmp_path)
    before = (root/'wiki/index.md').read_bytes()
    assert 'wiki/index.md' in project.project(root, check=True)
    assert (root/'wiki/index.md').read_bytes() == before
    assert 'wiki/index.md' in project.project(root)
    text = (root/'wiki/index.md').read_text()
    assert 'Own description' in text and '| status | active |' in text
    assert 'Keep this narrative.' in text
    assert project.project(root, check=True) == []
    (root/'docs/plan.md').write_text('---\ndescription: Edited description\nstatus: done\n---\n# Plan\n')
    assert run(['project', '--repo', str(root), '--check']) == 1
    project.project(root)
    assert '| status | done |' in (root/'wiki/index.md').read_text()


@pytest.mark.req('lockstep-doc-facts/python-description-and-interface-are-static')
def test_python_description_and_interface_are_static(tmp_path):
    root = _repo(tmp_path, source='api.py', fields=['description', 'signature'], symbol='greet')
    p = root/'api.py'
    p.write_text('raise RuntimeError("must not execute")\ndef greet(name: str) -> str:\n    """Say hello."""\n    return name\n')
    project.project(root)
    text = (root/'wiki/index.md').read_text()
    assert 'Say hello.' in text and 'greet(name: str) -&gt; str' in text
    p.write_text(p.read_text().replace('name: str', 'name: str, loud: bool = False').replace('Say hello.', 'Say hello loudly.'))
    assert 'wiki/index.md' in project.project(root, check=True)
    project.project(root)
    assert 'loud: bool=False' in (root/'wiki/index.md').read_text()
    assert 'Say hello loudly.' in (root/'wiki/index.md').read_text()


@pytest.mark.req('lockstep-doc-facts/markdown-facts-regenerate-and-stale-check-is-read-only')
def test_plan_target_composes_facts_and_coverage(tmp_path):
    root = _repo(tmp_path)
    spec = root/'openspec/specs/demo/spec.md'
    spec.parent.mkdir(parents=True)
    spec.write_text('### Requirement: Works\nIt SHALL work.\n')
    target = root/'wiki/index.md'
    plan = root/'docs/plans/test.md'
    plan.parent.mkdir()
    plan.write_text('# Plan\n\nCloses: demo/works\n\n'+target.read_text())
    cfg = yaml.safe_load((root/'lockstep.yaml').read_text())
    cfg['projections'][0]['target'] = 'docs/plans/test.md'
    (root/'lockstep.yaml').write_text(yaml.safe_dump(cfg))
    project.project(root)
    assert project.START in plan.read_text()
    assert '| status | active |' in plan.read_text()
    assert project.project(root, check=True) == []
    assert project.project(root) == []


@pytest.mark.req('lockstep-doc-facts/python-description-and-interface-are-static')
def test_python_docstring_fact_sees_generated_requirement_copy(tmp_path):
    root = _repo(tmp_path, source='src/api.py', fields=['docstring'])
    (root/'src').mkdir()
    source = root/'src/api.py'
    source.write_text('"""API description.\n\nImplements: demo/works\n"""\n')
    spec = root/'openspec/specs/demo/spec.md'
    spec.parent.mkdir(parents=True)
    spec.write_text('### Requirement: Works\nIt SHALL work.\n')
    project.project(root)
    assert 'It SHALL work.' in (root/'wiki/index.md').read_text()
    assert project.project(root, check=True) == []


@pytest.mark.req('lockstep-doc-facts/python-description-and-interface-are-static')
def test_class_signature_preserves_creation_keywords(tmp_path):
    root = _repo(tmp_path, source='api.py', fields=['signature'], symbol='A')
    source = root/'api.py'
    source.write_text('class A(Base, metaclass=FirstMeta, category="public"):\n    pass\n')
    project.project(root)
    assert 'metaclass=FirstMeta' in (root/'wiki/index.md').read_text()
    assert "category='public'" in (root/'wiki/index.md').read_text()
    source.write_text(source.read_text().replace('FirstMeta', 'SecondMeta'))
    assert project.project(root, check=True) == ['wiki/index.md']


@pytest.mark.req('lockstep-doc-facts/invalid-projection-input-fails-before-writing')
def test_full_file_coverage_target_collision_refuses_before_any_write(tmp_path):
    root = _repo(tmp_path)
    spec = root/'openspec/specs/demo/spec.md'
    spec.parent.mkdir(parents=True)
    spec.write_text('### Requirement: Works\nIt SHALL work.\n')
    status = root/'docs/status.md'
    status.write_bytes((root/'wiki/index.md').read_bytes())
    cfg = yaml.safe_load((root/'lockstep.yaml').read_text())
    cfg['projections'][0]['target'] = 'docs/status.md'
    (root/'lockstep.yaml').write_text(yaml.safe_dump(cfg))
    before = status.read_bytes()
    assert run(['project', '--repo', str(root)]) == 2
    assert status.read_bytes() == before


@pytest.mark.req('lockstep-doc-facts/evidence-fields-are-read-from-native-records')
@pytest.mark.parametrize('name', ['evidence.json', 'evidence.yaml'])
def test_evidence_fields_are_read_from_native_records(tmp_path, name):
    root = _repo(tmp_path, source=name, fields=['result'])
    p = root/name
    p.write_text(json.dumps({'result': 'failed'}))
    project.project(root)
    assert '| result | failed |' in (root/'wiki/index.md').read_text()
    p.write_text(json.dumps({'result': 'passed'}))
    assert 'wiki/index.md' in project.project(root, check=True)


@pytest.mark.req('lockstep-doc-facts/evidence-fields-are-read-from-native-records')
def test_yaml_date_scalar_is_stable(tmp_path):
    root = _repo(tmp_path, source='record.yaml', fields=['date'])
    (root/'record.yaml').write_text('date: 2026-11-12\n')
    project.project(root)
    assert '2026-11-12' in (root/'wiki/index.md').read_text()
    assert project.project(root, check=True) == []


@pytest.mark.req('lockstep-doc-facts/markdown-facts-regenerate-and-stale-check-is-read-only')
def test_source_base_url_and_scalar_html_are_portable(tmp_path):
    root = _repo(tmp_path)
    cfg = yaml.safe_load((root/'lockstep.yaml').read_text())
    cfg['source_base_url'] = 'https://example.test/owner/repository/blob/main/'
    (root/'lockstep.yaml').write_text(yaml.safe_dump(cfg))
    (root/'docs/plan.md').write_text('---\ndescription: "<script>x()</script> | true"\nstatus: done\n---\n')
    project.project(root)
    page = (root/'wiki/index.md').read_text()
    assert '(https://example.test/owner/repository/blob/main/docs/plan.md)' in page
    assert '<script>' not in page and '&lt;script&gt;' in page and '&#124;' in page


@pytest.mark.req('lockstep-doc-facts/invalid-projection-input-fails-before-writing')
@pytest.mark.parametrize('url', ['javascript:alert(1)', 'https://user:password@example.test/', 12])
def test_invalid_source_base_url_refuses_generation(tmp_path, url):
    root = _repo(tmp_path)
    cfg = yaml.safe_load((root/'lockstep.yaml').read_text())
    cfg['source_base_url'] = url
    (root/'lockstep.yaml').write_text(yaml.safe_dump(cfg))
    before = (root/'wiki/index.md').read_bytes()
    assert run(['project', '--repo', str(root)]) == 2
    assert (root/'wiki/index.md').read_bytes() == before


@pytest.mark.req('lockstep-doc-facts/invalid-projection-input-fails-before-writing')
@pytest.mark.parametrize('fault', ['missing_field', 'missing_source', 'missing_marker', 'duplicate_marker', 'traversal', 'symlink'])
def test_invalid_projection_input_fails_before_writing(tmp_path, fault):
    root = _repo(tmp_path)
    cfg = yaml.safe_load((root/'lockstep.yaml').read_text())
    if fault == 'missing_field':
        cfg['projections'][0]['fields'] = ['unknown']
    if fault == 'missing_source':
        (root/'docs/plan.md').unlink()
    if fault == 'missing_marker':
        (root/'wiki/index.md').write_text('# Wiki\n')
    if fault == 'duplicate_marker':
        p = root/'wiki/index.md'
        p.write_text(p.read_text()+p.read_text())
    if fault == 'traversal':
        cfg['projections'][0]['source'] = '../outside.md'
    if fault == 'symlink':
        outside = tmp_path.parent/'outside-facts.md'
        outside.write_text('---\nstatus: active\n---\n')
        (root/'docs/plan.md').unlink()
        (root/'docs/plan.md').symlink_to(outside)
    (root/'lockstep.yaml').write_text(yaml.safe_dump(cfg))
    before = (root/'wiki/index.md').read_bytes()
    assert run(['project', '--repo', str(root)]) == 2
    assert (root/'wiki/index.md').read_bytes() == before
    assert not (root/'docs/status.md').exists()


@pytest.mark.req('lockstep-doc-facts/refresh-only-updates-declared-facts')
def test_refresh_only_updates_declared_facts(tmp_path, monkeypatch):
    from lockstep.doc_projection import refresh_cli
    root = _repo(tmp_path)
    monkeypatch.chdir(root)
    assert refresh_cli(['--repo', str(root)]) == 0
    assert not (root/'docs/status.md').exists()
    assert '| status | active |' in (root/'wiki/index.md').read_text()
    traces = list((root/'.lockstep').glob('projection-*.jsonl'))
    event = json.loads(traces[0].read_text().splitlines()[0])
    assert event['inputs'][0]['facts'] == {'description': 'Own description', 'status': 'active'}


@pytest.mark.req('lockstep-doc-facts/installed-post-edit-hook-refreshes-and-precommit-rejects-stale')
def test_refresh_records_source_error_without_raw_tool_input(tmp_path, monkeypatch):
    import io
    from lockstep.doc_projection import refresh_cli
    root = _repo(tmp_path)
    (root/'docs/plan.md').write_text('---\nstatus: active\n---\n')
    monkeypatch.setattr(sys, 'stdin', io.StringIO(json.dumps({
        'cwd': str(root), 'tool_name': 'Write', 'tool_input': {
            'file_path': str(root/'docs/plan.md'), 'content': 'private tool payload'}})))
    assert refresh_cli(['--client', 'claude']) == 2
    trace = next((root/'.lockstep').glob('projection-*.jsonl')).read_text()
    event = json.loads(trace)
    assert event['exit_status'] == 2 and event['tool'] == 'Write'
    assert 'missing source field(s): description' in event['error']
    assert event['inputs'][0]['source'] == 'docs/plan.md'
    assert 'private tool payload' not in trace


@pytest.mark.req('lockstep-doc-facts/invalid-projection-input-fails-before-writing')
def test_refresh_refuses_escaping_trace_symlink_before_writes(tmp_path):
    from datetime import datetime, timezone
    from lockstep.doc_projection import refresh_cli
    root = _repo(tmp_path)
    (root/'.lockstep').mkdir()
    outside = tmp_path.parent/'outside-trace.jsonl'
    outside.write_text('preserve\n')
    trace = root/'.lockstep'/f'projection-{datetime.now(timezone.utc):%Y-%m-%d}.jsonl'
    trace.symlink_to(outside)
    before = (root/'wiki/index.md').read_bytes()
    assert refresh_cli(['--repo', str(root)]) == 2
    assert (root/'wiki/index.md').read_bytes() == before
    assert outside.read_text() == 'preserve\n'


@pytest.mark.req('lockstep-doc-facts/refresh-only-updates-declared-facts')
def test_empty_repository_does_not_invent_coverage(tmp_path):
    (tmp_path/'docs').mkdir()
    assert project.project(tmp_path, check=True) == []
    assert project.project(tmp_path) == []
    assert not (tmp_path/'docs/status.md').exists()


@pytest.mark.req('lockstep-doc-facts/refresh-only-updates-declared-facts')
def test_refresh_ignores_unrelated_file_edit(tmp_path, monkeypatch):
    import io
    from lockstep.doc_projection import refresh_cli
    root = _repo(tmp_path)
    monkeypatch.chdir(root)
    before = (root/'wiki/index.md').read_bytes()
    monkeypatch.setattr(sys, 'stdin', io.StringIO(json.dumps({
        'cwd': str(root), 'tool_name': 'Write', 'tool_input': {'file_path': str(root/'other.md')}})))
    assert refresh_cli(['--client', 'claude']) == 0
    assert (root/'wiki/index.md').read_bytes() == before
    assert not (root/'.lockstep').exists()


@pytest.mark.req('lockstep-doc-facts/installed-post-edit-hook-refreshes-and-precommit-rejects-stale')
@pytest.mark.parametrize('client', ['claude', 'codex'])
def test_installed_post_edit_hook_refreshes_and_precommit_rejects_stale(tmp_path, client):
    from lockstep.init_repo import init_repo
    root = _repo(tmp_path)
    init_repo(root, owner='Acme', source='git+https://example.invalid/tool')
    rel = '.claude/settings.json' if client == 'claude' else '.codex/hooks.json'
    hooks = json.loads((root/rel).read_text())['hooks']['PostToolUse']
    assert any('lockstep refresh' in h['command'] for row in hooks for h in row['hooks'])
    pre = yaml.safe_load((root/'lefthook.yml').read_text())['pre-commit']['commands']['lockstep']['run']
    assert 'project --check' in pre
    command = [sys.executable, '-c', 'from lockstep.check import cli;raise SystemExit(cli())', 'refresh', '--client', client]
    env = {**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[3]/'src')}
    result = subprocess.run(command, env=env, cwd=root, input=json.dumps({'cwd': str(root), 'tool_name': 'Write', 'tool_input': {'file_path': str(root/'docs/plan.md')}}), text=True, capture_output=True)
    assert result.returncode == 0, result.stdout+result.stderr
    assert '| status | active |' in (root/'wiki/index.md').read_text()
    (root/'docs/plan.md').write_text('---\ndescription: Edited\nstatus: done\n---\n')
    assert run(['project', '--repo', str(root), '--check']) == 1


def _array_repo(tmp_path, suffix='json'):
    root = _repo(tmp_path, source='units.' + suffix, fields=['id', 'status'])
    cfg = yaml.safe_load((root/'lockstep.yaml').read_text())
    cfg['projections'][0]['items'] = 'units'
    (root/'lockstep.yaml').write_text(yaml.safe_dump(cfg))
    source = root/('units.' + suffix)
    source.write_text(json.dumps({'units': [{'id': 'A|<', 'status': 'ready'}, {'id': 'B', 'status': 'done'}]}))
    return root, source


@pytest.mark.req('lockstep-doc-facts/array-facts-remain-current')
@pytest.mark.parametrize('suffix', ['json', 'yaml'])
def test_array_facts_remain_current(tmp_path, suffix):
    root, source = _array_repo(tmp_path, suffix)
    project.project(root)
    page = root/'wiki/index.md'
    text = page.read_text()
    assert '| id | status |' in text
    assert '| A&#124;&lt; | ready |' in text
    assert text.index('A&#124;&lt;') < text.index('| B | done |')
    before = page.read_bytes()
    source.write_text(source.read_text().replace('ready', 'accepted'))
    assert run(['project', '--repo', str(root), '--check']) == 1
    assert page.read_bytes() == before
    project.project(root)
    assert '| A&#124;&lt; | accepted |' in page.read_text()
    assert project.project(root, check=True) == []


@pytest.mark.req('lockstep-doc-facts/invalid-array-facts-fail-before-writing')
@pytest.mark.parametrize('units', [None, {}, [None], [{'id':'A'}], [{'status':'done'}],
                                  [{'id':'', 'status':'done'}], [{'id':'A', 'status':None}],
                                  [{'id':'A','status':[]}], [{'id':'A','status':'ok'}, {'id':'A','status':'done'}]])
def test_invalid_array_facts_fail_before_writing(tmp_path, units):
    root, source = _array_repo(tmp_path)
    source.write_text(json.dumps({'units': units}))
    before = (root/'wiki/index.md').read_bytes()
    assert run(['project', '--repo', str(root)]) == 2
    assert (root/'wiki/index.md').read_bytes() == before


@pytest.mark.req('lockstep-doc-facts/array-facts-remain-current')
@pytest.mark.parametrize('client', ['claude', 'codex'])
def test_array_edit_through_native_refresh(tmp_path, monkeypatch, client):
    import io
    from lockstep.doc_projection import refresh_cli
    root, source = _array_repo(tmp_path)
    monkeypatch.chdir(root)
    payload = {'cwd': str(root), 'tool_name': 'Write', 'tool_input': {'file_path': str(source)}}
    monkeypatch.setattr(sys, 'stdin', io.StringIO(json.dumps(payload)))
    assert refresh_cli(['--client', client]) == 0
    assert '| A&#124;&lt; | ready |' in (root/'wiki/index.md').read_text()
    event = json.loads(next((root/'.lockstep').glob('projection-*.jsonl')).read_text())
    assert event['inputs'][0]['items'] == 'units'
    assert event['inputs'][0]['facts'] == [{'id': 'A|<', 'status': 'ready'}, {'id': 'B', 'status': 'done'}]
    source.write_text(source.read_text().replace('ready', 'accepted'))
    assert run(['project', '--repo', str(root), '--check']) == 1
    monkeypatch.setattr(sys, 'stdin', io.StringIO(json.dumps(payload)))
    assert refresh_cli(['--client', client]) == 0
    assert '| A&#124;&lt; | accepted |' in (root/'wiki/index.md').read_text()


@pytest.mark.req('lockstep-doc-facts/invalid-array-facts-fail-before-writing')
@pytest.mark.parametrize('items', [None, '', 1])
def test_invalid_array_declaration_refused(tmp_path, items):
    root, _ = _array_repo(tmp_path)
    cfg = yaml.safe_load((root/'lockstep.yaml').read_text())
    cfg['projections'][0]['items'] = items
    (root/'lockstep.yaml').write_text(yaml.safe_dump(cfg))
    before = (root/'wiki/index.md').read_bytes()
    assert run(['project', '--repo', str(root)]) == 2
    assert (root/'wiki/index.md').read_bytes() == before
