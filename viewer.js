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
      out.innerHTML = marked.parse(md);
      addHeaderIds(out);
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
