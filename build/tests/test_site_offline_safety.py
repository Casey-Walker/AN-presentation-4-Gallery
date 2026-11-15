from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent.parent / "interactive-dashboard"


def test_app_js_never_uses_fetch_or_xhr():
    text = (DOCS_DIR / "app.js").read_text(encoding="utf-8")
    assert "fetch(" not in text
    assert "XMLHttpRequest" not in text


def test_charts_js_is_a_plain_script_not_fetched_json():
    text = (DOCS_DIR / "charts.js").read_text(encoding="utf-8")
    assert text.startswith("window.CHARTS = ")


def test_index_html_loads_charts_via_script_tag_not_fetch():
    text = (DOCS_DIR / "index.html").read_text(encoding="utf-8")
    assert '<script src="charts.js"></script>' in text
    assert "fetch(" not in text
