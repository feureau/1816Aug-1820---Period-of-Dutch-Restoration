import html
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(REPO_ROOT, "39_Expanded_Keyword_Index.md")
OUT_HTML = os.path.join(REPO_ROOT, "dictionary.html")


def parse_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    items = []
    category = "General"

    for idx, raw in enumerate(lines, start=1):
        s = raw.strip()
        if not s or s.startswith("# ") or s == "---":
            continue
        if s.startswith("## "):
            raw_cat = re.sub(r"^\d+\.\s*", "", s[3:].strip())
            raw_cat = re.sub(r"\s*\(Appendix[^)]*\)", "", raw_cat).strip()
            category = raw_cat
            continue
        if s.startswith("### "):
            raw_sub = re.sub(r"\s*\(Appendix[^)]*\)", "", s[4:].strip())
            category = raw_sub
            continue

        m_bold = re.match(r"^[\*\-]\s+\*\*(.+?)\*\*\s*:?\s*(.*)$", s)
        if m_bold:
            items.append((idx, category, m_bold.group(1).strip(), m_bold.group(2).strip()))
            continue

        m_ital = re.match(r"^[\*\-]\s+\*(.+?)\*\s*(.*)$", s)
        if m_ital:
            items.append((idx, category, m_ital.group(1).strip(), m_ital.group(2).strip()))
            continue

        m_plain = re.match(r"^(?:[\*\-]|\d+\.)\s+(.+)$", s)
        if m_plain:
            body = m_plain.group(1).strip()
            items.append((idx, category, body, ""))

    return items


def main():
    items = parse_index()
    categories = sorted(set(cat for _, cat, _, _ in items))
    total = len(items)

    cat_options = "\n".join(
        f'                <option value="{html.escape(c)}">{html.escape(c)}</option>'
        for c in categories
    )

    rows = []
    for ln, cat, term, desc in items:
        rows.append(
            f'            <tr data-cat="{html.escape(cat)}">'
            f'<td><span class="tag">{html.escape(cat)}</span></td>'
            f'<td class="term-cell">{html.escape(term)}</td>'
            f'<td>{html.escape(desc)}</td>'
            f'<td class="line-cell">L{ln}</td>'
            f"</tr>"
        )
    rows_html = "\n".join(rows)

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>Keyword &amp; Reference Dictionary — Dutch Restoration (1816–1820)</title>
    <style>
        :root {{ color-scheme: dark; --bg: #1a1a1a; --panel: #222222; --panel-alt: #2d2d2d; --fg: #e0e0e0; --muted: #9a9a9a; --line: #333333; --accent: #4a9eff; }}
        * {{ box-sizing: border-box; }}
        body {{ background-color: var(--bg); color: var(--fg); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        select option {{ background-color: var(--panel); color: var(--fg); }}
        .nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 18px; align-items: center; }}
        .nav a {{ color: var(--fg); background: var(--panel-alt); text-decoration: none; padding: 8px 14px; border-radius: 5px; border: 1px solid var(--line); font-size: 14px; }}
        .nav a:hover {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
        .header-card {{ background: var(--panel-alt); padding: 22px 26px; border-radius: 6px; border: 1px solid var(--line); margin-bottom: 20px; }}
        .header-card h1 {{ margin: 0 0 6px 0; font-size: 24px; color: #fff; }}
        .header-card p {{ margin: 0; color: var(--muted); font-size: 14px; }}
        .controls {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 14px; }}
        .controls input, .controls select {{ background: var(--panel); color: var(--fg); border: 1px solid #444; padding: 10px 14px; border-radius: 5px; font-size: 14px; }}
        .controls input {{ flex: 1; min-width: 240px; }}
        .controls select {{ min-width: 240px; }}
        #statsBar {{ color: var(--muted); font-size: 13px; margin-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; background: var(--panel); border: 1px solid var(--line); font-size: 14px; }}
        th {{ background: #262626; color: #fff; text-align: left; padding: 11px 12px; border-bottom: 2px solid #444; position: sticky; top: 0; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); vertical-align: top; }}
        tbody tr:nth-child(even) {{ background: #1f1f1f; }}
        tbody tr:hover {{ background: #2a323d; }}
        .tag {{ display: inline-block; background: #1f334d; color: #8ec5ff; border: 1px solid #355a85; border-radius: 4px; padding: 2px 8px; font-size: 12px; white-space: nowrap; }}
        .term-cell {{ font-weight: 600; color: #fff; }}
        .line-cell {{ color: var(--muted); font-family: monospace; font-size: 12px; white-space: nowrap; }}
    </style>
</head>
<body>
    <nav class="nav">
        <a href="index.html">← Portal</a>
        <a href="transcriptions.html">Side-by-Side Viewer</a>
        <a href="full.html">Full Documentation</a>
    </nav>
    <div class="header-card">
        <h1>Historical Reference &amp; Keyword Dictionary</h1>
        <p>Immutable ground-truth lexicon parsed directly from <code>39_Expanded_Keyword_Index.md</code> ({total} entries across {len(categories)} categories).</p>
    </div>
    <div class="controls">
        <input type="text" id="searchInput" placeholder="Filter by term, category, variant spelling, or historical description..." aria-label="Filter dictionary">
        <select id="categorySelect" aria-label="Filter by category">
            <option value="">All Categories ({total} entries)</option>
{cat_options}
        </select>
    </div>
    <div id="statsBar">Showing {total} of {total} entries.</div>
    <table>
        <thead>
            <tr>
                <th>Category</th>
                <th>Term / Name</th>
                <th>Description / Historical Role</th>
                <th>Index Ref</th>
            </tr>
        </thead>
        <tbody id="dictBody">
{rows_html}
        </tbody>
    </table>
    <script>
        const searchInput = document.getElementById("searchInput");
        const categorySelect = document.getElementById("categorySelect");
        const rows = Array.from(document.querySelectorAll("#dictBody tr"));
        const statsBar = document.getElementById("statsBar");
        const total = rows.length;

        function filterRows() {{
            const q = searchInput.value.trim().toLowerCase();
            const cat = categorySelect.value;
            let visible = 0;
            for (const row of rows) {{
                const rowCat = row.getAttribute("data-cat") || "";
                const text = row.textContent.toLowerCase();
                const matchCat = !cat || rowCat === cat;
                const matchText = !q || text.includes(q);
                if (matchCat && matchText) {{
                    row.style.display = "";
                    visible++;
                }} else {{
                    row.style.display = "none";
                }}
            }}
            statsBar.textContent = `Showing ${{visible}} of ${{total}} entries.`;
        }}

        searchInput.addEventListener("input", filterRows);
        categorySelect.addEventListener("change", filterRows);
    </script>
</body>
</html>
"""
    with open(OUT_HTML, "w", encoding="utf-8", newline="\n") as f:
        f.write(doc)
    print(f"Generated {OUT_HTML} with {total} entries across {len(categories)} categories.")


if __name__ == "__main__":
    main()
