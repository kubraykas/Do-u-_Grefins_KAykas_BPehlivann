"""
CBAM Web Application
Flask-based web interface
"""

from flask import Flask, render_template, request, jsonify, send_file, session
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Ana proje yolunu ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.cbam_calculator import CBAMCalculator
from src.cn_code_database import CN_CODE_DATABASE
from src.ets_predictor import ETSPricePredictor
from src.cbam_cost_forecaster import CBAMCostForecaster
from src.report_generator import CBAMReportGenerator
from src.emission_analyzer import EmissionAnalyzer
from src.pdf_generator import CBAMPDFGenerator

# Environment variables
load_dotenv()

# Gemini client (optional)
try:
    from google import genai
    gemini_api_key = os.getenv('GOOGLE_API_KEY')
    gemini_client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None
except:
    gemini_client = None

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'cbam-secret-key-2026')

# Global storage for last report data (for PDF generation)
app.last_report_data = None


@app.route('/')
def index():
    """Ana sayfa - Form"""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """CBAM hesaplama yap"""
    try:
        # Hangi buton tıklandı kontrol et
        action = request.form.get('action', 'calculate')
        
        # Eğer tam analiz istenmişse, full_analysis'e yönlendir
        if action == 'full-analysis':
            return full_analysis()
        
        # Normal hesaplama
        ets_price = float(request.form['ets_price'])
        quantity = float(request.form['quantity'])
        cn_code = request.form['cn_code']
        
        # Opsiyonel detaylı emisyon verileri
        detailed_data = {}
        
        # Tesis Bilgileri
        if request.form.get('plant_id'):
            detailed_data['reporting'] = {
                'plant_id': request.form.get('plant_id', ''),
                'country_code': request.form.get('country_code', ''),
                'reporting_year': request.form.get('reporting_year', ''),
                'production_route': request.form.get('production_route', ''),
                'electricity_source': request.form.get('electricity_source', '')
            }
        
        # Scope 1 - Doğrudan Emisyonlar
        scope1_data = {}
        if request.form.get('coking_coal_ton') or request.form.get('natural_gas_nm3'):
            scope1_data['fuel'] = {
                'coking_coal_ton': float(request.form.get('coking_coal_ton', 0) or 0),
                'natural_gas_nm3': float(request.form.get('natural_gas_nm3', 0) or 0),
                'fuel_oil_ton': float(request.form.get('fuel_oil_ton', 0) or 0)
            }
            scope1_data['process'] = {
                'limestone_ton': float(request.form.get('limestone_ton', 0) or 0)
            }
            scope1_data['thermal_systems'] = {
                'reheating_fuel_nm3': float(request.form.get('reheating_fuel_nm3', 0) or 0)
            }
            scope1_data['steel_output_ton'] = float(request.form.get('steel_output_ton', 0) or 0)
            detailed_data['scope1'] = scope1_data
        
        # Scope 2 - Dolaylı Emisyonlar
        if request.form.get('electricity_consumption_mwh'):
            detailed_data['scope2'] = {
                'electricity': {
                    'electricity_consumption_mwh': float(request.form.get('electricity_consumption_mwh', 0) or 0),
                    'grid_emission_factor_kgco2_kwh': float(request.form.get('grid_emission_factor', 0) or 0),
                    'renewable_share_percent': float(request.form.get('renewable_share_percent', 0) or 0)
                }
            }
        
        # Veri Kalitesi
        if request.form.get('natural_gas_quality') or request.form.get('electricity_quality'):
            detailed_data['data_quality'] = {}
            if request.form.get('natural_gas_quality'):
                detailed_data['data_quality']['natural_gas_nm3'] = {
                    'quality': request.form.get('natural_gas_quality', '')
                }
            if request.form.get('electricity_quality'):
                detailed_data['data_quality']['electricity_consumption_mwh'] = {
                    'quality': request.form.get('electricity_quality', '')
                }
        
        calc = CBAMCalculator(ets_price)
        summary = calc.get_summary(cn_code, quantity)
        
        if summary is None:
            return render_template('error.html', 
                                 error="CN Code bulunamadı!")
        
        return render_template('results.html', 
                             summary=summary, 
                             detailed_data=detailed_data if detailed_data else None)
        
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/cn-codes')
def cn_codes():
    """CN kodları listesi"""
    codes = []
    for code, data in CN_CODE_DATABASE.items():
        codes.append({
            'code': code,
            'description': data['description'],
            'category': data['category'],
            'total_ei': data['total']
        })
    return render_template('cn_codes.html', codes=codes)


