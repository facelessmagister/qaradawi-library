---
title: Wiki Log
created: 2026-05-16
updated: 2026-06-09T16:00
type: log
tags: [meta, log]
---

# Wiki Log

## 2026-06-09 — Created 21 new stub concept pages

Created 21 new stub concept pages under `/root/qaradawi-library/concepts/`. Each contains:
- YAML frontmatter (title, created, updated, type, tags, sources, confidence, transliteration)
- Arabic term with transliteration
- 100-150 word definition grounded in Qaradawi's treatment
- 2-3 key positions with source citations
- Cross-references (2-5 wikilinks to related existing concepts)
- Source references

New stubs:
1. `concept-dawah.md` — دَعْوَة Islamic propagation/invitation
2. `concept-darurah.md` — ضَرُورَة Necessity as a fiqh principle
3. `concept-hudud.md` — حُدُود Fixed/Hudud punishments
4. `concept-ikhlas.md` — إِخْلَاص Sincerity in worship
5. `concept-isnad.md` — إِسْنَاد Hadith chain of transmission
6. `concept-mal.md` — مَال Wealth/property in Islamic law
7. `concept-nisab.md` — نِصَاب Zakat minimum threshold
8. `concept-hawl.md` — حَوْل Zakat fiscal year
9. `concept-obligation.md` — وُجُوب / فَرْض Obligation/wajib/fard
10. `concept-sabr.md` — صَبْر Patience/perseverance
11. `concept-qiyas.md` — قِيَاس Analogical reasoning
12. `concept-quran.md` — قُرْآن The Qur'an
13. `concept-responsibility.md` — مَسْؤُولِيَّة Responsibility in Islam
14. `concept-riya.md` — رِيَاء Showing off/ostentation
15. `concept-tajdid.md` — تَجْدِيد Renewal/revival
16. `concept-tawhid.md` — تَوْحِيد Monotheism
17. `concept-tazkiyah.md` — تَزْكِيَة Spiritual purification
18. `concept-usul-al-fiqh.md` — أُصُول الفِقْه Principles of Islamic jurisprudence
19. `concept-waqf.md` — وَقْف Islamic endowment
20. `concept-wasatiyyah.md` — وَسَطِيَّة Middle way/moderation
21. `concept-wisdom.md` — حِكْمَة Wisdom/hikmah

Updated `concepts-index.md` to include all 21 new concepts in the All Concepts list and added a "New Stub Concepts" section. Total page count: 54 (26 full + 7 redirects + 21 stubs).

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: create, ingest, update, query, lint, cross-ref, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-05-16] create | Wiki initialized
- Domain: Islamic scholarly corpus — complete works of Dr. Yusuf al-Qaradawi
- Structure created: AGENTS.md, CLAUDE.md, README.md, SCHEMA.md, index.md, log.md
- Tools created: download_book.py, extract_book.py, ingest_book.py, cross_reference.py, wiki_lint.py
- Config created: books.yaml
- Raw directories: raw/pdfs/, raw/extracted/
- Wiki directories: entities/, concepts/, comparisons/, queries/
- Total pages at initialization: 0
- Books in registry: 14
- Next action: Begin Phase 1 — download first book

## [2026-06-09] create | concept-zakat
- Written: /root/qaradawi-library/concepts/concept-zakat.md
- Sources: raw/extracted/fiqh-al-zakah/ch-01.txt (lines 1-350), raw/extracted/economic-security/ch-04.txt (lines 1-300)
- Type: concept page

