import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRANS_DIR = os.path.join(REPO_ROOT, "Transcriptionv2")
ENTITY_DB_PATH = os.path.join(os.path.dirname(__file__), "entity_database.json")
INDEX_FILE_URL = "file:///f:/GitHub/1816Aug-1820%20-%20Period%20of%20Dutch%20Restoration/39_Expanded_Keyword_Index.md"

with open(ENTITY_DB_PATH, "r", encoding="utf-8") as f:
    ENTITY_DB = json.load(f)

BY_LINE = {e["line"]: e for e in ENTITY_DB}

# Manual overrides for known tricky shorthand/label lookups
TERM_LINE_OVERRIDES = {
    "yogyakarta": 392,
    "yogya": 392,
    "djokja": 392,
    "djocja": 392,
    "surakarta": 393,
    "solo": 393,
    "sala": 393,
    "semarang": 395,
    "batavia": 391,
    "java": 391,
    "salis": 345,
    "de salis": 345,
    "danureja iv": 184,
    "sasradiningrat": 212,
    "nahuys": 341,
    "van ijsseldijk": 314,
    "capellen": 287,
    "van der capellen": 287,
    "elout": 289,
    "daendels": 282,
    "raffles": 283,
    "crawfurd": 333,
    "winter": 385,
    "carey": 385,
    "peter carey": 385,
    "deventer": 385,
    "van deventer": 385,
    "william i": 385,
    "pakubuwana iv": 18,
    "pakubuwana v": 19,
    "pakubuwana vi": 20,
    "pakubuwana vii": 21,
    "hamengkubuwana i": 11,
    "hamengkubuwana ii": 12,
    "hamengkubuwana iii": 13,
    "hamengkubuwana iv": 14,
    "hamengkubuwana v": 15,
    "dipanagara": 10,
    "paku alam i": 23,
    "pakualam i": 23,
    "natakusuma": 23,
    "paku alam ii": 24,
    "mangkunagara ii": 27,
    "prangwedana": 27,
    "buminata": 79,
    "mangkubumi": 63,
    "ratu kedhaton": 30,
    "ratu kencana": 32,
    "ratu ageng": 30,
    "tan jin sing": 193,
    "secadiningrat": 193,
    "jagakarya": 203,
    "iman sampurna": 132,
    "murma": 131,
    "kedhu": 468,
    "kedu": 468,
    "kediri": 468,
    "sukawati": 468,
    "klathèn": 423,
    "klaten": 423,
    "imagiri": 427,
    "pacitan": 424,
    "magelang": 411,
    "banyumas": 419,
    "madiun": 416,
    "gamping": 420,
    "bedhaya": 450,
    "tembayat": 436,
    "kraton": 518,
    "patih": 541,
    "payung": 542,
    "ratu": 554,
    "cacah": 489,
    "jung": 504,
    "bau": 504,
    "bekel": 485,
    "bèkèl": 485,
    "bandar": 482,
    "demang": 491,
    "pengulu": 545,
    "santri": 555,
    "tarekat": 562,
    "jihad": 503,
    "perang sabil": 503,
    "pusaka": 553,
    "garebeg": 497,
    "sawah": 556,
    "pajeg": 532,
    "land-rent": 532,
    "spanish dollar": 651,
    "sp. d": 651,
    "java rupee": 676,
    "florin": 657,
    "guilder": 657,
    "opium": 662,
    "tollgate": 663,
    "pasar": 664,
    "babad": 597,
    "fort vredenburg": 647,
    "fort rustenburg": 647,
    "mangkunagaran legion": 636,
    "sepoy": 638,
    "bengal": 638,
    "bataviasche courant": 660,
    "residency": 572,
    "diplomatic": 572,
    "calibration": 572,
    "dutch restoration": 287,
}


def strip_accents(s: str) -> str:
    reps = str.maketrans("éèêëäàâöòôïìîüùûñÉÈÊËÄÀÂÖÒÔÏÌÎÜÙÛ", "eeeeaaaoooiiiuuunEEEEAAAOOOIIIUUU")
    return s.translate(reps)