@app.route('/full-analysis', methods=['POST'])
def full_analysis():
    """Tam analiz: CBAM + ETS Tahmin + Maliyet Projeksiyonu + Rapor"""
    try:
        if not gemini_client:
            return render_template('error.html', 
                                 error="Gemini API yapılandırılmamış. .env dosyasına GOOGLE_API_KEY ekleyin.")
        
        ets_price = float(request.form['ets_price'])
        quantity = float(request.form['quantity'])
        cn_code = request.form['cn_code']
        
        # CSV path - projede veya masaüstünde
        csv_path = os.getenv('ETS_CSV_PATH', 'C:\\Users\\LENOVO\\Desktop\\icap-graph-price-data-2014-01-01-2025-11-21.csv')
        
        # Alternatif path denemeleri
        if not os.path.exists(csv_path):
            csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'icap-graph-price-data-2014-01-01-2025-11-21.csv')
        
        if not os.path.exists(csv_path):
            return render_template('error.html', 
                                 error=f"ETS fiyat CSV dosyası bulunamadı: {csv_path}")
        
        # === ADIM 1: CBAM HESAPLAMA ===
        calc = CBAMCalculator(ets_price)
        cbam_summary = calc.get_summary(cn_code, quantity)
        
        if cbam_summary is None:
            return render_template('error.html', error="CN Code bulunamadı!")
        
        # === YENİ: SCOPE 1 & 2 ANALİZİ ===
        emission_analysis = None
        optimization_scenarios = None
        
        # Scope 1 & 2 verilerini topla
        scope1_data = None
        scope2_data = None
        
        if request.form.get('natural_gas_nm3') or request.form.get('coking_coal_ton'):
            scope1_data = {
                'fuel': {
                    'coking_coal_ton': float(request.form.get('coking_coal_ton', 0) or 0),
                    'natural_gas_nm3': float(request.form.get('natural_gas_nm3', 0) or 0),
                    'fuel_oil_ton': float(request.form.get('fuel_oil_ton', 0) or 0)
                },
                'process': {
                    'limestone_ton': float(request.form.get('limestone_ton', 0) or 0)
                },
                'thermal_systems': {
                    'reheating_fuel_nm3': float(request.form.get('reheating_fuel_nm3', 0) or 0)
                },
                'steel_output_ton': float(request.form.get('steel_output_ton', 0) or 5000)
            }
        
        if request.form.get('electricity_consumption_mwh'):
            scope2_data = {
                'electricity': {
                    'electricity_consumption_mwh': float(request.form.get('electricity_consumption_mwh', 0) or 0),
                    'grid_emission_factor_kgco2_kwh': float(request.form.get('grid_emission_factor', 0) or 0),
                    'renewable_share_percent': float(request.form.get('renewable_share_percent', 0) or 0)
                }
            }
        
        # Emisyon analizi yap
        if scope1_data or scope2_data:
            analyzer = EmissionAnalyzer()
            
            if scope1_data:
                analyzer.calculate_scope1(scope1_data)
            if scope2_data:
                analyzer.calculate_scope2(scope2_data)
            
            emission_analysis = analyzer.get_summary()
            optimization_scenarios = analyzer.get_optimization_scenarios(scope1_data, scope2_data, ets_price)
            
            print(f"\n✅ Emisyon Analizi Tamamlandı:")
            print(f"   Scope 1: {emission_analysis['scope1']['total_scope1'] if emission_analysis['scope1'] else 0:.2f} tCO2")
            print(f"   Scope 2: {emission_analysis['scope2']['total_scope2'] if emission_analysis['scope2'] else 0:.2f} tCO2")
            print(f"   Toplam: {emission_analysis['total_emissions']:.2f} tCO2")
            print(f"   Optimizasyon Senaryoları: {len(optimization_scenarios)} adet\n")
        
        # === ADIM 2: ETS FİYAT TAHMİNİ ===
        predictor = ETSPricePredictor(gemini_client)
        ets_forecast, ets_stats = predictor.predict(csv_path)
        
        # === ADIM 3: CBAM MALİYET PROJEKSİYONU ===
        forecaster = CBAMCostForecaster(gemini_client)
        cbam_cost_forecast = forecaster.forecast(cbam_summary, ets_forecast)
        
        # === ADIM 4: YÖNETİCİ RAPORU (Emisyon analizi dahil) ===
        generator = CBAMReportGenerator(gemini_client)
        report = generator.generate_report(
            cbam_summary, 
            ets_forecast, 
            cbam_cost_forecast,
            emission_analysis,
            optimization_scenarios
        )
        
        # Session'a kaydet (sadece özet bilgiler - cookie limiti için)
        session['last_report'] = {
            'cbam_cost': cbam_summary['total_cost'],
            'total_emissions': emission_analysis.get('total_emissions', 0),
            'timestamp': datetime.now().isoformat()
        }
        
        # Tam rapor verisini app context'e kaydet (PDF için)
        app.last_report_data = {
            'cbam_summary': cbam_summary,
            'ets_forecast': ets_forecast,
            'report_text': report['report_text'],
            'emission_analysis': emission_analysis,
            'optimization_scenarios': optimization_scenarios,
            'company_info': company_info,
            'timestamp': datetime.now()
        }
        
        # === RAPORU DOSYAYA KAYDET ===
        try:
            from pathlib import Path
            reports_dir = Path(__file__).parent.parent / 'reports'
            reports_dir.mkdir(exist_ok=True)
            
            # Dosya adı: şirket_ismi_tarih.txt
            company_name = company_info.get('company_name', 'firma').replace(' ', '_').lower()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{company_name}_raporu_{timestamp}.txt"
            filepath = reports_dir / filename
            
            # Rapor içeriğini hazırla
            report_content = f"""
{'='*80}
CBAM ANALİZ RAPORU
{'='*80}

ŞİRKET BİLGİLERİ:
  Firma: {company_info.get('company_name', 'N/A')}
  Ülke: {company_info.get('origin_country', 'N/A')}
  Ürün: {company_info.get('product_name', 'N/A')}
  CN Kodu: {company_info.get('cn_code', 'N/A')}
  Miktar: {company_info.get('quantity', 0)} ton
  Gömülü Emisyon: {company_info.get('embedded_emissions', 0)} tCO2e/ton
  Tarih: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

{'='*80}
CBAM MALİYET ÖZETİ
{'='*80}

  Toplam Emisyon: {cbam_summary['total_emissions']:,.2f} tCO2e
  Ortalama ETS Fiyatı: €{cbam_summary['avg_ets_price']:.2f}/tCO2
  Toplam CBAM Maliyeti: €{cbam_summary['total_cost']:,.2f}
  Birim Maliyet: €{cbam_summary['cost_per_ton']:.2f}/ton ürün

{'='*80}
ETS FİYAT TAHMİNLERİ (İlk 8 Çeyrek)
{'='*80}

"""
            # ETS forecast tablosu
            for idx, row in enumerate(ets_forecast.head(8).to_dict('records'), 1):
                report_content += f"  {idx}. {row['Quarter']}: €{row['Predicted_Price']:.2f}/tCO2\n"
            
            report_content += f"\n{'='*80}\nEMİSYON ANALİZİ (Scope 1 & 2)\n{'='*80}\n\n"
            
            # Scope 1 detayları
            if emission_analysis.get('scope1'):
                scope1 = emission_analysis['scope1']
                report_content += f"SCOPE 1 (Doğrudan Emisyonlar):\n"
                report_content += f"  Toplam: {scope1.get('total_scope1', 0):,.2f} tCO2\n\n"
                
                if scope1.get('fuel_combustion'):
                    report_content += "  Yakıt Yanması:\n"
                    for fuel, data in scope1['fuel_combustion'].items():
                        report_content += f"    - {fuel}: {data['emission_tco2']:,.2f} tCO2 ({data['consumption']:.2f} {data.get('unit', 'ton')})\n"
                
                if scope1.get('process_emissions'):
                    report_content += f"\n  Proses Emisyonları: {scope1['process_emissions']:,.2f} tCO2\n"
                
                if scope1.get('thermal_energy'):
                    report_content += f"  Termal Enerji: {scope1['thermal_energy']:,.2f} tCO2\n"
            
            # Scope 2 detayları
            if emission_analysis.get('scope2'):
                scope2 = emission_analysis['scope2']
                report_content += f"\nSCOPE 2 (Dolaylı Emisyonlar):\n"
                report_content += f"  Elektrik Tüketimi: {scope2.get('total_scope2', 0):,.2f} tCO2\n"
                if scope2.get('electricity_kwh'):
                    report_content += f"    Tüketim: {scope2['electricity_kwh']:,.2f} MWh\n"
                if scope2.get('renewable_share'):
                    report_content += f"    Yenilenebilir Enerji: %{scope2['renewable_share']:.1f}\n"
            
            report_content += f"\nTOPLAM EMİSYON: {emission_analysis.get('total_emissions', 0):,.2f} tCO2\n"
            
            # Optimizasyon senaryoları
            if optimization_scenarios:
                report_content += f"\n{'='*80}\nOPTİMİZASYON SENARYOLARI\n{'='*80}\n\n"
                for idx, scenario in enumerate(optimization_scenarios, 1):
                    report_content += f"{idx}. {scenario['name']}\n"
                    report_content += f"   Açıklama: {scenario['description']}\n"
                    report_content += f"   Emisyon Azaltımı: {scenario['emission_reduction']:,.2f} tCO2 ({scenario['reduction_percent']:.1f}%)\n"
                    report_content += f"   Maliyet Tasarrufu: €{scenario['cost_saving']:,.2f}\n"
                    report_content += f"   Yatırım: €{scenario['investment']:,.2f}\n"
                    report_content += f"   Geri Ödeme: {scenario['payback_years']:.1f} yıl\n"
                    report_content += f"   ROI: %{scenario['roi']:.1f}\n\n"
            
            # Yönetici raporu
            report_content += f"\n{'='*80}\nYÖNETİCİ RAPORU (AI Tarafından Oluşturuldu)\n{'='*80}\n\n"
            report_content += report['report_text']
            
            report_content += f"\n\n{'='*80}\nRAPOR SONU\n{'='*80}\n"
            
            # Dosyaya yaz
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"\n✅ Rapor kaydedildi: {filepath}")
            
        except Exception as e:
            print(f"\n⚠️ Rapor kaydetme hatası: {e}")
            # Hata olsa bile devam et
        
        # Sonuçları render et
        return render_template('full_results.html',
                             cbam_summary=cbam_summary,
                             ets_forecast=ets_forecast.to_dict('records')[:8],
                             ets_stats=ets_stats,
                             report=report,
                             cbam_df=report['cbam_df'].to_dict('records')[:8],
                             emission_analysis=emission_analysis,
                             optimization_scenarios=optimization_scenarios)
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return render_template('error.html', 
                             error=f"Analiz hatası: {str(e)}<br><br><pre>{error_detail}</pre>")


