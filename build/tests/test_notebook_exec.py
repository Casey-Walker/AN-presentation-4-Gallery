import json
import shutil
from pathlib import Path

import nbformat
import pytest

from notebook_exec import build_working_copy, collect_stream_warnings, execute_notebook

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


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


def test_build_working_copy_raises_if_a_show_call_is_left_untransformed(tmp_path):
    src = tmp_path / "src.ipynb"
    cell_src = "other_widget.show()\n"
    nbformat.write(nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(cell_src)]), src)
    dst = tmp_path / "dst.ipynb"
    with pytest.raises(ValueError, match="untransformed"):
        build_working_copy(str(src), str(dst))


def test_collect_stream_warnings_finds_marked_print_output(tmp_path):
    nb = nbformat.v4.new_notebook(cells=[
        nbformat.v4.new_code_cell("print('[chart_export] thumbnail export failed for chart 24_0: boom')"),
        nbformat.v4.new_code_cell("print('ordinary output, not a warning')"),
    ])
    path = tmp_path / "nb.ipynb"
    nbformat.write(nb, path)
    execute_notebook(str(path), cwd=str(tmp_path))
    warnings = collect_stream_warnings(str(path))
    assert warnings == ["[chart_export] thumbnail export failed for chart 24_0: boom"]


def test_repeated_calls_to_same_static_id_get_deduped_at_runtime(tmp_path):
    cell_src = (
        "import plotly.express as px\n"
        "def make_chart(y):\n"
        "    fig = px.bar(x=[1], y=[y])\n"
        "    fig.show()\n"
        "make_chart(1)\n"
        "make_chart(2)\n"
    )
    src = tmp_path / "src.ipynb"
    nbformat.write(nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(cell_src)]), src)
    dst = tmp_path / "dst.ipynb"
    build_working_copy(str(src), str(dst))

    (tmp_path / "scripts").mkdir()
    shutil.copy(SCRIPTS_DIR / "chart_export.py", tmp_path / "scripts" / "chart_export.py")

    execute_notebook(str(dst), cwd=str(tmp_path))

    manifest_path = tmp_path / "interactive-dashboard" / "_manifest_raw.jsonl"
    ids = [json.loads(line)["id"] for line in manifest_path.read_text().splitlines()]
    assert ids == ["0_0", "0_0_1"]