def classify_entry(entry: dict) -> str:
    cat = (entry.get("top_category", "") + " " + entry.get("sub_category", "")).lower()
    if any(k in cat for k in ["royalty", "religious", "officials", "commanders", "colonial officials", "figures"]):
        return "People"
    if any(k in cat for k in ["places", "regiments", "units", "ships", "forts"]):
        return "Places & Institutions"
    return "Terms"


def find_best_entity_for_line_or_label(label: str, line_hint: int | None) -> dict | None:
    norm_lbl = strip_accents(label).lower()
    # Check overrides first if line_hint is missing or clearly mismatched
    sig_words = [w for w in re.findall(r"[a-z]{4,}", norm_lbl) if w not in {
        "sultan", "sunan", "raden", "pangeran", "major", "resident", "acting",
        "historical", "later", "colonial", "officials", "concept", "terms",
        "institutional", "category", "listed", "under", "prince", "king",
        "baron", "count", "knight", "governor", "general", "javanese", "dutch",
        "british", "royal", "court", "area", "district", "province", "place",
    }]

    if line_hint and line_hint in BY_LINE:
        ent = BY_LINE[line_hint]
        ent_text = strip_accents(ent["raw"]).lower()
        if any(w in ent_text for w in sig_words):
            return ent
        # Even if words didn't match, check override on label

    for k, target_ln in TERM_LINE_OVERRIDES.items():
        if k in norm_lbl and target_ln in BY_LINE:
            return BY_LINE[target_ln]

    # Search ENTITY_DB for best match on sig_words
    best = None
    best_score = 0
    for ent in ENTITY_DB:
        t_low = strip_accents(ent["term"]).lower()
        d_low = strip_accents(ent["desc"]).lower()
        score = sum(3 for w in sig_words if w in t_low) + sum(1 for w in sig_words if w in d_low)
        if score > best_score:
            best_score = score
            best = ent
    if best and best_score >= 3:
        return best

    if line_hint and line_hint in BY_LINE:
        return BY_LINE[line_hint]
    return None


def parse_sections(text: str, fname: str) -> dict:
    """Split markdown file into logical sections by top headings."""
    lines = text.splitlines()
    title = f"# Transcription of {fname[:-3]}.jpg"
    sections = []
    cur_h = None
    cur_lines = []

    for ln in lines:
        if ln.startswith("# Transcription"):
            title = f"# Transcription of {fname[:-3]}.jpg"
            continue
        if re.match(r"^#{2,3}\s+", ln):
            if cur_h is not None or any(x.strip() for x in cur_lines):
                sections.append((cur_h or "PREAMBLE", "\n".join(cur_lines).strip()))
            cur_h = ln.strip()
            cur_lines = []
        else:
            cur_lines.append(ln)
    if cur_h is not None or any(x.strip() for x in cur_lines):
        sections.append((cur_h or "PREAMBLE", "\n".join(cur_lines).strip()))

    return {"title": title, "sections": sections}


def normalize_iso_date(raw: str) -> str:
    s = raw.strip()
    if re.match(r"^(\d{4}(-\d{2}){0,2}(\s+to\s+\d{4}(-\d{2}){0,2})?|Circa\s+\d{4})$", s):
        return s
    # Extract YYYY-MM-DD / YYYY-MM / YYYY spans if embedded with parenthetical notes
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", s)
    if len(dates) >= 2:
        return f"{dates[0]} to {dates[-1]}"
    if len(dates) == 1:
        return dates[0]
    ym = re.findall(r"\d{4}-\d{2}", s)
    if len(ym) >= 2:
        return f"{ym[0]} to {ym[-1]}"
    if len(ym) == 1:
        return ym[0]
    yrs = re.findall(r"\b(1[789]\d{2})\b", s)
    if len(yrs) >= 2 and yrs[0] != yrs[-1]:
        return f"{yrs[0]} to {yrs[-1]}"
    if yrs:
        return f"Circa {yrs[0]}"
    return "Circa 1816 to 1820"


