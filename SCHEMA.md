# Wiki Schema

## Domain
Islamic Scholarly Corpus — Complete works of Dr. Yusuf al-Qaradawi (1926–2022), focused on fiqh, usul al-fiqh, tafsir methodology, ethics, and spirituality.

## Conventions
- **File names:** lowercase, hyphens, no spaces, no apostrophes in slugs (e.g., `fiqh-al-zakah-ch-01.md`, `concept-zakat.md`)
- **Every wiki page starts with YAML frontmatter** (template below)
- **Use `[[wikilinks]]`** to link between pages (minimum 2 outbound links per page)
- **When updating a page, always bump the `updated` date**
- **Every new page must be added to `index.md`** under the correct section
- **Every action must be appended to `log.md`**
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/extracted/{book-slug}/ch-01.txt]` at the end of paragraphs whose claims come from a specific source
- **Arabic terms:** Always include Arabic in original script with diacritics for precision: *zakah* (زَكَاة), *fiqh* (فِقْه), *usul* (أُصُول)

## Frontmatter Template

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | chapter | book-overview
tags: [from taxonomy below]
sources: [raw/extracted/{book-slug}/ch-01.txt]
book: book-slug  # For chapter pages: which book this belongs to
chapter: 1      # For chapter pages: chapter number
confidence: high | medium | low
contested: true
transliteration: slug-safe-name  # For pages with Arabic titles
---
```

### Raw Source Frontmatter
Every extracted chapter file gets:
```yaml
---
source_url: https://archive.org/details/identifier
ingested: YYYY-MM-DD
book: book-slug
chapter: 1
sha256: <hex digest of extracted content>
---
```

## Tag Taxonomy

### By Subject (Fiqh Domains)
- `fiqh-ibadat` — Worship (salah, zakah, sawm, hajj)
- `fiqh-muamalat` — Transactions (trade, contracts, inheritance)
- `fiqh-ahwal-shakhsiyyah` — Personal status (marriage, divorce, custody)
- `fiqh-jinayat` — Criminal law / hudud
- `fiqh-dawah` — Islamic propagation and methodology

### By Discipline
- `usul-al-fiqh` — Principles of jurisprudence
- `tafsir-methodology` — Quranic exegesis methods
- `hadith-methodology` — Hadith sciences
- `islamic-ethics` — Akhlaq and character
- `islamic-economics` — Financial and economic rulings
- `islamic-education` — Pedagogy and tarbiyyah

### By Meta
- `book-overview` — Summary/overview of a complete book
- `chapter` — Individual chapter page
- `concept` — Thematic concept page
- `comparison` — Side-by-side analysis
- `query` — Filed research result
- `scholar` — Biographical entity page
- `publisher` — Publishing house entity

### By Quality
- `verified` — Content checked against original PDF
- `incomplete` — Partial extraction or pending verification
- `political-excluded` — Source contains political content that was skipped

## Page Thresholds
- **Create a chapter page** when a chapter has ≥3 substantive sections or concepts
- **Create a concept page** when a concept appears in 2+ books/chapters
- **Create a comparison page** when 2+ scholars/books address the same issue with differing views
- **DON'T create a page** for passing mentions, du'a collections, or purely political content
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when fully superseded by a newer edition — move to `_archive/`

## Chapter Page Structure
Each chapter page MUST include:
1. **Overview** — What this chapter covers, its place in the book
2. **Key Concepts** — Concepts introduced or developed, linked via `[[concept-slug]]`
3. **Key Rulings** — Fiqh positions stated, with evidence cited
4. **Cross-Book Connections** — Links to other Qaradawi books addressing the same topic
5. **Arabic Terminology** — Key Arabic terms with original script
6. **Source Reference** — `raw/extracted/{book-slug}/ch-XX.txt` with line range

## Concept Page Structure
Each concept page MUST include:
1. **Definition** — Clear definition with Arabic term
2. **Qaradawi's Position** — His specific view with book citations
3. **Evidence Base** — Quranic verses and hadith he cites
4. **Comparison with Classical Scholars** — How his view aligns with or differs from the 4 madhabs
5. **Related Concepts** — `[[wikilinks]]` to connected topics
6. **Contemporary Relevance** — Why this matters today

## Update Policy
When new information conflicts with existing content:
1. Check dates — Qaradawi's later works generally supersede earlier ones on the same topic
2. If genuinely contradictory, note both positions with dates and sources
3. Mark contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report

## Navigation
- `index.md` — Sectioned catalog: Books → Chapters → Concepts → Comparisons → Queries
- `log.md` — Append-only chronological record
- Every page links to its parent book overview and to related concept pages
