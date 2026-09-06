#!/usr/bin/env python3
"""
Convert the Family Halaqah Course markdown into a professional dark-themed XeLaTeX PDF.
Uses: Noto Sans (main), Noto Naskh Arabic (Arabic text), tcolorbox for verses/hadith.
"""

import re, os

# ── Read the markdown ──
with open("/root/qaradawi-library/family-halaqah-course.md", "r", encoding="utf-8") as f:
    md = f.read()

# ── Preprocess: replace problematic Unicode ──
replacements = {
    '\uFDFA': '(saw)',
    '\u2192': '\\ensuremath{\\rightarrow}',
    '\u2248': '\\ensuremath{\\approx}',
    '\u2014': '---',
    '\u2018': "'",
    '\u2019': "'",
    '\u201c': '"',
    '\u201d': '"',
    '\u2026': '...',
    '\u2605': '*',
    '\u2606': 'o',
    '\u221e': '$\\infty$',
    '\u00b7': '-',
    '\u2713': 'OK',
    '\u2717': 'X',
}
for old, new in replacements.items():
    md = md.replace(old, new)

# ── Escape LaTeX special characters ──
def esc(text):
    """Escape LaTeX special chars but preserve already-converted commands."""
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    text = text.replace('_', '\\_')
    text = text.replace('$', '\\$')
    return text

# ── Convert markdown bold/italic to LaTeX ──
def fmt(text):
    """Convert **bold** and *italic* markdown to LaTeX, escaping special chars."""
    # Protect double-stars first
    text = re.sub(r'\*\*(.+?)\*\*', lambda m: '\\textbf{' + esc(m.group(1)) + '}', text)
    # Single-star italic (not preceded by *)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', lambda m: '\\textit{' + esc(m.group(1)) + '}', text)
    # Escape remaining special chars (not inside \textbf/\textit)
    # Split on commands, escape non-command parts
    parts = re.split(r'(\\textbf\{[^}]*\}|\\textit\{[^}]*\})', text)
    result = []
    for part in parts:
        if part.startswith('\\textbf{') or part.startswith('\\textit{'):
            result.append(part)
        else:
            result.append(esc(part))
    return ''.join(result)

# ── Wrap Arabic text ──
def wrap_arabic(text):
    """Wrap Arabic segments with \\arabicfont{}."""
    result = []
    current_arabic = ''
    current_other = ''
    in_arabic = False
    for ch in text:
        if '\u0600' <= ch <= '\u06FF' or ch in '\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652':
            if in_arabic:
                current_arabic += ch
            else:
                if current_other:
                    result.append(current_other)
                    current_other = ''
                current_arabic = ch
                in_arabic = True
        else:
            if not in_arabic:
                current_other += ch
            else:
                result.append('\\arabicfont{' + current_arabic + '}')
                current_arabic = ''
                current_other = ch
                in_arabic = False
    if current_arabic:
        result.append('\\arabicfont{' + current_arabic + '}')
    if current_other:
        result.append(current_other)
    return ''.join(result)

# ── Parse the markdown into LaTeX body ──
lines = md.split('\n')
tex = []
in_table = False
in_code = False
i = 0

