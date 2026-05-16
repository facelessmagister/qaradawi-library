#!/usr/bin/env python3
"""
generate.py — Build the Qaradawi Library e-library static site from the wiki.

Reads wiki markdown, applies the design system, writes complete HTML to dist/.
Python 3 stdlib only. No external dependencies.

Usage:
    python3 generate.py
"""

import os, re, yaml, shutil
from datetime import datetime
from collections import defaultdict

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WEBSITE_DIR = os.path.dirname(SCRIPT_DIR)
WIKI_ROOT = os.path.dirname(WEBSITE_DIR)
DIST_DIR = os.path.join(WEBSITE_DIR, "dist")
ENTITIES_DIR = os.path.join(WIKI_ROOT, "entities")
CONCEPTS_DIR = os.path.join(WIKI_ROOT, "concepts")
CONFIG_PATH = os.path.join(WIKI_ROOT, ".config", "books.yaml")
RAW_EXTRACTED = os.path.join(WIKI_ROOT, "raw", "extracted")
CSS_SRC = os.path.join(SCRIPT_DIR, "style.css")
CSS_DST = os.path.join(DIST_DIR, "style.css")

# ── Domain metadata ──
DOMAIN_LABELS = {
    "fiqh-ibadat": "Ibadah / Worship",
    "fiqh-muamalat": "Mu'amalat / Transactions",
    "fiqh-ahwal-shakhsiyyah": "Ahwal Shakhsiyyah / Family",
    "fiqh-dawah": "Da'wah",
    "usul-al-fiqh": "Usul al-Fiqh",
    "hadith-methodology": "Hadith Methodology",
    "islamic-ethics": "Islamic Ethics",
    "islamic-education": "Islamic Education",
    "tazkiyah": "Tazkiyah / Spirituality",
}

DOMAIN_SORT = [
    "fiqh-ibadat", "fiqh-muamalat", "fiqh-ahwal-shakhsiyyah",
    "tazkiyah", "islamic-ethics", "usul-al-fiqh", "hadith-methodology",
    "fiqh-dawah", "islamic-education",
]

# ── Nav bar ──
NAV_HTML = """<nav class="site-nav">
  <div class="nav-inner">
    <a href="/" class="nav-brand">Qaradawi Library<span>مكتبة</span></a>
    <button class="nav-toggle" onclick="this.nextElementSibling.classList.toggle('open')" aria-label="Menu">☰</button>
    <div class="nav-links">
      <a href="/">Library</a>
      <a href="/books/">Books</a>
      <a href="/topics/">Topics</a>
    </div>
  </div>
</nav>"""

FOOTER_HTML = """<footer class="site-footer">
  <p><strong>Qaradawi Library</strong> — قَرَضَاوِيّ مَكْتَبَة</p>
  <p>The scholarly works of the late Prof. Dr. Yusuf al-Qaradawi (1926–2022)</p>
  <p style="margin-top: 8px; font-size: 0.75rem;">
    Built with ❤️ · 
    <a href="https://github.com/facelessmagister/qaradawi-library">GitHub</a>
  </p>
</footer>"""


