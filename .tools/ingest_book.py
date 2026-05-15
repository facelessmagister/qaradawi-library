#!/usr/bin/env python3
"""
ingest_book.py — Ingest extracted book text into the wiki

Usage:
    python3 ingest_book.py --book halal-haram
    python3 ingest_book.py --book halal-haram --reingest
"""
import argparse
import hashlib
import os
import re
import sys
import yaml
from datetime import datetime

WIKI_ROOT = "/root/qaradawi-library"
CONFIG_PATH = os.path.join(WIKI_ROOT, ".config", "books.yaml")
EXTRACT_DIR = os.path.join(WIKI_ROOT, "raw", "extracted")
ENTITIES_DIR = os.path.join(WIKI_ROOT, "entities")
CONCEPTS_DIR = os.path.join(WIKI_ROOT, "concepts")
INDEX_PATH = os.path.join(WIKI_ROOT, "index.md")
LOG_PATH = os.path.join(WIKI_ROOT, "log.md")
SCHEMA_PATH = os.path.join(WIKI_ROOT, "SCHEMA.md")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(cfg, f, sort_keys=False, allow_unicode=True)


def append_log(action, details):
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## [{today}] {action}\n"
    for k, v in details.items():
        entry += f"- {k}: {v}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)


def slugify(title):
    """Convert a title to a safe filename slug."""
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:80]


def ensure_dir(d):
    os.makedirs(d, exist_ok=True)


def write_page(path, frontmatter, body):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, allow_unicode=True, sort_keys=False)
        f.write("---\n\n")
        f.write(body)


def read_page(path):
    if not os.path.exists(path):
        return None, None
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1])
    except Exception:
        fm = {}
    return fm, parts[2].strip()


def extract_concepts(text, book_tags):
    """
    Extract key concepts from chapter text using keyword heuristics.
    Returns list of concept dicts: {name, arabic, confidence}
    """
    concepts = []
    # Keyword map: concept name -> Arabic, tags
    keyword_map = {
        "zakat": ("زَكَاة", "fiqh-muamalat"),
        "zakah": ("زَكَاة", "fiqh-muamalat"),
        "salah": ("صَلَاة", "fiqh-ibadat"),
        "prayer": ("صَلَاة", "fiqh-ibadat"),
        "sawm": ("صَوْم", "fiqh-ibadat"),
        "fasting": ("صَوْم", "fiqh-ibadat"),
        "hajj": ("حَجّ", "fiqh-ibadat"),
        "pilgrimage": ("حَجّ", "fiqh-ibadat"),
        "nikah": ("نِكَاح", "fiqh-ahwal-shakhsiyyah"),
        "marriage": ("نِكَاح", "fiqh-ahwal-shakhsiyyah"),
        "talaq": ("طَلَاق", "fiqh-ahwal-shakhsiyyah"),
        "divorce": ("طَلَاق", "fiqh-ahwal-shakhsiyyah"),
        "riba": ("رِبَا", "fiqh-muamalat"),
        "usury": ("رِبَا", "fiqh-muamalat"),
        "halal": ("حَلَال", "fiqh-ibadat"),
        "haram": ("حَرَام", "fiqh-ibadat"),
        "taharah": ("طَهَارَة", "fiqh-ibadat"),
        "purity": ("طَهَارَة", "fiqh-ibadat"),
        "jihad": ("جِهَاد", "fiqh-dawah"),
        "dawah": ("دَعْوَة", "fiqh-dawah"),
        "aqeedah": ("عَقِيدَة", "tazkiyah"),
        "creed": ("عَقِيدَة", "tazkiyah"),
        "tawhid": ("تَوْحِيد", "tazkiyah"),
        "sunnah": ("سُنَّة", "hadith-methodology"),
        "ijtihad": ("اجْتِهَاد", "usul-al-fiqh"),
        "qiyas": ("قِيَاس", "usul-al-fiqh"),
        "ijma": ("إِجْمَاع", "usul-al-fiqh"),
        "consensus": ("إِجْمَاع", "usul-al-fiqh"),
        "niyyah": ("نِيَّة", "fiqh-ibadat"),
        "intention": ("نِيَّة", "fiqh-ibadat"),
        "taqwa": ("تَقْوَى", "islamic-ethics"),
        "akhlaq": ("أَخْلَاق", "islamic-ethics"),
        "character": ("أَخْلَاق", "islamic-ethics"),
        "adab": ("أَدَب", "islamic-ethics"),
        "fiqh": ("فِقْه", "usul-al-fiqh"),
        "shariah": ("شَرِيعَة", "usul-al-fiqh"),
        "sharia": ("شَرِيعَة", "usul-al-fiqh"),
        "quran": ("قُرْآن", "tafsir-methodology"),
        "hadith": ("حَدِيث", "hadith-methodology"),
    }

    text_lower = text.lower()
    for keyword, (arabic, tag) in keyword_map.items():
        count = text_lower.count(keyword)
        if count >= 2:  # Appears at least twice
            concepts.append({
                "name": keyword.capitalize() if keyword not in ["quran", "hadith", "sunnah"] else keyword.title(),
                "arabic": arabic,
                "slug": slugify(keyword),
                "tag": tag,
                "frequency": count,
            })

    # Sort by frequency descending
    concepts.sort(key=lambda x: x["frequency"], reverse=True)
    return concepts[:8]  # Top 8 concepts per chapter


