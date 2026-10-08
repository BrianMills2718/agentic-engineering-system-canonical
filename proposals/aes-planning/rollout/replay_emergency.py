"""Replay the "Emergency: none" refusal over every [Unplanned] commit in ~/code since 2026-10-07 (ROLLOUT.md, 2026-10-08).

Run: PYTHONPATH=src .venv/bin/python proposals/aes-planning/rollout/replay_emergency.py"""
import glob, subprocess
from pathlib import Path
from agentic_engineering_system import commit_rule as c
hit=[];total=0
for g in glob.glob(str(Path.home() / 'code' / '*' / '.git')):
    r=g.split('/')[4]
    out=subprocess.run(['git','-C',g[:-5],'log','--all','--since=2026-10-07','--format=%h%x01%B%x02'],capture_output=True,text=True).stdout
    for rec in out.split('\x02'):
        if '\x01' not in rec: continue
        h,b=rec.strip().split('\x01',1)
        if not b.startswith('[Unplanned]'): continue
        total+=1
        lines=c.EMERGENCY_LINE_RE.findall(b)
        if lines and all(c.NO_EMERGENCY_RE.match(l) for l in lines):
            hit.append((r,h,lines[0][:70]))
print('Unplanned commits since 10-07:',total,' would now be refused:',len(hit))
for x in hit: print(' ',*x)
