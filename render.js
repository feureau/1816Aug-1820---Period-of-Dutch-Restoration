/**
 * render.js — load document.md (live over HTTP, embedded under file://)
 * and render it into #markdown-output using marked.
 */
(function () {
  "use strict";

  const SOURCE_FILE = "1816Aug-1820 - Period of Dutch Restoration.md";
  const OUTPUT_ID = "markdown-output";

  async function getMarkdown() {
    const embedded = (window.__BOOK_DATA__ || {})[SOURCE_FILE];

    // Under http(s)://, try the live file first so edits show up on refresh.
    if (location.protocol === "http:" || location.protocol === "https:") {
      try {
        const res = await fetch(SOURCE_FILE, { cache: "no-store" });
        if (res.ok) {
          const text = await res.text();
          if (text.trim()) return text;
        }
      } catch (_) {
        // Network hiccup — fall through to embedded.
      }
    }

    // file:// or fetch failed → use whatever build.py baked in.
    if (typeof embedded === "string" && embedded.length) {
      return embedded;
    }

    throw new Error(
      "No markdown source. Either serve this folder over HTTP " +
        "(python3 -m http.server) or run build.py to regenerate book-data.js."
    );
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
      "<p>If you opened this file with <code>file://</code>, " +
      "start a local server in this folder:</p>" +
      "<pre>python3 -m http.server 8000</pre>" +
      "<p>then visit <a href='http://localhost:8000/full.html'>" +
      "http://localhost:8000/full.html</a>.</p>" +
      "</div>";
  }

  function configureMarked() {
    if (typeof marked === "undefined") return;
    
    // Modern marked versions use marked.use() for extensions
    // but for the minified basic version, we ensure options are set.
    // Note: headerIds was moved to a separate extension in marked 5.0+
    // We will try to use the options object for compatibility.
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
