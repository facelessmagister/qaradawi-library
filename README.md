# Qaradawi Library

> LLM Wiki of the complete scholarly works of the late Prof. Dr. Yusuf al-Qaradawi (1926–2022)

## What This Is

A persistent, compounding knowledge base built using the Karpathy LLM Wiki pattern. Every book is decomposed into chapter-level entity pages, cross-linked with thematic concept pages, comparison analyses, and filed query results. Designed for scholarly research, fiqh study, and as training-ready structured corpus for Islamic AI assistants.

## Project Structure

```
qaradawi-library/
├── AGENTS.md           ← Agent identity and orientation (read first)
├── CLAUDE.md           ← Detailed operational instructions
├── README.md           ← This file
├── SCHEMA.md           ← Wiki conventions, taxonomy, rules
├── index.md            ← Content catalog
├── log.md              ← Chronological action log
├── raw/
│   ├── pdfs/           ← Downloaded PDFs (immutable)
│   └── extracted/      ← Extracted text per book (immutable)
├── entities/           ← Book chapter pages, scholar bios, publisher info
├── concepts/           ← Thematic pages (zakat, salah, halal/haram, etc.)
├── comparisons/        ← Side-by-side analyses (madhhab views, scholarly opinions)
├── queries/            ← Filed deep-dive query results
├── .tools/             ← Automation scripts
├── .config/
│   └── books.yaml      ← Canonical book registry
├── .cache/             ← Temporary build artifacts
└── .stats/             ← Analytics and lint reports
```

## Quick Start

### For Hermes Agent

```bash
# 1. Orient — ALWAYS do this first
cd /root/qaradawi-library
read_file SCHEMA.md
read_file index.md
read_file log.md  # last 30 lines

# 2. Download a book
python3 .tools/download_book.py --book halal-haram

# 3. Extract text
python3 .tools/extract_book.py --book halal-haram

# 4. Ingest into wiki (creates entities, concepts, updates index)
python3 .tools/ingest_book.py --book halal-haram

# 5. Lint
python3 .tools/wiki_lint.py
```

### For Human Researchers

Open the `entities/` and `concepts/` directories in any markdown editor (Obsidian, VS Code, Typora). All pages use `[[wikilinks]]` for cross-referencing and YAML frontmatter for metadata.

## Books in Corpus

| Book | Status | Archive.org |
|---|---|---|
| The Lawful and the Prohibited in Islam | ⬜ Not downloaded | [link](https://archive.org/details/lawfulprohibited0000qara_y8p5) |
| Fiqh al-Zakāh (2 vols) | ⬜ Not downloaded | [link](https://archive.org/details/fiqh-al-zakah-volume-2) |
| Approaching the Sunnah | ⬜ Not downloaded | [link](https://archive.org/details/approaching-the-sunnah-comprehension-controversy) |
| Priorities of the Islamic Movement | ⬜ Not downloaded | [link](https://archive.org/details/prioritiesofisla0000yusu) |
| Islamic Prayer: Between Extremism and Negligence | ⬜ Not downloaded | [link](https://archive.org/details/islamicprayerbet0000yusu) |
| Economic Security in Islam | ⬜ Not downloaded | [link](https://archive.org/details/economic-security-in-islam_202503) |
| Ethics in Islam | ⬜ Not downloaded | [link](https://archive.org/details/ethics-in-islam_202503) |
| Time in the Life of a Muslim | ⬜ Not downloaded | [link](https://archive.org/details/timeinlifeofmusl0000qara) |
| Education and Economy in the Sunnah | ⬜ Not downloaded | [link](https://archive.org/details/education-and-economy-in-the-sunnah) |
| Diversion and Arts in Islam | ⬜ Not downloaded | [link](https://archive.org/details/diversion-and-arts-in-islam) |
| Contemporary Fatwa Vol. 1 | ⬜ Not downloaded | [link](https://archive.org/details/contemporary-fatwa-volume-1) |
| Islamic Education and Hasan al-Banna | ⬜ Not downloaded | [link](https://archive.org/details/islamiceducation0000qara) |
| Faith and Life | ⬜ Not downloaded | [link](https://archive.org/details/faith-and-life) |
| Auspices of the Ultimate Victory of Islam | ⬜ Not downloaded | [link](https://archive.org/details/auspices-of-the-ultimate-victory-of-islam) |

See `.config/books.yaml` for the canonical registry with download/extraction/ingest flags.

## Design Decisions

- **Immutable raw sources** — PDFs and extracted text are never modified after creation. All analysis and corrections happen in wiki pages.
- **Chapter-level granularity** — Each book chapter becomes its own entity page, enabling precise cross-referencing and surgical updates.
- **Fiqh-first focus** — Political works are noted but not deeply ingested. The domain is Islamic jurisprudence, ethics, and methodology.
- **No federation** — This is a standalone scholarly wiki, not part of the multi-wiki federation.
- **Git-backed** — The wiki directory is tracked with git (raw/ is gitignored). Weekly auto-commit via cron.

## License

Personal scholarly project. Source texts are in the public domain or fair-use educational extracts from Archive.org. Wiki content is original synthesis.