def create_book_overview(book, slug, chapter_count):
    """Create the book overview entity page."""
    page_path = os.path.join(ENTITIES_DIR, f"{slug}-overview.md")
    today = datetime.now().strftime("%Y-%m-%d")

    fm = {
        "title": book["title"],
        "created": today,
        "updated": today,
        "type": "book-overview",
        "tags": book.get("tags", ["fiqh-ibadat"]),
        "sources": [f"raw/extracted/{slug}/metadata.yaml"],
        "book": slug,
        "arabic_title": book.get("arabic_title", ""),
        "domain": book.get("domain", "fiqh-ibadat"),
        "chapter_count": chapter_count,
    }

    body = f"""# {book['title']}

**Arabic:** {book.get('arabic_title', 'N/A')}
**Domain:** {book.get('domain', 'fiqh-ibadat')}
**Chapters:** {chapter_count}
**Archive.org:** [{book['archive_id']}]({book['archive_url']})

## Overview

This book by Dr. Yusuf al-Qaradawi addresses {book.get('domain', 'Islamic jurisprudence')}.

## Chapter Index

"""
    for i in range(1, chapter_count + 1):
        body += f"- [[{slug}-ch-{i:02d}|Chapter {i}]]\n"

    body += f"""
## Key Concepts Covered

"""
    # Concepts will be populated after chapters are processed
    body += "_See individual chapter pages for concept listings._\n\n"

    body += f"""## Related Books

See [[concepts-index|Concepts Index]] for thematic cross-references across all Qaradawi books.

## Source
- Raw extraction: `raw/extracted/{slug}/`
- PDF: `raw/pdfs/{slug}.pdf`
"""

    write_page(page_path, fm, body)
    return page_path


def create_chapter_page(book, slug, ch_num, ch_text, ch_title, concepts, total_chapters):
    """Create a chapter entity page."""
    page_path = os.path.join(ENTITIES_DIR, f"{slug}-ch-{ch_num:02d}.md")
    today = datetime.now().strftime("%Y-%m-%d")

    # Build wikilinks to related pages
    links = []
    # Link to book overview
    links.append(f"[[{slug}-overview|Book Overview]]")
    # Link to prev/next chapter if they exist
    if ch_num > 1:
        links.append(f"[[{slug}-ch-{ch_num-1:02d}|← Chapter {ch_num-1}]]")
    if ch_num < total_chapters:
        links.append(f"[[{slug}-ch-{ch_num+1:02d}|Chapter {ch_num+1} →]]")
    # Link to concept pages
    for c in concepts[:5]:
        links.append(f"[[concept-{c['slug']}|{c['name']} ({c['arabic']})]]")

    # Deduplicate
    seen = set()
    unique_links = []
    for l in links:
        core = l.split("|")[0].strip("[]")
        if core not in seen:
            seen.add(core)
            unique_links.append(l)

    fm = {
        "title": ch_title or f"Chapter {ch_num}",
        "created": today,
        "updated": today,
        "type": "chapter",
        "tags": book.get("tags", ["fiqh-ibadat"]),
        "sources": [f"raw/extracted/{slug}/ch-{ch_num:02d}.txt"],
        "book": slug,
        "chapter": ch_num,
        "confidence": "medium",
    }

    # Extract key lines (first 20 non-empty lines as preview)
    preview_lines = []
    for line in ch_text.split("\n")[:40]:
        stripped = line.strip()
        if stripped and len(stripped) > 20:
            preview_lines.append(stripped)
        if len(preview_lines) >= 10:
            break
    preview = "\n".join(preview_lines)

    body = f"""# {ch_title or f'Chapter {ch_num}'}

**Book:** [[{slug}-overview|{book['title']}]]
**Chapter:** {ch_num} of {total_chapters}

## Chapter Links
"""
    for l in unique_links:
        body += f"- {l}\n"

    body += f"""
## Key Concepts

| Concept | Arabic | Frequency |
|---------|--------|-----------|
"""
    for c in concepts[:8]:
        body += f"| [[concept-{c['slug']}|{c['name']}]] | {c['arabic']} | {c['frequency']} |\n"

    body += f"""
## Preview

```
{preview[:800]}
```

## Full Source
See `raw/extracted/{slug}/ch-{ch_num:02d}.txt` for complete text.

---

*Extracted from {book['title']} — Chapter {ch_num}*
"""

    write_page(page_path, fm, body)
    return page_path


