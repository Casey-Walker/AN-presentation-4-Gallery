# Interactive Chart Gallery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn every chart in `Presentation 4 - Metro Analytics Notebook.ipynb` into a standalone, fully-interactive file, and build a static gallery+presenter site around them that Casey can drive live in class, opened straight from a local (private) git repo.

**Architecture:** A Python build pipeline executes an unmodified copy of the notebook with small injected hooks that export each Plotly figure to self-contained HTML (plus a PNG thumbnail) and each matplotlib figure to a plain PNG, recording everything to a manifest. A hand-authored metadata table supplies section/caption text. A plain HTML/CSS/JS site (no framework, no fetch of local files) reads that manifest as an inline `<script>` and renders a gallery grid plus a full-screen Next/Previous presenter view.

**Tech Stack:** Python (nbformat, nbclient, plotly, kaleido, pytest), vanilla HTML/CSS/JS, git.

**Spec:** [specs/2026-11-12-chart-gallery-design.md](2026-11-12-chart-gallery-design.md)

> **Note on plan location:** the design doc already moved planning artifacts out of `docs/` (to avoid colliding with the gallery site that will be served/opened from there), so this plan is saved alongside it in `specs/`, overriding the skill's usual `docs/superpowers/plans/` default.

## Global Constraints

- The original `.ipynb` is never modified by the build pipeline — it always runs against a working copy.
- Every exported chart must keep full Plotly interactivity (hover, zoom, pan, legend toggle).
- Exported charts must reflect the notebook's actual current computations against `Presentation 4 Jobs data.csv` — no reimplementation of the analysis.
- The repo is private; there is no public GitHub Pages URL. The site must work by opening `docs/index.html` directly from disk, with no local server and no internet access required after the repo is cloned.
- Every chart's HTML references one shared `docs/vendor/plotly.min.js` rather than embedding or CDN-loading its own copy of Plotly.
- Planning docs live in `specs/`, never inside `docs/`.
- The gallery groups tiles by the notebook's 15 top-level `##` sections; only section 11 (Geospatial Analytics) shows subsection sub-labels, for its 11c/11d charts.
- No build step, bundler, or JS framework for the site.

## Review Focus

