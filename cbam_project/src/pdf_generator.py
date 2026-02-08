"""
PDF Report Generator for CBAM Analysis
Generates professional executive reports with charts and tables
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
import io


class CBAMPDFGenerator:
    """Professional PDF report generator for CBAM analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#334155'),
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Highlight box style
        self.styles.add(ParagraphStyle(
            name='HighlightBox',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=15,
            spaceBefore=15,
            leftIndent=20,
            rightIndent=20,
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(self, cbam_summary, ets_forecast, report_text, 
                       emission_analysis=None, optimization_scenarios=None):
        """
        Generate a professional PDF report
        
        Args:
            cbam_summary: Dictionary with CBAM calculation summary
            ets_forecast: DataFrame with ETS price forecasts
            report_text: Generated report text from Gemini
            emission_analysis: Optional emission analysis data
            optimization_scenarios: Optional optimization scenarios
        
        Returns:
            BytesIO object containing the PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            topMargin=2*cm,
            bottomMargin=2*cm,
            leftMargin=2.5*cm,
            rightMargin=2.5*cm
        )
        
        story = []
        
        # Header
        story.append(Paragraph("⚡ GreFins", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.3*cm))
        
        # Title
        story.append(Paragraph("CBAM Executive Analysis Report", self.styles['CustomTitle']))
        story.append(Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y')}",
            self.styles['CustomSubtitle']
        ))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#3b82f6')))
        story.append(Spacer(1, 0.5*cm))
        
        # Executive Summary Box
        story.append(Paragraph("📊 Executive Summary", self.styles['SectionHeader']))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Product', cbam_summary.get('product', 'N/A')],
            ['Quantity', f"{cbam_summary.get('quantity_tonnes', 0):,.0f} tonnes"],
            ['Total Emission', f"{cbam_summary.get('total_emission', 0):,.2f} tCO2e"],
            ['CBAM Cost', f"€{cbam_summary.get('cbam_cost', 0):,.2f}"],
            ['Emission Intensity', f"{cbam_summary.get('total_ei', 0)} tCO2/tonne"],
        ]
        
        summary_table = Table(summary_data, colWidths=[8*cm, 7*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f1f5f9')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.5*cm))
        
        # ETS Forecast Table
        if ets_forecast is not None and not ets_forecast.empty:
            story.append(Paragraph("📈 ETS Price Forecast (6-Year Projection)", self.styles['SectionHeader']))
            
            forecast_data = [['Period', 'ETS Price (€/tCO2)', 'CBAM Cost (€)']]
            for _, row in ets_forecast.head(8).iterrows():
                forecast_data.append([
                    row['period'],
                    f"€{row['ets_price']:,.2f}",
                    f"€{row['projected_cbam_cost']:,.2f}"
                ])
            
            forecast_table = Table(forecast_data, colWidths=[5*cm, 5*cm, 5*cm])
            forecast_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#06b6d4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ]))
            story.append(forecast_table)
            story.append(Spacer(1, 0.5*cm))
        
        # Emission Analysis
        if emission_analysis:
            story.append(Paragraph("🔬 Emission Analysis", self.styles['SectionHeader']))
            
            if emission_analysis.get('scope1'):
                scope1 = emission_analysis['scope1']
                story.append(Paragraph(
                    f"<b>Scope 1 (Direct Emissions):</b> {scope1.get('total_scope1', 0):,.2f} tCO2",
                    self.styles['CustomBody']
                ))
            
            if emission_analysis.get('scope2'):
                scope2 = emission_analysis['scope2']
                story.append(Paragraph(
                    f"<b>Scope 2 (Indirect Emissions):</b> {scope2.get('total_scope2', 0):,.2f} tCO2",
                    self.styles['CustomBody']
                ))
            
            story.append(Paragraph(
                f"<b>Total Emissions:</b> {emission_analysis.get('total_emissions', 0):,.2f} tCO2",
                self.styles['HighlightBox']
            ))
            story.append(Spacer(1, 0.3*cm))
        
        # Optimization Scenarios
        if optimization_scenarios and len(optimization_scenarios) > 0:
            story.append(Paragraph("💡 Optimization Scenarios", self.styles['SectionHeader']))
            
            opt_data = [['Scenario', 'Annual Savings', 'Investment', 'ROI (years)']]
            for scenario in optimization_scenarios:
                opt_data.append([
                    scenario.get('name', 'N/A'),
                    f"€{scenario.get('annual_savings', 0):,.0f}",
                    f"€{scenario.get('investment_cost', 0):,.0f}",
                    f"{scenario.get('roi_years', 0):.1f}"
                ])
            
            opt_table = Table(opt_data, colWidths=[6*cm, 3*cm, 3*cm, 3*cm])
            opt_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#22c55e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(opt_table)
            story.append(Spacer(1, 0.5*cm))
        
        # Page break before detailed report
        story.append(PageBreak())
        
        # Detailed AI Report
        story.append(Paragraph("📋 Detailed Analysis Report", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1')))
        story.append(Spacer(1, 0.3*cm))
        
        # Split report text into paragraphs
        if report_text:
            paragraphs = report_text.split('\n')
            for para in paragraphs:
                if para.strip():
                    # Check if it's a header (starts with ##)
                    if para.strip().startswith('##'):
                        header_text = para.strip().replace('##', '').strip()
                        story.append(Paragraph(header_text, self.styles['SectionHeader']))
                    elif para.strip().startswith('#'):
                        header_text = para.strip().replace('#', '').strip()
                        story.append(Paragraph(header_text, self.styles['Heading3']))
                    else:
                        # Regular paragraph
                        story.append(Paragraph(para.strip(), self.styles['CustomBody']))
        
        # Footer
        story.append(Spacer(1, 1*cm))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1')))
        story.append(Paragraph(
            "Generated by GreFins CBAM Calculator | Professional Carbon Compliance Analysis",
            self.styles['CustomSubtitle']
        ))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
