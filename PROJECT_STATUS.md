# Governing Resilient Cities — project status

Last updated: 29 October 2026 (Network tab split into two panels; city-base filter added). This file is a handoff summary: what exists,
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

## Network tab layout (changed 3 November 2026)

The Network tab now has three columns: a **left panel** with all the filtering options, the graph in the
middle, and a **right panel** with the results.

- Left, **Filtering options** (with an "i" explaining that every selection builds a different network):
  **1) Filtering the network** (the category presets and *Choose categories*, unchanged) and
  **2) Filtering organizations** (type, city base, city agenda, themes discussed).
- Right: the search bar, the **selected organization** (this panel used to float over the graph; it now
  opens at the top of the right panel, and on phones it is still a bottom sheet), the **community
  results** (colour mode, community list, *Detail* slider) and the **view options** (tie strength, node size,
  labels, layout).
- The **Themes** preset button was removed from the network filter on every tab; thematic filtering is now
  only done through *Themes discussed* under Filtering organizations. **Open question:** the individual
  theme categories are still listed under *Choose categories*, and "All" still builds ties from all 46
  discourse categories, so the baseline (4,939 ties, 3 communities) is unchanged. Removing the theme
  categories from the ties altogether would change those baseline results, so it was not done.

## Community profiles: "vs community" mode (4 November 2026)

The Category profile card has a third view, **vs community**, next to *Share* and *vs network*. It looks like
*vs network* (bars to the right = above the reference, to the left = below, values in percentage points) but the
reference comes only from the community's own data, with no network data involved: each category is compared with the
community's **average category**, defined as an even spread of the section over the categories the community actually
mentions. If a community mentions 10 concepts, the average is 10% each, so a concept at 25% reads +15 pp. It shows
what stands out inside the community. Definition details:

- The average is worked out per section (concepts, solutions, themes), over the categories the community mentions
  in the categories currently selected in the network filter.
- Categories the community never mentions are shown as light-gray 0% and are not compared (the same rule as vs network).
- A group row (VP.2, VP.3) is compared with the sum of its mentioned parts' averages, so it equals the sum of its
  parts' differences when expanded.
- Row tooltips state the average and how it was obtained; the legend reads "Above / Below community average".
- The scale is shared across communities, like vs network. Code: `selfRefVec()` and `domainFor(…, "self")`.
- The *Most / Least emphasised vs network* lists on the left of the card are unchanged (they are always vs network).
- Verified against an independent calculation from the dataset for every community and row (261 rows, three filter
  states); Share and vs network render exactly as before.
- Also fixed: the Share tooltip still referred to the Weighting option removed earlier.

## Community profiles: types of organization (4 November 2026)

The community card (left side of the Communities tab) has a **Types of organization** block, just under the
member counts, drawn as a single **100% stacked bar**: one segment per type (government, business, civil society,
science & academia, international, councils & consortia, and "Not classified" for organizations missing from the
attribute file), in a fixed order. Colour: each type is a **shade of the community's own colour** (one hue per
community, lightness stepping from dark to light in the legend order, so the same type has the same position in the
ramp for every community); the text inside a segment switches between white and dark depending on the shade, and the
ramp starts a little lighter in dark mode. A thin bar below shows the same mix for all organizations in the current
view (the same reference group as the rest of the card) in **neutral gray with the same lightness steps**. Segments
wide enough (14%+) print their percentage; a legend lists every type with its count and percentage (types the
community lacks are greyed). Hovering a segment or a legend item shows the type's share in the community and in the
network, the difference, and the community's members of that type (top 12 by weighted degree). A line under the block
names the types that are over- or under-represented by 5 percentage points or more, or says the mix is close to the
network's. It follows the network and organization filters like the rest of the card. Verified against the dataset for
every community under several filters. Code: `shadeFor()` in `renderComm()`. The theme button now also re-renders the
visible tab, so colours written into the Communities, Organizations and Centrality tabs follow the theme at once.

## Consistency and UX pass (3 November 2026)

A round of small fixes after an inspection of the platform:

1. **Wording:** the Centrality tab is now titled *Organization centrality* (was "Actor centrality") and the
   eigenvector measure reads "Ties to well-connected organizations". The entity is called an "organization"
   everywhere now; "actor(s)" survives only inside the coded category definitions, where it is the source term.
2. **Empty organization list:** the Organizations list now shows "No organization matches …" instead of a blank
   card when a search or community filter hides every row.
3. **Communities subtitle:** when the filter matches no organizations, the Community profiles subtitle says so
   plainly instead of "These 0 communities have a very weak structure"; a single community now reads "This single
   community has…".
4. **Reset:** the top-bar Reset now clears the Organizations search box too (it already cleared the Network one).
5. **"Average connections":** the community metric tile no longer abbreviates it to "Avg.".
6. **Mobile selected-organization sheet:** on phones the detail panel is now a partial bottom sheet (~42vh) with a
   grab handle; the graph and the Fit / Clear buttons stay visible above it instead of being covered.
