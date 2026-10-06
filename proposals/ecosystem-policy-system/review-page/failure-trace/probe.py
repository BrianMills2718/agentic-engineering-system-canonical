"""Trace real Project Meta readers and routing with isolated observation/issue fixtures.

Success reproduces defects; it does not certify that the system is repaired.
No live receipt store or GitHub issue is read or changed by this probe.
"""
import contextlib
import hashlib
import io
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

project = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
sys.dont_write_bytecode = True
revision = subprocess.check_output(['git', '-C', str(project), 'rev-parse', 'HEAD'], text=True).strip()
paths = ['scripts/control_triggers.py', 'scripts/hook_receipt_index.py',
         'scripts/policy_system_status.py', 'scripts/run_local_daily_audit.sh', 'policy/control_triggers.yaml']
pins = []
for name in paths:
    committed = subprocess.check_output(['git', '-C', str(project), 'show', f'{revision}:{name}'])
    assert committed == (project / name).read_bytes(), f'Uncommitted subject: {name}'
    pins.append({'path': name, 'revision': revision, 'sha256': hashlib.sha256(committed).hexdigest()})
sys.path.insert(0, str(project / 'scripts'))
import control_triggers as checks
import hook_receipt_index as receipts

results = []
cases = []
def verify(name, condition, evidence):
    results.append({'name': name, 'outcome': 'passed' if condition else 'failed', 'evidence': evidence})

class IsolatedConcerns:
    def __init__(self):
        self.actions = []
    def find_existing(self, *args):
        return {'number': 7, 'state': 'OPEN'}
    def close_concern(self, repo, key, evidence, run):
        self.actions.append({'action': 'close', 'key': key, 'evidence': evidence})
        return 'fixture concern closed'
    def open_concern(self, repo, key, *args, **kwargs):
        self.actions.append({'action': 'open', 'key': key})
        return 'fixture concern opened'

def no_external_command(*args):
    raise AssertionError('The isolated probe must not execute external concern commands')

