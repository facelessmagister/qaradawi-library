#!/usr/bin/env python3
"""
clean_extracted.py — Fix common pdftotext extraction artifacts in Qaradawi Library extracts.

Run this before regenerating the website to produce clean chapter content.

Usage:
    python3 .tools/clean_extracted.py
    python3 .tools/clean_extracted.py --book faith-and-life
"""
import argparse, os, re, glob, sys

WIKI_ROOT = "/root/qaradawi-library"
EXTRACT_DIR = os.path.join(WIKI_ROOT, "raw", "extracted")

# Common patterns: standalone leading "e" before headers — this is the PDF bullet character
PDF_BULLET_PATTERN = re.compile(r'^[ \t]*e[ \t]+', re.MULTILINE)
# Fix common OCR confusion: J → I (e.g., "Jman" → "Iman", "Jslam" → "Islam")
J_CONFUSION = re.compile(r'\bJ(man|slam|man|slamic|slamist|manity|nsha|qra|shaa|shaa)\b', re.IGNORECASE)
# Fix other common garbled characters from PDF extraction
# Form feed artifacts
FORMFEED_CLEAN = re.compile(r'\f+')
# Page number + header noise: "4     Faith and Life" or similar
PAGE_HEADER_PATTERN = re.compile(r'^\s*\d+\s+Faith and Life\s*$', re.MULTILINE | re.IGNORECASE)
# Repeated whitespace collapse
WHITESPACE_COLLAPSE = re.compile(r'[ \t]{2,}')
# Fix broken words: "Jman" → "Iman", "Jslam" → "Islam"
# Also handle common PDF-to-text rendering issues
FIXES = [
    (re.compile(r'\bJman\b', re.IGNORECASE), 'Iman'),
    (re.compile(r'\bJ(man|SLAM|slam|slamic|slamist|manity)\b', re.IGNORECASE), 
     lambda m: 'I' + m.group(1).lower() if m.group(1)[0].lower() == 's' else 'I' + m.group(1)),
    (re.compile(r'\bsLlam\b', re.IGNORECASE), 'Islam'),
    (re.compile(r'\bslamic\b', re.IGNORECASE), 'Islamic'),
    (re.compile(r'\bjman\b', re.IGNORECASE), 'Iman'),
    (re.compile(r'\bJ\s+man\b', re.IGNORECASE), 'Iman'),
    (re.compile(r'\bJ\s+slam\b', re.IGNORECASE), 'Islam'),
]


