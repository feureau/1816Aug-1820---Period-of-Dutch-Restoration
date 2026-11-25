import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRANS_DIR = os.path.join(REPO_ROOT, "Transcriptionv2")
BACKUP_DIR = os.path.join(REPO_ROOT, "older_transcription_versions", "backup_Transcriptionv2_pre_pilot")

# Hand-verified or specialized multi-column / physical artifact files to skip auto-overwrite
HAND_DONE = {"IMG_1289", "IMG_1290", "IMG_1439", "IMG_1445", "IMG_1446", "IMG_1454", "IMG_1553", "IMG_1554", "IMG_1555"}
TABULAR_AND_PEGON = {"IMG_1463", "IMG_1464", "IMG_1501", "IMG_1507", "IMG_1508", "IMG_1548", "IMG_1561"}
ARCHETYPE_3 = {
    "IMG_1218", "IMG_1219", "IMG_1240", "IMG_1244", "IMG_1248", "IMG_1252",
    "IMG_1285", "IMG_1287", "IMG_1288", "IMG_1299", "IMG_1304", "IMG_1305",
    "IMG_1306", "IMG_1311", "IMG_1359", "IMG_1361", "IMG_1372", "IMG_1421",
    "IMG_1500", "IMG_1505", "IMG_1506", "IMG_1539", "IMG_1552", "IMG_1556",
}

SHORTHAND_EXPANSIONS = [
    (r"\bDP\b", "DP [Pangéran Dipanagara]"),
    (r"\bHB\s*I\b", "HB I [Sultan Hamengkubuwana I]"),
    (r"\bHB\s*II\b", "HB II [Sultan Hamengkubuwana II]"),
    (r"\bHB\s*III\b", "HB III [Sultan Hamengkubuwana III]"),
    (r"\bHB\s*IV\b", "HB IV [Sultan Hamengkubuwana IV]"),
    (r"\bHB\s*V\b", "HB V [Sultan Hamengkubuwana V]"),
    (r"\bH\.B\.\s*IV\b", "H.B. IV [Sultan Hamengkubuwana IV]"),
    (r"\bPB\s*III\b", "PB III [Sunan Pakubuwana III]"),
    (r"\bPB\s*IV\b", "PB IV [Sunan Pakubuwana IV]"),
    (r"\bP\.B\.\s*IV\b", "P.B. IV [Sunan Pakubuwana IV]"),
    (r"\bPB\s*V\b", "PB V [Sunan Pakubuwana V]"),
    (r"\bPB\s*VI\b", "PB VI [Sunan Pakubuwana VI]"),
    (r"\bPA\s*I\b", "PA I [Pangéran Natakusuma / Paku Alam I]"),
    (r"\bP\.A\.\b", "P.A. [Paku Alam I]"),
    (r"\bPA\b", "PA [Pangéran Natakusuma / Paku Alam I]"),
    (r"\bMB\b", "MB [Pangéran Mangkubumi]"),
    (r"\bMN\s*I\b", "MN I [Mangkunagara I]"),
    (r"\bMN\s*II\b", "MN II [Pangéran Prangwedana / Mangkunagara II]"),
    (r"\bMN\b", "MN [Mangkunagara II]"),
    (r"\bNvB\b", "NvB [Major Huibert Gerard Nahuys van Burgst]"),
    (r"\bvIJ\b", "vIJ [Willem Herman van IJsseldijk]"),
    (r"\bG\.G\.\b", "G.G. [Governor-General]"),
    (r"\bSp\.\s*[Dd]\.\b", "Sp. D. [Spanish Dollars]"),
    (r"\bJ\.R\.\b", "J.R. [Java Rupees]"),
    (r"\bDfl\b", "Dfl [Dutch Florins / Guilders]"),
    (r"\bDR\s*IV\b", "DR IV [Radèn Adipati Danureja IV]"),
    (r"\bAsst\.?\s*Res\.?", "Asst. Res [Assistant Resident]"),
    (r"\bGovt\.", "Govt. [Government]"),
    (r"\bgovnm?nt\.?", "govnmt. [government]"),
]


