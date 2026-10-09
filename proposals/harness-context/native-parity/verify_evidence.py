"""Check saved paired traces without model calls; integrity is not behavior parity."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tomllib

import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts/learning_loop'))
import subagents as collector  # noqa: E402


def read(path):
    return json.loads(path.read_text())


def digest(value):
    raw = value if isinstance(value, bytes) else json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


def require(condition, name, checks):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def fields(result):
    values = {k: result[k] for k in ('root_cause', 'recommended_parent_action', 'mutation_declaration')}
    for k in ('evidence', 'causal_chain', 'alternatives_ruled_out', 'limitations'):
        values.update({f'{k}[{i}]': v for i, v in enumerate(result[k])})
    return values


def review_result(result, review, root, checks):
    """Check review coverage/provenance. A human or agent supplies semantic judgments."""
    values, entries = fields(result), review['items']
    require(len(entries) == len(values) and {e['field'] for e in entries} == set(values),
            'semantic review covers every result field exactly once', checks)
    counts = dict.fromkeys(('supported', 'qualified', 'incorrect', 'inconclusive'), 0)
    allowed_sources = set(read(HERE / 'input/task.json')['allowed_read_paths'])
    for e in entries:
        name = e['field']
        require(e['value_sha256'] == digest(values[name]), f'review binds {name}', checks)
        require(e['verdict'] in counts and bool(e['rationale']), f'review disposition for {name}', checks)
        counts[e['verdict']] += 1
        for s in e['sources']:
            require(s['path'] in allowed_sources, f'review source is in frozen packet for {name}', checks)
            lines = (root / s['path']).read_text().splitlines()
            a, b = s['start_line'], s['end_line']
            require(0 < a <= b <= len(lines) and s['quote'] == '\n'.join(lines[a-1:b]),
                    f'exact source excerpt for {name}', checks)
    require(review['verdict'] == ('pass' if counts['supported'] == len(entries) else 'inconclusive'),
            'review summary cannot hide qualified or incorrect fields', checks)
    return {'verdict': review['verdict'], 'counts': counts, 'items': len(entries)}


def trace(ref, checks):
    path = Path(ref['path'])
    raw = path.read_bytes()
    require(digest(raw) == ref['sha256'], f'{path.name}: full trace digest', checks)
    rows = [v for _, v in collector.rows(path)]
    require(len(rows) == len(raw.splitlines()), f'{path.name}: complete well-formed records', checks)
    return rows


def events(rows, client):
    calls, outputs = {}, {}
    for n, row in enumerate(rows, 1):
        p = row.get('payload', {})
        if client == 'codex' and row.get('type') == 'response_item':
            if p.get('type') in ('custom_tool_call', 'function_call'):
                key = p['call_id']
                require(key not in calls, 'unique Codex call identity', [])
                calls[key] = {'line': n, 'name': p['name'],
                              'input_sha256': digest(p.get('input', p.get('arguments')))}
            elif p.get('type') in ('custom_tool_call_output', 'function_call_output'):
                key = p['call_id']
                require(key not in outputs, 'unique Codex output identity', [])
                outputs[key] = {'line': n, 'output_sha256': digest(p['output'])}
        elif client == 'claude':
            content = row.get('message', {}).get('content', [])
            for b in content if isinstance(content, list) else []:
                if b.get('type') == 'tool_use':
                    key = b['id']
                    value = {'line': n, 'name': b['name'], 'input_sha256': digest(b['input']),
                             'path': b['input'].get('file_path', b['input'].get('path'))}
                    require(key not in calls or calls[key]['input_sha256'] == value['input_sha256'],
                            'consistent Claude repeated call', [])
                    calls.setdefault(key, value)
                elif b.get('type') == 'tool_result':
                    outputs[b['tool_use_id']] = {'line': n, 'output_sha256': digest(b)}
    return {'calls': calls, 'outputs': outputs}


def usage(rows, client):
    if client == 'codex':
        data = [r['payload']['info'] for r in rows if r.get('type') == 'event_msg'
                and r['payload'].get('type') == 'token_count' and r['payload'].get('info')]
        return {'first': data[0]['last_token_usage'], 'total': data[-1]['total_token_usage']}
    generations = {}
    for r in rows:
        m = r.get('message', {})
        if r.get('type') == 'assistant' and m.get('usage') and m.get('model') != '<synthetic>':
            generations[m['id']] = m['usage']
    first = next(iter(generations.values()))
    keys = ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens', 'output_tokens')
    return {'first': first, 'first_input_including_cache': sum(first.get(k, 0) or 0 for k in keys[:3]),
            'generations': len(generations),
            'total': {k: sum(u.get(k, 0) or 0 for u in generations.values()) for k in keys}}


def behavior(semantics, derived, claude_raw):
    """Derive current verdicts; unavailable execution evidence never becomes pass."""
    cx = derived['codex']
    cl = derived['claude']
    try:
        json.loads(claude_raw)
        literal_json = True
    except ValueError:
        literal_json = False
    checks = [
        {'requirement': 'Required native role delivered', 'claude': 'pass', 'codex': 'pass'},
        {'requirement': 'Every source claim supported', **{
            c: ('fail' if s['counts']['incorrect'] else 'inconclusive' if s['verdict'] != 'pass' else 'pass')
            for c, s in semantics.items()}},
        {'requirement': 'Literal JSON-only output', 'codex': 'pass',
         'claude': 'pass' if literal_json else 'fail'},
        {'requirement': 'Initial input smaller than parent in tested route',
         'codex': 'pass' if cx['child']['first']['input_tokens'] < cx['parent']['first']['input_tokens'] else 'fail',
         'claude': 'pass' if cl['child']['first_input_including_cache'] < cl['parent']['first_input_including_cache'] else 'fail'},
        {'requirement': 'Actual child denial / writable-parent isolation', 'claude': 'inconclusive', 'codex': 'inconclusive'},
        {'requirement': 'Native five-file read enforcement', 'claude': 'inconclusive', 'codex': 'inconclusive'},
        {'requirement': 'Required hook execution parity', 'claude': 'inconclusive', 'codex': 'inconclusive'}]
    counts = {v: sum(c[k] == v for c in checks for k in ('claude', 'codex'))
              for v in ('pass', 'fail', 'inconclusive')}
    verdict = 'fail' if counts['fail'] else 'inconclusive' if counts['inconclusive'] else 'pass'
    return {'verdict': verdict, 'counts': counts, 'checks': checks, 'complete': verdict == 'pass'}


def verify():
    checks = []
    packet, audit = read(HERE / 'input/task.json'), read(HERE / 'paired-trace-review.json')
    require(audit['task_sha256'] == digest(packet), 'review binds frozen task', checks)
    sources = {e['path']: e for e in packet['source_manifest']}
    require(all(digest((ROOT / p).read_bytes()) == e['sha256'] for p, e in sources.items()),
            'all five frozen source hashes match', checks)
    skill_repo = Path.home() / 'code/agent-skills'
    schema = read(skill_repo / 'contracts/specialists/development-investigation-result.v1.schema.json')
    native, results, semantics = {}, {}, {}
    for client, relative in [('codex', 'codex-child-result.json'), ('claude', 'claude-paid/child-result.json')]:
        result = read(HERE / relative)
        jsonschema.validate(result, schema)
        require(result['task_id'] == packet['task_id'], f'{client}: task identity and schema', checks)
        require(all(e['path'] in sources and 0 < int(e['locator'][1:]) <= len(
            (ROOT / e['path']).read_text().splitlines()) for e in result['evidence']),
            f'{client}: citation locations exist (not a meaning check)', checks)
        results[client] = result
        semantics[client] = review_result(result, audit[client]['semantic_review'], ROOT, checks)
        native[client] = {k: trace(v, checks) for k, v in audit[client]['traces'].items()}
        observed = events(native[client]['child'], client)
        require(observed == audit[client]['tool_events'], f'{client}: exact reviewed calls and outputs', checks)
        require(set(observed['outputs']) <= set(observed['calls']), f'{client}: attributed outputs', checks)
        if client == 'codex':
            require(bool(observed['calls']) and set(observed['outputs']) == set(observed['calls']),
                    'Codex completed leaf has a result for every call', checks)
    cx, cl = native['codex'], native['claude']
    cm, pm = cx['child'][0]['payload'], cx['parent'][0]['payload']
    require(cm['parent_thread_id'] == pm['id'] and cm['agent_role'] == 'development-investigator',
            'Codex native parent-child identity', checks)
    spawns = [json.loads(r['payload']['arguments']) for r in cx['parent'] if r.get('type') == 'response_item'
              and r['payload'].get('name') == 'spawn_agent']
    require(len(spawns) == 1 and spawns[0]['fork_turns'] == 'none' and
            spawns[0]['agent_type'] == 'development-investigator', 'Codex fresh-history role dispatch', checks)
    prompt = (HERE / 'parent-prompt.txt').read_text()
    require(json.JSONDecoder().raw_decode(prompt[prompt.index('{'):])[0] == packet,
            'Codex actual parent packet equals frozen task', checks)
    parent_texts = [collector.text_content(r['payload']['content']) for r in cx['parent']
                    if r.get('type') == 'response_item' and r['payload'].get('role') == 'user']
    require(prompt.strip() in {t.strip() for t in parent_texts}, 'Codex actual parent received saved prompt', checks)
    encrypted = [b['encrypted_content'] for r in cx['child'] if r.get('type') == 'response_item'
                 and r['payload'].get('type') == 'agent_message'
                 and r['payload'].get('author') == pm.get('agent_path', '/root')
                 and r['payload'].get('recipient') == cm['agent_path']
                 for b in r['payload'].get('content', []) if b.get('type') == 'encrypted_content']
    require(spawns[0]['message'] in encrypted, 'Codex encrypted delegation transport continuity (not plaintext)', checks)
    role = tomllib.loads((Path.home() / '.codex/agents/development-investigator.toml').read_text())
    texts = [b['text'] for r in cx['child'] if r.get('type') == 'response_item'
             and r['payload'].get('type') == 'message' and r['payload'].get('role') == 'developer'
             for b in r['payload'].get('content', []) if 'text' in b]
    require(role['developer_instructions'].strip() in {t.strip() for t in texts}, 'Codex exact role delivered', checks)
    policies = [r['payload'] for r in cx['child'] if r.get('type') == 'turn_context']
    require(bool(policies) and all(p['sandbox_policy'] == {'type': 'read-only'} and p['approval_policy'] == 'never'
            for p in policies), 'Codex effective read-only and no escalation', checks)
    require([p['permission_profile'] for p in policies] == audit['codex']['permission_profiles'],
            'Codex actual permission scope (includes root reads)', checks)
    final = [r['payload'] for r in cx['child'] if r.get('type') == 'response_item'
             and r['payload'].get('phase') == 'final_answer'][-1]
    require(json.loads(collector.text_content(final['content'])) == results['codex'], 'Codex original final matches', checks)
    d = read(HERE / 'claude-paid/workflow-and-parity-evidence.json')['native_claude_delivery']
    snapshot = cl['child'][d['execution_ready_snapshot_line']-1]['attachment']
    require([t['name'] for t in snapshot['tools']] == ['Read', 'Grep', 'Glob'], 'Claude exact ready tool catalog', checks)
    compiled = (skill_repo / 'distribution/agents/claude/development-investigator.md').read_text().split('---', 2)[2].strip()
    require(compiled in {p.strip() for p in snapshot['systemPrompt']}, 'Claude exact role delivered', checks)
    require(digest('\n'.join(snapshot['systemPrompt']).encode()) == d['system_prompt_sha256'], 'Claude observed prompt hash', checks)
    parent_calls = events(cl['parent'], 'claude')['calls']
    require(parent_calls[d['agent_tool_use_id']]['name'] == 'Agent' and all(
        r.get('agentId') == d['child_id'] and r.get('sessionId') == d['parent_session_id'] for r in cl['child']),
        'Claude native dispatch and child identity', checks)
    agent_inputs = [b['input'] for r in cl['parent']
                    for b in r.get('message', {}).get('content', [])
                    if isinstance(b, dict) and b.get('id') == d['agent_tool_use_id']]
    require(bool(agent_inputs) and all(a['subagent_type'] == 'development-investigator' and
            json.JSONDecoder().raw_decode(a['prompt'][a['prompt'].index('{'):])[0] == packet for a in agent_inputs),
            'Claude actual native dispatch carries identical frozen task', checks)
    raw = collector.text_content(cl['child'][d['final_child_line']-1]['message']['content'])
    require(digest(raw.encode()) == d['result_sha256'], 'Claude original raw final hash', checks)
    require(json.loads(raw.removeprefix('```json\n').removesuffix('\n```')) == results['claude'],
            'Claude only JSON framing removed; no answer correction', checks)
    require(all(c['name'] in {'Read', 'Grep', 'Glob'} and any(c['path'].endswith('/'+p)
                for p in packet['allowed_read_paths']) for c in audit['claude']['tool_events']['calls'].values()),
            'Claude observed read paths within frozen packet', checks)
    derived = {client: {kind: usage(rows, client) for kind, rows in pairs.items()} for client, pairs in native.items()}
    require(derived == audit['derived_usage'], 'usage derived from raw events, caches and streaming deduplicated', checks)
    probe = read(HERE / 'permission-probe.json')
    require(probe['exit_code'] == 0 and probe['expected_denials_verified'] and not probe['sentinel_exists_after'],
            'independent sandbox denial retained, not child denial', checks)
    judgments = behavior(semantics, derived, raw)
    return {'checks_passed': len(checks), 'checks_failed': 0, 'checks_errored': 0, 'checks_skipped': 0,
            'exit_status': 0, 'checks': checks, 'parity_traces_available': [f'{c}_{k}' for c in native for k in native[c]],
            'missing_required_trace': None, 'derived_usage': derived, 'semantic_review': semantics,
            'behavior_findings': audit['behavior_findings'], 'behavior_checks': judgments['checks'],
            'behavior_counts': judgments['counts'], 'behavior_verdict': judgments['verdict'],
            'cross_client_goal_complete': judgments['complete'],
            'limits': ['Integrity success is not behavior parity.', 'Semantic judgments are bound parent review, not automatic prose inference.',
                       'Five-file reads were voluntary; neither native read boundary enforces that allowlist.',
                       'Independent sandbox probe does not prove actual child denial or isolation from writable parent.',
                       'Hooks and compact Codex0.162 entrypoint were not exercised.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-parity', action='store_true')
    args = parser.parse_args()
    try:
        receipt = verify()
    except (AssertionError, ValueError, KeyError, OSError, jsonschema.ValidationError) as exc:
        print(json.dumps({'checks_failed': 1, 'exit_status': 1, 'error': str(exc)}))
        return 1
    if args.require_parity and not receipt['cross_client_goal_complete']:
        receipt['exit_status'] = 1
    (HERE / 'verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({k: receipt[k] for k in ('checks_passed', 'checks_failed', 'checks_errored',
          'checks_skipped', 'exit_status', 'parity_traces_available', 'behavior_verdict', 'cross_client_goal_complete')}))
    return receipt['exit_status']


if __name__ == '__main__':
    raise SystemExit(main())
