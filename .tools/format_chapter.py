#!/usr/bin/env python3
"""
format_chapter.py — Clean and format Qaradawi chapter text into publication-quality HTML.

Key insight for Qaradawi PDFs (Faith and Life, etc.):
  - Paragraphs are separated by blank lines
  - First line of a paragraph has 2-space indentation
  - Continuation lines have 0 indentation
  - The first line of a paragraph block is often the section heading
  - Verse text flows followed by verse reference
"""

import re

# ═══════════════════════════════════════════════════════════════
#  CLEANING
# ═══════════════════════════════════════════════════════════════

def clean_text(text):
    """Remove pdftotext artifacts from extracted text."""
    text = re.sub(r'\f+', '\n\n', text)
    text = re.sub(r'^[ \t]*e[ \t]+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\bJ(man|slam|slamic|slamist|manity)\b', lambda m: 'I' + m.group(1).lower(), text, flags=re.IGNORECASE)
    text = re.sub(r'^\s*\d+\s+Faith and Life\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^(Chapter|CHAPTER)\s+(One|Two|Three|Four|[0-9]+)\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^Chapter\s+(One|Two|Three|Four)\s+\w+$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'\n\s*Chapter\s+(One|Two|Three|Four)\s*\n', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'\n\s*Faith and Life\s*\n', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'\b1\s+(created|know|am|will|have)\b', r'I \1', text, flags=re.IGNORECASE)
    text = re.sub(r'\bifyou\b', 'if you', text, flags=re.IGNORECASE)
    text = re.sub(r'\bsciel\s+ntist\b', 'scientist', text, flags=re.IGNORECASE)
    text = re.sub(r'[ \t]{3,}', '  ', text)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()


# ═══════════════════════════════════════════════════════════════
#  CLASSIFICATION
# ═══════════════════════════════════════════════════════════════

VERSE_REF_RE = re.compile(r'\([A-Za-z\x27\-]+:\s*\d+[^\)]*\)')
HADITH_RE = re.compile(r'(Prophet|Messenger|hadith|narrated|al-Bukhari|Muslim|divine hadith)')

def is_verse(text):
    """Verse blocks: start with quote AND contain a verse reference, or contain a verse ref + long text."""
    s = text.strip()
    if not s:
        return False
    has_ref = bool(VERSE_REF_RE.search(s))
    starts_quote = s.startswith('"')
    return has_ref and (starts_quote or len(s) > 60)

def is_hadith(text):
    """Hadith blocks: contain hadith keywords, typically long, NOT starting with quote."""
    s = text.strip()
    if not s or s.startswith('"') or len(s) < 40:
        return False
    return bool(HADITH_RE.search(s))

def is_heading(text):
    """
    Section headings: short, starts with capital, contains 'and'/'in'/'of',
    no internal periods, no verse references.
    """
    s = text.strip()
    if not s:
        return False
    if len(s) < 3 or len(s) > 55:
        return False
    if not s[0].isupper():
        return False
    if ' ' not in s:
        return False
    if '.' in s and s.index('.') < len(s) - 5:
        return False
    if VERSE_REF_RE.search(s):
        return False
    if '"' in s:
        return False
    return True

def is_toc_line(text):
    """Table of contents entries look like short section headers."""
    return is_heading(text)

# ═══════════════════════════════════════════════════════════════
#  FORMATTING
# ═══════════════════════════════════════════════════════════════

def format_block(block_text, in_toc=False):
    """Classify and format a single block of text."""
    s = block_text.strip()
    if not s:
        return None
    
    if is_verse(s):
        return f'<div class="section-verse"><p>{escape_html(s)}</p></div>'
    
    if is_hadith(s):
        return f'<div class="hadith-block"><p>{escape_html(s)}</p></div>'
    
    if is_heading(s):
        if in_toc:
            return f'<li>{s}</li>'
        return f'<h3 class="section-heading">{s}</h3>'
    
    return f'<p>{escape_html(s)}</p>'


def escape_html(text):
    """Lightweight HTML escape."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


# ═══════════════════════════════════════════════════════════════
#  MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════

def format_chapter_body(text, max_paragraphs=60):
    """
    Full pipeline: clean text → extract TOC → process blocks → format HTML.
    Returns dict: {html: str, outline: list}
    """
    text = clean_text(text)
    
    # Split into raw blocks by double newline
    raw_blocks = [b.strip() for b in text.split('\n\n') if b.strip()]
    
    # --- TOC detection ---
    # Find consecutive heading blocks at the top of the chapter
    outline = []
    toc_end = 0
    for i, block in enumerate(raw_blocks[:15]):
        # First line of the block
        first_line = block.split('\n')[0].strip()
        if is_toc_line(first_line):
            outline.append(first_line)
            toc_end = i + 1
        elif i < 2:  # First 2 blocks are always headings or chapter title
            if is_toc_line(block) or len(block) < 40:
                outline.append(block)
                toc_end = i + 1
        elif len(block) > 60:
            # Long text marks end of TOC
            break
    
    # Remove outline blocks from content (they are just TOC, not body)
    content_blocks = raw_blocks[toc_end:]
    
    # --- Merge verse references with preceding verse text ---
    # If a block ends with a verse ref and the next block starts with a quote or is short
    merged = []
    skip_next = False
    for i, block in enumerate(content_blocks):
        if skip_next:
            skip_next = False
            continue
        
        # If current block has verse ref at end, and next block starts with quote
        if i + 1 < len(content_blocks) and is_verse(content_blocks[i+1]):
            # Check if CURRENT block is the verse text (has opening quote)
            if block.startswith('"') and VERSE_REF_RE.search(block):
                pass  # Already a complete verse
            next_block = content_blocks[i+1]
            if block.startswith('"') and is_verse(block):
                # Merge adjacent verse parts
                merged.append(block + '  ' + next_block)
                skip_next = True
                continue
        
        # Join multi-line blocks: replace single newlines within a block with spaces
        merged_block = ' '.join(block.split('\n'))
        merged.append(merged_block)
    
    # --- Format to HTML ---
    html_parts = []
    paragraph_count = 0
    for block in merged:
        if paragraph_count >= max_paragraphs:
            break
        formatted = format_block(block)
        if formatted is None:
            continue
        html_parts.append(formatted)
        if formatted.startswith('<p>'):
            paragraph_count += 1
    
    return {'html': '\n'.join(html_parts), 'outline': outline}


if __name__ == '__main__':
    path = '/root/qaradawi-library/raw/extracted/faith-and-life/ch-01.txt'
    with open(path, 'r') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        body = parts[2].strip() if len(parts) >= 3 else content
    else:
        body = content
    
    result = format_chapter_body(body, max_paragraphs=40)
    print("=== OUTLINE ===")
    for item in result['outline']:
        print(f"  • {item}")
    print("\n=== HTML PREVIEW (first 1500 chars) ===")
    print(result['html'][:1500])
    print("\n...")
    print("\n=== FULL HTML LENGTH ===")
    print(f"{len(result['html'])} chars")
