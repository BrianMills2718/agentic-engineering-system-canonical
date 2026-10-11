import json,subprocess,re,os,sys
LIVE="2026-10-10T23:54:42Z"
EXCL={"aes-durable-docs","61_durable_documents_gate","62_quick_adopt_reliability","63_durable_docs_pilot","durable-docs-docstring","system-model-arc42"}
inv=json.load(open(sys.argv[1]))
repos=inv['repos'] if isinstance(inv,dict) and 'repos' in inv else inv
paths={os.path.expanduser(r.get('path') or r.get('local_path')) for r in repos if (r.get('path') or r.get('local_path'))}
paths|={os.path.expanduser('~/code/company-planning'),os.path.expanduser('~/code/agentic-engineering-system-canonical')}
def g(p,*a): return subprocess.run(['git','-C',p,*a],capture_output=True,text=True).stdout
rows=[]
for p in sorted(paths):
    if not os.path.isdir(p): print("MISSING",p,file=sys.stderr); continue
    g(p,'fetch','-q','origin')
    for f in g(p,'ls-tree','-r','--name-only','origin/main').splitlines():
        if not f.endswith('receipt.json'): continue
        try: d=json.loads(g(p,'show',f'origin/main:{f}'))
        except Exception: continue
        if d.get('record_type')!='planning_method_conformance_receipt': continue
        ca=d.get('completed_at','')
        if ca<LIVE: continue
        ref=d['plan']['plan_ref']; pid=os.path.basename(ref)
        pid=re.sub(r'\.md$','',pid)
        if pid=='PLAN': pid=os.path.basename(os.path.dirname(ref))
        if pid in EXCL: continue
        num=re.match(r'(\d+)_',pid)
        pat=rf'\[(Goal {re.escape(pid)}|Plan #{num.group(1)})\]' if num else rf'\[Goal {re.escape(pid)}\]'
        log=g(p,'log','origin/main','-E',f'--grep={pat}','--format=%H %cI')
        lines=log.split('\n'); lines=[l for l in lines if l]
        last=lines[0].split()[1] if lines else ''
        rows.append(dict(repo=os.path.basename(p),path=p,plan_id=pid,plan_ref=ref,adopted=ca,last_commit=last,commits=len(lines),first=lines[-1].split()[0] if lines else '',lastsha=lines[0].split()[0] if lines else ''))
rows=[r for r in rows if r['commits']>0]
rows.sort(key=lambda r:r['last_commit'],reverse=True)
json.dump(rows,open(sys.argv[2],'w'),indent=1)
for i,r in enumerate(rows): print(i+1,r['repo'],r['plan_id'],r['adopted'],r['last_commit'],r['commits'])
