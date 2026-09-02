# -*- coding: utf-8 -*-
"""ინვოისი № 001 — PDF გენერატორი (ინდ. მეწარმე ნინო ჩაგუნავა → შპს „მერცხალი")."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("Geo", FONT))
pdfmetrics.registerFont(TTFont("Geo-Bold", FONT_BOLD))

ACCENT = colors.HexColor("#1a3a5c")
LIGHT = colors.HexColor("#eef2f6")
GRID = colors.HexColor("#b9c4ce")

base = ParagraphStyle("base", fontName="Geo", fontSize=9.5, leading=14,
                      textColor=colors.HexColor("#222222"))
bold = ParagraphStyle("bold", parent=base, fontName="Geo-Bold")
title = ParagraphStyle("title", parent=bold, fontSize=17, leading=22,
                       textColor=ACCENT)
section = ParagraphStyle("section", parent=bold, fontSize=10.5, leading=15,
                         textColor=ACCENT, spaceBefore=10, spaceAfter=3)
small = ParagraphStyle("small", parent=base, fontSize=8.5, leading=12,
                       textColor=colors.HexColor("#555555"))

doc = SimpleDocTemplate(
    "invoice_001.pdf", pagesize=A4,
    leftMargin=20 * mm, rightMargin=20 * mm,
    topMargin=18 * mm, bottomMargin=18 * mm,
    title="ინვოისი № 001 — ნინო ჩაგუნავა",
    author="ინდივიდუალური მეწარმე ნინო ჩაგუნავა",
)

story = []

# ---- სათაური ----
story.append(Paragraph("ინვოისი № 001", title))
story.append(Paragraph("გაცემის თარიღი: 2026 წლის 1 სექტემბერი, ქ. თბილისი", base))
story.append(Spacer(1, 4))
story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT))
story.append(Spacer(1, 6))

# ---- მხარეები ----
provider = [
    Paragraph("მომსახურების გამწევი", bold),
    Paragraph("ინდივიდუალური მეწარმე ნინო ჩაგუნავა", base),
    Paragraph("საიდენტიფიკაციო / პირადი ნომერი: 01001089783", base),
    Paragraph("იურიდიული მისამართი: ვარდევანის 14", base),
    Paragraph("ტელეფონი: 555 78 93 06", base),
    Paragraph("ელ. ფოსტა: ______________", base),
]
client = [
    Paragraph("დამკვეთი", bold),
    Paragraph("შპს „მერცხალი“", base),
    Paragraph("საიდენტიფიკაციო კოდი: 202050984", base),
    Paragraph("იურიდიული მისამართი: ______________________________", base),
]
parties = Table([[provider, client]], colWidths=[85 * mm, 85 * mm])
parties.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
    ("BOX", (0, 0), (0, 0), 0.5, GRID),
    ("BOX", (1, 0), (1, 0), 0.5, GRID),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(parties)

# ---- გაწეული მომსახურება ----
story.append(Paragraph("გაწეული მომსახურება", section))

hdr = ParagraphStyle("hdr", parent=bold, fontSize=9, textColor=colors.white)
cell = ParagraphStyle("cell", parent=base, fontSize=9)
amount_style = ParagraphStyle("amt", parent=bold, fontSize=11, alignment=2)

svc_data = [
    [Paragraph("№", hdr),
     Paragraph("მომსახურების აღწერა", hdr),
     Paragraph("რაოდ.", hdr),
     Paragraph("თანხა (GEL)", hdr)],
    [Paragraph("1", cell), Paragraph("", cell), Paragraph("", cell),
     Paragraph("", cell)],
    [Paragraph("ჩასარიცხი თანხა (GEL)", bold), "",
     Paragraph("4 876.54", amount_style), ""],
]
svc = Table(svc_data, colWidths=[12 * mm, 103 * mm, 20 * mm, 35 * mm])
svc.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, 1), 0.5, GRID),
    ("SPAN", (0, 2), (1, 2)),
    ("SPAN", (2, 2), (3, 2)),
    ("ALIGN", (0, 2), (1, 2), "LEFT"),
    ("BACKGROUND", (0, 2), (-1, 2), LIGHT),
    ("BOX", (0, 2), (-1, 2), 0.5, GRID),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("MINROWHEIGHT", (0, 1), (-1, 1), 14 * mm),
]))
story.append(svc)
story.append(Spacer(1, 4))
story.append(Paragraph(
    "ჩასარიცხი თანხა სიტყვიერად: <b>ოთხი ათას რვაას სამოცდათექვსმეტი ლარი "
    "და 54 თეთრი</b>.", base))

# ---- საბანკო რეკვიზიტები ----
story.append(Paragraph("საბანკო რეკვიზიტები", section))
bank_rows = [
    ["მიმღები:", "ინდივიდუალური მეწარმე ნინო ჩაგუნავა"],
    ["ბანკი:", "საქართველოს ბანკი"],
    ["ანგარიშის ნომერი (IBAN):", "GE75BG0000000526098069"],
    ["ბანკის კოდი (SWIFT):", "BAGAGE22"],
    ["საკონტაქტო ტელეფონი:", "555 78 93 06"],
]
bank = Table(
    [[Paragraph(k, bold), Paragraph(v, base)] for k, v in bank_rows],
    colWidths=[55 * mm, 115 * mm],
)
bank.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
    ("BOX", (0, 0), (-1, -1), 0.5, GRID),
    ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.white),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(bank)

# ---- გადახდის პირობები ----
story.append(Spacer(1, 10))
story.append(Paragraph(
    "<b>გადახდის პირობები:</b> ინვოისი გადასახდელია გაცემიდან 3 (სამი) "
    "სამუშაო დღის ვადაში.", base))
story.append(Paragraph(
    "გადახდისას დანიშნულებაში მიუთითეთ ინვოისის ნომერი და თარიღი.", small))

# ---- ხელმოწერები ----
story.append(Spacer(1, 26))
sig = Table([
    [Paragraph("__________________________", base),
     Paragraph("__________________________", base)],
    [Paragraph("მომსახურების გამწევი — ნინო ჩაგუნავა", small),
     Paragraph("დამკვეთი — შპს „მერცხალი“", small)],
], colWidths=[85 * mm, 85 * mm])
sig.setStyle(TableStyle([
    ("TOPPADDING", (0, 1), (-1, 1), 2),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
]))
story.append(sig)

doc.build(story)
print("invoice_001.pdf created")
