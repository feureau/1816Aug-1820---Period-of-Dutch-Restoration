# Master Transcription Template Specification (Peter Carey Archival Collections)

This document establishes the canonical, unified formatting standard for all manuscript transcriptions across the Peter Carey archival research collections—covering both the **1792–1809 Yogyakarta Residency Letters** and the **1816–1830 Dutch Restoration and Java War period**. Every transcription file must follow one of the three archetypes below depending on its document type, ensuring total uniformity in metadata, spatial classification, shorthand expansions, and cross-referencing.

---

## 1. General Rules & Conventions

1. **File Naming & Encoding:**
   * Files reside in the active transcription directory (e.g., `transcription/` or `Transcriptionv2/`) as `<IMAGE_BASENAME>.md` (or `.txt`).
   * Character encoding is strictly **UTF-8**.
2. **Shorthand & Acronym Expansions:**
   * All historical abbreviations, initials, and shorthand references must be expanded using square brackets on first occurrence:
     * *People:* `DP [Pangéran Dipanagara]`, `HB II [Sultan Hamengkubuwana II]`, `HB IV [Sultan Hamengkubuwana IV]`, `PB IV [Sunan Pakubuwana IV]`, `MB [Pangéran Mangkubumi]`, `PA [Pangéran Natakusuma / Paku Alam I]`, `MN I [Radèn Mas Said / Mangkunagara I]`, `MN II [Pangéran Prangwedana / Mangkunagara II]`, `Wat [Matthijs Waterloo]`, `Eng [Nicolaus Engelhard]`, `NvB [Major Huibert Gerard Nahuys van Burgst]`, `vIJ [Wouter Hendrik van IJsseldijk / Willem Herman van IJsseldijk]`.
     * *Offices & Places:* `Res [Resident]`, `Asst. Res [Assistant Resident]`, `Gov [Governor]`, `G.G. [Governor-General]`, `TR [Tegalrejo]`, `Solo [Surakarta]`, `Djogja / Yogya [Yogyakarta]`, `Bat. [Batavia]`, `Sem. [Semarang]`, `VL [Vorstenlanden]`.
     * *Currencies & Measures:* `Sp. D. [Spanish Dollars / Real de a Ocho]`, `RD [Rijksdaalders]`, `J.R. [Java Rupees]`, `Dfl [Dutch Florins / Guilders]`, `cacah [households]`, `jung [approx. 4 bau]`, `bau`.
     * *Prose:* `w/ [with]`, `w/o [without]`, `v. [against / versus]`, `Govt. [Government]`, `pop. [population]`.
3. **Date Standardization:**
   * In the `Metadata` section, dates must use ISO format: `YYYY-MM-DD` or range `YYYY-MM-DD to YYYY-MM-DD`. If month/day is uncertain, use `YYYY-MM` or `Circa YYYY`.
4. **Table Formatting:**
   * In Markdown tables, separate multiple lines within a single cell using `<br>`.
   * For nested sub-bullets or indented notes inside table cells, use `&nbsp;&nbsp;&nbsp;&nbsp;• `.