- A chart whose `.show()` call is a standalone statement after an earlier, separate `style(fig, ...)` statement (this exact pattern occurs in cell 50's dashboard) — the transformer must still find and export it, not just the chained `style(fig, ...).show()` form. (Task 2)
- A single notebook cell that reassigns the same `fig` variable and calls `.show()` several times in sequence (this happens in cells 13, 15, and 39–45) — each occurrence must get its own unique chart id and export file, in call order, not overwrite the previous one. (Task 2)
- A caption sourced from a markdown cell that contains markdown syntax (`**bold**`, backticks, links) — it must render as plain text in the gallery, not leak literal asterisks/backticks. (Task 5)
- The site opened via `file://` directly in Chrome — manifest loading must not depend on `fetch()` of a separate JSON file (Chrome blocks that under `file://`), so the gallery must not render empty with no visible error. (Task 7)
- A single chart's thumbnail export failing (e.g. a kaleido error on a mapbox/choropleth figure) — the pipeline must log it and continue, leaving that one tile without a thumbnail, rather than aborting the whole run. (Task 3)

---

## File Structure

```
scripts/
  chart_transform.py     # pure: rewrites `.show()` calls in cell source
  chart_export.py        # export_chart(), export_image(), ManifestWriter
  chart_meta.py           # hand-authored CHART_META + validate() + strip_markdown()
  notebook_exec.py        # build_working_copy(), execute_notebook()
  export_charts.py        # CLI orchestrator (main())
tests/
  test_chart_transform.py
  test_chart_export.py
  test_chart_meta.py
  test_notebook_exec.py
docs/
  index.html
  styles.css
  app.js
  charts.js                # generated: window.CHARTS = [...]
  vendor/plotly.min.js     # generated via plotly.offline.get_plotlyjs()
  charts/<id>.html          # generated, one per interactive chart
  images/<id>.png           # generated, one per static (matplotlib) chart
  thumbs/<id>.png           # generated thumbnail per chart
requirements.txt
.gitignore
README.md
```

---

### Task 1: Project scaffolding

**Files:**
- Create: `requirements.txt`, `.gitignore`
- Create (empty dirs via `.gitkeep` or first real file): `scripts/`, `tests/`, `docs/`

**Interfaces:**
- Produces: a git repo at the project root with an initial commit; `kaleido` and `pytest` importable.

- [ ] **Step 1: Initialize git**

Run: `git init` in the project root.
Expected: `Initialized empty Git repository`.

- [ ] **Step 2: Write `.gitignore`**

Include at least: `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`, `docs/_manifest_raw.jsonl` (the build pipeline's internal scratch file, defined in Task 4).

- [ ] **Step 3: Write `requirements.txt`**

Pin: `nbformat`, `nbclient`, `plotly`, `kaleido`, `pytest` (versions matching what's already installed: nbformat 5.11.1, nbclient 0.11.0, plotly 7.1.0; kaleido and pytest latest).

- [ ] **Step 4: Install missing packages**

Run: `pip install kaleido pytest`
Expected: both import successfully (`python -c "import kaleido, pytest"`).

- [ ] **Step 5: Create `scripts/`, `tests/`, `docs/` directories**

- [ ] **Step 6: Commit**

```bash
git add requirements.txt .gitignore
git commit -m "chore: scaffold chart gallery project"
```

---

### Task 2: Chart-cell transformer

**Files:**
- Create: `scripts/chart_transform.py`
- Test: `tests/test_chart_transform.py`

**Interfaces:**
- Produces: `transform_cell_source(source: str, cell_index: int) -> tuple[str, int]` — handles **Plotly charts only** (the notebook's matplotlib word clouds and the self-saving pyLDAvis cell are handled separately in Task 4, since they don't use this `.show()` pattern at all). Returns `(new_source, n_charts_found)`. Every top-level `.show()` call on a Plotly figure expression (`fig.show()`, or `style(fig, ...).show()` chained, or a standalone `fig.show()` following an earlier separate `style(fig, ...)` statement) is rewritten to call `_export(<the same expression, minus .show()>, "<cell_index>_<occurrence>")`, where `occurrence` starts at 0 per cell and increments once per match, in source order. All other source is left byte-for-byte unchanged.

- [ ] **Step 1: Write the failing tests**

```python
def test_single_chained_show():
    src = (
        "fig = px.bar(missing[missing['% Missing'] > 0], x='% Missing', y='Column')\n"
        "style(fig, height=450, yaxis={'categoryorder': 'total ascending'}, "
        "coloraxis_showscale=False).show()\n"
    )
    new_src, n = transform_cell_source(src, cell_index=3)
    assert n == 1
    assert '_export(style(fig, height=450, yaxis={\'categoryorder\': \'total ascending\'}, coloraxis_showscale=False), "3_0")' in new_src
    assert ".show()" not in new_src

def test_multiple_show_same_cell_get_unique_ids():
    src = (
        "fig = px.bar(skill_share.sort_values('Share (%)'), x='Share (%)', y='Skill')\n"
        "style(fig, height=520, coloraxis_showscale=False).show()\n"
        "\n"
        "fig = px.histogram(df.dropna(subset=['years_required']), x='years_required', nbins=15)\n"
        "style(fig, bargap=0.08).show()\n"
    )
    new_src, n = transform_cell_source(src, cell_index=13)
    assert n == 2
    assert '"13_0"' in new_src
    assert '"13_1"' in new_src

def test_standalone_show_after_separate_style_call():
    src = (
        "style(fig, height=600, title_text='Executive Summary Dashboard')\n"
        "fig.show()\n"
    )
    new_src, n = transform_cell_source(src, cell_index=50)
    assert n == 1
    assert '_export(fig, "50_0")' in new_src
    assert ".show()" not in new_src

def test_no_show_call_is_unchanged():
    src = "df['cluster'] = kmeans.labels_\n"
    new_src, n = transform_cell_source(src, cell_index=24)
    assert n == 0
    assert new_src == src
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_chart_transform.py -v`
Expected: FAIL with `transform_cell_source` undefined.

- [ ] **Step 3: Implement `transform_cell_source` in `scripts/chart_transform.py`**

One line on the approach: a single regex alternation matching either `style\(fig[^\n]*?\)\.show\(\)` or a bare `fig\.show\(\)` on its own line, replacing each match (in order) with `_export(<matched expression without the trailing .show()>, "<cell_index>_<occurrence>")`, and resetting `occurrence` to 0 at the start of each call.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_chart_transform.py -v`
Expected: PASS (all 4 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/chart_transform.py tests/test_chart_transform.py
git commit -m "feat: add chart-cell .show() transformer"
```

---

### Task 3: Export helpers

**Files:**
- Create: `scripts/chart_export.py`
- Test: `tests/test_chart_export.py`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces:
  - `write_vendor_plotly_js(path: str) -> None` — writes the installed Plotly's JS bundle to `path` via `plotly.offline.get_plotlyjs()`.
  - `class ManifestWriter(path: str)` with `.append(entry: dict) -> None`, which appends one JSON line to `path` immediately (the executed notebook runs in a separate kernel process, so entries must be persisted to disk as they happen, not accumulated in memory).
  - `export_chart(fig, chart_id: str, out_dir: str, thumb_dir: str, vendor_rel_path: str) -> dict` — writes `out_dir/<chart_id>.html` via `fig.write_html(path, include_plotlyjs=vendor_rel_path, full_html=True)`, then tries `fig.write_image(thumb_dir/<chart_id>.png, width=400, height=260)`; on any exception from `write_image`, logs a warning and leaves the thumbnail unwritten. Returns `{"id": chart_id, "title": <fig.layout.title.text or "">, "file": "charts/<chart_id>.html", "thumbnail": "thumbs/<chart_id>.png" or None, "interactive": True}`.
  - `export_image(mpl_fig, chart_id: str, img_dir: str, thumb_dir: str, title: str) -> dict` — saves `mpl_fig` to `img_dir/<chart_id>.png` and copies the same file to `thumb_dir/<chart_id>.png`. Returns `{"id": chart_id, "title": title, "file": "images/<chart_id>.png", "thumbnail": "thumbs/<chart_id>.png", "interactive": False}`.

- [ ] **Step 1: Write the failing tests**

```python
def test_export_chart_writes_html_and_thumbnail(tmp_path):
    fig = px.bar(x=[1, 2], y=[3, 4], title="Test Chart")
    entry = export_chart(fig, "99_0", str(tmp_path / "charts"), str(tmp_path / "thumbs"), "../vendor/plotly.min.js")
    assert (tmp_path / "charts" / "99_0.html").exists()
    assert (tmp_path / "thumbs" / "99_0.png").exists()
    assert entry == {"id": "99_0", "title": "Test Chart", "file": "charts/99_0.html",
                      "thumbnail": "thumbs/99_0.png", "interactive": True}

def test_export_chart_survives_thumbnail_failure(tmp_path, monkeypatch):
    fig = px.bar(x=[1, 2], y=[3, 4], title="Test Chart")
    monkeypatch.setattr(type(fig), "write_image", lambda self, *a, **kw: (_ for _ in ()).throw(RuntimeError("kaleido boom")))
    entry = export_chart(fig, "99_1", str(tmp_path / "charts"), str(tmp_path / "thumbs"), "../vendor/plotly.min.js")
    assert (tmp_path / "charts" / "99_1.html").exists()
    assert entry["thumbnail"] is None

def test_manifest_writer_appends_jsonl(tmp_path):
    path = tmp_path / "manifest.jsonl"
    mw = ManifestWriter(str(path))
    mw.append({"id": "1"})
    mw.append({"id": "2"})
    lines = path.read_text().strip().splitlines()
    assert [json.loads(l)["id"] for l in lines] == ["1", "2"]

def test_write_vendor_plotly_js(tmp_path):
    path = tmp_path / "plotly.min.js"
    write_vendor_plotly_js(str(path))
    assert path.stat().st_size > 1_000_000  # real plotly.js bundle is multi-MB
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_chart_export.py -v`
Expected: FAIL with the functions/class undefined.

- [ ] **Step 3: Implement `scripts/chart_export.py`**

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_chart_export.py -v`
Expected: PASS (all 4 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/chart_export.py tests/test_chart_export.py
git commit -m "feat: add chart/thumbnail export helpers and manifest writer"
```

---

### Task 4: Notebook execution harness

**Files:**
- Create: `scripts/notebook_exec.py`
- Test: `tests/test_notebook_exec.py`

**Interfaces:**
- Consumes: `transform_cell_source` (Task 2).
- Produces:
  - `MATPLOTLIB_CHART_CELLS: dict[int, str]` — a fixed, explicit mapping of the notebook's two matplotlib word-cloud cell indices to a short slug, e.g. `{16: "wordcloud_before_after", 17: "wordcloud_entry_accessible"}` (confirm the exact indices against the current notebook before hardcoding — they were correct as of this plan's writing but a re-check costs one `nbformat.read` + print). For each cell index in this dict, its sole `plt.show()` statement (there is exactly one per cell) is rewritten to `_export_image(fig, "<cell_index>_mpl0", title=(fig.axes[0].get_title() if fig.axes else ""))`, reusing whatever local variable named `fig` the matplotlib code already assigns (`fig, ax = plt.subplots(...)`).
  - `build_working_copy(src_ipynb: str, dst_ipynb: str) -> int` — reads `src_ipynb` via `nbformat`, applies `transform_cell_source` to every code cell's source, then applies the `MATPLOTLIB_CHART_CELLS` rewrite described above to the matching two cells, prepends `sys.path.insert(0, "scripts")` and `from chart_export import export_chart as _export, export_image as _export_image` plus a module-level `ManifestWriter` instance assigned to `_manifest` to the first code cell, writes the result to `dst_ipynb` via `nbformat.write`. Never writes to `src_ipynb`. Returns the total chart count found across all cells (Plotly + matplotlib).
  - `execute_notebook(nb_path: str, cwd: str) -> None` — executes `nb_path` in place using `nbclient.NotebookClient`, with `resources={"metadata": {"path": cwd}}` so relative paths (the CSV) resolve, raising on any cell execution error.

- [ ] **Step 1: Write the failing tests**

```python
def test_build_working_copy_does_not_touch_source(tmp_path):
    src = tmp_path / "src.ipynb"
    nbformat.write(nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("fig.show()")]), src)
    before = src.read_bytes()
    dst = tmp_path / "dst.ipynb"
    build_working_copy(str(src), str(dst))
    assert src.read_bytes() == before
    assert dst.exists()

def test_build_working_copy_injects_export_calls(tmp_path):
    src = tmp_path / "src.ipynb"
    nbformat.write(nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("fig.show()")]), src)
    dst = tmp_path / "dst.ipynb"
    n = build_working_copy(str(src), str(dst))
    assert n == 1
    nb = nbformat.read(dst, as_version=4)
    assert any("_export(" in c.source for c in nb.cells if c.cell_type == "code")
    assert any("from chart_export import" in c.source for c in nb.cells if c.cell_type == "code")

def test_execute_notebook_runs_simple_notebook(tmp_path):
    nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("x = 1 + 1\nassert x == 2")])
    path = tmp_path / "nb.ipynb"
    nbformat.write(nb, path)
    execute_notebook(str(path), cwd=str(tmp_path))  # must not raise

def test_execute_notebook_raises_on_cell_error(tmp_path):
    nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("raise ValueError('boom')")])
    path = tmp_path / "nb.ipynb"
    nbformat.write(nb, path)
    with pytest.raises(Exception):
        execute_notebook(str(path), cwd=str(tmp_path))

def test_build_working_copy_rewrites_matplotlib_wordcloud_cell(tmp_path, monkeypatch):
    monkeypatch.setattr("notebook_exec.MATPLOTLIB_CHART_CELLS", {0: "wordcloud_test"})
    src = tmp_path / "src.ipynb"
    cell_src = "fig, ax = plt.subplots()\nax.imshow(wc)\nplt.show()\n"
    nbformat.write(nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(cell_src)]), src)
    dst = tmp_path / "dst.ipynb"
    build_working_copy(str(src), str(dst))
    nb = nbformat.read(dst, as_version=4)
    out_src = nb.cells[0].source
    assert '_export_image(fig, "0_mpl0"' in out_src
    assert "plt.show()" not in out_src
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_notebook_exec.py -v`
Expected: FAIL with the functions undefined.

- [ ] **Step 3: Implement `scripts/notebook_exec.py`**

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_notebook_exec.py -v`
Expected: PASS (all 5 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/notebook_exec.py tests/test_notebook_exec.py
git commit -m "feat: add non-destructive notebook execution harness"
```

---

### Task 5: Chart metadata

**Files:**
- Create: `scripts/chart_meta.py`
- Test: `tests/test_chart_meta.py`

**Interfaces:**
- Consumes: nothing from earlier tasks at test time (uses small fixture lists).
- Produces:
  - `strip_markdown(text: str) -> str` — removes `**bold**`/`*italic*` markers, backtick code spans, and `[text](url)` link syntax, leaving plain text (e.g. `"**SQL** is key"` → `"SQL is key"`).
  - `CHART_META: dict[str, dict]` — keyed by chart id (`"<cell_index>_<occurrence>"`), each value `{"section": str, "subsection": str | None, "caption": str}`. `caption` values are plain text (already passed through `strip_markdown` by whoever authored them).
  - `validate(found_ids: list[str]) -> tuple[list[str], list[str]]` — returns `(missing, extra)`: ids in `found_ids` not in `CHART_META`, and ids in `CHART_META` not in `found_ids`.

- [ ] **Step 1: Write the failing tests**

```python
def test_strip_markdown_removes_bold_and_backticks():
    assert strip_markdown("**SQL** is the `universal` requirement") == "SQL is the universal requirement"

def test_strip_markdown_removes_links():
    assert strip_markdown("see [Census data](https://example.com) for details") == "see Census data for details"

def test_validate_reports_missing_and_extra():
    import chart_meta
    chart_meta.CHART_META = {"1_0": {"section": "S", "subsection": None, "caption": "c"}}
    missing, extra = validate(["1_0", "2_0"])
    assert missing == ["2_0"]
    assert extra == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_chart_meta.py -v`
Expected: FAIL with the functions undefined.

- [ ] **Step 3: Implement `strip_markdown` and `validate` in `scripts/chart_meta.py`**

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_chart_meta.py -v`
Expected: PASS (all 3 tests).

- [ ] **Step 5: Discover every real chart id**

Write a short throwaway script (not committed, or committed under `scripts/_discover.py` and removed after use) that loads the real notebook with `nbformat`, calls `transform_cell_source` (Task 2) on every code cell, and prints each discovered `"<cell_index>_<occurrence>"` id next to the cell's source snippet (so a `title=`/`title_text=` string, if present, is visible). This gives the exact list of Plotly chart ids to cover — no need to guess or run the full analysis. Add to this list, by hand: the two matplotlib ids from `MATPLOTLIB_CHART_CELLS` (Task 4, e.g. `"16_mpl0"`, `"17_mpl0"`) and one fixed id for the pyLDAvis panel (e.g. `"29_lda"`, matching whatever id Task 6's Step 1a assigns it).

- [ ] **Step 6: Author `CHART_META` for every discovered id**

Read the notebook's markdown cells and each chart cell's `title=`/`title_text=` argument; for every id from Step 5 (Plotly, matplotlib, and the pyLDAvis entry), add a `CHART_META` entry with its section (one of the 15 `##` headings — the pyLDAvis and both word-cloud ids belong to the sections they visually sit in: section 9 for the LDA panel, section 5 for both word clouds), subsection (only `"11c"`/`"11d"` for section 11's charts, else `None`), and a one-line caption built from the nearest markdown takeaway, passed through `strip_markdown`.

- [ ] **Step 7: Commit**

```bash
git add scripts/chart_meta.py tests/test_chart_meta.py
git commit -m "feat: add chart metadata table and validator"
```

---

### Task 6: CLI orchestrator and full pipeline run

**Files:**
- Create: `scripts/export_charts.py`
- Modify: none

**Interfaces:**
- Consumes: `build_working_copy`, `execute_notebook` (Task 4); `ManifestWriter`, `write_vendor_plotly_js` (Task 3); `CHART_META`, `validate` (Task 5).
- Produces: `main(argv: list[str] | None = None) -> int` — CLI entry point. Returns `0` on success, `1` if `validate()` reports any missing/extra id.

- [ ] **Step 1: Implement `main()` in `scripts/export_charts.py`**

Sequence: ensure `docs/vendor/plotly.min.js` exists (call `write_vendor_plotly_js` if not); call `build_working_copy` on a temp working copy of the real notebook; call `execute_notebook` with `cwd` set to the project root (so the notebook's own `Presentation 4 Jobs data.csv` lookup resolves); **after execution**, check for `pyldavis_topics.html` in the project root (the notebook's own `pyLDAvis.save_html` call writes it there as a side effect) — if present, move it to `docs/charts/pyldavis.html` and append one manifest entry by hand: `{"id": "29_lda", "title": "LDA Topic Model (pyLDAvis)", "file": "charts/pyldavis.html", "thumbnail": None, "interactive": True}`; read the resulting `docs/_manifest_raw.jsonl` line by line, merge each entry (plus the pyLDAvis one) with its `CHART_META` section/subsection/caption; call `validate()` against the merged ids and print `missing`/`extra`; write `docs/charts.js` as `window.CHARTS = <json array>;`; print a one-line summary (counts of interactive vs. static charts, and any ids without a thumbnail).

- [ ] **Step 2: Run the full pipeline against the real notebook**

Run: `python scripts/export_charts.py` from the project root.
Expected: exit code `0`; console reports `0 missing, 0 extra`.

- [ ] **Step 3: Verify outputs on disk**

Check: `docs/charts.js` exists and is non-empty; the number of `docs/charts/*.html` plus `docs/images/*.png` files equals the chart count the script printed; `docs/vendor/plotly.min.js` exists.

- [ ] **Step 4: Spot-check two or three exported charts render correctly**

Open two or three of `docs/charts/*.html` directly in a browser (e.g. one scatter/PCA chart, one choropleth) and confirm hover tooltips and zoom work, and that the numbers match what the live notebook shows for the same chart.

- [ ] **Step 5: Commit**

```bash
git add scripts/export_charts.py docs/charts.js docs/vendor/plotly.min.js docs/charts docs/images docs/thumbs
git commit -m "feat: add pipeline orchestrator and generate the chart gallery assets"
```

---

### Task 7: Gallery grid page

**Files:**
- Create: `docs/index.html`, `docs/styles.css`, `docs/app.js`

**Interfaces:**
- Consumes: `window.CHARTS` (global array, defined by `docs/charts.js` from Task 6), each entry shaped `{id, title, file, thumbnail, interactive, section, subsection, caption}`.
- Produces: a `renderGallery(charts: Array) -> void` function in `app.js` that populates `#gallery` in `index.html` with one tile per chart, grouped into `<section>` blocks by `section` (in notebook order), with a sub-heading for entries whose `subsection` is set.

- [ ] **Step 1: Write `docs/index.html`**

A `<div id="gallery"></div>`, a `<script src="vendor/plotly.min.js"></script>` is **not** needed here (only the presenter view loads chart iframes); load order: `<script src="charts.js"></script>` then `<script src="app.js"></script>`.

- [ ] **Step 2: Write `renderGallery` in `docs/app.js`**

For each chart, a tile shows its `thumbnail` image (or a plain text placeholder card with the title, when `thumbnail` is `null` — covers both the pyLDAvis panel and any chart whose thumbnail export failed) and `title`; clicking a tile sets `location.hash = "#chart/" + chart.id`.

- [ ] **Step 3: Write `docs/styles.css`**

A responsive grid (`CSS grid`, wraps at narrow widths), section headings, tile hover state. No specific values are pinned by the spec — match the notebook's existing chart palette (`presentation_layout` in the notebook: Arial/sans-serif, `#2c3e50` text, `#f8f9fa` background) for visual consistency.

- [ ] **Step 4: Verify by opening `docs/index.html` directly via `file://` in Chrome**

Open the file directly (not through a local server). Expected: the grid renders with every chart's thumbnail/placeholder and title, grouped by section — confirms the manifest loads via the inline `<script>` tag rather than `fetch()`, so it isn't blocked by Chrome's `file://` CORS restriction.

- [ ] **Step 5: Commit**

```bash
git add docs/index.html docs/styles.css docs/app.js
git commit -m "feat: add gallery grid landing page"
```

---

### Task 8: Presenter / slide view

**Files:**
- Modify: `docs/app.js`, `docs/index.html`, `docs/styles.css`

**Interfaces:**
- Consumes: `window.CHARTS` (Task 6); `renderGallery` (Task 7).
- Produces: `renderPresenter(charts: Array, chartId: string) -> void` in `app.js`; a hash-change listener that calls `renderPresenter` when `location.hash` matches `#chart/<id>` and `renderGallery` (clearing the presenter view) otherwise.

- [ ] **Step 1: Add the presenter container to `docs/index.html`**

A `<div id="presenter" hidden></div>` holding: a caption/title bar, a progress readout, an `<iframe id="presenter-frame">`, Previous/Next buttons, and a "Back to gallery" link (`href="#"`).

- [ ] **Step 2: Implement `renderPresenter` in `docs/app.js`**

Looks up `chartId` in `charts` (flattened, ordered by section then original notebook order); sets the iframe's `src` to the chart's `file`; sets the caption bar to `title` + `caption`; sets the progress readout to `"<position> / <total>"`; wires Previous/Next to update `location.hash` to the neighboring chart's id (disabled/no-op at the first/last chart).

- [ ] **Step 3: Add keyboard navigation**

A `keydown` listener on `document`: `ArrowRight`/`ArrowLeft` trigger the same Next/Previous behavior as the buttons, only while the presenter view is visible; `Escape` navigates back to the gallery (clears the hash).

- [ ] **Step 4: Verify manually**

Open `docs/index.html` via `file://`, click a tile, confirm the presenter view opens full-screen on that chart with working Prev/Next buttons and arrow keys, the progress readout updates, and "Back to gallery" (or `Escape`) returns to the grid.

- [ ] **Step 5: Commit**

```bash
git add docs/app.js docs/index.html docs/styles.css
git commit -m "feat: add full-screen presenter view with next/previous navigation"
```

---

### Task 9: Repo finalization

**Files:**
- Create: `README.md`
- Modify: `.gitignore` (final pass)

**Interfaces:** none (closing task, no new code interfaces).

- [ ] **Step 1: Write `README.md`**

Cover: what this repo is (chart gallery for the AN class presentation), how to open it for presenting (clone, open `docs/index.html` in a browser — no server needed), and how to regenerate the gallery if the notebook changes (`python scripts/export_charts.py`).

- [ ] **Step 2: Review `.gitignore`**

Confirm `docs/_manifest_raw.jsonl` and any stray `__pycache__`/`.ipynb_checkpoints` are excluded; confirm generated `docs/charts/`, `docs/images/`, `docs/thumbs/`, `docs/charts.js`, and `docs/vendor/plotly.min.js` are **not** excluded (they're the site itself).

- [ ] **Step 3: Final commit**

```bash
git add README.md .gitignore
git commit -m "docs: add README"
```

- [ ] **Step 4: Document (do not perform) the GitHub push**

Note in the handoff to Casey: this environment has no `gh` CLI, so creating the private GitHub repo and pushing is a manual step — create an empty private repo on GitHub.com, then `git remote add origin <url>` and `git push -u origin main`.
