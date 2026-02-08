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
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import pandas as pd


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
        self.styles.add(ParagraphStyle(
            name='Heading3',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=10,
            spaceBefore=15,
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
        story.append(Paragraph(" GreFins", self.styles['CustomSubtitle']))
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
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
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
        
        # --- CHARTS SECTION ---
        story.append(Paragraph("Visual Analysis", self.styles['SectionHeader']))
        
        # 1. Cost Projection Chart
        if ets_forecast is not None and not ets_forecast.empty:
            cost_chart_img = self._create_cost_chart(ets_forecast)
            if cost_chart_img:
                story.append(Image(cost_chart_img, width=16*cm, height=8*cm))
                story.append(Spacer(1, 0.5*cm))
        
        # 2. Emission Breakdown Chart (if data exists)
        if emission_analysis:
            emission_chart_img = self._create_emission_pie_chart(emission_analysis)
            if emission_chart_img:
                story.append(Image(emission_chart_img, width=16*cm, height=8*cm))
                story.append(Spacer(1, 0.5*cm))

        # ETS Forecast Table
        if ets_forecast is not None and not ets_forecast.empty:
            story.append(Paragraph(" ETS Price Forecast (6-Year Projection)", self.styles['SectionHeader']))
            
            forecast_data = [['Period', 'ETS Price (€/tCO2)', 'CBAM Cost (€)']]
            # Try to determine column names dynamically to be robust
            cols = ets_forecast.columns.tolist()
            period_col = 'Quarter' if 'Quarter' in cols else ('period' if 'period' in cols else cols[0])
            price_col = 'ETS_Price' if 'ETS_Price' in cols else ('ets_price' if 'ets_price' in cols else (cols[1] if len(cols) > 1 else cols[0]))
            cost_col = 'CBAM_Cost' if 'CBAM_Cost' in cols else ('projected_cbam_cost' if 'projected_cbam_cost' in cols else (cols[2] if len(cols) > 2 else price_col))

            for _, row in ets_forecast.head(8).iterrows():
                try:
                    p_val = row[period_col] if period_col in row else "N/A"
                    pr_val = row[price_col] if price_col in row else 0
                    c_val = row[cost_col] if cost_col in row else 0
                    
                    forecast_data.append([
                        p_val,
                        f"€{pr_val:,.2f}" if isinstance(pr_val, (int, float)) else str(pr_val),
                        f"€{c_val:,.2f}" if isinstance(c_val, (int, float)) else str(c_val)
                    ])
                except Exception as e:
                    print(f"Row parsing error: {e}")
                    continue
            
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
            story.append(Paragraph(" Emission Analysis", self.styles['SectionHeader']))
            
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
            story.append(Paragraph(" Optimization Scenarios", self.styles['SectionHeader']))
            
            opt_data = [['Scenario', 'Annual Savings', 'Investment', 'ROI (years)']]
            # Handle both list and dict formats for optimization scenarios
            scenarios_list = []
            if isinstance(optimization_scenarios, dict):
                scenarios_list = list(optimization_scenarios.values())
            elif isinstance(optimization_scenarios, list):
                scenarios_list = optimization_scenarios

            for scenario in scenarios_list:
                if not isinstance(scenario, dict): continue
                
                annual_savings = scenario.get('annual_cbam_saving_eur') or scenario.get('annual_savings') or 0
                investment = scenario.get('investment_needed_eur') or scenario.get('investment_cost') or 0
                roi = scenario.get('roi_years') or 0
                
                opt_data.append([
                    scenario.get('name', 'N/A'),
                    f"€{annual_savings:,.0f}",
                    f"€{investment:,.0f}",
                    f"{roi:.1f}"
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
        story.append(Paragraph(" Detailed Analysis Report", self.styles['SectionHeader']))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1')))
        story.append(Spacer(1, 0.3*cm))
        
        # Helper to clean markdown and convert to ReportLab tags
        def md_to_rl(text):
            import re
            # Convert **bold** to <b>bold</b>
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
            # Convert *italic* to <i>italic</i>
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
            return text

        # Split report text into paragraphs
        if report_text:
            paragraphs = report_text.split('\n')
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                
                # Check for headers
                if para.startswith('###'):
                    header_text = md_to_rl(para.replace('###', '').strip())
                    story.append(Paragraph(header_text, self.styles['Heading3']))
                elif para.startswith('##'):
                    header_text = md_to_rl(para.replace('##', '').strip())
                    story.append(Paragraph(header_text, self.styles['SectionHeader']))
                elif para.startswith('#'):
                    header_text = md_to_rl(para.replace('#', '').strip())
                    story.append(Paragraph(header_text, self.styles['CustomTitle']))
                elif para.startswith('-') or para.startswith('*'):
                    # Handle bullet points
                    bullet_text = md_to_rl(para[1:].strip())
                    story.append(Paragraph(f"• {bullet_text}", self.styles['CustomBody']))
                else:
                    # Regular paragraph
                    story.append(Paragraph(md_to_rl(para), self.styles['CustomBody']))
        
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

    def _create_cost_chart(self, df):
        """Create a professional CBAM cost projection chart"""
        try:
            # Set style for dark/professional theme
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(10, 5), dpi=120)
            fig.patch.set_facecolor('#0B1121')
            ax.set_facecolor('#0B1121')
            
            # Colors
            primary_color = '#C9FD02'
            
            # Determine column names
            cols = df.columns.tolist()
            period_col = 'Quarter' if 'Quarter' in cols else ('period' if 'period' in cols else cols[0])
            cost_col = 'CBAM_Cost' if 'CBAM_Cost' in cols else ('projected_cbam_cost' if 'projected_cbam_cost' in cols else (cols[2] if len(cols) > 2 else cols[0]))
            
            # Get data for first 8 periods (2 years)
            plot_df = df.head(8).copy()
            
            # Plot
            bars = ax.bar(plot_df[period_col], plot_df[cost_col], color=primary_color, alpha=0.3, label='Maliyet (Bar)')
            ax.plot(plot_df[period_col], plot_df[cost_col], color=primary_color, marker='o', linewidth=3, markersize=8, label='Trend')
            
            # Styling
            ax.set_title('CBAM Maliyet Projeksiyonu (8 Çeyrek)', fontsize=16, fontweight='bold', color='white', pad=20)
            ax.set_xlabel('Dönem', fontsize=10, color='#94A3B8')
            ax.set_ylabel('Tahmini Maliyet (€)', fontsize=10, color='#94A3B8')
            plt.xticks(rotation=45, color='#94A3B8')
            plt.yticks(color='#94A3B8')
            
            # Hide spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#2D3748')
            ax.spines['bottom'].set_color('#2D3748')
            
            ax.grid(axis='y', linestyle='--', alpha=0.1)
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
            img_buffer.seek(0)
            plt.close()
            return img_buffer
        except Exception as e:
            print(f"Error creating cost chart: {e}")
            return None

    def _create_emission_pie_chart(self, emission_analysis):
        """Create a professional emission breakdown pie chart"""
        try:
            labels = []
            sizes = []
            # Concept colors
            colors_list = ['#C9FD02', '#10B981', '#3B82F6', '#6366F1']
            
            if emission_analysis.get('scope1') and emission_analysis['scope1'].get('total_scope1', 0) > 0:
                labels.append('Scope 1')
                sizes.append(emission_analysis['scope1']['total_scope1'])
                
            if emission_analysis.get('scope2') and emission_analysis['scope2'].get('total_scope2', 0) > 0:
                labels.append('Scope 2')
                sizes.append(emission_analysis['scope2']['total_scope2'])
            
            if not sizes:
                return None
                
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
            fig.patch.set_facecolor('#0B1121')
            
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, autopct='%1.1f%%', startangle=140, 
                colors=colors_list[:len(sizes)], 
                wedgeprops={'edgecolor': '#151E32', 'linewidth': 2, 'antialiased': True},
                textprops={'color': 'white', 'fontweight': 'bold'}
            )
            
            ax.set_title('Karbon Emisyon Profili (Scope 1 & 2)', fontsize=16, fontweight='bold', color='white', pad=20)
            plt.axis('equal')
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
            img_buffer.seek(0)
            plt.close()
            return img_buffer
        except Exception as e:
            print(f"Error creating emission chart: {e}")
            return None
