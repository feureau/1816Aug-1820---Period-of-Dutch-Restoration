# Dutch Restoration Documentation (1816–1820)
## Yogyakarta Residency Letters & The Period of Dutch Restoration

This repository contains a comprehensive historical documentary collection, primary source transcriptions, archival summaries, and research dossiers assembled by **Professor Peter Carey** from primary European and Javanese archival repositories. 

The collection documents the pivotal transitional period in modern Javanese history between **August 1816 and December 1820**: the retrocession of Java from the British colonial administration (under Lieutenant-Governor Thomas Stamford Raffles and Resident John Crawfurd) back to the Kingdom of the Netherlands (*Commissarissen-Generaal* C.T. Elout, G.A.G.P. Baron van der Capellen, A.A. Buyskes, and Yogyakarta Resident Major Huibert Gerard Nahuys van Burgst).

---

## 📚 Key Historical Themes

1. **The British Retrocession & Dutch Restoration (August 1816)**
   - Formal power transfer from British Resident John Crawfurd to returning Dutch authorities.
   - Renegotiation and re-affirmation of the 1812 treaties.
   - Redeployment of British-Indian troops (Bengal & Light Volunteer Battalions) and court diplomacy with Sultan Hamengkubuwana IV and Susuhunan Pakubuwana IV.

2. **The Kyai Murmo (Kiai Murma) Affair & Jurisdictional Conflict (1816)**
   - Legal and political crisis surrounding the arrest of Kyai Murmo, inventorying of his gold, kris, and jewel treasures, and his flight to Kapundhung.
   - Jurisdictional disputes between Yogyakarta and Surakarta courts (*Pradoto*, *Surambi*, *Grobog*).

3. **Court Diplomacy, Exiled Rulers & Subsidies (1816–1817)**
   - Commissioner Willem Herman van IJsseldijk's special diplomatic mission to the Vorstenlanden.
   - Intelligence monitoring of exiled Sultan Hamengkubuwana II (Sultan Sepuh) in Ambon, Penang, and Batavia.
   - Subsidies and military arrangements for Paku Alam I and Pangeran Prangwedana (Mangkunagara II).

4. **Security, Armed Banditry & Social Unrest (1817–1818)**
   - Governance of Major Nahuys van Burgst (Yogyakarta) and Resident Van Haak (Surakarta).
   - Conflicts between civil residents and military commanders (Commandant Le Sueur).
   - Menace of armed banditry (*kecus*, *wong durjana*) and suppression of Pangeran Dipasana's millenarian uprising in Malang/Kediri.

5. **Socio-Economic Reforms, Land Leasing (*Landhuur*) & Public Health (1817–1820)**
   - Rapid expansion of European and Chinese land leases across Surakarta and Yogyakarta.
   - Toll-gate (*bandar*) tax schedules, village leasehold registers, and labor obligations.
   - Smallpox vaccination campaigns under Dr. Menke and health initiatives.
   - Governor-General Decree of 25 March 1819 (*Besluit* No. 5) regulating civil service training (*élèves*) and Javanese language instruction.
   - The *Enquête d'Abo* agricultural survey (31 December 1820).

---

## 📁 Repository Structure

```
.
├── 1816Aug-1820 - Period of Dutch Restoration.md  # Master text & archival compilation (alias document.md)
├── 39_Expanded_Keyword_Index.md                   # Expanded thematic keyword index
├── Correction_Dictionary_and_Keyword_Index.md     # 19th-century spelling & EYD mapping dictionary
│
├── index.html                                     # Main portal for the local web viewer
├── full.html                                      # Full document interactive web reader
├── transcriptions.html                            # Individual manuscript transcription viewer
├── dictionary.html                                # Keyword & correction dictionary web app
├── start_server.bat                               # Windows script to launch local HTTP server
│
├── Transcription/                                 # Primary manuscript text transcriptions (670+ files)
├── Transcriptionv2/ & Transcriptionv3/            # Iterative transcriptions & revised texts
├── transcriptions-data.js & transcriptions-content.js # JS payload for zero-CORS offline browsing
├── build-transcriptions.py                        # Script to rebuild embedded transcription JS data
├── extract.py                                     # Python script to extract names, places & terms
│
└── references/                                    # Historical chapters, timelines & appendices:
    ├── 01_Front_Matter.md - 05_Maps.md           # Front matter, table of contents, preface, maps
    ├── 06_Chapter_01_... - 17_Chapter_12_...     # Research chapters on Dipanagara & Javanese history
    └── 18_Appendix_01_... - 38_Index.md          # Royal family trees, landholdings, price indices, index
```

---

## 🚀 Quick Start (Local Web Viewer)

The repository includes a dark-themed local web application for reading documents, browsing manuscript transcriptions, and searching historical terms offline.

### Option 1: Using the Windows Batch Launcher
1. Double-click [`start_server.bat`](file:///F:/GitHub/1816Aug-1820%20-%20Period%20of%20Dutch%20Restoration/start_server.bat).
2. Open your browser to: **`http://localhost:8000`**

### Option 2: Command Line
Start a local Python HTTP server from the project root directory:
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000` in your web browser.

---

## 🌐 Web Application Features

- **Full Documentation Reader ([`full.html`](file:///F:/GitHub/1816Aug-1820%20-%20Period%20of%20Dutch%20Restoration/full.html)):**
  Rendered directly from [`1816Aug-1820 - Period of Dutch Restoration.md`](file:///F:/GitHub/1816Aug-1820%20-%20Period%20of%20Dutch%20Restoration/1816Aug-1820%20-%20Period%20of%20Dutch%20Restoration.md) with table of contents and full Markdown rendering.
- **Individual Transcriptions Browser ([`transcriptions.html`](file:///F:/GitHub/1816Aug-1820%20-%20Period%20of%20Dutch%20Restoration/transcriptions.html)):**
  Browse and search over 670 transcribed letters and official reports side-by-side with manuscript metadata.
- **Keyword & Correction Dictionary ([`dictionary.html`](file:///F:/GitHub/1816Aug-1820%20-%20Period%20of%20Dutch%20Restoration/dictionary.html)):**
  Search historical names, titles, places, 19th-century phonetic variants, and modern EYD standardized equivalents.

---

## 🛠️ Data Maintenance Scripts

- **Rebuild Transcriptions JS Data:**
  If you add or update text files in `Transcription/`, regenerate the embedded viewer script with:
  ```bash
  python build-transcriptions.py
  ```
- **Extract Historical Entities:**
  To extract proper nouns, places, and italicized terms into a markdown summary:
  ```bash
  python extract.py
  ```

---

## 🏛️ Archival Sources & Acknowledgments

The materials in this collection derive from primary European and Javanese archival repositories:
- **Arsip Nasional Republik Indonesia (ANRI):** *Djokjo Brieven* and *Solo Brieven* series (Bundels 40, 41, 44, 51A, 61, 63, and 79).
- **Universiteitsbibliotheek Leiden (Leiden University Library):** BPL 616 (*Nahuys van Burgst Papers*).
- **Nationaal Archief (The Hague):** De Kock, Van Alphen-Engelhard, and Baud Collections.
- **Koninklijk Instituut voor Taal-, Land- en Volkenkunde (KITLV)**
- Published documentary studies by **P.H. van der Kemp** and **Dr. Frederik de Haan**.
- Research assembly and editing by **Professor Peter Carey**.

---

## 📜 License

See [`LICENSE`](file:///F:/GitHub/1816Aug-1820%20-%20Period%20of%20Dutch%20Restoration/LICENSE) for licensing details regarding the compilation and materials in this repository.
