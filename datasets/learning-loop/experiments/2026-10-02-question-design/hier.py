import json, os, glob, sys, urllib.request, math
from v2lib import F, key
GROUPS = {
 "evidence_and_claims": ("A belief or claim went wrong: stated without the check that would refute it, observed from the wrong place, untested reasoning, a partial list read as complete, building before checking what exists.", "A check or test that ran but was broken (checks_and_tests); a rule or gate problem (rules_and_controls).", "U V B Q R T"),
 "checks_and_tests": ("A verification mechanism itself was weak: a check that cannot fail, parts tested but never the whole, an empty or zero result read as success, one bad record hiding a batch.", "A claim made with no check at all (evidence_and_claims).", "A C M X"),
 "rules_and_controls": ("A rule, gate, policy, authority or official route misbehaved: never fires, costs too much, conflicts with another rule, the official route is broken, or an agent's scope or authority drifted.", "A plain mistake in reasoning or state (evidence_and_claims, state_and_targets).", "D F J N S"),
 "state_and_targets": ("Operations on state went wrong: copies left stale, steps run in a breaking order, the wrong object selected, one object with two identities, an unbounded default.", "A claim or report about state that was wrong (evidence_and_claims).", "E K L Y W"),
 "communication_and_priorities": ("Nothing technical was wrong, but the report failed its reader, or the work could not matter because what it depends on had stopped.", "Technical failures.", "G O"),
}
q = {"group": {"type":"choice","instructions":"Which kind of failure does this learning record?",
     "criteria": {**{g:{"what":w,"not_for":nf} for g,(w,nf,_) in GROUPS.items()},
                  "other":{"what":"A real reasoning or control failure that none of the other options describes.","not_for":"Plain facts about how a tool or product behaves (not_a_failure)."},
                  "not_a_failure":{"what":"A plain fact, behaviour or gotcha of a tool or product; nobody's reasoning or control went wrong.","not_for":"Cases where an agent or system made a mistake because of that behaviour."}}}}
for g,(_,_,fams) in GROUPS.items():
    q["in_"+g] = {"type":"choice","instructions":"Which specific failure does this learning record?","criteria":{F[l][0]:{"what":F[l][1],"not_for":F[l][2]} for l in fams.split()}}
n2l = {v[0]:k for k,v in F.items()}
def run(items, out):
    rows=[]
    for k, txt, ra, acc in items:
        state={"learning":txt[:1800],"recommended_action":ra[:400]}
        req=urllib.request.Request("https://openrouter.ai/api/v1/systemone",data=json.dumps({"model":"typesafe/jev-1.13","state":state,"questions":q}).encode(),headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
        r=json.loads(urllib.request.urlopen(req,timeout=120).read()); a=r["answers"]
        gp=a["group"]["probabilities"]; paths={}
        for g,p in gp.items():
            if g in GROUPS:
                for fam,pf in a["in_"+g]["probabilities"].items(): paths[n2l[fam]]=p*pf
            else: paths[g]=p
        rows.append({"key":k,"acc":acc,"group_choice":a["group"]["choice"],"group_conf":a["group"]["confidence"],"group_probs":gp,"paths":paths,"cost":r.get("usage",{}).get("cost")})
    json.dump(rows,open(out,"w"),indent=1)
docs={d.get("entry_id"):d for d in (json.load(open(f)) for f in glob.glob(os.path.expanduser("~/code/project-meta/learnings/entries/*.json")))}
def t(d): return str(d.get("learning") or d.get("finding") or d.get("lesson") or "")
ho=[(k,t(docs[k]),str(docs[k].get("recommended_action") or ""),a.split()) for k,a in (l.split("\t") for l in open("holdout_gt.tsv").read().strip().split("\n"))]
ho+=[(k,x,"",a.split()) for k,(x,a) in json.load(open("synthetic.json")).items()]
tuned=[]
for k,a in (l.split("\t") for l in open("gt.tsv").read().strip().split("\n")):
    d=docs.get(k) or next(d for d in reversed(list(docs.values())) if k in t(d))
    tuned.append((k,t(d),str(d.get("recommended_action") or ""),a.split()))
run(ho,"hier_holdout.json"); run(tuned,"hier_tuned.json")