## [2026-06-09] update | concept-ijtihad
- Written: /root/qaradawi-library/concepts/concept-ijtihad.md
- Sources: raw/extracted/fiqh-al-zakah/ch-01.txt, ch-02, ch-05, ch-07, ch-08; raw/extracted/approaching-the-sunnah/ch-01, ch-02, ch-03
- Type: concept page (expanded from stub)
- Content: Detailed concept page covering definition, Qaradawi's 7 key positions on ijtihad, evidence base, comparison with 4 madhhabs + Zahiris + post-classical reformers, criteria for sound ijtihad, contemporary relevance, and related concepts
- Confidence upgraded: low → high
- Tags updated: usul-al-fiqh, shariah, islamic-economics, zakat, sunnah, meta
- Content: Definition, Qaradawi's positions, evidence base (Quranic + hadith), comparison with 4 madhhabs + Zahiri, conditions for zakatability, rates table, Zakat al-Fitr, contemporary relevance, related concepts
- Tags: fiqh-ibadat, fiqh-muamalat, zakat, sadaqah, islamic-economics, aqeedah
- Outbound links: concept-nisab, concept-sadaqah, concept-riba, concept-mal, concept-hawl, concept-waqf (6 wikilinks)

## [2026-05-16] extract
- book: Approaching the Sunnah: Comprehension and Controversy
- slug: approaching-the-sunnah
- chapters: 3
- total_chars: 523091
- status: SUCCESS

## [2026-05-16] extract
- book: Auspices of the Ultimate Victory of Islam
- slug: auspices-victory
- chapters: 1
- total_chars: 357094
- status: SUCCESS

## [2026-05-16] extract
- book: Contemporary Fatwa Volume 1
- slug: contemporary-fatwa-1
- status: FAILED — OCR needed

## [2026-05-16] extract
- book: Diversion and Arts in Islam
- slug: diversion-arts
- chapters: 1
- total_chars: 169730
- status: SUCCESS

## [2026-05-16] extract
- book: Economic Security in Islam
- slug: economic-security
- chapters: 7
- total_chars: 309791
- status: SUCCESS

## [2026-05-16] extract
- book: Education and Economy in the Sunnah
- slug: education-economy-sunnah
- chapters: 2
- total_chars: 72654
- status: SUCCESS

## [2026-05-16] extract
- book: Ethics in Islam
- slug: ethics-in-islam
- chapters: 4
- total_chars: 1204911
- status: SUCCESS

## [2026-05-16] extract
- book: Faith and Life
- slug: faith-and-life
- chapters: 4
- total_chars: 155087
- status: SUCCESS

## [2026-05-16] extract
- book: Fiqh al-Zakah (2 Volumes)
- slug: fiqh-al-zakah
- chapters: 10
- total_chars: 838161
- status: SUCCESS

## [2026-05-16] ingest
- book: Approaching the Sunnah: Comprehension and Controversy
- slug: approaching-the-sunnah
- chapters: 3
- chapter_pages: 3
- concept_pages_created: 12
- concept_pages_updated: 12
- total_pages: 16

## [2026-05-16] ingest
- book: Economic Security in Islam
- slug: economic-security
- chapters: 7
- chapter_pages: 7
- concept_pages_created: 5
- concept_pages_updated: 18
- total_pages: 13

## [2026-05-16] ingest
- book: Education and Economy in the Sunnah
- slug: education-economy-sunnah
- chapters: 2
- chapter_pages: 2
- concept_pages_created: 0
- concept_pages_updated: 13
- total_pages: 3

## [2026-05-16] ingest
- book: Ethics in Islam
- slug: ethics-in-islam
- chapters: 4
- chapter_pages: 4
- concept_pages_created: 2
- concept_pages_updated: 30
- total_pages: 7

## [2026-05-16] ingest
- book: Fiqh al-Zakah (2 Volumes)
- slug: fiqh-al-zakah
- chapters: 10
- chapter_pages: 10
- concept_pages_created: 2
- concept_pages_updated: 56
- total_pages: 13

## [2026-05-16] ingest
- book: Auspices of the Ultimate Victory of Islam
- slug: auspices-victory
- chapters: 1
- chapter_pages: 1
- concept_pages_created: 1
- concept_pages_updated: 7
- total_pages: 3