def parse_frontmatter(text):
    """Return (frontmatter_dict, body_str) from a markdown file."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except:
        fm = {}
    return fm, parts[2].strip()


def resolve_wikilinks(body, book_slug=None):
    """Convert [[slug|Label]] wikilinks to proper <a> HTML links.

    Rules (order matters):
    - [[xxx-overview|...]]  → /books/{book}/
    - [[xxx-ch-NN|...]]     → /books/{book}/ch-{N}/
    - [[concept-xxx|...]]   → /topics/xxx/
    - [[concepts-index]]    → /topics/
    - [[xxx]] (fallback)    → try pattern match
    """

    def replace_wikilink(m):
        target = m.group(1)
        label = m.group(2) if m.group(2) else target

        # concept-xxx → /topics/xxx/
        if target.startswith("concept-"):
            slug = target.replace("concept-", "")
            return f'<a href="/topics/{slug}/" class="topic-pill">{label}</a>'

        # concepts-index → /topics/
        if target == "concepts-index":
            return f'<a href="/topics/">{label}</a>'

        # xxx-overview → /books/{book}/
        over_match = re.match(r"(.+)-overview$", target)
        if over_match:
            b = over_match.group(1)
            return f'<a href="/books/{b}/">{label}</a>'

        # xxx-ch-NN → /books/{book}/ch-{N}/
        ch_match = re.match(r"(.+)-ch-(\d+)$", target)
        if ch_match:
            b = ch_match.group(1)
            n = int(ch_match.group(2))
            return f'<a href="/books/{b}/ch-{n}/">{label}</a>'

        # fallback: plain text
        return label

    # Handle [[target|label]] and [[target]]
    pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
    return re.sub(pattern, replace_wikilink, body)


def html_page(title, body_html, description="", extra_head=""):
    """Wrap content in the full HTML shell."""
    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="/style.css">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Inter:wght@400;500;600&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap" rel="stylesheet">
  <meta name="description" content="{description}">
  {extra_head}
</head>
<body>
{NAV_HTML}
{body_html}
{FOOTER_HTML}
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════
#  PAGE GENERATORS
# ═══════════════════════════════════════════════════════════════

def generate_library_home(books_cfg):
    """dist/index.html — Library home with book grid."""
    books = books_cfg.get("books", {})
    ingested_books = {k: v for k, v in books.items() if v.get("ingested")}
    all_books = {k: v for k, v in books.items()}

    # Stats
    total_books = len(all_books)
    total_ingested = len(ingested_books)
    total_chapters = sum(v.get("chapters", 0) or 0 for v in ingested_books.values())

    # Count concepts
    concept_count = len([f for f in os.listdir(CONCEPTS_DIR) if f.startswith("concept-") and f.endswith(".md")])

    stats_html = f"""<div class="hero-stats">
  <div class="stat-item"><div class="stat-num">{total_ingested}</div><div class="stat-label">Books Published</div></div>
  <div class="stat-item"><div class="stat-num">{total_chapters}</div><div class="stat-label">Chapters</div></div>
  <div class="stat-item"><div class="stat-num">{concept_count}</div><div class="stat-label">Topics</div></div>
  <div class="stat-item"><div class="stat-num">{total_books - total_ingested}</div><div class="stat-label">Coming Soon</div></div>
</div>"""

    hero_html = f"""<header class="hero-library">
  <h1>Qaradawi Library</h1>
  <div class="arabic-title">قَرَضَاوِيّ مَكْتَبَة</div>
  <p class="subtitle">The complete scholarly works of the late Prof. Dr. Yusuf al-Qaradawi (1926–2022), presented as a searchable e-library with per-book, per-chapter, and per-topic navigation.</p>
  {stats_html}
</header>"""

    # Build book cards — ingested first, then coming soon
    cards = []

    for slug in sorted(ingested_books.keys(), key=lambda s: ingested_books[s].get("priority", 3)):
        b = ingested_books[slug]
        domain = b.get("domain", "fiqh-ibadat")
        domain_label = DOMAIN_LABELS.get(domain, domain)
        cards.append(f"""  <a href="/books/{slug}/" class="book-card">
    <div class="card-domain">{domain_label}</div>
    <div class="card-arabic">{b.get('arabic_title', '')}</div>
    <h3>{b['title']}</h3>
    <div class="card-meta"><strong>{b.get('chapters', '?')} chapters</strong> · {b.get('notes', '')[:80]}</div>
  </a>""")

    for slug in sorted(set(all_books.keys()) - set(ingested_books.keys())):
        b = all_books[slug]
        domain = b.get("domain", "fiqh-ibadat")
        domain_label = DOMAIN_LABELS.get(domain, domain)
        cards.append(f"""  <div class="book-card coming-soon">
    <div class="card-domain">{domain_label}</div>
    <div class="card-arabic">{b.get('arabic_title', '')}</div>
    <h3>{b['title']}</h3>
    <div class="card-meta">Coming soon</div>
  </div>""")

    body = f"""{hero_html}
<main class="content">
  <div class="section-header">
    <h2 class="section-title">All Books</h2>
    <p class="section-subtitle">{total_ingested} of {total_books} books ingested and published</p>
  </div>
  <div class="book-grid">
{chr(10).join(cards)}
  </div>
</main>"""

    desc = f"Complete scholarly works of Dr. Yusuf al-Qaradawi — {total_ingested} books, {total_chapters} chapters, {concept_count} topics."
    return html_page("Qaradawi Library", body, desc)


def generate_books_index(books_cfg):
    """dist/books/index.html — All books listing (alternative view)."""
    books = books_cfg.get("books", {})
    ingested_books = {k: v for k, v in books.items() if v.get("ingested")}
    all_books = {k: v for k, v in books.items()}

    breadcrumb = """<div class="breadcrumb"><a href="/">Library</a><span>›</span>Books</div>"""

    cards = []
    for slug in sorted(ingested_books.keys(), key=lambda s: ingested_books[s].get("priority", 3)):
        b = ingested_books[slug]
        domain = b.get("domain", "fiqh-ibadat")
        domain_label = DOMAIN_LABELS.get(domain, domain)
        cards.append(f"""  <a href="/books/{slug}/" class="book-card">
    <div class="card-domain">{domain_label}</div>
    <div class="card-arabic">{b.get('arabic_title', '')}</div>
    <h3>{b['title']}</h3>
    <div class="card-meta"><strong>{b.get('chapters', '?')} chapters</strong></div>
  </a>""")

    # Coming soon
    for slug in sorted(set(all_books.keys()) - set(ingested_books.keys())):
        b = all_books[slug]
        domain = b.get("domain", "fiqh-ibadat")
        domain_label = DOMAIN_LABELS.get(domain, domain)
        cards.append(f"""  <div class="book-card coming-soon">
    <div class="card-domain">{domain_label}</div>
    <div class="card-arabic">{b.get('arabic_title', '')}</div>
    <h3>{b['title']}</h3>
    <div class="card-meta">Coming soon</div>
  </div>""")

    body = f"""{breadcrumb}
