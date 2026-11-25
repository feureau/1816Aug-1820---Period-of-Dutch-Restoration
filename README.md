# 1816 (August) – 1820: Yogyakarta Residency Letters & Period of Dutch Restoration

Archival transcription corpus, research database, and static digital portal covering Professor Peter Carey's archival research notes and primary dispatches from the **1816–1820 Dutch Restoration** in South-Central Java (Yogyakarta and Surakarta).

---

## Corpus Overview

- **Total Folios:** **336** synchronized scans (`jpg/IMG_1218.jpg`–`IMG_1561.jpg`) and Markdown transcriptions (`Transcriptionv2/IMG_1218.md`–`IMG_1561.md`).
  *(Note: `IMG_1460` and `IMG_1494` were skipped in original archival photography; zero gaps exist in physical records.)*
- **Manifest Index:** [`data.json`](data.json) (and synchronized compatibility copy [`transcriptions-data.json`](transcriptions-data.json)) using POSIX `/` paths.
- **Reference Glossary:** [`39_Expanded_Keyword_Index.md`](39_Expanded_Keyword_Index.md) (**strictly read-only ground truth**, indexed into `scripts/entity_database.json` and [`dictionary.html`](dictionary.html)).

---

## Launching Locally (Windows / CLI)

Because modern browsers block `fetch("data.json")` over `file://` CORS restrictions, launch the built-in local HTTP server:

- **One-click Windows launcher:** Double-click [`launch_server.bat`](launch_server.bat) (or [`start_server.bat`](start_server.bat)).
- **Command line:**
  ```powershell
  python scripts/serve.py
  ```
  Options:
  - `python scripts/serve.py 8080` — serve on a specific port (auto-selects a free port from `8000` by default)
  - `python scripts/serve.py 8080 --no-browser` — start headless without opening a browser tab
- **GitHub Pages:** Ready to serve statically as-is (`.nojekyll` disables Jekyll processing).

---

## Portal Pages & Features

1. **[`index.html`](index.html)** — Main landing portal with collection summary, GitHub repository link, whole-collection exporter (`js/export.js`), and navigation cards.
2. **[`transcriptions.html`](transcriptions.html)** — Side-by-side manuscript image viewer (cursor-anchored mouse-wheel zoom `0.2x`–`5x`, drag panning) and rendered GFM Markdown panel with folio jump, keyboard `ArrowLeft`/`ArrowRight` navigation, per-folio `.md`/`.html`/`.doc` downloads, and selection-aware GitHub Issue errata reporting.
3. **[`full.html`](full.html)** — Streaming full-corpus reader rendering all 336 folios sequentially with progress indicator, smooth-scroll jump selector, floating Back-to-Top button, and whole-collection `.md`/`.html`/`.doc`/`.pdf`/`.zip` exports (offline vendored `marked.min.js`, `js/vendor/fflate.min.js`, `js/vendor/pdf-lib.min.js`).
4. **[`dictionary.html`](dictionary.html)** — Searchable historical reference dictionary (650 entries across 12 categories) generated from `39_Expanded_Keyword_Index.md`.

---

## Maintenance & Verification Scripts (`scripts/`)

| Script | Purpose |
| :--- | :--- |
| `scripts/scan_orientations.py` | OpenCV Canny + Hough pre-flight orientation check across all 336 JPEGs |
| `scripts/build_entity_index.py` | Parses read-only `39_Expanded_Keyword_Index.md` into `scripts/entity_database.json` |
| `scripts/audit_verbatim_fidelity.py` | Audits `Transcriptionv2/*.md` against `older_transcription_versions/backup_Transcriptionv2_pre_pilot/*.txt` |
| `scripts/restore_verbatim_from_backup.py` | Restores verbatim primary/note wording on paraphrased narrative folios |
| `scripts/normalize_archetypes.py` | Enforces the strict 3-Archetype Markdown specification and verified `#L` index citations |
| `scripts/fix_table_pipes.py` | Escapes stray inner pipes `\|` inside Markdown table prose cells |
| `scripts/format_all_transcriptions_markdown.py` | Normalizes CommonMark/GFM spacing, metadata line breaks, and UTF-8 (no BOM) |
| `scripts/validate_transcriptions.py` | Full corpus validator checking concordance, structure, HTML balance, GFM columns, and index citations |
| `scripts/build_dictionary_html.py` | Regenerates `dictionary.html` from `39_Expanded_Keyword_Index.md` |
| `scripts/serve.py` | Zero-dependency local HTTP server with `Cache-Control: no-store` |
