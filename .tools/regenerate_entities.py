#!/usr/bin/env python3
"""Regenerate entity pages for re-split books and update overviews/books.yaml."""
import os
import re
import yaml
from datetime import date

WIKI_ROOT = '/root/qaradawi-library'
ENTITIES = f'{WIKI_ROOT}/entities'

today = date.today().isoformat()

# Define the new chapter structures for re-split books
RESELLITS = {
    'diversion-arts': {
        'title': 'Diversion and Arts in Islam',
        'arabic_title': 'اللهو والفنون في الإسلام',
        'domain': 'fiqh-ibadat',
        'chapters': [
            {'num': 1, 'slug': 'ch-01', 'title': 'Islam and Sense of Reality',
             'tags': ['fiqh-ibadat', 'arts', 'entertainment', 'islamic-ethics']},
            {'num': 2, 'slug': 'ch-02', 'title': 'Beauty in the Quran and Universe',
             'tags': ['fiqh-ibadat', 'arts', 'beauty', 'quran']},
            {'num': 3, 'slug': 'ch-03', 'title': 'Expression of Beauty: Poetry and Literature',
             'tags': ['fiqh-ibadat', 'arts', 'poetry', 'literature']},
            {'num': 4, 'slug': 'ch-04', 'title': 'The Judgement of Islam on Singing and Music',
             'tags': ['fiqh-ibadat', 'arts', 'music', 'singing', 'islamic-ruling']},
            {'num': 5, 'slug': 'ch-05', 'title': 'Painting, Picture-Making and Decoration',
             'tags': ['fiqh-ibadat', 'arts', 'painting', 'visual-arts']},
            {'num': 6, 'slug': 'ch-06', 'title': 'Photography',
             'tags': ['fiqh-ibadat', 'arts', 'photography']},
            {'num': 7, 'slug': 'ch-07', 'title': 'Comedy, Humor, Games and Conclusion',
             'tags': ['fiqh-ibadat', 'arts', 'entertainment', 'games', 'humor']},
        ]
    },
    'auspices-victory': {
        'title': 'Auspices of the Ultimate Victory of Islam',
        'arabic_title': 'بشارات النصر المبين',
        'domain': 'fiqh-dawah',
        'chapters': [
            {'num': 1, 'slug': 'ch-01', 'title': 'Prelude',
             'tags': ['fiqh-dawah', 'islamic-movement', 'hope']},
            {'num': 2, 'slug': 'ch-02', 'title': 'Auspices From The Glorious Quran',
             'tags': ['fiqh-dawah', 'quran', 'prophecy']},
            {'num': 3, 'slug': 'ch-03', 'title': 'Auspices From The Sunnah',
             'tags': ['fiqh-dawah', 'sunnah', 'prophecy']},
            {'num': 4, 'slug': 'ch-04', 'title': 'Auspices From History',
             'tags': ['fiqh-dawah', 'history', 'victory']},
            {'num': 5, 'slug': 'ch-05', 'title': 'Auspices From The Actual Time',
             'tags': ['fiqh-dawah', 'contemporary', 'victory']},
            {'num': 6, 'slug': 'ch-06', 'title': 'Auspices From The Divine Laws',
             'tags': ['fiqh-dawah', 'divine-laws', 'sunnah-allah']},
            {'num': 7, 'slug': 'ch-07', 'title': 'A Necessary Pause',
             'tags': ['fiqh-dawah', 'reflection', 'caution']},
            {'num': 8, 'slug': 'ch-08', 'title': 'Light Shed on Misconceived Hadiths',
             'tags': ['fiqh-dawah', 'hadith', 'misconceptions']},
        ]
    },
    'ethics-in-islam': {
        'title': 'Ethics in Islam',
        'arabic_title': 'الأخلاق في الإسلام',
        'domain': 'islamic-ethics',
        'chapters': [
            # Chapter 1 overview (includes introduction + subsections 1.1-1.6)
            {'num': 1, 'slug': 'ch-01', 'title': 'Ethics in Islam: Definition, Philosophy, Status, Objectives, and Methods',
             'tags': ['islamic-ethics', 'akhlaq', 'tazkiyah'],
             'subsections': [
                 ('section-00', 'Introduction'),
                 ('section-01-01', 'Definitions And Concepts Of Islamic Ethics'),
                 ('section-01-02', 'The Status Of Ethics In Islam'),
                 ('section-01-03', 'Higher Objectives And Goals Of Islamic Ethics'),
                 ('section-01-04', 'Methods Of Achieving The Objectives Of Ethics'),
                 ('section-01-05', 'Effects Of Faith-Based Education On Controlling Instincts And Habits'),
                 ('section-01-06', 'The Need For The Islamic Community And Islamic Regime'),
             ]},
            # Chapter 2
            {'num': 2, 'slug': 'ch-02', 'title': 'Research on Ethics',
             'tags': ['islamic-ethics', 'moral-philosophy', 'comparative-ethics'],
             'subsections': [
                 ('section-02-01', 'History Of Moral Philosophy In The West'),
                 ('section-02-02', 'Modern Moral Philosophies In The West'),
                 ('section-02-03', 'Pre-Islamic Arab Moral Philosophy'),
                 ('section-02-04', 'Arab Moral Philosophy After Islam'),
                 ('section-02-05', 'Religious Ethics And The Theory Of Divine Revelation'),
                 ('section-02-06', 'Standards Of Ethical Judgments In Islam'),
                 ('section-02-07', 'Review Of Khalid Mohammed Khalid\'s Book'),
             ]},
            # Chapter 3
            {'num': 3, 'slug': 'ch-03', 'title': 'The Foundations of Moral Philosophy in Islam',
             'tags': ['islamic-ethics', 'moral-philosophy', 'foundations'],
             'subsections': [
                 ('section-03-01', 'Moral Obligation'),
                 ('section-03-02', 'Moral Responsibility'),
                 ('section-03-03', 'Punishment'),
                 ('section-03-04', 'Intentions And Motives'),
                 ('section-03-05', 'Work And Exerted Effort'),
                 ('section-03-06', 'Complementary Principles To The Five Foundations'),
                 ('section-03-07', 'The Three Higher Transcendental Values'),
             ]},
            # Chapter 4
            {'num': 4, 'slug': 'ch-04', 'title': 'Applied Ethics',
             'tags': ['islamic-ethics', 'applied-ethics', 'divine-ethics'],
             'subsections': [
                 ('section-04-01', 'Divine Ethics: Human Morality Toward The Divine'),
                 ('section-04-02', 'Individual Ethics'),
                 ('section-04-03', 'Collective Human Ethics'),
             ]},
        ]
    },
}

