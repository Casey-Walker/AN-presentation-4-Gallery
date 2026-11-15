function groupBySectionThenSubsection(charts) {
  const sections = new Map();
  for (const chart of charts) {
    if (!sections.has(chart.section)) sections.set(chart.section, []);
    sections.get(chart.section).push(chart);
  }

  const groups = [];
  for (const [sectionName, sectionCharts] of sections) {
    const subsections = new Map();
    for (const chart of sectionCharts) {
      const key = chart.subsection || "";
      if (!subsections.has(key)) subsections.set(key, []);
      subsections.get(key).push(chart);
    }
    groups.push({ sectionName, subsections });
  }
  return groups;
}

function flattenOrdered(charts) {
  const flat = [];
  for (const { subsections } of groupBySectionThenSubsection(charts)) {
    for (const subCharts of subsections.values()) {
      flat.push(...subCharts);
    }
  }
  return flat;
}

function renderGallery(charts) {
  const gallery = document.getElementById("gallery");
  gallery.innerHTML = "";

  for (const { sectionName, subsections } of groupBySectionThenSubsection(charts)) {
    const section = document.createElement("section");
    section.className = "chart-section";

    const heading = document.createElement("h2");
    heading.textContent = sectionName;
    section.appendChild(heading);

    for (const [subsectionName, subCharts] of subsections) {
      if (subsectionName) {
        const subHeading = document.createElement("h3");
        subHeading.textContent = subsectionName;
        section.appendChild(subHeading);
      }

      const grid = document.createElement("div");
      grid.className = "tile-grid";

      for (const chart of subCharts) {
        grid.appendChild(renderTile(chart));
      }

      section.appendChild(grid);
    }

    gallery.appendChild(section);
  }
}

function renderTile(chart) {
  const tile = document.createElement("a");
  tile.className = "tile";
  tile.href = "#chart/" + chart.id;

  if (chart.thumbnail) {
    const img = document.createElement("img");
    img.src = chart.thumbnail;
    img.alt = chart.title;
    tile.appendChild(img);
  } else {
    const placeholder = document.createElement("div");
    placeholder.className = "tile-placeholder";
    placeholder.textContent = chart.title;
    tile.appendChild(placeholder);
  }

  if (!chart.interactive) {
    const badge = document.createElement("span");
    badge.className = "tile-badge";
    badge.textContent = "Static image";
    tile.appendChild(badge);
  }

  const overlay = document.createElement("div");
  overlay.className = "tile-overlay";
  const caption = document.createElement("p");
  caption.className = "tile-title";
  caption.textContent = chart.title;
  overlay.appendChild(caption);
  tile.appendChild(overlay);

  return tile;
}

function renderPresenter(charts, chartId) {
  const ordered = flattenOrdered(charts);
  const index = ordered.findIndex((c) => c.id === chartId);
  if (index === -1) return;

  const chart = ordered[index];
  const total = ordered.length;

  document.getElementById("gallery").hidden = true;
  const presenter = document.getElementById("presenter");
  presenter.hidden = false;

  document.getElementById("presenter-frame").src = chart.file;
  document.getElementById("presenter-title").textContent = chart.title + (chart.interactive ? "" : " (static image)");
  document.getElementById("presenter-text").textContent = chart.caption;
  document.getElementById("presenter-progress").textContent = (index + 1) + " / " + total;

  const prevBtn = document.getElementById("presenter-prev");
  const nextBtn = document.getElementById("presenter-next");
  prevBtn.disabled = index === 0;
  nextBtn.disabled = index === total - 1;
  prevBtn.onclick = () => {
    if (index > 0) location.hash = "#chart/" + ordered[index - 1].id;
  };
  nextBtn.onclick = () => {
    if (index < total - 1) location.hash = "#chart/" + ordered[index + 1].id;
  };
}

function showGallery() {
  document.getElementById("presenter").hidden = true;
  document.getElementById("gallery").hidden = false;
}

function handleHashChange() {
  const match = location.hash.match(/^#chart\/(.+)$/);
  if (match) {
    renderPresenter(window.CHARTS, decodeURIComponent(match[1]));
  } else {
    showGallery();
  }
}

function handlePresenterKey(key) {
  const presenter = document.getElementById("presenter");
  if (presenter.hidden) return;

  if (key === "ArrowRight") {
    document.getElementById("presenter-next").click();
  } else if (key === "ArrowLeft") {
    document.getElementById("presenter-prev").click();
  } else if (key === "Escape") {
    location.hash = "";
  }
}

document.addEventListener("keydown", (event) => handlePresenterKey(event.key));

// Chart pages run in an <iframe>: once a click lands inside one (to use the
// chart's own zoom/hover/legend controls), keydown events go to that
// iframe's document instead of this one. Each chart's own page forwards
// arrow/Escape keys here via postMessage so navigation still works.
window.addEventListener("message", (event) => {
  if (event.data && event.data.type === "presenter-key") {
    handlePresenterKey(event.data.key);
  }
});

window.addEventListener("hashchange", handleHashChange);

renderGallery(window.CHARTS);
handleHashChange();
