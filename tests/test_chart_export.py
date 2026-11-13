import json

import plotly.express as px

from chart_export import ManifestWriter, export_chart, write_vendor_plotly_js


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