9. **Tabs** carry `aria-current="page"` on the active tab for screen readers.
10. **Info icons:** the two that lacked an `aria-label` (Detail/resolution, community structure) now have one, so
    all ten are labelled.
11. **"Recalculating…" cue:** a small spinner appears under *Community results* while a filter or the Detail slider
    rebuilds the network, so a change is visibly taking effect. It respects reduced-motion.

Not done in this pass (from the same inspection, left for later): keyboard operation of the graph canvas,
a "share this view" link that encodes the active filters in the URL, a first-paint loading cue, and touch-specific
"how to use" text.

## Compare two organizations (3 November 2026)

The Organizations tab has a **View** switch: *Single profile* (as before) or *Compare two organizations*. The network
filter and the Concepts / Solutions / Themes switch apply to both. A **Compare with…** button on a profile opens the
comparison with that organization as A; *Open profile* inside the comparison, or opening an organization from another
tab, returns to the single profile.

In compare mode: two selectors (A and B, with a swap button and one-click suggestions of the six most similar
organizations to A), then
- **Summary:** profile similarity (cosine over the categories shown, the same measure as "Most similar profiles"),
  similarity per section, categories in common (of the categories mentioned by either), direct tie strength and
  common neighbours in the current network.
- **Profile attributes:** type, city agenda, city base, community, connections, weighted degree and mentions side by
  side, with an "in common" column (shared agendas and bases, same type / same community).
- **Similarities and differences:** shared emphasis (both mention, ranked by the smaller share), different emphasis
  (largest gap in percentage points), and the categories only A or only B mentions.
- **Profiles side by side:** a mirrored bar chart, A on the left and B on the right, on one shared axis per section
  and with the same expandable groups as the other profile charts. Rows are tagged "A only" / "B only". *Sort by*
  (combined emphasis, largest difference, A, B, category order) and *Show* (everything mentioned, shared, mentioned
  by only one) control it. Categories neither mentions are never listed.
- A and B use fixed colours (rose and teal) that are different from the community colours. Phone layout stacks the
  columns.
- Code: section "compare two organizations" in `platform.html` (`renderCompare()`); verified against an independent
  calculation (similarity, overlaps, tie, common neighbours and every category value and tag).
- Also fixed: the "Show" switch on the profile tabs was wider than a phone screen. Known and left alone: the top tab
  strip is wider than a 390 px phone on every tab.

## Export of the filtered graph (3 November 2026)

New **Export filtered graph** section in the Network tab's right panel, with **GraphML** and **CSV (.zip)**
buttons. Files are generated in the browser (no server). The export is the graph as filtered: the organizations
that pass the network and organization filters (only those with ties when *Hide organizations without ties* is on)
and all the ties between them. The checkbox *Only ties currently shown* restricts the ties to those at or above
the minimum tie strength slider; by default all filtered ties are exported, because communities and centralities
are calculated on all of them.

- **GraphML**: one file (undirected); the filters used are stored in the graph's `description`.
- **CSV**: a zip with `nodes.csv`, `edges.csv` and a `README.txt` (filters used and a description of every column).
  Files are UTF-8 with a byte-order mark so Excel shows accents. `nodes.csv` has `id` and `edges.csv` has
  `source`, `target`, `type`, `weight`, the columns Gephi's spreadsheet import expects.
- **Node attributes**: label, full name, type, the three agendas, the six city-base flags, community in the
  view and in the full network, connections, weighted degree, betweenness, eigenvector, mentions (selected
  categories), layout position (`x`, `y`; `y` flipped to match Gephi) and the mention count of each of the 46
  categories. Blank = not recorded.
