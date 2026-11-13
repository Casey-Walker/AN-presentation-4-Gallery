import json
import os
import shutil
import sys
from pathlib import Path

from chart_export import write_vendor_plotly_js
from chart_meta import CHART_META, validate
from notebook_exec import build_working_copy, execute_notebook

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_IPYNB = PROJECT_ROOT / "Presentation 4 - Metro Analytics Notebook.ipynb"
BUILD_DIR = PROJECT_ROOT / ".superpowers" / "build"
WORKING_COPY = BUILD_DIR / "working_copy.ipynb"
DOCS_DIR = PROJECT_ROOT / "docs"
VENDOR_JS = DOCS_DIR / "vendor" / "plotly.min.js"
RAW_MANIFEST = DOCS_DIR / "_manifest_raw.jsonl"
CHARTS_JS = DOCS_DIR / "charts.js"
PYLDAVIS_SRC = PROJECT_ROOT / "pyldavis_topics.html"
PYLDAVIS_DST = DOCS_DIR / "charts" / "pyldavis.html"
PYLDAVIS_ENTRY = {
    "id": "29_lda",
    "title": "LDA Topic Model (pyLDAvis)",
    "file": "charts/pyldavis.html",
    "thumbnail": None,
    "interactive": True,
}


def _clean_build_outputs() -> None:
    for d in ("charts", "images", "thumbs"):
        shutil.rmtree(DOCS_DIR / d, ignore_errors=True)
    RAW_MANIFEST.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    _clean_build_outputs()

    if not VENDOR_JS.exists():
        write_vendor_plotly_js(str(VENDOR_JS))

    build_working_copy(str(SRC_IPYNB), str(WORKING_COPY))
    execute_notebook(str(WORKING_COPY), cwd=str(PROJECT_ROOT))

    raw_entries = []
    if RAW_MANIFEST.exists():
        with open(RAW_MANIFEST, encoding="utf-8") as f:
            raw_entries = [json.loads(line) for line in f if line.strip()]

    if PYLDAVIS_SRC.exists():
        PYLDAVIS_DST.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(PYLDAVIS_SRC), str(PYLDAVIS_DST))
        raw_entries.append(PYLDAVIS_ENTRY)

    found_ids = [e["id"] for e in raw_entries]
    missing, extra = validate(found_ids)
    print(f"{len(missing)} missing, {len(extra)} extra")
    if missing:
        print("missing (no CHART_META entry):", missing)
    if extra:
        print("extra (in CHART_META but not produced):", extra)

    merged = []
    for entry in raw_entries:
        meta = CHART_META.get(entry["id"], {"section": "Uncategorized", "subsection": None, "caption": ""})
        merged.append({**entry, **meta})

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    with open(CHARTS_JS, "w", encoding="utf-8") as f:
        f.write("window.CHARTS = ")
        json.dump(merged, f, indent=2)
        f.write(";\n")

    n_interactive = sum(1 for e in merged if e["interactive"])
    n_static = sum(1 for e in merged if not e["interactive"])
    no_thumb = [e["id"] for e in merged if e.get("thumbnail") is None]
    print(f"{n_interactive} interactive, {n_static} static charts exported")
    if no_thumb:
        print("no thumbnail:", no_thumb)

    return 1 if (missing or extra) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
