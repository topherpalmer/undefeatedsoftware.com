"""Builds the Undefeated Software site: each page in pages/ wrapped in the shared head,
header and footer, written to the output folder with the stylesheet, script and icon.

    python build.py <out-dir>            the site, as full pages
    python build.py <out-dir> --preview  the same, with index.html as page content only
                                         (an Artifact preview wraps its main page itself)
"""

import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
FONTS = (
    "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,600..900"
    "&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap"
)
NAV = [
    ("services.html", "Services"),
    ("approach.html", "How we work"),
    ("work.html", "Work"),
    ("about.html", "About"),
]
MARK = """<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true">
  <rect width="32" height="32" rx="9" fill="var(--accent)"/>
  <path d="M9.5 8.5v8.2a6.5 6.5 0 0 0 13 0V8.5" fill="none" stroke="var(--accent-ink)" stroke-width="3.2" stroke-linecap="round"/>
  <circle cx="16" cy="9.6" r="2.1" fill="var(--accent-ink)"/>
</svg>"""
ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="9" fill="#1e9fe3"/><path d="M9.5 8.5v8.2a6.5 6.5 0 0 0 13 0V8.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/><circle cx="16" cy="9.6" r="2.1" fill="#fff"/></svg>"""


def header(current: str) -> str:
    here = ' aria-current="page"'
    links = "\n".join(
        f'      <a href="{href}"{here if href == current else ""}>{label}</a>' for href, label in NAV
    )
    return f"""<header class="site-head" data-open="false">
  <div class="wrap head-row">
    <a class="brand" href="index.html" aria-label="Undefeated Software, home">
      {MARK}
      <span class="brand-name">Undefeated<span>.</span></span>
    </a>
    <nav class="nav" id="site-nav" aria-label="Main">
{links}
    </nav>
    <div class="head-actions">
      <a class="pill line" href="contact.html">Contact us</a>
      <a class="pill solid" href="contact.html#start">Book a call</a>
    </div>
    <button class="menu-btn" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Menu">
      <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 6h14M3 10h14M3 14h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>"""


FOOTER = """<footer class="site-foot">
  <div class="wrap foot-row">
    <div style="display:grid;gap:10px;max-width:380px">
      <a class="brand" href="index.html" aria-label="Undefeated Software, home">""" + MARK + """<span class="brand-name">Undefeated<span>.</span></span></a>
      <p>AI business automation. Agents build your software and run your workflows; your people decide at every gate.</p>
    </div>
    <nav class="foot-links" aria-label="Footer">
      <a href="services.html">Services</a>
      <a href="approach.html">How we work</a>
      <a href="work.html">Work</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
    </nav>
    <p>&copy; 2026 Undefeated Software</p>
  </div>
</footer>"""


def page(source: Path) -> tuple[str, str, str]:
    text = source.read_text()
    meta = re.match(r"<!--\s*title:(.*?)\|\s*description:(.*?)-->\n", text, re.S)
    assert meta, f"{source.name} needs a title/description comment"
    return meta.group(1).strip(), meta.group(2).strip(), text[meta.end():]


def head(title: str, description: str) -> str:
    return f"""<title>{title}</title>
<meta name="description" content="{description}">
<meta name="claude:viewport-fit-sides" content="cover">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta name="theme-color" content="#1e9fe3">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="site.css">"""


def build(out: Path, preview: bool) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for source in sorted((HERE / "pages").glob("*.html")):
        title, description, body = page(source)
        content = f"{header(source.name)}\n<main>\n{body}\n</main>\n{FOOTER}\n<script src=\"site.js\"></script>\n"
        if preview and source.name == "index.html":
            html = head(title, description) + "\n" + content
        else:
            html = (
                "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                f"{head(title, description)}\n</head>\n<body>\n{content}</body>\n</html>\n"
            )
        (out / source.name).write_text(html)
    shutil.copy(HERE / "site.css", out / "site.css")
    shutil.copy(HERE / "site.js", out / "site.js")
    (out / "icon.svg").write_text(ICON)


if __name__ == "__main__":
    build(Path(sys.argv[1]), "--preview" in sys.argv[2:])
