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
    
    def build_report_prompt(self, cbam_summary, ets_forecast_table, cbam_df, metrics):
        """
        Build comprehensive report prompt for Gemini
        
        Args:
            cbam_summary (dict): Current CBAM calculation summary
            ets_forecast_table (pandas.DataFrame): ETS price forecasts
            cbam_df (pandas.DataFrame): CBAM cost forecasts
            metrics (dict): Calculated metrics
            
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
## 🎯 GÖREV

Aşağıdaki başlıklar altında **yönetici raporu** hazırla:

### 1. EXECUTIVE SUMMARY (Yönetici Özeti)
- Toplam CBAM risk tutarı
- Ana bulgular (2-3 cümle)
- Kritik dönemler

### 2. RISK ANALİZİ
- Yüksek riskli dönemler
- ETS fiyat volatilitesi
- Maliyet artış trendleri

### 3. STRATEJİK ÖNERİLER
- Kısa vadeli aksiyonlar (2025-2026)
- Orta vadeli aksiyonlar (2027-2028)
- Uzun vadeli aksiyonlar (2029-2030)

### 4. FİNANSAL ETKİ
- Yıllık maliyet artışı
- Bütçe planlama önerileri
- Nakit akışı etkileri

### 5. SONUÇ VE TAVSİYELER

---
**NOT**: Rapor Türkçe olmalı, profesyonel ve net bir dille yazılmalı. Rakamları vurgula.
"""
        
        return prompt
    
    def generate_report(self, cbam_summary, ets_forecast_table, cbam_cost_response, model="gemini-2.5-flash"):
        """
        Generate complete executive CBAM report
        
        Args:
            cbam_summary (dict): Current CBAM calculation summary
            ets_forecast_table (pandas.DataFrame): ETS price forecasts
            cbam_cost_response (str): Raw CBAM cost forecast response
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
        
        # Build report prompt
        report_prompt = self.build_report_prompt(cbam_summary, ets_forecast_table, cbam_df, metrics)
        
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
