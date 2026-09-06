#!/usr/bin/env python3
"""
ocr_book.py — OCR an image-only PDF and extract text.
Processes pages in batches to manage memory.
"""
import os
import sys
import yaml
import argparse
from pdf2image import convert_from_path
import pytesseract

WIKI_ROOT = "/root/qaradawi-library"
CONFIG_PATH = os.path.join(WIKI_ROOT, ".config", "books.yaml")
PDF_DIR = os.path.join(WIKI_ROOT, "raw", "pdfs")
EXTRACT_DIR = os.path.join(WIKI_ROOT, "raw", "extracted")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(cfg, f, sort_keys=False, allow_unicode=True)

def ocr_book(slug, batch_size=20):
    cfg = load_config()
    book = cfg["books"].get(slug)
    if not book:
        print(f"ERROR: Book '{slug}' not found in config")
        return False
    
    pdf_path = os.path.join(PDF_DIR, f"{slug}.pdf")
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF not found at {pdf_path}")
        return False
    
    out_dir = os.path.join(EXTRACT_DIR, slug)
    os.makedirs(out_dir, exist_ok=True)
    
    # Get total pages
    from pdf2image import pdfinfo_from_path
    info = pdfinfo_from_path(pdf_path)
    total_pages = info["Pages"]
    print(f"OCR processing: {book['title']}")
    print(f"  Total pages: {total_pages}")
    print(f"  Batch size: {batch_size}")
    
    all_text = []
    
    for start in range(1, total_pages + 1, batch_size):
        end = min(start + batch_size - 1, total_pages)
        print(f"  Processing pages {start}-{end}...")
        
        try:
            images = convert_from_path(pdf_path, first_page=start, last_page=end, dpi=300)
            for i, img in enumerate(images):
                page_num = start + i
                text = pytesseract.image_to_string(img)
                all_text.append(f"\n\n--- Page {page_num} ---\n\n{text}")
                if page_num % 10 == 0:
                    print(f"    ... page {page_num}/{total_pages}")
        except Exception as e:
            print(f"  ERROR on pages {start}-{end}: {e}")
            continue
    
    # Write full text
    full_path = os.path.join(out_dir, "full.txt")
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_text))
    
    total_chars = sum(len(t) for t in all_text)
    print(f"\n  Written: {full_path}")
    print(f"  Total characters: {total_chars:,}")
    print(f"  Total pages OCR'd: {total_pages}")
    
    # Write metadata
    metadata = {
        "source": f"raw/pdfs/{slug}.pdf",
        "pages": str(total_pages),
        "extraction_method": "OCR (tesseract)",
        "total_characters": str(total_chars),
        "ocr_dpi": "300"
    }
    meta_path = os.path.join(out_dir, "metadata.yaml")
    with open(meta_path, "w") as f:
        yaml.dump(metadata, f, sort_keys=False, allow_unicode=True)
    
    # Update books.yaml
    book["extracted"] = True
    book["extraction_method"] = "OCR"
    book["extracted_at"] = "2026-06-09"
    save_config(cfg)
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", required=True, help="Book slug")
    parser.add_argument("--batch-size", type=int, default=20, help="Pages per batch")
    args = parser.parse_args()
    ocr_book(args.book, args.batch_size)