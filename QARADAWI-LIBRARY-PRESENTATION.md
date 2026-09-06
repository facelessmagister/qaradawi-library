# The Qaradawi Library LLM Wiki

**A Machine-Readable Knowledge Base of Shaykh Yusuf al-Qaradawi's Works**

---

**From:** Developer of Genesis and Genesis Hermes AI
**To:** Our Brothers and Sisters in Islam
**Date:** 9 June 2026

---

## 1. What Is the Qaradawi Library LLM Wiki?

The Qaradawi Library LLM Wiki is a **structured, machine-readable knowledge base** that systematically organises the English translations of Shaykh Yusuf al-Qaradawi's scholarly works into a format that AI systems can search, cross-reference, and reason over.

It is not a website. It is not an app. It is a **private corpus** — a collection of plain text files following the "LLM Wiki" pattern pioneered by Andrej Karpathy — designed so that an AI assistant (or a human with a search tool) can instantly find what Qaradawi said on any topic across all his books at once, compare his positions across different works, and trace every claim back to the exact chapter and page.

Think of it as the difference between having nine books on a shelf (beautiful but hard to cross-reference) and having those same nine books indexed, tagged, interlinked, and searchable by concept — so that asking "What does Qaradawi say about the relationship between zakat and social justice?" returns answers from *Fiqh al-Zakah*, *Economic Security in Islam*, *Ethics in Islam*, and *The Lawful and the Prohibited* simultaneously, each linked back to its source chapter.

---

## 2. The Books Currently Contained

The wiki currently contains **9 books** — 8 extracted as machine-readable text, and 1 recovered through OCR from an image-only PDF:

### Primary Fiqh Works

| # | Book | Arabic Title | Domain | Extracted |
|---|------|-------------|--------|-----------|
| 1 | **Fiqh al-Zakah** (2 Volumes) | فقه الزكاة | Zakah jurisprudence | 1.4M chars, 10 chapters |
| 2 | **The Lawful and the Prohibited in Islam** | الحلال والحرام في الإسلام | Halal/haram rulings | 1.4M chars, 5 chapters (OCR) |
| 3 | **Approaching the Sunnah: Comprehension and Controversy** | كيف نتفهم السنة | Hadith methodology | 996K chars, 3 chapters |

### Economic and Social Works

| # | Book | Arabic Title | Domain | Extracted |
|---|------|-------------|--------|-----------|
| 4 | **Economic Security in Islam** | الأمن الاقتصادي في الإسلام | Islamic economics | 608K chars, 7 chapters |
| 5 | **Education and Economy in the Sunnah** | التربية والاقتصاد في السنة | Prophetic pedagogy | 144K chars, 2 chapters |

### Ethics and Spirituality

| # | Book | Arabic Title | Domain | Extracted |
|---|------|-------------|--------|-----------|
| 6 | **Ethics in Islam** | أخلاق المسلم | Islamic ethics | 3.6M chars, 4 chapters, 23 subsections |
| 7 | **Faith and Life** | الإيمان والحياة | Spirituality | 292K chars, 4 chapters |
| 8 | **Diversion and Arts in Islam** | اللهو والفنون في الإسلام | Rulings on recreation & arts | 360K chars, 7 sections |

### Da'wah and Strategy

| # | Book | Arabic Title | Domain | Extracted |
|---|------|-------------|--------|-----------|
| 9 | **Auspices of the Ultimate Victory of Islam** | مقدمات النصر المبين للإسلام | Eschatological signs | 712K chars, 8 sections |

**Total extracted corpus: approximately 9.4 million characters of searchable text.**

---

## 3. How It Was Built — Full Disclosure

We believe in full transparency about how this knowledge base was constructed. Here is precisely what was done:

### Phase 0: Source Acquisition and Text Extraction

1. **PDFs were downloaded** from Archive.org using their public download API. Where a book was available as a text-selectable PDF, the `pdftotext` tool (poppler-utils) was used to extract the raw text.

