"""
CBAM Web Application
Flask-based web interface
"""

from flask import Flask, render_template, request, jsonify, send_file, session
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
import json
from decimal import Decimal
import uuid

# Ana proje yolunu ekle
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
    
print(f"🚀 Başlatılıyor... Proje Dizini: {BASE_DIR}")

# Environment variables
load_dotenv()

# Gemini configuration (Lazy loaded to prevent startup timeout)
def get_gemini_client():
    try:
        from google import genai
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return None
        return genai.Client(api_key=api_key)
    except:
        return None

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'cbam-secret-key-2026')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'gemini-2.0-flash')

# Global storage for last report data
app.last_report_data = None

# AWS DynamoDB Configuration
def get_db_table():
    try:
        import boto3
        session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
        )
        dynamodb = session.resource('dynamodb')
        return dynamodb.Table('GrefinsReports')
    except Exception as e:
        print(f"❌ AWS Bağlantı Hatası: {e}")
        return None

def convert_to_decimal(obj):
    """DynamoDB için float değerleri Decimal'e çevirir"""
    if isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    return obj

def save_report_to_aws(data):
    """Veriyi AWS DynamoDB'ye kaydet"""
    table = get_db_table()
    if not table:
        return False
    
    try:
        # report_id Partition Key'dir
        if 'report_id' not in data:
            data['report_id'] = str(uuid.uuid4())
            
        data['created_at'] = datetime.now().isoformat()
        
        # Decimal dönüşümü
        db_data = convert_to_decimal(data)
        
        table.put_item(Item=db_data)
        print(f"✅ Veri AWS'ye kaydedildi: {data['report_id']}")
        return True
    except Exception as e:
        print(f"❌ AWS Kayıt Hatası: {e}")
        return False