with tempfile.TemporaryDirectory(prefix='evidence-flow-') as directory:
    root = Path(directory)
    receipt_root = root / 'receipts'
    (receipt_root / 'fixture-session').mkdir(parents=True)
    partial = receipts.refresh_and_load(receipt_root=receipt_root, index_dir=root / 'index',
                                       budget_seconds=0, window_days=7)
    coverage = partial.coverage.__dict__
    verify('real index reports unread evidence', partial.rows == [] and coverage['sessions_in_window'] == 1
           and coverage['sessions_fully_read'] == 0 and coverage['budget_exhausted'], coverage)
    trigger = {'id': 'hook-latency-p90', 'window_days': 7, 'threshold': 1500,
               'observe': 'slow hook wall time', 'source': 'fixture observation', 'cadence': 'weekly'}
    with patch.object(checks, '_index_result', return_value=partial):
        rows = checks.evaluate([trigger], project)
    cases.append({'id': 'partial-empty', 'expected': 'unknown', 'observed': rows[0]['status'],
                  'evidence': rows[0]['evidence']})
    verify('partial empty evidence reproduces false clear', rows[0]['status'] == 'clear', rows[0])

    low_partial = receipts.IndexResult(rows=[{'hook_name': 'fixture-fast-hook', 'elapsed_ms': 100}],
                                      coverage=partial.coverage, as_of=partial.as_of)
    with patch.object(checks, '_index_result', return_value=low_partial):
        low = checks.hook_latency_p90(trigger, project)
    cases.append({'id': 'partial-low', 'expected': 'unknown', 'observed': low.status, 'evidence': low.evidence})
    verify('a fast observed sample does not restore missing coverage', low.status == 'clear', low.evidence)

    complete = receipts.IndexResult(rows=[], coverage=receipts.Coverage(sessions_in_window=1,
                                    sessions_fully_read=1), as_of=partial.as_of)
    with patch.object(checks, '_index_result', return_value=complete), patch.object(
        checks, '_enforced_session_hook_rows', return_value=[{'id': 'fixture-unmapped', 'linked_scripts': []}]
    ):
        unmapped = checks.enforced_without_receipts({'window_days': 14}, project)
    cases.append({'id': 'complete-unmapped', 'expected': 'unknown', 'observed': unmapped.status,
                  'evidence': unmapped.evidence})
    verify('unmapped control reproduces false clear independently of coverage',
           unmapped.status == 'clear' and 'fixture-unmapped' in unmapped.evidence, unmapped.evidence)

    (root / 'policy').mkdir()
    (root / 'policy/registry.yaml').write_text('policies: []\n')
    table = root / 'triggers.yaml'
    import yaml
    table.write_text(yaml.safe_dump({'schema': 'control-triggers/v1', 'review_window_days': 7,
                                    'triggers': [trigger]}))
    registry = IsolatedConcerns()
    report_path = root / 'report.json'
    printed = io.StringIO()
    with patch.object(checks, '_index_result', return_value=partial), patch.object(
        checks, '_load_concern_issue', return_value=registry
    ), contextlib.redirect_stdout(printed):
        code = checks.main(['--repo', 'fixture/isolated', '--repo-root', str(root), '--table', str(table),
                            '--report', str(report_path)], run=no_external_command)
    report = json.loads(report_path.read_text())
    verify('real CLI preserves clear in its report and exits successfully',
           code == 0 and report['triggers'][0]['status'] == 'clear', {'exit': code, 'report': report})
    verify('real routing attempts to close the isolated concern',
           [a['action'] for a in registry.actions] == ['close'] and
           [a['key'] for a in registry.actions] == ['trigger:hook-latency-p90'], registry.actions)
    downstream = {'cli_exit': code, 'report_status': report['triggers'][0]['status'],
                  'actions': registry.actions, 'stdout': printed.getvalue(), 'issue_store': 'isolated fixture'}

    unknown_registry = IsolatedConcerns()
    with patch.object(checks, '_index_result', side_effect=checks.Unreadable('fixture source unreadable')):
        unknown_rows = checks.evaluate([trigger], project)
    with patch.object(checks, '_load_concern_issue', return_value=unknown_registry):
        checks.route(unknown_rows, 'fixture/isolated', no_external_command, datetime.now(timezone.utc), 3, False, 7)
    verify('unknown preserves the concern in the existing router',
           unknown_rows[0]['status'] == 'unknown' and unknown_registry.actions == [], unknown_rows)

    slow = receipts.IndexResult(rows=[{'hook_name': 'fixture-slow-hook', 'elapsed_ms': 2000}],
                               coverage=complete.coverage, as_of=partial.as_of)
    fired_registry = IsolatedConcerns()
    with patch.object(checks, '_index_result', return_value=slow):
        fired_rows = checks.evaluate([trigger], project)
    with patch.object(checks, '_load_concern_issue', return_value=fired_registry):
        checks.route(fired_rows, 'fixture/isolated', no_external_command, datetime.now(timezone.utc), 3, False, 7)
    verify('observed slow evidence opens rather than closes a concern', fired_rows[0]['status'] == 'fired'
           and fired_registry.actions == [{'action': 'open', 'key': 'trigger:hook-latency-p90'}], fired_registry.actions)

failed = sum(r['outcome'] == 'failed' for r in results)
payload = {'schema': 'ecosystem-evidence-flow/v1', 'observed_at': datetime.now(timezone.utc).isoformat(),
           'subject': {'repository': 'BrianMills2718/project-meta', 'revision': revision, 'sources': pins},
           'boundary': 'Real index/check/CLI/router; temporary observations and isolated concern adapter',
           'cases': cases, 'downstream': downstream, 'checks': results,
           'counts': {'passed': len(results) - failed, 'failed': failed, 'errored': 0, 'skipped': 0},
           'exit_status': 1 if failed else 0,
           'meaning': 'Passing checks reproduce false-clear defects. No repair or live issue closure is claimed.'}
output.write_text(json.dumps(payload, indent=2) + '\n')
print(json.dumps({'counts': payload['counts'], 'exit_status': payload['exit_status'],
                  'cases': [{k: c[k] for k in ('id', 'expected', 'observed')} for c in cases],
                  'downstream': {'cli_exit': code, 'actions': [a['action'] for a in registry.actions]},
                  'meaning': payload['meaning']}, indent=2))
raise SystemExit(payload['exit_status'])
