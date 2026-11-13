import nbformat
import pytest

from notebook_exec import build_working_copy, execute_notebook


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