def convert_decimal_to_float(obj):
    """DynamoDB'den gelen Decimal değerleri float'a çevirir (JSON için)"""
    if isinstance(obj, list):
        return [convert_decimal_to_float(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def get_reports_from_aws(limit=50):
    """AWS DynamoDB'den geçmiş raporları çek"""
    table = get_db_table()
    if not table:
        return []
    
    try:
        response = table.scan(Limit=limit)
        items = response.get('Items', [])
        # Tarihe göre sırala (en yeni en üstte)
        items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return convert_decimal_to_float(items)
    except Exception as e:
        print(f"❌ AWS Veri Çekme Hatası: {e}")
        return []


@app.route('/dashboard')
def dashboard():
    """Kurumsal Dashboard - Geçmiş Analizler ve Trendler"""
    reports = get_reports_from_aws()
    
    # Trend verisi hazırlama (Zaman serisi)
    trend_data = []
    for r in reversed(reports): # Eskiden yeniye
        trend_data.append({
            'date': r.get('created_at', '')[:10], # YYYY-MM-DD
            'emissions': r.get('emission_analysis', {}).get('total_emissions', 0) or r.get('cbam_summary', {}).get('total_emission', 0),
            'cost': r.get('cbam_summary', {}).get('cbam_cost', 0),
            'company': r.get('company_info', {}).get('company_name', 'Bilinmiyor')
        })
    
    return render_template('dashboard.html', reports=reports, trend_data=trend_data)


@app.route('/')
def index():
    """Ana sayfa - Form"""
    from src.cn_code_database import CN_CODE_DATABASE
    return render_template('index.html', cn_codes=CN_CODE_DATABASE)


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
        
        # AWS'ye kaydet
        aws_data = {
            'type': 'simple_calculation',
            'summary': summary,
            'detailed_data': detailed_data if detailed_data else {},
            'timestamp': datetime.now().isoformat()
        }
        save_report_to_aws(aws_data)
        
        return render_template('results.html', 
                             summary=summary, 
                             detailed_data=detailed_data if detailed_data else None)
        
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/cn-codes')
def cn_codes():
    """CN kodları listesi"""
    from src.cn_code_database import CN_CODE_DATABASE
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
        gemini_client = get_gemini_client()
        if not gemini_client:
            return render_template('error.html', 
                                 error="Gemini API yapılandırılmamış. .env dosyasına GOOGLE_API_KEY ekleyin.")
        
        ets_price = float(request.form['ets_price'])
        quantity = float(request.form['quantity'])
        cn_code = request.form['cn_code']
        
        # CSV path - projede veya Render secrets klasöründe
        csv_path = os.getenv('ETS_CSV_PATH', 'icap-graph-price-data-2014-01-01-2025-11-21.csv')
        
        # Alternatif path denemeleri (Render Secret Files yolu dahil)
        search_paths = [
            csv_path,
            os.path.join('/etc/secrets', os.path.basename(csv_path)),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', os.path.basename(csv_path)),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), os.path.basename(csv_path))
        ]
        
        found_path = None
        for p in search_paths:
            if os.path.exists(p):
                found_path = p
                break
        
        if not found_path:
            return render_template('error.html', 
                                 error=f"ETS fiyat CSV dosyası bulunamadı. Lütfen Render Secrets alanına dosyayı eklediğinizden emin olun.")
        
        csv_path = found_path
        
        # === ADIM 1: CBAM HESAPLAMA ===
        from src.cbam_calculator import CBAMCalculator
        calc = CBAMCalculator(ets_price)
        cbam_summary = calc.get_summary(cn_code, quantity)
        
        if cbam_summary is None:
            return render_template('error.html', error="CN Code bulunamadı!")
        
        # Company info for reports
        company_info = {
            'company_name': request.form.get('company_name', 'Firma'),
            'origin_country': request.form.get('country_code', 'TR'),
            'reporting_period': request.form.get('reporting_period', '2024'),
            'product_name': cbam_summary['product'],
            'cn_code': cn_code,
            'quantity': quantity,
            'sector': request.form.get('sector', 'iron_steel'),
            'production_route': request.form.get('production_route', 'eaf'),
            'export_quantity': float(request.form.get('export_quantity', 0) or 0),
            'financials': {
                'annual_revenue': float(request.form.get('annual_revenue', 0) or 0),
                'export_revenue': float(request.form.get('export_revenue', 0) or 0),
                'profit_margin': float(request.form.get('profit_margin', 0) or 0),
                'electricity_price': float(request.form.get('electricity_price', 90) or 90)
            },
            'scrap_rate': float(request.form.get('scrap_rate', 0) or 0),
            'clinker_ratio': float(request.form.get('clinker_ratio', 95) or 95)
        }
        cbam_summary.update(company_info)
        
        # === YENİ: SCOPE 1 & 2 ANALİZİ ===
        from src.emission_analyzer import EmissionAnalyzer
        emission_analysis = None
        optimization_scenarios = None
        
        # Scope 1 & 2 verilerini topla
        scope1_data = None
        scope2_data = None
        
        if any([request.form.get(f) for f in ['natural_gas_nm3', 'coking_coal_ton', 'diesel_liter', 'purchased_heat_mwh']]):
            scope1_data = {
                'fuel': {
                    'coking_coal_ton': float(request.form.get('coking_coal_ton', 0) or 0),
                    'natural_gas_nm3': float(request.form.get('natural_gas_nm3', 0) or 0),
                    'fuel_oil_ton': float(request.form.get('fuel_oil_ton', 0) or 0)
                },
                'mobile': {
                    'diesel_liter': float(request.form.get('diesel_liter', 0) or 0)
                },
                'process': {
                    'limestone_ton': float(request.form.get('limestone_ton', 0) or 0),
                    'electrode_ton': float(request.form.get('electrode_ton', 0) or 0),
                    'anode_ton': float(request.form.get('anode_ton', 0) or 0),
                    'reductants_ton': float(request.form.get('reductants_ton', 0) or 0),
                    'pfc_emissions_ton': float(request.form.get('pfc_emissions_ton', 0) or 0),
                    'ammonia_ton': float(request.form.get('ammonia_ton', 0) or 0),
                    'nitric_acid_ton': float(request.form.get('nitric_acid_ton', 0) or 0),
                    'alloy_elements_ton': float(request.form.get('alloy_elements_ton', 0) or 0)
                },
                'thermal_systems': {
                    'reheating_fuel_nm3': float(request.form.get('reheating_fuel_nm3', 0) or 0),
                    'purchased_heat_mwh': float(request.form.get('purchased_heat_mwh', 0) or 0)
                },
                'steel_output_ton': float(request.form.get('steel_output_ton', 0) or 5000)
            }
        
        if request.form.get('electricity_consumption_mwh'):
            scope2_data = {
                'electricity': {
                    'electricity_consumption_mwh': float(request.form.get('electricity_consumption_mwh', 0) or 0),
                    'grid_emission_factor_kgco2_kwh': float(request.form.get('grid_emission_factor', 0.44) or 0.44),
                    'source_type': request.form.get('electricity_source', 'grid') 
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
            
        # === ADIM 2: ETS FİYAT TAHMİNLERİ ===
        import gc
        gc.collect() # Belleği temizle
        from src.ets_predictor import ETSPricePredictor
        gemini_client = get_gemini_client()
        predictor = ETSPricePredictor(gemini_client)
        ets_forecast, ets_stats = predictor.predict(csv_path, model=DEFAULT_MODEL)
        gc.collect() # Belleği tekrar temizle
        
        # === ADIM 3: CBAM MALİYET PROJEKSİYONU ===
        from src.cbam_cost_forecaster import CBAMCostForecaster
        forecaster = CBAMCostForecaster(gemini_client)
        cbam_cost_forecast = forecaster.forecast(cbam_summary, ets_forecast, model=DEFAULT_MODEL)
        
        # === ADIM 4: YÖNETİCİ RAPORU (Emisyon analizi dahil) ===
        from src.report_generator import CBAMReportGenerator
        generator = CBAMReportGenerator(gemini_client)
        report = generator.generate_report(
            cbam_summary, 
            ets_forecast, 
            cbam_cost_forecast,
            emission_analysis,
            optimization_scenarios,
            model=DEFAULT_MODEL
        )
        
        # Session'a kaydet (sadece özet bilgiler - cookie limiti için)
        session['last_report'] = {
            'cbam_cost': cbam_summary['cbam_cost'],
            'total_emissions': emission_analysis.get('total_emissions', 0) if emission_analysis else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Tam rapor verisini app context'e kaydet (PDF için)
        app.last_report_data = {
            'cbam_summary': cbam_summary,
            'ets_forecast': report['cbam_df'],
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

  Toplam Emisyon: {cbam_summary['total_emission']:,.2f} tCO2e
  ETS Fiyatı: €{cbam_summary['ets_price']:.2f}/tCO2
  Toplam CBAM Maliyeti: €{cbam_summary['cbam_cost']:,.2f}
  Birim Maliyet: €{cbam_summary['cbam_cost']/quantity:.2f}/ton ürün

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
                
                # Eğer dict gelirse listeye çevir (compatibility)
                scenarios_list = optimization_scenarios.values() if isinstance(optimization_scenarios, dict) else optimization_scenarios
                
                for idx, scenario in enumerate(scenarios_list, 1):
                    report_content += f"{idx}. {scenario.get('name', 'İyileştirme')}\n"
                    report_content += f"   Emisyon Azaltımı: {scenario.get('emission_saving_tco2', 0):,.2f} tCO2\n"
                    report_content += f"   Maliyet Tasarrufu: €{scenario.get('annual_cbam_saving_eur', 0):,.2f}\n"
                    report_content += f"   Geri Ödeme Süresi: {scenario.get('roi_years', 0):,.1f} yıl\n\n"
            
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
        
        # === AWS DYNAMODB KAYIT ===
        try:
            full_aws_data = {
                'type': 'full_analysis',
                'company_info': company_info,
                'cbam_summary': cbam_summary,
                'emission_analysis': emission_analysis,
                'ets_forecast': ets_forecast.to_dict('records')[:8] if hasattr(ets_forecast, 'to_dict') else [],
                'optimization_scenarios': optimization_scenarios if optimization_scenarios else [],
                'report_text': report.get('report_text', ''),
                'timestamp': datetime.now().isoformat()
            }
            save_report_to_aws(full_aws_data)
        except Exception as aws_e:
            print(f"⚠️ AWS full_analysis kayıt hatası: {aws_e}")

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
        from src.pdf_generator import CBAMPDFGenerator
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


if __name__ == "__main__":
    # Render için port ayarı
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