<main class="content">
  <div class="section-header">
    <h2 class="section-title">All Books</h2>
    <p class="section-subtitle">{len(ingested_books)} published · {len(all_books) - len(ingested_books)} coming soon</p>
  </div>
  <div class="book-grid">
{chr(10).join(cards)}
  </div>
</main>"""

    return html_page("Books — Qaradawi Library", body, "Browse all books in the Qaradawi Library")


def generate_book_page(slug, book, chapters_info, all_concepts_mentioned):
    """dist/books/{slug}/index.html — Single book overview page."""
    breadcrumb = f"""<div class="breadcrumb"><a href="/">Library</a><span>›</span><a href="/books/">Books</a><span>›</span>{book['title']}</div>"""

    domain = book.get("domain", "fiqh-ibadat")
    domain_label = DOMAIN_LABELS.get(domain, domain)

    hero = f"""<header class="hero-book">
  <div class="domain-badge">{domain_label}</div>
  <h1>{book['title']}</h1>
  <div class="arabic-title">{book.get('arabic_title', '')}</div>
  <div class="hero-book-meta">
    <span>✍️ <strong>Dr. Yusuf al-Qaradawi</strong></span>
    <span>📖 {book.get('chapters', '?')} chapters</span>
    <span>🏷️ {domain_label}</span>
  </div>
</header>"""

    # Chapter list
    chapter_rows = []
    for ch in chapters_info:
        rows = f"""  <a href="/books/{slug}/ch-{ch['num']}/" class="chapter-row">
    <span class="ch-num">{ch['num']}</span>
    <span class="ch-title">{ch.get('title', f'Chapter {ch["num"]}')}</span>
    <span class="ch-arrow">→</span>
  </a>"""
        chapter_rows.append(rows)

    # Concepts
    concept_pills = ""
    if all_concepts_mentioned:
        pills = []
        for c in sorted(all_concepts_mentioned):
            pills.append(f'<a href="/topics/{c}/" class="topic-pill">{c.replace("-", " ").title()}</a>')
        concept_pills = f"""<div class="section">
  <h2 class="section-title">Topics Covered</h2>
  <div class="topic-pills">{chr(10).join(pills)}</div>
</div>"""

    body = f"""{breadcrumb}
{hero}
<main class="content">
  <div class="section">
    <h2 class="section-title">Chapters</h2>
  </div>
  <div class="chapter-list">
{chr(10).join(chapter_rows)}
  </div>
  {concept_pills}
</main>"""

    desc = f"{book['title']} by Dr. Yusuf al-Qaradawi — {book.get('chapters','?')} chapters on {domain_label}"
    return html_page(f"{book['title']} — Qaradawi Library", body, desc)


def generate_simple_chapter_page(slug, ch_num, book, ch_title, concepts, raw_text):
    """Generate a chapter page with preview text (for non-Faith-and-Life books)."""
    breadcrumb = f"""<div class="breadcrumb"><a href="/">Library</a><span>›</span><a href="/books/{slug}/">{book['title']}</a><span>›</span>Chapter {ch_num}</div>"""

    # Extract preview: first 30 non-empty lines > 20 chars
    preview_lines = []
    for line in raw_text.split("\n")[:60]:
        s = line.strip()
        if s and len(s) > 20:
            preview_lines.append(s)
        if len(preview_lines) >= 15:
            break
    preview = "\n".join(preview_lines)[:1200]

    # Concept pills
    pill_html = ""
    if concepts:
        pills = []
        for c in concepts[:8]:
            pills.append(f'<a href="/topics/{c["slug"]}/" class="topic-pill">{c["name"]}</a>')
        pill_html = f"""<div class="topic-pills">{chr(10).join(pills)}</div>"""

    # Chapter nav
    prev_link = ""
    next_link = ""
    if ch_num > 1:
        prev_link = f'<a href="/books/{slug}/ch-{ch_num-1}/">← Chapter {ch_num-1}</a>'
    total = book.get("chapters", 1) or 1
    if ch_num < total:
        next_link = f'<a href="/books/{slug}/ch-{ch_num+1}/">Chapter {ch_num+1} →</a>'

    chapter_nav = f"""<div class="chapter-nav">
  <span>{prev_link}</span>
  <a href="/books/{slug}/">↑ Book Overview</a>
  <span>{next_link}</span>
