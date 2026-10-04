#!/usr/bin/env python3
"""Throwaway prototype: derive diagram data from an AES target (optionally + a proposal overlay).

Usage: extract.py <target.yaml> [--proposal P.yaml] [--repo ROOT] [--only-delta] > model.json

Everything in the output comes from target records, except wires with source
"realized-imports", which are read from the repository's Python imports because
the current target has no typed signatures to derive wires from (that gap is the point).
"""
import argparse, ast, json, re, sys
from pathlib import Path
import yaml

TRIVIAL = {"Path", "str", "int", "bool", "None", "dict", "list", "Any", "set[str]", "list[str]",
           "dict[str, Any]", "Sequence[str] | None", "datetime | None"}


def overlay(target, proposal):
    delta = proposal["target_delta"]
    changed = set()
    for fam, entries in (delta.get("change") or {}).items():
        key = "evidence_requirement_ref" if fam == "external_boundaries" else "id"
        for e in entries:
            target[fam] = [e if m[key] == e[key] else m for m in target[fam]]
            changed.add(e[key])
    for fam, entries in (delta.get("add") or {}).items():
        key = "evidence_requirement_ref" if fam == "external_boundaries" else "id"
        target.setdefault(fam, []).extend(entries)
        changed.update(e[key] for e in entries)
    return changed


def parse_sig(entry):
    if "(" not in entry:
        return {"name": entry, "args": [], "ret": None, "typed": False}
    fn = ast.parse(f"def {entry}:\n    pass\n").body[0]
    args = [(a.arg, ast.unparse(a.annotation) if a.annotation else None) for a in fn.args.args]
    ret = ast.unparse(fn.returns) if fn.returns else None
    return {"name": fn.name, "args": args, "ret": ret, "typed": True}


def base_types(t):
    """'list[GateFinding]' -> {'list[GateFinding]', 'GateFinding'}."""
    if t is None:
        return set()
    out = {t}
    m = re.fullmatch(r"(?:list|set|tuple)\[(\w+)\]", t)
    if m:
        out.add(m.group(1))
    return out - TRIVIAL


def short(text, n=70):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1].rsplit(" ", 1)[0] + "…"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--proposal")
    ap.add_argument("--repo")
    ap.add_argument("--only-delta", action="store_true")
    a = ap.parse_args()
    t = yaml.safe_load(open(a.target))
    changed = overlay(t, yaml.safe_load(open(a.proposal))) if a.proposal else set()

    arts = {x["id"]: x for x in t["planned_artifacts"]}
    path_to_comp = {}
    comps = []
    for c in t["components"]:
        files, tests, exports = [], [], []
        for ref in c["planned_artifact_refs"]:
            art = arts[ref]
            p = art["locator"]["exact_path"]
            path_to_comp[p] = c["id"]
            (tests if art["kind"] == "test" else files).append(Path(p).name)
            for e in art.get("exports", []):
                s = parse_sig(e)
                s["artifact"] = ref
                exports.append(s)
        comps.append({
            "id": c["id"], "label": c["id"].replace("RU-AES-", "").title(),
            "files": files, "tests": tests, "exports": exports,
            "criteria": [r for r in c["target_refs"] if r.startswith("SC-")],
            "new": c["id"] in changed,
            "touched": c["id"] in changed or any(r in changed for r in c["planned_artifact_refs"]),
        })

    ext = {b["evidence_requirement_ref"] for b in t.get("external_boundaries", [])}
    criteria = []
    for sc in t["success_criteria"]:
        proofs = [{"id": v["id"], "role": v["proof_role"], "kind": v["proof_kind"]}
                  for v in t["verification_subjects"] if sc["id"] in v["criterion_refs"]]
        ers = [er["id"] for er in sc["evidence_requirements"]]
        criteria.append({"id": sc["id"], "text": short(sc["statement"]), "proofs": proofs,
                         "external": [e for e in ers if e in ext], "new": sc["id"] in changed})

    wires = []
    # plan-derived wires: a typed export's return type is another typed export's argument type
    for prod in comps:
        for pe in prod["exports"]:
            if not pe["typed"]:
                continue
            for cons in comps:
                for ce in cons["exports"]:
                    if not ce["typed"] or ce is pe:
                        continue
                    # exact type match first, then element-type match; each input port takes one wire
                    taken = {w["to_arg"] for w in wires if w["to"] == cons["id"] and w["to_port"] == ce["name"]}
                    cands = [(0 if pe["ret"] == ann else 1, arg, base_types(pe["ret"]) & base_types(ann))
                             for arg, ann in ce["args"] if arg not in taken]
                    cands = sorted(c for c in cands if c[2])
                    if cands:
                        _, arg, hit = cands[0]
                        wires.append({"from": prod["id"], "from_port": pe["name"], "to": cons["id"],
                                      "to_port": ce["name"], "to_arg": arg, "label": pe["ret"],
                                      "ambiguous": len([c for c in cands if c[0] == cands[0][0]]) > 1,
                                      "source": "plan-types"})
    if a.repo:  # realized imports between planned source files
        pkg = "agentic_engineering_system"
        for p, cid in path_to_comp.items():
            fp = Path(a.repo) / p
            if not fp.suffix == ".py" or not fp.exists() or not p.startswith("src/"):
                continue
            for node in ast.walk(ast.parse(fp.read_text())):
                if isinstance(node, ast.ImportFrom) and node.module and (node.level == 1 or node.module.startswith(pkg)):
                    mod = node.module.split(".")[-1]
                    src = f"src/{pkg}/{mod}.py"
                    pc = path_to_comp.get(src)
                    if pc and pc != cid:
                        for n in node.names:
                            wires.append({"from": pc, "from_port": n.name, "to": cid, "to_port": None,
                                          "label": n.name, "source": "realized-imports"})
    seen, uniq = set(), []
    for w in wires:
        k = (w["from"], w["from_port"], w["to"], w["to_port"])
        if k not in seen:
            seen.add(k)
            uniq.append(w)
    if a.only_delta:
        keep = {c["id"] for c in comps if c["touched"]}
        keep |= {w["from"] for w in uniq if w["to"] in keep} | {w["to"] for w in uniq if w["from"] in keep}
        comps = [c for c in comps if c["id"] in keep]
        uniq = [w for w in uniq if w["from"] in keep and w["to"] in keep]
        crit_keep = {s for c in comps if c["touched"] for s in c["criteria"]}
        criteria = [s for s in criteria if s["id"] in crit_keep]
    json.dump({"target_id": t["target_id"], "proposal": a.proposal and Path(a.proposal).name,
               "components": comps, "criteria": criteria, "wires": uniq}, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
