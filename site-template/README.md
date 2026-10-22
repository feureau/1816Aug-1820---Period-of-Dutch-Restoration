# Digital Archival Collection & Transcription Template

A modular, zero-dependency, dark-mode static website blueprint designed for historical document archives, manuscripts, and transcription projects.

---

## 🚀 Key Features

- **Side-by-side Transcription Viewer (`transcriptions.html`)**:
  - High-resolution manuscript scan on the left with **mouse-wheel zoom** and **drag-to-pan**.
  - Markdown-rendered transcription on the right.
- **Context-Aware GitHub Issue Reporting**:
  - Highlights selected text from the document and pre-fills a GitHub Issue template automatically with the `Transcription ID` and `Original Text`.
- **Multi-Format On-The-Fly Downloads**:
  - Download transcriptions instantly in `.md` (Markdown), `.html` (Webpage), or `.doc` (MS Word) format directly in the browser.
- **Continuous Reading Scroll (`full.html`)**:
  - Renders all transcriptions sequentially in a single scrollable document.
- **Anti-Caching Protection**:
  - Pre-configured `<meta>` cache-control headers prevent browsers from locking onto stale versions.

---

## 📁 Repository Structure

```
site-template/
├── index.html                 # Main portal / Home page
├── transcriptions.html        # Side-by-side manuscript & transcription viewer
├── full.html                  # Continuous scroll viewer for all documents
├── dictionary.html            # Keyword dictionary / Glossary reference page
│
├── marked.min.js              # Lightweight client-side Markdown parser
├── data.json                  # Index mapping image files to text files
│
├── sample_images/             # Folder containing manuscript scan images (.jpg/.png)
└── sample_transcriptions/     # Folder containing Markdown text transcriptions (.txt/.md)
```

---

## 🛠️ How to Customize for a New Project

### Step 1: Set your GitHub Repository
Open `transcriptions.html` and `full.html` in a text editor and update the top variable in the inline JavaScript:
```javascript
const GITHUB_REPO = "YourUsername/YourRepoName";
```

### Step 2: Add Your Manuscript Scans & Transcriptions
1. Drop your scanned manuscript images into `sample_images/` (e.g., `IMG_0001.jpg`).
2. Create matching `.txt` transcription files in `sample_transcriptions/` (e.g., `IMG_0001.txt`).

### Step 3: Register Items in `data.json`
Update `data.json` to map your image files to their text files:
```json
[
  { "id": "IMG_0001", "image": "sample_images/IMG_0001.jpg", "text": "sample_transcriptions/IMG_0001.txt" },
  { "id": "IMG_0002", "image": "sample_images/IMG_0002.jpg", "text": "sample_transcriptions/IMG_0002.txt" }
]
```

---

## 🌐 Deployment to GitHub Pages or Local Web Server

1. **Local Server:** Run `python -m http.server 8000` or use your `start_server.bat` script, then visit `http://localhost:8000/`.
2. **GitHub Pages:** Commit and push the folder contents to a public GitHub repository. Go to **Settings -> Pages**, select `main` branch, and save.