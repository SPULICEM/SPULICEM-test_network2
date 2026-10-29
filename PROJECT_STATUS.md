# Governing Resilient Cities — project status

Last updated: 29 October 2026 (node attribute filter added). This file is a handoff summary: what exists,
what's still open, and what to tell Claude if you pick this project back up
in a new conversation.

## What this project is

A public website for the CCD: Carbon Neutral Cities project, presenting
research on governance arrangements for smart, resilient and sustainable
cities in São Paulo, Santos and São José dos Campos — built around a network
analysis of 124 organisations and the discourses (concepts, solutions and
themes) they share.

## The five pages

| Page | File | What it does |
|---|---|---|
| Welcome | `index.html` | Landing page: project framing, live animated network snapshots (real data), the "Step by step" guide, partner logos, project/funding details. |
| Short introduction | `intro.html` | The theoretical pitch in plain language — why a network/discourse-affinity approach, the central research question. |
| How it works | `how.html` | Walks through the method with real-data figures: an animated full network view, a two-tie example, community convergence, a real community profile, a real "most similar profiles" (cosine similarity) example. |
| Scientific basis | `scientific-basis.html` | The academic grounding: policy coherence literature, the Advocacy Coalition Framework, discourse networks, research questions, four hypotheses, full reference list with working in-text citation links. |
| Platform | `platform.html` | The interactive explorer itself — Network / Communities / Organizations / Centrality / Discourses tabs, a category filter and an organization filter (type + city agenda) that rebuild ties and recompute communities live, multiple layouts (force, Fruchterman–Reingold, Yifan Hu, stress/MDS, circular, radial), a guided tour, light/dark theme. |

All five are self-contained HTML files with everything (styling, fonts
fallback, the charting library, the data, the partner logos) embedded inline
— no build step, no external dependencies beyond Google Fonts. `README.md`
has the steps to publish them on GitHub Pages.

## Data

- `data/network_twomode_combined_1.csv` and `data/network_onemode_combined.csv`
  — the source files behind the current platform (124 organisations; concept,
  solution and theme discourse coding; the one-mode tie matrix).
- `data/processed_graph.json` — the derived dataset actually embedded in
  `platform.html`: node list with community assignments, centralities,
  per-category mention counts, and the edge list. Regenerating the network itself from new
  source data would still require rebuilding `platform.html`'s embedded data block; node attributes
  can be refreshed with `tools/merge_node_attributes.py` (see below).

Headline numbers, for reference: 124 organisations, 46 discourse categories
(20 concepts, 7 solutions, 19 themes), 1,044 coded mentions, 4,939 ties at
full density, 3 communities at default resolution (modularity 0.13 — flagged
throughout the site as a weak split, since this network is dense and
dominated by a few heavily-coded organisations).

## Organization attribute filter (added 29 October 2026)

New sidebar section **Filtering organizations** on the Network tab, below the category filter.
It keeps only organizations with the chosen profile, using `data/nodes_profile.xlsx`:

- **Type of organization** — GOV, BUS, SOC, SCI, INT, CONS (plus "Not classified" for organizations
  missing from the file). Select several to combine them; select none to include everyone.
- **City agenda** — the three 0/1 columns (Cidades Resilientes / Inteligentes / Descarbonizadas),
  with an "Any of" / "All of" switch.

How it behaves: ties are rebuilt only among the organizations that pass the filter, then centralities
and communities are recomputed — the same pipeline as the category filter, and the two combine. All
tabs follow (Communities, Organizations, Centrality). The Discourses tab keeps describing the full
dataset; filtered-out organizations appear there in their own "Outside the organization filter" row.
The detail panel and Organization profile show each organization's type and agendas. **Reset** clears it.
Organizations with no recorded attribute are left out whenever a type or agenda is selected, and the
panel says how many.

Data files and tooling:

- `data/node_attributes.csv` — audit table: each network node, the sheet row it was matched to, and how.
- `data/node_attribute_crosswalk.csv` — the hand-made matches where the sheet's acronym differs from the
  network's (e.g. `CAIXA` → `CEF`). Edit this file to correct or add a match.
- `tools/merge_node_attributes.py` — re-run after editing the crosswalk or replacing the sheet:
  `python tools/merge_node_attributes.py data/nodes_profile.xlsx`. It updates `processed_graph.json`
  (nodes gain `t` = type and `a` = [resilient, smart, decarbonized]) **and** the data block inside
  `platform.html`, so the embedded-data rebuild problem noted above is solved for attributes.

Coverage: 109 of 124 nodes matched (72 exact acronym, 28 variants, 8 *probable*, 1 duplicate resolved);
**15 nodes have no row in the sheet** and show as "Not classified": CMMCE-MSP, CONGEPDEC, CSC, GCM-MSP,
MCR2030, MCT, NEXUS, PA, SCLIMA-MSP, SEBRAE-SP, SEC-SANTOS, SECLIMA, SEMAM, SIMACLIM, SUS-SJC.
CBCS has a type but blank agenda flags.

Things to confirm with the project team:

- The 8 *probable* matches (marked in the crosswalk): CC, CET, COMDEC-MSP, NECTA, SDET-MSP, SDH-SP,
  SEC-SJC, SGRI-SP.
- The sheet lists CEBDS twice with different flags; the Conselho Empresarial row was used.
- The sheet has about 90 rows for organizations that are not in the 124-node network; they are ignored.
- The English labels for the type codes and the reading of the three 0/1 columns as "city agendas the
  organization is linked to" are interpretations — check against the source codebook.

## Known placeholders and flagged assumptions

These were left visible rather than invented, so they're easy to find and fix:

- **Scientific basis page:** the second concept box ("How Discourses Shape
  Policy Action") says "Content pending." One hypothesis has a "citation
  pending" marker. The Leifeld (2017) reference is missing its page range,
  and the Weible et al. (2011) reference is missing its DOI.
- **Roadmap for integration page does not exist yet.** Every page's
  navigation lists it with a "Soon" tag. This is the obvious next page to
  build once you have its text.
- Category labels throughout the platform (FDRM/VCE/VP/S/T codes and their
  descriptions) are in Portuguese, as in the source data; the hover
  explanations for each one were written by Claude from the label text, not
  from an official codebook — worth a check against the real definitions if
  one exists.
- "Try it for yourself; discover new potential groups to collab." on the How
  it works page keeps "collab" as given, read as a deliberate casual touch
  rather than a typo.

## Where things are published right now

The live, editable versions (on claude.ai, separate from this static bundle)
were published at these links as of this handoff — ask Claude to pull up any
of them to keep editing interactively instead of rebuilding from the files
here:

- Welcome: https://claude.ai/artifact/GY13ytxrf7aACF5rAE8QDy
- Short introduction: https://claude.ai/artifact/UwXXfsXk6M4NTF3h7aQPAd
- How it works: https://claude.ai/artifact/GCnvYWBgrvWzHztnjz7MZJ
- Scientific basis: https://claude.ai/artifact/Vd2i6vgAHJuZHMxnA5SBc7
- Platform: https://claude.ai/artifact/X2Zi1iNFzH6XL2PtmidHGe

**The claude.ai links above have not been updated with the attribute filter** — only this bundle has it.
The files in this bundle are static snapshots of those pages with the links
between them rewritten to point at each other by filename, so they work as a
standalone site (e.g. on GitHub Pages) independent of claude.ai.

## Picking this back up

If you start a new conversation: upload this bundle (or just mention the
links above) and describe what you want next — for example, building the
Roadmap for integration page, filling in the pending citations and content,
or adjusting anything on the platform. There's no need to re-explain the
project background; this file and the files themselves carry that context.
