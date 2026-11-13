import json
import logging
import os
import shutil
import urllib.request

import plotly.offline

logger = logging.getLogger(__name__)

GEO_TOPOJSON_URL = "https://cdn.plot.ly/un/usa_110m.json"
GEO_TOPOJSON_NAME = "usa_110m"


def write_vendor_plotly_js(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(plotly.offline.get_plotlyjs())


def build_geo_assets_js(topojson: dict) -> str:
    return (
        "window.PlotlyGeoAssets = window.PlotlyGeoAssets || {topojson: {}};\n"
        f"window.PlotlyGeoAssets.topojson[{json.dumps(GEO_TOPOJSON_NAME)}] = "
        f"{json.dumps(topojson)};\n"
    )


# Some CDNs (d3js.org among them) reject urllib's default "Python-urllib/x.y"
# User-Agent outright; a plain browser-looking one is accepted by all of them.
_DOWNLOAD_HEADERS = {"User-Agent": "Mozilla/5.0"}


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=_DOWNLOAD_HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def write_geo_assets_js(path: str, url: str = GEO_TOPOJSON_URL) -> None:
    topojson = json.loads(_fetch(url))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_geo_assets_js(topojson))


def download_text(url: str, path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    text = _fetch(url).decode("utf-8")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def rewrite_pyldavis_urls(html: str, url_to_local: dict) -> str:
    for url in sorted(url_to_local, key=len, reverse=True):
        html = html.replace(url, url_to_local[url])
    return html


class ManifestWriter:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    def append(self, entry: dict) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")


_GEO_TRACE_TYPES = {"choropleth", "scattergeo"}

# Chart pages render in an <iframe>; once a click lands inside one (to use
# the chart's own zoom/hover/legend controls), keydown events go to that
# iframe's document and the presenter's Next/Previous/Escape shortcuts stop
# working. This forwards arrow/Escape keys to the parent page via
# postMessage so presenter navigation still works.
KEY_FORWARD_SCRIPT = (
    "document.addEventListener('keydown', function(e) {"
    "  if (e.key === 'ArrowRight' || e.key === 'ArrowLeft' || e.key === 'Escape') {"
    "    parent.postMessage({type: 'presenter-key', key: e.key}, '*');"
    "  }"
    "});"
)


def has_geo_trace(fig) -> bool:
    return any(trace.type in _GEO_TRACE_TYPES for trace in fig.data)


def export_chart(fig, chart_id: str, out_dir: str, thumb_dir: str, vendor_rel_path: str,
                  geo_assets_rel_path: str | None = None) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(thumb_dir, exist_ok=True)

    html_path = os.path.join(out_dir, f"{chart_id}.html")
    fig.write_html(html_path, include_plotlyjs=vendor_rel_path, full_html=True,
                    post_script=KEY_FORWARD_SCRIPT)

    if geo_assets_rel_path and has_geo_trace(fig):
        with open(html_path, encoding="utf-8") as f:
            html = f.read()
        src_pos = html.index(f'src="{vendor_rel_path}"')
        tag_start = html.rfind("<script", 0, src_pos)
        geo_tag = f'<script src="{geo_assets_rel_path}"></script>'
        html = html[:tag_start] + geo_tag + html[tag_start:]
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

    thumb_path = os.path.join(thumb_dir, f"{chart_id}.png")
    thumbnail = f"thumbs/{chart_id}.png"
    try:
        fig.write_image(thumb_path, width=400, height=260)
    except Exception as exc:
        logger.warning("thumbnail export failed for chart %s: %s", chart_id, exc)
        thumbnail = None

    title = fig.layout.title.text if fig.layout.title and fig.layout.title.text else ""

    return {
        "id": chart_id,
        "title": title,
        "file": f"charts/{chart_id}.html",
        "thumbnail": thumbnail,
        "interactive": True,
    }


def export_image(mpl_fig, chart_id: str, img_dir: str, thumb_dir: str, title: str) -> dict:
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(thumb_dir, exist_ok=True)

    img_path = os.path.join(img_dir, f"{chart_id}.png")
    mpl_fig.savefig(img_path)

    thumb_path = os.path.join(thumb_dir, f"{chart_id}.png")
    shutil.copyfile(img_path, thumb_path)

    return {
        "id": chart_id,
        "title": title,
        "file": f"images/{chart_id}.png",
        "thumbnail": f"thumbs/{chart_id}.png",
        "interactive": False,
    }