while i < len(lines):
    line = lines[i]
    s = line.strip()

    # Skip YAML frontmatter
    if s == '---' and i < 5:
        while i < len(lines) and lines[i].strip() != '---':
            i += 1
        i += 1
        continue

    # Code blocks
    if s.startswith('```'):
        if in_code:
            in_code = False
            tex.append('\\end{quotebox}')
        else:
            in_code = True
            tex.append('\\begin{quotebox}')
        i += 1
        continue
    if in_code:
        tex.append(esc(s))
        i += 1
        continue

    # Empty line
    if not s:
        if in_table:
            in_table = False
            tex.append('\\end{longtable}')
        tex.append('')
        i += 1
        continue

    # Horizontal rule
    if s == '---' or s == '***':
        tex.append('\\vspace{6pt}\\noindent{\\color{border}\\rule{\\textwidth}{0.5pt}}\\vspace{6pt}')
        i += 1
        continue

    # Phase header with blockquote theme
    if s.startswith('## PHASE') or s.startswith('> **Phase theme:**'):
        if in_table:
            in_table = False
            tex.append('\\end{longtable}')
        if s.startswith('## PHASE'):
            tex.append('\\newpage')
            tex.append('\\section{' + fmt(s[3:]) + '}')
            i += 1
            # Check for blockquote theme
            if i < len(lines) and lines[i].strip().startswith('> **Phase theme:**'):
                theme = lines[i].strip().replace('> **Phase theme:**', '').strip()
                theme = re.sub(r'\*\*(.+?)\*\*', r'\1', theme)
                tex.append('\\begin{quotebox}\\itshape ' + fmt(theme) + '\\end{quotebox}')
                tex.append('\\vspace{8pt}')
                i += 1
            continue
        else:
            # standalone blockquote theme
            theme = s.replace('> **Phase theme:**', '').strip()
            theme = re.sub(r'\*\*(.+?)\*\*', r'\1', theme)
            tex.append('\\begin{quotebox}\\itshape ' + fmt(theme) + '\\end{quotebox}')
            i += 1
            continue

    # H1
    if s.startswith('# ') and not s.startswith('## '):
        if in_table:
            in_table = False
            tex.append('\\end{longtable}')
        tex.append('\\section*{' + fmt(s[2:]) + '}')
        i += 1
        continue

    # H2
    if s.startswith('## ') and not s.startswith('### '):
        if in_table:
            in_table = False
            tex.append('\\end{longtable}')
        tex.append('\\subsection*{' + fmt(s[3:]) + '}')
        i += 1
        continue

    # H3
    if s.startswith('### ') and not s.startswith('#### '):
        if in_table:
            in_table = False
            tex.append('\\end{longtable}')
        tex.append('\\subsubsection*{' + fmt(s[4:]) + '}')
        i += 1
        continue

    # H4
    if s.startswith('#### '):
        if in_table:
            in_table = False
            tex.append('\\end{longtable}')
        tex.append('\\paragraph*{' + fmt(s[5:]) + '}')
        i += 1
        continue

    # Table rows
    if s.startswith('|'):
        cells_raw = [c.strip() for c in s.split('|')]
        cells = [c for c in cells_raw if c != '']
        # Separator line
        if all(re.match(r'^[-:]+$', c) for c in cells):
            i += 1
            continue
        if not in_table:
            in_table = True
            ncols = len(cells)
            if ncols == 2:
                col_spec = '|p{4.5cm}|p{11cm}|'
            elif ncols == 3:
                col_spec = '|p{2cm}|p{5cm}|p{8.5cm}|'
            elif ncols == 4:
                col_spec = '|p{2.5cm}|p{3.5cm}|p{4.5cm}|p{5cm}|'
            elif ncols == 5:
                col_spec = '|p{2cm}|p{3.5cm}|p{3.5cm}|p{3cm}|p{3.5cm}|'
            else:
                col_spec = '|l' * ncols + '|'
            tex.append('\\begin{longtable}{' + col_spec + '}')
            tex.append('\\hline')
            header = ' & '.join('\\textbf{\\color{accent}' + esc(c.replace('**','')) + '}' for c in cells)
            tex.append(header + ' \\\\')
            tex.append('\\hline')
        else:
            body_cells = [esc(c.replace('**','')) for c in cells]
            tex.append(' & '.join(body_cells) + ' \\\\')
            tex.append('\\hline')
        i += 1
        continue

    # Blockquote
    if s.startswith('> '):
        qt = s[2:]
        if 'Phase theme' in qt:
            i += 1
            continue
        tex.append('\\begin{quotebox}\\itshape ' + fmt(qt) + '\\end{quotebox}')
        i += 1
        continue

    # Bold label lines: **Label:** content
    bold_label = re.match(r'^\*\*(.+?)\*\*:?\s*(.*)$', s)
    if bold_label and not s.startswith('* '):
        label = bold_label.group(1)
        rest = bold_label.group(2)

        if 'Learning objective' in label:
            i += 1
            parts = [fmt(rest)] if rest else []
            while i < len(lines) and lines[i].strip():
                parts.append(fmt(lines[i].strip()))
                i += 1
            tex.append('\\begin{outcomebox} ' + ' '.join(parts) + ' \\end{outcomebox}')
            continue

        if label.startswith("Qur") and not rest:
            i += 1
            verses = []
            while i < len(lines) and lines[i].strip():
                v = lines[i].strip()
                if v.startswith('**Hadith'):
                    break
                verses.append(fmt(v.lstrip('- ').strip()))
                i += 1
            tex.append('\\begin{quranbox} ' + ' \\\\ '.join(verses) + ' \\end{quranbox}')
            continue

        if 'Hadith' in label and not rest:
            i += 1
            hadiths = []
            while i < len(lines) and lines[i].strip():
                h = lines[i].strip()
                if h.startswith('**Qaradawi') or h.startswith('**Family') or h.startswith('**Closing'):
                    break
                hadiths.append(fmt(h.lstrip('- ').strip()))
                i += 1
            tex.append('\\begin{hadithbox} ' + ' \\\\ '.join(hadiths) + ' \\end{hadithbox}')
            continue

        if 'Family discussion' in label:
            i += 1
            qs = []
            while i < len(lines) and lines[i].strip():
                q = lines[i].strip()
                if q.startswith('**Family activity') or q.startswith('**Closing'):
                    break
                qs.append(fmt(q))
                i += 1
            tex.append('\\begin{discussionbox} ' + ' \\\\ '.join(qs) + ' \\end{discussionbox}')
            continue

        if 'Family activity' in label:
            content = fmt(rest)
            i += 1
            extra = []
            while i < len(lines) and lines[i].strip():
                el = lines[i].strip()
                if el.startswith('**Closing') or el.startswith('---') or el.startswith('### ') or el.startswith('## '):
                    break
                extra.append(fmt(el))
                i += 1
            if extra:
                content = content + ' ' + ' '.join(extra)
            tex.append('\\begin{activitybox} ' + content + ' \\end{activitybox}')
            continue

        if 'Closing' in label and 'du' in label.lower():
            content_parts = [fmt(rest)] if rest else []
            i += 1
            while i < len(lines) and lines[i].strip():
                el = lines[i].strip()
                if el.startswith('---') or el.startswith('### ') or el.startswith('## '):
                    break
                content_parts.append(el)
                i += 1
            full = ' '.join(content_parts)
            # Check for Arabic
            has_arabic = any('\u0600' <= ch <= '\u06FF' for ch in full)
            if has_arabic:
                full_wrapped = wrap_arabic(full)
                # Also format bold/italic in the non-Arabic parts
                full_wrapped = fmt(full_wrapped)
                tex.append('\\begin{duabox} ' + full_wrapped + ' \\end{duabox}')
            else:
                tex.append('\\begin{duabox} ' + fmt(full) + ' \\end{duabox}')
            continue

        if 'Qaradawi' in label:
            content = fmt(rest)
            i += 1
            extra = []
            while i < len(lines) and lines[i].strip():
                el = lines[i].strip()
                if el.startswith('**Family') or el.startswith('**Closing') or el.startswith('### ') or el.startswith('## ') or el.startswith('---'):
                    break
                extra.append(fmt(el))
                i += 1
            if extra:
                content = content + ' ' + ' '.join(extra)
            tex.append('\\paragraph*{' + esc(label) + ':} ' + content)
            continue

        if 'Source' in label:
            tex.append('\\textbf{' + esc(label) + ':} ' + fmt(rest))
            i += 1
            continue

        # Generic bold label
        tex.append('\\textbf{' + esc(label) + ':} ' + fmt(rest))
        i += 1
        continue

    # Bullet lists
    if s.startswith('- '):
        item = fmt(s[2:])
        tex.append('\\begin{itemize}')
        tex.append('\\item ' + item)
        i += 1
        while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('  - ')):
            tex.append('\\item ' + fmt(lines[i].strip().lstrip('- ').strip()))
            i += 1
        tex.append('\\end{itemize}')
        tex.append('')
        continue

    # Numbered lists
    num = re.match(r'^(\d+)\.\s+(.+)$', s)
    if num:
        tex.append('\\begin{enumerate}')
        tex.append('\\item ' + fmt(num.group(2)))
        i += 1
        while i < len(lines):
            nn = re.match(r'^(\d+)\.\s+(.+)$', lines[i].strip())
            if nn:
                tex.append('\\item ' + fmt(nn.group(2)))
                i += 1
            else:
                break
        tex.append('\\end{enumerate}')
        tex.append('')
        continue

    # Tree/box chars
    if s.startswith('\u251C') or s.startswith('\u2514') or s.startswith('\u2502'):
        tex.append('\\texttt{' + esc(s) + '}')
        i += 1
        continue

    # Regular paragraph
    para = fmt(s)
    if any('\u0600' <= ch <= '\u06FF' for ch in s):
        para = wrap_arabic(s)
        para = fmt(para)
    tex.append(para)
    i += 1

