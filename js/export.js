(function (global) {
    "use strict";

    const GITHUB_REPO = "feureau/1816Aug-1820---Period-of-Dutch-Restoration";
    const RAW_BASE = `https://raw.githubusercontent.com/${GITHUB_REPO}/main/`;
    const COLLECTION_TITLE = "1816 (August) – 1820: Yogyakarta Residency Letters & The Period of Dutch Restoration";

    function uint8ToBase64(bytes) {
        let binary = "";
        const CHUNK = 0x8000;
        for (let i = 0; i < bytes.length; i += CHUNK) {
            binary += String.fromCharCode.apply(null, bytes.subarray(i, i + CHUNK));
        }
        return btoa(binary);
    }

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
    }

    function triggerDownload(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 4000);
    }

    async function fetchPool(items, concurrency, worker, signal, onProgress) {
        let nextIdx = 0;
        let done = 0;
        const results = new Array(items.length);

        async function runWorker() {
            while (true) {
                if (signal && signal.aborted) {
                    throw new DOMException("Aborted", "AbortError");
                }
                const i = nextIdx++;
                if (i >= items.length) break;
                results[i] = await worker(items[i], i, signal);
                done++;
                if (onProgress) onProgress(done, items.length);
            }
        }

        const workers = [];
        for (let k = 0; k < Math.min(concurrency, items.length); k++) {
            workers.push(runWorker());
        }
        await Promise.all(workers);
        return results;
    }

    function mount(container, options) {
        if (!container) return;
        const getMdCache = (options && options.getMdCache) || (() => ({}));
        const manifestUrl = (options && options.manifestUrl) || "data.json";

        container.innerHTML = `
            <div style="background: var(--panel-alt, #2d2d2d); border: 1px solid var(--line, #333); border-radius: 6px; padding: 14px 18px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between;">
                <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
                    <strong style="color: #fff; font-size: 14px;">Collection Export:</strong>
                    <select id="exp-trans-select" aria-label="Export Transcriptions Only" style="background: #222; color: #e0e0e0; border: 1px solid #444; padding: 8px 12px; border-radius: 5px; font-size: 13px; cursor: pointer;">
                        <option value="">📄 Transcription Only…</option>
                        <option value="md">Markdown (.md)</option>
                        <option value="html">Standalone Web Page (.html)</option>
                        <option value="doc">Word Document (.doc)</option>
                        <option value="pdf">Printable PDF (.pdf)</option>
                        <option value="zip">ZIP Archive (.zip)</option>
                    </select>
                    <select id="exp-ms-select" aria-label="Export Manuscripts Only" style="background: #222; color: #e0e0e0; border: 1px solid #444; padding: 8px 12px; border-radius: 5px; font-size: 13px; cursor: pointer;">
                        <option value="">🖼️ Manuscript Only…</option>
                        <option value="zip">JPEG Scans ZIP (.zip)</option>
                        <option value="pdf">Manuscript PDF (.pdf)</option>
                        <option value="md">Scan Index (.md)</option>
                        <option value="html">Embedded HTML (.html)</option>
                        <option value="doc">Embedded Word (.doc)</option>
                    </select>
                </div>
                <div id="exp-status-wrap" style="display: none; align-items: center; gap: 10px; flex: 1; min-width: 220px;">
                    <progress id="exp-progress" value="0" max="100" style="flex: 1; height: 14px;"></progress>
                    <span id="exp-status-text" style="color: #ccc; font-size: 12px; white-space: nowrap;">Starting…</span>
                    <button id="exp-cancel-btn" type="button" style="background: #5c2b2b; color: #fff; border: 1px solid #8a4444; padding: 4px 10px; border-radius: 4px; font-size: 12px; cursor: pointer;">Cancel</button>
                </div>
            </div>
        `;

        const transSel = container.querySelector("#exp-trans-select");
        const msSel = container.querySelector("#exp-ms-select");
        const statusWrap = container.querySelector("#exp-status-wrap");
        const progBar = container.querySelector("#exp-progress");
        const statusText = container.querySelector("#exp-status-text");
        const cancelBtn = container.querySelector("#exp-cancel-btn");
        let currentAbort = null;

        function setBusy(busy, msg) {
            transSel.disabled = busy;
            msSel.disabled = busy;
            statusWrap.style.display = busy || msg ? "flex" : "none";
            cancelBtn.style.display = busy ? "inline-block" : "none";
            if (msg) statusText.textContent = msg;
        }

        function updateProgress(done, total, label) {
            progBar.max = total || 1;
            progBar.value = done;
            statusText.textContent = `${label} ${done}/${total}`;
        }

        cancelBtn.addEventListener("click", () => {
            if (currentAbort) currentAbort.abort();
        });

        async function loadManifest(signal) {
            const resp = await fetch(manifestUrl, { cache: "no-store", signal });
            if (!resp.ok) throw new Error(`HTTP ${resp.status} loading ${manifestUrl}`);
            return await resp.json();
        }

        async function fetchAllMarkdown(manifest, signal) {
            const cache = getMdCache();
            return await fetchPool(
                manifest,
                6,
                async (entry) => {
                    if (cache && cache[entry.id]) {
                        return { entry, md: cache[entry.id] };
                    }
                    const r = await fetch(entry.text, { cache: "no-store", signal });
                    if (!r.ok) throw new Error(`Failed ${entry.text}: HTTP ${r.status}`);
                    const md = await r.text();
                    return { entry, md };
                },
                signal,
                (done, total) => updateProgress(done, total, "Fetching transcripts")
            );
        }

        transSel.addEventListener("change", async () => {
            const fmt = transSel.value;
            transSel.value = "";
            if (!fmt) return;

            currentAbort = new AbortController();
            const signal = currentAbort.signal;
            setBusy(true, "Loading manifest…");

            try {
                const manifest = await loadManifest(signal);
                const docs = await fetchAllMarkdown(manifest, signal);

                if (fmt === "md") {
                    const combined = `# ${COLLECTION_TITLE}\n\n` + docs.map((d) => d.md.trim()).join("\n\n---\n\n") + "\n";
                    triggerDownload(new Blob([combined], { type: "text/markdown;charset=utf-8" }), "dutch_restoration_1816_1820_transcriptions.md");
                } else if (fmt === "html" || fmt === "doc" || fmt === "pdf") {
                    if (typeof global.marked === "undefined") throw new Error("marked.min.js not loaded");
                    global.marked.setOptions({ gfm: true, breaks: false, mangle: false });
                    const toc = docs.map((d) => `<li><a href="#${escapeHtml(d.entry.id)}">${escapeHtml(d.entry.id)}</a></li>`).join("");
                    const sections = docs.map((d, idx) => {
                        const brk = fmt === "pdf" && idx < docs.length - 1 ? ' style="break-after: page; page-break-after: always;"' : "";
                        return `<section id="${escapeHtml(d.entry.id)}"${brk}>${global.marked.parse(d.md)}</section>`;
                    }).join("\n<hr>\n");

                    const css = `
                        body { font-family: Georgia, serif; max-width: 960px; margin: 24px auto; padding: 0 20px; color: #111; line-height: 1.55; }
                        h1, h2, h3 { color: #1a2a3a; }
                        table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13px; }
                        th, td { border: 1px solid #999; padding: 6px 8px; vertical-align: top; text-align: left; }
                        th { background: #f0f0f0; }
                        code { background: #f4f4f4; padding: 1px 4px; border-radius: 3px; }
                        .toc { columns: 3; font-size: 13px; margin-bottom: 24px; }
                        @media print { .toc { page-break-after: always; } }
                    `;

                    if (fmt === "doc") {
                        const wordHtml = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40"><head><meta charset="utf-8"><title>${escapeHtml(COLLECTION_TITLE)}</title><style>${css}</style></head><body><h1>${escapeHtml(COLLECTION_TITLE)}</h1><h2>Table of Contents</h2><ul class="toc">${toc}</ul>${sections}</body></html>`;
                        triggerDownload(new Blob(["\ufeff", wordHtml], { type: "application/msword" }), "dutch_restoration_1816_1820_transcriptions.doc");
                    } else if (fmt === "html") {
                        const htmlDoc = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>${escapeHtml(COLLECTION_TITLE)}</title><style>${css}</style></head><body><h1>${escapeHtml(COLLECTION_TITLE)}</h1><h2>Table of Contents</h2><ul class="toc">${toc}</ul>${sections}</body></html>`;
                        triggerDownload(new Blob([htmlDoc], { type: "text/html;charset=utf-8" }), "dutch_restoration_1816_1820_transcriptions.html");
                    } else if (fmt === "pdf") {
                        setBusy(true, "Preparing print view…");
                        const printDoc = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>${escapeHtml(COLLECTION_TITLE)}</title><style>${css}</style></head><body><h1>${escapeHtml(COLLECTION_TITLE)}</h1>${sections}</body></html>`;
                        const iframe = document.createElement("iframe");
                        iframe.style.position = "fixed";
                        iframe.style.right = "0";
                        iframe.style.bottom = "0";
                        iframe.style.width = "0";
                        iframe.style.height = "0";
                        iframe.style.border = "0";
                        document.body.appendChild(iframe);
                        iframe.contentDocument.open();
                        iframe.contentDocument.write(printDoc);
                        iframe.contentDocument.close();
                        setTimeout(() => {
                            iframe.contentWindow.focus();
                            iframe.contentWindow.print();
                            setTimeout(() => iframe.remove(), 60000);
                        }, 300);
                    }
                } else if (fmt === "zip") {
                    if (typeof global.fflate === "undefined") throw new Error("js/vendor/fflate.min.js not loaded");
                    setBusy(true, "Compressing ZIP archive…");
                    const zipMap = {};
                    const enc = new TextEncoder();
                    zipMap["data.json"] = enc.encode(JSON.stringify(manifest, null, 2));
                    for (const d of docs) {
                        zipMap[d.entry.text] = enc.encode(d.md);
                    }
                    const zipped = global.fflate.zipSync(zipMap, { level: 6 });
                    triggerDownload(new Blob([zipped], { type: "application/zip" }), "dutch_restoration_1816_1820_transcriptions.zip");
                }
                setBusy(false, "Export ready.");
            } catch (err) {
                if (err.name === "AbortError") {
                    setBusy(false, "Export cancelled.");
                } else {
                    console.error(err);
                    setBusy(false, `Export failed: ${err.message}`);
                }
            } finally {
                currentAbort = null;
            }
        });

        msSel.addEventListener("change", async () => {
            const fmt = msSel.value;
            msSel.value = "";
            if (!fmt) return;

            currentAbort = new AbortController();
            const signal = currentAbort.signal;

            try {
                const manifest = await loadManifest(signal);
                if (fmt === "md") {
                    const mdLines = [
                        `# ${COLLECTION_TITLE} — Manuscript Scans`,
                        "",
                        `Total scans: ${manifest.length}`,
                        "",
                        "| Folio ID | Local Path | GitHub Raw URL |",
                        "| :--- | :--- | :--- |",
                        ...manifest.map((m) => `| ${m.id} | \`${m.image}\` | ${RAW_BASE}${m.image} |`),
                        "",
                    ].join("\n");
                    triggerDownload(new Blob([mdLines], { type: "text/markdown;charset=utf-8" }), "dutch_restoration_1816_1820_manuscripts_index.md");
                    setBusy(false, "Scan index ready.");
                    return;
                }

                if ((fmt === "html" || fmt === "doc") && manifest.length > 50) {
                    const ok = global.confirm(
                        `Embedding all ${manifest.length} full-resolution JPEG manuscript scans into a single ${fmt.toUpperCase()} file can exceed 600 MB and use substantial RAM. Continue?`
                    );
                    if (!ok) return;
                }

                setBusy(true, "Fetching JPEG scans…");
                const scans = await fetchPool(
                    manifest,
                    6,
                    async (entry) => {
                        const r = await fetch(entry.image, { cache: "no-store", signal });
                        if (!r.ok) throw new Error(`Failed ${entry.image}: HTTP ${r.status}`);
                        const buf = new Uint8Array(await r.arrayBuffer());
                        return { entry, buf };
                    },
                    signal,
                    (done, total) => updateProgress(done, total, "Fetching scans")
                );

                if (fmt === "zip") {
                    if (typeof global.fflate === "undefined") throw new Error("js/vendor/fflate.min.js not loaded");
                    setBusy(true, "Bundling JPEG scans (STORE mode)…");
                    const zipMap = {};
                    zipMap["data.json"] = new TextEncoder().encode(JSON.stringify(manifest, null, 2));
                    for (const s of scans) {
                        zipMap[s.entry.image] = s.buf;
                    }
                    const zipped = global.fflate.zipSync(zipMap, { level: 0 });
                    triggerDownload(new Blob([zipped], { type: "application/zip" }), "dutch_restoration_1816_1820_manuscripts.zip");
                } else if (fmt === "pdf") {
                    if (typeof global.PDFLib === "undefined") throw new Error("js/vendor/pdf-lib.min.js not loaded");
                    const pdfDoc = await global.PDFLib.PDFDocument.create();
                    for (let i = 0; i < scans.length; i++) {
                        if (signal.aborted) throw new DOMException("Aborted", "AbortError");
                        const s = scans[i];
                        let img;
                        try {
                            img = await pdfDoc.embedJpg(s.buf);
                        } catch (_) {
                            img = await pdfDoc.embedPng(s.buf);
                        }
                        const page = pdfDoc.addPage([img.width, img.height]);
                        page.drawImage(img, { x: 0, y: 0, width: img.width, height: img.height });
                        if (i % 10 === 0) {
                            updateProgress(i + 1, scans.length, "Building PDF");
                            await new Promise((r) => setTimeout(r, 0));
                        }
                    }
                    updateProgress(scans.length, scans.length, "Saving PDF");
                    const pdfBytes = await pdfDoc.save();
                    triggerDownload(new Blob([pdfBytes], { type: "application/pdf" }), "dutch_restoration_1816_1820_manuscripts.pdf");
                } else if (fmt === "html" || fmt === "doc") {
                    const blocks = [];
                    for (let i = 0; i < scans.length; i++) {
                        const s = scans[i];
                        const b64 = uint8ToBase64(s.buf);
                        blocks.push(`<div style="page-break-after: always; margin-bottom: 24px;"><h2>${escapeHtml(s.entry.id)}</h2><img src="data:image/jpeg;base64,${b64}" style="max-width: 100%; height: auto;"></div>`);
                        if (i % 10 === 0) {
                            updateProgress(i + 1, scans.length, "Encoding scans");
                            await new Promise((r) => setTimeout(r, 0));
                        }
                    }
                    if (fmt === "doc") {
                        const wordHtml = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40"><head><meta charset="utf-8"><title>${escapeHtml(COLLECTION_TITLE)}</title></head><body><h1>${escapeHtml(COLLECTION_TITLE)}</h1>${blocks.join("")}</body></html>`;
                        triggerDownload(new Blob(["\ufeff", wordHtml], { type: "application/msword" }), "dutch_restoration_1816_1820_manuscripts.doc");
                    } else {
                        const htmlDoc = `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>${escapeHtml(COLLECTION_TITLE)}</title></head><body style="background:#1a1a1a;color:#eee;font-family:sans-serif;max-width:1000px;margin:0 auto;padding:20px;"><h1>${escapeHtml(COLLECTION_TITLE)}</h1>${blocks.join("")}</body></html>`;
                        triggerDownload(new Blob([htmlDoc], { type: "text/html;charset=utf-8" }), "dutch_restoration_1816_1820_manuscripts.html");
                    }
                }
                setBusy(false, "Export ready.");
            } catch (err) {
                if (err.name === "AbortError") {
                    setBusy(false, "Export cancelled.");
                } else {
                    console.error(err);
                    setBusy(false, `Export failed: ${err.message}`);
                }
            } finally {
                currentAbort = null;
            }
        });
    }

    global.CollectionExporter = { mount };
})(window);