5. **Index Citations:**
   * All entities in the cross-reference section must cite the exact line number from [`39_Expanded_Keyword_Index.md`](file:///F:/GitHub/1816Aug-1820%20-%20Period%20of%20Dutch%20Restoration/39_Expanded_Keyword_Index.md). **Never edit or alter the index file.**
6. **Blank Leaves & Physical Card Dividers:**
   * Archival folder dividers (e.g., grey cards with tabs) and blank verso leaves must be transcribed under **Archetype 3**. Record their physical properties (paper stock, ruling, tape reinforcements, binding perforations, faint ink show-through, and visible file tabs) rather than leaving the file empty.

---

## 2. Archetype 1: Narrative Notes, Diaries & Letters

*Use for: Chronological diary entries, residency correspondence, meeting notes, intelligence memoranda, and narrative archival summaries.*

```markdown
# Transcription of IMG_XXXX.jpg

## Metadata
- **Image File:** `jpg/IMG_XXXX.jpg`
- **Source:** Peter Carey Collection / Archival Research Notes ([Archival Series, e.g., ANRI 'Djokjo Brieven' Bundel 40 / Leiden Univ BPL 616])
- **Date Range:** YYYY-MM-DD to YYYY-MM-DD
- **Key Events & Entities:**
  - **Key Events:** [Dense, scholarly paragraph summarizing the principal events, letters, political decisions, court assemblies, or military movements described on this page.]
  - **Key Entities (Persons):** [Comma-separated full standardized names with titles, e.g., Sultan Hamengkubuwana II, Sunan Pakubuwana IV, Matthijs Waterloo, Nicolaus Engelhard, Radèn Adipati Danureja II]
  - **Key Entities (Places):** [Comma-separated standardized place names with abbreviations, e.g., Yogyakarta (Djogja), Surakarta (Solo), Tegalrejo (TR), Batavia]
  - **Key Entities (Institutions / Terms):** [Comma-separated historical terms, offices, and cultural concepts, e.g., Garebeg Puasa, Patih office, Vorstenlanden demography, Salt trade monopoly]

---

### Header & Archival Classification

* **[Top Left / Series]:** `[Archival portfolio, bundle, or series notation, e.g., ANRI Djokjo Brieven Bundel 40 / B.P.L. 616]`
* **[Top Center (Ink Color / Notation)]:** `[Archival heading, date notation, or red ink marking, e.g., 1806 / DIARY of Chevallier]`
* **[Top Right / Folio]:** `[Sheet or folio numbering, e.g., Solo Bv. 23 / Folio 14 / AN 'Djokjo Brieven' no. 86]`
* **[Upper Subheading / Annotations]:** `[Subheadings, sender/recipient indications, or dates, e.g., Wat – Eng. | 28 Feb. 1806]`

---

### Main Text & Margin Notes

| Margin Notes | Main Text |
| :--- | :--- |
| **[Day / Date]<br>[Margin Heading]** | **[Sender] → [Recipient]**<br>[Date]<br>• [Transcribed body text with bracketed shorthand expansions]<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Indented sub-bullet details]<br>&nbsp;&nbsp;&nbsp;&nbsp;• [Additional details]<br><br>• [Subsequent entry or quote formatted with italics or blockquote: *"...quoted text..."*] |
| **[Next Date / Note]** | **[Next Subject / Entry Heading]**<br>• [Transcribed body text]<br>• [Transcribed body text] |

---

### Cross-Reference with `39_Expanded_Keyword_Index.md`

* **People:**
  * **[Full Name]** (`[Shorthand / Variant]`): Listed under *[Category Name]* (line [Line #]). [Brief biographical context, court office, or historical role].
* **Places & Institutions:**
  * **[Place Name]** (`[Shorthand / Variant]`): Listed under *[Category Name]* (line [Line #]). [Geographical relevance and administrative jurisdiction].
* **Terms:**
  * **[Historical Term / Concept]**: Listed under line [Line #]. [Precise definition and institutional role].
```

---

## 3. Archetype 2: Tabular Surveys, Land Registers & Fiscal Ledgers

*Use for: Village demarcations, appanage partitions, tollgate registers, cacah counts, tax farm auctions, crop ledgers (Book of Klèpu, Enquête d'Abo), and comparative textual collations (Band Coll. 308).*

```markdown
# Transcription of IMG_XXXX.jpg

## Metadata
- **Image File:** `jpg/IMG_XXXX.jpg`
- **Source:** Peter Carey Collection / Archival Research Notes (ANRI [Archival Series] No. [X]: *[Document Title]*, [Year])
- **Date Range:** YYYY-MM-DD to YYYY-MM-DD
- **Key Events & Entities:**
  - **Key Events:** [Dense, scholarly paragraph summarizing the survey scope, commissioners, boundary adjudications, fiscal metrics (cacah, jung, bau, rupiah), and sovereign court allocations.]
  - **Key Entities (Persons):** [Royal signatories, commissioners, patihs, appanage lords, and chief survey officials]
  - **Key Entities (Places):** [Provinces, river basins, districts, and surveyed villages / toll stations]
  - **Key Entities (Institutions / Terms):** [Survey titles, land units (cacah, jung, bau), tax offices (bèkèl, bandar), currency units (Sp. D., J.R.)]

---

### Header & Archival Classification

* **[Top Heading]:** `[Document or survey title, e.g., Lands in Pajang, Gunung Kidul / Master Register of Tollgates]`
* **[Archival Document Citation]:** `[Full archival series and date, e.g., ANRI Dj. Br. no. 41: Ingekomen stukken wegens opgenomen Vorsten Landen]`
* **[Commission Dispatch / Report]:** `[Commissioners, recipient, date, and location of submission]`
* **[Annotations / Ink Notations]:** `[Red ballpoint, pencil, or stamp annotations, e.g., 1770 Book of Klèpu]`

---

### Main Text & Margin Notes

| Margin Notes | Main Text |
| :--- | :--- |
| **Archival Context:<br>[Series Citation]<br>([Date])** | <b>[Survey Title / Registered Domain]:</b><br><br>[Introductory text explaining survey purpose, treaty context, and adjudicating court authorities (e.g., HB I, PB III, MN I)]. |

### Table Variation A: Cadastral, Village & Cacah Surveys

| Location / Village / Post | Headman / Collector [Bèkèl / Bandar] | Metric / Acreage [Households / Jung / Bau] | Appanage Lord / Sovereign [Court Owner] | Remarks & Archival Notes |
| :--- | :--- | :--- | :--- | :--- |
| **[Location Name]** | [Official Name] | [Count] cacahs ([Acreage]) | **[Ruler/Prince]** [Expanded Name] | [Boundary remarks, appointment notes, or treaty references] |
| **[Location Name]** | [Official Name] | [Count] cacahs ([Acreage]) | **[Ruler/Prince]** [Expanded Name] | [Boundary remarks, appointment notes, or treaty references] |

### Table Variation B: Comparative Textual & Bilingual Collations

| Folio / Date | Javanese Text | Dutch Text | Textual Analysis / Discrepancy |
| :--- | :--- | :--- | :--- |
| **[Folio / Ref]** | [Transcribed Javanese phrasing] | [Official Dutch record] | [Significance of textual alteration, translation omission, or political intent] |

---

### Cross-Reference with `39_Expanded_Keyword_Index.md`

* **People:**
  * **[Ruler / Appanage Lord]** (`[Abbr]`): Listed under *[Category]* (line [Line #]). [Reign dates, territorial entitlement, or treaty role].
* **Places & Institutions:**
  * **[Province / Village]**: Listed under line [Line #]. [Geographical location and historical importance].
* **Terms:**
  * **Cacah**: Listed under line 489. Peasant household unit used for measuring land productivity and taxation.
  * **Jung / Bau**: Listed under line 504. Javanese agrarian land measurement units.
  * **Bèkèl / Bandar**: Listed under line 485. Local tax-collector or tollgate leaseholder.
```

---

## 4. Archetype 3: Archival Covers, Spines, Dividers & Physical Calibration Artifacts

*Use for: Archive box covers, bundle labels, portfolio folders, container spines, internal cardboard divider sheets, and pre-digitization photographic calibration targets (e.g., X-Rite ColorChecker, grey balance cards).*

```markdown
# Transcription of IMG_XXXX.jpg

## Metadata
- **Image File:** `jpg/IMG_XXXX.jpg`
- **Source:** Peter Carey Collection / Archival Research Notes ([Dossier Container / Photographic Target / Binder Divider])
- **Date Range:** YYYY-MM-DD to YYYY-MM-DD
- **Key Events & Entities:**
  - **Key Events:** [Dense description of physical container, divider sheet, or calibration target marking the research dossier enclosing primary documents, letters, and notes for the designated chronological span.]
  - **Key Entities (Persons):** Professor Peter Carey (compiler/historian), [Principal historical figures documented within the container]
  - **Key Entities (Places):** [Principal court regions covered, e.g., Yogyakarta, Surakarta, Batavia]
  - **Key Entities (Institutions / Terms):** Archival bundle (*brievenbundel*), Physical preservation standards, ColorChecker calibration.

---

### Header & Archival Classification

* **[Physical Target / Object Description]:** `[Detailed physical description of binder, wrapping paper, tape, cardboard divider, or optical calibration target (e.g., X-Rite ColorChecker Passport Video, 2019 Edition)]`
* **[Affixed Label / Notation]:** `[Exact placement, typography, ink color, and transcription of handwritten or typed labels]`
* **[Visible Tabs / Secondary Markings]:** `[Chronological file tabs, marginalia, or serial stamps, e.g., 1801, 1806, kabinet]`

---

### Main Text & Margin Notes

| Margin Notes | Main Text |
| :--- | :--- |
| **Physical Object<br>[Description / Placement]** | <b>[Object Title / Target Name]:</b><br><br>[Physical description of panels, color patches, card surfaces, or typed label text]:<br><br>```text<br>[Verbatim label or target inscription]<br>```<br><br>*(Scope description summarizing the archival contents enclosed within this physical folder or technical calibration target).* |

---

### Cross-Reference with `39_Expanded_Keyword_Index.md`

* **People:**
  * **Prof. Peter Carey**: Modern historian, author of *The Power of Prophecy*, and compiler of the Yogyakarta Residency Letters archival dossiers.
  * **[Key Historical Figure]**: Listed under *[Category]* (line [Line #]). [Significance to this archival dossier].
* **Places & Institutions:**
  * **Yogyakarta**: Listed under lines 405, 468. Archival provenance of the residency papers.
* **Terms:**
  * **Archival Calibration Target**: Standardized technical reference card used to ensure chromatic fidelity, exposure calibration, and archival preservation standards in digitizing historical manuscripts.
  * **Residency Letters**: Official archival correspondence between the Yogyakarta Residency and central colonial authorities.
```

---

## 5. Standard Expansion Lexicon

### 5.1 Epoch 1: Yogyakarta Residency Letters (1792–1809)

| Abbreviation / Shorthand | Expanded Form | Standard Index Citation | Context / Historical Office |
| :--- | :--- | :--- | :--- |
| **HB I / Mangkubumi** | Sultan Mangkubumi (Hamengkubuwana I) | line 11 | First Sultan of Yogyakarta (1749–1792), founder of sultanate |
| **HB II / Sultan Sepuh** | Sultan Hamengkubuwana II | line 12 | Second Sultan of Yogyakarta (1792–1810, 1811–1812, 1826–1828) |
| **CP / P.A. Anom** | Crown Prince (Pangéran Adipati Anom / later HB III) | line 13 | Recognized heir apparent on 20 Aug 1792; later HB III |
| **PB III** | Sunan Pakubuwana III of Surakarta | line 10 | Signatory to Treaty of Giyanti (1755) and Book of Klèpu (1770) |
| **PB IV / Sunan Bagus** | Sunan Pakubuwana IV of Surakarta | line 18 | Ruler of Surakarta (1788–1820); chief rival to HB II |
| **MN I / Mas Said** | Radèn Mas Said (Mangkunagara I) | line 26 | Founder of the Mangkunagaran line (reigned 1757–1795) |
| **MN II / PWD / Prangwedana** | Pangéran Prangwedana (Mangkunagara II) | line 27 | Ruler of the Mangkunagaran (1796–1835); formed Mangkunagaran Legion |
| **Danurejo I** | Radèn Adipati Danureja I | line 183 | First Patih of Yogyakarta (in office 1755–1799) |
| **Danurejo II / Rèksanagara** | Radèn Adipati Danureja II | line 183 | Patih of Yogyakarta (in office 1799–1811; earlier R.T. Rèksanagara) |
| **Rongga III** | Radèn Rongga Prawiradirja III | line 178 | Bupati Wedana of Madiun (1796–1810) and brother-in-law to HB II |
| **Wat / Res. Waterloo** | Matthijs Waterloo | line 330 | Dutch Resident of Yogyakarta (1803–1808) |
| **vdBerg / Van den Berg** | Johannes Gerardus van den Berg | line 329 | Dutch Resident of Yogyakarta (1798–1803; 1803 MvO) |
| **vIJ / Van IJsseldijk** | Wouter Hendrik van IJsseldijk | line 327 | Dutch Resident of Yogyakarta (1786–1798; 1798 MvO) |
| **Rothenbühler** | Frederik Jacob Rothenbühler | line 328 | Dutch Resident of Yogyakarta (1799) |
| **Eng / Gov. Engelhard** | Nicolaus Engelhard | line 301 | Governor of Java's Northeast Coast (Semarang, 1801–1808) |
| **P. Engelhard** | Pieter Engelhard | line 331 | Dutch Resident of Yogyakarta (1808, 1810–1811) |
| **Daendels / G.G.** | Marshal Herman Willem Daendels | line 282 | Governor-General of the East Indies (1808–1811) |
| **Wiese / G.G.** | Albert Henricus Wiese | line 281 | Governor-General of the East Indies (1805–1808) |
| **Siberg / G.G.** | Johannes Siberg | line 280 | Governor-General of the East Indies (1801–1805) |
| **Overstraten / G.G.** | Pieter Gerardus van Overstraten | lines 279, 299 | Governor Northeast Coast (1791–1796); Governor-General (1796–1801) |
| **Alting / G.G.** | Willem Arnold Alting | line 278 | Governor-General of the East Indies (1780–1796) |
| **Moorrees / Morris** | Johannes Wilhelmus Moorrees | line 301 | Colonial secretary and minister for Solo/Yogya affairs |
| **Book of Klèpu** | Book of Klèpu (1770 / 1773) | line 489 | Boundary and *cacah* partition treaty between Yogya, Solo, and MN |
| **Sp. D.** | Spanish Dollars (*Real de a Ocho*) | line 106 | Primary silver specie of late 18th/early 19th c. Java |
| **RD / Ducaton** | Rijksdaalders / Silver Ducatons | line 656 | Dutch colonial trade coinage |
| **VL** | Vorstenlanden | line 468 | The Principalities of Central Java (Yogyakarta and Surakarta) |

---

### 5.2 Epoch 2: Dutch Restoration & Java War Period (1816–1830)

| Abbreviation / Shorthand | Expanded Form | Standard Index Citation | Context / Historical Office |
| :--- | :--- | :--- | :--- |
| **DP / Dip.** | Pangéran Dipanagara (Diponegoro) | line 10 | Leader of the Java War (1825–1830), eldest son of HB III |
| **HB III** | Sultan Hamengkubuwana III | line 13 | Third Sultan of Yogyakarta (reigned 1812–1814) |
| **HB IV** | Sultan Hamengkubuwana IV (Jarot) | line 14 | Fourth Sultan of Yogyakarta (reigned 1814–1822) |
| **HB V** | Sultan Hamengkubuwana V | line 15 | Fifth Sultan of Yogyakarta (minor child ruler, acceded 1822) |
| **PB IV** | Sunan Pakubuwana IV of Surakarta | line 18 | Ruler of Surakarta (reigned 1788–1820) |
| **PB V** | Sunan Pakubuwana V of Surakarta | line 19 | Ruler of Surakarta (reigned 1820–1823) |
| **PB VI** | Sunan Pakubuwana VI (Radèn Mas Saperdan) | line 20 | Ruler of Surakarta (reigned 1823–1830), exiled to Ambon |
| **PA / PA I** | Pangéran Natakusuma (Paku Alam I) | line 23 | Independent prince of the Pakualaman (reigned 1812–1829) |
| **MB / Mangkub.** | Pangéran Mangkubumi | line 63, line 80 | Son of HB I, uncle of Dipanagara (Yogya); brother of PB IV (Solo) |
| **Ratu Ibu** | Ratu Kencana (Ratu Ibu / Ratu Ageng) | line 32 | Mother of HB IV who allied with Danureja IV |
| **Ratu Ageng / Ratu Kedhaton** | Ratu Kedhaton (grandmother of HB IV) | line 30 | Widow of HB II, died 12 July 1820 |
| **Danurejo / DR IV / Patih** | Radèn Adipati Danureja IV | line 184 | Pro-Dutch Patih of Yogyakarta (in office 1813–1847) |
| **Sasradiningrat** | Radèn Adipati Sasradiningrat II | line 212 | Patih of Surakarta (in office 1812–1846) |
| **NvB / Res. Nahuys** | Major Huibert Gerard Nahuys van Burgst | line 341 | Resident of Yogyakarta (1816–1822) |
| **Smissaert / Res** | Anthonië Hendrik Smissaert | line 345 | Resident of Yogyakarta (1823–1825) |
| **Chevallier / ASST RES** | Petrus Franciscus Henricus Chevallier | line 346 | Assistant Resident of Yogyakarta (1823–1825) |
| **MacGillavry** | Hendrik Mauritz MacGillavry | line 346 | Acting Resident of Yogyakarta (1825) |
| **van IJ / vIJ** | Willem Herman van IJsseldijk | lines 314, 328 | Commissioner-General Extraordinary during the Restoration |
| **van der Capellen / G.G.** | G.A.G.P. Baron van der Capellen | line 287 | Governor-General of the Dutch East Indies (1816–1826) |
| **De Kock** | Hendrik Merkus de Kock | line 289 | Lieutenant Governor-General and Dutch military supreme commander |
| **Crawfurd** | John Crawfurd | line 313, 333 | British Resident of Yogyakarta (1811–1816) |
| **Johnson** | Major Jeremiah Martin Johnson | line 312 | British Resident of Surakarta (1813–1816) |
| **TR** | Tegalrejo | line 462 | Country estate of Pangéran Dipanagara |
| **J.R.** | Java Rupees | line 107 | Restoration-period currency |
| **Dfl** | Dutch Florins / Guilders | line 108 | Netherlands Indies guilders |
| **Bandar** | Tollgate / customs post keeper | lines 468, 663 | Tax-farmer operating customs barriers |
