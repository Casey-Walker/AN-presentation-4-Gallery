import json
import logging
import os
import shutil

import plotly.offline

logger = logging.getLogger(__name__)


def write_vendor_plotly_js(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(plotly.offline.get_plotlyjs())


class ManifestWriter:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    def append(self, entry: dict) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")


def export_chart(fig, chart_id: str, out_dir: str, thumb_dir: str, vendor_rel_path: str) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(thumb_dir, exist_ok=True)

    html_path = os.path.join(out_dir, f"{chart_id}.html")
    fig.write_html(html_path, include_plotlyjs=vendor_rel_path, full_html=True)

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
