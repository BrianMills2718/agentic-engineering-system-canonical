"""Detached local merge gate with retained output, timings and explicit exits."""
import json
import os
from pathlib import Path
import subprocess
import time

root = Path.cwd()
folder = root / 'proposals/trace-review-enforcement'
python = os.environ['AES_GATE_PYTHON']
provider = os.environ['AES_TRACE_REVIEW_TEST_PROVIDER']
env = os.environ.copy()
env.update(PYTHONPATH='src', AES_TRACE_REVIEW_COMMAND=provider)
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
steps = []
with (folder / 'final-gate.log').open('w') as log:
    for name, command in [('check', ['make', 'check', 'PYTHON=' + python]),
                          ('native', ['make', 'aes', 'AES_PYTHON=' + python])]:
        start = time.monotonic()
        print('BEGIN', name, flush=True)
        log.write('BEGIN ' + name + '\n'); log.flush()
        result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
        step = {'step': name, 'command': command, 'seconds': round(time.monotonic()-start, 2),
                'exit_status': result.returncode}
        steps.append(step)
        print(json.dumps(step), flush=True); log.write(json.dumps(step) + '\n'); log.flush()
        if result.returncode: break
outcome = {'revision': revision, 'steps': steps,
           'exit_status': next((s['exit_status'] for s in steps if s['exit_status']), 0)}
(folder / 'final-gate.json').write_text(json.dumps(outcome, indent=2) + '\n')
print(json.dumps(outcome), flush=True)
raise SystemExit(outcome['exit_status'])
