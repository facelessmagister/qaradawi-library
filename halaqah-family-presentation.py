#!/usr/bin/env python3
"""
Halaqah Presentation: Wisdom for the Family from Yusuf al-Qaradawi
Design: Deep green primary, gold accent, parchment surface (tarbiyyah palette)
Source: Qaradawi Library LLM Wiki (/root/qaradawi-library/)
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Design Tokens (Tarbiyyah Palette) ──
C_PRIMARY     = RGBColor(0x1B, 0x4D, 0x3E)
C_PRIMARY_DK  = RGBColor(0x10, 0x33, 0x2B)
C_SECONDARY   = RGBColor(0x6B, 0x90, 0x80)
C_ACCENT      = RGBColor(0xC9, 0xA8, 0x57)
C_SURFACE     = RGBColor(0xFA, 0xF6, 0xF0)
C_SURFACE_R   = RGBColor(0xED, 0xE5, 0xD8)
C_TEXT        = RGBColor(0x1C, 0x19, 0x17)
C_TEXT_MUTED  = RGBColor(0x57, 0x53, 0x4E)
C_WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
C_CARD_BG     = RGBColor(0xF5, 0xEF, 0xE3)

W = Inches(13.333)
H = Inches(7.5)

FOOTER_TEXT = 'Qaradawi Library LLM Wiki | Halaqah Presentation'

# ── Helpers ──

def add_top_rule(slide):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), W, Inches(0.10))
    shape.fill.solid()
    shape.fill.fore_color.rgb = C_PRIMARY
    shape.line.fill.background()

def add_footer(slide, text=FOOTER_TEXT):
    tx = slide.shapes.add_textbox(Inches(0.5), H - Inches(0.45), W - Inches(1.0), Inches(0.30))
    p = tx.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(9)
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.RIGHT

def add_slide_title(slide, title, subtitle=None):
    add_top_rule(slide)
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(0.25), W - Inches(1.2), Inches(0.55))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.font.name = 'Georgia'
    ul = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.82), Inches(1.6), Inches(0.04))
    ul.fill.solid(); ul.fill.fore_color.rgb = C_ACCENT; ul.line.fill.background()
    if subtitle:
        stx = slide.shapes.add_textbox(Inches(0.6), Inches(0.92), W - Inches(1.2), Inches(0.28))
        sp = stx.text_frame.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(14)
        sp.font.color.rgb = C_TEXT_MUTED
        sp.font.italic = True
    return 1.15

def add_arabic_box(slide, arabic_text, y_inches=0.55, box_h=Inches(0.85)):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(y_inches), W - Inches(1.2), box_h)
    bg.fill.solid(); bg.fill.fore_color.rgb = C_SURFACE_R; bg.line.fill.background()
    lb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(y_inches), Inches(0.05), box_h)
    lb.fill.solid(); lb.fill.fore_color.rgb = C_ACCENT; lb.line.fill.background()
    tx = slide.shapes.add_textbox(Inches(0.8), Inches(y_inches), W - Inches(1.6), box_h)
    tf = tx.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = arabic_text
    p.font.size = Pt(22)
    p.font.color.rgb = C_PRIMARY
    p.alignment = PP_ALIGN.CENTER
    return y_inches + box_h.inches + 0.08

def add_translation(slide, text, y_inches, italic=True):
    tx = slide.shapes.add_textbox(Inches(0.8), Inches(y_inches), W - Inches(1.6), Inches(0.45))
    tf = tx.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(13)
    p.font.italic = italic
    p.font.color.rgb = C_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER
    return y_inches + 0.48

def add_card(slide, x, y, w, h, title, body_lines, accent_color=C_ACCENT, title_color=None):
    if title_color is None:
        title_color = C_PRIMARY
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.fill.solid(); card.fill.fore_color.rgb = C_CARD_BG; card.line.fill.background()
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.06), Inches(h))
    bar.fill.solid(); bar.fill.fore_color.rgb = accent_color; bar.line.fill.background()
    tx = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.1), Inches(w - 0.3), Inches(0.35))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = title_color; p.font.name = 'Georgia'
    body_tx = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.5), Inches(w - 0.3), Inches(h - 0.6))
    tf = body_tx.text_frame; tf.word_wrap = True
    for i, line in enumerate(body_lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(11); p.font.color.rgb = C_TEXT; p.space_after = Pt(3)

def add_stat_callout(slide, big_text, label, x, y, w=2.8, h=1.6):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    bg.fill.solid(); bg.fill.fore_color.rgb = C_PRIMARY; bg.line.fill.background()
    tx1 = slide.shapes.add_textbox(Inches(x), Inches(y + 0.15), Inches(w), Inches(0.85))
    p1 = tx1.text_frame.paragraphs[0]
    p1.text = big_text
    p1.font.size = Pt(40); p1.font.bold = True; p1.font.color.rgb = C_ACCENT; p1.alignment = PP_ALIGN.CENTER
    tx2 = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 1.0), Inches(w - 0.3), Inches(0.5))
    tf2 = tx2.text_frame; tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = label
    p2.font.size = Pt(12); p2.font.color.rgb = C_SURFACE; p2.alignment = PP_ALIGN.CENTER

def add_quote_card(slide, quote, source, y_inches=1.3, h=Inches(1.2)):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(y_inches), W - Inches(2.0), h)
    bg.fill.solid(); bg.fill.fore_color.rgb = C_SURFACE_R; bg.line.fill.background()
    lb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(y_inches), Inches(0.06), h)
    lb.fill.solid(); lb.fill.fore_color.rgb = C_ACCENT; lb.line.fill.background()
    tx = slide.shapes.add_textbox(Inches(1.3), Inches(y_inches + 0.12), W - Inches(2.6), h - Inches(0.4))
    tf = tx.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = '\u201c' + quote + '\u201d'
    p.font.size = Pt(16); p.font.italic = True; p.font.color.rgb = C_PRIMARY; p.font.name = 'Georgia'
    src_tx = slide.shapes.add_textbox(Inches(1.3), Inches(y_inches + h.inches - 0.35), W - Inches(2.6), Inches(0.30))
    sp = src_tx.text_frame.paragraphs[0]
    sp.text = '\u2014 ' + source
    sp.font.size = Pt(11); sp.font.color.rgb = C_TEXT_MUTED; sp.alignment = PP_ALIGN.RIGHT

def add_section_icon_circle(slide, number, x, y, d=0.5):
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    circle.fill.solid(); circle.fill.fore_color.rgb = C_ACCENT; circle.line.fill.background()
    tx = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(d), Inches(d))
    tf = tx.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = str(number)
    p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_PRIMARY; p.alignment = PP_ALIGN.CENTER

# ═══════════════════════════════════════════
# SLIDE BUILDERS
# ═══════════════════════════════════════════

def make_title_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_PRIMARY_DK
    bb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), H - Inches(0.10), W, Inches(0.10))
    bb.fill.solid(); bb.fill.fore_color.rgb = C_ACCENT; bb.line.fill.background()
    tb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), W, Inches(0.06))
    tb.fill.solid(); tb.fill.fore_color.rgb = C_ACCENT; tb.line.fill.background()

    tx_ar = slide.shapes.add_textbox(Inches(0.5), Inches(0.8), W - Inches(1.0), Inches(0.6))
    p_ar = tx_ar.text_frame.paragraphs[0]
    p_ar.text = '\u062d\u0650\u0643\u0652\u0645\u064e\u0629\u064c \u0644\u0650\u0644\u0652\u0639\u064e\u0627\u0626\u0650\u0644\u064e\u0629'
    p_ar.font.size = Pt(32); p_ar.font.color.rgb = C_ACCENT; p_ar.alignment = PP_ALIGN.CENTER

    tx1 = slide.shapes.add_textbox(Inches(0.5), Inches(1.6), W - Inches(1.0), Inches(1.0))
    p = tx1.text_frame.paragraphs[0]
    p.text = 'Wisdom for the Family'
    p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = C_WHITE; p.font.name = 'Georgia'
    p.alignment = PP_ALIGN.CENTER

    tx2 = slide.shapes.add_textbox(Inches(0.5), Inches(2.7), W - Inches(1.0), Inches(0.5))
    p2 = tx2.text_frame.paragraphs[0]
    p2.text = 'A Halaqah Presentation from the Works of Shaykh Yusuf al-Qaradawi'
    p2.font.size = Pt(20); p2.font.italic = True; p2.font.color.rgb = C_SURFACE; p2.alignment = PP_ALIGN.CENTER

    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.5), Inches(3.4), Inches(2.3), Inches(0.03))
    div.fill.solid(); div.fill.fore_color.rgb = C_ACCENT; div.line.fill.background()

    tx3 = slide.shapes.add_textbox(Inches(0.5), Inches(3.6), W - Inches(1.0), Inches(0.35))
    p3 = tx3.text_frame.paragraphs[0]
    p3.text = '5 Themes | 9 Books | 48 Concepts | ~9.4 Million Characters of Source Text'
    p3.font.size = Pt(14); p3.font.color.rgb = C_SECONDARY; p3.alignment = PP_ALIGN.CENTER

    tx4 = slide.shapes.add_textbox(Inches(0.5), Inches(5.5), W - Inches(1.0), Inches(0.35))
    p4 = tx4.text_frame.paragraphs[0]
    p4.text = 'Qaradawi Library LLM Wiki  |  9 June 2026'
    p4.font.size = Pt(12); p4.font.color.rgb = C_SECONDARY; p4.alignment = PP_ALIGN.CENTER


def make_about_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    add_slide_title(slide, 'About This Presentation', 'From the Qaradawi Library LLM Wiki')

    add_card(slide, 0.6, 1.3, 5.8, 2.8,
        'Shaykh Yusuf al-Qaradawi (1926\u20132022)',
        [
            'Egyptian Islamic scholar, wasatiyyah jurist,',
            'and one of the most prolific authors in',
            'contemporary Islamic thought \u2014 170+ works.',
            '',
            'Founder of the Faculty of Shari\u2019ah at the',
            'University of Qatar; chairman of the',
            'International Union of Muslim Scholars.',
            '',
            'This wiki focuses on his fiqh, ethics,',
            'and spiritual writings.',
        ])

    add_card(slide, 6.9, 1.3, 5.8, 2.8,
        'The LLM Wiki',
        [
            '9 books ingested and fully searchable.',
            '48 concept pages with cross-references.',
            '4 cross-book comparison syntheses.',
            '~9.4 million characters of source text.',
            '',
            'Every claim traces back to the exact',
            'chapter and page in the original work.',
            '',
            'Built using the Karpathy LLM Wiki pattern',
            'for AI-searchable Islamic knowledge.',
        ])

    add_card(slide, 0.6, 4.3, 12.1, 2.5,
        'How This Halaqah Was Prepared',
        [
            'Five themes were selected from the wiki that are suitable for a family audience: Akhlaq (Good Character),',
            'Wasatiyyah (Moderation), Sabr (Patience), Marriage & Family Life, and Tazkiyah & Ikhlas (Purification & Sincerity).',
            '',
            'Each theme is drawn from multiple books \u2014 Ethics in Islam, Faith and Life, The Lawful and the Prohibited,',
            'Approaching the Sunnah, and Fiqh al-Zakah \u2014 synthesising Qaradawi\u2019s positions across his corpus.',
            '',
            'All Qur\u2019anic verses and hadiths are cited. Arabic text is included where central to the topic.',
        ])
    add_footer(slide)


def make_agenda_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    add_slide_title(slide, 'Today\u2019s Five Themes', 'A journey through Qaradawi\u2019s wisdom for family life')

    themes = [
        ('1', 'Akhlaq \u2014 Good Character', 'The Prophet\u2019s mission: to perfect good morals'),
        ('2', 'Wasatiyyah \u2014 The Middle Way', 'Balance between extremism and laxity'),
        ('3', 'Sabr \u2014 Patience & Perseverance', 'Three dimensions of endurance'),
        ('4', 'Marriage & Family Life', 'Affection, mercy, and simplicity'),
        ('5', 'Tazkiyah & Ikhlas \u2014 Purification & Sincerity', 'Cleansing the soul, purifying intention'),
    ]

    for i, (num, title, desc) in enumerate(themes):
        yi = 1.4 + i * 1.05
        add_section_icon_circle(slide, num, 0.8, yi, d=0.55)
        tx = slide.shapes.add_textbox(Inches(1.6), Inches(yi), Inches(6.0), Inches(0.40))
        p = tx.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = C_PRIMARY; p.font.name = 'Georgia'
        tx2 = slide.shapes.add_textbox(Inches(1.6), Inches(yi + 0.42), Inches(8.0), Inches(0.30))
        p2 = tx2.text_frame.paragraphs[0]
        p2.text = desc
        p2.font.size = Pt(13); p2.font.italic = True; p2.font.color.rgb = C_TEXT_MUTED

    add_footer(slide)


def make_theme1_akhlaq(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    y = add_slide_title(slide, 'Theme 1: Akhlaq \u2014 Good Character', '\u0623\u064e\u062e\u0652\u0644\u064e\u0627\u0642 | The heaviest deed on the scales')

    y = add_arabic_box(slide, '\u0648\u064e\u0625\u0650\u0646\u0651\u064e\u0643\u064e \u0644\u064e\u0639\u064e\u0644\u064e\u0649\u0670 \u062e\u064f\u0644\u064f\u0642\u064d \u0639\u064e\u0638\u0650\u064a\u0645\u064d', y + 0.05, Inches(0.7))
    y = add_translation(slide, '\u201cAnd indeed, you are of a great moral character.\u201d  \u2014 Qur\u2019an 68:4', y)

    add_quote_card(slide,
        'I have been sent to perfect good morals and conduct.',
        'Prophet Muhammad (PBUH) (Ahmed 8952, al-Bukhari, al-Hakim)',
        y + 0.1, Inches(0.9))

    add_card(slide, 0.6, 3.8, 5.8, 3.1,
        'What is Akhlaq?',
        [
            'Akhlaq = moral character \u2014 the inner self',
            'with its stable traits, good or evil.',
            '',
            'Two types:',
            '  \u2022 Innate (gharizi): endowed by Allah',
            '  \u2022 Acquired (muktasab): through practice,',
            '    companionship, and self-discipline',
            '',
            'Key insight from al-Ghazali:',
            '  Character is what you ARE,',
            '  not what you APPEAR to do.',
        ])

    add_card(slide, 6.9, 3.8, 5.8, 3.1,
        'Qaradawi\u2019s Key Positions',
        [
            '1. Akhlaq is the core Islamic concern.',
            '   The Prophet\u2019s mission statement.',
            '',
            '2. Good character outweighs ritual.',
            '   \u2018A person reaches the status of those',
            '   who fast and pray by good character.\u2019',
            '',
            '3. Character is MUTABLE, not fixed.',
            '   \u2018Dogs and horses can be trained to be',
            '   gentle, and people too.\u2019 \u2014 al-Ghazali',
            '',
            '4. Companionship shapes character.',
            '   Applies to friends, media, environment.',
        ])
    add_footer(slide)


def make_theme2_wasatiyyah(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    y = add_slide_title(slide, 'Theme 2: Wasatiyyah \u2014 The Middle Way', '\u0648\u064e\u0633\u064e\u0637\u0650\u064a\u0651\u0629 | Balance between extremes')

    y = add_arabic_box(slide, '\u0648\u064e\u0643\u064e\u0630\u064e\u0670\u0644\u0650\u0643\u064e \u062c\u064e\u0639\u064e\u0644\u0652\u0646\u064e\u0627\u0643\u064f\u0645\u0652 \u0623\u064f\u0645\u0651\u064e\u0629\u064b \u0648\u064e\u0633\u064e\u0637\u064b\u0627', y + 0.05, Inches(0.7))
    y = add_translation(slide, '\u201cAnd thus We have made you a middle nation.\u201d  \u2014 Qur\u2019an 2:143', y)

    add_quote_card(slide,
        'Your body owns a right over you, your eyes own a right over you, your family own a right over you.',
        'Prophet Muhammad (PBUH), correcting three men who vowed extreme asceticism',
        y + 0.1, Inches(0.95))

    add_card(slide, 0.6, 3.6, 3.8, 3.3,
        'In Worship',
        [
            'Not excessive asceticism,',
            'not mere ritualism.',
            '',
            'The Prophet rejected:',
            '  \u2022 Fasting every day',
            '  \u2022 Praying all night',
            '  \u2022 Abstaining from marriage',
            '',
            'Balance: worship + family',
            '+ rest + social duties.',
        ])

    add_card(slide, 4.75, 3.6, 3.8, 3.3,
        'In Fiqh',
        [
            'Not blind taqlid,',
            'not reckless innovation.',
            '',
            'Qaradawi\u2019s methodology:',
            '  \u2022 Renewed ijtihad grounded',
            '    in authentic sources',
            '  \u2022 Middle position on zakat:',
            '    neither expanding beyond',
            '    classical categories nor',
            '    restricting to four only.',
        ])

    add_card(slide, 8.9, 3.6, 3.8, 3.3,
        'In Ethics',
        [
            'Not extremism, not secularism.',
            '',
            'Islam regulates freedom',
            'and keeps desire in check.',
            '',
            'Wasatiyyah is NOT compromise',
            'between truth and falsehood \u2014',
            'it is the straight path between',
            'two extremes of error.',
        ])
    add_footer(slide)


def make_theme3_sabr(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    y = add_slide_title(slide, 'Theme 3: Sabr \u2014 Patience & Perseverance', '\u0635\u064e\u0628\u0652\u0631 | Appearing 90+ times in the Qur\u2019an')

    y = add_arabic_box(slide, '\u0625\u0650\u0646\u0651\u064e \u0627\u0644\u0644\u0651\u064e\u0647\u064e \u0645\u064e\u0639\u064e \u0627\u0644\u0635\u0651\u064e\u0627\u0628\u0650\u0631\u0650\u064a\u0652\u0646\u064e', y + 0.05, Inches(0.7))
    y = add_translation(slide, '\u201cIndeed, Allah is with the patient.\u201d  \u2014 Qur\u2019an 2:153', y)

    add_stat_callout(slide, '3', 'Dimensions of Sabr', 0.8, y + 0.2, w=3.5, h=1.5)
    add_stat_callout(slide, '90+', 'Times in the Qur\u2019an', 4.9, y + 0.2, w=3.5, h=1.5)
    add_stat_callout(slide, '\u221e', 'Allah\u2019s company promised', 9.0, y + 0.2, w=3.5, h=1.5)

    add_card(slide, 0.6, 4.6, 3.8, 2.3,
        '1. Sabr fi al-Ta\u2019ah',
        [
            'Patience IN obedience.',
            '',
            'Persisting in prayer,',
            'fasting, zakat, and good',
            'deeds even when it is',
            'difficult or inconvenient.',
        ])

    add_card(slide, 4.75, 4.6, 3.8, 2.3,
        '2. Sabr \u2018an al-Ma\u2019siyah',
        [
            'Patience AGAINST sin.',
            '',
            'Steadfastly refusing',
            'temptation and resisting',
            'the pull of wrongdoing,',
            'even when easy to commit.',
        ])

    add_card(slide, 8.9, 4.6, 3.8, 2.3,
        '3. Sabr \u2018ala al-Musibah',
        [
            'Patience IN affliction.',
            '',
            'Enduring trials, loss,',
            'and hardship without',
            'despair \u2014 paired with',
            'hope (raja\u2019) in Allah.',
        ])
    add_footer(slide)


def make_theme4_marriage(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    y = add_slide_title(slide, 'Theme 4: Marriage & Family Life', '\u0646\u0650\u0643\u064e\u0627\u062d | Affection, mercy, and simplicity')

    y = add_arabic_box(slide, '\u0648\u064e\u0645\u0650\u0646\u0652 \u0622\u064a\u064e\u0627\u062a\u0650\u0647\u0650\u0670 \u0623\u064e\u0646\u0652 \u062e\u064e\u0644\u064e\u0642\u064e \u0644\u064e\u0643\u064f\u0645 \u0645\u0651\u0650\u0646\u0652 \u0623\u064e\u0646\u0641\u064f\u0633\u0650\u0643\u064f\u0645\u0652 \u0623\u064e\u0632\u0652\u0648\u064e\u0627\u062c\u064b\u0627 \u0644\u0651\u0650\u062a\u064e\u0633\u0652\u0643\u064f\u0646\u064f\u0648\u0627 \u0625\u0650\u0644\u064e\u064a\u0652\u0647\u064e\u0627 \u0648\u064e\u062c\u064e\u0639\u064e\u0644\u064e \u0628\u064e\u064a\u0652\u0646\u064e\u0643\u064f\u0645 \u0645\u0651\u064e\u0648\u064e\u062f\u0651\u064e\u0629\u064b \u0648\u064e\u0631\u064e\u062d\u0652\u0645\u064e\u0629\u064b', y + 0.05, Inches(0.75))
    y = add_translation(slide, '\u201cAnd among His signs is that He created for you mates... and placed between you affection and mercy.\u201d  \u2014 Qur\u2019an 30:21', y)

    add_quote_card(slide,
        'The best of marriages are the simplest ones. The best of dowries are the simplest ones.',
        'Prophet Muhammad (PBUH) (Abu Dawud 2117)',
        y + 0.05, Inches(0.85))

    add_card(slide, 0.6, 3.6, 5.8, 3.3,
        'Qaradawi\u2019s Principles for Families',
        [
            '1. Marriage is the foundation of society.',
            '   A solemn covenant (Q 4:21).',
            '',
            '2. Celibacy is rejected \u2014 \u2018No monasticism in Islam.\u2019',
            '   \u2018Your body has its rights, your wife has her rights.\u2019',
            '',
            '3. Dowries must be affordable.',
            '   Cultural dowry inflation obstructs the Sunnah.',
            '   Excessive weddings delay marriage \u2192 risk of sin.',
            '',
            '4. Spouse selection: religion & character first.',
            '   \u2018Marry the religious one; otherwise you will regret it.\u2019',
        ])

    add_card(slide, 6.9, 3.6, 5.8, 3.3,
        'Affection, Mercy & Mutual Rights',
        [
            'Marriage is built on mawaddah (affection)',
            'and rahmah (mercy) \u2014 Q 30:21.',
            '',
            'The Qur\u2019an uses \u2018you\u2019 (plural, not dual):',
            '  affection and mercy flow FROM the couple',
            '  TO the rest of the family and society.',
            '',
            'Kindness to wives is commanded:',
            '  \u2018Live with them in kindness\u2019 (Q 4:19).',
            '',
            'The community must help the poor marry \u2014',
            '  zakat funds may be used for this purpose.',
            '',
            'Divorce: \u2018Most hated of permissible things.\u2019',
        ])
    add_footer(slide)


def make_theme5_tazkiyah(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    y = add_slide_title(slide, 'Theme 5: Tazkiyah & Ikhlas', '\u062a\u064e\u0632\u0652\u0643\u0650\u064a\u064e\u0629 | \u0625\u0650\u062e\u0652\u0644\u064e\u0627\u0635 | Purification and Sincerity')

    y = add_arabic_box(slide, '\u0642\u064e\u062f\u0652 \u0623\u064e\u0641\u0652\u0644\u064e\u062d\u064e \u0645\u064e\u0646 \u0632\u064e\u0643\u0651\u064e\u0649\u0670\u0647\u064e\u0627 \u0648\u064e\u0642\u064e\u062f\u0652 \u062e\u064e\u0627\u0628\u064e \u0645\u064e\u0646 \u062f\u064e\u0633\u0651\u064e\u0649\u0670\u0647\u064e\u0627', y + 0.05, Inches(0.7))
    y = add_translation(slide, '\u201cSuccessful is the one who purifies it, and failed is the one who corrupts it.\u201d  \u2014 Qur\u2019an 91:9-10', y)

    add_card(slide, 0.6, 2.7, 5.8, 4.2,
        'Tazkiyah \u2014 Spiritual Purification',
        [
            'Tazkiyah = cleansing the soul from vice',
            'and cultivating virtue.',
            '',
            'DUAL meaning from the same root (z-k-w):',
            '  \u2022 Tazkiyat al-nafs = purification of SOUL',
            '  \u2022 Tazkiyat al-mal = purification of WEALTH',
            '',
            'The Sunnah is \u2018the agreed-upon source',
            'for the purification of the soul.\u2019',
            '',
            'Tazkiyah is NOT passive mysticism \u2014',
            'it is an active, knowledge-driven process',
            'of choosing virtue over vice.',
            '',
            'Key: \u2018Moral life is founded on',
            'knowledge and willpower.\u2019',
        ])

    add_card(slide, 6.9, 2.7, 5.8, 4.2,
        'Ikhlas \u2014 Sincerity in Worship',
        [
            'Ikhlas = purifying intention for Allah alone,',
            'free from showing off (riya\u2019) or worldly gain.',
            '',
            '\u2018They were not commanded except to worship',
            'Allah, sincere to Him in religion.\u2019 (Q 98:5)',
            '',
            'Three key positions:',
            '',
            '1. Ikhlas is the CRITERION for acceptance',
            '   of deeds \u2014 not the outward magnitude.',
            '   \u2018Actions are but by intentions.\u2019',
            '',
            '2. Ikhlas + ijtihad must go together \u2014',
            '   a jurist must seek truth, not fame.',
            '',
            '3. Zakat requires ikhlas \u2014 without it,',
            '   the spiritual purpose is lost.',
        ])
    add_footer(slide)


def make_reflection_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    add_slide_title(slide, 'Reflection & Discussion', 'Questions for the family circle')

    questions = [
        ('1', 'Which of the five themes resonates most with our family today, and why?'),
        ('2', 'How can we practice wasatiyyah (moderation) in our daily family routine \u2014 in worship, screen time, spending, and discipline?'),
        ('3', 'What is one practical way we can simplify our next family celebration (wedding, aqiqah, eid) following the Prophetic principle of ease?'),
        ('4', 'Which of the three dimensions of sabr is most needed in our household right now \u2014 patience in obedience, against sin, or in hardship?'),
        ('5', 'How do we cultivate ikhlas in our children \u2014 teaching them to do good for Allah\u2019s sake, not for praise or reward?'),
    ]

    for i, (num, q) in enumerate(questions):
        yi = 1.35 + i * 1.05
        add_section_icon_circle(slide, num, 0.7, yi, d=0.5)
        tx = slide.shapes.add_textbox(Inches(1.5), Inches(yi), Inches(11.0), Inches(0.85))
        tf = tx.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = q
        p.font.size = Pt(15); p.font.color.rgb = C_TEXT; p.font.name = 'Georgia'

    add_footer(slide)


def make_sources_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_SURFACE
    add_slide_title(slide, 'Sources & Further Reading', 'From the Qaradawi Library LLM Wiki')

    add_card(slide, 0.6, 1.3, 5.8, 5.5,
        'Books Referenced (9 ingested)',
        [
            '1. Ethics in Islam',
            '   3.6M chars | 4 chapters, 23 subsections',
            '',
            '2. Faith and Life',
            '   292K chars | 4 chapters',
            '',
            '3. The Lawful and the Prohibited in Islam',
            '   1.4M chars | 5 chapters (OCR recovered)',
            '',
            '4. Approaching the Sunnah',
            '   996K chars | 3 chapters',
            '',
            '5. Fiqh al-Zakah (2 volumes)',
            '   1.4M chars | 10 chapters',
            '',
            '6. Economic Security in Islam',
            '   608K chars | 7 chapters',
            '',
            '7. Education and Economy in the Sunnah',
            '8. Diversion and Arts in Islam',
            '9. Auspices of the Ultimate Victory of Islam',
        ])

    add_card(slide, 6.9, 1.3, 5.8, 2.5,
        'Concept Pages Used',
        [
            '\u2022 Akhlaq / Character',
            '\u2022 Wasatiyyah / The Middle Way',
            '\u2022 Sabr / Patience',
            '\u2022 Marriage / Nikah',
            '\u2022 Tazkiyah / Purification',
            '\u2022 Ikhlas / Sincerity',
            '\u2022 Dawah / Propagation',
            '\u2022 Responsibility / Mas\u2019uliyyah',
        ])

    add_card(slide, 6.9, 4.0, 5.8, 2.8,
        'About the Wiki',
        [
            'Total wiki pages: 135',
            'Concept pages: 48 full + 16 redirects',
            'Cross-book comparisons: 4',
            'Extracted corpus: ~9.4M characters',
            '',
            'Every claim traces to its source chapter.',
            'Summaries are AI-generated, grounded in',
            'the extracted text \u2014 not Qaradawi\u2019s own words.',
            'Verify any claim against the original.',
        ])
    add_footer(slide)


def make_conclusion_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C_PRIMARY_DK
    bb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), H - Inches(0.10), W, Inches(0.10))
    bb.fill.solid(); bb.fill.fore_color.rgb = C_ACCENT; bb.line.fill.background()
    tb = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), W, Inches(0.06))
    tb.fill.solid(); tb.fill.fore_color.rgb = C_ACCENT; tb.line.fill.background()

    tx = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), W - Inches(1.0), Inches(0.6))
    p = tx.text_frame.paragraphs[0]
    p.text = 'Closing Du\u2019a'
    p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = C_WHITE; p.font.name = 'Georgia'
    p.alignment = PP_ALIGN.CENTER

    tx2 = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), W - Inches(1.0), Inches(0.7))
    p2 = tx2.text_frame.paragraphs[0]
    p2.text = '\u0631\u064e\u0628\u0651\u064e\u0646\u064e\u0627 \u0647\u064e\u0628\u0652 \u0644\u064e\u0646\u064e\u0627 \u0645\u0650\u0646\u0652 \u0623\u064e\u0632\u0652\u0648\u064e\u0627\u062c\u0650\u0646\u064e\u0627 \u0648\u064e\u0630\u064f\u0631\u0651\u0650\u064a\u0651\u064e\u0627\u062a\u0650\u0646\u064e\u0627 \u0642\u064f\u0631\u0651\u064e\u0629\u064e \u0623\u064e\u0639\u0652\u064a\u064f\u0646\u064d'
    p2.font.size = Pt(24); p2.font.color.rgb = C_ACCENT; p2.alignment = PP_ALIGN.CENTER

    tx3 = slide.shapes.add_textbox(Inches(0.5), Inches(2.3), W - Inches(1.0), Inches(0.45))
    p3 = tx3.text_frame.paragraphs[0]
    p3.text = '\u201cOur Lord, grant us from among our spouses and offspring comfort to our eyes.\u201d'
    p3.font.size = Pt(15); p3.font.italic = True; p3.font.color.rgb = C_SURFACE; p3.alignment = PP_ALIGN.CENTER

    tx3b = slide.shapes.add_textbox(Inches(0.5), Inches(2.8), W - Inches(1.0), Inches(0.30))
    p3b = tx3b.text_frame.paragraphs[0]
    p3b.text = '\u2014 Qur\u2019an 25:74'
    p3b.font.size = Pt(12); p3b.font.color.rgb = C_SECONDARY; p3b.alignment = PP_ALIGN.CENTER

    tx4 = slide.shapes.add_textbox(Inches(1.0), Inches(3.4), W - Inches(2.0), Inches(1.6))
    tf4 = tx4.text_frame; tf4.word_wrap = True
    p4 = tf4.paragraphs[0]
    p4.text = 'These five themes \u2014 good character, moderation, patience, family bonds, and sincere purification \u2014 are not separate topics but one integrated vision: a family rooted in faith, balanced in practice, patient in trial, bound by affection, and sincere toward Allah.'
    p4.font.size = Pt(15); p4.font.color.rgb = C_SURFACE; p4.alignment = PP_ALIGN.CENTER
    p4.font.italic = True

    tx5 = slide.shapes.add_textbox(Inches(0.5), Inches(6.2), W - Inches(1.0), Inches(0.35))
    p5 = tx5.text_frame.paragraphs[0]
    p5.text = 'Qaradawi Library LLM Wiki  \u00b7  Halaqah Presentation  \u00b7  9 June 2026'
    p5.font.size = Pt(11); p5.font.color.rgb = C_SECONDARY; p5.alignment = PP_ALIGN.CENTER


# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════

if __name__ == '__main__':
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    prs.core_properties.author = 'Qaradawi Library LLM Wiki'
    prs.core_properties.title = 'Wisdom for the Family \u2014 Halaqah Presentation'
    prs.core_properties.subject = 'Halaqah presentation from the works of Yusuf al-Qaradawi'

    make_title_slide(prs)
    make_about_slide(prs)
    make_agenda_slide(prs)
    make_theme1_akhlaq(prs)
    make_theme2_wasatiyyah(prs)
    make_theme3_sabr(prs)
    make_theme4_marriage(prs)
    make_theme5_tazkiyah(prs)
    make_reflection_slide(prs)
    make_sources_slide(prs)
    make_conclusion_slide(prs)

    out_path = '/root/qaradawi-library/halaqah-wisdom-for-the-family.pptx'
    prs.save(out_path)
    print(f'Saved: {out_path}')
    print(f'Slides: {len(prs.slides)}')