def create_or_update_concept(concept, book, slug, ch_num):
    """Create or update a concept page."""
    page_path = os.path.join(CONCEPTS_DIR, f"concept-{concept['slug']}.md")
    today = datetime.now().strftime("%Y-%m-%d")

    existing_fm, existing_body = read_page(page_path)

    if existing_body is None:
        # Create new concept page
        fm = {
            "title": f"{concept['name']} ({concept['arabic']})",
            "created": today,
            "updated": today,
            "type": "concept",
            "tags": [concept["tag"]],
            "sources": [f"raw/extracted/{slug}/ch-{ch_num:02d}.txt"],
            "confidence": "low",
        }

        body = f"""# {concept['name']} ({concept['arabic']})

**Arabic:** {concept['arabic']}
**Domain:** {concept['tag'].replace('-', ' ').title()}

## Definition

*Definition pending full extraction from multiple sources.*

## Qaradawi's Treatment

- [[{slug}-ch-{ch_num:02d}|{book['title']} — Chapter {ch_num}]]

## Related Concepts

*Links to related concepts will be added as corpus grows.*

## Classical Scholarly Context

*Comparison with classical madhhab positions pending.*

---

*Concept extracted from {book['title']}. Page will expand as more books are ingested.*
"""
        write_page(page_path, fm, body)
        return "created"
    else:
        # Update existing concept page
        existing_fm = existing_fm or {}
        existing_fm["updated"] = today
        sources = existing_fm.get("sources", [])
        new_source = f"raw/extracted/{slug}/ch-{ch_num:02d}.txt"
        if new_source not in sources:
            sources.append(new_source)
        existing_fm["sources"] = sources

        # Add Qaradawi treatment link if not present
        new_link = f"- [[{slug}-ch-{ch_num:02d}|{book['title']} — Chapter {ch_num}]]"
        if new_link not in existing_body:
            # Insert before "Related Concepts" or at the end
            if "## Related Concepts" in existing_body:
                existing_body = existing_body.replace(
                    "## Related Concepts",
                    f"## Qaradawi's Treatment\n\n{new_link}\n\n## Related Concepts"
                )
            else:
                existing_body += f"\n\n## Qaradawi's Treatment\n\n{new_link}\n"

        write_page(page_path, existing_fm, existing_body)
        return "updated"


def update_index(cfg, new_pages):
    """Append new entries to index.md without overwriting the whole file."""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index_content = f.read()

    today = datetime.now().strftime("%Y-%m-%d")
    total_pages = len([
        f for root, dirs, files in os.walk(WIKI_ROOT)
        for f in files if f.endswith(".md") and not f.startswith(".")
        and "raw" not in root and ".tools" not in root and ".config" not in root
    ])

    # Update header
    index_content = re.sub(
        r"Last updated: \d{4}-\d{2}-\d{2} \| Total pages: \d+",
        f"Last updated: {today} | Total pages: {total_pages}",
        index_content,
    )

    # For each new page, insert into the appropriate section
    # This is a simplified approach — in production, we parse sections more carefully
    for page_info in new_pages:
        section = page_info.get("section", "Entities")
        line = page_info.get("line", "")

        # Find the section header and insert after it
        pattern = rf"(## {section}\n)"
        if re.search(pattern, index_content):
            index_content = re.sub(
                pattern,
                rf"\1{line}\n",
                index_content,
                count=1,
            )
        else:
            # Section doesn't exist, append at end
            index_content += f"\n{line}\n"

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(index_content)