def clean_text(text):
    """Apply all cleaning transformations to extracted text."""
    # Remove form feeds
    text = FORMFEED_CLEAN.sub('\n\n', text)
    
    # Remove PDF bullet dots (standalone "e " at line start)
    text = PDF_BULLET_PATTERN.sub('', text)
    
    # Fix "Jman" → "Iman", "Jslam" → "Islam" etc.
    text = re.sub(r'\bJman\b', 'Iman', text, flags=re.IGNORECASE)
    text = re.sub(r"\bJ(man's|man|slamic|slamist|slam)\b", lambda m: 'I' + m.group(1).lower(), text, flags=re.IGNORECASE)
    text = re.sub(r'\bJ Man\b', 'Iman', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJ Islam\b', 'Islam', text, flags=re.IGNORECASE)
    
    # Remove page headers and footers: "4     Faith and Life" or "Chapter One"
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        s = line.strip()
        # Skip page number + book title headers
        if re.match(r'^\d+\s+Faith and Life\s*$', s, re.IGNORECASE):
            continue
        if re.match(r'^(Chapter|CHAPTER)\s+(One|Two|Three|Four|[0-9]+)\s*$', s, re.IGNORECASE):
            if not cleaned_lines:  # Only skip if at top
                continue
        # Skip "Chapter One 5" page footer patterns
        if re.match(r'^Chapter\s+(One|Two|Three|Four)\s+\d+$', s, re.IGNORECASE):
            continue
        # Skip standalone "Chapter One" at start of paragraph block
        if s == 'Chapter One' or s == 'Chapter Two' or s == 'Chapter Three' or s == 'Chapter Four':
            continue
        cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)
    
    # Remove "Chapter One X" that got inline with text
    text = re.sub(r'Chapter\s+(One|Two|Three|Four)\s+\d+', '', text, flags=re.IGNORECASE)
    
    # Fix garbled symbols
    text = text.replace('€', '"')
    text = text.replace('®', '"')
    text = text.replace('«', '"')
    text = text.replace('»', '"')
    # "4We" → " «We" or "We" (page number 4 before verse)
    text = re.sub(r'\b\d+We\b', '"We', text)
    text = re.sub(r'\b\d+Allah\b', 'Allah', text)  # page num before Allah
    text = re.sub(r'\b\d+Behold\b', 'Behold', text)
    # "(AF Isra'" → "(Al-Isra'" 
    text = re.sub(r'\(AF\s+', '(Al-', text)
    text = re.sub(r'\(Al-Baga\s+To\b', '(Al-Baqarah: 115). To', text)
    text = re.sub(r'\(Al-Bagarah', '(Al-Baqarah', text, flags=re.IGNORECASE)
    text = re.sub(r'\(Qaf:\s*16\)\s*€', '(Qaf: 16) "', text)
    text = re.sub(r'\(Al-Mujadalah:\s*7\)\s*The', '(Al-Mujadalah: 7). The', text)
    text = re.sub(r'"\)\s*This\s+is', '"). This is', text)
    text = re.sub(r'\(Al- Alaq', '(Al-Alaq', text)
    text = re.sub(r':\s*1-5\)', ': 1-5)', text)
    text = re.sub(r"\(Az-Zumar:\s*72\)\s*This", '(Az-Zumar: 72). This', text)
    # Broken hadith end markers
    text = re.sub(r'""\)', '"', text)
    text = re.sub(r"'\)\)", "'", text)
    text = re.sub(r'\)\)', ')', text)
    # "ifyou" → "if you"
    text = re.sub(r'\bifyou\b', 'if you', text, flags=re.IGNORECASE)
    text = re.sub(r'\bIfyou\b', 'If you', text)
    # Common fused words from PDF extraction
    text = re.sub(r'\bhimselfa\b', 'himself a', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhimselfb\b', 'himself b', text, flags=re.IGNORECASE)
    # "ofhimself" → "of himself", "tohimself" → "to himself"
    text = re.sub(r'\bofhimself\b', 'of himself', text, flags=re.IGNORECASE)
    text = re.sub(r'\btohimself\b', 'to himself', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbyhimself\b', 'by himself', text, flags=re.IGNORECASE)
    text = re.sub(r'\bforhimself\b', 'for himself', text, flags=re.IGNORECASE)
    text = re.sub(r'\bwithhimself\b', 'with himself', text, flags=re.IGNORECASE)
    text = re.sub(r'\bofhim\b', 'of him', text, flags=re.IGNORECASE)
    text = re.sub(r'\btohim\b', 'to him', text, flags=re.IGNORECASE)
    text = re.sub(r'\bforhim\b', 'for him', text, flags=re.IGNORECASE)
    text = re.sub(r'\bwithhim\b', 'with him', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbyhim\b', 'by him', text, flags=re.IGNORECASE)
    text = re.sub(r'\bfromhim\b', 'from him', text, flags=re.IGNORECASE)
    text = re.sub(r'\bathim\b', 'at him', text, flags=re.IGNORECASE)
    text = re.sub(r'\binhim\b', 'in him', text, flags=re.IGNORECASE)
    text = re.sub(r'\bonhim\b', 'on him', text, flags=re.IGNORECASE)
    text = re.sub(r'\bandhim\b', 'and him', text, flags=re.IGNORECASE)
    text = re.sub(r'\bthathim\b', 'that him', text, flags=re.IGNORECASE)
    # Common PDF-to-text errors
    text = re.sub(r'\bF\s+scommand\b', 'by His command', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsciel\s+ntist\b', 'scientist', text, flags=re.IGNORECASE)
    text = re.sub(r'\bifye\b', 'if you', text, flags=re.IGNORECASE)
    text = re.sub(r'\bIfye\b', 'If you', text)
    text = re.sub(r'\bOfthe\b', 'Of the', text)
    text = re.sub(r'\bofthe\b', 'of the', text, flags=re.IGNORECASE)
    text = re.sub(r'\b1\s+created\b', 'I created', text, flags=re.IGNORECASE)
    text = re.sub(r'\b1\s+know\b', 'I know', text, flags=re.IGNORECASE)
    text = re.sub(r'\b1\s+am\b', 'I am', text, flags=re.IGNORECASE)
    text = re.sub(r'\b1\s+will\b', 'I will', text, flags=re.IGNORECASE)
    text = re.sub(r'\b1\s+have\b', 'I have', text, flags=re.IGNORECASE)
    # Footnote markers
    text = re.sub(r'["\']\)+\s*', '" ', text)
    # "1. Narrated by..." footnote reference
    text = re.sub(r'\n\s*\d+\.\s*Narrated.*?\n', '\n', text, flags=re.IGNORECASE)
    # "Chapter One  it" — page number footers
    text = re.sub(r'Chapter\s+(One|Two|Three|Four)\s+\w+', '', text, flags=re.IGNORECASE)
    # Remove standalone "Faith and Life" headers/footers
    text = re.sub(r'\n\s*Faith and Life\s*\n', '\n\n', text, flags=re.IGNORECASE)
    # "Chapter One" standalone anywhere
    text = re.sub(r'\n\s*Chapter\s+(One|Two|Three|Four)\s*\n', '\n', text, flags=re.IGNORECASE)
    
    # Collapse excessive whitespace
    text = re.sub(r'[ \t]{3,}', '  ', text)
    
    # Clean up double newlines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    return text


def count_artifacts(text):
    """Count remaining artifacts in text."""
    counts = {
        'pdf_bullets': len(PDF_BULLET_PATTERN.findall(text)),
        'form_feeds': text.count('\f'),
        'jman': len(re.findall(r'\bJ\s*[Mm]an\b', text)),
        'jslam': len(re.findall(r'\bJ\s*[Ss]lam\b', text)),
    }
    return counts


def process_book(slug):
    """Clean all extracted chapter files for a single book."""
    book_dir = os.path.join(EXTRACT_DIR, slug)
    if not os.path.isdir(book_dir):
        print(f"  SKIP: {slug} — no extracted directory")
        return 0, 0, {}
    
    files = sorted(glob.glob(os.path.join(book_dir, "ch-*.txt")))
    if not files:
        print(f"  SKIP: {slug} — no chapter files")
        return 0, 0, {}
    
    total_files = 0
    total_changes = 0
    total_counts = {}
    
    for ch_file in files:
        with open(ch_file, 'r', encoding='utf-8', errors='replace') as f:
            original = f.read()
        
        # Separate frontmatter if present
        body = original
        frontmatter = ''
        if original.startswith('---'):
            parts = original.split('---', 2)
            if len(parts) >= 3:
                frontmatter = '---' + parts[1] + '---\n\n'
                body = parts[2]
        
        cleaned_body = clean_text(body)
        
        # Check if any changes were made
        before_counts = count_artifacts(body)
        after_counts = count_artifacts(cleaned_body)
        changes = sum(before_counts.values()) - sum(after_counts.values())
        
        if changes > 0 or cleaned_body != body:
            new_content = frontmatter + cleaned_body
            with open(ch_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            total_files += 1
            total_changes += changes
        
        for k, v in after_counts.items():
            total_counts[k] = total_counts.get(k, 0) + v
    
    return total_files, total_changes, total_counts


def main():
    parser = argparse.ArgumentParser(description="Clean pdftotext artifacts from Qaradawi extracts")
    parser.add_argument("--book", help="Specific book slug to clean (default: all)")
    args = parser.parse_args()
    
    if args.book:
        books = [args.book]
    else:
        books = sorted([d for d in os.listdir(EXTRACT_DIR) 
                        if os.path.isdir(os.path.join(EXTRACT_DIR, d))])
    
    print("=" * 60)
    print("  Qaradawi Library — Extracted Text Cleaner")
    print("=" * 60)
    
    grand_files = 0
    grand_changes = 0
    
    for slug in books:
        files, changes, counts = process_book(slug)
        if files > 0:
            print(f"\n  {slug}: cleaned {files} files, {changes} artifact(s) removed")
            for k, v in counts.items():
                if v > 0:
                    print(f"    Remaining {k}: {v}")
            grand_files += files
            grand_changes += changes
    
    print(f"\n{'='*60}")
    print(f"  TOTAL: {grand_files} files cleaned, {grand_changes} artifacts removed")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
