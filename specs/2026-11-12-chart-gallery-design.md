# Interactive Chart Gallery for AN Presentation — Design

## Intent and why

Casey is presenting the analysis in `Presentation 4 - Metro Analytics
Notebook.ipynb` (UK-graduate-to-US-analytics-job-market study) to his AN
class. He wants a clean way to display all of the notebook's charts
*while presenting* — not a general portfolio for recruiters. The site
needs to look good projected on a classroom screen and be easy to drive
live: click through charts in order, but also be able to jump to any
chart if a question comes up.

## Goals

- Every interactive Plotly chart currently in the notebook is viewable
  in the site, with full interactivity preserved (hover tooltips, zoom,
  pan, legend toggling).
- A gallery landing page shows all charts as a grid, grouped by the
  notebook's own section structure, so it reads as an actual gallery.
- Clicking any chart opens a full-screen "presenter" view with
  Next/Previous controls (click + arrow keys) that steps through the
  remaining charts in notebook order, each with a one-line caption.
  A control returns to the gallery grid at any point.
- The site is resilient to flaky classroom wifi: once the page has
  loaded, moving between charts does not depend on a CDN.
- The repo is clean and presentable on GitHub, and the site is viewable
  both via GitHub Pages and by opening the files locally (wifi-outage
  fallback).

## Non-goals

- Not building a recruiter-facing portfolio (reusable later, but not
  the design target now).
- Not re-deriving or second-guessing the notebook's analysis. The
  charts shown must be exactly what the notebook currently produces.
- No backend/server/Dash app — purely static files.

## Anti-goals

- A chart that's supposed to be interactive rendering as a flat image.
- Any exported chart showing different numbers/clusters than what the
  notebook actually computes (would undermine the presentation).
- The site breaking or going blank without internet access.

## Constraints

- Must preserve full Plotly interactivity in every exported chart.
- Must reflect the same computations/data already in
  `Presentation 4 Jobs data.csv` — no reimplementation of the analysis.
- This folder is not a git repo yet.
- The notebook already auto-detects it isn't running in Colab (cell 2:
  `IN_COLAB = 'google.colab' in sys.modules`) and falls back to loading
  `Presentation 4 Jobs data.csv` from the working directory, so it can
  run locally without modification to produce the same results.

## Approaches considered

- **A — single scrolling page**, sections in notebook order with
  context text and charts embedded inline. Good narrative flow, but
  jumping to answer an out-of-order question means scrolling.
- **B — gallery grid + individual full-screen chart pages**, no
  slideshow flow. Matches "gallery" literally, but driving the full
  chart sequence live means clicking back to the grid between every
  chart.
- **C — gallery grid + full-screen presenter/slide mode** (chosen).
  Same grid as B for the overview and for jumping to any chart, but
  clicking a chart drops into a Next/Previous flow through the rest of
  the charts. Best fit for "browsable gallery that's also smooth to
  drive live." Picked by Casey in conversation.

## How it's built (my calls)

1. **Chart extraction.** A build script
   (`scripts/export_charts.py`) works off a copy of the notebook — the
   original `.ipynb` is never modified. It runs the notebook's own code
   locally (same CSV, same computations) and, right after each chart's
   existing `.show()` call, additionally:
   - calls `fig.write_html(path, include_plotlyjs='<relative path to
     a shared vendor file>', full_html=True)` to export a standalone,
     fully interactive chart file, and
   - calls `fig.write_image(thumb_path, width=..., height=...)` (via
     `kaleido`) to produce a static PNG thumbnail for the gallery grid.
2. **Non-Plotly outputs.**
   - Both matplotlib word clouds — the before/after-cleaning comparison
     (section 5) and the entry-accessible-postings one (also section 5)
     — are saved as plain PNGs and shown as static images in the
     gallery/slide flow, clearly labeled non-interactive.
   - The pyLDAvis topic panel already saves itself to
     `pyldavis_topics.html` — copied into the site as-is and slotted
     into the gallery/slide flow like any other chart, with a text
     thumbnail (auto-thumbnailing doesn't apply to it).
3. **Self-hosted Plotly.js.** One shared `docs/vendor/plotly.min.js`
   that every chart's HTML references, instead of each chart embedding
   or CDN-loading its own copy. Keeps chart files small and means chart
   navigation doesn't depend on internet access once the page is open.
4. **Site: plain HTML/CSS/JS, no framework, no build step.**
   - `docs/index.html` — gallery grid grouped by the notebook's section
     headings; each tile is a thumbnail + chart title.
   - A presenter/slide view (same site, different state) — loads the
     chart's HTML in an iframe full-screen, with Prev/Next, arrow-key
     support, a short caption, a progress readout ("12 / 27"), and a
     "back to gallery" control.
   - `docs/charts.json` — manifest generated by the build script: one
     entry per chart with id, section, title, short caption, file
     path, thumbnail path, and an `interactive: true/false` flag.
5. **Hosting.** The repo is private (Casey's call — the notebook, the
   scraped job-postings CSV, and grading-sensitive content shouldn't be
   public). Free GitHub Pages needs a public repo, so there's no public
   URL; the site is driven by opening `docs/index.html` directly from a
   local clone on presentation day. Nothing in the design changes to
   support this — it's the same self-hosted-Plotly.js, no-CDN-dependency
   site either way, just viewed from disk instead of a Pages URL. If a
   shareable link is ever wanted later, the repo can be made public (or
   mirrored into a second, pages-only public repo) with no rework.
6. **Repo layout.** Notebook + CSV stay in the repo (e.g. at root or a
   `notebook/` folder) for reference/grading; `docs/` holds the
   generated site (and only the generated site — planning docs like
   this one live in a top-level `specs/` folder, outside `docs/`, so
   GitHub Pages never publishes them); `scripts/export_charts.py` is
   the re-runnable, non-destructive build script, so the site can be
   regenerated if the notebook changes before presentation day.
7. **Gallery grouping.** Tiles group by the notebook's 15 top-level
   `##` sections. Where a section's charts span multiple `###`
   subsections with real topic differences (only section 11,
   Geospatial Analytics, qualifies — its charts live under 11c/11d),
   the subsection label shows as a small sub-header within that
   section's group rather than splitting into separate top-level
   groups.

## What's left to the builder

- Exact wording of each chart's one-line caption (pulled from the
  nearest markdown takeaway in the notebook, trimmed to fit).
- Visual styling details (colors/fonts/spacing) within a "clean,
  presentable" direction consistent with the notebook's own chart
  styling (`presentation_layout` in cell 2).
- Exact thumbnail sizing and gallery grid breakpoints.
- README content for the repo.
