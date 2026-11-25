import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(REPO_ROOT, "39_Expanded_Keyword_Index.md")
OUT_PATH = os.path.join(os.path.dirname(__file__), "entity_database.json")


def main():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    entries = []
    top_cat = ""
    sub_cat = ""

    for idx, raw in enumerate(lines, start=1):
        s = raw.strip()
        if not s:
            continue
        if s.startswith("## "):
            top_cat = s[3:].strip()
            sub_cat = ""
            continue
        if s.startswith("### "):
            sub_cat = s[4:].strip()
            continue
        if s.startswith("# ") or s == "---":
            continue

        # Bold bullet: *   **Term**: Description
        m_bold = re.match(r'^[\*\-]\s+\*\*(.+?)\*\*\s*:?\s*(.*)$', s)
        if m_bold:
            term = m_bold.group(1).strip()
            desc = m_bold.group(2).strip()
            entries.append({
                "line": idx,
                "top_category": top_cat,
                "sub_category": sub_cat,
                "term": term,
                "desc": desc,
                "raw": s,
            })
            continue

        # Italic bullet: *   *Term* (Description) or *   *Term*: Description
        m_ital = re.match(r'^[\*\-]\s+\*(.+?)\*\s*(.*)$', s)
        if m_ital:
            term = m_ital.group(1).strip()
            desc = m_ital.group(2).strip()
            entries.append({
                "line": idx,
                "top_category": top_cat,
                "sub_category": sub_cat,
                "term": term,
                "desc": desc,
                "raw": s,
            })
            continue

        # Plain bullet: *   Name (Dates) or 1. Name
        m_plain = re.match(r'^(?:[\*\-]|\d+\.)\s+(.+)$', s)
        if m_plain:
            body = m_plain.group(1).strip()
            entries.append({
                "line": idx,
                "top_category": top_cat,
                "sub_category": sub_cat,
                "term": body,
                "desc": "",
                "raw": s,
            })

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"Parsed {len(lines)} lines from 39_Expanded_Keyword_Index.md -> {len(entries)} indexed entries in {OUT_PATH}")


if __name__ == "__main__":
    main()
