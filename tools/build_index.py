"""Regenerate index.html (personal intro + post archive grouped by year) and sitemap.xml.

Usage: python3 tools/build_index.py
"""
import html
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POST = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-.*\.html$")
TITLE = re.compile(r"<title>(.*?)</title>", re.S)
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def clean_title(raw: str, slug: str) -> str:
    """Old imports carry markdown/caption junk in titles; fall back to the slug."""
    text = html.unescape(re.sub(r"\s+", " ", raw)).strip()
    junk = text.startswith(("[", "!", "\\[", "_")) or "http" in text or len(text) > 140
    if not text or text in {"…", "..."} or junk:
        words = slug.split("-")[3:] or ["untitled"]
        text = " ".join(words[:8]).capitalize()
    return text


def posts():
    for path in sorted(ROOT.glob("*.html"), reverse=True):
        m = POST.match(path.name)
        if not m:
            continue
        found = TITLE.search(path.read_text(encoding="utf-8", errors="replace"))
        title = clean_title(found.group(1) if found else "", path.stem)
        yield m.group(1), f"{MONTHS[int(m.group(2)) - 1]} {int(m.group(3))}", title, path.name


def write_sitemap(hrefs):
    urls = ["  <url><loc>https://nilleb.io/</loc></url>"] + [
        f"  <url><loc>https://nilleb.io/{html.escape(h)}</loc><lastmod>{h[:10]}</lastmod></url>"
        for h in hrefs
    ]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )


def main():
    by_year = defaultdict(list)
    for year, day, title, href in posts():
        by_year[year].append((day, title, href))
    archive = "\n".join(
        f'<section class="year"><h3>{year}</h3><ul>'
        + "".join(
            f'<li><a href="{html.escape(h)}">{html.escape(t)}</a><span>{d}</span></li>'
            for d, t, h in items
        )
        + "</ul></section>"
        for year, items in sorted(by_year.items(), reverse=True)
    )
    template = (ROOT / "tools" / "index.template.html").read_text(encoding="utf-8")
    count = sum(len(v) for v in by_year.values())
    out = template.replace("{{archive}}", archive).replace("{{count}}", str(count))
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    write_sitemap(h for items in by_year.values() for _, _, h in items)
    print(f"index.html + sitemap.xml: {count} posts across {len(by_year)} years")


if __name__ == "__main__":
    main()
