/**
 * viewer.js — render one transcription + its scan side by side.
 * Picks the transcript from ?id=IMG_xxxx (or the first entry).
 * Under http(s):// it fetches the live .txt so edits show up on refresh.
 * Under file:// it uses the copy baked into transcriptions-content.js.
 */
(function () {
  "use strict";

  const OUTPUT_ID     = "transcript-output";
  const TITLE_ID      = "doc-title";
  const SCAN_ID       = "scan";
  const SCAN_LINK_ID  = "scan-link";
  const SCAN_NOTE_ID  = "scan-note";
  const GITHUB_REPO   = "Feureau/1816Aug-1820---Period-of-Dutch-Restoration";

  /* ---------- lookup helpers ---------- */
  function list() { return window.__TRANSCRIPTIONS_DATA__ || []; }

  function getEntry(id) {
    const l = list();
    if (!id) return l[0];
    return l.find(e => e.id === id) || l[0];
  }

  /* ---------- markdown source ---------- */
  async function getMarkdown(entry) {
    const embedded = (window.__TRANSCRIPTIONS_CONTENT__ || {})[entry.id];
    const src = entry.text;

    // Live fetch when served over HTTP so .txt edits appear on refresh.
    if (location.protocol === "http:" || location.protocol === "https:") {
      try {
        const res = await fetch(src, { cache: "no-store" });
        if (res.ok) {
          const text = await res.text();
          if (text.trim()) return text;
        }
      } catch (_) { /* fall through to embedded */ }
    }

    if (typeof embedded === "string" && embedded.length) return embedded;

    throw new Error(
      "No transcript source for " + entry.id +
      ".  Run `python3 build-transcriptions.py` to regenerate " +
      "transcriptions-content.js, or serve the folder over HTTP."
    );
  }

  /* ---------- marked setup ---------- */
  function configureMarked() {
    if (typeof marked === "undefined") return;
    marked.setOptions({
      gfm: true,       // tables, task lists, autolinks
      breaks: false,
      mangle: false,
    });
  }

  function addHeaderIds(root) {
    root.querySelectorAll("h1,h2,h3,h4,h5,h6").forEach(h => {
      h.id = h.textContent
        .toLowerCase()
        .replace(/[^\w\s-]/g, "")
        .replace(/\s+/g, "-")
        .replace(/-+/g, "-")
        .replace(/^-+|-+$/g, "");
    });
  }

  /* ---------- scan image (with folder/extension fallbacks) ---------- */
  function imageCandidates(entry) {
    const id  = entry.id;
    const out = [];
    const exts    = ["jpg", "jpeg", "JPG", "JPEG", "png", "PNG"];
    const folders = ["", "jpg", "jpeg", "images", "img", "scans"];

    if (entry.image) out.push(entry.image);

    for (const f of folders) {
      for (const e of exts) {
        const p = f ? `${f}/${id}.${e}` : `${id}.${e}`;
        if (!out.includes(p)) out.push(p);
      }
    }
    return out;
  }

  async function setupImage(entry) {
    const img   = document.getElementById(SCAN_ID);
    const link  = document.getElementById(SCAN_LINK_ID);
    const note  = document.getElementById(SCAN_NOTE_ID);
    const cands = imageCandidates(entry);
    let working = cands[0];

    // Probe over HTTP; under file:// just try the first and let onerror step forward.
    if (location.protocol === "http:" || location.protocol === "https:") {
      for (const c of cands) {
        try {
          const r = await fetch(c, { method: "HEAD" });
          if (r.ok) { working = c; break; }
        } catch (_) {}
      }
    }

    img.alt   = "Scan of " + entry.id;
    img.style.cursor = "zoom-in";
    // img.onclick = () => window.open(img.src, "_blank"); // disabled per user request
    // ---- Pan & Zoom state ----
    let scale = 1;
    let translateX = 0;
    let translateY = 0;
    const updateTransform = () => {
      img.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    };
    // Wheel zoom (mouse wheel or touchpad)
    img.addEventListener('wheel', (e) => {
      e.preventDefault();
      const delta = e.deltaY < 0 ? 1.1 : 0.9;
      // Compute cursor position relative to image
      const rect = img.getBoundingClientRect();
      const offsetX = e.clientX - rect.left;
      const offsetY = e.clientY - rect.top;
      // Adjust translation to keep point under cursor stationary
      translateX = (translateX - offsetX) * delta + offsetX;
      translateY = (translateY - offsetY) * delta + offsetY;
      scale *= delta;
      // Clamp scale
      if (scale < 0.2) { scale = 0.2; }
      if (scale > 5)   { scale = 5;   }
      updateTransform();
    }, { passive: false });
    // Drag to pan
    let isPanning = false;
    let startX = 0;
    let startY = 0;
    img.addEventListener('mousedown', (e) => {
      if (e.button !== 0) return; // only left button
      isPanning = true;
      startX = e.clientX - translateX;
      startY = e.clientY - translateY;
      img.style.cursor = 'grabbing';
      e.preventDefault();
    });
    document.addEventListener('mousemove', (e) => {
      if (!isPanning) return;
      translateX = e.clientX - startX;
      translateY = e.clientY - startY;
      updateTransform();
    });
    document.addEventListener('mouseup', () => {
      if (!isPanning) return;
      isPanning = false;
      img.style.cursor = 'zoom-in';
    });
    // Reset on double click
    img.addEventListener('dblclick', () => {
      scale = 1;
      translateX = 0;
      translateY = 0;
      updateTransform();
    });
    // Ensure transform origin is top-left for proper calculations
    img.style.transformOrigin = '0 0';
    link.href   = working;
    link.hidden = false;
    note.textContent = working;
    img.src = working;

    img.onerror = () => {
      const i = cands.indexOf(working);
      if (i >= 0 && i < cands.length - 1) {
        working = cands[i + 1];
        img.src  = working;
        link.href = working;
        note.textContent = "Trying: " + working;
        return;
      }
      note.textContent = "Image not found: " + (entry.image || entry.id);
      img.alt = note.textContent;
      img.src = "data:image/svg+xml;utf8," + encodeURIComponent(
        `<svg xmlns="http://www.w3.org/2000/svg" width="480" height="320">` +
        `<rect fill="#222" width="100%" height="100%"/>` +
        `<text x="50%" y="50%" fill="#888" font-family="sans-serif" ` +
        `font-size="14" text-anchor="middle">${note.textContent}</text></svg>`
      );
    };
  }

  /* ---------- prev / next navigation ---------- */
  function setupNav(entry) {
    const l   = list();
    const idx = l.findIndex(e => e.id === entry.id);
    const prev = idx > 0 ? l[idx - 1] : null;
    const next = idx >= 0 && idx < l.length - 1 ? l[idx + 1] : null;

    document.querySelectorAll('[data-nav="prev"]').forEach(a => {
      if (prev) { a.href = "?id=" + encodeURIComponent(prev.id); a.removeAttribute("aria-disabled"); }
      else      { a.href = "#"; a.setAttribute("aria-disabled", "true"); }
    });
    document.querySelectorAll('[data-nav="next"]').forEach(a => {
      if (next) { a.href = "?id=" + encodeURIComponent(next.id); a.removeAttribute("aria-disabled"); }
      else      { a.href = "#"; a.setAttribute("aria-disabled", "true"); }
    });

    document.addEventListener("keydown", e => {
      if (e.target.matches("input,textarea,select")) return;
      if (e.key === "ArrowLeft"  && prev) location.href = "?id=" + encodeURIComponent(prev.id);
      if (e.key === "ArrowRight" && next) location.href = "?id=" + encodeURIComponent(next.id);
    });
  }

  /* ---------- errors ---------- */
  function showError(out, err) {
    const safe = String(err && err.message ? err.message : err)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;");
    out.innerHTML =
      '<div class="render-error">' +
        "<h2>Could not load transcript</h2>" +
        '<pre>' + safe + '</pre>' +
        '<p>If you opened this with <code class="btn">file://</code>, either run ' +
        '<code class="btn">python3 build-transcriptions.py</code> to regenerate ' +
        '<code class="btn">transcriptions-content.js</code>, or start a local server:</p>' +
        '<pre>python3 -m http.server 8000</pre>' +
      "</div>";
  }

  /* ---------- main ---------- */
  async function render() {
    const out   = document.getElementById(OUTPUT_ID);
    const title = document.getElementById(TITLE_ID);
    if (!out) return;

    const id    = new URLSearchParams(location.search).get("id");
    const entry = getEntry(id);

    if (!entry) {
      showError(out, new Error("No transcription entries found in transcriptions-data.js."));
      return;
    }

    document.title = entry.id + " — Transcription Viewer";
    if (title) title.textContent = entry.id;

    setupNav(entry);
    setupImage(entry);   // parallel with the fetch

    try {
      const md = await getMarkdown(entry);
      if (typeof marked === "undefined") {
        throw new Error("marked.min.js did not load.  Keep it next to transcriptions.html.");
      }

      // Inject the GitHub button before the content
      const buttonHtml = `<div style="margin-bottom: 20px;"><a href="#" id="github-report-btn" class="btn" style="background:#2ea043; border-color:#2ea043; color:white; display:inline-flex; align-items:center; gap:6px;"><svg height="16" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" style="fill:white;"><path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.46-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path></svg> Report Issue on GitHub</a></div>`;

      out.innerHTML = buttonHtml + marked.parse(md);
      addHeaderIds(out);

      // Setup dynamic click handler for the GitHub button
      const githubBtn = document.getElementById("github-report-btn");
      if (githubBtn) {
        githubBtn.addEventListener("click", (e) => {
          e.preventDefault();
          const sel = window.getSelection();
          let selectionText = "";

          if (sel.rangeCount > 0 && out.contains(sel.anchorNode)) {
              selectionText = sel.toString().trim();
          }

          let body = `**Transcription ID:** ${entry.id}\n\n`;
          if (selectionText) {
              body += `**Original Text:**\n> ${selectionText.replace(/\n/g, '\n> ')}\n\n`;
          }
          body += `**Suggested Correction / Notes:**\n`;

          const url = `https://github.com/${GITHUB_REPO}/issues/new?title=${encodeURIComponent('Transcription Note: ' + entry.id)}&body=${encodeURIComponent(body)}`;
          window.open(url, '_blank');
        });
      }
    } catch (err) {
      console.error(err);
      showError(out, err);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      configureMarked();
      render().then(() => {
        const closeBtn = document.querySelector('.close-btn');
        if (closeBtn) {
          closeBtn.addEventListener('click', () => {
            const bar = closeBtn.parentElement;
            if (bar) bar.style.display = 'none';
          });
        }
      });
    });
  } else {
    configureMarked();
    render().then(() => {
      const closeBtn = document.querySelector('.close-btn');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          const bar = closeBtn.parentElement;
          if (bar) bar.style.display = 'none';
        });
      }
    });
  }
})();