## [2026-05-16] ingest
- book: Diversion and Arts in Islam
- slug: diversion-arts
- chapters: 1
- chapter_pages: 1
- concept_pages_created: 1
- concept_pages_updated: 7
- total_pages: 3

## [2026-05-16] ingest | Faith and Life (superseded — see fix below)
- book: Faith and Life
- slug: faith-and-life
- chapters: 1 (incorrect — all 4 chapters dumped into ch-01)
- chapter_pages: 1
- concept_pages_created: 1
- concept_pages_updated: 7
- total_pages: 3

## [2026-05-16] cross-ref
- pages_scanned: 61
- orphans: 0
- broken_links: 8
- links_added: 345

## [2026-05-16] lint | 75 issues found
- critical: 0
- warning: 67

## [2026-05-16] ingest-batch | 8 books ingested
- approaching-the-sunnah: 3 chapters, 12 concepts
- economic-security: 7 chapters, 5 concepts
- education-economy-sunnah: 2 chapters, 0 new concepts
- ethics-in-islam: 4 chapters, 2 concepts
- fiqh-al-zakah: 10 chapters, 2 concepts
- auspices-victory: 1 chapter, 1 concept
- diversion-arts: 1 chapter, 1 concept
- faith-and-life: 1 chapter, 1 concept
- Total wiki pages: 62 (37 entities + 25 concepts)
- Total outbound links: 456
- Cross-reference pass: 345 links added
- Lint: 0 critical issues, 0 broken links
- contemporary-fatwa-1: OCR needed (image-only PDF)
- 7 books restricted on Archive.org (pending browser download)

## [2026-05-16] lint | 9 issues found
- critical: 0
- warning: 1

## [2026-05-16] lint | 8 issues found
- critical: 0
- warning: 0

## [2026-05-16] fix | faith-and-life chapter re-split
- problem: All 4 chapters dumped into ch-01.txt due to page-header false positives
- action: Manually split full.txt at known boundaries (lines 265, 1244, 1664, 2603)
- added proper frontmatter with chapter titles
- re-ingested with --reingest flag
- result: 5 pages (1 overview + 4 chapters), 13 concept updates
- old entity files cleaned; index.md duplicates removed

## [2026-05-16] ingest | Faith and Life (re-ingest after fix)
- book: Faith and Life
- slug: faith-and-life
- chapters: 4
- chapter_pages: 4
- concept_pages_created: 0
- concept_pages_updated: 13
- total_pages: 5

## [2026-05-16] lint | 8 issues found
- critical: 0
- warning: 0

- [2026-06-09] [concept] Expanded concept-usury.md from stub to full concept page with content from Economic Security ch-01, ch-02, ch-07; Fiqh al-Zakah; Economy in the Sunnah; Ethics in Islam. Added definition, Qaradawi's position, evidence base, contemporary relevance, scholarly references, and cross-links.