2. **The Lawful and the Prohibited in Islam** was a special case. The Archive.org copy was restricted (lending-library), so an alternative PDF was sourced from a public WordPress mirror. This PDF turned out to be image-only (scanned pages, no text layer). We therefore ran **OCR (Optical Character Recognition)** using Tesseract at 300 DPI across all 379 pages, recovering approximately 709,000 characters. The OCR quality is good for the main body text (pages 57 onwards) but less reliable for cover pages, formatted headers, and pages with complex layouts.

3. **Contemporary Fatwa Volume 1** was downloaded but is also image-only and has not yet been OCR'd. It sits in the raw directory awaiting processing.

4. **Six books could not be downloaded** because Archive.org classified them as "lending-library" items requiring authenticated browser sessions. These remain unavailable:
   - Priorities of the Islamic Movement in the Coming Phase (أولويات الحركة الإسلامية)
   - Islamic Prayer: Between Extremism and Negligence (الصلاة بين الإفراط والتفريط)
   - Time in the Life of a Muslim (الوقت في حياة المسلم)
   - Islamic Education and Hasan al-Banna (التربية الإسلامية والإمام حسن البنا)
   - Fiqh al-Taharah (Arabic original — فقه الطهارة)
   - Al-Sahwah al-Islamiyyah (Arabic original — الصحوة الإسلامية)

### Phase 1: Chapter Splitting and Structure Extraction

Once raw text was extracted, each book was split into its constituent chapters or logical sections based on the book's own table of contents. Some books required re-splitting:

- **Diversion and Arts** was a single monographic essay; it was split into 7 logical sections.
- **Auspices of Victory** was split into 8 sections per its own structure.
- **Ethics in Islam** was split into 4 main chapters plus 23 subsections (the most detailed treatment).

Each split produced a separate text file, so that a query about "ethics of wealth" can retrieve just the relevant subsection rather than making you scan the entire 3.6M-character book.

### Phase 2: Entity and Concept Page Generation

For each book and each chapter, a **wiki page** was created with:
- YAML frontmatter (metadata: title, type, tags, sources)
- A scholarly summary (written by AI, grounded in the extracted text)
- Cross-references using `[[wikilinks]]` to related concepts and other chapters

For each key Islamic concept that appears across Qaradawi's works (zakat, usury, prayer, hijab, wasatiyyah, etc.), a **concept page** was created with:
- The Arabic term with diacritical marks (e.g., زَكَاة for zakat)
- A definition grounded in Qaradawi's treatment
- Key positions Qaradawi takes on the concept
- Cross-references to every chapter that discusses the concept

Currently there are **48 full concept pages** and **16 redirect pages** (for variant transliterations — e.g., "zakah" redirects to "zakat", "riba" redirects to "usury").

### Phase 3: Cross-Book Comparison Pages

Four **comparison pages** were created that synthesise how Qaradawi treats a theme across multiple books:

1. **Zakat and Economic Justice** — traces zakat across *Fiqh al-Zakah*, *Economic Security*, *Ethics in Islam*, and *The Lawful and the Prohibited*
2. **Sunnah Methodology Across Contexts** — compares hadith authentication approaches across *Approaching the Sunnah*, *Education and Economy*, and *Diversion and Arts*
3. **Halal/Haram and Islamic Permissibility** — examines the principle of original permissibility (al-ibahah al-asliyyah) across lifestyle, legal, ethical, and economic contexts
4. **Wasatiyyah — The Middle Way** — identifies wasatiyyah as Qaradawi's master framework across fiqh, ethics, lifestyle, and spirituality

### Phase 4: Federation with the LLM Wiki Hub

The Qaradawi Library is registered in a **federated LLM Wiki hub** (`~/.llm-wiki/`) that also contains the Quran Wiki (114 surahs), Hoffbrand Essential Haematology (medical textbook), and To Be a Muslim (by Fathi Yakan).

A **cross-wiki bridge document** maps 13 shared concepts between the Qaradawi Library and the Quran Wiki (such as tawhid, zakat, prayer, usury, wasatiyyah), telling exactly which Qaradawi chapters and which Qur'anic surahs treat the same theme.

A **federated query tool** enables a single search across all wikis simultaneously, ranked by relevance.

---

## 4. What You Can Do With It

### For Islamic Movement Workers