def compute_word_freq(filepath, top_n=15):
    """Compute top concept word frequencies from a chapter file."""
    if not os.path.exists(filepath):
        return {}
    
    with open(filepath, 'r', errors='replace') as f:
        text = f.read()
    
    # Key Islamic concept terms with Arabic
    concept_map = {
        'hadith': 'حَدِيث', 'sunnah': 'سُنَّة', 'prayer': 'صَلَاة', 'zakat': 'زَكَاة',
        'zakah': 'زَكَاة', 'fasting': 'صَوْم', 'hajj': 'حَجّ', 'pilgrimage': 'حَجّ',
        'creed': 'عَقِيدَة', 'character': 'أَخْلَاق', 'haram': 'حَرَام', 
        'sharia': 'شَرِيعَة', 'jihad': 'جِهَاد', 'marriage': 'نِكَاح',
        'intention': 'نِيَّة', 'consensus': 'إِجْمَاع', 'quran': 'قُرْآن',
        'faith': 'إِيمَان', 'obligation': 'وَاجِب', 'wisdom': 'حِكْمَة',
        'patience': 'صَبْر', 'justice': 'عَدْل', 'purity': 'طَهَارَة',
        'repentance': 'تَوْبَة', 'charity': 'صَدَقَة', 'piety': 'تَقْوَى',
        'music': 'مُوسِيقَى', 'singing': 'غِنَاء', 'art': 'فَنّ',
        'ethics': 'أَخْلَاق', 'morality': 'أَخْلَاق',
        'punishment': 'عِقَاب', 'responsibility': 'مَسْئُولِيَّة',
        'obligation_concept': 'فَرْض',
    }
    
    text_lower = text.lower()
    freq = {}
    for eng, arb in concept_map.items():
        count = text_lower.count(eng)
        if count > 0:
            freq[eng] = (count, arb)
    
    # Sort by frequency, take top N
    sorted_freq = sorted(freq.items(), key=lambda x: x[1][0], reverse=True)[:top_n]
    return sorted_freq

def get_preview(filepath, max_chars=400):
    """Get a text preview from the chapter file."""
    if not os.path.exists(filepath):
        return "Preview not available."
    
    with open(filepath, 'r', errors='replace') as f:
        text = f.read()
    
    # Skip front matter / TOC - start from meaningful content
    # Find first substantial paragraph
    lines = text.split('\n')
    content_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if len(stripped) > 80 and not stripped.startswith('www.') and not stripped.startswith('http'):
            content_start = i
            break
    
    preview_text = '\n'.join(lines[content_start:content_start+15])[:max_chars]
    return preview_text