def ingest_book(slug, cfg_data, force=False):
    books = cfg_data.get("books", {})
    if slug not in books:
        print(f"ERROR: Book '{slug}' not found in registry")
        return False

    book = books[slug]
    if not book.get("extracted"):
        print(f"ERROR: Book '{slug}' not extracted. Run extract_book.py first.")
        return False
    if book.get("ingested") and not force:
        print(f"Book '{slug}' already ingested. Use --reingest to force.")
        return True

    extract_path = os.path.join(EXTRACT_DIR, slug)
    if not os.path.exists(extract_path):
        print(f"ERROR: Extraction path not found: {extract_path}")
        return False

    print(f"Ingesting: {book['title']}")

    # Find all chapter files
    chapter_files = sorted([
        f for f in os.listdir(extract_path)
        if f.startswith("ch-") and f.endswith(".txt")
    ])

    if not chapter_files:
        print("ERROR: No chapter files found")
        return False

    total_chapters = len(chapter_files)
    pages_created = []
    concepts_created = 0
    concepts_updated = 0

    # Create book overview
    overview_path = create_book_overview(book, slug, total_chapters)
    pages_created.append({
        "path": overview_path,
        "section": "Books (Overview Pages)",
        "line": f"- [[{slug}-overview|{book['title']}]] — {book.get('domain', 'fiqh')}",
    })

    # Process each chapter
    for ch_file in chapter_files:
        ch_num = int(ch_file.split("-")[1].split(".")[0])
        ch_path = os.path.join(extract_path, ch_file)

        with open(ch_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                ch_text = parts[2].strip()
                ch_fm = yaml.safe_load(parts[1]) if len(parts) > 1 else {}
            else:
                ch_text = content
                ch_fm = {}
        else:
            ch_text = content
            ch_fm = {}

        ch_title = ch_fm.get("title", f"Chapter {ch_num}")

        # Extract concepts
        concepts = extract_concepts(ch_text, book.get("tags", []))

        # Create chapter page
        ch_page_path = create_chapter_page(book, slug, ch_num, ch_text, ch_title, concepts, total_chapters)
        pages_created.append({
            "path": ch_page_path,
            "section": "Chapters (Entity Pages)",
            "line": f"- [[{slug}-ch-{ch_num:02d}|Chapter {ch_num}: {ch_title}]]",
        })

        # Create/update concept pages
        for concept in concepts:
            result = create_or_update_concept(concept, book, slug, ch_num)
            if result == "created":
                concepts_created += 1
                pages_created.append({
                    "path": os.path.join(CONCEPTS_DIR, f"concept-{concept['slug']}.md"),
                    "section": "Concepts",
                    "line": f"- [[concept-{concept['slug']}|{concept['name']} ({concept['arabic']})]] — {concept['tag']}",
                })
            else:
                concepts_updated += 1

    # Update index
    update_index(cfg_data, pages_created)

    # Update config
    book["ingested"] = True
    book["ingested_at"] = datetime.now().strftime("%Y-%m-%d")
    book["pages_created"] = len(pages_created)
    save_config(cfg_data)

    append_log("ingest", {
        "book": book["title"],
        "slug": slug,
        "chapters": total_chapters,
        "chapter_pages": total_chapters,
        "concept_pages_created": concepts_created,
        "concept_pages_updated": concepts_updated,
        "total_pages": len(pages_created),
    })

    print(f"\n{'='*60}")
    print(f"INGEST COMPLETE: {book['title']}")
    print(f"  Chapter pages:      {total_chapters}")
    print(f"  Concept pages created: {concepts_created}")
    print(f"  Concept pages updated: {concepts_updated}")
    print(f"  Total new pages:    {len(pages_created)}")
    print(f"{'='*60}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Ingest extracted Qaradawi books into wiki")
    parser.add_argument("--book", required=True, help="Book slug to ingest")
    parser.add_argument("--reingest", action="store_true", help="Force re-ingestion")
    args = parser.parse_args()

    cfg = load_config()
    ingest_book(args.book, cfg, force=args.reingest)


if __name__ == "__main__":
    main()
