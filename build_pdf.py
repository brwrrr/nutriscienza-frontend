"""
Genera un PDF di esempio del Piano Base NutriScienza per Giulia M.
Utilizza ReportLab platypus con stili custom coerenti col brand della landing.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, NextPageTemplate, FrameBreak
)
from reportlab.pdfgen import canvas
from datetime import datetime

# ---------- Brand palette ----------
GREEN_DEEP = HexColor("#2D5F3F")
GREEN_DARK = HexColor("#1A2E22")
GREEN_SOFT = HexColor("#4A8264")
GREEN_TINT = HexColor("#E8F0EB")
CREAM = HexColor("#F5F1E8")
CREAM_LIGHT = HexColor("#FBF9F4")
GOLD = HexColor("#C9A66B")
GOLD_DARK = HexColor("#A88349")
TEXT = HexColor("#2A2A2A")
TEXT_MUTED = HexColor("#6B6B6B")
BORDER = HexColor("#E5E0D3")

# ---------- Output ----------
OUTPUT = "/sessions/affectionate-youthful-sagan/mnt/outputs/nutriscienza_piano_base_esempio.pdf"

# ---------- Styles ----------
styles = getSampleStyleSheet()

H1 = ParagraphStyle('H1', parent=styles['Heading1'],
    fontName='Helvetica-Bold', fontSize=28, textColor=GREEN_DEEP,
    leading=34, spaceAfter=14, spaceBefore=0)
H2 = ParagraphStyle('H2', parent=styles['Heading2'],
    fontName='Helvetica-Bold', fontSize=18, textColor=GREEN_DEEP,
    leading=22, spaceAfter=10, spaceBefore=14)
H3 = ParagraphStyle('H3', parent=styles['Heading3'],
    fontName='Helvetica-Bold', fontSize=13, textColor=GREEN_DEEP,
    leading=16, spaceAfter=6, spaceBefore=10)
EYEBROW = ParagraphStyle('Eyebrow', parent=styles['Normal'],
    fontName='Helvetica-Bold', fontSize=9, textColor=GOLD_DARK,
    leading=11, spaceAfter=6, letterSpacing=1.5)
BODY = ParagraphStyle('Body', parent=styles['Normal'],
    fontName='Helvetica', fontSize=10.5, textColor=TEXT,
    leading=15, spaceAfter=8, alignment=TA_LEFT)
BODY_JUST = ParagraphStyle('BodyJust', parent=BODY, alignment=TA_JUSTIFY)
LEAD = ParagraphStyle('Lead', parent=BODY,
    fontSize=12, leading=17, textColor=TEXT_MUTED, spaceAfter=14)
SMALL = ParagraphStyle('Small', parent=BODY,
    fontSize=8.5, leading=12, textColor=TEXT_MUTED)
META_LABEL = ParagraphStyle('MetaLabel', parent=BODY,
    fontSize=8, textColor=TEXT_MUTED, leading=10,
    fontName='Helvetica-Bold', spaceAfter=2)
META_VALUE = ParagraphStyle('MetaVal', parent=BODY,
    fontSize=14, textColor=GREEN_DEEP, leading=18,
    fontName='Helvetica-Bold')
COVER_TITLE = ParagraphStyle('CoverTitle', parent=H1,
    fontSize=44, leading=50, textColor=GREEN_DEEP, spaceAfter=10)
COVER_SUB = ParagraphStyle('CoverSub', parent=BODY,
    fontSize=14, leading=20, textColor=TEXT_MUTED, spaceAfter=20)

# ---------- Page decorations ----------
def page_header_footer(canv, doc, show_header=True):
    """Header with brand mark + page footer."""
    canv.saveState()
    width, height = A4

    if show_header:
        # Top bar
        canv.setFillColor(GREEN_DEEP)
        canv.rect(0, height - 0.45*cm, width, 0.45*cm, fill=1, stroke=0)
        # Brand mark in header
        canv.setFont('Helvetica-Bold', 10)
        canv.setFillColor(GREEN_DEEP)
        canv.drawString(2*cm, height - 1.1*cm, "NutriScienza")
        canv.setFillColor(GOLD_DARK)
        canv.drawString(2*cm + 2.6*cm, height - 1.1*cm, "·")
        canv.setFillColor(TEXT_MUTED)
        canv.setFont('Helvetica', 9)
        canv.drawString(2*cm + 2.85*cm, height - 1.1*cm, "Piano Base · Giulia M.")
        # Right side
        canv.setFillColor(TEXT_MUTED)
        canv.setFont('Helvetica', 8.5)
        canv.drawRightString(width - 2*cm, height - 1.1*cm, "nutriscienza.org")

    # Footer
    canv.setStrokeColor(BORDER)
    canv.setLineWidth(0.4)
    canv.line(2*cm, 1.6*cm, width - 2*cm, 1.6*cm)
    canv.setFont('Helvetica', 8)
    canv.setFillColor(TEXT_MUTED)
    canv.drawString(2*cm, 1*cm, "© 2026 NutriScienza S.r.l. — Conforme alle linee guida LARN")
    canv.drawRightString(width - 2*cm, 1*cm, f"Pagina {doc.page}")
    canv.restoreState()

def cover_page(canv, doc):
    """Special cover layout — no header/footer."""
    canv.saveState()
    width, height = A4

    # Big cream block on top half
    canv.setFillColor(CREAM)
    canv.rect(0, height/2, width, height/2, fill=1, stroke=0)

    # Green accent bar at top
    canv.setFillColor(GREEN_DEEP)
    canv.rect(0, height - 0.6*cm, width, 0.6*cm, fill=1, stroke=0)

    # Logo top-left
    canv.setFont('Helvetica-Bold', 16)
    canv.setFillColor(GREEN_DEEP)
    canv.drawString(2*cm, height - 2*cm, "Nutri")
    text_width = canv.stringWidth("Nutri", 'Helvetica-Bold', 16)
    canv.setFillColor(GOLD)
    canv.drawString(2*cm + text_width, height - 2*cm, "Scienza")

    # Eyebrow
    canv.setFont('Helvetica-Bold', 9)
    canv.setFillColor(GOLD_DARK)
    canv.drawString(2*cm, height - 5*cm, "PIANO BASE  ·  7 GIORNI")

    # Title
    canv.setFont('Helvetica-Bold', 36)
    canv.setFillColor(GREEN_DEEP)
    canv.drawString(2*cm, height - 7*cm, "Il tuo piano")
    canv.drawString(2*cm, height - 8.4*cm, "alimentare")
    canv.setFillColor(GREEN_SOFT)
    canv.drawString(2*cm, height - 9.8*cm, "personalizzato.")

    # Decorative line
    canv.setStrokeColor(GOLD)
    canv.setLineWidth(2)
    canv.line(2*cm, height - 11*cm, 4.5*cm, height - 11*cm)

    # Customer block (white card on cream lower half)
    canv.setFillColor(white)
    canv.setStrokeColor(BORDER)
    canv.setLineWidth(0.6)
    canv.roundRect(2*cm, height/2 - 6*cm, width - 4*cm, 4.8*cm, 0.3*cm, fill=1, stroke=1)

    canv.setFont('Helvetica-Bold', 8)
    canv.setFillColor(TEXT_MUTED)
    canv.drawString(2.6*cm, height/2 - 1*cm, "PREPARATO PER")
    canv.setFont('Helvetica-Bold', 22)
    canv.setFillColor(GREEN_DEEP)
    canv.drawString(2.6*cm, height/2 - 1.8*cm, "Giulia M.")
    canv.setFont('Helvetica', 11)
    canv.setFillColor(TEXT_MUTED)
    canv.drawString(2.6*cm, height/2 - 2.5*cm, "Milano · 34 anni · Obiettivo: dimagrimento sostenibile")

    # Date and validity
    canv.setStrokeColor(BORDER)
    canv.line(2.6*cm, height/2 - 3.2*cm, width - 2.6*cm, height/2 - 3.2*cm)

    today = datetime.now().strftime("%d %B %Y").lower()
    months_it = {'january':'gennaio','february':'febbraio','march':'marzo','april':'aprile',
                 'may':'maggio','june':'giugno','july':'luglio','august':'agosto',
                 'september':'settembre','october':'ottobre','november':'novembre','december':'dicembre'}
    for en, it in months_it.items():
        today = today.replace(en, it)

    canv.setFont('Helvetica-Bold', 8)
    canv.setFillColor(TEXT_MUTED)
    canv.drawString(2.6*cm, height/2 - 4*cm, "DATA DI EMISSIONE")
    canv.setFont('Helvetica', 11)
    canv.setFillColor(TEXT)
    canv.drawString(2.6*cm, height/2 - 4.7*cm, today.capitalize())

    canv.setFont('Helvetica-Bold', 8)
    canv.setFillColor(TEXT_MUTED)
    canv.drawString(11*cm, height/2 - 4*cm, "VALIDITÀ DEL PIANO")
    canv.setFont('Helvetica', 11)
    canv.setFillColor(TEXT)
    canv.drawString(11*cm, height/2 - 4.7*cm, "7 giorni")

    # Authority line at bottom
    canv.setFont('Helvetica', 9)
    canv.setFillColor(TEXT_MUTED)
    canv.drawCentredString(width/2, 3.2*cm,
        "Metodologia conforme alle linee guida LARN — Società Italiana di Nutrizione Umana (SINU)")
    canv.drawCentredString(width/2, 2.7*cm,
        "Calcoli energetici basati sull'equazione Mifflin-St Jeor (1990)")

    # Bottom accent
    canv.setFillColor(GREEN_DEEP)
    canv.rect(0, 0, width, 0.6*cm, fill=1, stroke=0)
    canv.setFillColor(GOLD)
    canv.rect(0, 0.6*cm, width, 0.15*cm, fill=1, stroke=0)

    canv.restoreState()

# ---------- Doc setup ----------
class PianoDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4,
            leftMargin=2*cm, rightMargin=2*cm,
            topMargin=2*cm, bottomMargin=2.2*cm,
            title="NutriScienza — Piano Base", author="NutriScienza")

        cover_frame = Frame(0, 0, A4[0], A4[1], id='cover',
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        normal_frame = Frame(self.leftMargin, self.bottomMargin,
            self.width, self.height, id='normal')

        self.addPageTemplates([
            PageTemplate(id='Cover', frames=[cover_frame], onPage=cover_page),
            PageTemplate(id='Normal', frames=[normal_frame], onPage=page_header_footer),
        ])

# ---------- Helpers ----------
def metric_card(label, value, sub=""):
    """Build a small KPI-style card as a single-cell table."""
    inner = [
        [Paragraph(label.upper(), META_LABEL)],
        [Paragraph(value, META_VALUE)],
    ]
    if sub:
        inner.append([Paragraph(sub, SMALL)])
    t = Table(inner, colWidths=[4.2*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CREAM_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    return t

def meal_table(day_label, meals):
    """Build a styled meal table for a day."""
    rows = [[Paragraph(f"<b>{day_label}</b>", H3), Paragraph("", BODY)]]
    for meal_name, meal_text, kcal in meals:
        rows.append([
            Paragraph(f"<b>{meal_name}</b>", BODY),
            Paragraph(meal_text, BODY),
            Paragraph(f"{kcal} kcal", SMALL),
        ])

    # Restructure: header + 5 meal rows
    header_row = [Paragraph(f"<b>{day_label}</b>", ParagraphStyle('DH', parent=H3, textColor=white, spaceBefore=0, spaceAfter=0)), "", ""]
    body_rows = []
    for meal_name, meal_text, kcal in meals:
        body_rows.append([
            Paragraph(f"<b>{meal_name}</b>", BODY),
            Paragraph(meal_text, BODY),
            Paragraph(f"<b>{kcal}</b> kcal", SMALL),
        ])

    data = [header_row] + body_rows
    t = Table(data, colWidths=[3.2*cm, 11*cm, 2.3*cm])
    style = TableStyle([
        # Header row
        ('BACKGROUND', (0,0), (-1,0), GREEN_DEEP),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('SPAN', (0,0), (-1,0)),
        ('LEFTPADDING', (0,0), (-1,0), 14),
        ('TOPPADDING', (0,0), (-1,0), 8),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        # Body rows
        ('BACKGROUND', (0,1), (-1,-1), white),
        ('LINEBELOW', (0,1), (-1,-2), 0.4, BORDER),
        ('LEFTPADDING', (0,1), (-1,-1), 12),
        ('RIGHTPADDING', (0,1), (-1,-1), 12),
        ('TOPPADDING', (0,1), (-1,-1), 9),
        ('BOTTOMPADDING', (0,1), (-1,-1), 9),
        ('VALIGN', (0,1), (-1,-1), 'TOP'),
        # Box
        ('BOX', (0,0), (-1,-1), 0.6, BORDER),
        ('ALIGN', (2,1), (2,-1), 'RIGHT'),
    ])
    t.setStyle(style)
    return t

def info_box(title, body_html, accent=GREEN_DEEP):
    """Colored callout box."""
    inner = [
        [Paragraph(f"<b>{title}</b>", ParagraphStyle('IBT', parent=BODY, fontSize=11, textColor=accent, spaceAfter=4))],
        [Paragraph(body_html, BODY)],
    ]
    t = Table(inner, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GREEN_TINT),
        ('LINEBEFORE', (0,0), (0,-1), 3, accent),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ]))
    return t

# ---------- Content ----------
story = []

# === PAGE 1: COVER (handled by cover_page) ===
story.append(NextPageTemplate('Normal'))
story.append(PageBreak())

# === PAGE 2: Il tuo profilo nutrizionale ===
story.append(Paragraph("IL TUO PROFILO", EYEBROW))
story.append(Paragraph("I numeri che contano per te.", H1))
story.append(Paragraph(
    "Abbiamo calcolato il tuo fabbisogno energetico utilizzando la formula di Mifflin-St Jeor — "
    "lo standard scientifico più validato per stimare il metabolismo basale — "
    "applicando un fattore di attività moderato e un deficit calorico controllato del 18%, "
    "in linea con le raccomandazioni LARN per un dimagrimento sostenibile.",
    BODY_JUST))
story.append(Spacer(1, 12))

# Profile data table
profile_data = [
    [Paragraph("<b>Età</b>", BODY), Paragraph("34 anni", BODY),
     Paragraph("<b>Sesso</b>", BODY), Paragraph("Femminile", BODY)],
    [Paragraph("<b>Altezza</b>", BODY), Paragraph("165 cm", BODY),
     Paragraph("<b>Peso attuale</b>", BODY), Paragraph("68,0 kg", BODY)],
    [Paragraph("<b>BMI</b>", BODY), Paragraph("25,0 (sovrappeso lieve)", BODY),
     Paragraph("<b>Peso obiettivo</b>", BODY), Paragraph("63,0 kg (-5 kg)", BODY)],
    [Paragraph("<b>Attività</b>", BODY), Paragraph("Moderata (1,55)", BODY),
     Paragraph("<b>Allenamenti</b>", BODY), Paragraph("3-4 volte/sett.", BODY)],
]
profile_table = Table(profile_data, colWidths=[2.5*cm, 4.8*cm, 3*cm, 6.2*cm])
profile_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), CREAM_LIGHT),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(profile_table)
story.append(Spacer(1, 18))

# Calculated metrics
story.append(Paragraph("Il tuo fabbisogno calcolato", H3))
story.append(Spacer(1, 8))

metrics_data = [[
    metric_card("Metabolismo basale", "1.380", "kcal — BMR (Mifflin-St Jeor)"),
    metric_card("Fabbisogno totale", "2.139", "kcal — TDEE (con attività)"),
    metric_card("Target giornaliero", "1.750", "kcal — deficit -18%"),
]]
metrics_table = Table(metrics_data, colWidths=[5.6*cm, 5.6*cm, 5.6*cm])
metrics_table.setStyle(TableStyle([
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
]))
story.append(metrics_table)
story.append(Spacer(1, 18))

story.append(Paragraph("Ripartizione macronutrienti", H3))
macro_data = [
    [Paragraph("<b>Macronutriente</b>", BODY), Paragraph("<b>% kcal</b>", BODY),
     Paragraph("<b>Grammi/giorno</b>", BODY), Paragraph("<b>Funzione</b>", BODY)],
    [Paragraph("Proteine", BODY), Paragraph("28%", BODY),
     Paragraph("123 g (1,8 g/kg)", BODY), Paragraph("Preserva la massa muscolare durante il deficit", BODY)],
    [Paragraph("Carboidrati", BODY), Paragraph("42%", BODY),
     Paragraph("184 g", BODY), Paragraph("Energia per allenamenti e cervello", BODY)],
    [Paragraph("Grassi", BODY), Paragraph("30%", BODY),
     Paragraph("58 g", BODY), Paragraph("Equilibrio ormonale e sazietà", BODY)],
]
macro_table = Table(macro_data, colWidths=[3.5*cm, 2*cm, 3.8*cm, 7.2*cm])
macro_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), GREEN_DEEP),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('BACKGROUND', (0,1), (-1,-1), white),
    ('GRID', (0,0), (-1,-1), 0.4, BORDER),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 9),
    ('BOTTOMPADDING', (0,0), (-1,-1), 9),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
# Override header styling for macro table
for r in range(1, len(macro_data)):
    for c in range(len(macro_data[0])):
        macro_data[r][c].style = BODY
story.append(macro_table)
story.append(Spacer(1, 16))

story.append(info_box(
    "Perché questa ripartizione?",
    "L'apporto proteico più alto della media (1,8 g per kg di peso corporeo) è specifico per il tuo "
    "obiettivo: durante un deficit calorico è il principale fattore protettivo contro la perdita di "
    "massa muscolare, oltre a garantire una maggiore sazietà. La quota di carboidrati resta sufficiente "
    "a sostenere 3-4 allenamenti settimanali senza compromettere la performance."))

story.append(PageBreak())

# === PAGE 3: Metodologia ===
story.append(Paragraph("LA METODOLOGIA", EYEBROW))
story.append(Paragraph("Come abbiamo costruito questo piano.", H1))

story.append(Paragraph("1. Calcolo del metabolismo basale (BMR)", H2))
story.append(Paragraph(
    "Utilizziamo l'equazione di <b>Mifflin-St Jeor</b> (1990), considerata oggi lo standard più "
    "accurato dalla letteratura scientifica per stimare il dispendio energetico a riposo nella popolazione "
    "adulta sana. È la formula raccomandata dall'Academy of Nutrition and Dietetics e citata nelle "
    "linee guida LARN.",
    BODY_JUST))
story.append(Spacer(1, 6))
formula_table = Table([[
    Paragraph("<b>Formula applicata (donna):</b><br/>"
              "BMR = (10 × peso kg) + (6,25 × altezza cm) − (5 × età) − 161<br/>"
              "BMR = (10 × 68) + (6,25 × 165) − (5 × 34) − 161 = <b>1.380 kcal</b>",
              BODY)
]], colWidths=[16.5*cm])
formula_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), CREAM_LIGHT),
    ('LINEBEFORE', (0,0), (0,-1), 3, GOLD),
    ('LEFTPADDING', (0,0), (-1,-1), 14),
    ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
]))
story.append(formula_table)
story.append(Spacer(1, 12))

story.append(Paragraph("2. Fabbisogno energetico totale (TDEE)", H2))
story.append(Paragraph(
    "Al BMR applichiamo un fattore di attività (PAL) basato sulle abitudini dichiarate. "
    "Un livello moderato — corrispondente a 3-4 allenamenti settimanali e una quotidianità non sedentaria — "
    "corrisponde a un coefficiente di <b>1,55</b>. TDEE = 1.380 × 1,55 = <b>2.139 kcal</b>.",
    BODY_JUST))
story.append(Spacer(1, 12))

story.append(Paragraph("3. Deficit calorico controllato", H2))
story.append(Paragraph(
    "Per un dimagrimento sostenibile evitiamo deficit aggressivi: applichiamo una riduzione del "
    "<b>18% sul TDEE</b>, che corrisponde a circa 390 kcal in meno al giorno e una perdita "
    "attesa di 0,4-0,5 kg a settimana. Deficit superiori al 25% nel medio termine sono associati "
    "in letteratura a maggiore perdita di massa muscolare, alterazioni ormonali e maggiore probabilità di "
    "recupero del peso (effetto rebound).",
    BODY_JUST))
story.append(Spacer(1, 12))

story.append(Paragraph("4. Ripartizione dei macronutrienti", H2))
story.append(Paragraph(
    "L'apporto proteico è impostato a 1,8 g/kg di peso corporeo, "
    "in linea con le evidenze sulla preservazione della massa magra durante il deficit "
    "(Helms et al., 2014; Phillips & Van Loon, 2011). Carboidrati e grassi sono distribuiti per "
    "garantire energia agli allenamenti e supporto ormonale.",
    BODY_JUST))

story.append(Spacer(1, 16))
story.append(info_box(
    "Riferimenti scientifici",
    "Le scelte di questo piano sono basate sulle <b>linee guida LARN</b> (Livelli di Assunzione di "
    "Riferimento di Nutrienti) della Società Italiana di Nutrizione Umana (SINU, 2014, IV revisione), "
    "sui <i>Dietary Reference Intakes</i> dell'Institute of Medicine, e sulla letteratura peer-reviewed "
    "in nutrizione applicata.",
    accent=GOLD_DARK))

story.append(PageBreak())

# === PAGES 4-7: Meal plan (2 days per page) ===
story.append(Paragraph("IL TUO MENÙ — 7 GIORNI", EYEBROW))
story.append(Paragraph("Cosa mangerai questa settimana.", H1))
story.append(Paragraph(
    "Pasti pensati sull'alimentazione mediterranea, varianti realistiche, ingredienti facilmente "
    "reperibili in qualsiasi supermercato italiano. Le grammature sono indicative del peso a crudo "
    "salvo diversa indicazione.",
    LEAD))

# Days
days = [
    ("Lunedì", [
        ("Colazione", "Yogurt greco 0% (170 g) con frutti di bosco freschi (80 g), fiocchi d'avena (30 g) e un cucchiaino di miele.", 350),
        ("Spuntino", "1 mela media + 10 mandorle non salate.", 180),
        ("Pranzo", "Pasta integrale (70 g) con sugo di pomodoro fresco e tonno al naturale (80 g sgocciolato), insalata mista con olio EVO (1 cucchiaino).", 540),
        ("Spuntino", "Tisana + 2 gallette di riso integrale con ricotta (30 g) e un filo di miele.", 130),
        ("Cena", "Petto di pollo alla griglia (130 g) con verdure miste grigliate (200 g) e 1 fetta di pane integrale (40 g).", 470),
    ]),
    ("Martedì", [
        ("Colazione", "2 fette di pane integrale tostato (60 g) con ricotta (60 g) e marmellata senza zuccheri aggiunti, caffè o tè.", 360),
        ("Spuntino", "1 yogurt greco 0% (150 g) con cannella.", 110),
        ("Pranzo", "Insalatona di farro (60 g a crudo) con ceci lessati (80 g), pomodorini, feta (40 g), basilico, olio EVO.", 530),
        ("Spuntino", "1 banana + 1 quadretto di cioccolato fondente 85%.", 150),
        ("Cena", "Filetto di salmone al forno (140 g) con spinaci saltati in padella (200 g) e patate al forno (150 g).", 580),
    ]),
    ("Mercoledì", [
        ("Colazione", "Porridge di avena (40 g) cotto in latte parzialmente scremato (200 ml) con ½ banana e cannella.", 340),
        ("Spuntino", "1 pera + noci (15 g).", 170),
        ("Pranzo", "Riso integrale (70 g) con zucchine, gamberetti (100 g), prezzemolo e limone.", 510),
        ("Spuntino", "Bastoncini di carota + hummus di ceci (30 g).", 130),
        ("Cena", "Frittata con 2 uova intere + 2 albumi, asparagi, parmigiano (10 g), insalata mista. 1 fetta pane integrale.", 510),
    ]),
    ("Giovedì", [
        ("Colazione", "Yogurt greco 0% (170 g) con granola integrale senza zuccheri (35 g) e mirtilli.", 360),
        ("Spuntino", "1 kiwi + 5 mandorle.", 120),
        ("Pranzo", "Pasta integrale (70 g) con pesto leggero alla genovese, fagiolini lessati (150 g), parmigiano (15 g).", 560),
        ("Spuntino", "Tè verde + 2 fette biscottate integrali con un velo di miele.", 110),
        ("Cena", "Polpette di tacchino al forno (120 g carne) con verdure miste e quinoa (60 g a crudo).", 490),
    ]),
    ("Venerdì", [
        ("Colazione", "Pancake proteici (1 uovo + 30 g avena + ½ banana + albumi), frutti di bosco e un velo di sciroppo d'acero.", 380),
        ("Spuntino", "1 mela + parmigiano (20 g).", 150),
        ("Pranzo", "Vellutata di lenticchie (200 g a fine cottura) con crostini integrali, insalata di cetrioli e cipolla.", 510),
        ("Spuntino", "1 yogurt naturale (125 g) con cannella.", 90),
        ("Cena", "Branzino al forno (150 g) con olive taggiasche e pomodorini, verdure grigliate, 1 fetta pane integrale.", 560),
    ]),
    ("Sabato", [
        ("Colazione", "Smoothie bowl: 1 banana, 150 ml latte di mandorla, 30 g fiocchi d'avena, frutti rossi, 10 g semi di chia.", 380),
        ("Spuntino", "1 arancia.", 70),
        ("Pranzo", "Risotto allo zafferano (70 g riso) con bocconcini di pollo (100 g) e asparagi.", 580),
        ("Spuntino", "2 noci + tisana al finocchio.", 110),
        ("Cena", "Pizza casalinga su base integrale (100 g pasta) con mozzarella light (80 g), pomodoro, rucola, prosciutto crudo sgrassato (30 g).", 590),
    ]),
    ("Domenica", [
        ("Colazione", "2 fette pane integrale + ½ avocado + 1 uovo in camicia + caffè.", 400),
        ("Spuntino", "Macedonia di stagione (200 g).", 140),
        ("Pranzo", "Lasagna casalinga porzione moderata (180 g) con insalata mista. — il piatto della domenica.", 620),
        ("Spuntino", "1 yogurt greco 0%.", 90),
        ("Cena", "Crema di zucca (250 ml) + bruschetta integrale e insalata di tonno al naturale (60 g) con cipolla rossa.", 460),
    ]),
]

# Render 2 days per page
for i, (day_label, meals) in enumerate(days):
    story.append(meal_table(day_label, meals))
    story.append(Spacer(1, 14))
    if i % 2 == 1 and i < len(days) - 1:
        story.append(PageBreak())

story.append(PageBreak())

# === PAGE: Lista della spesa ===
story.append(Paragraph("LISTA DELLA SPESA", EYEBROW))
story.append(Paragraph("Una settimana, una sola spesa.", H1))
story.append(Paragraph(
    "Quantità calcolate per i 7 giorni di piano. Suggeriamo di fare una spesa unica all'inizio della "
    "settimana e una piccola integrazione di freschi (frutta, verdura) a metà settimana.",
    LEAD))

shopping = [
    ("Verdura e frutta fresca", [
        "Pomodorini · 500 g", "Pomodori · 4 medi", "Insalata mista · 2 buste",
        "Spinaci freschi · 250 g", "Asparagi · 400 g", "Zucchine · 4 medie",
        "Fagiolini · 200 g", "Cetrioli · 2", "Carote · 500 g",
        "Cipolla rossa · 1", "Zucca · 600 g", "Patate · 300 g",
        "Rucola · 1 busta", "Mele · 4", "Banane · 4", "Pere · 2",
        "Kiwi · 2", "Arance · 2", "Frutti di bosco freschi · 250 g",
        "Avocado · 1", "Limoni · 2",
    ]),
    ("Carne, pesce e uova", [
        "Petto di pollo · 230 g", "Filetto di salmone · 140 g",
        "Branzino · 1 (300 g)", "Tonno al naturale · 2 scatolette (140 g)",
        "Gamberetti surgelati · 100 g", "Macinato di tacchino · 120 g",
        "Prosciutto crudo sgrassato · 30 g", "Uova fresche · 6",
    ]),
    ("Latticini", [
        "Yogurt greco 0% · 6 vasetti (150 g)", "Yogurt naturale · 1 vasetto",
        "Ricotta vaccina · 100 g", "Parmigiano Reggiano · 60 g",
        "Mozzarella light · 80 g", "Feta · 40 g", "Latte parz. scremato · 1 L",
        "Latte di mandorla · 200 ml",
    ]),
    ("Cereali, legumi e pane", [
        "Pasta integrale · 250 g", "Riso integrale · 70 g",
        "Riso Carnaroli · 70 g", "Farro perlato · 60 g", "Quinoa · 60 g",
        "Avena (fiocchi) · 200 g", "Pane integrale · 1 filone (400 g)",
        "Fette biscottate integrali · 1 confezione",
        "Gallette di riso integrale · 1 confezione",
        "Ceci lessati · 1 barattolo (240 g)",
        "Lenticchie secche · 100 g", "Pasta lasagne pronta · 100 g",
    ]),
    ("Frutta secca, semi e grassi", [
        "Mandorle non salate · 50 g", "Noci · 30 g", "Semi di chia · 20 g",
        "Olive taggiasche · 30 g", "Olio EVO · per uso settimanale",
    ]),
    ("Dispensa", [
        "Miele · 1 vasetto", "Marmellata senza zuccheri aggiunti · 1 vasetto",
        "Sciroppo d'acero · piccola bottiglia", "Pesto pronto leggero · 1 vasetto",
        "Sugo di pomodoro · 400 g", "Hummus di ceci · 30 g",
        "Cioccolato fondente 85% · 1 tavoletta (per spuntini)",
        "Granola integrale senza zuccheri · 200 g",
        "Caffè / tè verde / tisane · a piacere",
        "Cannella, prezzemolo, basilico, zafferano",
    ]),
]

for category, items in shopping:
    story.append(Paragraph(category, H3))
    # 3-column list
    rows = []
    row = []
    for it in items:
        row.append(Paragraph(f"• {it}", BODY))
        if len(row) == 3:
            rows.append(row); row = []
    while len(row) < 3 and len(row) > 0:
        row.append(Paragraph("", BODY))
    if row: rows.append(row)
    t = Table(rows, colWidths=[5.7*cm]*3)
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

story.append(PageBreak())

# === PAGE: Note + disclaimer ===
story.append(Paragraph("NOTE METODOLOGICHE DEL PIANO", EYEBROW))
story.append(Paragraph("Cinque consigli che fanno la differenza.", H1))

tips = [
    ("Idratazione",
     "Punta a 2-2,5 litri di acqua al giorno. Caffè e tisane contano per circa metà del loro volume. "
     "L'idratazione corretta ha un effetto diretto sulla sazietà e sul metabolismo."),
    ("Tempistica dei carboidrati",
     "Concentra la quota maggiore di carboidrati nei pasti pre e post allenamento — è quando il muscolo "
     "li utilizza meglio. La sera, se non ti alleni, riduci leggermente la porzione di pane o pasta."),
    ("Settimo giorno: la domenica italiana",
     "La lasagna domenicale è prevista nel piano. Mangiare in modo flessibile in occasioni sociali è "
     "parte di un percorso sostenibile. La rigidità totale è il principale predittore di abbandono."),
    ("Pesa al mattino, una volta a settimana",
     "Una sola misurazione settimanale (stessa ora, stesse condizioni) è più affidabile del controllo "
     "quotidiano, che genera ansia per oscillazioni fisiologiche fino a 2 kg legate ad acqua e glicogeno."),
    ("Sonno: il pilastro nascosto",
     "Dormire meno di 7 ore peggiora la regolazione di leptina e grelina, gli ormoni della fame. "
     "Per ogni piano alimentare, il sonno è un acceleratore o un freno."),
]

for title, text in tips:
    story.append(Paragraph(f"<b>{title}</b>", H3))
    story.append(Paragraph(text, BODY_JUST))
    story.append(Spacer(1, 8))

story.append(Spacer(1, 18))

# Disclaimer box
disclaimer = Table([[
    Paragraph("<b>AVVERTENZA IMPORTANTE</b>", ParagraphStyle('DT', parent=BODY,
        fontSize=10, textColor=GOLD_DARK, fontName='Helvetica-Bold', spaceAfter=6)),
], [
    Paragraph(
        "Questo piano alimentare ha finalità educative ed è basato sulle linee guida LARN della Società "
        "Italiana di Nutrizione Umana. <b>Non sostituisce il parere di un medico, di un dietologo o di "
        "un biologo nutrizionista in presenza di condizioni patologiche</b> (diabete, patologie tiroidee, "
        "renali, cardiovascolari, disturbi del comportamento alimentare, gravidanza e allattamento). "
        "In caso di dubbi consulta sempre il tuo medico curante prima di iniziare un nuovo regime alimentare. "
        "NutriScienza S.r.l. non assume responsabilità per usi del piano in difformità rispetto alle presenti indicazioni.",
        SMALL)
]], colWidths=[16.5*cm])
disclaimer.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), CREAM),
    ('LINEBEFORE', (0,0), (0,-1), 3, GOLD),
    ('LEFTPADDING', (0,0), (-1,-1), 14),
    ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
]))
story.append(disclaimer)
story.append(Spacer(1, 18))

# Signature
sig = Table([[
    Paragraph(
        "<b>Documento generato con intelligenza artificiale</b><br/>"
        "Questo piano è stato elaborato con il supporto di modelli di intelligenza "
        "artificiale a partire da riferimenti nutrizionali pubblici e tracciabili: "
        "linee guida LARN/SINU (IV revisione, 2014), riferimenti EFSA e WHO/FAO. "
        "I calcoli di fabbisogno energetico e dei macronutrienti sono deterministici e "
        "basati sull'equazione di Mifflin-St Jeor (1990), ampiamente validata in letteratura. "
        "Il piano non costituisce una diagnosi medica né sostituisce la consulenza "
        "di un medico, di un dietologo o di un biologo nutrizionista.",
        SMALL),
    Paragraph("<b>Hai domande sul tuo piano?</b><br/>"
              "Scrivici a supporto@nutriscienza.org<br/>"
              "Risposta entro 48 ore lavorative", BODY),
]], colWidths=[10.5*cm, 6*cm])
sig.setStyle(TableStyle([
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LINEABOVE', (0,0), (-1,0), 0.5, BORDER),
]))
story.append(sig)

# Build
doc = PianoDoc(OUTPUT)
doc.build(story)

print(f"PDF creato: {OUTPUT}")
