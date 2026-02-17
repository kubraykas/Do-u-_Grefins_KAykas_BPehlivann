"""
High-End Corporate CBAM Report Generator
Premium PDF design with Adobe InDesign-like aesthetics.
"""

import os
import io
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, 
    Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, NextPageTemplate
)

# --- BRANDING & DESIGN SYSTEM ---
COLOR_NAVY = colors.HexColor('#0B1121')
COLOR_NAVY_LIGHT = colors.HexColor('#151E32')
COLOR_NEON = colors.HexColor('#C9FD02')
COLOR_TEXT_MAIN = colors.HexColor('#FFFFFF')
COLOR_TEXT_MUTED = colors.HexColor('#94A3B8')
COLOR_BORDER = colors.HexColor('#2D3748')
COLOR_WHITE = colors.HexColor('#FFFFFF')

LOGO_PATH = "/Users/busrapehlivan/grefinsdogus/Do-u-_Grefins_KAykas_BPehlivann/cbam_project/favicon.png"

# --- FONT REGISTRATION ---
def register_premium_fonts():
    paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf"
    ]
    
    reg_name = "PremiumSans"
    bold_name = "PremiumSans-Bold"
    
    regular_path = next((p for p in paths if os.path.exists(p) and "Bold" not in p), None)
    bold_path = next((p for p in paths if os.path.exists(p) and "Bold" in p), None)
    
    if regular_path:
        pdfmetrics.registerFont(TTFont(reg_name, regular_path))
        if bold_path:
            pdfmetrics.registerFont(TTFont(bold_name, bold_path))
        else:
            pdfmetrics.registerFont(TTFont(bold_name, regular_path))
        return reg_name, bold_name
    else:
        return "Helvetica", "Helvetica-Bold"

FONT_REG, FONT_BOLD = register_premium_fonts()

