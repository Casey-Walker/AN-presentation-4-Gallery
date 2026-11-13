# Metro Analytics Chart Gallery

An interactive chart gallery for presenting *"Where Should a UK Graduate
Start a U.S. Analytics Career?"* — the analysis in
[`Presentation 4 - Metro Analytics Notebook.ipynb`](Presentation%204%20-%20Metro%20Analytics%20Notebook.ipynb) —
to the AN class.

Every Plotly chart in the notebook (and the pyLDAvis topic-model panel) is
exported to a standalone, fully interactive HTML file. `docs/` is a static
site with a gallery grid of all of them, grouped by the notebook's own
sections, plus a full-screen presenter view with Next/Previous and
arrow-key navigation for walking through them live.

## Presenting

No server, no internet connection needed once you have the files:

1. Clone (or download) this repo.
2. Open `docs/index.html` in a browser.
3. Click any chart to enter presenter mode. Use the on-screen
   Previous/Next buttons, the left/right arrow keys, or `Escape`/"Back to
   gallery" to return to the grid and jump to a different chart.

## Regenerating the gallery

If the notebook changes before presentation day, regenerate every chart,
thumbnail, and the gallery's manifest with:

```bash
pip install -r requirements.txt
python scripts/export_charts.py
```

This runs an unmodified copy of the notebook (the original `.ipynb` file
is never changed) against `Presentation 4 Jobs data.csv`, and rewrites
everything under `docs/charts/`, `docs/images/`, `docs/thumbs/`, and
`docs/charts.js`. If anything goes wrong partway through (a cell errors,
or a chart ends up without a matching caption), the previous working
gallery is restored automatically and nothing is left half-broken.

**Regenerating needs internet access** (to install packages, download
NLTK's stopword list, and fetch the map outlines and pyLDAvis's JS
library so they can be vendored locally) — but once it's done, *presenting*
from `docs/` needs none. `kaleido` (used for chart thumbnails) also needs
a local Chrome/Chromium; if one isn't already on your machine, `pip
install kaleido` pulls one down for it automatically on first use.

## Repo layout

- `Presentation 4 - Metro Analytics Notebook.ipynb`, `Presentation 4 Jobs data.csv` — the source analysis and data.
- `scripts/` — the build pipeline that exports charts from the notebook.
- `docs/` — the generated gallery site (this is what you open to present).
- `specs/` — the design doc and implementation plan this project was built from.
