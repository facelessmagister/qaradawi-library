#!/usr/bin/env python3
"""
split_halal_haram.py — Split the OCR'd Halal & Haram text into chapters
"""
import os

WIKI_ROOT = "/root/qaradawi-library"
EXTRACT_DIR = os.path.join(WIKI_ROOT, "raw", "extracted", "halal-haram")

with open(os.path.join(EXTRACT_DIR, "full.txt"), 'r') as f:
    text = f.read()

lines = text.split('\n')
print(f"Total lines: {len(lines)}")

# Chapter boundaries (0-based line indices)
# Introduction starts at line 520 (1-based: 521)
# Chapter 1 content starts around line 932 where "The Islamic Principles Pertaining" heading is
# Chapter 2 at line 2118 (1-based: 2119)
# Chapter 3 at line 6958 (1-based: 6959)  
# Chapter 4 at line 10964 (1-based: 10965)

# Find exact ch1 start - search backwards from "The Islamic Principles"
ch1_start = None
for i, line in enumerate(lines):
    if i < 900 or i > 960:
        continue
    if 'The Islamic Principles Pertaining' in line:
        # Go back to find the section heading
        for j in range(i-1, max(i-10, 0), -1):
            if lines[j].strip() == '':
                ch1_start = j + 1
                break
        if ch1_start is None:
            ch1_start = i - 2
        break

print(f"Ch1 start found at line {ch1_start}")
print(f"Context: {lines[ch1_start-2][:60]} / {lines[ch1_start-1][:60]} / {lines[ch1_start][:60]}")

chapters = {
    'ch-00': {
        'title': 'Introduction',
        'start': 520,
        'end': ch1_start - 1
    },
    'ch-01': {
        'title': 'The Islamic Principles Pertaining to the Lawful and the Prohibited',
        'start': ch1_start,
        'end': 2118
    },
    'ch-02': {
        'title': 'The Lawful and the Prohibited in Eating, Drinking, and Economic Life',
        'start': 2118,
        'end': 6958
    },
    'ch-03': {
        'title': 'The Lawful and the Prohibited in Marriage and Family Life',
        'start': 6958,
        'end': 10964
    },
    'ch-04': {
        'title': 'The Lawful and the Prohibited in Dress, Adornment, and Social Relations',
        'start': 10964,
        'end': len(lines)
    }
}

for slug, info in chapters.items():
    chapter_text = '\n'.join(lines[info['start']:info['end']])
    char_count = len(chapter_text)
    line_count = info['end'] - info['start']
    print(f"{slug}: {info['title']} ({line_count} lines, {char_count:,} chars)")
    
    filepath = os.path.join(EXTRACT_DIR, f"{slug}.txt")
    with open(filepath, 'w') as f:
        f.write(chapter_text)
    print(f"  Written: {filepath}")