if in_table:
    tex.append('\\end{longtable}')

body = '\n'.join(tex)

# ── Assemble full document ──
preamble = r"""\documentclass[11pt,a4paper]{article}

\usepackage[margin=2.2cm]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{tikz}
\usepackage{tcolorbox}
\tcbuselibrary{breakable}
\usepackage{parskip}

\definecolor{bgdark}{HTML}{0F1F1A}
\definecolor{bgcard}{HTML}{1A2F26}
\definecolor{accent}{HTML}{C9A857}
\definecolor{accent2}{HTML}{E8D59E}
\definecolor{gold}{HTML}{D4AF37}
\definecolor{textlight}{HTML}{E8E0D5}
\definecolor{textmuted}{HTML}{A0988E}
\definecolor{border}{HTML}{3A5040}
\definecolor{deepgreen}{HTML}{4A8060}
\definecolor{qbg}{HTML}{0D2A1F}
\definecolor{activitybg}{HTML}{2A2015}

\setmainfont[Path=/usr/share/fonts/truetype/noto/, Extension=.ttf,
  BoldFont=NotoSans-Bold,
  ItalicFont=NotoSans-Italic,
  BoldItalicFont=NotoSans-BoldItalic]{NotoSans-Regular}
\newfontfamily\arabicfont[Path=/usr/share/fonts/truetype/noto/, Extension=.ttf,
  Script=Arabic,
  BoldFont=NotoNaskhArabic-Bold]{NotoNaskhArabic-Regular}

\makeatletter
\renewcommand{\normalcolor}{\color{textlight}}
\makeatother

\titleformat{\section}
  {\normalfont\Large\bfseries\color{accent}}
  {\thesection}{1em}{}
  [\color{border}\titlerule]
\titleformat{\subsection}
  {\normalfont\large\bfseries\color{accent2}}
  {\thesubsection}{1em}{}
\titleformat{\subsubsection}
  {\normalfont\normalsize\bfseries\color{textlight}}
  {\thesubsubsection}{1em}{}

\newtcolorbox{quranbox}{
  breakable, colback=qbg, colframe=accent, coltext=textlight,
  coltitle=accent, fonttitle=\bfseries,
  title={\small Qur'an}, boxrule=0.8pt, arc=3pt,
  left=8pt, right=8pt, top=4pt, bottom=4pt
}
\newtcolorbox{hadithbox}{
  breakable, colback=bgcard, colframe=deepgreen, coltext=textlight,
  coltitle=deepgreen, fonttitle=\bfseries,
  title={\small Hadith}, boxrule=0.8pt, arc=3pt,
  left=8pt, right=8pt, top=4pt, bottom=4pt
}
\newtcolorbox{activitybox}{
  breakable, colback=activitybg, colframe=accent2, coltext=textlight,
  coltitle=accent2, fonttitle=\bfseries,
  title={\small Family Activity}, boxrule=0.8pt, arc=3pt,
  left=8pt, right=8pt, top=4pt, bottom=4pt
}
\newtcolorbox{discussionbox}{
  breakable, colback=bgcard, colframe=accent2, coltext=textlight,
  coltitle=accent2, fonttitle=\bfseries,
  title={\small Family Discussion}, boxrule=0.8pt, arc=3pt,
  left=8pt, right=8pt, top=4pt, bottom=4pt
}
\newtcolorbox{outcomebox}{
  breakable, colback=bgcard, colframe=deepgreen, coltext=textlight,
  coltitle=deepgreen, fonttitle=\bfseries,
  title={\small Learning Objective}, boxrule=0.8pt, arc=3pt,
  left=8pt, right=8pt, top=4pt, bottom=4pt
}
\newtcolorbox{duabox}{
  breakable, colback=qbg, colframe=gold, coltext=textlight,
  coltitle=gold, fonttitle=\bfseries,
  title={\small Closing Du'a}, boxrule=0.8pt, arc=3pt,
  left=8pt, right=8pt, top=4pt, bottom=4pt
}
\newtcolorbox{quotebox}{
  breakable, colback=bgcard, colframe=border, coltext=textlight,
  boxrule=0.5pt, arc=3pt,
  left=8pt, right=8pt, top=4pt, bottom=4pt
}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\color{textmuted}\small Family Halaqah Course}
\fancyhead[R]{\color{textmuted}\small From the Works of Yusuf al-Qaradawi}
\fancyfoot[C]{\color{textmuted}\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}
\renewcommand{\headrule}{\color{border}\hrule width\headwidth height\headrulewidth}

\setlist[itemize]{leftmargin=1.5em, itemsep=2pt, topsep=2pt}
\setlist[enumerate]{leftmargin=1.5em, itemsep=2pt, topsep=2pt}
"""

