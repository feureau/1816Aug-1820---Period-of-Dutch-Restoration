#!/usr/bin/env python3
"""
Regenerate transcriptions-content.js from the .txt files listed in
transcriptions-data.js.  Embeds every transcript as a JSON-escaped
JavaScript string so the viewer works from file:// with no CORS issues.
"""
import json, re
from pathlib import Path

DATA_JS = Path("transcriptions-data.js")
OUT     = Path("transcriptions-content.js")
BASE    = Path(".")          # adjust if script is run from elsewhere

# --- 1. Parse transcriptions-data.js for id / image / text mappings ---
src = DATA_JS.read_text(encoding="utf-8")

# matches:  { "id": "IMG_1218", "image": "...", "text": "..." }
PATTERN = re.compile(
    r'\{\s*"id"\s*:\s*"([^"]+)"\s*,\s*"image"\s*:\s*"([^"]+)"\s*,\s*"text"\s*:\s*"([^"]+)"\s*\}'
)
entries = PATTERN.findall(src)
if not entries:
    raise SystemExit("No entries found in transcriptions-data.js — check the file.")

# --- 2. Read every transcript ---
content = {}
missing = []
for entry_id, image, text_path in entries:
    p = BASE / text_path
    if p.exists():
        content[entry_id] = p.read_text(encoding="utf-8")
    else:
        missing.append(text_path)

# --- 3. Emit JSON (valid JavaScript object literal) ---
payload = json.dumps(content, ensure_ascii=False)
# Guard against U+2028 / U+2029, which are valid JSON but illegal in JS strings.
payload = payload.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

OUT.write_text(
    "/* AUTO-GENERATED from Transcription/*.txt — do not edit by hand. */\n"
    "window.__TRANSCRIPTIONS_CONTENT__ = " + payload + ";\n",
    encoding="utf-8",
)

total = sum(len(v) for v in content.values())
print(f"Wrote {OUT}  ({len(content)} transcripts, {total:,} chars)")
if missing:
    print(f"WARNING: {len(missing)} transcript file(s) not found:")
    for m in missing[:10]:
        print(f"  - {m}")
    if len(missing) > 10:
        print(f"  ... and {len(missing) - 10} more")
