"""Render the editable business report as a paginated PDF. Requires reportlab."""
from pathlib import Path
from xml.sax.saxutils import escape
import json
import re
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image

ROOT = Path(__file__).resolve().parents[1]
NAVY = colors.HexColor('#123348')
TEAL = colors.HexColor('#087F8C')
GRAY = colors.HexColor('#53636E')


def inline(text):
    text = escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" color="#087F8C">\1</a>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    text = re.sub(r'`([^`]+)`', r'<font color="#365769">\1</font>', text)
    return text


def main():
    source = (ROOT / 'reports/business_insights.md').read_text(encoding='utf-8')
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ReportBody', fontName='Helvetica', fontSize=10, leading=14.4, textColor=NAVY, spaceAfter=9))
    styles.add(ParagraphStyle(name='ReportTitle', fontName='Helvetica-Bold', fontSize=31, leading=35, textColor=NAVY, spaceAfter=16))
    styles.add(ParagraphStyle(name='ReportSection', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=TEAL, spaceAfter=13, keepWithNext=True))
    styles.add(ParagraphStyle(name='ReportSmall', fontName='Helvetica', fontSize=8, leading=11, textColor=GRAY, spaceAfter=6))
    story = []
    width = A4[0] - 96
    lines = source.splitlines()
    break_sections = ('## 1.', '## 3.', '## 4.', '## 6.', '## Scope,')
    i = 0
    cover_chart_added = False
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith(break_sections):
            if line.startswith('## 1.') and not cover_chart_added:
                pic = Image(str(ROOT / 'images/monthly_revenue.png'))
                pic.drawHeight *= width / pic.drawWidth
                pic.drawWidth = width
                story.extend([Spacer(1, 10), pic, Paragraph('Monthly Gross Sales; December 2011 is partial.', styles['ReportSmall'])])
                cover_chart_added = True
            story.append(PageBreak())
        if line.startswith('# '):
            story.append(Paragraph(inline(line[2:]), styles['ReportTitle']))
        elif line.startswith('## '):
            story.append(Paragraph(inline(line[3:]), styles['ReportSection']))
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                parts = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+', x) for x in parts):
                    rows.append([Paragraph(inline(x), styles['ReportSmall']) for x in parts])
                i += 1
            table = Table(rows, colWidths=[38, 180, 122, width-340], repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E5F2F3')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),0.4,colors.HexColor('#D6E1E6'))]))
            story.extend([table, Spacer(1, 10)])
            continue
        else:
            style = styles['ReportSmall'] if line.startswith('**Evidence:') or line.startswith('Source:') else styles['ReportBody']
            story.append(Paragraph(inline(line), style))
        i += 1
    evidence = json.loads((ROOT / 'reports/evidence.json').read_text(encoding='utf-8'))
    story.extend([Spacer(1, 12), Paragraph('Reproducible calculation checks', styles['ReportSection'])])
    for check in evidence['checks_passed']:
        story.append(Paragraph('- ' + inline(check), styles['ReportSmall']))
    story.append(Paragraph('Source hashes and detailed invoice evidence are supplied with the repository in reports/evidence.json.', styles['ReportSmall']))

    def page_frame(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(2)
        canvas.line(48, A4[1]-31, A4[0]-48, A4[1]-31)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(GRAY)
        canvas.drawString(48, 27, 'E-commerce Sales Analysis | Historical data: Dec 2010 - Dec 2011 | GBP')
        canvas.drawRightString(A4[0]-48, 27, str(doc.page))
        canvas.restoreState()

    out = ROOT / 'reports/business_insights.pdf'
    doc = SimpleDocTemplate(str(out), pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48,
                            title='E-commerce Sales Analysis - Business Insights & Recommendations', author='E-commerce Sales Analysis')
    doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
    print(out)


if __name__ == '__main__':
    main()
