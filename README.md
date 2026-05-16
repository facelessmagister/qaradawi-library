# قَرَضَاوِيّ مَكْتَبَة — Qaradawi Library

> The complete scholarly works of the late **Prof. Dr. Yusuf al-Qaradawi** (1926–2022), published as a beautiful, mobile-optimised e-library with per-book, per-chapter, and per-topic navigation.

**🌐 Live Site:** [qaradawi-library.vercel.app](https://qaradawi-library.vercel.app)

---

## About Dr. Yusuf al-Qaradawi (1926–2022)

Shaykh Dr. Yusuf al-Qaradawi was one of the most prolific and influential Muslim scholars of the 20th and 21st centuries. Born in Egypt, he graduated from al-Azhar University and authored over 120 books spanning fiqh (Islamic jurisprudence), usul al-fiqh (principles of jurisprudence), hadith methodology, tazkiyah (spiritual purification), Islamic ethics, economics, and da'wah.

His works are characterised by moderation (*wasatiyyah*), deep engagement with contemporary issues, and a commitment to balancing classical scholarship with modern realities.

---

## About This Library

This project aims to build the most comprehensive, searchable, and cross-referenced digital archive of Dr. al-Qaradawi's scholarly works in English. Each book is decomposed into chapter-level pages and cross-linked with thematic concept pages covering key fiqh topics.

**Current corpus:**
- **8 books** fully ingested (32 chapters)
- **25 concept topics** cross-referenced across all books
- **8 books** pending (restricted on Archive.org or awaiting OCR)
- **71 pages** in the LLM Wiki backend

---

## Navigating the E-Library

### Three-Tier Navigation

```
Library Home (/)                    — All books in a beautiful grid
    ↓
  Book Page (/books/faith-and-life/)  — Metadata, chapter index, concept pills
    ↓
  Chapter Page (/.../ch-1/)           — Full chapter content with verses and quotes
    
  Topic Hub (/topics/creed/)          — Every chapter across ALL books mentioning this concept
```

### Featured Book: Faith and Life

*Faith and Life* (الإيمان والحياة) chapters 1–4 are published with full rich formatting:
- **Ch. 1:** Iman and the Dignity of Man
- **Ch. 2:** Iman and Happiness
- **Ch. 3:** Iman and Love
- **Ch. 4:** Iman and Hope

Each chapter includes Qur'anic verses in Arabic, hadith excerpts, and scholarly quotes from al-Ghazali, ibn al-Qayyim, and others.

---

## Published Books

| Book | Domain | Chapters |
|------|--------|:--:|
| **Fiqh al-Zakah** (2 Volumes) | Mu'amalat / Transactions | 10 |
| **Economic Security in Islam** | Mu'amalat / Transactions | 7 |
| **Ethics in Islam** | Islamic Ethics | 4 |
| **Faith and Life** | Tazkiyah / Spirituality | 4 |
| **Approaching the Sunnah** | Hadith Methodology | 3 |
| **Education & Economy in the Sunnah** | Islamic Education | 2 |
| **Diversion and Arts in Islam** | Ibadah / Worship | 1 |
| **Auspices of the Ultimate Victory** | Da'wah | 1 |

---

## Technical Architecture

This is a **static HTML e-library** generated from a Karpathy-style LLM Wiki:

```
Wiki (65 markdown pages)  →  generate.py  →  67 HTML pages  →  Vercel
```

- **No frameworks** — vanilla HTML/CSS with Python 3 stdlib generator
- **Design:** Notion-inspired warm paper tones, *Playfair Display* serif headings, amber-gold academic accent
- **Mobile-responsive** with dark mode via `prefers-color-scheme`
- **Auto-deploy:** Every `git push` to master triggers Vercel redeployment

### Project Structure

```
qaradawi-library/
├── website/
│   ├── src/
│   │   ├── generate.py    ← Site generator (reads wiki → writes HTML)
│   │   └── style.css      ← Design system CSS
│   └── dist/              ← Generated static site (deployed)
├── entities/              ← Book + chapter wiki pages (40)
├── concepts/              ← Thematic concept pages (25)
├── raw/
│   ├── pdfs/              ← Downloaded PDFs (gitignored)
│   └── extracted/         ← Extracted chapter text (gitignored)
├── .tools/                ← Python scripts (download, extract, ingest, lint)
├── .config/books.yaml     ← Canonical book registry
└── vercel.json            ← Vercel deployment config
```

---

## Pipeline (for Contributors)

The workflow for adding new books:

```bash
# 1. Download from Archive.org
python3 .tools/download_book.py --book {slug}

# 2. Extract text and split into chapters
python3 .tools/extract_book.py --book {slug}

# 3. Ingest into wiki (creates entities + concepts + cross-links)
python3 .tools/ingest_book.py --book {slug}

# 4. Regenerate e-library site
cd website/src && python3 generate.py

# 5. Push to trigger Vercel auto-deploy
git add -A && git commit -m "feat: ingest {book}" && git push
```

---

## Credits

- **Author:** Prof. Dr. Yusuf al-Qaradawi (1926–2022)
- **Publisher:** Al-Falah Foundation for Translation, Publication & Distribution
- **Source texts:** Archive.org open-access PDFs
- **Library Curation:** Hafiz HMZ + Hermes Agent
- **Repository:** [github.com/facelessmagister/qaradawi-library](https://github.com/facelessmagister/qaradawi-library)

---

*Built with ❤️ for students of knowledge everywhere.*
