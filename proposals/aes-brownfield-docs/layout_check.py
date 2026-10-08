#!/usr/bin/env python3
"""layout_check.py REPO [REF] : is the repository's documentation organized in its declared AES layout?

Reads .agentic/repo.yaml at REF (default HEAD) and reports a finding for each of:
  root-missing        a declared normative, decision or plan root holds no tracked file
  decision-outside    an ADR-* file, or a file in a folder named decisions/, outside every decision root
  design-outside      a file in a folder named architecture/ outside every normative root
  plan-outside        a numbered plan file (NNN_name.md) outside every plan root
  generated-outside   a generator output (a *OUTPUT* Path constant in a .py file, or a Makefile
                      --output-root / --output argument) outside generated/
Folders a repository keeps on purpose can be listed in .md-file-cap.yaml `layout_ok` with a reason.
Uses paths, file names and code assignments only, never document prose. Exits 1 on any finding.
"""
import os, re, subprocess, sys

repo = sys.argv[1]
ref = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "HEAD"
git = lambda *a: subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout
try:
    import yaml
except ImportError:
    sys.exit("PyYAML required")
cfg = yaml.safe_load(git("show", f"{ref}:.agentic/repo.yaml") or "{}") or {}
if not cfg:
    print("no .agentic/repo.yaml; layout not declared   exit 1")
    sys.exit(1)
roots = cfg.get("authorities") or {}
norm = [r.rstrip("/") + "/" for r in roots.get("normative_roots") or []]
dec = [r.rstrip("/") + "/" for r in roots.get("decision_roots") or []]
plans = [r.rstrip("/") + "/" for r in roots.get("plan_roots") or []]
cap = yaml.safe_load(git("show", f"{ref}:.md-file-cap.yaml") or "{}") or {}
keep = [(str(e["path"]).rstrip("/") + "/", str(e.get("reason") or "").strip()) for e in cap.get("layout_ok") or []]
bad_keep = [p for p, r in keep if not r]
tracked = git("ls-tree", "-r", "--name-only", ref).splitlines()
inside = lambda p, rs: any(p.startswith(r) for r in rs)
kept = lambda p: any(p == k.rstrip("/") or p.startswith(k) for k, _ in keep)  # a file or a folder
outputs = set()
for f in (p for p in tracked if p.endswith(".py")):
    outputs.update(re.findall(r"^\s*\w*OUTPUT\w*\s*=\s*Path\(\s*[\"']([^\"']+)[\"']", git("show", f"{ref}:{f}"), re.M | re.I))
mk = git("show", f"{ref}:Makefile")
outputs.update(re.findall(r"--output(?:-root)?[ =]+([\w./-]+)", mk))
gen_roots = [o.lstrip('./').rstrip('/') + '/' for o in outputs]
findings = []
for r in norm + dec + plans:
    if not any(p.startswith(r) for p in tracked):
        findings.append(("root-missing", r))
for p in tracked:
    if not p.lower().endswith(".md") or kept(p) or os.path.basename(p) in ("CLAUDE.md", "AGENTS.md", "README.md", "INDEX.md"):
        continue
    parts = p.split("/")
    if p.startswith("generated/") or any(p == g.rstrip("/") or p.startswith(g) for g in gen_roots):
        continue  # generator output is judged by the generated-outside rule, not as a record
    if "okf" in parts[:-1]:
        continue  # OKF knowledge bundles hold typed concepts about the organization, not this repository's own decisions or design
    if (re.match(r"ADR[-_]", os.path.basename(p)) or "decisions" in parts[:-1]) and not inside(p, dec):
        findings.append(("decision-outside", p))
    elif "architecture" in parts[:-1] and not inside(p, norm):
        findings.append(("design-outside", p))
    elif re.match(r"\d{2,4}_[\w.-]+\.md$", os.path.basename(p)) and not inside(p, plans):
        findings.append(("plan-outside", p))
for o in sorted(outputs):
    o = o.lstrip("./").rstrip("/")
    committed = any(p == o or p.startswith(o + "/") for p in tracked)  # runtime outputs that are never committed are not documentation
    if o and committed and not o.startswith("generated/") and not kept(o) and not o.startswith(("$", "/tmp")):
        findings.append(("generated-outside", o))
for p in bad_keep:
    findings.append(("layout-ok-without-reason", p))
counts = {}
for k, _ in findings:
    counts[k] = counts.get(k, 0) + 1
show = "--list" in sys.argv
for k, p in findings if show else findings[:25]:
    print(f"  {k:<20} {p}")
if not show and len(findings) > 25:
    print(f"  ... {len(findings) - 25} more (use --list)")
print(f"{os.path.basename(os.path.abspath(repo))} @ {ref}: layout findings {len(findings)} " + (str(counts) if counts else "") + f"   exit {1 if findings else 0}")
sys.exit(1 if findings else 0)
