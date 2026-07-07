#!/usr/bin/env python3
"""Генератор блога: превращает posts/*.md в страницы blog/*.html,
обновляет blog/index.html и sitemap.xml. Запуск: python3 build.py"""

import datetime
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://alexandragulamova.com"
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

HEADER = """<header class="site">
  <div class="wrap">
    <a class="logo" href="../index.html">Alexandra Gulamova</a>
    <nav>
      <a href="../index.html">About</a>
      <a href="index.html" aria-current="page">Blog</a>
      <a href="../talks/index.html">Talks</a>
      <a href="../media-kit.html">Media kit</a>
    </nav>
  </div>
</header>"""

FOOTER = """<footer class="site">
  <div class="wrap">
    © 2026 Alexandra Gulamova · <a href="https://savant.chat">Savant.chat</a>
  </div>
</footer>"""


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("Нет frontmatter (блока --- ... --- в начале файла)")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, m.group(2).strip()


def inline_md(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def md_to_html(md):
    blocks = re.split(r"\n\s*\n", md)
    out = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith("## "):
            out.append(f"      <h2>{inline_md(block[3:])}</h2>")
        elif all(line.startswith("- ") for line in block.splitlines()):
            items = "\n".join(f"        <li>{inline_md(l[2:])}</li>" for l in block.splitlines())
            out.append(f"      <ul>\n{items}\n      </ul>")
        elif all(line.startswith(">") for line in block.splitlines()):
            quote = " ".join(l.lstrip("> ").strip() for l in block.splitlines())
            out.append(f"      <blockquote>\n        <p>{inline_md(quote)}</p>\n      </blockquote>")
        else:
            out.append(f"      <p>{inline_md(' '.join(block.splitlines()))}</p>")
    return "\n\n".join(out)


def month_year(date_str):
    d = datetime.date.fromisoformat(date_str)
    return f"{MONTHS[d.month - 1]} {d.year}"


def build_post(meta, body_html, slug):
    title = meta["title"]
    esc_title = html.escape(title, quote=False)
    desc = html.escape(meta["description"], quote=True)
    meta_line = f"{month_year(meta['date'])} · Alexandra Gulamova"
    if meta.get("meta_extra"):
        meta_line += f" · {html.escape(meta['meta_extra'], quote=False)}"
    json_title = title.replace('"', '\\"')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc_title} — Alexandra Gulamova</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE_URL}/blog/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{desc}">
<link rel="stylesheet" href="../style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{json_title}",
  "datePublished": "{meta['date']}",
  "author": {{
    "@type": "Person",
    "name": "Alexandra Gulamova",
    "url": "{SITE_URL}/"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Savant.chat",
    "url": "https://savant.chat"
  }}
}}
</script>
</head>
<body>

{HEADER}

<main>
  <div class="wrap">
    <article>
      <h1>{esc_title}</h1>
      <p class="meta">{meta_line}</p>

{body_html}
    </article>
  </div>
</main>

{FOOTER}

</body>
</html>
"""


def build_index(posts):
    items = []
    for meta, slug in posts:
        items.append(f"""      <li>
        <span class="date">{month_year(meta['date'])}</span>
        <a class="title" href="{slug}.html">{html.escape(meta['title'], quote=False)}</a>
        <p>{html.escape(meta['description'], quote=False)}</p>
      </li>""")
    items_html = "\n".join(items)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog — Alexandra Gulamova</title>
<meta name="description" content="Notes by Alexandra Gulamova, co-founder of Savant.chat, on AI-native security, smart contract auditing and building in Web3.">
<link rel="canonical" href="{SITE_URL}/blog/">
<link rel="stylesheet" href="../style.css">
</head>
<body>

{HEADER}

<main>
  <div class="wrap">
    <h1>Blog</h1>
    <p class="tagline">Notes on AI-native security and building Savant.chat.</p>

    <ul class="post-list">
{items_html}
    </ul>
  </div>
</main>

{FOOTER}

</body>
</html>
"""


def build_sitemap(posts):
    today = datetime.date.today().isoformat()
    urls = [(f"{SITE_URL}/", today),
            (f"{SITE_URL}/media-kit.html", today),
            (f"{SITE_URL}/blog/", today)]
    urls += [(f"{SITE_URL}/blog/{slug}.html", meta["date"]) for meta, slug in posts]
    talks_dir = ROOT / "talks"
    if talks_dir.is_dir():
        urls.append((f"{SITE_URL}/talks/", today))
        urls += [(f"{SITE_URL}/talks/{f.name}", today)
                 for f in sorted(talks_dir.glob("*.html")) if f.name != "index.html"]
    entries = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n  </url>"
        for loc, mod in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n'


def main():
    posts_dir = ROOT / "posts"
    blog_dir = ROOT / "blog"
    blog_dir.mkdir(exist_ok=True)

    posts = []
    for md_file in sorted(posts_dir.glob("*.md")):
        meta, body = parse_frontmatter(md_file.read_text(encoding="utf-8"))
        for field in ("title", "date", "description"):
            if field not in meta:
                raise ValueError(f"{md_file.name}: не хватает поля '{field}' в frontmatter")
        datetime.date.fromisoformat(meta["date"])  # валидация формата даты
        slug = md_file.stem
        (blog_dir / f"{slug}.html").write_text(build_post(meta, md_to_html(body), slug), encoding="utf-8")
        posts.append((meta, slug))
        print(f"✓ blog/{slug}.html")

    posts.sort(key=lambda p: p[0]["date"], reverse=True)
    (blog_dir / "index.html").write_text(build_index(posts), encoding="utf-8")
    print("✓ blog/index.html")
    (ROOT / "sitemap.xml").write_text(build_sitemap(posts), encoding="utf-8")
    print("✓ sitemap.xml")
    print(f"\nГотово: {len(posts)} статей. Не забудь задеплоить сайт.")


if __name__ == "__main__":
    main()
