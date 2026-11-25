import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRANS_DIR = os.path.join(REPO_ROOT, "Transcriptionv2")
BACKUP_DIR = os.path.join(REPO_ROOT, "older_transcription_versions", "backup_Transcriptionv2_pre_pilot")

SKIP_RECALL = {
    # Archetype 2 tabular restructurings
    "IMG_1463", "IMG_1464", "IMG_1507", "IMG_1508", "IMG_1548", "IMG_1561",
    # Archetype 3 physical cards/covers/versos (backups sometimes describe layout differently)
    "IMG_1218", "IMG_1219", "IMG_1240", "IMG_1244", "IMG_1248", "IMG_1252",
    "IMG_1285", "IMG_1287", "IMG_1288", "IMG_1299", "IMG_1304", "IMG_1305",
    "IMG_1306", "IMG_1311", "IMG_1359", "IMG_1361", "IMG_1372", "IMG_1421",
    "IMG_1500", "IMG_1505", "IMG_1506", "IMG_1539", "IMG_1552", "IMG_1556",
}


def strip_old_editorial_scaffolding(bak_text: str) -> str:
    lines = bak_text.splitlines()
    cleaned = []
    skip = False
    for ln in lines:
        s = ln.strip()
        if s in ("### Contextual Notes", "### Editorial Note", "**Keyword Index Check:**"):
            skip = True
            continue
        if skip and (s == "---" or s.startswith("## ")):
            skip = False
        if not skip and not re.match(r"^\[\^\d+\]:", s):
            cleaned.append(ln)
    return "\n".join(cleaned)


def normalize_tokens(text: str) -> list[str]:
    text = re.sub(r"\[[^\]]*\]\([^\)]*\)", "", text)
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"<br>|&nbsp;|•", " ", text)
    return [w.lower() for w in re.findall(r"[A-Za-z0-9]{3,}", text)]


def extract_main_text_section(md_text: str) -> str:
    m = re.search(
        r"(?ms)^##+ (?:Main Text & Margin Notes|Main Text|Spatial Transcription.*?|Transcription:.*?)\n(.*?)(?=^##+ (?:Cross-Reference|Historical Cross-References|Critical Apparatus|Detailed Notes|Contextual)|$\Z)",
        md_text,
    )
    return m.group(1) if m else md_text


def main():
    md_files = sorted(f for f in os.listdir(TRANS_DIR) if f.endswith(".md"))
    suspects = []
    footnote_drops = []
    ellipsis_hits = []

    for fname in md_files:
        stem = os.path.splitext(fname)[0]
        if stem in SKIP_RECALL:
            continue

        md_path = os.path.join(TRANS_DIR, fname)
        bak_path = os.path.join(BACKUP_DIR, stem + ".txt")
        if not os.path.exists(bak_path):
            continue

        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()
        with open(bak_path, "r", encoding="utf-8") as f:
            bak_text = f.read()

        body_text = extract_main_text_section(md_text)

        # Ignore translation-only ellipses in Pegon script manuscript IMG_1501 and continued word markers in 1438-1441
        if stem != "IMG_1501":
            bak_dots = len(re.findall(r"\.\.\.", bak_text))
            new_dots = len(re.findall(r"\.\.\.", body_text))
            if new_dots - bak_dots >= 2:
                ellipsis_hits.append((stem, bak_dots, new_dots))

        # Check genuine primary footnotes (* ...)
        bak_fn = [ln.strip() for ln in bak_text.splitlines() if re.match(r"^\*\s+[A-Za-z]", ln.strip())]
        for fn in bak_fn:
            # Skip bullet items inside raw Carey lists when formatted as prose/bullets; focus on actual bottom footnotes or check first 3 alpha words (excluding LaTeX tokens)
            fn_clean = re.sub(r"\$\\therefore\$|\\therefore", " ", fn)
            words = re.findall(r"[A-Za-z]{4,}", fn_clean)[:3]
            if words and not all(re.search(re.escape(w), body_text, re.I) for w in words):
                footnote_drops.append((stem, fn[:80]))

        bt_clean = strip_old_editorial_scaffolding(bak_text)
        bak_toks = normalize_tokens(bt_clean)
        if len(bak_toks) >= 30:
            body_set = set(normalize_tokens(body_text))
            hits = sum(1 for t in bak_toks if t in body_set)
            recall = hits / len(bak_toks)
            if recall < 0.92:
                suspects.append((stem, round(recall * 100, 1), len(bak_toks)))

    print(f"Audited {len(md_files)} files (excluding {len(SKIP_RECALL)} Archetype 2/3 files).")
    print(f"Ellipsis additions (>=2 new '...'): {len(ellipsis_hits)}")
    for item in ellipsis_hits:
        print(f"  {item}")
    print(f"Missing primary footnotes: {len(footnote_drops)}")
    for stem, fn in footnote_drops:
        print(f"  {stem}: {fn}")
    print(f"Low token recall (<92%): {len(suspects)}")
    for item in sorted(suspects, key=lambda x: x[1]):
        print(f"  {item[0]}: recall={item[1]}% (bak_tokens={item[2]})")


if __name__ == "__main__":
    main()
