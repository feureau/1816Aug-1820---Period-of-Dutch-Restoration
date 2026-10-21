/**
 * render.js — loads all individual transcriptions sequentially and renders them into #markdown-output using marked.
 */
(async function () {
  "use strict";

  const OUTPUT_ID = "markdown-output";

  function showError(out, err) {
    out.innerHTML =
      '<div class="render-error">' +
      "<h2>Could not load document</h2>" +
      "<pre>" +
      String(err && err.message ? err.message : err)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;") +
      "</pre>" +
      "<p>Check your console for more details.</p>" +
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

  async function renderAll() {
    const out = document.getElementById(OUTPUT_ID);
    if (!out) return;

    if (typeof marked === "undefined") {
      showError(out, new Error("marked.min.js did not load. Check that it sits next to full.html."));
      return;
    }

    const list = window.__TRANSCRIPTIONS_DATA__ || [];
    if (list.length === 0) {
      showError(out, new Error("No transcription data found. Make sure transcriptions-data.js is loaded."));
      return;
    }

    out.innerHTML = ""; // Clear "Loading..."

    for (const entry of list) {
      let mdText = "";
      const src = entry.text;

      // 1. Try to fetch live file (works on http/https)
      if (location.protocol === "http:" || location.protocol === "https:") {
        try {
          const res = await fetch(src, { cache: "no-store" });
          if (res.ok) {
            mdText = await res.text();
          }
        } catch (_) { /* fall through */ }
      }

      // 2. Fallback to bundled content (works on file://)
      if (!mdText) {
        const embedded = (window.__TRANSCRIPTIONS_CONTENT__ || {})[entry.id];
        if (typeof embedded === "string") {
          mdText = embedded;
        }
      }

      if (mdText) {
        const section = document.createElement("div");
        section.className = "transcription-section";
        section.style.marginBottom = "40px";
        section.style.borderBottom = "1px solid #333";
        section.style.paddingBottom = "20px";

        const contentHTML = marked.parse(mdText);
        section.innerHTML = `<h2 id="${entry.id}">${entry.id}</h2>\n` + contentHTML;
        out.appendChild(section);
      } else {
        console.warn(`Could not load text for ${entry.id}`);
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      configureMarked();
      renderAll();
    });
  } else {
    configureMarked();
    renderAll();
  }
})();
