"""Write the per-plan sections of m5-disproof-sample.md from git, for the first 10 candidates."""
import json,subprocess,re,sys
rows=json.load(open(sys.argv[1]))[:10]
def g(p,*a): return subprocess.run(['git','-C',p,*a],capture_output=True,text=True).stdout
def durable_paths(p):
    y=g(p,'show','origin/main:.agentic/repo.yaml')
    blk=y.split('durable_documents:',1)[1] if 'durable_documents:' in y else ''
    out={}
    for m in re.finditer(r'^  (\w+):\s*(\S+)?\s*$',blk,re.M):
        k,v=m.group(1),m.group(2)
        if v and not v.startswith('"'): out[k]=[v]
    for m in re.finditer(r'^  system_model:\n((?:    .*\n)+)',blk,re.M):
        out['system_model']=re.findall(r':\s*(\S+)',m.group(1))
    return out
out=[]
for i,r in enumerate(rows,1):
    p=r['path']; rel=r['plan_ref'].split(p+'/')[-1]; txt=g(p,'show',f'origin/main:{rel}')
    line=next((l.strip() for l in txt.splitlines() if l.strip().startswith('Durable documents:')),None)
    num=re.match(r'(\d+)_',r['plan_id'])
    pat=rf"\[(Goal {re.escape(r['plan_id'])}|Plan #{num.group(1)})\]" if num else rf"\[Goal {re.escape(r['plan_id'])}\]"
    commits=g(p,'log','origin/main','-E',f'--grep={pat}','--format=%H').split()
    first,last=commits[-1],commits[0]
    base=g(p,'rev-parse',f'{first}^').strip()
    rng=f'{base[:12]}..{last[:12]}'
    stat=g(p,'diff','--stat=100',f'{base}..{last}').rstrip()
    out.append(f"### {i}. {r['repo']} `{r['plan_id']}`\n")
    out.append(f"- Plan file: `{rel}` (on `origin/main`); adoption receipt `completed_at` {r['adopted']}; last plan-tagged commit {r['last_commit']}.")
    out.append(f"- Durable-documents line: {('`'+line+'`') if line else '**absent** (no `Durable documents:` line in the plan)'}")
    out.append(f"- Commit range: `{rng}` (parent of the first to the last of the {len(commits)} commits tagged with this plan id; the range can include other writers' commits, so the declared-document diffs below use only the plan's own commits).")
    out.append(f"- Plan commits: {', '.join(c[:9] for c in reversed(commits))}\n")
    out.append("`git diff --stat` over the range:\n\n```text\n"+stat+"\n```\n")
    if line and not re.match(r'Durable documents:\s*none',line):
        dp=durable_paths(p); roles=[x.split('#')[0].strip() for x in line.split(':',1)[1].split(',')]
        for role in dict.fromkeys(roles):
            for path in ([rel] if role=='plans' else dp.get(role,[])):
                d=g(p,'log','-p','--reverse','--format=commit %h %s','origin/main','-E',f'--grep={pat}','--',path).rstrip()
                out.append(f"Full diff of declared role `{role}` (`{path}`), plan commits only:\n\n```diff\n{d or '(no change)'}\n```\n")
    else:
        dp=durable_paths(p); paths=[x for k,v in dp.items() if k!='plans' for x in v]
        touched=sorted(set(g(p,'log','origin/main','-E',f'--grep={pat}','--format=','--name-only','--',*paths).split())) if paths else []
        out.append(f"Declared durable paths on `origin/main` today (plans role excluded): {', '.join('`'+x+'`' for x in paths) or 'none declared'}. Touched by this plan's commits: {', '.join('`'+x+'`' for x in touched) or '**none**'}.\n")
        for t in touched:
            d=g(p,'log','-p','--reverse','--format=commit %h %s','origin/main','-E',f'--grep={pat}','--',t).rstrip()
            out.append(f"Full diff of `{t}`, plan commits only:\n\n```diff\n{d}\n```\n")
    out.append('Classification: **TBD**\n')
open(sys.argv[2],'w').write('\n'.join(out))
print(len('\n'.join(out)))
