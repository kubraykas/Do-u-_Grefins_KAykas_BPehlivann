"""
Grefins High-End Corporate Report Intelligence
Generates partner-level strategic insights for CBAM.
"""

import pandas as pd
from datetime import datetime

class CBAMReportGenerator:
    """
    World-class strategic reporting for CBAM compliance and financial strategy.
    """
    
    def __init__(self, gemini_client):
        self.client = gemini_client
    
    def add_risk_analysis(self, cbam_df):
        """Quantify financial exposure levels"""
        if cbam_df.empty:
            cbam_df['Risk_Level'] = []
            return cbam_df

        q90 = cbam_df['CBAM_Cost'].quantile(0.9)
        mean_cost = cbam_df['CBAM_Cost'].mean()

        def risk_label(x):
            if x >= q90: return "High Exposure"
            elif x >= mean_cost: return "Moderate Exposure"
            else: return "Managed Risk"

        cbam_df['Risk_Level'] = cbam_df['CBAM_Cost'].apply(risk_label)
        return cbam_df
    
    def calculate_metrics(self, cbam_summary, ets_forecast_table, cbam_df):
        """Extract high-level financial metrics for the executive board"""
        metrics = {
            'product': cbam_summary.get('product', 'Unspecified'),
            'quantity_tonnes': cbam_summary.get('quantity_tonnes', 0),
            'total_ei': cbam_summary.get('total_ei', 0),
            'total_emission': cbam_summary.get('total_emission', 0),
            'current_cbam_cost': cbam_summary.get('cbam_cost', 0),
            'company_name': cbam_summary.get('company_name', 'Executive Leadership'),
            'sector': cbam_summary.get('sector', 'iron_steel'),
            'production_route': cbam_summary.get('production_route', 'eaf'),
            'financials': cbam_summary.get('financials', {}),
            'reporting_period': cbam_summary.get('reporting_period', '2024'),
            'origin_country': cbam_summary.get('origin_country', 'TR'),
            'export_quantity': cbam_summary.get('export_quantity', 0)
        }
        
        if isinstance(ets_forecast_table, pd.DataFrame) and not ets_forecast_table.empty:
            cols = ets_forecast_table.columns.tolist()
            val_col = next((c for c in cols if 'forecast' in c.lower() or 'price' in c.lower() or 'value' in c.lower()), cols[0])
            prices = ets_forecast_table[val_col]
            metrics.update({
                'ets_avg': prices.mean(),
                'ets_max': prices.max(),
                'ets_trend': "Bullish (Yükseliş Trendi)" if (prices.iloc[-1] > prices.iloc[0]) else "Bearish (Düşüş/Yatay Trend)"
            })
            
        if not cbam_df.empty:
            metrics['projected_total_2030'] = cbam_df['CBAM_Cost'].sum()
            metrics['highest_quarter'] = cbam_df.loc[cbam_df['CBAM_Cost'].idxmax(), 'Quarter']
            
        return metrics

    def format_emission_data(self, emission_analysis):
        """Convert raw emission dict into a professional summary string"""
        if not emission_analysis: return "Veri bulunamadı."
        
        lines = []
        scope1 = emission_analysis.get('scope1', {})
        if scope1:
            lines.append("--- SCOPE 1 (Doğrudan Emisyonlar) ---")
            for cat, ems in scope1.items():
                if isinstance(ems, dict):
                    for k, v in ems.items():
                        if v > 0:
                            lines.append(f"- {k.replace('_', ' ').title()}: {v:.2f} tCO2")
                elif isinstance(ems, (int, float)) and cat.startswith('total_'):
                     lines.append(f"**{cat.replace('_', ' ').upper()}**: {ems:.2f} tCO2")

        scope2 = emission_analysis.get('scope2', {})
        if scope2:
            lines.append("\n--- SCOPE 2 (Dolaylı / Elektrik) ---")
            lines.append(f"- Elektrik Tüketimi: {scope2.get('consumption_mwh', 0):,.2f} MWh")
            lines.append(f"- Toplam Scope 2 Emisyonu: {scope2.get('total_scope2', 0):,.2f} tCO2")
            lines.append(f"- Enerji Kaynağı: {scope2.get('description', 'Grid')}")
            
        lines.append(f"\n**TOPLAM EMİSYON**: {emission_analysis.get('total_emissions', 0):,.2f} tCO2")
        return "\n".join(lines)

    def format_optimization_data(self, optimization_scenarios):
        """Format optimization scenarios into the format requested by the user"""
        if not optimization_scenarios: return "Optimizasyon senaryosu hesaplanamadı."
        
        lines = []
        for key, scenario in optimization_scenarios.items():
            if key == 'combined': continue
            
            name = scenario.get('name', 'İyileştirme')
            current = scenario.get('current_consumption', 0)
            target = scenario.get('target_consumption', 0)
            saving = scenario.get('emission_saving_tco2', 0)
            cost_saving = scenario.get('annual_cbam_saving_eur', 0)
            reduction = scenario.get('reduction_percent', 100)
            
            unit = "Nm³" if "natural_gas" in key else "tCO2 (Market-based)"
            
            lines.append(f"### {name}")
            lines.append(f"✓ Mevcut kullanım: {current:,.2f} {unit} → Önerilen hedef: {target:,.2f} {unit} (%{reduction} azaltım)")
            lines.append(f"✓ Yıllık Karbon Tasarrufu: {saving:,.2f} tCO2")
            lines.append(f"✓ Yıllık CBAM Maliyet Tasarrufu: €{cost_saving:,.2f}")
            lines.append(f"✓ Yatırım Geri Dönüşü (ROI): {scenario.get('roi_years', 0):,.1f} Yıl")
            lines.append(f"✓ Uygulanacak Adımlar: {', '.join(scenario.get('measures', []))}")
            lines.append("")
            
        return "\n".join(lines)

    def build_report_prompt(self, metrics, emission_analysis, optimization_scenarios):
        """Construct a high-stakes partner-level prompt with specific numerical requirements"""
        
        prompt = f"""
Sen bir **Global Stratejik Danışmanlık Firması (McKinsey, BCG, Deloitte)** Kıdemli Partnerisin. Görevin, bir Holding CEO'su ve Yönetim Kurulu için kapsamlı bir **"CBAM STRATEJİK YÖNETİCİ RAPORU"** hazırlamaktır.

# 🎯 GÖREV
Aşağıdaki başlıklar altında **yönetici raporu** hazırla:

**ÖNEMLİ TALİMAT**: Bu rapor GERÇEK firma verileriyle hazırlanıyor. Aşağıdaki Scope 1&2 emisyon verilerini ve optimizasyon senaryolarını DOĞRUDAN KULLAN ve her öneride şu formatı uygula:
✓ "Mevcut kullanım: X ton/Nm³/MWh → Önerilen hedef: Y → Tasarruf: Z tCO2"
✓ Gerçek sayıları raporda belirt ve üzerinden somut öneriler sun.

### 1. EXECUTIVE SUMMARY (Yönetici Özeti)
- Toplam CBAM risk tutarı (Projenlendirilen 2030 toplamı: €{metrics.get('projected_total_2030', 0):,.2f}) ve emisyon profili özeti (SAYILARLA).
- Ana bulgular (2-3 cümle, GERÇEK verilerden çıkarım).
- Kritik dönemler ve en büyük emisyon kaynakları.

### 2. RISK ANALİZİ
- Yüksek riskli dönemler (ETS fiyat artışı ile ilişkilendir). En yüksek maliyetli dönem: {metrics.get('highest_quarter', 'Bilinmiyor')}.
- ETS fiyat volatilitesi ve tahmini trend ({metrics.get('ets_trend', 'Nötr')}).
- Maliyet artış trendleri ve firma kâr marjı ({metrics.get('financials', {}).get('profit_margin', 0)}%) üzerindeki baskı.

### 3. EMİSYON ANALİZİ (Scope 1 & 2) - **ZORUNLU: GERÇEK VERİ KULLAN**
Aşağıdaki teknik analiz verilerini kullanarak:
- Her kaynak için mevcut kullanım MİKTARI (örn: "Elektrot: {metrics.get('total_emission', 0):,.2f} tCO2 toplam emisyon payı içerisinde...")
- Toplam emisyon içindeki PAY (% olarak hesapla).
- En yüksek 3 emisyon kaynakları sırala ve değerlerini belirt.
- Her kaynak için iyileştirme potansiyeli değerlendir.

### 4. OPTİMİZASYON FIRSATLARİ - **SAYISAL HEDEFLERLE**
Aşağıdaki senaryoları kullanarak her kaynak için:
- "Mevcut: X → Hedef: Y (%Z azaltım) = W tCO2 tasarruf" formatını her kalem için uygula.
- Her öneri için yatırım tutarı ve geri ödeme süresi (tahmini).
- ROI hesabı (CBAM tasarrufu / yatırım maliyeti).
- Önceliklendirme (hızlı kazanç vs uzun vadeli yatırım).

### 5. STRATEJİK ÖNERİLER - **FİRMANIN GERÇEK VERİLERİNE ÖZEL**
Firmadaki mevcut tüketim bazında SOMUT adımlar:
- Kısa vadeli (2025-2026): Operasyonel değişikliklerle hızlı kazanımlar.
- Orta vadeli (2027-2028): Teknoloji yatırımları (Yenilenebilir enerji, proses değişikliği).
- Uzun vadeli (2029-2030): Toplam emisyon hedefi ve karbon-nötr vizyonu.

### 6. FİNANSAL ETKİ - **EURO BAZINDA NET HESAPLAR**
- Şu anki durum: CBAM maliyeti €{metrics.get('current_cbam_cost', 0):,.2f}
- Optimizasyonlar sonrası tahmini yıllık ve 2030 kümülatif tasarruf potansiyelleri.
- Toplam yatırım ihtiyacı vs. 5 yıllık tasarruf karşılaştırması.

### 7. SONUÇ VE TAVSİYELER

---
## ANALİZ İÇİN TEKNİK VERİLER:
- **Firma**: {metrics.get('company_name')} ({metrics.get('sector')} sektörü, {metrics.get('production_route')} rotası)
- **Raporlama Dönemi**: {metrics.get('reporting_period', '2024')}
- **Toplam Gömülü Emisyon**: {metrics.get('total_emission', 0):,.2f} tCO2e
- **Mevcut İhracat Miktarı**: {metrics.get('export_quantity', 0):,.2f} Ton
- **DETAYLI EMİSYON ANALİZİ (SAYILAR)**: 
{emission_analysis}

- **OPTİMİZASYON SENARYOLARI (SAYILAR)**:
{optimization_scenarios}

**NOT**: Rapor Türkçe olmalı, profesyonel ve net bir dille yazılmalı. Rakamları vurgula (**bold**). Metne "Aşağıdaki tabloda..." gibi giriş yapmadan doğrudan yönetici özetiyle başla.
"""
        return prompt

    def generate_report(self, cbam_summary, ets_forecast_table, cbam_cost_response, emission_analysis=None, optimization_scenarios=None, model="gemini-2.0-flash"):
        """Orchestrate the AI report generation"""
        from .cbam_cost_forecaster import CBAMCostForecaster
        forecaster = CBAMCostForecaster(self.client)
        cbam_df = forecaster.parse_forecast_response(cbam_cost_response)
        cbam_df = self.add_risk_analysis(cbam_df)
        metrics = self.calculate_metrics(cbam_summary, ets_forecast_table, cbam_df)
        
        # Format technical data for the prompt
        formatted_emissions = self.format_emission_data(emission_analysis)
        formatted_optimizations = self.format_optimization_data(optimization_scenarios)
        
        prompt = self.build_report_prompt(metrics, formatted_emissions, formatted_optimizations)
        
        import time
        max_retries = 3
        response = None
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(model=model, contents=prompt)
                break
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"⚠️ Gemini Rate Limit (429) hit. Retrying in {attempt + 2} seconds...")
                    time.sleep(attempt + 2)
                else:
                    raise e
        
        report_text = response.text if response else ""
        
        return {
            'metrics': metrics,
            'cbam_df': cbam_df,
            'report_text': report_text,
            'timestamp': datetime.now().isoformat()
        }

    def save_report(self, report_result, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_result['report_text'])
