#!/usr/bin/env python3
"""Re-split ethics-in-islam full.txt into subsections based on TOC structure."""
import yaml

with open('/root/qaradawi-library/raw/extracted/ethics-in-islam/full.txt', 'r', errors='replace') as f:
    lines = f.readlines()

# Subsection boundaries (1-indexed line numbers from content analysis)
# Include the Introduction and Chapter headers as separate sections
sections = [
    # Introduction
    {"num": "00", "title": "Introduction", "start": 107},
    # Chapter 1
    {"num": "01-01", "title": "Definitions And Concepts Of Islamic Ethics", "start": 400},
    {"num": "01-02", "title": "The Status Of Ethics In Islam", "start": 1312},
    {"num": "01-03", "title": "Higher Objectives And Goals Of Islamic Ethics", "start": 1857},
    {"num": "01-04", "title": "Methods Of Achieving The Objectives Of Ethics", "start": 3306},
    {"num": "01-05", "title": "Effects Of Faith-Based Education On Controlling Instincts And Habits", "start": 4234},
    {"num": "01-06", "title": "The Need For The Islamic Community And Islamic Regime", "start": 5042},
    # Chapter 2
    {"num": "02-01", "title": "History Of Moral Philosophy In The West", "start": 5282},
    {"num": "02-02", "title": "Modern Moral Philosophies In The West", "start": 5494},
    {"num": "02-03", "title": "Pre-Islamic Arab Moral Philosophy", "start": 5974},
    {"num": "02-04", "title": "Arab Moral Philosophy After Islam", "start": 6278},
    {"num": "02-05", "title": "Religious Ethics And The Theory Of Divine Revelation", "start": 8149},
    {"num": "02-06", "title": "Standards Of Ethical Judgments In Islam", "start": 9442},
    {"num": "02-07", "title": "Review Of Khalid Mohammed Khalid's Book", "start": 9801},
    # Chapter 3
    {"num": "03-01", "title": "Moral Obligation", "start": 10489},
    {"num": "03-02", "title": "Moral Responsibility", "start": 11012},
    {"num": "03-03", "title": "Punishment", "start": 11652},
    {"num": "03-04", "title": "Intentions And Motives", "start": 12125},
    {"num": "03-05", "title": "Work And Exerted Effort", "start": 12484},
    {"num": "03-06", "title": "Complementary Principles To The Five Foundations", "start": 12955},
    {"num": "03-07", "title": "The Three Higher Transcendental Values", "start": 13256},
    # Chapter 4
    {"num": "04-01", "title": "Divine Ethics: Human Morality Toward The Divine", "start": 13745},
    {"num": "04-02", "title": "Individual Ethics", "start": 14529},
    {"num": "04-03", "title": "Collective Human Ethics", "start": 16072},
]

# Map sub-sections to chapter-level files
# Keep 4 chapter files but with proper subsection markers
# Also save individual subsection files for wiki generation

chapter_map = {
    "00": "ch-01", "01": "ch-01",  # Intro + Ch1
    "02": "ch-02",  # Ch2
    "03": "ch-03",  # Ch3
    "04": "ch-04",  # Ch4
}

# Create individual subsection files
for i, sec in enumerate(sections):
    start = sec["start"] - 1  # 0-indexed
    if i + 1 < len(sections):
        end = sections[i + 1]["start"] - 1
    else:
        end = len(lines)
    
    content = ''.join(lines[start:end])
    filename = f'/root/qaradawi-library/raw/extracted/ethics-in-islam/section-{sec["num"]}.txt'
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Created section-{sec['num']}.txt: L{sec['start']}-{end+1} ({len(content)} chars) - {sec['title'][:60]}")

# Keep the 4 chapter files but regenerate them from subsections
chapters = {
    "ch-01.txt": (0, 5),   # sections 0-5 (intro + 1.1-1.6)
    "ch-02.txt": (6, 12),   # sections 2.1-2.7
    "ch-03.txt": (13, 19),  # sections 3.1-3.7
    "ch-04.txt": (20, 22),  # sections 4.1-4.3
}

for ch_file, (start_idx, end_idx) in chapters.items():
    start = sections[start_idx]["start"] - 1
    end = len(lines) if end_idx == len(sections) - 1 else sections[end_idx + 1]["start"] - 1
    content = ''.join(lines[start:end])
    filepath = f'/root/qaradawi-library/raw/extracted/ethics-in-islam/{ch_file}'
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Regenerated {ch_file}: L{sections[start_idx]['start']}-{end+1} ({len(content)} chars)")

# Update metadata
meta = {
    'author': 'Yusuf al-Qaradawi',
    'pages': '434',
    'pdf_sha256': '0ae94261a3d10ec7d1df2e78c192caaf1838397f0f4fef39694d3c7c727ba6fe',
    'title': 'Ethics in Islam',
    'chapters': 4,
    'subsections': 23
}
with open('/root/qaradawi-library/raw/extracted/ethics-in-islam/metadata.yaml', 'w') as f:
    yaml.dump(meta, f, default_flow_style=False)
print("\nUpdated metadata.yaml")