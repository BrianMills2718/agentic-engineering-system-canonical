"""Reproduce two existing check defects; this does not implement their repair.

Pass the Project Meta checkout whose pinned revision is in sources.json.
Only the observation boundary is synthetic. The check functions are real.
"""
import json
import sys
from pathlib import Path
from unittest.mock import patch

if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 probe.py <project-meta-checkout>')
project = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(project / 'scripts'))
import control_triggers as checks
import hook_receipt_index as receipts

partial = receipts.IndexResult(
    rows=[],
    coverage=receipts.Coverage(
        sessions_in_window=3,
        sessions_fully_read=0,
        sessions_partially_read=1,
        budget_exhausted=True,
    ),
    as_of='2026-10-06T00:00:00+00:00',
)
results = []
with patch.object(checks, '_index_result', return_value=partial):
    result = checks.hook_latency_p90({'window_days': 7, 'threshold': 1500}, project)
    results.append({'case': 'incomplete-receipt-coverage', 'observed': result.status,
                    'desired': 'unknown', 'evidence': result.evidence})
with patch.object(checks, '_index_result', return_value=partial), patch.object(
    checks, '_enforced_session_hook_rows',
    return_value=[{'id': 'synthetic-unmapped-control', 'linked_scripts': []}],
):
    result = checks.enforced_without_receipts({'window_days': 14}, project)
    results.append({'case': 'unmapped-required-control', 'observed': result.status,
                    'desired': 'unknown', 'evidence': result.evidence})
reproduced = sum(row['observed'] == 'clear' for row in results)
print(json.dumps({'results': results, 'reproduced': reproduced, 'not_reproduced': 2 - reproduced,
                  'exit': 0 if reproduced == 2 else 1,
                  'meaning': 'Reproduction success means the existing false-clear defects remain present.'}, indent=2))
raise SystemExit(0 if reproduced == 2 else 1)
