import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TRANS_DIR = os.path.join(REPO_ROOT, "Transcriptionv2")


def fix_file_pipes(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    new_lines = []
    expected_cols = None
    fixes = 0

    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("|") and s.endswith("|"):
            parts = re.split(r"(?<!\\)\|", s)[1:-1]
            # Delimiter row
            if all(re.match(r"^\s*:?-+:?\s*$", p) for p in parts):
                expected_cols = len(parts)
                new_lines.append(s)
                continue

            # Check if next line is delimiter row (meaning this is a table header row)
            if i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if nxt.startswith("|") and nxt.endswith("|"):
                    nxt_parts = re.split(r"(?<!\\)\|", nxt)[1:-1]
                    if all(re.match(r"^\s*:?-+:?\s*$", p) for p in nxt_parts):
                        expected_cols = len(nxt_parts)
                        new_lines.append(s)
                        continue

            if expected_cols is not None and len(parts) > expected_cols:
                # For 2-column Margin Notes | Main Text, keep col 0 and merge excess pipes as \| into col 1
                if expected_cols == 2:
                    c0 = parts[0].strip()
                    c1 = r" \| ".join(p.strip() for p in parts[1:])
                    new_lines.append(f"| {c0} | {c1} |")
                else:
                    # Keep first (expected_cols - 1) columns, merge excess into last column or prose col
                    fixed_parts = [p.strip() for p in parts[:expected_cols - 1]]
                    last = r" \| ".join(p.strip() for p in parts[expected_cols - 1:])
                    fixed_parts.append(last)
                    new_lines.append("| " + " | ".join(fixed_parts) + " |")
                fixes += 1
                continue

            new_lines.append(ln)
        else:
            expected_cols = None
            new_lines.append(ln)

    if fixes:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(new_lines) + "\n")
    return fixes


def main():
    files = sorted(f for f in os.listdir(TRANS_DIR) if f.endswith(".md"))
    total_rows_fixed = 0
    files_fixed = []
    for fname in files:
        cnt = fix_file_pipes(os.path.join(TRANS_DIR, fname))
        if cnt:
            total_rows_fixed += cnt
            files_fixed.append((fname, cnt))
    print(f"Repaired {total_rows_fixed} table rows across {len(files_fixed)} files: {files_fixed}")


if __name__ == "__main__":
    main()