def expand_first_occurrence(text: str) -> str:
    """Expand recognized shorthands only on their first occurrence, skipping inside existing brackets."""
    lines = text.splitlines()
    expanded_keys = set()
    out_lines = []
    for line in lines:
        for idx, (pat, repl) in enumerate(SHORTHAND_EXPANSIONS):
            if idx in expanded_keys:
                continue
            # Split by existing bracketed groups so we never nest brackets
            parts = re.split(r"(\[[^\]]*\])", line)
            changed = False
            for i in range(0, len(parts), 2):
                m = re.search(pat, parts[i])
                if m:
                    # Also verify right after match is not ' ['
                    after = parts[i][m.end():]
                    if not after.lstrip().startswith("["):
                        parts[i] = parts[i][:m.start()] + repl + after
                        expanded_keys.add(idx)
                        changed = True
                        break
            if changed:
                line = "".join(parts)
        out_lines.append(line)
    return "\n".join(out_lines)


def strip_old_editorial_scaffolding(bak_text: str) -> str:
    """Remove synthetic Markdown scaffolding (like `### Contextual Note` or `[^1]: ...`) ONLY if it was an earlier GPT wrap, NOT original source lines."""
    # Check if backup contains old-draft wrapper markers (`^### Contextual Notes:` or `^[^1]:`)
    lines = bak_text.splitlines()
    cleaned = []
    skip_editorial_notes = False
    for ln in lines:
        s = ln.strip()
        if s in ("### Contextual Notes", "### Editorial Note", "**Keyword Index Check:**"):
            skip_editorial_notes = True
            continue
        if skip_editorial_notes and (s == "---" or s.startswith("## ")):
            skip_editorial_notes = False
        if not skip_editorial_notes:
            cleaned.append(ln)
    return "\n".join(cleaned)


def compute_recall(bak_text: str, md_text: str) -> tuple[float, int]:
    bt_clean = strip_old_editorial_scaffolding(bak_text)
    bt_clean = re.sub(r"\[\^\d+\]:.*", "", bt_clean)
    bt_clean = re.sub(r"\[[^\]]*\]", " ", bt_clean)
    m = re.search(
        r"(?ms)^##+ (?:Main Text & Margin Notes|Main Text|Transcription:.*?)\n(.*?)(?=^##+ (?:Cross-Reference|Historical Cross-References|Critical Apparatus|Detailed Notes|Contextual)|$\Z)",
        md_text,
    )
    body = m.group(1) if m else md_text
    body_clean = re.sub(r"\[[^\]]*\]\([^\)]*\)|\[[^\]]*\]|<br>|&nbsp;|•", " ", body)
    btoks = [w.lower() for w in re.findall(r"[A-Za-z0-9]{3,}", bt_clean)]
    if not btoks:
        return 1.0, 0
    bset = set(w.lower() for w in re.findall(r"[A-Za-z0-9]{3,}", body_clean))
    rec = sum(1 for t in btoks if t in bset) / len(btoks)
    return rec, len(btoks)


def bak_to_table_rows(bak_text: str) -> str:
    """Convert pre-pilot verbatim text lines into clean | Margin Notes | Main Text | table rows preserving 100% of text."""
    expanded = expand_first_occurrence(bak_text.strip())
    lines = expanded.splitlines()

    # Split into blank-line-separated blocks, grouping contiguous small header blocks neatly
    blocks = []
    cur = []
    for ln in lines:
        s = ln.rstrip()
        if s == "---" and cur:
            blocks.append(cur)
            cur = []
            continue
        if not s.strip():
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(s)
    if cur:
        blocks.append(cur)

    rows = []
    rows.append("| Margin Notes | Main Text |")
    rows.append("| :--- | :--- |")

    margin_pat = re.compile(
        r"^(?:\[(?:Margin|Red|Top|Note|Footnote)[^\]]*\]|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z.]*(?:\s+18\d\d)?\.?:?|18\d\d(?:\s*[-–]\s*18\d\d)?\s*[:.]?|(?:Nahuys|vIJ|Van IJsseldijk|PB\s*IV|HB\s*IV|PB\s*V|G\.G\.|Res\.|Asst\.\s*Res).*?(?:->|→|to)\s+.*)$",
        re.IGNORECASE,
    )

    pending_margin = []
    for blk in blocks:
        # Check if entire small block looks like top metadata/margin header
        if len(blk) <= 4 and all(len(x) < 48 for x in blk) and len(blocks) > 1 and any(margin_pat.match(x.strip()) or x.strip().startswith("[") or x.strip().isupper() for x in blk):
            # Accumulate as margin / section label if followed by more blocks
            if blk != blocks[-1]:
                pending_margin.extend(blk)
                continue

        # Check first line for inline margin marker or date header
        left_items = list(pending_margin)
        pending_margin = []
        right_lines = []

        for idx, raw_ln in enumerate(blk):
            esc_ln = raw_ln.replace("|", r"\|").replace("\\therefore", "∴").replace(".·.", "∴")
            esc_ln = esc_ln.replace("$\therefore$", "∴")
            if idx == 0 and margin_pat.match(raw_ln.strip()) and len(blk) > 1:
                left_items.append(esc_ln)
            else:
                right_lines.append(esc_ln)

        left_cell = "<br>".join(f"**{x}**" if not x.startswith("**") else x for x in left_items) if left_items else "**Archival Record / Entry**"
        right_cell = "<br>".join(right_lines) if right_lines else "<br>".join(x.replace("|", r"\|") for x in blk)
        rows.append(f"| {left_cell} | {right_cell} |")

    if pending_margin:
        left_cell = "**Archival Notation**"
        right_cell = "<br>".join(x.replace("|", r"\|") for x in pending_margin)
        rows.append(f"| {left_cell} | {right_cell} |")

    return "\n".join(rows)