- **Edge attributes**: `weight`, `shared_categories`, `same_community`.
- The column definitions live in `NODE_COLS` / `EDGE_COLS` in `platform.html` (section "export the filtered
  graph"); both formats are built from them, so adding a column there adds it to both.
- Tested by downloading the files in a browser and checking them against an independent calculation from the
  source data (nodes, ties, weights, attributes) with NetworkX and pandas. Not tested in Gephi or Cytoscape
  themselves. Downloads work in the deployed page; some embedded previews block file downloads.

## Community profiles: "vs network" and categories not mentioned (3 November 2026)

In the Category profile's **vs network** view, a category the community never mentions is no longer compared
with the network. It is shown like in the Share view: light gray, **0%**, no bar, listed after the categories
that are compared. Its tooltip says no difference is calculated. The bar scale is now set by the largest
difference among the categories that are compared, and the "Most / Least emphasised vs network" lists
only consider categories the community mentions (before, a category at 0% could appear as the "least
emphasised"). The Share view is unchanged.

## Community profiles: weighting option removed (3 November 2026)

The *Weighting* dropdown on the Community profile's Category profile card was removed, because the
network data is already normalized. The bars always use the pooled calculation that was the default
before: the share of all mentions of a type, made by the community's members, that fall in each category.
The rendered charts are identical to the previous default (checked for every community, mode, section and
filter state). The alternative "equal weight per organization" average, and the code behind it, were
deleted. If you meant the equal-weight average to be the one kept, it is a small change to switch.

## Label placement (changed 3 November 2026)

Labels on the Network graph never overlap, in any layout, zoom level or label mode. Each frame the
labels are placed in screen space, in priority order: the hovered or selected organization (always drawn),
then its neighbours or the search matches, then everyone else by node size. Each label tries eight
positions around its dot (below, above, right, left and the four diagonals), preferring one that does not
cover another dot, and is nudged to stay inside the visible map; a label that fits nowhere is skipped.

- **Auto** now labels as many organizations as fit, largest first, with extra spacing (it used to label only
  large dots, which left some layouts with almost no labels).
- **All** packs labels tightly; when some are skipped the right panel says how many ("N labels hidden to
  avoid overlaps — zoom in or filter to show more"). **None** is unchanged.
- The code is in `render()` in `platform.html` (look for "labels: placed in screen space").

## Organization attribute filter (added 29 October 2026)

Section **Filtering organizations** on the Network tab (left panel), below the network filter.
It keeps only organizations with the chosen profile, using `data/nodes_profile.xlsx`:

- **Type of organization** — GOV, BUS, SOC, SCI, INT, CONS (plus "Not classified" for organizations
  missing from the file). Select several to combine them; select none to include everyone.
- **City base** (added 3 November 2026) — six chips from `data/nodes_city_base.xlsx`: São Paulo,
  São José dos Campos, Santos, State of São Paulo ("Estado de SP"), Federal ("Federação") and
  International, with an "Any of" / "All of" switch. An organization can have several. Blank cells count as
  0; 108 of 124 nodes have a recorded city base (CBCS is blank in every column, and the 15 unmatched nodes
  have no row). The English labels, and reading "Federação" as the federal level, are interpretations.
- **City agenda** — the three 0/1 columns (Cidades Resilientes / Inteligentes / Descarbonizadas),
  with an "Any of" / "All of" switch.
- **Themes discussed** (thematic filter) — a collapsible checklist of the 19 themes (T.1–T.20; there is
  no T.11 in the coding), each with the number of organizations that mention it, and its own
  "Any of" / "All of" switch. An organization "discusses" a theme when it has at least one coded
  mention of it. 18 organizations mention no theme, so any theme selection leaves them out.

How it behaves: ties are rebuilt only among the organizations that pass the filter, then centralities
and communities are recomputed — the same pipeline as the category filter, and the two combine. All
tabs follow (Communities, Organizations, Centrality). The Discourses tab keeps describing the full
dataset; filtered-out organizations appear there in their own "Outside the organization filter" row.
The detail panel and Organization profile show each organization's type, agendas and the themes it mentions. **Reset** clears it.
Organizations with no recorded attribute are left out whenever a type or agenda is selected, and the
panel says how many.

Data files and tooling:

- `data/node_attributes.csv` — the node table: each network node, the sheet row it was matched to (and how),
  type, the three agenda flags, the six city-base flags (`base_*`), `themes_discussed` (number of themes mentioned) and **one column per
  theme** (`T.1 Criminalidade` … `T.20 Transparência`) holding that organization's number of coded
  mentions of the theme (0 = does not discuss it). Theme columns come from the network data itself
  (checked against `network_twomode_combined_1.csv`), not from the attribute sheet.
- **Full organization names:** each node also carries `fn`, taken from the sheet's *Nome* column, and the
  platform shows it next to the acronym in the Organizations tab (list and profile header) and in the
  Network detail panel; both searches also match it. 106 of 124 nodes have one. The 15 nodes that are not
  in the sheet show only the acronym (so do ECOBAIRRO, INSPER and MACKENZIE, whose sheet name is just the
  acronym again). Names are shown exactly as typed in the sheet (a few have typos, e.g. "aquaviacrios", and
  some carry notes in brackets), and the 8 *probable* matches borrow their name from the matched row.
- `data/node_attribute_crosswalk.csv` — the hand-made matches where the sheet's acronym differs from the
  network's (e.g. `CAIXA` → `CEF`). Edit this file to correct or add a match.
- `tools/merge_node_attributes.py` — re-run after editing the crosswalk or replacing the sheet:
  `python tools/merge_node_attributes.py data/nodes_profile.xlsx data/nodes_city_base.xlsx`. It updates `processed_graph.json`
  (nodes gain `t` = type, `a` = [resilient, smart, decarbonized] and `b` = city base) **and** the data block inside
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
