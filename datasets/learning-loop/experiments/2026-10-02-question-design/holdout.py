import json, os, glob, urllib.request
from v2lib import Q, key, name2letter
GT = {l.split("\t")[0]: l.split("\t")[1].split() for l in open("holdout_gt.tsv").read().strip().split("\n")}
syn = json.load(open("synthetic.json"))
docs = {d.get("entry_id"): d for d in (json.load(open(f)) for f in glob.glob(os.path.expanduser("~/code/project-meta/learnings/entries/*.json")))}
items = [(k, str(docs[k].get("learning") or docs[k].get("finding") or docs[k].get("lesson") or ""), str(docs[k].get("recommended_action") or ""), acc) for k, acc in GT.items()]
items += [(k, t, "", a.split()) for k, (t, a) in syn.items()]
rows = []
for k, txt, ra, acc in items:
    state = {"learning": txt[:1800], "recommended_action": ra[:400]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/systemone", data=json.dumps({"model":"typesafe/jev-1.13","state":state,"questions":Q}).encode(), headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"}, method="POST")
    r = json.loads(urllib.request.urlopen(req, timeout=120).read()); a = r["answers"]["kind"]
    rows.append({"key":k,"acc":acc,"choice":name2letter.get(a["choice"],a["choice"]),"confidence":a.get("confidence"),"probs":{name2letter.get(n,n):p for n,p in a["probabilities"].items()},"cost":r.get("usage",{}).get("cost")})
json.dump(rows, open("holdout_out.json","w"), indent=1)