def main():
    updated = []
    skipped_tables = []

    for fname in sorted(os.listdir(TRANS_DIR)):
        if not fname.endswith(".md"):
            continue
        stem = fname[:-3]
        if stem in HAND_DONE or stem in TABULAR_AND_PEGON or stem in ARCHETYPE_3:
            continue

        bak_path = os.path.join(BACKUP_DIR, stem + ".txt")
        md_path = os.path.join(TRANS_DIR, fname)
        if not os.path.exists(bak_path):
            continue

        with open(bak_path, "r", encoding="utf-8") as f:
            bak_text = f.read()
        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        rec, btoks = compute_recall(bak_text, md_text)
        # Check missing asterisk footnotes
        bak_fn = [ln.strip() for ln in bak_text.splitlines() if re.match(r"^\*\s+[A-Za-z]", ln.strip())]
        fn_missing = any(
            not all(re.search(re.escape(w), md_text, re.I) for w in re.findall(r"[A-Za-z]{4,}", fn)[:4])
            for fn in bak_fn
        )

        if (btoks >= 30 and rec < 0.90) or fn_missing:
            # Check if file has extra markdown data tables we want to preserve below the main text table
            table_rows_md = bak_to_table_rows(bak_text)

            # Extract any extra non-Margin data tables to keep if present
            extra_table_block = ""
            lines = md_text.splitlines()
            for i, ln in enumerate(lines[:-1]):
                if ln.strip().startswith("|") and re.match(r"^\|[\s:\-\|]+\|$", lines[i+1].strip()):
                    if "Margin Notes" not in ln:
                        skipped_tables.append(stem)
                        # Grab table block
                        j = i
                        while j < len(lines) and (lines[j].strip().startswith("|") or not lines[j].strip()):
                            j += 1
                        extra_table_block += "\n\n" + "\n".join(lines[i:j]).strip()

            # Replace main text section cleanly
            m = re.search(
                r"(?ms)(^##+ (?:Main Text & Margin Notes|Main Text|Transcription:.*?)\n)(.*?)(?=^##+ (?:Cross-Reference|Historical Cross-References|Critical Apparatus|Detailed Notes|Contextual)|$\Z)",
                md_text,
            )
            if not m:
                continue

            new_body = "\n" + table_rows_md + extra_table_block + "\n\n---\n\n"
            new_md = md_text[:m.start()] + "### Main Text & Margin Notes\n" + new_body + md_text[m.end():]
            with open(md_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_md)
            updated.append((stem, round(rec * 100, 1), fn_missing))

    print(f"Restored verbatim source text in {len(updated)} files:")
    for s, r, fn in updated:
        print(f"  {s}: prev_recall={r}%, fn_missing={fn}")
    if skipped_tables:
        print(f"Preserved extra Archetype 2 tables in: {skipped_tables}")


if __name__ == "__main__":
    main()
