import nbformat
from nbclient import NotebookClient

from chart_transform import transform_cell_source

MATPLOTLIB_CHART_CELLS: dict[int, str] = {
    16: "wordcloud_before_after",
    17: "wordcloud_entry_accessible",
}

_PRELUDE = (
    "import sys\n"
    "sys.path.insert(0, \"scripts\")\n"
    "from chart_export import export_chart as _export_chart, export_image as _export_image_impl, ManifestWriter\n"
    "_manifest = ManifestWriter(\"interactive-dashboard/_manifest_raw.jsonl\")\n"
    "_seen_chart_ids = {}\n"
    "def _dedupe_id(chart_id):\n"
    "    n = _seen_chart_ids.get(chart_id, 0)\n"
    "    _seen_chart_ids[chart_id] = n + 1\n"
    "    return chart_id if n == 0 else f\"{chart_id}_{n}\"\n"
    "def _export(fig, chart_id):\n"
    "    entry = _export_chart(fig, _dedupe_id(chart_id), \"interactive-dashboard/charts\", \"interactive-dashboard/thumbs\", \"../vendor/plotly.min.js\", \"../vendor/geo-assets.js\")\n"
    "    _manifest.append(entry)\n"
    "    return entry\n"
    "def _export_image(fig, chart_id, img_dir, thumb_dir, title):\n"
    "    entry = _export_image_impl(fig, _dedupe_id(chart_id), img_dir, thumb_dir, title)\n"
    "    _manifest.append(entry)\n"
    "    return entry\n"
)


def _rewrite_matplotlib_show(source: str, cell_index: int) -> str:
    slug = MATPLOTLIB_CHART_CELLS[cell_index]
    chart_id = f"{cell_index}_mpl0"
    replacement = (
        f'_export_image(fig, "{chart_id}", "interactive-dashboard/images", "interactive-dashboard/thumbs", '
        f'(fig.axes[0].get_title() if fig.axes else ""))'
    )
    return source.replace("plt.show()", replacement)


def build_working_copy(src_ipynb: str, dst_ipynb: str) -> int:
    nb = nbformat.read(src_ipynb, as_version=4)
    total_charts = 0
    first_code_cell = True

    for cell_index, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        new_source, n = transform_cell_source(cell.source, cell_index)
        total_charts += n
        if cell_index in MATPLOTLIB_CHART_CELLS:
            new_source = _rewrite_matplotlib_show(new_source, cell_index)
            total_charts += 1
        if ".show()" in new_source:
            raise ValueError(
                f"cell {cell_index}: a .show() call was left untransformed after "
                "chart extraction -- it would silently render inline instead of "
                "being exported, and CHART_META validation would never catch it "
                "since it never becomes a chart id"
            )
        if first_code_cell:
            new_source = _PRELUDE + new_source
            first_code_cell = False
        cell.source = new_source

    nbformat.write(nb, dst_ipynb)
    return total_charts


def execute_notebook(nb_path: str, cwd: str) -> None:
    nb = nbformat.read(nb_path, as_version=4)
    client = NotebookClient(nb, resources={"metadata": {"path": cwd}})
    client.execute()
    nbformat.write(nb, nb_path)


def collect_stream_warnings(nb_path: str, marker: str = "[chart_export]") -> list[str]:
    """Scans an already-executed notebook's stdout for lines containing
    `marker`. The kernel that runs it is a separate process with no console
    of its own, so this is how a print() inside the injected prelude (e.g.
    a thumbnail export failure) becomes visible to whoever ran the build."""
    nb = nbformat.read(nb_path, as_version=4)
    warnings = []
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") == "stream":
                for line in output.get("text", "").splitlines():
                    if marker in line:
                        warnings.append(line)
    return warnings
