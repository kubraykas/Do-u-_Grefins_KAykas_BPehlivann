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
COLOR_NEON = colors.HexColor('#C9FD02')
COLOR_TEAL = colors.HexColor('#1F7A8C')
COLOR_GRAY_SOFT = colors.HexColor('#F3F4F6')
COLOR_TEXT = colors.HexColor('#333333')
COLOR_WHITE = colors.HexColor('#FFFFFF')

LOGO_PATH = "/Users/busrapehlivan/grefinsdogus/Do-u-_Grefins_KAykas_BPehlivann/cbam_project/favicon.png"

# --- FONT REGISTRATION (Robust for MacOS/Turkish) ---
def register_premium_fonts():
    paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf"
    ]
    
    reg_name = "PremiumSans"
    bold_name = "PremiumSans-Bold"
    
    # Try to find valid paths
    regular_path = next((p for p in paths if os.path.exists(p) and "Bold" not in p), None)
    bold_path = next((p for p in paths if os.path.exists(p) and "Bold" in p), None)
    
    if regular_path:
        pdfmetrics.registerFont(TTFont(reg_name, regular_path))
        if bold_path:
            pdfmetrics.registerFont(TTFont(bold_name, bold_path))
        else:
            pdfmetrics.registerFont(TTFont(bold_name, regular_path)) # Fallback to reg
        return reg_name, bold_name
    else:
        # Emergency Fallback
        return "Helvetica", "Helvetica-Bold"

FONT_REG, FONT_BOLD = register_premium_fonts()

