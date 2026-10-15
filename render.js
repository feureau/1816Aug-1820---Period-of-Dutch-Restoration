/**
 * render.js — load "1816Aug-1820 - Period of Dutch Restoration.md" live
 * and render it into #markdown-output using marked.
 */
(function () {
  "use strict";

  const SOURCE_FILE = "1816Aug-1820 - Period of Dutch Restoration.md";
  const OUTPUT_ID = "markdown-output";

  async function getMarkdown() {
    try {
      const res = await fetch(SOURCE_FILE, { cache: "no-store" });
      if (res.ok) {
        const text = await res.text();
        if (text.trim()) return text;
      }
      throw new Error(`Failed to load ${SOURCE_FILE} (status ${res.status})`);
    } catch (err) {
      throw new Error(
        `Could not fetch ${SOURCE_FILE}.\n` +
        "Make sure you are running a local web server in this directory:\n" +
        "  python -m http.server 8000\n" +
        "then visit: http://localhost:8000/full.html"
      );
    }
  }

  function showError(out, err) {
    out.innerHTML =
      '<div class="render-error">' +
      "<h2>Could not load document</h2>" +
      "<pre>" +
      String(err && err.message ? err.message : err)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;") +
      "</pre>" +
      "<p>Start a local web server in your project folder:</p>" +
      "<pre>python -m http.server 8000</pre>" +
      "<p>Then visit: <a href='http://localhost:8000/full.html'>" +
      "http://localhost:8000/full.html</a></p>" +
      "</div>";
  }

  function configureMarked() {
    if (typeof marked === "undefined") return;
    marked.setOptions({
      gfm: true,
      breaks: false,
      mangle: false,
    });
  }

  function addHeaderIds(container) {
    const headings = container.querySelectorAll("h1, h2, h3, h4, h5, h6");
    headings.forEach(h => {
      const text = h.textContent;
      const id = text.toLowerCase()
        .replace(/[^\w\s-]/g, "")
        .replace(/\s+/g, "-")
        .replace(/-+/g, "-")
        .replace(/^-+|-+$/g, "");
      h.id = id;
    });
  }

  async function render() {
    const out = document.getElementById(OUTPUT_ID);
    if (!out) return;

    try {
      const md = await getMarkdown();
      if (typeof marked === "undefined") {
        throw new Error(
          "marked.min.js did not load. Check that it sits next to full.html."
        );
      }
      out.innerHTML = marked.parse(md);
      addHeaderIds(out);
      document.title =
        (md.match(/^#\s+(.+)$/m) || [, document.title])[1].trim();
    } catch (err) {
      console.error(err);
      showError(out, err);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      configureMarked();
      render();
    });
  } else {
    configureMarked();
    render();
  }
})();
