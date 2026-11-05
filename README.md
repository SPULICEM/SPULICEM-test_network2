# Governing Resilient Cities — static site bundle

Five self-contained HTML files, ready to publish on GitHub Pages. No build step,
no dependencies to install — everything (including the fonts, all logos and the entire
platform app) is embedded inline, so the site also works if you just double-click a file and open it
locally.

## Files

| File                      | Page               |
|---------------------------|--------------------|
| `index.html`              | Welcome            |
| `intro.html`              | Short introduction |
| `how.html`                | How it works       |
| `scientific-basis.html`   | Scientific basis   |
| `platform.html`           | The network explorer platform |

`index.html` is the homepage, so GitHub Pages will show it automatically at
your site's root URL. Every page links to the others by filename, so as long
as all five files stay in the same folder, navigation works without any
further changes.

## Publish on GitHub Pages

1. Create a new repository on GitHub (public, so Pages can serve it on a free
   plan — e.g. `governing-resilient-cities`).
2. Add the five HTML files and the `.nojekyll` file (an empty file that tells GitHub Pages to serve the files as they are) to the repository root (drag-and-drop them in the
   GitHub web UI under "Add file → Upload files", or `git add` / `git commit`
   / `git push` if you're working from the command line).
3. Optionally add the `data/` and `tools/` folders too; the site does not need them to run.
4. In the repository, go to **Settings → Pages**.
5. Under "Build and deployment", set **Source** to "Deploy from a branch",
   pick the branch you pushed to (usually `main`), and set the folder to `/`
   (root).
6. Save. GitHub will give you a URL shortly, typically
   `https://<your-username>.github.io/<repository-name>/`.

The "Roadmap for integration" page isn't built yet, so its nav entries are
still marked "Soon" throughout the site — add `roadmap.html` later and point
those entries at it the same way the other pages link to each other.

## Data and tooling

`data/` holds the source CSVs, the processed graph and the organization attribute files
(`nodes_profile.xlsx`, `nodes_city_base.xlsx`, `node_attributes.csv`, `node_attribute_crosswalk.csv`).
`tools/merge_node_attributes.py` merges the attribute sheet into `processed_graph.json` and the
data embedded in `platform.html` (needs Python with `pandas` and `openpyxl`). It is not needed to
publish the site.

## Checked before delivery

All five pages were opened from a local web server: every link between them resolves, there are no JavaScript
errors, and no page requests anything from outside the folder. Links between pages use plain file names, so the
folder works the same on GitHub Pages (`https://<user>.github.io/<repo>/`) or opened locally.
