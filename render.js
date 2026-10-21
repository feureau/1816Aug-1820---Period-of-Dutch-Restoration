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

    // Listen for clicks on dynamically generated GitHub buttons
    out.addEventListener("click", (e) => {
      const btn = e.target.closest(".github-report-btn");
      if (!btn) return;
      e.preventDefault();

      const entryId = btn.getAttribute("data-id");
      const section = btn.closest(".transcription-section");

      const sel = window.getSelection();
      let selectionText = "";

      if (sel.rangeCount > 0 && section && section.contains(sel.anchorNode)) {
          selectionText = sel.toString().trim();
      }

      let body = `**Transcription ID:** ${entryId}\n\n`;
      if (selectionText) {
          body += `**Original Text:**\n> ${selectionText.replace(/\n/g, '\n> ')}\n\n`;
      }
      body += `**Suggested Correction / Notes:**\n`;

      const url = `https://github.com/Feureau/1816Aug-1820---Period-of-Dutch-Restoration/issues/new?title=${encodeURIComponent('Transcription Note: ' + entryId)}&body=${encodeURIComponent(body)}`;
      window.open(url, '_blank');
    });

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

        const buttonHtml = `<div style="margin-top: 10px; margin-bottom: 20px;"><a href="#" class="btn github-report-btn" data-id="${entry.id}" style="background:#2ea043; border-color:#2ea043; color:white; display:inline-flex; align-items:center; gap:6px; padding:6px 12px; border-radius:5px; text-decoration:none; font-family:Arial, sans-serif; font-size:0.88rem;"><svg height="16" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" style="fill:white;"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.46-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path></svg> Report Issue on GitHub</a></div>`;

        const contentHTML = marked.parse(mdText);
        section.innerHTML = `<h2 id="${entry.id}" style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #333; padding-bottom:10px;">${entry.id} ${buttonHtml}</h2>\n` + contentHTML;
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
