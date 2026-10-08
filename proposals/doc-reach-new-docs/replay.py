"""Replay: commits since 2026-10-07 in Brian-owned repos that ADD .md files; are the added files
reachable from wiki/index.md within 2 links at that commit (daily-check rules)?"""
import sys, subprocess, glob, collections, json
sys.path.insert(0, '/home/brian/code/project-meta/scripts')
import md_file_cap as m
rows=[]; per=collections.Counter(); kinds=collections.Counter()
for g in sorted(glob.glob('/home/brian/code/*/.git')):
    top=g[:-5]
    slug=(m.remote_slug(top) or '')
    if not slug.lower().startswith(('brianmills2718/','brianmills-spec/')): continue
    log=m.git(top,'log','--since=2026-10-07','--no-merges','--diff-filter=A','--name-only','--format=@@%h %s','origin/HEAD') or ''
    cur=None; added={}
    for line in log.splitlines():
        if line.startswith('@@'): cur=line[2:]; added[cur]=[]
        elif line.strip().lower().endswith('.md') and cur: added[cur].append(line.strip())
    for c,files in added.items():
        if not files: continue
        h=c.split()[0]
        r=m.reachability(top,h)
        bad=set(r['orphans'])|set(r['beyond'])
        hit=[f for f in files if f in bad]
        rows.append((top.split('/')[-1],c[:70],len(files),len(hit),r['status'],hit[:3]))
        per[top.split('/')[-1]]+=1 if hit else 0
        kinds['commits_adding_md']+=1; kinds['would_refuse']+=1 if hit else 0
        if hit and r['status']=='no-wiki': kinds['refuse_no_wiki']+=1
        for f in hit:
            k='plan' if f.startswith(('proposals/','docs/plans/')) else 'other'
            kinds['unreached_'+k]+=1
print(json.dumps(kinds)); print(per.most_common(15))
for r in rows:
    if r[3]: print(r)