cover = r"""
\begin{titlepage}
\begin{tikzpicture}[remember picture, overlay]
  \fill[bgdark] (current page.south west) rectangle (current page.north east);
\end{tikzpicture}
\thispagestyle{empty}

\vspace*{3cm}
\begin{center}
{\fontsize{28}{34}\selectfont\bfseries\color{gold} Family Halaqah Course\par}
\vspace{12pt}
{\fontsize{14}{18}\selectfont\color{accent2}\itshape A Structured 30-Week Curriculum\par}
\vspace{6pt}
{\fontsize{14}{18}\selectfont\color{accent2}\itshape from the Works of Shaykh Yusuf al-Qaradawi\par}
\vspace{24pt}
{\color{border}\rule{8cm}{0.8pt}}
\vspace{24pt}

{\fontsize{12}{16}\selectfont\color{textlight} 5 Phases \quad\textbullet\quad 30 Modules \quad\textbullet\quad Weekly Family Sessions\par}
\vspace{6pt}
{\fontsize{11}{14}\selectfont\color{textmuted} Sources: Yusuf al-Qaradawi's Books, Qur'an, and Hadith\par}
\vspace{36pt}

{\fontsize{11}{14}\selectfont\color{textlight}
\begin{tabular}{rl}
\color{accent}\textbf{Phase 1:} & \color{textlight}Roots --- Faith as the Foundation (Weeks 1--6) \\
\color{accent}\textbf{Phase 2:} & \color{textlight}Trunk --- Character and Inner Purification (Weeks 7--12) \\
\color{accent}\textbf{Phase 3:} & \color{textlight}Branches --- The Family Unit (Weeks 13--18) \\
\color{accent}\textbf{Phase 4:} & \color{textlight}Leaves --- Living Islam in the World (Weeks 19--25) \\
\color{accent}\textbf{Phase 5:} & \color{textlight}Fruit --- Trust, Hope, and Eternal Vision (Weeks 26--30) \\
\end{tabular}\par}

\vfill
{\color{border}\rule{12cm}{0.4pt}}
\vspace{8pt}
{\fontsize{10}{12}\selectfont\color{textmuted} Qaradawi Library LLM Wiki \quad\textbullet\quad June 2026\par}
\end{center}
\end{titlepage}
"""

full_doc = preamble + "\n\n\\begin{document}\n\n\\pagecolor{bgdark}\n\\color{textlight}\n\\normalcolor\n\n"
full_doc += cover
full_doc += "\n\n"
full_doc += body
full_doc += "\n\n\\end{document}\n"

tex_path = "/root/qaradawi-library/family-halaqah-course.tex"
with open(tex_path, 'w', encoding='utf-8') as f:
    f.write(full_doc)

print(f"TeX file written: {tex_path}")
print(f"Size: {len(full_doc)} chars, {full_doc.count(chr(10))} lines")