def build_metadata(meta_body: str, fname: str, commentary_extra: str) -> tuple[str, dict]:
    """Ensure all 9 required Metadata bullets are cleanly present."""
    img_name = fname[:-3] + ".jpg"
    fields = {
        "Image File": f"`jpg/{img_name}`",
        "Source": "Peter Carey Collection / Archival Research Notes",
        "Date Range": "Circa 1816 to 1820",
        "Key Events": "",
        "Persons": "",
        "Places": "",
        "Terms": "",
    }
    doc_type = ""
    for ln in meta_body.splitlines():
        s = ln.strip()
        if s.startswith("- **Image File:**"):
            fields["Image File"] = f"`jpg/{img_name}`"
        elif s.startswith("- **Source:**"):
            fields["Source"] = s.split("**Source:**", 1)[1].strip()
        elif s.startswith("- **Date Range:**"):
            fields["Date Range"] = normalize_iso_date(s.split("**Date Range:**", 1)[1].strip())
        elif s.startswith("- **Document Type:**"):
            doc_type = s.split("**Document Type:**", 1)[1].strip()
        elif s.startswith("- **Key Events:**"):
            fields["Key Events"] = s.split("**Key Events:**", 1)[1].strip()
        elif s.startswith("- **Key Entities (Persons):**"):
            fields["Persons"] = s.split("**Key Entities (Persons):**", 1)[1].strip()
        elif s.startswith("- **Key Entities (Places):**"):
            fields["Places"] = s.split("**Key Entities (Places):**", 1)[1].strip()
        elif s.startswith("- **Key Entities (Institutions / Terms):**"):
            fields["Terms"] = s.split("**Key Entities (Institutions / Terms):**", 1)[1].strip()
        elif s.startswith("- **Key Entities (Terms):**"):
            fields["Terms"] = s.split("**Key Entities (Terms):**", 1)[1].strip()

    if doc_type and doc_type not in fields["Source"]:
        fields["Source"] = f"{fields['Source']} ({doc_type})"

    if not fields["Key Events"]:
        if commentary_extra:
            first_para = commentary_extra.split("\n\n")[0].replace("\n", " ").strip()
            fields["Key Events"] = first_para[:600]
        else:
            fields["Key Events"] = f"Archival manuscript leaf and research record from {fields['Source']}."

    if not fields["Persons"]:
        fields["Persons"] = "Professor Peter Carey (compiler/historian)"
    if not fields["Places"]:
        fields["Places"] = "Yogyakarta (Djogja), Surakarta (Solo), Java"
    if not fields["Terms"]:
        fields["Terms"] = "Dutch Restoration archives, Physical archival leaf"

    out = [
        f"- **Image File:** {fields['Image File']}  ",
        f"- **Source:** {fields['Source']}  ",
        f"- **Date Range:** {fields['Date Range']}  ",
        "- **Key Events & Entities:**  ",
        f"  - **Key Events:** {fields['Key Events']}  ",
        f"  - **Key Entities (Persons):** {fields['Persons']}  ",
        f"  - **Key Entities (Places):** {fields['Places']}  ",
        f"  - **Key Entities (Institutions / Terms):** {fields['Terms']}",
    ]
    return "\n".join(out), fields


def clean_inline(text: str) -> str:
    text = text.replace(r"$\therefore$", "∴").replace("$∴$", "∴").replace(r"\therefore", "∴")
    return text


def build_classification(class_blocks: list[tuple[str, str]], meta_fields: dict, is_arch3: bool) -> str:
    """Produce canonical ### Header & Archival Classification block."""
    collected_bullets = []
    for hdr, body in class_blocks:
        b = body.strip()
        if not b or b == "---":
            continue
        for ln in b.splitlines():
            s = ln.strip()
            if not s or s == "---":
                continue
            if s.startswith("*") or s.startswith("-"):
                # Normalize leading marker to *
                collected_bullets.append("* " + re.sub(r"^[\*\-]\s+", "", s))
            else:
                collected_bullets.append(f"* **[Archival Note]:** `{s.strip('`')}`")

    if collected_bullets:
        # Remove duplicates while preserving order
        seen = set()
        dedup = []
        for b in collected_bullets[:8]:
            if b not in seen:
                seen.add(b)
                dedup.append(b)
        return "\n".join(dedup)

    if is_arch3:
        return "\n".join([
            f"* **[Physical Target / Object Description]:** `{meta_fields['Source']}`",
            f"* **[Affixed Label / Notation]:** `Physical archival card, divider, cover, or verso leaf ({meta_fields['Date Range']})`",
            f"* **[Visible Tabs / Secondary Markings]:** `See spatial diplomatic transcription below`",
        ])

    return "\n".join([
        f"* **[Top Left / Series]:** `{meta_fields['Source']}`",
        f"* **[Top Center / Date Scope]:** `{meta_fields['Date Range']}`",
        f"* **[Top Right / Folio]:** `{meta_fields['Image File'].strip('`')}`",
        "* **[Upper Subheading / Annotations]:** `See diplomatic table below`",
    ])