@app.route('/download-pdf')
def download_pdf():
    """Download PDF report"""
    try:
        # App context'ten rapor verisini al
        if not hasattr(app, 'last_report_data') or app.last_report_data is None:
            return "Rapor bulunamadı. Lütfen önce analiz çalıştırın.", 404
        
        report_data = app.last_report_data
        
        # PDF oluştur
        pdf_generator = CBAMPDFGenerator()
        
        pdf_buffer = pdf_generator.generate_report(
            cbam_summary=report_data['cbam_summary'],
            ets_forecast=report_data['ets_forecast'],
            report_text=report_data['report_text'],
            emission_analysis=report_data.get('emission_analysis'),
            optimization_scenarios=report_data.get('optimization_scenarios')
        )
        
        # PDF dosya adı (şirket ismiyle)
        company_name = report_data.get('company_info', {}).get('company_name', 'Firma')
        company_name_clean = company_name.replace(' ', '_').replace('/', '_')
        filename = f"CBAM_Raporu_{company_name_clean}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return f"PDF oluşturma hatası: {str(e)}<br><br><pre>{error_detail}</pre>", 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌍 CBAM WEB UYGULAMASI")
    print("="*70)
    print("\n📱 Adres: http://localhost:5000")
    print("🛑 Durdurmak için: CTRL+C\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
