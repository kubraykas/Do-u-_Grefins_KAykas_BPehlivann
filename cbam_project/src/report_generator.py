"""
CBAM Executive Report Generator Module
Generates professional executive reports using Gemini LLM
"""

import pandas as pd
from datetime import datetime


class CBAMReportGenerator:
    """
    Generates comprehensive CBAM executive reports
    """
    
    def __init__(self, gemini_client):
        """
        Initialize report generator with Gemini client
        
        Args:
            gemini_client: Gemini API client instance
        """
        self.client = gemini_client
    
    def add_risk_analysis(self, cbam_df):
        """
        Add risk level classification to CBAM cost forecast
        
        Args:
            cbam_df (pandas.DataFrame): CBAM cost forecast data
            
        Returns:
            pandas.DataFrame: Data with risk levels added
        """
        if cbam_df.empty:
            cbam_df['Risk_Level'] = []
            return cbam_df

        q90 = cbam_df['CBAM_Cost'].quantile(0.9)
        mean_cost = cbam_df['CBAM_Cost'].mean()

        def risk_label(x):
            if x >= q90:
                return "🔴 High Risk"
            elif x >= mean_cost:
                return "🟠 Medium Risk"
            else:
                return "🟢 Low Risk"

        cbam_df['Risk_Level'] = cbam_df['CBAM_Cost'].apply(risk_label)
        return cbam_df
    
    def calculate_metrics(self, cbam_summary, ets_forecast_table, cbam_df):
        """
        Calculate comprehensive metrics for the report
        
        Args:
            cbam_summary (dict): Current CBAM calculation summary
            ets_forecast_table (pandas.DataFrame): ETS price forecasts
            cbam_df (pandas.DataFrame): CBAM cost forecasts
            
        Returns:
            dict: Complete set of metrics
        """
        metrics = {}
        
        # Product information
        metrics['product'] = cbam_summary['product']
        metrics['category'] = cbam_summary['category']
        metrics['quantity_tonnes'] = cbam_summary['quantity_tonnes']
        metrics['total_ei'] = cbam_summary['total_ei']
        metrics['current_cbam_cost'] = cbam_summary['cbam_cost']
        
        # ETS Forecast analysis
        if isinstance(ets_forecast_table, pd.DataFrame) and not ets_forecast_table.empty:
            # Find the correct column name
            ets_col = None
            if 'Forecasted Value' in ets_forecast_table.columns:
                ets_col = 'Forecasted Value'
            elif 'Forecasted_Value' in ets_forecast_table.columns:
                ets_col = 'Forecasted_Value'
            elif 'forecasted_value' in ets_forecast_table.columns:
                ets_col = 'forecasted_value'
            
            if ets_col:
                ets_prices = ets_forecast_table[ets_col]
                metrics['ets_min'] = ets_prices.min()
                metrics['ets_max'] = ets_prices.max()
                metrics['ets_avg'] = ets_prices.mean()
                metrics['ets_start'] = ets_prices.iloc[0]
                metrics['ets_end'] = ets_prices.iloc[-1]
                
                # Calculate trend
                change_pct = ((metrics['ets_end'] - metrics['ets_start']) / metrics['ets_start']) * 100
                if change_pct > 10:
                    metrics['ets_trend'] = "↗️ Yükseliş"
                elif change_pct < -10:
                    metrics['ets_trend'] = "↘️ Düşüş"
                else:
                    metrics['ets_trend'] = "➡️ Stabil"
                metrics['ets_trend_pct'] = f"{change_pct:+.1f}%"
            else:
                metrics.update({
                    'ets_min': 0, 'ets_max': 0, 'ets_avg': 0,
                    'ets_start': 0, 'ets_end': 0,
                    'ets_trend': "N/A", 'ets_trend_pct': "N/A"
                })
        else:
            metrics.update({
                'ets_min': 0, 'ets_max': 0, 'ets_avg': 0,
                'ets_start': 0, 'ets_end': 0,
                'ets_trend': "N/A", 'ets_trend_pct': "N/A"
            })
        
        # CBAM Cost analysis
        if not cbam_df.empty:
            metrics['total_cbam_cost'] = cbam_df['CBAM_Cost'].sum()
            metrics['avg_cbam_cost'] = cbam_df['CBAM_Cost'].mean()
            metrics['max_cbam_cost'] = cbam_df['CBAM_Cost'].max()
            metrics['min_cbam_cost'] = cbam_df['CBAM_Cost'].min()
            
            # Critical period
            idx_max = cbam_df['CBAM_Cost'].idxmax()
            metrics['critical_quarter'] = cbam_df.loc[idx_max, 'Quarter']
            metrics['critical_cost'] = cbam_df.loc[idx_max, 'CBAM_Cost']
            
            # Yearly totals
            cbam_df['Year'] = cbam_df['Quarter'].str.extract(r'(\d{4})')
            yearly = cbam_df.groupby('Year')['CBAM_Cost'].sum()
            metrics['yearly_totals'] = yearly.to_dict()
            metrics['highest_year'] = yearly.idxmax()
            metrics['highest_year_cost'] = yearly.max()
        else:
            metrics.update({
                'total_cbam_cost': 0, 'avg_cbam_cost': 0,
                'max_cbam_cost': 0, 'min_cbam_cost': 0,
                'critical_quarter': 'N/A', 'critical_cost': 0,
                'yearly_totals': {}, 'highest_year': 'N/A',
                'highest_year_cost': 0
            })
        
        return metrics
    
    def _format_emission_analysis(self, emission_analysis):
        """Format emission analysis for report prompt"""
        if not emission_analysis:
            return "**Detaylı emisyon verisi sağlanmadı.**"
        
        text = ""
        
        # Scope 1
        if emission_analysis.get('scope1'):
            s1 = emission_analysis['scope1']
            text += f"""
**Scope 1 - Doğrudan Emisyonlar: {s1['total_scope1']:,.2f} tCO2**

Dağılım:
- Yakıt Bazlı: {s1['total_fuel']:,.2f} tCO2 ({s1['breakdown_percent']['fuel']:.1f}%)
  - Kok Kömürü: {s1['fuel_emissions']['coking_coal']:,.2f} tCO2
  - Doğalgaz: {s1['fuel_emissions']['natural_gas']:,.2f} tCO2
  - Fuel Oil: {s1['fuel_emissions']['fuel_oil']:,.2f} tCO2
- Proses Bazlı: {s1['total_process']:,.2f} tCO2 ({s1['breakdown_percent']['process']:.1f}%)
  - Kireçtaşı: {s1['process_emissions']['limestone']:,.2f} tCO2
- Termal Sistemler: {s1['total_thermal']:,.2f} tCO2 ({s1['breakdown_percent']['thermal']:.1f}%)

Emisyon Yoğunluğu: {s1['emission_intensity']:.2f} tCO2/ton çelik
"""
        
        # Scope 2
        if emission_analysis.get('scope2'):
            s2 = emission_analysis['scope2']
            text += f"""
**Scope 2 - Dolaylı Emisyonlar: {s2['total_scope2']:,.2f} tCO2**

Dağılım:
- Grid Elektrik ({s2['grid_share_percent']:.0f}%): {s2['grid_emissions']:,.2f} tCO2
- Yenilenebilir ({s2['renewable_percent']:.0f}%): {s2['renewable_emissions']:,.2f} tCO2
- Toplam Tüketim: {s2['consumption_mwh']:,.2f} MWh
- Grid Emisyon Faktörü: {s2['grid_emission_factor']:.3f} kgCO2/kWh
"""
        
        # Total
        if 'total_emissions' in emission_analysis:
            text += f"""
**Toplam Scope 1+2 Emisyonlar: {emission_analysis['total_emissions']:,.2f} tCO2**
"""
        
        return text
    
    def _format_optimization_scenarios(self, optimization_scenarios):
        """Format optimization scenarios for report prompt"""
        if not optimization_scenarios:
            return "**Optimizasyon senaryoları hesaplanmadı.**"
        
        text = ""
        for key, scenario in optimization_scenarios.items():
            if key == 'combined':
                text += f"""
**{scenario['name']}**
- Toplam Emisyon Tasarrufu: {scenario['total_emission_saving_tco2']:,.2f} tCO2/yıl
- Toplam CBAM Tasarrufu: €{scenario['total_annual_cbam_saving_eur']:,.2f}/yıl
- Toplam Yatırım: €{scenario['total_investment_needed_eur']:,.2f}
- ROI: {scenario['roi_years']:.1f} yıl
- Emisyon Azaltımı: {scenario['emission_reduction_percent']:.1f}%
"""
            else:
                text += f"""
**{scenario['name']}**
- Emisyon Tasarrufu: {scenario['emission_saving_tco2']:,.2f} tCO2/yıl
- Yıllık CBAM Tasarrufu: €{scenario['annual_cbam_saving_eur']:,.2f}
- Gereken Yatırım: €{scenario['investment_needed_eur']:,.2f}
- ROI: {scenario['roi_years']:.1f} yıl
- Önlemler: {', '.join(scenario['measures'])}

"""
        
        return text
    
    def build_report_prompt(self, cbam_summary, ets_forecast_table, cbam_df, metrics, emission_analysis=None, optimization_scenarios=None):
        """
        Build comprehensive report prompt for Gemini
        
        Args:
            cbam_summary (dict): Current CBAM calculation summary
            ets_forecast_table (pandas.DataFrame): ETS price forecasts
            cbam_df (pandas.DataFrame): CBAM cost forecasts
            metrics (dict): Calculated metrics
            emission_analysis (dict): Scope 1&2 emission analysis
            optimization_scenarios (dict): Optimization scenarios
            
        Returns:
            str: Formatted prompt for Gemini
        """
        # ETS forecast table
        if isinstance(ets_forecast_table, pd.DataFrame):
            ets_table_str = ets_forecast_table.to_string(index=False)
        else:
            ets_table_str = str(ets_forecast_table)
        
        # CBAM cost table
        if not cbam_df.empty:
            cbam_table_str = cbam_df.to_string(index=False)
        else:
            cbam_table_str = "No data available"
        
        # Yearly breakdown
        yearly_text = "\n".join([f"{year}: €{cost:,.0f}" for year, cost in metrics['yearly_totals'].items()])
        
        prompt = f"""
Sen bir **EU CBAM Finansal Danışmanı**sın. Aşağıdaki verilere dayanarak **üst düzey yöneticiler** için profesyonel bir rapor hazırla.

---
## 📦 ÜRÜN BİLGİLERİ
- **Ürün**: {metrics['product']}
- **Sektör**: {metrics['category']}
- **İthalat Miktarı**: {metrics['quantity_tonnes']:,.0f} ton
- **Emisyon Yoğunluğu**: {metrics['total_ei']:.2f} tCO2/ton
- **Mevcut CBAM Maliyeti**: €{metrics['current_cbam_cost']:,.2f}

---
## 📊 ETS FİYAT TAHMİNLERİ (Q1 2025 - Q4 2030)

{ets_table_str}

**ETS Fiyat İstatistikleri:**
- Minimum: €{metrics['ets_min']:.2f}
- Maksimum: €{metrics['ets_max']:.2f}
- Ortalama: €{metrics['ets_avg']:.2f}
- Trend: {metrics['ets_trend']} ({metrics['ets_trend_pct']})

---
## 💰 CBAM MALİYET PROJEKSİYONLARI

{cbam_table_str}

**CBAM Maliyet İstatistikleri:**
- **Toplam CBAM Maliyeti (2025-2030)**: €{metrics['total_cbam_cost']:,.2f}
- **Ortalama Çeyreklik Maliyet**: €{metrics['avg_cbam_cost']:,.2f}
- **En Yüksek Maliyet Dönemi**: {metrics['critical_quarter']} (€{metrics['critical_cost']:,.2f})

**Yıllık CBAM Maliyet Dağılımı:**
{yearly_text}

**En Yüksek Maliyetli Yıl**: {metrics['highest_year']} (€{metrics['highest_year_cost']:,.2f})

---
## � EMİSYON PROFİLİ ANALİZİ (Scope 1 & 2)

{self._format_emission_analysis(emission_analysis)}

---
## 💡 OPTİMİZASYON SENARYOLARI

{self._format_optimization_scenarios(optimization_scenarios)}

---
## �🎯 GÖREV

Aşağıdaki başlıklar altında **yönetici raporu** hazırla:

**ÖNEMLİ TALİMAT**: Bu rapor GERÇEK firma verileriyle hazırlanıyor. Yukarıdaki Scope 1&2 emisyon verilerini DOĞRUDAN KULLAN ve her öneride şu formatı uygula:
✓ "Mevcut kullanım: X ton/Nm³/MWh → Önerilen hedef: Y → Tasarruf: Z tCO2"
✓ Gerçek sayıları raporda belirt ve üzerine öneriler sun

### 1. EXECUTIVE SUMMARY (Yönetici Özeti)
- Toplam CBAM risk tutarı ve emisyon profili özeti (SAYILARLA)
- Ana bulgular (2-3 cümle, yukarıdaki GERÇEK verilerden çıkarım)
- Kritik dönemler ve en büyük emisyon kaynakları

### 2. RISK ANALİZİ
- Yüksek riskli dönemler (ETS fiyat artışı ile ilişkilendir)
- ETS fiyat volatilitesi (€/tCO2 bazında)
- Maliyet artış trendleri (yıllık % olarak)

### 3. EMİSYON ANALİZİ (Scope 1 & 2) - **ZORUNLU: GERÇEK VERİ KULLAN**
Yukarıdaki tablodaki SAYISAL verileri kullanarak:
- Her kaynak için mevcut kullanım MİKTARI (örn: "Kok Kömürü: 1,500 ton → 2,400 tCO2 emisyon")
- Toplam emisyon içindeki PAY (% olarak hesapla)
- En yüksek 3 emisyon kaynağını sırala ve değerlerini belirt
- Her kaynak için iyileştirme potansiyeli değerlendir

### 4. OPTİMİZASYON FIRSATLARİ - **SAYISAL HEDEFLERLE**
Her senaryo için HESAPLANMIŞ somut öneriler:
- Yukarıdaki optimizasyon senaryolarını kullanarak her kaynak için:
  * "Mevcut: X ton/Nm³ → Hedef: Y ton/Nm³ (%Z azaltım) = W tCO2 tasarruf"
- Her öneri için yatırım tutarı ve geri ödeme süresi
- ROI hesabı (CBAM tasarrufu / yatırım maliyeti)
- Önceliklendirme (hızlı kazanç vs uzun vadeli yatırım)

### 5. STRATEJİK ÖNERİLER - **FİRMANIN GERÇEK VERİLERİNE ÖZEL**
Firmadaki mevcut tüketim bazında SOMUT adımlar:
- Kısa vadeli (2025-2026): Operasyonel değişikliklerle hızlı kazanımlar (sayısal hedefler)
- Orta vadeli (2027-2028): Teknoloji yatırımları ile spesifik emisyon azaltımları
- Uzun vadeli (2029-2030): Toplam emisyon hedefi (başlangıca göre %X azalım)

### 6. FİNANSAL ETKİ - **EURO BAZINDA NET HESAPLAR**
Hesaplanmış tasarruf potansiyelleri:
- Şu anki durum: CBAM maliyeti €X
- Optimizasyon Senaryo 1 ile: €Y tasarruf (%Z azalım)
- Optimizasyon Senaryo 2 ile: €W tasarruf (%V azalım)
- Toplam yatırım ihtiyacı vs. 5 yıllık tasarruf karşılaştırması

### 7. SONUÇ VE TAVSİYELER

---
**NOT**: Rapor Türkçe olmalı, profesyonel ve net bir dille yazılmalı. Rakamları vurgula.
"""
        
        return prompt
    
    def generate_report(self, cbam_summary, ets_forecast_table, cbam_cost_response, emission_analysis=None, optimization_scenarios=None, model="gemini-2.5-flash"):
        """
        Generate complete executive CBAM report
        
        Args:
            cbam_summary (dict): Current CBAM calculation summary
            ets_forecast_table (pandas.DataFrame): ETS price forecasts
            cbam_cost_response (str): Raw CBAM cost forecast response
            emission_analysis (dict): Scope 1&2 emission analysis (optional)
            optimization_scenarios (dict): Optimization scenarios (optional)
            model (str): Gemini model to use
            
        Returns:
            dict: Report results including metrics, dataframes, and report text
        """
        print("\n" + "="*70)
        print("📊 CBAM YÖNETİCİ RAPORU ÜRETİLİYOR...")
        print("="*70 + "\n")
        
        # Parse CBAM cost table
        from .cbam_cost_forecaster import CBAMCostForecaster
        forecaster = CBAMCostForecaster(self.client)
        cbam_df = forecaster.parse_forecast_response(cbam_cost_response)
        
        # Add risk analysis
        cbam_df = self.add_risk_analysis(cbam_df)
        
        # Calculate metrics
        metrics = self.calculate_metrics(cbam_summary, ets_forecast_table, cbam_df)
        
        # Build report prompt (with emission analysis and optimization)
        report_prompt = self.build_report_prompt(
            cbam_summary, 
            ets_forecast_table, 
            cbam_df, 
            metrics,
            emission_analysis,
            optimization_scenarios
        )
        
        # Generate report with Gemini
        response = self.client.models.generate_content(
            model=model,
            contents=report_prompt
        )
        
        report_text = response.text
        
        # Print report
        print("\n" + "="*70)
        print("📋 CBAM YÖNETİCİ RAPORU")
        print("="*70 + "\n")
        print(report_text)
        print("\n" + "="*70)
        print("✅ Rapor başarıyla oluşturuldu")
        print("="*70 + "\n")
        
        return {
            'metrics': metrics,
            'cbam_df': cbam_df,
            'report_text': report_text,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_report(self, report_result, output_path):
        """
        Save report to file
        
        Args:
            report_result (dict): Report generation result
            output_path (str): Path to save report
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("CBAM YÖNETİCİ RAPORU\n")
            f.write(f"Oluşturulma Tarihi: {report_result['timestamp']}\n")
            f.write("="*70 + "\n\n")
            f.write(report_result['report_text'])
        
        print(f"✅ Rapor kaydedildi: {output_path}")
