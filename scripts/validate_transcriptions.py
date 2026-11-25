import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_JSON = os.path.join(REPO_ROOT, "data.json")
TRANS_JSON = os.path.join(REPO_ROOT, "transcriptions-data.json")
ENTITY_DB_PATH = os.path.join(os.path.dirname(__file__), "entity_database.json")
TRANS_DIR = os.path.join(REPO_ROOT, "Transcriptionv2")
JPG_DIR = os.path.join(REPO_ROOT, "jpg")


def main():
    errors = []

    if not os.path.exists(DATA_JSON):
        print("ERROR: data.json missing")
        sys.exit(1)

    with open(DATA_JSON, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    with open(TRANS_JSON, "r", encoding="utf-8") as f:
        trans_manifest = json.load(f)
    with open(ENTITY_DB_PATH, "r", encoding="utf-8") as f:
        entity_db = json.load(f)

    valid_lines = {e["line"] for e in entity_db}
    if manifest != trans_manifest:
        errors.append("Manifest mismatch: data.json != transcriptions-data.json")

    # Disk concordance & orphan checks
    disk_jpgs = sorted(f"jpg/{f}" for f in os.listdir(JPG_DIR) if f.lower().endswith(".jpg"))
    disk_mds = sorted(f"Transcriptionv2/{f}" for f in os.listdir(TRANS_DIR) if f.endswith(".md"))
    man_imgs = sorted(x["image"] for x in manifest)
    man_txts = sorted(x["text"] for x in manifest)

    if disk_jpgs != man_imgs:
        errors.append(f"Image concordance mismatch: disk={len(disk_jpgs)}, manifest={len(man_imgs)}")
    if disk_mds != man_txts:
        errors.append(f"Text concordance mismatch: disk={len(disk_mds)}, manifest={len(man_txts)}")

    seen_ids = set()
    req_meta_bullets = [
        "## Metadata",
        "- **Image File:**",
        "- **Source:**",
        "- **Date Range:**",
        "- **Key Events & Entities:**",
        "- **Key Events:**",
        "- **Key Entities (Persons):**",
        "- **Key Entities (Places):**",
        "- **Key Entities (Institutions / Terms):**",
    ]
    legacy_markers = ["## Content", "**Keyword Index Check:**", "**Transcription Type:**", "**Transcribed by:**"]

    for entry in manifest:
        fid = entry["id"]
        if fid in seen_ids:
            errors.append(f"{fid}: Duplicate id in manifest")
        seen_ids.add(fid)

        for key in ("image", "text"):
            if "\\" in entry[key]:
                errors.append(f"{fid}: Backslash in path {entry[key]}")
            full_p = os.path.join(REPO_ROOT, entry[key])
            if not os.path.exists(full_p):
                errors.append(f"{fid}: Missing file {entry[key]}")

        md_path = os.path.join(REPO_ROOT, entry["text"])
        raw = open(md_path, "rb").read()
        if raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{fid}: UTF-8 BOM detected")
        c = raw.decode("utf-8")

        img_base = os.path.basename(entry["image"])
        if not c.startswith(f"# Transcription of {img_base}"):
            errors.append(f"{fid}: Title does not start with '# Transcription of {img_base}'")

        for b in req_meta_bullets:
            if b not in c:
                errors.append(f"{fid}: Missing metadata bullet '{b}'")

        for sec in [
            "### Header & Archival Classification",
            "### Main Text & Margin Notes",
            "### Cross-Reference with `39_Expanded_Keyword_Index.md`",
            "* **People:**",
            "* **Places & Institutions:**",
            "* **Terms:**",
        ]:
            if sec not in c:
                errors.append(f"{fid}: Missing required section '{sec}'")

        for leg in legacy_markers:
            if leg in c:
                errors.append(f"{fid}: Legacy marker leaked '{leg}'")

        # No non-template H2 headings
        for ln in c.splitlines():
            if ln.startswith("## ") and ln.strip() != "## Metadata":
                errors.append(f"{fid}: Non-template H2 heading '{ln.strip()}'")

        # Inline HTML balance
        for tag in ("u", "i", "b", "span"):
            opens = len(re.findall(rf"<{tag}(\s[^>]*)?>", c))
            closes = len(re.findall(rf"</{tag}>", c))
            if opens != closes:
                errors.append(f"{fid}: Unbalanced <{tag}> tags ({opens} open vs {closes} close)")

        # Table column integrity
        lines = c.splitlines()
        expected_cols = None
        for idx, ln in enumerate(lines, start=1):
            s = ln.strip()
            if s.startswith("|") and s.endswith("|"):
                parts = re.split(r"(?<!\\)\|", s)[1:-1]
                if all(re.match(r"^\s*:?-+:?\s*$", p) for p in parts):
                    expected_cols = len(parts)
                elif expected_cols is not None and len(parts) != expected_cols:
                    errors.append(f"{fid} L{idx}: GFM table column count {len(parts)} != expected {expected_cols}")
            else:
                expected_cols = None

        # Index citation bounds check
        for m in re.finditer(r"39_Expanded_Keyword_Index\.md#L(\d+)", c):
            ln_num = int(m.group(1))
            if ln_num not in valid_lines:
                errors.append(f"{fid}: Cited index line L{ln_num} does not exist in entity_database.json")

        if r"\therefore" in c:
            errors.append(f"{fid}: Raw LaTeX \\therefore detected")

    print(f"Validated {len(manifest)} corpus entries -> {len(errors)} error(s).")
    if errors:
        for e in errors[:40]:
            print(f"  ERROR: {e}")
        sys.exit(1)
    print("CORPUS VALIDATION PASSED: 0 errors across all 336 entries!")


if __name__ == "__main__":
    main()
