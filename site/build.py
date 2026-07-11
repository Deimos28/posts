#!/usr/bin/env python3
"""Build the essay site.
essays/<nn>-<slug>/published.md  -> _site/<slug>.html
essays without published.md but with a Substack URL in notes.md -> external link on index.
notes.md and draft.md are never published."""
import re, subprocess, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
OUT.mkdir(exist_ok=True)
(OUT / "style.css").write_text((ROOT / "site/style.css").read_text())

FIGS = ROOT / "shared/figures"

def inline_figures(html_path: pathlib.Path):
    """Replace <img src="figures/X.svg"...> with the SVG contents so page fonts apply."""
    h = html_path.read_text()
    def repl(m):
        svg_file = FIGS / pathlib.Path(m.group(1)).name
        if not svg_file.exists():
            return m.group(0)
        svg = svg_file.read_text()
        svg = svg.replace("<svg ", '<svg style="width:100%;height:auto;margin:1.5rem 0" ', 1)
        return svg
    h = re.sub(r'<img src="figures/([^"]+\.svg)"[^>]*/?>', repl, h)
    html_path.write_text(h)

def first_heading(md):
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else "Untitled"

def subtitle(md):
    m = re.search(r"^\*(.+)\*$", md, re.M)
    return m.group(1).strip() if m else ""

entries = []
for d in sorted((ROOT / "essays").iterdir()):
    if not d.is_dir():
        continue
    slug = re.sub(r"^\d+\w*-", "", d.name)
    pub, notes = d / "published.md", d / "notes.md"
    if pub.exists():
        md = pub.read_text()
        title = first_heading(md)
        subprocess.run(
            ["pandoc", str(pub), "-f", "markdown", "-t", "html5", "--standalone",
             "--template", str(ROOT / "site/template.html"),
             "--metadata", f"title={title}", "-V", "root=",
             "-o", str(OUT / f"{slug}.html")], check=True)
        inline_figures(OUT / f"{slug}.html")
        entries.append((title, subtitle(md), f"{slug}.html"))
    elif notes.exists():
        m = re.search(r"https://deimos28\.substack\.com/\S+", notes.read_text())
        if m:
            entries.append((first_heading(notes.read_text()), "on Substack",
                            m.group(0).rstrip(").,")))

items = "\n".join(
    f'<li><a href="{html.escape(h)}">{html.escape(t)}</a>'
    f'<span class="sub">{html.escape(s)}</span></li>'
    for t, s, h in entries)
body = f'<h1>Essays</h1>\n<ul class="essays">\n{items}\n</ul>'
tpl = (ROOT / "site/template.html").read_text()
page = (tpl.replace("$title$", "Essays — Charles-Edouard Cady")
           .replace("$root$", "").replace("$body$", body))
(OUT / "index.html").write_text(page)
print("built:", [e[2] for e in entries])
