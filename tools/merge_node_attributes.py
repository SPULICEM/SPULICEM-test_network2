#!/usr/bin/env python3
"""Merge organization attributes (nodes_profile.xlsx) into the explorer data.

    python tools/merge_node_attributes.py path/to/nodes_profile.xlsx [path/to/nodes_city_base.xlsx]

The second file (default data/nodes_city_base.xlsx, skipped if absent) holds the "city base" flags:
São Paulo, São José dos Campos, Santos, Estado de SP, Federação, International. It must list the
same acronyms in the same row order as the profile sheet. Blank cells count as 0; a row that is
blank in every column is treated as "not recorded". When one acronym has several rows and no
crosswalk row is given (UNDRR), the city-base flags of those rows are combined (union).

Matching: a network node is matched to a sheet row by exact acronym (Sigla) unless
data/node_attribute_crosswalk.csv names a different row for it. Nodes with no match
keep no attributes (the platform shows them as "Not classified").

Writes data/node_attributes.csv (the node table: type, the three agenda flags, the match audit
and one column per theme holding the organization's number of coded mentions of it, 0 = not
discussed; themes come from the network data itself), adds `fn` (full name, from the sheet's Nome column), `t` (type), `b` (city base,
[SP, SJC, Santos, State, Federal, International]) and `a`
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

CITY_COLS = ["São Paulo", "São José dos Campos", "Santos", "Estado de SP", "Federação", "International"]
CITY_CSV = ["base_sao_paulo", "base_sao_jose_dos_campos", "base_santos", "base_state_sp", "base_federal", "base_international"]
city_path = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data" / "nodes_city_base.xlsx"
city = None
if city_path.exists():
    city = pd.read_excel(city_path)
    city.columns = ["sigla"] + CITY_COLS
    city["sigla"] = city["sigla"].astype(str).str.strip()
    assert list(city["sigla"]) == list(sheet["sigla"]), "city-base sheet must list the same acronyms in the same order as the profile sheet"

by_sigla = {}
for i, r in sheet.iterrows():
    by_sigla.setdefault(r.sigla, []).append(i)

cross = {}
with open(ROOT / "data" / "node_attribute_crosswalk.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        cross[r["graph_node"]] = r

graph = json.loads((ROOT / "data" / "processed_graph.json").read_text(encoding="utf-8"))

# theme columns, in natural order (T.1, T.2, ... T.20)
THEMES = sorted([(i, c) for i, c in enumerate(graph["cats"]) if c["type"] == "theme"],
                key=lambda ic: int(ic[1]["code"].split(".")[1]))
THEME_COLS = [f'{c["code"]} {c["label"]}' for _, c in THEMES]

def city_flags(idxs):
    """Union of the city-base flags over the given sheet rows; None when nothing is recorded."""
    if city is None: return None
    sub = city.loc[idxs, CITY_COLS]
    if sub.isna().all(axis=None): return None
    return [int(sub[c].fillna(0).max()) for c in CITY_COLS]

def flag(v):
    return None if pd.isna(v) else int(v)

rows, matched = [], 0
for n in graph["nodes"]:
    name, idx, how, cand = n["name"], None, "none", []
    if name in cross:
        c = cross[name]
        cand = by_sigla.get(c["sheet_sigla"].strip(), [])
        if c["sheet_row"]:
            idx = int(c["sheet_row"]) - 2          # Excel row number -> 0-based data index
        elif len(cand) >= 1:
            idx = cand[0]
        how = c["confidence"]
    elif name in by_sigla:
        cand = by_sigla[name]
        idx, how = cand[0], "exact"
    n.pop("t", None); n.pop("a", None); n.pop("fn", None); n.pop("b", None)
    th = [n["k"][i] for i, _ in THEMES]
    tail = [sum(1 for v in th if v > 0), *th]
    if idx is None:
        rows.append([name, "", "", "", "", "", *[""] * 6, "none", *tail]); continue
    b = city_flags([idx] if (name in cross and cross[name]["sheet_row"]) else (cand or [idx]))
    if b is not None: n["b"] = b
    r = sheet.loc[idx]
    t = None if pd.isna(r.tipo) else str(r.tipo).strip()
    a = [flag(r.res), flag(r.smart), flag(r.decarb)]
    if t: n["t"] = t
    full = " ".join(str(r.nome).split())
    if full and full.lower() != name.lower(): n["fn"] = full
    if any(x is not None for x in a): n["a"] = a
    matched += 1
    rows.append([name, r.nome, t or "", *("" if x is None else x for x in a),
                 *(b if b is not None else [""] * 6), how, *tail])

with open(ROOT / "data" / "node_attributes.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["graph_node", "sheet_name", "type", "resilient", "smart", "decarbonized", *CITY_CSV, "match",
                "themes_discussed", *THEME_COLS])
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