def build_cross_references(xref_body: str, meta_fields: dict) -> str:
    """Normalize Cross-Reference with 39_Expanded_Keyword_Index.md into People / Places & Institutions / Terms with verified lines."""
    buckets = {"People": [], "Places & Institutions": [], "Terms": []}
    seen_lines = {"People": set(), "Places & Institutions": set(), "Terms": set()}

    for ln in xref_body.splitlines():
        s = ln.strip()
        if not s or s == "---":
            continue
        if re.match(r"^[\*\-]\s+\*\*(?:People|Places & Institutions|Terms):\*\*\s*$", s):
            continue
        if not (s.startswith("*") or s.startswith("-")):
            continue

        # Strip any prior markdown links/formatting from line before parsing
        clean_s = re.sub(r"\[([^\]]*)\]\([^\)]+\)", r"\1", s)
        # Parse label, line number, description
        m_link = re.search(r"\(?\[line\s+(\d+)\]\([^\)]*#L(\d+)\)\)?", s)
        m_filelink = re.search(r"\[\`?([^\]]*?)\`?\]\(file:///[^\)]*39_Expanded_Keyword_Index\.md#L(\d+)\)", s)
        m_plain = re.search(r"\(line\s+(\d+)\)", s)

        line_hint = None
        if m_link:
            line_hint = int(m_link.group(2))
        elif m_filelink and "39_Expanded_Keyword_Index" not in m_filelink.group(1):
            line_hint = int(m_filelink.group(2))
        elif m_plain:
            line_hint = int(m_plain.group(1))
        else:
            m_any = re.search(r"#L(\d+)", s)
            if m_any:
                line_hint = int(m_any.group(1))

        body_no_bullet = re.sub(r"^[\*\-]\s+", "", clean_s)
        body_no_bullet = re.sub(r"^Line\s+\d+:\s*", "", body_no_bullet)
        # Remove duplicated parenthesized markdown remnants
        body_no_bullet = re.sub(r"\(`[^`]*Line\s+\d+[^`]*`\)", "", body_no_bullet)

        label_part = body_no_bullet
        desc_part = ""
        m_colon = re.match(r"^(?:\*\*|\`)?([^:\[\]\(\n]+?)(?:\*\*|\`)?(?:\s*\(`[^`]+`\))?\s*:\s*(.*)$", body_no_bullet)
        if m_colon:
            label_part = m_colon.group(1).strip(" *`")
            desc_part = m_colon.group(2).strip()
            desc_part = re.sub(r"^Listed under.*?(?:\)\.?|Line\s+\d+\.?)\s*", "", desc_part).strip()
            desc_part = re.sub(r"\[?Line\s+\d+\]?", "", desc_part).strip(" .")

        ent = find_best_entity_for_line_or_label(label_part, line_hint)
        if ent:
            bname = classify_entry(ent)
            ln_num = ent["line"]
            if ln_num in seen_lines[bname]:
                continue
            seen_lines[bname].add(ln_num)
            cat_name = ent["sub_category"] or ent["top_category"] or "Keyword Index"
            raw_ent_desc = ent["desc"] if len(ent["desc"]) < 140 else ""
            short_desc = desc_part if desc_part and "Listed under" not in desc_part else (raw_ent_desc or cat_name)
            disp_name = ent["term"] if len(ent["term"]) <= 75 else (label_part or cat_name)
            variant_note = ""
            if label_part and strip_accents(label_part).lower() not in strip_accents(disp_name).lower() and len(label_part) <= 45:
                variant_note = f" (`{label_part}`)"
            buckets[bname].append(
                f"  * **{disp_name}**{variant_note}: Listed under *{cat_name}* ([line {ln_num}]({INDEX_FILE_URL}#L{ln_num})). {short_desc}"
            )

    # Guarantee non-empty People / Places & Institutions / Terms by seeding from Metadata Key Entities if any bucket is empty
    seed_map = [
        ("People", meta_fields["Persons"], [287, 341, 14, 18, 385]),
        ("Places & Institutions", meta_fields["Places"], [392, 393, 391]),
        ("Terms", meta_fields["Terms"], [518, 572, 663]),
    ]
    for bname, raw_text, fallbacks in seed_map:
        if not buckets[bname]:
            for token in re.split(r"[,;]", raw_text):
                tok = token.strip()
                if len(tok) < 3:
                    continue
                ent = find_best_entity_for_line_or_label(tok, None)
                if ent and ent["line"] not in seen_lines[bname]:
                    # Accept into this bucket (or use exact bucket)
                    cat_name = ent["sub_category"] or ent["top_category"] or "Keyword Index"
                    seen_lines[bname].add(ent["line"])
                    buckets[bname].append(
                        f"  * **{ent['term']}**: Listed under *{cat_name}* ([line {ent['line']}]({INDEX_FILE_URL}#L{ent['line']})). {ent['desc'] or cat_name}"
                    )
                    break
        if not buckets[bname]:
            for fb in fallbacks:
                if fb in BY_LINE and fb not in seen_lines[bname]:
                    ent = BY_LINE[fb]
                    cat_name = ent["sub_category"] or ent["top_category"] or "Keyword Index"
                    seen_lines[bname].add(fb)
                    buckets[bname].append(
                        f"  * **{ent['term']}**: Listed under *{cat_name}* ([line {fb}]({INDEX_FILE_URL}#L{fb})). {ent['desc'] or cat_name}"
                    )
                    break

    out = []
    for bname in ("People", "Places & Institutions", "Terms"):
        out.append(f"* **{bname}:**")
        out.extend(buckets[bname])
    return "\n".join(out)