</div>"""

    body = f"""{breadcrumb}
<main class="content">
  <div class="section-header">
    <h2 class="section-title">Chapter {ch_num}: {ch_title}</h2>
    <p class="section-subtitle">From <a href="/books/{slug}/">{book['title']}</a></p>
  </div>
  {pill_html}
  {chapter_nav}
  <div class="section">
    <h3 class="section-title" style="font-size:1.2rem;">Text Preview</h3>
    <div class="preview-block">{preview}</div>
    <p style="font-size:0.82rem; color:var(--text-light); margin-top:8px;">
      Full text available in the source PDF. Deeper formatting coming in Phase 2.
    </p>
  </div>
  {chapter_nav}
</main>"""

    desc = f"Chapter {ch_num}: {ch_title} — {book['title']} by Dr. Yusuf al-Qaradawi"
    return html_page(f"Chapter {ch_num}: {ch_title} — Qaradawi Library", body, desc)


def generate_topics_index():
    """dist/topics/index.html — All concept topics grouped by domain."""
    concepts = []
    for fname in sorted(os.listdir(CONCEPTS_DIR)):
        if fname.startswith("concept-") and fname.endswith(".md"):
            with open(os.path.join(CONCEPTS_DIR, fname), "r") as f:
                content = f.read()
            fm, body = parse_frontmatter(content)
            slug = fname.replace("concept-", "").replace(".md", "")
            concepts.append({
                "slug": slug,
                "title": fm.get("title", slug.replace("-", " ").title()),
                "tags": fm.get("tags", []),
            })

    # Group by domain
    by_domain = defaultdict(list)
    for c in concepts:
        tag = c["tags"][0] if c["tags"] else "general"
        by_domain[tag].append(c)

    breadcrumb = """<div class="breadcrumb"><a href="/">Library</a><span>›</span>Topics</div>"""

    domain_sections = []
    for domain in DOMAIN_SORT:
        items = by_domain.get(domain, [])
        if not items:
            continue
        pills = []
        for c in items:
            pills.append(f'<a href="/topics/{c["slug"]}/" class="topic-pill">{c["title"]}</a>')
        domain_label = DOMAIN_LABELS.get(domain, domain)
        domain_sections.append(f"""<div class="domain-group">
  <h3>{domain_label}</h3>
  <div class="topic-pills">{chr(10).join(pills)}</div>
</div>""")

    body = f"""{breadcrumb}
<main class="content">
  <div class="section-header">
    <h2 class="section-title">All Topics</h2>
    <p class="section-subtitle">{len(concepts)} concepts extracted across all books</p>
  </div>
{chr(10).join(domain_sections)}
</main>"""

    return html_page("Topics — Qaradawi Library", body, f"{len(concepts)} scholarly concepts from Dr. al-Qaradawi's works")


def generate_topic_page(slug, concept_data, linked_chapters):
    """dist/topics/{slug}/index.html — Topic hub page."""
    fm, body = concept_data
    title = fm.get("title", slug.replace("-", " ").title())
    tags = fm.get("tags", [])
    domain = tags[0] if tags else "general"
    domain_label = DOMAIN_LABELS.get(domain, domain)

    breadcrumb = f"""<div class="breadcrumb"><a href="/">Library</a><span>›</span><a href="/topics/">Topics</a><span>›</span>{title}</div>"""

    # Group linked chapters by book
    by_book = defaultdict(list)
    for book_slug, ch_num, ch_title in linked_chapters:
        by_book[book_slug].append((ch_num, ch_title))

    chapter_html_parts = []
    for book_slug in sorted(by_book.keys()):
        ch_list = by_book[book_slug]
        items = []
        for ch_num, ch_title in ch_list:
            items.append(f'<li><a href="/books/{book_slug}/ch-{ch_num}/">Chapter {ch_num}: {ch_title}</a></li>')
        chapter_html_parts.append(f"""<div class="domain-group">
  <h3><a href="/books/{book_slug}/" style="color:inherit;text-decoration:none;">📖 {book_slug.replace('-', ' ').title()}</a></h3>
  <ul style="list-style:none; padding-left:16px;">
{chr(10).join(items)}
  </ul>
