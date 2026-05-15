# Qaradawi Library — Operational Guide

## Project Root
`/root/qaradawi-library/`

## Session Startup Protocol (ALWAYS)

Every time you work on this project, follow this exact order:

1. `cd /root/qaradawi-library`
2. Read `SCHEMA.md` — refresh conventions and taxonomy
3. Read `index.md` — know what exists
4. Read `log.md` (last 30 lines) — know recent activity
5. Read `AGENTS.md` — refresh project identity and constraints

Only after these 5 orientation steps should you perform any wiki operation.

---

## Phase 1: Download Books

### Manual Download (One-off)
```bash
cd /root/qaradawi-library
python3 .tools/download_book.py --book halal-haram
```

### Batch Download
```bash
python3 .tools/download_book.py --all
```

### What `download_book.py` does:
1. Reads `.config/books.yaml` for Archive.org identifier and format preference
2. Downloads the best available PDF to `raw/pdfs/{book-slug}.pdf`
3. Verifies download integrity (file size check against expected)
4. Updates `books.yaml`: `downloaded: true`, `downloaded_at: YYYY-MM-DD`
5. Appends to `log.md`

### Expected Archive.org Format Priority:
1. `Text PDF` (OCR'd, searchable)
2. `LCP Encrypted PDF` (if Text PDF unavailable)
3. `Image Container PDF` (fallback — requires OCR later)

---

## Phase 2: Extract Text

### Per-Book Extraction
```bash
python3 .tools/extract_book.py --book halal-haram
```

### What `extract_book.py` does:
1. Runs `pdftotext -layout raw/pdfs/{book-slug}.pdf raw/extracted/{book-slug}/full.txt`
2. Runs `pdfinfo raw/pdfs/{book-slug}.pdf` to capture metadata (title, author, pages, creation date)
3. Creates chapter boundary markers by detecting:
   - "Chapter X" or "CHAPTER X" headers
   - Arabic chapter titles in isolated lines
   - Page number discontinuities (indicates new chapter)
4. Splits `full.txt` into `raw/extracted/{book-slug}/ch-01.txt`, `ch-02.txt`, etc.
5. Adds raw frontmatter to each chapter file
6. Computes SHA256 of each chapter for drift detection
7. Updates `books.yaml`: `extracted: true`
8. Creates `raw/extracted/{book-slug}/metadata.yaml` with book-level info
9. Appends to `log.md`

### Handling Poor-Quality PDFs
If the PDF is image-only (no embedded text), `pdftotext` will produce empty or garbage output. In this case:
1. Flag in `books.yaml`: `ocr_needed: true`
2. The extraction script will skip text extraction and create a placeholder
3. For critical books, note in `log.md` that OCR is pending

---

## Phase 3: Ingest into Wiki

### Per-Book Ingest
```bash
python3 .tools/ingest_book.py --book halal-haram
```

### What `ingest_book.py` does:
1. Reads all chapter files from `raw/extracted/{book-slug}/`
2. Creates `entities/{book-slug}-overview.md` — Book overview page
3. For each chapter:
   - Creates `entities/{book-slug}-ch-{NN}.md` — Chapter entity page
   - Extracts key concepts, fiqh rulings, Arabic terminology
   - Generates `[[wikilinks]]` to related concept pages
4. Creates or updates `concepts/` pages for concepts mentioned in the chapter
5. Updates `index.md` with new pages
6. Updates `log.md` with batch summary
7. Updates `books.yaml`: `ingested: true`, `pages_created: N`

### Ingest Quality Requirements
- Each chapter page must have ≥2 `[[wikilinks]]` outbound
- Each concept page must have ≥2 `[[wikilinks]]` outbound
- Every page must have valid YAML frontmatter
- Every page must reference its source in `sources:` frontmatter
- Arabic terms must include original script with diacritics

### Ingest Report
The script prints a summary:
```
Ingested: The Lawful and the Prohibited in Islam
- Chapter pages created: 12
- Concept pages created: 8
- Concept pages updated: 3
- Total wiki pages: 143
- Orphan check: 0 orphans
- Cross-links added: 47
```

---

## Phase 4: Cross-Referencing

After ingesting 2+ books, run the cross-reference pass:

```bash
python3 .tools/cross_reference.py
```

### What it does:
1. Scans all chapter pages for shared concepts
2. Adds bi-directional `[[wikilinks]]` between chapters addressing the same topic
3. Identifies contradictions between books on the same issue
4. Flags for comparison page creation
5. Updates `comparisons/` if a new comparison is warranted
6. Appends to `log.md`

---

## Phase 5: Lint / Health Check

```bash
python3 .tools/wiki_lint.py
```

### Checks performed:
1. **Orphan pages** — Pages with zero inbound `[[wikilinks]]`
2. **Broken links** — `[[wikilinks]]` pointing to non-existent files
3. **Missing frontmatter** — Pages without required YAML
4. **Index completeness** — Every page must appear in `index.md`
5. **Stale content** — Pages not updated in 90+ days with newer sources available
6. **Tag audit** — Tags not in SCHEMA.md taxonomy
7. **Arabic terms** — Pages with Arabic terms missing diacritics or original script
8. **Source drift** — SHA256 mismatch in raw/ (indicates tampering)
9. **Page size** — Pages over 200 lines flagged for splitting

### Severity Grouping
- **CRITICAL:** Broken links, missing frontmatter, index orphans
- **WARNING:** Orphan pages, stale content, source drift
- **INFO:** Tag sprawl, page size, Arabic formatting

---

## Phase 6: Query / Research

When the user asks a fiqh question:

1. Read `index.md` to identify relevant pages
2. `search_files "topic" path="/root/qaradawi-library" file_glob="*.md"`
3. Read relevant pages
4. Synthesize answer with citations: "Based on [[concept-zakat]] and [[fiqh-al-zakah-ch-03]]..."
5. If the synthesis is substantial and novel, file it as `queries/{topic-slug}.md`
6. Update `log.md`

---

## Special Operations

### Re-Ingest (Book Updated or Better PDF Found)
```bash
python3 .tools/ingest_book.py --book halal-haram --reingest
```
- Recomputes SHA256, compares to stored value
- If different: flags drift, re-extracts, re-ingests
- If identical: skips with message

### Add a New Book to Registry
1. Edit `.config/books.yaml` — append new book entry
2. Run `download_book.py --book {new-slug}`
3. Run `extract_book.py --book {new-slug}`
4. Run `ingest_book.py --book {new-slug}`
5. Run `cross_reference.py`
6. Run `wiki_lint.py`
7. Update `README.md` book table
8. Git commit

### Git Workflow
```bash
cd /root/qaradawi-library
git add -A
git commit -m "ingest: halal-haram — 12 chapters, 8 concepts, 47 cross-links"
```

**raw/ is gitignored.** Only wiki pages, schemas, indices, logs, and tools are committed.

---

## Error Handling

| Problem | Action |
|---------|--------|
| PDF download fails | Retry with curl `-L --retry 3`. If still fails, flag in books.yaml and skip |
| pdftotext produces garbage | Flag `ocr_needed: true`, skip extraction, note in log |
| Chapter boundary unclear | Use heuristic: "Chapter" + number + isolated line. If fails, ask user |
| Ingest creates orphan pages | Run `cross_reference.py` immediately after ingest |
| Contradiction detected | Create comparison page, mark `contested: true`, flag for review |
| Broken wikilinks after bulk generation | Run `wiki_lint.py --fix-orphans` to create missing stubs |

---

## Weekly Maintenance (Cron)

| Task | Frequency | Script |
|------|-----------|--------|
| Git backup | Weekly | `.tools/cron-backup.sh` |
| Lint | After every ingest | `wiki_lint.py` |
| Cross-reference refresh | After every 2nd book ingest | `cross_reference.py` |
| Orphan sweep | Monthly | `wiki_lint.py --fix-orphans` |