- [2026-06-09] [concept] Expanded concept-prayer.md from stub to detailed concept page. Sources: Ethics in Islam ch-01 (moral purpose of prayer, void without ethics, communal dimension, moderation vs extremism, faith-prayer integration), Education & Economy in the Sunnah ch-01 (Prophetic individualisation, ṣalāh as best deed at proper time). Added 7 Qaradawi positions, 8 Qur'anic verses with references, 6 hadiths, classical comparison, contemporary relevance, and 7 cross-links.
- [2026-06-09] [concept] Expanded concept-jihad.md from stub to detailed concept page. Sources: Ethics in Islam (section-01-03: self-purification and jihad against desire; section-03-06: greater jihad as inner struggle; section-03-07: threefold striving worship/social good/resisting evil; section-04-02: greater jihad tradition; section-04-03: jihad as care for parents; ch-01: ethics of warfare and armed jihad constraints). Added definition, 6 Qaradawi positions (jihad al-nafs, greater/lesser jihad, parental duty, striving in Allah's cause, ethics of war, jihad against desire), evidence base with 9 Qur'anic verses and 5 hadiths, classical comparison, contemporary relevance, and 6 cross-links.
- [2026-06-09] [concept] Expanded concept-consensus.md from stub to detailed concept page. Sources: Approaching the Sunnah ch-02 (ijma' verification, ijma' as fabrication criterion, consensus on Sunnah's authority, ijma' establishing legal categories), Fiqh al-Zakah ch-04 (ijma' on zakah on trade assets), Ethics in Islam ch-02 (scope of consensus, Ibn Mas'ud on truth, moral consensus), Ethics in Islam ch-03 (four sources converge on Allah, moral obligation). Added definition, 7 Qaradawi positions, evidence base with 3 Qur'anic verses, 1 hadith, 2 companion statements, classical comparison, contemporary relevance, and 6 cross-links.
- [2026-06-09] [concept] Expanded concept-fiqh.md from stub to detailed concept page. Sources: Approaching the Sunnah ch-01 (Sunnah as exposition of Qur'an, balanced method), ch-02 (linking hadith and fiqh, duty of scholarly revision of fiqh legacy, all jurists refer to Sunnah, weak hadiths in fiqh books, zakah examples), ch-03 (understanding Sunnah in light of Qur'an, zakah on produce, bloodwit for dhimmis and women, preferring Quran-supporting juristic views), Fiqh al-Zakah ch-01 (definition of mal, conditions for zakatability, growth principle, zakah rates fixed by nusus and ijma', nisab of gold vs silver). Added definition, 5 Qaradawi positions, evidence base (5 Qur'anic verses, 5 key hadiths), comparison tables (zakah on produce, bloodwit for dhimmis, bloodwit for women, nisab for paper money), contemporary relevance, and 8 cross-links.
- [2026-06-09] [concept] Expanded concept-sharia.md from low-confidence stub to detailed concept page with medium confidence. Sources: Diversion and Arts ch-01 (torch of Shariah and Fiqh, middle course, original permissibility principle, halal/haram extremes), ch-04 (al-Asl principle, Sharia's intrinsic tolerance and middle ground, Ghazali's methodology, hadiths on permissibility), ch-06 (abrogation of earlier dispensations), ch-07 (moderation and middle course in jest), Ethics in Islam ch-04 (Maqasid al-Sharia via al-Asfahani's three objectives, Sharia and animal welfare, Sharia as bond of Ummah, conditional obedience to rulers, Al-Siyasa Al-Shar'iyya reference), Fiqh al-Zakah (Qaradawi as Dean of Shariah College). Added 9 Qaradawi positions, evidence base (10 Qur'anic verses, 3 hadiths, 3 classical references), comparison table with all 4 madhhabs, and 6 contemporary relevance items.
- [2026-06-09] [concept] Expanded concept-fasting.md from stub to detailed concept page. Sources: Approaching the Sunnah ch-01 (concessions in fasting, principle of ease), ch-03 (crescent-sighting vs astronomical calculation, al-Subki's ruling, ends vs means), Ethics in Islam section-00 & ch-01 (fasting and moral transformation, fasting without ethics is void), Faith and Life ch-03 (moderation in fasting, hadith of Abdullah ibn Amr on fasting of Dawud), Education & Economy in the Sunnah ch-01 (context-dependent fatwa, kissing while fasting), Diversion & Arts ch-04 (Eid al-Fitr). Added 5 Qaradawi positions (moral-spiritual inseparability, middle path vs asceticism, crescent calculation, concessions/ease, fatwa adaptability), evidence base (2 Qur'anic verses, 6 hadiths), comparison tables (crescent-sighting, concessions), 3 key sub-topics, 5 contemporary relevance items, and 6 cross-links. Confidence: low→medium.
|- [2026-06-09] [concept] Expanded concept-purity.md from stub to detailed concept page. Sources: Approaching the Sunnah ch-01 (concessions in purification, tayammum in janabah, wounded man hadith, principle of ease), Ethics in Islam section-00 (worship and moral purification linked), section-01-04 (Prophet's mission of tazkiyyah, 6 Qur'anic purification verses), section-01-01 (Prophetic purification mission in 4 Qur'anic passages), Education & Economy in the Sunnah ch-02 (economy in ablution, Sa'd hadith on water waste), Faith & Life ch-01 (Islam dignifies the body vs materialist denigration). Added 6 Qaradawi positions (purification as Prophetic mission, moral/economic dimensions of wudu, concessions in taharah, over-scrupulousness warning, spiritual/moral interdependence, body dignity), evidence base (7 Qur'anic verses, 5 hadiths), comparison tables (tayammum, over-scrupulousness), 5 key sub-topics (wudu, ghusl, tayammum, najasah, tazkiyyah), 4 contemporary relevance items, and 6 cross-links. Confidence: low→medium.
- [2026-06-09] [concept] Expanded concept-hajj.md from stub to detailed concept page (7 Qaradawi positions). Sources: Approaching the Sunnah ch-02 (Prophet's strategic patience and ʿumrah at Kaʿbah with idols present), ch-03 (hajj as expiation, women's travel for hajj without maḥram, ʿĀʾishah's hajj precedent, Shāfiʿī and Ibn Ḥazm positions on safe travel, weights of Makkah / measures of Madinah), Economic Security ch-05 (hajj sacrifice types — kaffārah, tamattuʿ, qirān; Qur'an 5:95 and 2:196; social welfare dimension of sacrificial meat; Qur'an 22:28 and 22:36), ch-07 (Prophetic hadith of ʿAdī ibn Ḥātim: woman travelling safely from Ḥīrah to Kaʿbah), Fiqh al-Zakah ch-02 (pilgrimage and sacrifice analogy for livestock zakat rates), ch-03 (pilgrimage cost as non-deductible debt from zakatable wealth), ch-05 (Abū Yūsuf changing view after pilgrimage; saʿ needed for hajj expiation; ihram dual obligation analogy for ʿushr+kharāj). Added: definition, 7 positions (expiation, sacrifice types/significance, hajj as civilisational barometer, women's maḥram, strategic patience, metrological standards, zakah-hajj interactions), evidence base (4 Qur'anic verses, 3 hadiths), comparison across 4 madhhab positions, 5 contemporary relevance items, 8 cross-links. Confidence: low→medium.
- [2026-06-09] [concept] Replaced concept-pilgrimage.md with redirect alias page pointing to concept-hajj. Removed duplicate concept-pilgrimage entry from index.md. Updated concepts-index.md duplicate notes.

- [2026-06-09] [concept] Expanded concept-marriage.md from stub to detailed concept page. Sources: Ethics in Islam ch-01 (marriage as social foundation, mahr, mutual affection/mercy, spouse selection, prohibition of fornication, affordable marriage), ch-04 and section-04-03 (family ethics: engagement, prohibited partners, People of the Book, dowry, marital kindness, children, sexual rights), section-02-05 (monasticism vs marriage), Economic Security ch-01 (poverty as barrier to marriage, Q 24:32-33), ch-03 (husband's maintenance obligation), ch-04 (zakat for marriage, Umar's precedent). Added 10 Qaradawi positions (social foundation, anti-celibacy, affordable dowry, spouse selection, engagement limits, zakat for marriage, affection/mercy, prohibited categories, kinship bonds, fornication prohibition), evidence base (18 Qur'anic verses, 11 hadiths), comparison table with 4 madhhabs, and 6 contemporary relevance items. Confidence: low→high.

## [2026-06-09] P1 completion | Deep content pass

### P1-1: Concept definitions (20 complete, 3 redirects)
- Expanded 20 concept pages from stubs to full scholarly definitions with Qaradawi's positions, evidence base, classical comparison, and contemporary relevance
- Merged 3 duplicates: concept-zakah→concept-zakat, concept-ijma→concept-consensus, concept-salah→concept-prayer, concept-pilgrimage→concept-hajj
- Updated concepts-index.md with merged entries and redirect notes

### P1-2: Book overview synopses (8 books)
- Replaced all 8 generic stub overviews ("This book by Dr. Yusuf al-Qaradawi addresses [domain].") with proper 200-400 word scholarly synopses grounded in source text
- Each synopsis covers: purpose/motivation, central thesis, distinctive contribution, key topics

### P1-3: Chapter summaries (36 chapters)
- Replaced all "## Preview" sections (raw text dumps) with "## Summary" sections containing 150-250 word scholarly summaries
- Removed broken "See also" cross-links from Fiqh al-Zakah (10 chapters), Economic Security (7), Education & Economy (2), Approaching the Sunnah (3)
- Covered: Fiqh al-Zakah 10, Economic Security 7, Ethics in Islam 4, Approaching the Sunnah 3, Diversion & Arts 7, Auspices of Victory 8, Education & Economy 2, Faith & Life 4

### Verification
- 0 pages with "Definition pending" stubs
- 0 pages with generic book overview stub text
- 0 pages with "## Preview" sections
- 83 total markdown pages, 59M wiki size

## [2026-06-09] extract
- book: The Lawful and the Prohibited in Islam
- slug: halal-haram
- status: FAILED — OCR needed

## [2026-06-09] create | comparison-zakat-economic-justice
- Created comparison page: comparisons/comparison-zakat-economic-justice.md
- Sources: FZ ch-01 & ch-04, ES ch-04 & ch-05, EES ch-02
- Cross-references: 8 wikilinks to entity pages and concept pages
- Updated index.md: added entry under Comparisons section

## [2026-06-09] create | comparison-sunnah-methodology
- Created comparison page: comparisons/comparison-sunnah-methodology.md
- Sources: Approaching the Sunnah (ch-01, ch-02, ch-03), Fiqh al-Zakah (ch-01, ch-02, ch-03, ch-05, ch-09, ch-10), Ethics in Islam (ch-01–ch-04), Education & Economy in the Sunnah (ch-01, ch-02)
- Cross-references: 15+ wikilinks to entity pages, concept pages, and other comparison
- Thorough analysis of how hadith methodology varies across fiqh (legal evidence), ethics (moral exempla), and education (pedagogical model)
- Key sections: unified framework, fiqh application (general text rule, chain criticism, ijtihad), ethics application (authentication thresholds, fabrication rebuttal), education application (pedagogical model), comparative tables, tensions and resolutions
- Updated index.md: added entry under Comparisons section, bumped total pages to 72+

## [2026-06-09] create | comparison-wasatiyyah-moderation
- Created comparison page: comparisons/comparison-wasatiyyah-moderation.md
- Sources: Approaching the Sunnah (ch-01), Ethics in Islam (ch-01), Diversion and Arts (ch-01, ch-07), Auspices of Victory (ch-01, ch-07), Faith and Life (ch-02, ch-03)
- Cross-references: 14+ wikilinks to entity pages, concept pages, and other comparison
- Thorough analysis of how wasatiyyah operates as Qaradawi's master framework across 5 domains: fiqh (balanced Sunnah as hermeneutical criterion), ethics (moderation in worship and moral practice), lifestyle (middle course between asceticism and indulgence), eschatology (steering between despair and complacency), spirituality (material-spiritual balance in iman)
- Key sections: structural parallels table, recurring proof-text pattern analysis, wasatiyyah as hermeneutical principle vs. substantive content, role of ijtihad, key tensions and resolutions, conclusion establishing wasatiyyah as architectonic framework
- Updated index.md: added entry under Comparisons section, bumped total pages to 73+

## [2026-06-09] create | comparison-halal-haram-permissibility
- Created comparison page: comparisons/comparison-halal-haram-permissibility.md
- Sources: Diversion and Arts (ch-01, ch-04, ch-05, ch-06), Fiqh al-Zakah (ch-01), Ethics in Islam (ch-01, ch-04), Economic Security (ch-02)
- Cross-references: 15+ wikilinks to entity pages, concept pages, and other comparison
- Thorough analysis of how Qaradawi's permissibility principle (al-aṣl fī al-ashyāʾ al-ibāḥah) operates across fiqh, ethics, and lifestyle contexts
- Key sections: core principle definition, lifestyle context (music/arts graduated rulings), legal context (zakatability and halal wealth), ethical context (intention as moral axis), economic context (trusteeship and riba), comparative tables (permissibility across 4 contexts, two extremes in each, intention function, graduated scales), principle as signature method (5 dimensions), convergence points, cross-references
- Updated index.md: added entry under Comparisons section

## [2026-06-09] lint | 232 issues found
- critical: 189
- warning: 34
- info: 9

## [2026-06-09] lint | 232 issues found
- critical: 189
- warning: 34
- info: 9

## [2026-06-09] lint | 232 issues found
- critical: 189
- warning: 34
- info: 9

## [2026-06-09] lint | 247 issues found
- critical: 202
- warning: 36

## [2026-06-09] create | 5 concept pages
- concept-niyyah.md — redirect to concept-intention (Niyyah / نِيَّة)
- concept-singing.md — Singing / Ghina' (غِنَاء); full concept page with 7 references
- concept-music.md — Music / Musiqa (مُوسِيقَى); full concept page with 6 references
- concept-taqwa.md — Taqwa / God-consciousness (تَقْوَى); full concept page with 6 references
- concept-piety.md — redirect to concept-taqwa (Birr / بِرّ)
- Updated concepts-index.md with 3 new entries and 2 redirect notes
- info: 9

## [2026-06-09] create | 5 concept pages (faith, justice, punishment, art, ethics)
- concept-faith.md — Faith/Iman (إيمان); full concept page with 23 references, mainly from Faith and Life
- concept-justice.md — Justice/Adalah (عدل); full concept page with 20 references, mainly from Ethics in Islam
- concept-punishment.md — Punishment/Uqubah (عقوبة); full concept page with 11 references, mainly from Ethics in Islam and Diversion & Arts
- concept-art.md — Art/Fann (فن); full concept page with 38 references, mainly from Diversion and Arts
- concept-ethics.md — redirect to concept-character (Akhlaq/أخلاق = ethics = character)
- Updated concepts-index.md with 4 new entries + 1 redirect note
- Updated concept-character.md with ethics alias + cross-links
- Updated index.md Concepts table with 5 new rows

## [2026-06-09] lint | 138 issues found
- critical: 71
- warning: 57
- info: 10

## [2026-06-09] lint | 138 issues found
- critical: 71
- warning: 57
- info: 10

## [2026-06-09] lint | 138 issues found
- critical: 71
- warning: 57
- info: 10

## [2026-06-09] lint | 138 issues found
- critical: 71
- warning: 57
- info: 10

## [2026-06-09] create | scholar-qaradawi
- Written: /root/qaradawi-library/entities/scholar-qaradawi.md
- Type: scholar page
- Sources: All 9 book overview pages, web biographical research (Wikipedia, Muslim 500, Al Jazeera, AMUST, Encyclopedia.com)
- Sections: Biography, Intellectual Methodology, Major Works, Key Positions, Legacy and Influence, Cross-References
- Updated: /root/qaradawi-library/index.md — added Scholars section with link to scholar-qaradawi

## [2026-06-09] P3-1: Scholar Page Created
- Created scholar-qaradawi.md: comprehensive biography (14KB, 7 sections)
- Added Scholars section to index.md
- Corrected death date to 2022-09-26 (not 2026)

## [2026-06-09] lint | 141 issues found
- critical: 70
- warning: 60
- info: 11

## [2026-06-09] lint | 190 issues found
- critical: 39
- warning: 133
- info: 18

## [2026-06-09] lint | 190 issues found
- critical: 39
- warning: 133
- info: 18

## [2026-06-09] lint | 190 issues found
- critical: 39
- warning: 133
- info: 18

## [2026-06-09] lint | 190 issues found
- critical: 39
- warning: 133
- info: 18

## [2026-06-09] lint | 190 issues found
- critical: 39
- warning: 133
- info: 18

## [2026-06-09] lint | 181 issues found
- critical: 30
- warning: 133
- info: 18

## [2026-06-09] lint | 181 issues found
- critical: 30
- warning: 133
- info: 18

## [2026-06-09] lint | 181 issues found
- critical: 30
- warning: 133
- info: 18

## [2026-06-09] lint | 181 issues found
- critical: 30
- warning: 133
- info: 18

## [2026-06-09] lint | 130 issues found
- critical: 10
- warning: 101
- info: 19

## [2026-06-09] lint | 130 issues found
- critical: 10
- warning: 101
- info: 19

## [2026-06-09] lint | 130 issues found
- critical: 10
- warning: 101
- info: 19

## [2026-06-09] lint | 112 issues found
- critical: 10
- warning: 91
- info: 11

## [2026-06-09] lint | 112 issues found
- critical: 10
- warning: 91
- info: 11

## [2026-06-09] lint | 136 issues found
- critical: 0
- warning: 116
- info: 20

## [2026-06-09] lint | 136 issues found
- critical: 0
- warning: 116
- info: 20

## [2026-06-09] lint | 163 issues found
- critical: 0
- warning: 143
- info: 20


## [2026-06-09] P3: Scholar Page, Concept Stubs, Cross-Reference Sweep

- Created scholar-qaradawi.md: comprehensive biography (161 lines, 14KB, 7 sections)
- Created 31 concept pages (10 redirects + 21 stubs): akhlaq, charity, darurah, dawah, halal-haram, hudud, ikhlas, isnad, mal, morality, nisab, hawl, obligation, patience, qiyas, quran, responsibility, riba, riya, sabr, sadaqah, shariah, taharah, tajdid, tawhid, tazkiyah, usul-al-fiqh, waqf, wasatiyyah, wisdom, zakah
- Fixed 31 broken concept links (0 remaining)
- Fixed 9 escaped wikilinks in scholar-qaradawi.md
- Fixed all 10 redirect pages with proper YAML frontmatter
- Rewrote index.md: clean structure, accurate counts, no escaped wikilinks
- Updated concepts-index.md: 48 concepts + 16 redirects
- Final lint: 0 CRITICAL, 143 WARNING (all tags/orphans), 20 INFO
- Wiki total: 135 .md pages, 9.4M extracted corpus, 9 books, 50 chapters, 4 comparisons, 1 scholar page


## [2026-06-09] P4: Federation, Cross-Wiki, and Final Polish

- Updated LLM Wiki hub: wikis.yaml, index.md, active-wiki-map.md
- Created cross-wiki bridge page: meta/concepts/cross-wiki-bridge-qaradawi-quran.md
- Created federated query templates: meta/concepts/federated-query-templates.md
- Verified federated_query.py works across Quran Wiki and Qaradawi Library
- 13 key thematic bridges documented (zakat, sunnah, halal/haram, ethics, faith)
- Shared concept table: 13 concepts mapped across both wikis
- Final wiki stats: 135 .md pages, 9.4M corpus, 0 critical lint issues

## [2026-06-09] lint | 163 issues found
- critical: 0
- warning: 143
- info: 20

## [2026-06-09] lint | 163 issues found
- critical: 0
- warning: 143
- info: 20