1. **Instant topical research.** Ask "What does Qaradawi say about the permissibility of music?" and get the answer from *Diversion and Arts in Islam* Chapter 4, *The Lawful and the Prohibited* Chapter 1, and *Ethics in Islam* Chapter 4 — all at once, with exact source citations.

2. **Cross-reference across books.** When preparing a da'wah talk on zakat, pull Qaradawi's legal rulings from *Fiqh al-Zakah*, his economic vision from *Economic Security*, and his ethical framing from *Ethics in Islam* — and see where they converge or differ in emphasis.

3. **Understand Qaradawi's methodology.** The comparison pages show how Qaradawi applies the same principles (wasatiyyah, original permissibility, hadith authentication) consistently across different domains — which is valuable for understanding his usul and for criticising or building upon his work.

4. **Connect Qur'anic foundations to fiqh rulings.** The cross-wiki bridge links Qaradawi's positions on zakat, riba, prayer, marriage, etc. back to the specific Qur'anic verses and surahs they derive from — so you can verify that his rulings are grounded in revelation.

5. **Prepare study materials.** The chapter summaries and concept definitions can serve as starting points for halaqah preparation, article writing, or teaching — with the full extracted text available for deeper study.

### How to Use It (Technical)

The wiki lives on our private server. To search it:

```bash
# Search all of Qaradawi's works for a topic
python3 ~/.llm-wiki/.tools/federated_query.py "zakat nisab" --rank

# Search across Qaradawi Library AND Quran Wiki
python3 ~/.llm-wiki/.tools/federated_query.py "riba usury" --rank --top 10

# Search only the Quran Wiki for a verse
python3 ~/.llm-wiki/.tools/federated_query.py "2:177" --wiki religious/quran-wiki --rank
```

For non-technical users: simply ask the Hermes AI assistant a question about Qaradawi's positions, and it will search the wiki and return grounded answers with source citations.

---

## 5. Limitations — Full Disclosure

We are committed to honesty about what this system can and cannot do:

### 5.1 Extraction Accuracy

- **OCR quality varies.** The Halal and Haram book was OCR'd from a scanned PDF. Cover pages, chapter headers with decorative formatting, and pages with complex layouts may contain OCR errors (e.g., dropped headings, garbled formatting). The main body text from page 57 onwards is generally reliable, but any OCR'd text should be cross-checked against the original PDF for critical quotations.
- **pdftotext artifacts.** Even for text-selectable PDFs, automated extraction sometimes misses page breaks, mangles footnotes, or produces minor formatting artifacts. Chapter splits were done carefully but may not perfectly match every printed edition.
- **No Arabic text.** The wiki works exclusively with **English translations**. The two Arabic-only books (Fiqh al-Taharah and Al-Sahwah al-Islamiyyah) have not been ingested because we do not currently have an Arabic-capable text extraction and NLP pipeline. This is a significant gap — Qaradawi's Arabic original texts contain nuances that translations may not fully convey.

### 5.2 Content Gaps

- **6 of 16 registered books are unavailable.** The most impactful gap is *Priorities of the Islamic Movement in the Coming Phase* (أولويات الحركة الإسلامية) — a book directly relevant to Islamic movement work — which is locked behind Archive.org's lending-library restriction. Also unavailable: *Islamic Prayer*, *Time in the Life of a Muslim*, and *Islamic Education and Hasan al-Banna*.
- **Contemporary Fatwa Volume 1** is downloaded but unprocessed (image-only PDF, awaiting OCR).
- **No fatwa compilation.** Qaradawi issued thousands of fatwas beyond what is in these books. This wiki covers only his major monographic works.

### 5.3 AI-Generated Content

- **Summaries and concept definitions are AI-generated.** While they are grounded in the extracted text (the AI read the actual chapters before writing), they are not Qaradawi's own words. They represent an interpretation and synthesis. Always verify any claim by reading the original extracted chapter text.
- **Comparison pages are synthetic analysis.** The four comparison pages (zakat, sunnah, halal/haram, wasatiyyah) represent an AI's reading of patterns across multiple books. They may miss nuances or over-simplify Qaradawi's positions. They are tools for orientation, not authoritative rulings.
- **No human scholarly review.** The wiki has not been reviewed by an Islamic studies scholar. It is a research assistance tool, not a peer-reviewed academic publication.

