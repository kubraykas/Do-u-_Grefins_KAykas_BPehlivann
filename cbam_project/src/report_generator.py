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
            'company_name': cbam_summary.get('company_name', 'Executive Leadership')
        }
        
        if isinstance(ets_forecast_table, pd.DataFrame) and not ets_forecast_table.empty:
            cols = ets_forecast_table.columns.tolist()
            val_col = next((c for c in cols if 'forecast' in c.lower() or 'price' in c.lower() or 'value' in c.lower()), cols[0])
            prices = ets_forecast_table[val_col]
            metrics.update({
                'ets_avg': prices.mean(),
                'ets_max': prices.max(),
                'ets_trend': "Bullish" if (prices.iloc[-1] > prices.iloc[0]) else "Bearish"
            })
            
        if not cbam_df.empty:
            metrics['projected_total_2030'] = cbam_df['CBAM_Cost'].sum()
            metrics['highest_quarter'] = cbam_df.loc[cbam_df['CBAM_Cost'].idxmax(), 'Quarter']
            
        return metrics

    def build_report_prompt(self, metrics, emission_analysis, optimization_scenarios):
        """Construct a high-stakes partner-level prompt"""
        
        prompt = f"""
Sen bir **Global Stratejik Danışmanlık Firması (McKinsey, BCG, Deloitte)** Kıdemli Partnerisin. Görevin, bir Holding CEO'su ve Yönetim Kurulu için **"CBAM STRATEJİK MALİYET VE OPERASYONEL DÖNÜŞÜM ANALİZİ"** hazırlamaktır.

Rapor tonu: **Kararlı, Vizyoner, Veri Odaklı ve Kesinlikle Resmi.** 
Sunum dili kullanma, Adobe InDesign ile basılacak profesyonel bir "Thought Leadership" dökümanı gibi yaz.

Analizini şu bölümler altında yapılandır:

### 1. STRATEJİK YÖNETİCİ ÖZETİ VE STRATEJİK PERSPEKTİF
- Şirketin AB Yeşil Mutabakatı altındaki kritik finansal konumu.
- **Kritik Eşik**: Mevcut karbon yoğunluğunun sürdürülebilir karlılık üzerindeki net etkisi.

### 2. FİNANSAL RİSK MATRİSİ (2025-2030)
- ETS fiyat volatilitesi ve CBAM sertifika maliyetlerinin nakit akışına kümülatif etkisi.
- Karbon bazlı maliyetlerin ürün marjları üzerindeki baskı analizi.

### 3. OPERASYONEL VERİMLİLİK VE EMİSYON PROFİLİ
- Scope 1 & 2 dökümü üzerinden en yüksek iyileştirme potansiyeli olan süreçlerin tespiti.
- Benchmark Analizi: Sektörel düşük karbon liderleriyle olan "Verimlilik Gap" analizi.

### 4. YEŞİL SERMAYE VE KARBON YATIRIM STRATEJİSİ
- Düşük karbonlu üretime geçişin bir maliyet değil, bir **Sermaye Geri Kazanımı** yatırımı olarak analizi.
- Önerilen optimizasyonların ROI ve finansman kapasitesine (ESG Kredileri) çarpan etkisi.

### 5. 2030 STRATEJİK YOL HARİTASI
- Kısa, orta ve uzun vadeli aksiyon planı.
- Karbon nötr hedeflerinin pazar payı ve marka değeri üzerindeki kaldıraç etkisi.

---
## ANALİZ İÇİN DONELER (BU VERİLERİ METNE ENTEGRE ET):
- **Firma**: {metrics.get('company_name')}
- **Ürün**: {metrics.get('product')}
- **Toplam Gömülü Emisyon**: {metrics.get('total_emission', 0):,.2f} tCO2e
- **Mevcut CBAM Maruziyeti**: €{metrics.get('current_cbam_cost', 0):,.2f}
- **Emisyon Envanteri**: {emission_analysis if emission_analysis else 'Detaylı veri bekleniyor'}
- **Optimizasyon Hedefleri**: {optimization_scenarios if optimization_scenarios else 'Hesaplanıyor'}

**TALİMATLAR**: 
- Gerçekçi ve profesyonel ol. 
- Türkçe karakterleri (ğ, ü, ş, i, ö, ç) kusursuz kullan. 
- Önemli stratejik terimleri ve sayıları **bold** yap. 
- Metne "The following table", "Based on my analysis" gibi dolgu cümlelerle başlama, doğrudan analize gir.
"""
        return prompt

    def generate_report(self, cbam_summary, ets_forecast_table, cbam_cost_response, emission_analysis=None, optimization_scenarios=None, model="gemini-2.0-flash"):
        """Orchestrate the AI report generation"""
        from .cbam_cost_forecaster import CBAMCostForecaster
        forecaster = CBAMCostForecaster(self.client)
        cbam_df = forecaster.parse_forecast_response(cbam_cost_response)
        cbam_df = self.add_risk_analysis(cbam_df)
        metrics = self.calculate_metrics(cbam_summary, ets_forecast_table, cbam_df)
        
        prompt = self.build_report_prompt(metrics, emission_analysis, optimization_scenarios)
        
        response = self.client.models.generate_content(model=model, contents=prompt)
        report_text = response.text
        
        return {
            'metrics': metrics,
            'cbam_df': cbam_df,
            'report_text': report_text,
            'timestamp': datetime.now().isoformat()
        }

    def save_report(self, report_result, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_result['report_text'])
