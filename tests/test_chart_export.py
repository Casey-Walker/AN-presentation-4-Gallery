import json

import plotly.express as px

from chart_export import (
    ManifestWriter,
    build_geo_assets_js,
    export_chart,
    has_geo_trace,
    rewrite_pyldavis_urls,
    write_vendor_plotly_js,
)


def test_export_chart_writes_html_and_thumbnail(tmp_path):
    fig = px.bar(x=[1, 2], y=[3, 4], title="Test Chart")
    entry = export_chart(fig, "99_0", str(tmp_path / "charts"), str(tmp_path / "thumbs"), "../vendor/plotly.min.js")
    assert (tmp_path / "charts" / "99_0.html").exists()
    assert (tmp_path / "thumbs" / "99_0.png").exists()
    assert entry == {"id": "99_0", "title": "Test Chart", "file": "charts/99_0.html",
                      "thumbnail": "thumbs/99_0.png", "interactive": True}


def test_export_chart_forwards_arrow_and_escape_keys_to_parent(tmp_path):
    fig = px.bar(x=[1, 2], y=[3, 4], title="Test Chart")
    export_chart(fig, "99_4", str(tmp_path / "charts"), str(tmp_path / "thumbs"), "../vendor/plotly.min.js")
    html = (tmp_path / "charts" / "99_4.html").read_text(encoding="utf-8")
    assert "presenter-key" in html
    assert "parent.postMessage" in html


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


def test_has_geo_trace_true_for_choropleth():
    fig = px.choropleth(locations=["CA"], locationmode="USA-states", color=[1], scope="usa")
    assert has_geo_trace(fig) is True


def test_has_geo_trace_false_for_bar():
    fig = px.bar(x=[1, 2], y=[3, 4])
    assert has_geo_trace(fig) is False


def test_export_chart_injects_geo_assets_script_for_geo_figure(tmp_path):
    fig = px.choropleth(locations=["CA"], locationmode="USA-states", color=[1], scope="usa")
    export_chart(fig, "99_2", str(tmp_path / "charts"), str(tmp_path / "thumbs"),
                 "../vendor/plotly.min.js", geo_assets_rel_path="../vendor/geo-assets.js")
    html = (tmp_path / "charts" / "99_2.html").read_text(encoding="utf-8")
    geo_pos = html.index('src="../vendor/geo-assets.js"')
    plotly_pos = html.index('src="../vendor/plotly.min.js"')
    assert geo_pos < plotly_pos


def test_build_geo_assets_js_embeds_topojson_under_usa_110m_key():
    js = build_geo_assets_js({"type": "Topology", "objects": {}})
    assert 'window.PlotlyGeoAssets.topojson["usa_110m"]' in js
    assert '"Topology"' in js


def test_rewrite_pyldavis_urls_replaces_known_cdn_urls():
    html = (
        '<link href="https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.4.0/pyLDAvis/js/ldavis.v1.0.0.css">'
        'require.config({paths: {d3: "https://d3js.org/d3.v5"}});'
        'LDAvis_load_lib("https://d3js.org/d3.v5.js", ...)'
        'LDAvis_load_lib("https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.4.0/pyLDAvis/js/ldavis.v3.0.0.js", ...)'
    )
    out = rewrite_pyldavis_urls(html, {
        "https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.4.0/pyLDAvis/js/ldavis.v1.0.0.css": "../vendor/ldavis.v1.0.0.css",
        "https://d3js.org/d3.v5.js": "../vendor/d3.v5.js",
        "https://d3js.org/d3.v5": "../vendor/d3.v5.js",
        "https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.4.0/pyLDAvis/js/ldavis.v3.0.0.js": "../vendor/ldavis.v3.0.0.js",
    })
    assert "https://" not in out
    assert "../vendor/ldavis.v1.0.0.css" in out
    assert "../vendor/d3.v5.js" in out
    assert "../vendor/ldavis.v3.0.0.js" in out


def test_export_chart_omits_geo_assets_script_for_non_geo_figure(tmp_path):
    fig = px.bar(x=[1, 2], y=[3, 4])
    export_chart(fig, "99_3", str(tmp_path / "charts"), str(tmp_path / "thumbs"),
                 "../vendor/plotly.min.js", geo_assets_rel_path="../vendor/geo-assets.js")
    html = (tmp_path / "charts" / "99_3.html").read_text(encoding="utf-8")
    assert "geo-assets.js" not in html