def process_file(fname: str) -> bool:
    path = os.path.join(TRANS_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        orig = f.read()

    parsed = parse_sections(orig, fname)
    title = parsed["title"]
    secs = parsed["sections"]

    meta_body = ""
    class_blocks = []
    main_blocks = []
    commentary_blocks = []
    xref_parts = []

    is_arch3 = False
    for hdr, body in secs:
        h_low = hdr.lower()
        if hdr == "PREAMBLE":
            continue
        if h_low.startswith("## metadata"):
            meta_body = body
        elif any(k in h_low for k in [
            "header & archival", "archival classification", "visual layout & columnar",
            "physical description"
        ]):
            if "physical description" in h_low:
                is_arch3 = True
            class_blocks.append((hdr, body))
        elif any(k in h_low for k in [
            "main text", "transcription:", "spatial transcription", "visible inscriptions",
            "diplomatic transcription", "official attestation", "footnotes & annotations",
            "verbatim marginal", "center leaf inscription", "divider tab", "upper right backing",
            "inscription on affixed", "1. narrative", "2. statistical", "2. quantitative",
            "3. inventory", "4. official statutory", "1. horse load", "2. coolie", "3. livestock",
            "master register", "master land rent", "margin notes"
        ]):
            # Skip pure stub sub-headers that only say "see below"
            if h_low == "### margin notes" and "below" in body.lower():
                continue
            main_blocks.append((hdr, body))
        elif any(k in h_low for k in [
            "cross-reference", "cross-reference & lineage", "historical cross-references"
        ]):
            if body.strip():
                xref_parts.append(body)
        elif any(k in h_low for k in [
            "contextual", "archival context", "critical apparatus", "detailed notes",
            "detailed physical", "physical context"
        ]):
            commentary_blocks.append(body)
        else:
            # Preserve any unknown content sub-section inside main_blocks cleanly
            main_blocks.append((hdr, body))

    if any(k in fname for k in ["IMG_1218", "IMG_1219", "IMG_1240", "IMG_1244", "IMG_1248", "IMG_1252", "IMG_1285", "IMG_1287", "IMG_1288", "IMG_1299", "IMG_1304", "IMG_1305", "IMG_1306", "IMG_1311", "IMG_1359", "IMG_1361", "IMG_1372", "IMG_1421", "IMG_1500", "IMG_1505", "IMG_1506", "IMG_1539", "IMG_1552", "IMG_1556"]):
        is_arch3 = True

    commentary_extra = "\n\n".join(b for b in commentary_blocks if b.strip())
    norm_meta, meta_fields = build_metadata(meta_body, fname, commentary_extra)
    norm_class = build_classification(class_blocks, meta_fields, is_arch3)

    # Assemble clean Main Text & Margin Notes body (no stray ## headings, convert ### Main Text subheadings carefully)
    main_out_parts = []
    has_margin_table = False
    for hdr, body in main_blocks:
        b = clean_inline(body.strip()).rstrip("-").strip()
        if not b:
            continue
        if "| Margin Notes | Main Text |" in b:
            has_margin_table = True
        # Promote subheadings that contain tables or inscriptions cleanly
        if hdr in (
            "## Transcription: Spatial Layout & Textual Content",
            "## Spatial Transcription",
            "## Transcription: Main Text & Margin Notes",
            "## Transcription: Spatial Layout & Tabular Register",
            "## Transcription: Diplomatic Text & Inscriptions",
            "## Transcription: Spatial Layout & Statistical Register",
            "### Main Text & Margin Notes",
            "### Main Text",
            "### Main Text & Annotations",
            "### Spatial Transcription / Text Content",
            "### Spatial Transcription / Physical Attributes",
            "## Visible Inscriptions, Labels & Annotations",
        ):
            main_out_parts.append(b)
        else:
            # Ensure sub-section headers remain valid H4/H3 under ### Main Text & Margin Notes (never H2!)
            clean_h = re.sub(r"^##\s+", "#### ", hdr)
            clean_h = re.sub(r"^###\s+", "#### ", clean_h)
            main_out_parts.append(f"{clean_h}\n\n{b}")

    main_body = "\n\n".join(main_out_parts).strip()
    main_body = re.sub(r"\n{2,}---\n*$", "", main_body).strip()

    # If a file (e.g. Archetype 2 or 3 or list-only) has no `| Margin Notes | Main Text |` table at all,
    # ensure it either has `### Main Text & Margin Notes` with its table/text or an intro row before Archetype 2 tables
    if not has_margin_table and not main_body.startswith("|"):
        # Wrap code blocks/paragraphs cleanly in Archetype 3 or intro row if no table exists yet
        if is_arch3:
            esc = main_body.replace("\n", "<br>").replace("```text<br>", "```text\n").replace("<br>```", "\n```")
            main_body = f"| Margin Notes | Main Text |\n| :--- | :--- |\n| **Physical Object & Inscriptions** | {main_body} |"
            # Actually fenced blocks cannot cleanly sit inside inline single-line GFM table row if they have newlines; format without raw newlines!
            plain_inscr = re.sub(r"```(?:text)?\n(.*?)\n```", lambda m: "`" + " / ".join(x.strip() for x in m.group(1).splitlines() if x.strip()) + "`", main_body_raw := "\n\n".join(main_out_parts).strip(), flags=re.S)
            plain_inscr = "<br>".join(x.strip() for x in plain_inscr.splitlines() if x.strip())
            main_body = f"| Margin Notes | Main Text |\n| :--- | :--- |\n| **Physical Object & Verbatim Inscription** | {plain_inscr} |"

    norm_xref = build_cross_references("\n".join(xref_parts), meta_fields)

    final_doc = "\n".join([
        title,
        "",
        "## Metadata",
        norm_meta,
        "",
        "---",
        "",
        "### Header & Archival Classification",
        "",
        norm_class,
        "",
        "---",
        "",
        "### Main Text & Margin Notes",
        "",
        clean_inline(main_body),
        "",
        "---",
        "",
        "### Cross-Reference with `39_Expanded_Keyword_Index.md`",
        "",
        norm_xref,
        "",
    ])

    if final_doc != orig:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(final_doc)
        return True
    return False


def main():
    files = sorted(f for f in os.listdir(TRANS_DIR) if f.endswith(".md"))
    changed = 0
    for f in files:
        if process_file(f):
            changed += 1
    print(f"Normalized {len(files)} files ({changed} updated) to canonical 3-Archetype template.")


if __name__ == "__main__":
    main()