</div>""")

    chapters_html = chr(10).join(chapter_html_parts) if chapter_html_parts else "<p style='color:var(--text-muted);'>No chapters linked yet.</p>"

    body = f"""{breadcrumb}
<main class="content">
  <div class="section-header">
    <h2 class="section-title">{title}</h2>
    <p class="section-subtitle"><span class="topic-pill" style="font-size:0.75rem;">{domain_label}</span></p>
  </div>
  <div class="section">
    <h3 class="section-title" style="font-size:1.1rem;">Appears In</h3>
    {chapters_html}
  </div>
</main>"""

    desc = f"{title} — Scholarly concept from Dr. Yusuf al-Qaradawi's works"
    return html_page(f"{title} — Qaradawi Library", body, desc)


def extract_concepts_from_text(text, book_tags):
    """Extract key concepts from chapter text using keyword heuristics."""
    keyword_map = {
        "zakat": ("زَكَاة", "fiqh-muamalat"), "zakah": ("زَكَاة", "fiqh-muamalat"),
        "salah": ("صَلَاة", "fiqh-ibadat"), "prayer": ("صَلَاة", "fiqh-ibadat"),
        "sawm": ("صَوْم", "fiqh-ibadat"), "fasting": ("صَوْم", "fiqh-ibadat"),
        "hajj": ("حَجّ", "fiqh-ibadat"), "pilgrimage": ("حَجّ", "fiqh-ibadat"),
        "nikah": ("نِكَاح", "fiqh-ahwal-shakhsiyyah"), "marriage": ("نِكَاح", "fiqh-ahwal-shakhsiyyah"),
        "talaq": ("طَلَاق", "fiqh-ahwal-shakhsiyyah"), "divorce": ("طَلَاق", "fiqh-ahwal-shakhsiyyah"),
        "riba": ("رِبَا", "fiqh-muamalat"), "usury": ("رِبَا", "fiqh-muamalat"),
        "halal": ("حَلَال", "fiqh-ibadat"), "haram": ("حَرَام", "fiqh-ibadat"),
        "taharah": ("طَهَارَة", "fiqh-ibadat"), "purity": ("طَهَارَة", "fiqh-ibadat"),
        "jihad": ("جِهَاد", "fiqh-dawah"), "dawah": ("دَعْوَة", "fiqh-dawah"),
        "aqeedah": ("عَقِيدَة", "tazkiyah"), "creed": ("عَقِيدَة", "tazkiyah"),
        "tawhid": ("تَوْحِيد", "tazkiyah"), "sunnah": ("سُنَّة", "hadith-methodology"),
        "ijtihad": ("اجْتِهَاد", "usul-al-fiqh"), "qiyas": ("قِيَاس", "usul-al-fiqh"),
        "ijma": ("إِجْمَاع", "usul-al-fiqh"), "consensus": ("إِجْمَاع", "usul-al-fiqh"),
        "niyyah": ("نِيَّة", "fiqh-ibadat"), "intention": ("نِيَّة", "fiqh-ibadat"),
        "taqwa": ("تَقْوَى", "islamic-ethics"), "akhlaq": ("أَخْلَاق", "islamic-ethics"),
        "character": ("أَخْلَاق", "islamic-ethics"), "adab": ("أَدَب", "islamic-ethics"),
        "fiqh": ("فِقْه", "usul-al-fiqh"), "shariah": ("شَرِيعَة", "usul-al-fiqh"),
        "sharia": ("شَرِيعَة", "usul-al-fiqh"), "quran": ("قُرْآن", "tafsir-methodology"),
        "hadith": ("حَدِيث", "hadith-methodology"),
        "iman": ("إِيمَان", "tazkiyah"),
    }
    text_lower = text.lower()
    concepts = []
    for keyword, (arabic, tag) in keyword_map.items():
        count = text_lower.count(keyword)
        if count >= 2:
            s = re.sub(r"[^\w]", "", keyword.lower())
            concepts.append({"name": keyword.capitalize(), "arabic": arabic, "slug": s, "tag": tag, "frequency": count})
    concepts.sort(key=lambda x: x["frequency"], reverse=True)
    return concepts[:8]


# ═══════════════════════════════════════════════════════════════
#  FAITH AND LIFE — FULL CHAPTER FORMATTING
# ═══════════════════════════════════════════════════════════════

FAITH_AND_LIFE_CHAPTER_TITLES = {
    1: "Iman and the Dignity of Man",
    2: "Iman and Happiness",
    3: "Iman and Love",
    4: "Iman and Hope",
}

FAITH_AND_LIFE_ARABIC = {
    1: "الإيمان وكرامة الإنسان",
    2: "الإيمان والسعادة",
    3: "الإيمان والحب",
    4: "الإيمان والأمل",
}

def generate_faith_and_life_chapter(ch_num, book):
    """Generate a richly formatted chapter page for Faith and Life (full text)."""

    ch_path = os.path.join(RAW_EXTRACTED, "faith-and-life", f"ch-{ch_num:02d}.txt")
    if not os.path.exists(ch_path):
        return None

    with open(ch_path, "r") as f:
        content = f.read()

    fm, raw_text = parse_frontmatter(content)
    ch_title = FAITH_AND_LIFE_CHAPTER_TITLES.get(ch_num, fm.get("title", f"Chapter {ch_num}"))
    arabic = FAITH_AND_LIFE_ARABIC.get(ch_num, "")

    concepts = extract_concepts_from_text(raw_text, book.get("tags", []))

    # ── 1. Parse raw text into clean paragraphs ──
    lines = raw_text.splitlines()
    cleaned = []
    for line in lines:
        s = line.strip()
        if s.startswith("\f") or re.match(r"^\d+\s+Faith and Life\s*$", s) or s == "Faith and Life":
            continue
        cleaned.append(s)

    blank_groups = []
    buf = []
    for line in cleaned:
        if line == '':
            if buf:
                blank_groups.append(buf)
                buf = []
        else:
            buf.append(line)
    if buf:
        blank_groups.append(buf)

    # Split groups at internal section titles (e.g. "Man in the sight of materialists")
    def _is_section_title(line):
        return (
            10 <= len(line) <= 70
            and not re.search(r'[.!?]$', line)
            and line[0].isupper()
            and ' ' in line
            and re.search(r'\b(Man|Islam|Iman|Allah|Faith|Belief|Life|Human|Humanity|Spirit|Soul|Angels|Quran|Shariah|Sunnah|Worship|Jihad|Creation|Nature|Goal|Position|Honor|Dignity|Freedom|Death|Resurrection|Afterlife)\b', line)
        )

    final_groups = []
    for group in blank_groups:
        split_at = []
        for i, line in enumerate(group):
            if i > 0 and _is_section_title(line):
                split_at.append(i)
        if not split_at:
            final_groups.append(group)
        else:
            prev = 0
            for idx in split_at:
                final_groups.append(group[prev:idx])
                prev = idx
            final_groups.append(group[prev:])
    blank_groups = final_groups

    paragraphs = []
    for group in blank_groups:
        def looks_like_title(line):
            return 8 <= len(line) <= 70 and line and line[0].isupper() and ' ' in line and not re.search(r'[.!?]$', line)
        all_titles = all(looks_like_title(l) for l in group)
        if all_titles and len(group) > 1:
            for l in group:
                paragraphs.append(l.strip())
        else:
            paragraphs.append(' '.join(l.strip() for l in group))

    # ── 2. Extract outline from first paragraphs ──
    outline = []
    body_start = 0
    for i, p in enumerate(paragraphs):
        if not p or len(p) > 75:
            break
        if i > 20:
            break
        if re.match(r'^(Iman\s*\(Faith\)|Faith and Life)', p, re.I):
            continue
        if len(p) >= 8 and not re.search(r'[.!?]$', p):
            outline.append(p)
            body_start = i + 1

    # ── 3. Classify remaining paragraphs ──
    tagged = []
    body_started = False
    title_keywords = {'man', 'allah', 'islam', 'iman', 'human', 'faith', 'divine', 'prophet', 'soul', 'spirit', 'quran', 'angels', 'position', 'nature', 'goal', 'sight', 'believers', 'materialists', 'scholars', 'honor', 'sunnah', 'shariah', 'worship', 'jihad', 'life', 'world', 'creation'}

    for p in paragraphs[body_start:]:
        if not p or len(p) < 4:
            continue

        looks_like_title = (
            10 < len(p) < 85
            and not re.search(r'[.!?]$', p)
            and ' ' in p
            and p[0].isupper()
            and body_started
        )
        is_keyword_title = any(k in p.lower() for k in title_keywords)
        if looks_like_title and is_keyword_title:
            tagged.append(('title', p))
            body_started = True
            continue

        body_started = True

        # Verse: guillemets / starts with quote mark / contains (Al-...) ref
        verse_starts = bool(re.match(r'\s*["\u00ab\u2039]', p))
        has_surah_ref = bool(re.search(r'\([A-Z][a-z]+.*\d', p))
        if verse_starts or has_surah_ref:
            tagged.append(('verse', p))
        elif re.search(r'\b(hadith|narrated|prophet.*said|messenger|peace be upon him)\b', p, re.I) and ('"' in p or '"' in p):
            tagged.append(('quote', p))
        else:
            tagged.append(('p', p))

    # ── 4. Build HTML ──
    def _e(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    parts = []
    hero = f'''<header class="hero-book">
  <div class="domain-badge">Chapter {ch_num}</div>
  <h1>{ch_title}</h1>
  <div class="arabic-title">{arabic}</div>
  <p style="margin-top:8px;">From <a href="/books/faith-and-life/" style="color:var(--accent);">Faith and Life</a> by Dr. Yusuf al-Qaradawi</p>
</header>'''

    if outline:
        items_html = chr(10).join(f'    <li>{_e(item)}</li>' for item in outline)
        parts.append(f'''<div class="outline">
  <h3>Chapter Outline</h3>
  <ol>
{items_html}
  </ol>
</div>''')

    for t, p in tagged:
        block = _e(p)
        if t == 'title':
            parts.append(f'<div class="section-header">\n  <h2 class="section-title">{block}</h2>\n</div>')
        elif t == 'verse':
            parts.append(f'<div class="section-verse">\n  <p>{block}</p>\n</div>')
        elif t == 'quote':
            parts.append(f'<blockquote class="quote">\n  <p>{block}</p>\n</blockquote>')
        elif t == 'p':
            parts.append(f'<p>{block}</p>')

    pill_html = ""
    if concepts:
        pills = [f'<a href="/topics/{c["slug"]}/" class="topic-pill">{c["name"]}</a>' for c in concepts]
        pill_html = f'<div class="topic-pills">' + chr(10).join(pills) + '</div>'

    prev_link, next_link = "", ""
    if ch_num > 1:
        prev_link = f'<a href="/books/faith-and-life/ch-{ch_num-1}/">← Chapter {ch_num-1}</a>'
    if ch_num < 4:
        next_link = f'<a href="/books/faith-and-life/ch-{ch_num+1}/">Chapter {ch_num+1} →</a>'
    chapter_nav = f'''<div class="chapter-nav">
  <span>{prev_link}</span>
  <a href="/books/faith-and-life/">↑ Book Overview</a>
  <span>{next_link}</span>
</div>'''

    breadcrumb = f'''<div class="breadcrumb"><a href="/">Library</a><span>›</span><a href="/books/faith-and-life/">Faith and Life</a><span>›</span>Chapter {ch_num}</div>'''

    body = f"""{breadcrumb}
{hero}
<main class="content">
  {pill_html}
  {chapter_nav}
{chr(10).join(parts)}
  {chapter_nav}
