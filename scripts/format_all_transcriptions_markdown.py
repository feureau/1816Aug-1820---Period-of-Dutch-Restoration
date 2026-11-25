import os
import re
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRANS_DIR = os.path.join(REPO_ROOT, "Transcriptionv2")


def write_with_retry(path: str, content: str):
    for attempt in range(5):
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            return
        except PermissionError:
            time.sleep(0.1 * (attempt + 1))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def format_markdown(text: str) -> str:
    # Normalize CRLF -> LF and strip BOM
    text = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")

    # Split header block and body at the first standalone ---
    m_split = re.search(r"(?m)^---\s*$", text)
    if m_split:
        hdr = text[:m_split.start()].rstrip("\n")
        rest = text[m_split.end():].lstrip("\n")
        # Ensure multi-line metadata lines (except last before ---) end with two trailing spaces
        hdr_lines = hdr.splitlines()
        out_hdr = []
        for idx, ln in enumerate(hdr_lines):
            if idx < len(hdr_lines) - 1 and re.match(r"^\s*-\s+\*\*", ln):
                out_hdr.append(ln.rstrip() + "  ")
            else:
                out_hdr.append(ln.rstrip())
        text = "\n".join(out_hdr) + "\n\n---\n\n" + rest

    lines = text.splitlines()
    out = []
    in_code = False

    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("```"):
            if not in_code and out and out[-1] != "":
                out.append("")
            out.append(ln.rstrip())
            in_code = not in_code
            continue

        if in_code:
            out.append(ln.rstrip())
            continue

        is_heading = bool(re.match(r"^#{1,6}\s+", s))
        is_hr = bool(re.match(r"^---\s*$", s))
        is_tbl = s.startswith("|") and s.endswith("|")

        if is_heading or is_hr:
            if out and out[-1] != "":
                out.append("")
            out.append(s)
            out.append("")
            continue

        if is_tbl:
            prev_is_tbl = bool(out and out[-1].strip().startswith("|") and out[-1].strip().endswith("|"))
            if not prev_is_tbl and out and out[-1] != "":
                out.append("")
            out.append(ln.rstrip())
            continue

        # Ensure blank line after table ends
        if out and out[-1].strip().startswith("|") and out[-1].strip().endswith("|") and s != "":
            out.append("")

        out.append(ln.rstrip())

    res = "\n".join(out)
    res = re.sub(r"\n{3,}", "\n\n", res).strip() + "\n"
    return res


def main():
    files = sorted(f for f in os.listdir(TRANS_DIR) if f.endswith(".md"))
    changed = 0
    for fname in files:
        p = os.path.join(TRANS_DIR, fname)
        with open(p, "rb") as f:
            raw = f.read()
        orig = raw.decode("utf-8-sig")
        formatted = format_markdown(orig)
        if raw.startswith(b"\xef\xbb\xbf") or formatted != orig.replace("\r\n", "\n"):
            write_with_retry(p, formatted)
            changed += 1
    print(f"Formatted {len(files)} Markdown files ({changed} updated, 0 BOM).")


if __name__ == "__main__":
    main()