def make_chapter_entity(book_slug, chapter_info, total_chapters, book_title):
    """Generate a chapter entity page."""
    ch_num = chapter_info['num']
    ch_title = chapter_info['title']
    ch_slug = chapter_info['slug']
    tags = chapter_info['tags']
    
    source_path = f'raw/extracted/{book_slug}/{ch_slug}.txt'
    freq = compute_word_freq(f'{WIKI_ROOT}/{source_path}')
    preview = get_preview(f'{WIKI_ROOT}/{source_path}')
    
    # Build concept links
    concept_links = []
    concept_table_rows = []
    for eng, (count, arb) in freq[:8]:
        # Normalize zakah -> zakat for concept linking
        concept_slug = eng.replace('_concept', '').replace('zakah', 'zakat')
        concept_links.append(f'- [[concept-{concept_slug}|{eng.capitalize()} ({arb})]]')
        concept_table_rows.append(f'| [[concept-{concept_slug}|{eng.capitalize()}]] | {arb} | {count} |')
    
    # Build subsection links for ethics-in-islam
    subsection_section = ''
    if 'subsections' in chapter_info:
        subsection_lines = ['### Subsections', '']
        for sec_slug, sec_title in chapter_info['subsections']:
            subsection_lines.append(f'- **{sec_title}** → `raw/extracted/{book_slug}/{sec_slug}.txt`')
        subsection_section = '\n'.join(subsection_lines) + '\n\n'
    
    # Navigation links
    prev_link = f'- [[{book_slug}-ch-{(ch_num-1):02d}|← Chapter {ch_num-1}]]' if ch_num > 1 else ''
    next_link = f'- [[{book_slug}-ch-{(ch_num+1):02d}|Chapter {ch_num+1} →]]' if ch_num < total_chapters else ''
    
    nav = '\n'.join(filter(None, [prev_link, next_link]))
    
    content = f"""---
title: {ch_title}
created: '{today}'
updated: '{today}'
type: chapter
tags:
{chr(10).join('- ' + t for t in tags)}
sources:
- {source_path}
book: {book_slug}
chapter: {ch_num}
confidence: medium
---

# {ch_title}

**Book:** [[{book_slug}-overview|{book_title}]]
**Chapter:** {ch_num} of {total_chapters}

{subsection_section}## Chapter Links
- [[{book_slug}-overview|Book Overview]]
{chr(10).join(concept_links[:5])}

## Key Concepts

| Concept | Arabic | Frequency |
|---------|--------|-----------|
{chr(10).join(concept_table_rows)}

## Preview

```
{preview}
```

## Full Source
See `{source_path}` for complete text.

---

*Extracted from {book_title} — {ch_title}*
{nav}
"""
    return content

def make_overview_entity(book_slug, book_info):
    """Generate or update the book overview entity page."""
    title = book_info['title']
    arabic_title = book_info.get('arabic_title', '')
    domain = book_info.get('domain', '')
    chapters = book_info['chapters']
    
    chapter_lines = []
    for ch in chapters:
        chapter_lines.append(f"- [[{book_slug}-{ch['slug']}|Chapter {ch['num']}: {ch['title']}]]")
    chapter_index = '\n'.join(chapter_lines)
    
    content = f"""---
title: {title}
created: '2026-05-16'
updated: '{today}'
type: book-overview
tags:
- {domain}
sources:
- raw/extracted/{book_slug}/metadata.yaml
book: {book_slug}
arabic_title: '{arabic_title}'
domain: {domain}
chapter_count: {len(chapters)}
---

# {title}

**Arabic:** {arabic_title}
**Domain:** {domain}
**Chapters:** {len(chapters)}
**Archive.org:** [{book_slug}](https://archive.org/details/{book_info.get('archive_slug', book_slug)})

## Overview

This book by Dr. Yusuf al-Qaradawi addresses {domain}.

## Chapter Index

{chapter_index}

## Key Concepts Covered

_See individual chapter pages for concept listings._

## Related Books

See [[concepts-index|Concepts Index]] for thematic cross-references across all Qaradawi books.

## Source
- Raw extraction: `raw/extracted/{book_slug}/`
- PDF: `raw/pdfs/{book_slug}.pdf`
"""
    return content


# Process each re-split book
for book_slug, book_info in RESELLITS.items():
    chapters = book_info['chapters']
    total = len(chapters)
    
    # Generate chapter entity pages
    for ch in chapters:
        entity_content = make_chapter_entity(book_slug, ch, total, book_info['title'])
        entity_path = f'{ENTITIES}/{book_slug}-{ch["slug"]}.md'
        
        # Remove old file if it existed with different numbering
        with open(entity_path, 'w') as f:
            f.write(entity_content)
        print(f"Created {entity_path}")
    
    # Remove any old chapters that no longer exist (e.g., old diversion-arts had only ch-01)
    existing = [f for f in os.listdir(ENTITIES) if f.startswith(f'{book_slug}-ch-')]
    expected = {f'{book_slug}-{ch["slug"]}.md' for ch in chapters}
    for old_file in existing:
        if old_file not in expected:
            os.remove(f'{ENTITIES}/{old_file}')
            print(f"Removed old {old_file}")
    
    # Generate/update overview
    overview_content = make_overview_entity(book_slug, book_info)
    overview_path = f'{ENTITIES}/{book_slug}-overview.md'
    with open(overview_path, 'w') as f:
        f.write(overview_content)
    print(f"Updated {overview_path}")

print("\nDone! Entity pages regenerated.")