</main>"""

    desc = f"Chapter {ch_num}: {ch_title} — Faith and Life by Dr. Yusuf al-Qaradawi"
    return html_page(f"Chapter {ch_num}: {ch_title} — Qaradawi Library", body, desc)



# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("═" * 60)
    print("  Qaradawi Library — Site Generator")
    print("═" * 60)

    # Load book config
    with open(CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f)
    books = cfg.get("books", {})

    # Ensure dist dirs
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "books"), exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "topics"), exist_ok=True)

    # Copy CSS
    shutil.copy2(CSS_SRC, CSS_DST)
    print("\n✓ Copied style.css")

    # ─── 1. Library Home ───
    home_html = generate_library_home(cfg)
    with open(os.path.join(DIST_DIR, "index.html"), "w") as f:
        f.write(home_html)
    print("✓ Generated: /index.html (Library Home)")

    # ─── 2. Books Index ───
    books_index = generate_books_index(cfg)
    with open(os.path.join(DIST_DIR, "books", "index.html"), "w") as f:
        f.write(books_index)
    print("✓ Generated: /books/index.html")

    # ─── 3. Book Pages + Chapters ───
    ingested_books = {k: v for k, v in books.items() if v.get("ingested")}
    total_book_pages = 0
    total_chapter_pages = 0

    for slug, book in sorted(ingested_books.items()):
        book_dir = os.path.join(DIST_DIR, "books", slug)
        os.makedirs(book_dir, exist_ok=True)

        # Find chapter files in entities/
        chapters_info = []
        all_concepts_mentioned = set()

        for fname in sorted(os.listdir(ENTITIES_DIR)):
            if fname.startswith(f"{slug}-ch-") and fname.endswith(".md"):
                with open(os.path.join(ENTITIES_DIR, fname), "r") as f:
                    content = f.read()
                fm, body = parse_frontmatter(content)
                ch_match = re.search(rf"{slug}-ch-(\d+)", fname)
                if ch_match:
                    ch_num = int(ch_match.group(1))
                    ch_title = fm.get("title", f"Chapter {ch_num}")
                    chapters_info.append({"num": ch_num, "title": ch_title})

                    # Collect concepts from wikilinks
                    for m in re.finditer(r"\[\[concept-([^\]]+)\]\]", body):
                        all_concepts_mentioned.add(m.group(1).split("|")[0])

        chapters_info.sort(key=lambda x: x["num"])

        # Generate book overview
        book_html = generate_book_page(slug, book, chapters_info, all_concepts_mentioned)
        with open(os.path.join(book_dir, "index.html"), "w") as f:
            f.write(book_html)
        total_book_pages += 1

        # Generate chapter pages
        if slug == "faith-and-life":
            # FULL formatting for Faith and Life
            for ch_num in range(1, book.get("chapters", 4) + 1):
                ch_html = generate_faith_and_life_chapter(ch_num, book)
                if ch_html:
                    with open(os.path.join(book_dir, f"ch-{ch_num}.html"), "w") as f:
                        f.write(ch_html)
                    total_chapter_pages += 1
                    print(f"  ✓ {slug} / ch-{ch_num} (rich format)")
        else:
            # Simple preview for other books
            for ch in chapters_info:
                # Read raw text for preview
                raw_text = ""
                extract_dir = os.path.join(RAW_EXTRACTED, slug)
                ch_file = os.path.join(extract_dir, f"ch-{ch['num']:02d}.txt")
                if os.path.exists(ch_file):
                    with open(ch_file, "r") as f:
                        ch_content = f.read()
                    _, raw_text = parse_frontmatter(ch_content)

                # Extract concepts
                concepts = extract_concepts_from_text(raw_text, book.get("tags", []))

                ch_html = generate_simple_chapter_page(
                    slug, ch["num"], book, ch["title"], concepts, raw_text
                )
                with open(os.path.join(book_dir, f"ch-{ch['num']}.html"), "w") as f:
                    f.write(ch_html)
                total_chapter_pages += 1

        print(f"✓ {slug}: {len(chapters_info)} chapters")

    print(f"\n  Book pages: {total_book_pages} | Chapter pages: {total_chapter_pages}")

    # ─── 4. Topics Index ───
    topics_index = generate_topics_index()
    with open(os.path.join(DIST_DIR, "topics", "index.html"), "w") as f:
        f.write(topics_index)
    print("✓ Generated: /topics/index.html")

    # ─── 5. Topic Hub Pages ───
    # Build cross-reference: concept_slug → [(book_slug, ch_num, ch_title)]
    cross_ref = defaultdict(list)
    for slug in ingested_books:
        for fname in sorted(os.listdir(ENTITIES_DIR)):
            if fname.startswith(f"{slug}-ch-") and fname.endswith(".md"):
                with open(os.path.join(ENTITIES_DIR, fname), "r") as f:
                    body = f.read()
                ch_match = re.search(rf"{slug}-ch-(\d+)", fname)
                if ch_match:
                    ch_num = int(ch_match.group(1))
                else:
                    continue
                fm, _ = parse_frontmatter(body)
                ch_title = fm.get("title", f"Chapter {ch_num}")
                for m in re.finditer(r"\[\[concept-([^\]|]+)", body):
                    c_slug = m.group(1)
                    cross_ref[c_slug].append((slug, ch_num, ch_title))

    # Load each concept page
    topic_count = 0
    for fname in sorted(os.listdir(CONCEPTS_DIR)):
        if fname.startswith("concept-") and fname.endswith(".md"):
            slug = fname.replace("concept-", "").replace(".md", "")
            with open(os.path.join(CONCEPTS_DIR, fname), "r") as f:
                content = f.read()
            concept_data = parse_frontmatter(content)
            linked = cross_ref.get(slug, [])
            # Deduplicate
            seen = set()
            unique_linked = []
            for b, c, t in linked:
                key = (b, c)
                if key not in seen:
                    seen.add(key)
                    unique_linked.append((b, c, t))

            topic_html = generate_topic_page(slug, concept_data, unique_linked)
            topic_dir = os.path.join(DIST_DIR, "topics", slug)
            os.makedirs(topic_dir, exist_ok=True)
            with open(os.path.join(topic_dir, "index.html"), "w") as f:
                f.write(topic_html)
            topic_count += 1

    print(f"✓ Topic pages: {topic_count}")

    # ─── Summary ───
    total_pages = 1 + 1 + total_book_pages + total_chapter_pages + 1 + topic_count
    print(f"\n{'═' * 60}")
    print(f"  TOTAL PAGES GENERATED: {total_pages}")
    print(f"  Home: 1 | Books index: 1 | Book pages: {total_book_pages}")
    print(f"  Chapters: {total_chapter_pages} | Topics index: 1 | Topic hubs: {topic_count}")
    print(f"{'═' * 60}")


if __name__ == "__main__":
    main()
