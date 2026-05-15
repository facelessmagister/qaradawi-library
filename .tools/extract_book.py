#!/usr/bin/env python3
"""
extract_book.py — Extract text from PDFs and split into chapters

Usage:
    python3 extract_book.py --book halal-haram
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
import yaml

WIKI_ROOT = "/root/qaradawi-library"
CONFIG_PATH = os.path.join(WIKI_ROOT, ".config", "books.yaml")
PDF_DIR = os.path.join(WIKI_ROOT, "raw", "pdfs")
EXTRACT_DIR = os.path.join(WIKI_ROOT, "raw", "extracted")
LOG_PATH = os.path.join(WIKI_ROOT, "log.md")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(cfg, f, sort_keys=False, allow_unicode=True)


def append_log(action, details):
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## [{today}] {action}\n"
    for k, v in details.items():
        entry += f"- {k}: {v}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_pdftotext(pdf_path, txt_path):
    cmd = ["pdftotext", "-layout", pdf_path, txt_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: pdftotext failed: {e.stderr}")
        return False


def run_pdfinfo(pdf_path):
    cmd = ["pdfinfo", pdf_path]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        info = {}
        for line in result.stdout.strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                info[key.strip()] = val.strip()
        return info
    except Exception as e:
        print(f"  WARNING: pdfinfo failed: {e}")
        return {}


def detect_chapter_boundaries(text):
    """
    Heuristic chapter detection for Islamic scholarly texts.
    Returns list of (chapter_num, start_line, title_or_none).
    """
    lines = text.split("\n")
    chapters = []
    # Pattern: "CHAPTER 1", "Chapter 1", "CHAPTER ONE", "Chapter One"
    # Also: Arabic chapter markers like "الفصل الأول"
    chapter_re = re.compile(
        r"^(?:CHAPTER|Chapter)\s+(\d+|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|Twenty)[\.:\s]*(.*)$",
        re.IGNORECASE,
    )
    # Arabic numerals: "الفصل الأول", "الباب الأول"
    arabic_chapter_re = re.compile(
        r"^\s*(?:الفصل|الباب|المبحث)\s+(?:الأول|الثاني|الثالث|الرابع|الخامس|السادس|السابع|الثامن|التاسع|العاشر|\d+)\s*$"
    )

    for i, line in enumerate(lines):
        stripped = line.strip()
        m = chapter_re.match(stripped)
        if m:
            num_str = m.group(1)
            title = m.group(2).strip() if m.group(2) else None
            try:
                num = int(num_str)
            except ValueError:
                # Word to number mapping
                word_map = {
                    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
                    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
                    "nineteen": 19, "twenty": 20,
                }
                num = word_map.get(num_str.lower(), len(chapters) + 1)
            chapters.append((num, i, title))
            continue
        if arabic_chapter_re.match(stripped):
            chapters.append((len(chapters) + 1, i, stripped))

    return chapters


def split_into_chapters(text, boundaries):
    """Split text at chapter boundaries. Returns dict: chapter_num -> text."""
    lines = text.split("\n")
    if not boundaries:
        return {1: text}

    chapters = {}
    for idx, (num, start_line, title) in enumerate(boundaries):
        end_line = boundaries[idx + 1][1] if idx + 1 < len(boundaries) else len(lines)
        chapter_lines = lines[start_line:end_line]
        chapters[num] = "\n".join(chapter_lines)

    return chapters


def extract_book(slug, cfg_data):
    books = cfg_data.get("books", {})
    if slug not in books:
        print(f"ERROR: Book '{slug}' not found in registry")
        return False

    book = books[slug]
    if not book.get("downloaded"):
        print(f"ERROR: Book '{slug}' not downloaded. Run download_book.py first.")
        return False
    if book.get("extracted") and not book.get("ocr_needed"):
        print(f"Book '{slug}' already extracted. Use --force to re-extract.")
        return True

    pdf_path = os.path.join(PDF_DIR, f"{slug}.pdf")
    extract_path = os.path.join(EXTRACT_DIR, slug)
    os.makedirs(extract_path, exist_ok=True)

    print(f"Extracting: {book['title']}")
    print(f"  PDF: {pdf_path}")

    # Step 1: PDF info
    info = run_pdfinfo(pdf_path)
    metadata = {
        "title": info.get("Title", book["title"]),
        "author": info.get("Author", "Yusuf al-Qaradawi"),
        "pages": info.get("Pages", "unknown"),
        "pdf_sha256": sha256_file(pdf_path),
    }
    metadata_path = os.path.join(extract_path, "metadata.yaml")
    with open(metadata_path, "w") as f:
        yaml.dump(metadata, f, allow_unicode=True)

    # Step 2: Full text extraction
    full_txt = os.path.join(extract_path, "full.txt")
    if not run_pdftotext(pdf_path, full_txt):
        # Check if output is empty or tiny
        if os.path.exists(full_txt) and os.path.getsize(full_txt) < 1000:
            print("  WARNING: Extracted text is very small — PDF may be image-only.")
            book["ocr_needed"] = True
            save_config(cfg_data)
            append_log("extract", {
                "book": book["title"],
                "slug": slug,
                "status": "FAILED — OCR needed",
            })
            return False
        return False

    # Step 3: Read full text
    with open(full_txt, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    if len(text.strip()) < 5000:
        print("  WARNING: Very little text extracted. PDF may be image-only or heavily formatted.")
        book["ocr_needed"] = True
        save_config(cfg_data)
        append_log("extract", {
            "book": book["title"],
            "slug": slug,
            "status": "FAILED — OCR needed",
        })
        return False

    # Step 4: Detect chapter boundaries and split
    boundaries = detect_chapter_boundaries(text)
    print(f"  Detected {len(boundaries)} chapter boundaries")

    if not boundaries:
        print("  No chapter boundaries detected. Treating as single chapter.")
        chapters = {1: text}
    else:
        chapters = split_into_chapters(text, boundaries)

    # Step 5: Write chapter files with frontmatter
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    chapter_count = 0
    for num, ch_text in sorted(chapters.items()):
        ch_path = os.path.join(extract_path, f"ch-{num:02d}.txt")
        title = None
        for b_num, _, b_title in boundaries:
            if b_num == num:
                title = b_title
                break

        frontmatter = f"""---
source_url: {book['archive_url']}
ingested: {today}
book: {slug}
chapter: {num}
title: {title or f'Chapter {num}'}
sha256: {sha256_file(full_txt)}
---

"""
        with open(ch_path, "w", encoding="utf-8") as f:
            f.write(frontmatter + ch_text)
        chapter_count += 1
        print(f"    Written: ch-{num:02d}.txt ({len(ch_text)} chars)")

    # Step 6: Update config
    book["extracted"] = True
    book["extracted_at"] = today
    book["chapters"] = chapter_count
    save_config(cfg_data)

    append_log("extract", {
        "book": book["title"],
        "slug": slug,
        "chapters": chapter_count,
        "total_chars": len(text),
        "status": "SUCCESS",
    })

    print(f"  SUCCESS: {chapter_count} chapters extracted to {extract_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Extract text from Qaradawi PDFs")
    parser.add_argument("--book", required=True, help="Book slug to extract")
    parser.add_argument("--force", action="store_true", help="Re-extract even if already done")
    args = parser.parse_args()

    cfg = load_config()
    extract_book(args.book, cfg)


if __name__ == "__main__":
    main()