class CBAMPDFGenerator:
    """Premium McKinsey-Style Corporate Document Generator"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_executive_styles()

    def _setup_executive_styles(self):
        """Setup Professional Typography"""
        # Global Body
        self.styles.add(ParagraphStyle(
            name='ExecBody',
            fontName=FONT_REG,
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        # Dark Background Body (for card-like sections)
        self.styles.add(ParagraphStyle(
            name='ExecBodyDark',
            fontName=FONT_REG,
            fontSize=10,
            textColor=COLOR_TEXT_MAIN,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=8
        ))
        
        # Cover Titles
        self.styles.add(ParagraphStyle(
            name='CoverMainTitle',
            fontName=FONT_BOLD,
            fontSize=42,
            textColor=COLOR_WHITE,
            leading=48,
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='CoverSubTitle',
            fontName=FONT_REG,
            fontSize=18,
            textColor=COLOR_NEON,
            leading=22,
            alignment=TA_LEFT,
            spaceBefore=10
        ))
        
        # Section Headings
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            fontName=FONT_BOLD,
            fontSize=18,
            textColor=COLOR_NAVY,
            spaceBefore=25,
            spaceAfter=15,
            leading=22,
            borderPadding=(0, 0, 5, 0),
            borderWidth=0,
            alignment=TA_LEFT
        ))

        # Subsection Headings
        self.styles.add(ParagraphStyle(
            name='SubSectionHeading',
            fontName=FONT_BOLD,
            fontSize=12,
            textColor=colors.HexColor('#1F2937'),
            spaceBefore=15,
            spaceAfter=10,
            leading=14,
            alignment=TA_LEFT
        ))

    def _draw_cover_background(self, canvas, doc):
        """Elegant Corporate Cover"""
        canvas.saveState()
        # Main Navy background
        canvas.setFillColor(COLOR_NAVY)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        
        # Aesthetic background elements (Diagonal line)
        canvas.setStrokeColor(colors.HexColor('#151E32'))
        canvas.setLineWidth(150)
        canvas.line(-100, 200, 700, 900)
        
        # Strategic Neon Accent
        canvas.setStrokeColor(COLOR_NEON)
        canvas.setLineWidth(3)
        canvas.line(1.5*cm, 18*cm, 5*cm, 18*cm)
        
        # Logo on cover
        if os.path.exists(LOGO_PATH):
            canvas.drawImage(LOGO_PATH, 1.5*cm, 24*cm, width=4*cm, height=2.5*cm, mask='auto', preserveAspectRatio=True)
        
        canvas.restoreState()

    def _draw_standard_page(self, canvas, doc):
        """Standard White Interior Pages for Readability"""
        canvas.saveState()
        
        # Ensure background is white
        canvas.setFillColor(colors.white)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        
        # Vertical accent strip on the left (Navy)
        canvas.setFillColor(COLOR_NAVY)
        canvas.rect(0, 0, 0.4*cm, A4[1], fill=1, stroke=0)
        
        # Header text (Subtle Gray)
        canvas.setFont(FONT_BOLD, 8)
        canvas.setFillColor(colors.HexColor('#6B7280'))
        canvas.drawString(1.5*cm, doc.pagesize[1] - 1.2*cm, "Grefins Intelligence Systems | Board Member Report")
        
        # Footer
        canvas.setFont(FONT_REG, 8)
        canvas.setFillColor(colors.HexColor('#9CA3AF'))
        canvas.drawString(1.5*cm, 1*cm, f"Confidential | {datetime.now().year}")
        canvas.drawRightString(doc.pagesize[0] - 1.5*cm, 1*cm, f"Sayfa {doc.page}")
        
        canvas.restoreState()

    def draw_premium_charts(self, cbam_summary, ets_forecast, emission_analysis=None):
        """Generate Professional Visuals for Light Background"""
        charts = []
        
        # Chart 1: Carbon Mix
        if emission_analysis:
            plt.figure(figsize=(6, 4), dpi=300)
            s1 = float(emission_analysis.get('scope1', {}).get('total_scope1', 0))
            s2 = float(emission_analysis.get('scope2', {}).get('total_scope2', 0))
            
            if s1 > 0 or s2 > 0:
                wedges, texts, autotexts = plt.pie(
                    [s1, s2], labels=['Scope 1', 'Scope 2'], autopct='%1.1f%%',
                    colors=['#C9FD02', '#0B1121'], startangle=90,
                    wedgeprops={'width': 0.5, 'edgecolor': 'white'}
                )
                plt.setp(autotexts, size=8, weight="bold", color="white")
                plt.setp(texts, size=9, weight="bold", color="#1F2937") # Dark labels for light BG
                plt.title("Emisyon Dağılım Profili", fontsize=12, fontweight='bold', pad=20, color="#0B1121")
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
                buf.seek(0)
                charts.append(buf)
                plt.close()

        # Chart 2: Cost Trend
        if ets_forecast is not None and not ets_forecast.empty:
            plt.figure(figsize=(8, 4), dpi=300)
            df = ets_forecast.head(12)
            plt.plot(df['Quarter'], df['Forecasted Value'], color='#0B1121', linewidth=3, marker='o', markerfacecolor='#C9FD02', markersize=8)
            plt.fill_between(df['Quarter'], df['Forecasted Value'], color='#C9FD02', alpha=0.1)
            plt.title("CBAM Sertifika Fiyat Projeksiyonu (€)", fontsize=12, fontweight='bold', pad=15, color="#0B1121")
            plt.grid(axis='y', linestyle='--', alpha=0.2, color="#0B1121")
            plt.xticks(rotation=45, color="#4B5563")
            plt.yticks(color="#4B5563")
            plt.tight_layout()
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
            buf.seek(0)
            charts.append(buf)
            plt.close()
            
        return charts

    def generate_report(self, cbam_summary, ets_forecast, report_text, 
                       emission_analysis=None, optimization_scenarios=None):
        """Orchestrate the high-end document"""
        buffer = io.BytesIO()
        doc = BaseDocTemplate(buffer, pagesize=A4, leftMargin=2*cm, rightMargin=1.5*cm, topMargin=2.5*cm, bottomMargin=2.5*cm)
        
        full_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        
        cover_template = PageTemplate(id='Cover', frames=[full_frame], onPage=self._draw_cover_background)
        inside_template = PageTemplate(id='Inside', frames=[full_frame], onPage=self._draw_standard_page)
        
        doc.addPageTemplates([cover_template, inside_template])
        story = []
        
        # --- COVER PAGE ---
        story.append(Spacer(1, 8*cm))
        story.append(Paragraph("CBAM STRATEJİK MALİYET", self.styles['CoverMainTitle']))
        story.append(Paragraph("VE ANALİZ RAPORU", self.styles['CoverMainTitle']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("GreFins Intelligence Systems | Board Member Report", self.styles['CoverSubTitle']))
        
        story.append(Spacer(1, 4*cm))
        footer_style = ParagraphStyle(name='CoverFoot', fontName=FONT_REG, fontSize=11, textColor=COLOR_WHITE)
        story.append(Paragraph(f"<b>Firma:</b> {cbam_summary.get('company_name', 'Firma')}", footer_style))
        story.append(Paragraph(f"<b>Dönem:</b> {cbam_summary.get('reporting_period', '2024')}", footer_style))
        story.append(Paragraph(f"<b>Lokasyon:</b> {cbam_summary.get('origin_country', 'TR')}", footer_style))
        
        # CRITICAL: Switch template BEFORE the page break to affect page 2
        story.append(NextPageTemplate('Inside'))
        story.append(PageBreak())
        
        # --- EXECUTIVE DATA GRID (Now on White Page 2) ---
        story.append(Paragraph("1. YÖNETİCİ ÖZETİ VE KRİTİK VERİLER", self.styles['SectionHeading']))
        
        # Metrics Table (Professional Layout for WHITE background)
        qty = cbam_summary.get('quantity_tonnes', 0)
        try:
            qty_val = float(qty)
        except:
            qty_val = 0

        metrics_data = [
            [Paragraph("<b>TEMEL METRİKLER</b>", ParagraphStyle(name='TableHeader', fontName=FONT_BOLD, fontSize=11, textColor=COLOR_WHITE)), ""],
            [Paragraph("Üretim Rotası", self.styles['ExecBody']), Paragraph(f"{cbam_summary.get('production_route', 'N/A').upper()}", self.styles['ExecBody'])],
            [Paragraph("Ürün Segmenti", self.styles['ExecBody']), Paragraph(f"{cbam_summary.get('product', 'N/A')}", self.styles['ExecBody'])],
            [Paragraph("Toplam Emisyon", self.styles['ExecBody']), Paragraph(f"{float(cbam_summary.get('total_emission', 0)):,.2f} tCO2e", self.styles['ExecBody'])],
            [Paragraph("CBAM Maruziyeti (Güncel)", self.styles['ExecBody']), Paragraph(f"€{float(cbam_summary.get('cbam_cost', 0)):,.2f}", self.styles['ExecBody'])],
            [Paragraph("İhracat Miktarı", self.styles['ExecBody']), Paragraph(f"{qty_val:,.0f} ton", self.styles['ExecBody'])],
            [Paragraph("Birim Karbon Maliyeti", self.styles['ExecBody']), Paragraph(f"€{float(cbam_summary.get('cbam_cost', 0) / (qty_val if qty_val > 0 else 1)):,.2f} / t", self.styles['ExecBody'])]
        ]
        
        t = Table(metrics_data, colWidths=[7*cm, 10*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (1,0), COLOR_NAVY), # Dark header
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('LINEBELOW', (0,0), (-1,0), 2, COLOR_NEON),
            ('INNERGRID', (0,1), (-1,-1), 0.5, colors.HexColor('#E5E7EB')), # Light gray grid
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')]), # Zebra stripes
            ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t)
        story.append(Spacer(1, 1*cm))
        
        # --- AI CONTENT HANDLING ---
        def clean_md(text):
            if not text: return ""
            text = text.replace('✓', '•') # Standardize bullets
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            return text

        if report_text:
            sections = re.split(r'\n(?=###|\d\.)', report_text)
            for section in sections:
                lines = section.strip().split('\n')
                if not lines: continue
                
                header = lines[0]
                content_lines = lines[1:]
                
                # Main headings (Force Dark Color)
                if any(x in header for x in ['###', '1.', '2.', '3.', '4.', '5.']):
                    clean_h = header.replace('###', '').strip()
                    story.append(Paragraph(clean_md(clean_h), self.styles['SectionHeading']))
                else:
                    content_lines = [header] + content_lines
                
                # Visuals integration logic
                if "EMİSYON ANALİZİ" in header.upper() or "3." in header:
                    charts = self.draw_premium_charts(cbam_summary, ets_forecast, emission_analysis)
                    for c in charts:
                        story.append(KeepTogether([Image(c, width=14*cm, height=7*cm), Spacer(1, 0.5*cm)]))

                # Body text (Ensuring Dark Gray for readability)
                for line in content_lines:
                    line = line.strip()
                    if not line: continue
                    
                    p_style = self.styles['ExecBody']
                    if line.startswith('-') or line.startswith('*') or line.startswith('•'):
                        text = f"• {clean_md(line.replace('-', '').replace('*', '').strip())}"
                    else:
                        text = clean_md(line)
                    
                    story.append(Paragraph(text, p_style))

        # Final Branding
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph("Bu rapor GreFins Intelligence altyapısı tarafından üretilmiştir. Veriler Avrupa Komisyonu ve EU ETS piyasa verileriyle desteklenmektedir.", 
                               ParagraphStyle(name='Legal', fontName=FONT_REG, fontSize=7, textColor=colors.grey, alignment=TA_CENTER)))

        doc.build(story)
        buffer.seek(0)
        return buffer