### 5.4 Concept Coverage

- **48 concepts is not exhaustive.** The wiki covers major recurring themes (zakat, usury, prayer, faith, etc.) but does not yet have pages for every Islamic concept that appears in Qaradawi's works. Additional concept pages can be created as needed.
- **Redirects address transliteration variants** but may not cover every spelling convention.

### 5.5 Political Content Omission

- By design, the wiki focuses on Qaradawi's **fiqh, ethical, and spiritual** scholarship. Where a book contains political content (especially *Auspices of Victory* and *Priorities of the Islamic Movement*), the extraction and summarisation process was configured to flag rather than amplify political sections. This is a deliberate editorial choice — not censorship, but prioritisation of content that serves the wiki's purpose as a fiqh and ethics reference.

---

## 6. How It Can Be Expanded

The wiki is designed to grow. Here are the concrete expansion paths:

### Immediate (If Sources Become Available)

1. **Obtain the 6 blocked books.** If physical copies or unrestricted PDFs of *Priorities of the Islamic Movement*, *Islamic Prayer*, *Time in the Life of a Muslim*, and *Islamic Education and Hasan al-Banna* become available, they can be ingested within hours using the existing pipeline.
2. **OCR Contemporary Fatwa Volume 1.** The 21MB image-only PDF is already downloaded. Running it through the OCR pipeline would add Qaradawi's fatwa rulings on contemporary issues.
3. **Add more concept pages.** Any concept that appears in the extracted text can be given its own page with definition, positions, and cross-references.

### Medium-Term

4. **Arabic text pipeline.** Building an Arabic-capable extraction and search pipeline would unlock *Fiqh al-Taharah* and *Al-Sahwah al-Islamiyyah* — and more importantly, would allow ingesting Qaradawi's Arabic originals alongside their English translations for comparison.
5. **Human scholarly review.** Having a qualified scholar review and correct the AI-generated summaries and concept pages would significantly increase the wiki's reliability.
6. **More comparison pages.** Additional cross-book syntheses could cover themes like: Qaradawi on women, Qaradawi on jihad, Qaradawi on inter-faith relations, Qaradawi on governance.
7. **Qur'anic verse cross-links.** Each concept page could be enriched with explicit links to the specific Qur'anic verses it references, connecting to the Quran Wiki for tafsir context.

### Long-Term

8. **Full Qaradawi corpus.** Qaradawi authored over 170 works. The current 9 books represent a fraction. Expanding the corpus would require systematic access to English translations.
9. **Multi-scholar corpus.** The same LLM Wiki architecture could be applied to other scholars — e.g., building a Fathi Yakan wiki (already partially started), or integrating works by Ibrahim al-Bayoumi Ghanem, Muhammad al-Ghazali, or other wasatiyyah scholars. The federated hub design supports multiple simultaneous wikis.
10. **Arabic-English parallel alignment.** For scholarly rigour, aligning Arabic original passages with their English translations (paragraph-level) would enable precise verification of translation accuracy.

---

## 7. Summary of Current Wiki Statistics

| Metric | Count |
|---|---|
| Total wiki pages | 135 |
| Books ingested | 9 |
| Book overview pages | 9 |
| Chapter/entity pages | 50 |
| Scholar biography page | 1 |
| Full concept pages | 48 |
| Redirect concept pages | 16 |
| Cross-book comparison pages | 4 |
| Extracted text corpus | ~9.4 million characters |
| Critical lint issues | 0 |
| Books registered but unavailable | 6 |
| Books downloaded but unprocessed | 1 (Contemporary Fatwa Vol 1) |

---

## 8. Closing Note

This wiki was built in the spirit of **facilitating access to knowledge** (تيسير العلم) — one of the core principles Qaradawi himself championed throughout his career. It is offered as a tool for your work, with full honesty about its limitations and an open door for its improvement.

If you have access to physical copies or unrestricted PDFs of any of the 6 unavailable books, or if you would like to contribute scholarly review of any content, please reach out. This wiki belongs to the work.

---

*Developer of Genesis and Genesis Hermes AI*
*9 June 2026*