#!/usr/bin/env python3
"""Re-split diversion-arts full.txt into logical sections based on content analysis."""
import re

with open('/root/qaradawi-library/raw/extracted/diversion-arts/full.txt', 'r', errors='replace') as f:
    text = f.read()
lines = text.split('\n')

sections_div = [
    {"name": "intro-reality", "title": "Islam and Sense of Reality", "start_line": 29},
    {"name": "beauty-quran", "title": "Beauty in the Quran and Universe", "start_line": 188},
    {"name": "expression-poetry", "title": "Expression of Beauty: Poetry and Literature", "start_line": 310},
    {"name": "judgement-singing-music", "title": "The Judgement of Islam on Singing and Music", "start_line": 435},
    {"name": "painting-pictures", "title": "Painting, Picture-Making and Decoration", "start_line": 1956},
    {"name": "photography", "title": "Photography", "start_line": 2355},
    {"name": "humor-games-conclusion", "title": "Comedy, Humor, Games and Conclusion", "start_line": 2608},
]

# Verify boundaries first
for sec in sections_div:
    idx = sec["start_line"] - 1
    context = lines[idx:idx+3]
    print(f'L{sec["start_line"]}: [{sec["title"]}]')
    for c in context:
        print(f'  {c.strip()[:100]}')
    print()

# Create chapter files
for i, sec in enumerate(sections_div):
    start = sec["start_line"] - 1  # 0-indexed
    if i + 1 < len(sections_div):
        end = sections_div[i + 1]["start_line"] - 1
    else:
        end = len(lines)
    
    content = '\n'.join(lines[start:end])
    filename = f'/root/qaradawi-library/raw/extracted/diversion-arts/ch-{i+1:02d}.txt'
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Created {filename}: lines {start+1}-{end} ({len(content)} chars)")

# Update metadata
import yaml
meta = {
    'author': 'Qaradawi',
    'pages': '116',
    'pdf_sha256': 'b7f6559311d10ae0870adbbab28b96bf57120f409d842344be07e4865665819d',
    'title': 'Diversion And Arts In Islam',
    'chapters': 7
}
with open('/root/qaradawi-library/raw/extracted/diversion-arts/metadata.yaml', 'w') as f:
    yaml.dump(meta, f, default_flow_style=False)
print(f"\nUpdated metadata.yaml with chapters: 7")