#!/usr/bin/env python3
"""Regenerate book-data.js from document.md."""
import json
from pathlib import Path

SRC = Path("1816Aug-1820 - Period of Dutch Restoration.md")
OUT = Path("book-data.js")

md = SRC.read_text(encoding="utf-8")

# json.dumps escapes quotes, backslashes, newlines, and unicode safely.
# JSON string syntax is valid JavaScript, so the result parses as a JS object.
payload = json.dumps({SRC.name: md}, ensure_ascii=False)

OUT.write_text(
    f"/* AUTO-GENERATED from {SRC} — do not edit by hand. */\n"
    "window.__BOOK_DATA__ = " + payload + ";\n",
    encoding="utf-8",
)

print(f"Wrote {OUT} ({len(payload):,} bytes) from {SRC} ({len(md):,} chars)")
