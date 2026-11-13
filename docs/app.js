function renderGallery(charts) {
  const gallery = document.getElementById("gallery");
  gallery.innerHTML = "";

  const sections = new Map();
  for (const chart of charts) {
    if (!sections.has(chart.section)) sections.set(chart.section, []);
    sections.get(chart.section).push(chart);
  }

  for (const [sectionName, sectionCharts] of sections) {
    const section = document.createElement("section");
    section.className = "chart-section";

    const heading = document.createElement("h2");
    heading.textContent = sectionName;
    section.appendChild(heading);

    const subsections = new Map();
    for (const chart of sectionCharts) {
      const key = chart.subsection || "";
      if (!subsections.has(key)) subsections.set(key, []);
      subsections.get(key).push(chart);
    }

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

  const caption = document.createElement("div");
  caption.className = "tile-title";
  caption.textContent = chart.title;
  tile.appendChild(caption);

  return tile;
}

renderGallery(window.CHARTS);
