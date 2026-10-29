#!/usr/bin/env python3
"""Merge organization attributes (nodes_profile.xlsx) into the explorer data.

    python tools/merge_node_attributes.py path/to/nodes_profile.xlsx

Matching: a network node is matched to a sheet row by exact acronym (Sigla) unless
data/node_attribute_crosswalk.csv names a different row for it. Nodes with no match
keep no attributes (the platform shows them as "Not classified").

Writes data/node_attributes.csv (audit table), adds `t` (type) and `a`
([resilient, smart, decarbonized]; null = not recorded) to every node in
data/processed_graph.json, and rewrites the DATA block embedded in platform.html.
Safe to re-run.
"""
import csv, json, re, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
xlsx = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "nodes_profile.xlsx"
sheet = pd.read_excel(xlsx)
sheet.columns = ["nome", "sigla", "tipo", "res", "smart", "decarb"]
sheet["sigla"] = sheet["sigla"].astype(str).str.strip()
sheet["nome"] = sheet["nome"].astype(str).str.strip()

by_sigla = {}
for i, r in sheet.iterrows():
    by_sigla.setdefault(r.sigla, []).append(i)

cross = {}
with open(ROOT / "data" / "node_attribute_crosswalk.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        cross[r["graph_node"]] = r

graph = json.loads((ROOT / "data" / "processed_graph.json").read_text(encoding="utf-8"))

def flag(v):
    return None if pd.isna(v) else int(v)

rows, matched = [], 0
for n in graph["nodes"]:
    name, idx, how = n["name"], None, "none"
    if name in cross:
        c = cross[name]
        cand = by_sigla.get(c["sheet_sigla"].strip(), [])
        if c["sheet_row"]:
            idx = int(c["sheet_row"]) - 2          # Excel row number -> 0-based data index
        elif len(cand) >= 1:
            idx = cand[0]
        how = c["confidence"]
    elif name in by_sigla:
        idx, how = by_sigla[name][0], "exact"
    n.pop("t", None); n.pop("a", None)
    if idx is None:
        rows.append([name, "", "", "", "", "", "none"]); continue
    r = sheet.loc[idx]
    t = None if pd.isna(r.tipo) else str(r.tipo).strip()
    a = [flag(r.res), flag(r.smart), flag(r.decarb)]
    if t: n["t"] = t
    if any(x is not None for x in a): n["a"] = a
    matched += 1
    rows.append([name, r.nome, t or "", *("" if x is None else x for x in a), how])

with open(ROOT / "data" / "node_attributes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["graph_node", "sheet_name", "type", "resilient", "smart", "decarbonized", "match"])
    w.writerows(rows)

(ROOT / "data" / "processed_graph.json").write_text(
    json.dumps(graph, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

html_path = ROOT / "platform.html"
html = html_path.read_text(encoding="utf-8")
new_data = "const DATA = " + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + ";"
html, k = re.subn(r"const DATA = \{.*?\};(?=\n)", lambda m: new_data, html, count=1, flags=re.S)
assert k == 1, "DATA block not found in platform.html"
html_path.write_text(html, encoding="utf-8")
print(f"{matched}/{len(graph['nodes'])} nodes matched; wrote node_attributes.csv, processed_graph.json, platform.html")
