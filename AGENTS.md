# Qaradawi Library — Agent Context

## Project Identity

**Name:** Qaradawi Library (قَرَضَاوِيّ مَكْتَبَة)
**Domain:** Islamic Scholarly Corpus — Complete works of the late Prof. Dr. Yusuf al-Qaradawi (1926–2022)
**Location:** `/root/qaradawi-library/`
**Type:** LLM Wiki (Karpathy pattern) + Static E-Library Website + GitHub Repository

## Mission

Build and maintain the most comprehensive, searchable, cross-referenced digital knowledge base of Dr. Yusuf al-Qaradawi's books in English. Each book decomposed into chapter-level entity pages, with thematic concept pages, scholarly comparison pages, and filed query results.

## Critical Constraint — Sunni Authenticity

Dr. al-Qaradawi is a contemporary scholar whose works span fiqh, usul, politics, and da'wah. This wiki focuses **exclusively on his fiqh, usul al-fiqh, and spiritual writings**.

- ✅ **Include:** Fiqh rulings, usul, tafsir methodology, ethics, spirituality, hadith methodology
- ❌ **Exclude:** Political works, contemporary political fatwas, polemical writings
- When a source has mixed content, note the political sections but do not create wiki pages for them
- Tag all pages with `domain: fiqh | usul | tazkiyah | hadith-methodology` for filtering

## Zone Boundary

- **Personal project** — lives under `/root/qaradawi-library/`
- **Never references** Genesis business wikis or personal project wikis (shafira, tarbiyyah, codesign)
- **Standalone wiki** — no federation with other wikis unless explicitly requested

## Tooling Available

- `pdftotext` — PDF to text extraction
- `pdfinfo` — PDF metadata extraction
- `curl` — Download from Archive.org
- Python 3 — Custom extraction and processing scripts
- Hermes Agent — Wiki page generation, cross-referencing, linting
- Git — Version control
- GitHub — Repository hosting
- Vercel — Static site deployment

## Source Priority

1. **Archive.org** — Primary source for downloadable PDFs
2. **Verified Islamic publishers** — Dar al-Kutub al-Ilmiyyah, International Islamic Publishing House
3. **Academic repositories** — JSTOR, Brill (for scholarly articles about Qaradawi)

## Workflow Overview

```
Phase 1: Download → raw/pdfs/
Phase 2: Extract → raw/extracted/{book-slug}/
Phase 3: Split → Chapter-level temp files
Phase 4: Ingest → Generate wiki pages (entities, concepts)
Phase 5: Cross-reference → Link pages, update index
Phase 6: Lint → Health check, contradictions, orphans
Phase 7: Website → Generate static HTML from wiki
Phase 8: Deploy → GitHub push → Vercel auto-deploy
```

## Context Files (Read These First)

1. **SCHEMA.md** — Wiki conventions, tag taxonomy, frontmatter rules
2. **index.md** — Content catalog — read before any query
3. **log.md** — Chronological action log — read last 30 entries to orient
4. **CLAUDE.md** — Detailed operational instructions for every phase
5. **README.md** — Project overview for human readers
6. **.config/books.yaml** — Canonical book registry with URLs, status, metadata

## Directory Structure

```
/root/qaradawi-library/
├── .config/              # Book registry, templates
├── .tools/               # Python scripts (download, extract, ingest, lint)
├── raw/
│   ├── pdfs/            # Downloaded PDFs
│   └── extracted/       # pdftotext output, chapter splits
├── entities/            # Book + chapter wiki pages
├── concepts/            # Thematic concept pages
├── comparisons/         # Cross-book comparisons
├── queries/             # Filed research results
├── website/             # Static site source
│   ├── src/             # HTML/CSS/JS templates
│   ├── public/          # Static assets
│   └── dist/            # Build output
├── .github/
│   └── workflows/       # CI/CD: lint → build → deploy
├── index.md             # Wiki content index
├── log.md               # Action log
├── SCHEMA.md            # Wiki schema
├── README.md            # Human-facing overview
└── AGENTS.md            # This file
```

## Quality Gates

Before declaring any phase complete:
- Every new page must have YAML frontmatter (see SCHEMA.md)
- Every new page must link to ≥2 other pages via `[[wikilinks]]`
- Every action must be appended to `log.md`
- Every book ingest must update `index.md`
- All pages must pass `tools/wiki_lint.py`
- Website must pass W3C HTML validation
- Commit to GitHub with clear message: `[area] action | subject`

## GitHub / Vercel Integration

- **GitHub repo:** `github.com/hafizhmz/qaradawi-library` (or user-specified)
- **Vercel project:** linked to GitHub repo, auto-deploy on push to `main`
- **Tokens:** Use `GITHUB_TOKEN` and `VERCEL_TOKEN` from environment
- **CI/CD:** GitHub Actions runs `wiki_lint.py` on every PR, builds site on every push

## Book Registry

See `.config/books.yaml` for the canonical list of books, their Archive.org URLs, download status, extraction status, and ingest status.

## Notes for the Agent

- When a book needs OCR, flag it in `books.yaml` and skip extraction
- When a book is restricted on Archive.org, flag it and retry in next session
- When chapter boundaries are unclear, do a best-effort split and note it in the log
- When generating the website, prioritize readability and calm aesthetics over flashy design
- Arabic text support is a future goal — for now, focus on English content
- Always keep the wiki and the website in sync — they are two views of the same data
