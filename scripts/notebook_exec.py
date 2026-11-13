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
    "from chart_export import export_chart as _export, export_image as _export_image, ManifestWriter\n"
    "_manifest = ManifestWriter(\"docs/_manifest_raw.jsonl\")\n"
)


def _rewrite_matplotlib_show(source: str, cell_index: int) -> str:
    slug = MATPLOTLIB_CHART_CELLS[cell_index]
    chart_id = f"{cell_index}_mpl0"
    replacement = (
        f'_export_image(fig, "{chart_id}", "docs/images", "docs/thumbs", '
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