class CBAMPDFGenerator:
    """Premium Corporate Document Generator"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_executive_styles()

    def _setup_executive_styles(self):
        """Setup InDesign-like typography"""
        # Global Body
        self.styles.add(ParagraphStyle(
            name='IndyBody',
            fontName=FONT_REG,
            fontSize=10,
            textColor=COLOR_TEXT,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Cover Large Title
        self.styles.add(ParagraphStyle(
            name='CoverTitle',
            fontName=FONT_BOLD,
            fontSize=38,
            textColor=COLOR_WHITE,
            leading=44,
            alignment=TA_LEFT,
            leftIndent=0
        ))
        
        # Section Heading
        self.styles.add(ParagraphStyle(
            name='IndyHeading',
            fontName=FONT_BOLD,
            fontSize=16,
            textColor=COLOR_NAVY,
            spaceBefore=20,
            spaceAfter=12,
            leading=20
        ))
        
        # Summary Box Paragraph
        self.styles.add(ParagraphStyle(
            name='SummaryBoxText',
            fontName=FONT_REG,
            fontSize=11,
            textColor=COLOR_TEXT,
            leading=16,
            alignment=TA_JUSTIFY,
            leftIndent=10
        ))

    def _draw_cover_background(self, canvas, doc):
        """Full Navy Background for Cover"""
        canvas.saveState()
        canvas.setFillColor(COLOR_NAVY)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        
        # Add a subtle neon lime accent line on cover
        canvas.setStrokeColor(COLOR_NEON)
        canvas.setLineWidth(2)
        canvas.line(1.5*cm, 15*cm, 8*cm, 15*cm)
        
        # Logo on cover (Significantly larger)
        if os.path.exists(LOGO_PATH):
            canvas.drawImage(LOGO_PATH, 1.5*cm, 24*cm, width=5*cm, height=5*cm, mask='auto', preserveAspectRatio=True)
        
        canvas.restoreState()

    def _draw_header_footer(self, canvas, doc):
        """Navy Header and Subtle Footer for Inside Pages"""
        canvas.saveState()
        
        # Header Strip
        canvas.setFillColor(COLOR_NAVY)
        canvas.rect(0, doc.pagesize[1] - 1.5*cm, doc.pagesize[0], 1.5*cm, fill=1, stroke=0)
        
        # Header Text
        canvas.setFont(FONT_BOLD, 9)
        canvas.setFillColor(COLOR_WHITE)
        canvas.drawString(1.5*cm, doc.pagesize[1] - 0.9*cm, "Grefins Intelligence | CBAM Report")
        
        # Logo in Header (Larger)
        if os.path.exists(LOGO_PATH):
            canvas.drawImage(LOGO_PATH, doc.pagesize[0] - 5*cm, doc.pagesize[1] - 1.4*cm, width=3.5*cm, height=2.1*cm, mask='auto', preserveAspectRatio=True)
            
        # Footer
        canvas.setFont(FONT_REG, 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(1.5*cm, 1*cm, "Confidential | GreFins Strategic Analysis")
        canvas.drawRightString(doc.pagesize[0] - 1.5*cm, 1*cm, f"Page {doc.page}")
        
        # Line separating footer
        canvas.setStrokeColor(colors.lightgrey)
        canvas.setLineWidth(0.5)
        canvas.line(1.5*cm, 1.3*cm, doc.pagesize[0] - 1.5*cm, 1.3*cm)
        
        canvas.restoreState()

    def draw_premium_charts(self, cbam_summary, ets_forecast, emission_analysis=None):
        """Generate high-DPI Donut and Bar charts"""
        charts = []
        
        # 1. Donut Chart for Emissions
        if emission_analysis:
            labels = []
            values = []
            if emission_analysis.get('scope1', {}).get('total_scope1', 0) > 0:
                labels.append('Scope 1')
                values.append(emission_analysis['scope1']['total_scope1'])
            if emission_analysis.get('scope2', {}).get('total_scope2', 0) > 0:
                labels.append('Scope 2')
                values.append(emission_analysis['scope2']['total_scope2'])
            
            if values:
                plt.figure(figsize=(6, 5), dpi=300)
                plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, 
                        colors=['#C9FD02', '#0B1121'], # Neon Lime and Deep Navy
                        wedgeprops={'width': 0.4, 'edgecolor': 'white'}) # Donut hole
                plt.title("Carbon Footprint (Scope 1 vs 2)", fontsize=14, fontweight='bold', color='#0B1121', pad=20)
                plt.axis('equal')
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png', transparent=True)
                buf.seek(0)
                charts.append(buf)
                plt.close()

        # 2. Premium Bar Chart
        if ets_forecast is not None and not ets_forecast.empty:
            plt.figure(figsize=(10, 5), dpi=300)
            df = ets_forecast.head(10).copy()
            cols = df.columns.tolist()
            q_col = 'Quarter' if 'Quarter' in cols else cols[0]
            p_col = next((c for c in cols if 'forecast' in c.lower() or 'price' in c.lower()), cols[1])
            
            bars = plt.bar(df[q_col], df[p_col], color=COLOR_TEAL.hexval()[2:], alpha=0.9, width=0.6)
            plt.title("Carbon Price Projections (€/tCO2)", fontsize=14, fontweight='bold', color='#0B1121', pad=15)
            
            # Remove spines
            ax = plt.gca()
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.yaxis.set_ticks_position('none')
            
            # Light grid
            plt.grid(axis='y', linestyle='--', alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png', transparent=True)
            buf.seek(0)
            charts.append(buf)
            plt.close()
            
        return charts

    def generate_report(self, cbam_summary, ets_forecast, report_text, 
                       emission_analysis=None, optimization_scenarios=None):
        """Main flow using BaseDocTemplate for PageTemplates"""
        buffer = io.BytesIO()
        doc = BaseDocTemplate(buffer, pagesize=A4, leftMargin=1.5*cm, rightMargin=1.5*cm, topMargin=2.5*cm, bottomMargin=2.5*cm)
        
        # Frames
        full_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        
        # Templates
        cover_template = PageTemplate(id='Cover', frames=[full_frame], onPage=self._draw_cover_background)
        inside_template = PageTemplate(id='Inside', frames=[full_frame], onPage=self._draw_header_footer)
        
        doc.addPageTemplates([cover_template, inside_template])
        
        story = []
        
        # --- COVER CONTENT ---
        story.append(Spacer(1, 6*cm))
        story.append(Paragraph("CBAM STRATEJİK<br/>UYUM RAPORU", self.styles['CoverTitle']))
        story.append(Spacer(1, 1*cm))
        
        info_style = ParagraphStyle(name='Info', fontName=FONT_REG, fontSize=12, textColor=COLOR_WHITE)
        story.append(Paragraph(f"Tarih: {datetime.now().strftime('%d %B %Y')}", info_style))
        story.append(Paragraph(f"Rapor ID: GREF-CBAM-{datetime.now().strftime('%Y%j')}", info_style))
        story.append(Paragraph(f"Müşteri: {cbam_summary.get('company_name', 'Executive Leadership')}", info_style))
        
        story.append(PageBreak())
        
        # Switch to Inside Template
        story.append(NextPageTemplate('Inside'))
        
        # --- EXECUTIVE SUMMARY BOX ---
        story.append(Paragraph("1. Yönetici Özeti", self.styles['IndyHeading']))
        
        summary_text = f"""
        Bu stratejik rapor, <b>{cbam_summary.get('company_name', 'Firma')}</b> operasyonlarının AB Sınırda Karbon Düzenleme Mekanizması (CBAM) altındaki finansal ve uyum risklerini analiz etmektedir. 
        Tespit edilen <b>{cbam_summary.get('total_emission', 0):,.2f} tCO2e</b> toplam emisyon hacmi, şirket EBITDA'sı üzerinde kritik bir maliyet baskısı yaratma potansiyeline sahiptir. 
        Aşağıdaki analiz, optimizasyon senaryoları ve stratejik yol haritasını içermektedir.
        """
        
        summary_box_data = [[Paragraph(summary_text, self.styles['SummaryBoxText'])]]
        summary_box = Table(summary_box_data, colWidths=[17*cm])
        summary_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_GRAY_SOFT),
            ('INNERGRID', (0,0), (-1,-1), 0, colors.white),
            ('LINESTART', (0,0), (0,0), 3, COLOR_NEON), # Thick neon lime left border
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('TOPPADDING', (0,0), (-1,-1), 15),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(summary_box)
        story.append(Spacer(1, 1*cm))
        
        # --- CORE METRICS TABLE ---
        story.append(Paragraph("2. Kritik Operasyonel Veriler", self.styles['IndyHeading']))
        
        table_data = [
            [Paragraph("<b>Metrik Kategorisi</b>", ParagraphStyle(name='TH', fontName=FONT_BOLD, textColor=COLOR_WHITE)), 
             Paragraph("<b>Analiz Sonucu</b>", ParagraphStyle(name='TH', fontName=FONT_BOLD, textColor=COLOR_WHITE))],
            ["Ürün Segmenti", cbam_summary.get('product', 'N/A')],
            ["İthalat Hacmi (Metrik Ton)", f"{cbam_summary.get('quantity_tonnes', 0):,.0f} t"],
            ["Gömülü Emisyon Yoğunluğu", f"{cbam_summary.get('total_ei', 0)} tCO2/t"],
            ["Toplam Emisyon Hacmi", f"{cbam_summary.get('total_emission', 0):,.2f} tCO2e"],
            ["Mevcut CBAM Maliyet Riski", f"€{cbam_summary.get('cbam_cost', 0):,.2f}"],
        ]
        
        res_table = Table(table_data, colWidths=[8.5*cm, 8.5*cm])
        res_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_TEAL),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.white),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_GRAY_SOFT]),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('FONTNAME', (0,0), (-1,-1), FONT_REG),
        ]))
        story.append(res_table)
        story.append(Spacer(1, 1*cm))
        
        # --- VISUAL DATA ---
        story.append(Paragraph("3. Emisyon Kaynakları ve Fiyat Projeksiyonları", self.styles['IndyHeading']))
        charts = self.draw_premium_charts(cbam_summary, ets_forecast, emission_analysis)
        for c in charts:
            story.append(Image(c, width=15*cm, height=7.5*cm))
            story.append(Spacer(1, 0.5*cm))
            
        story.append(PageBreak())
        
        # --- STRATEGIC AI INSIGHTS ---
        story.append(Paragraph("4. Stratejik Değerlendirme ve Yol Haritası", self.styles['IndyHeading']))
        
        # Clean AI text
        def clean_md(text):
            if not text: return ""
            # Stop AI filler sentences
            text = text.replace("The following table provides...", "")
            text = text.replace("Based on the data provided...", "")
            import re
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            return text

        if report_text:
            lines = report_text.split('\n')
            for line in lines:
                line = line.strip()
                if not line: continue
                
                if line.startswith('###'):
                    story.append(Paragraph(clean_md(line.replace('###', '').strip()), self.styles['IndyHeading']))
                elif line.startswith('##') or line.startswith('#'):
                    story.append(Paragraph(clean_md(line.replace('#', '').strip()), self.styles['IndyHeading']))
                elif line.startswith('-') or line.startswith('*'):
                    story.append(Paragraph(f"• {clean_md(line[1:].strip())}", self.styles['IndyBody']))
                else:
                    story.append(Paragraph(clean_md(line), self.styles['IndyBody']))
        
        # Build Document
        doc.build(story)
        buffer.seek(0)
        return buffer
