import json, re
from pathlib import Path

src = Path("transcriptions-data.js").read_text(encoding="utf-8")
entries = re.findall(r'\{\s*"id"\s*:\s*"([^"]+)"\s*,\s*"image"\s*:\s*"([^"]+)"\s*,\s*"text"\s*:\s*"([^"]+)"\s*\}', src)

out = ["# All Transcriptions\n\nThis document contains all transcriptions compiled into a single reading view.\n"]
for eid, img, txt in entries:
    p = Path(txt)
    if p.exists():
        out.append(f"\n---\n\n## {eid}\n\n")
        out.append(p.read_text(encoding="utf-8").strip() + "\n")

Path("all_transcriptions.md").write_text("".join(out), encoding="utf-8")
print("Generated all_transcriptions.md successfully.")