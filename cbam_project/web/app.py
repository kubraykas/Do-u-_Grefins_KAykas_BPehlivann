"""
CBAM Web Application
Flask-based web interface
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
from dotenv import load_dotenv

# Ana proje yolunu ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.cbam_calculator import CBAMCalculator
from src.cn_code_database import CN_CODE_DATABASE
from src.ets_predictor import ETSPricePredictor
from src.cbam_cost_forecaster import CBAMCostForecaster
from src.report_generator import CBAMReportGenerator

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


@app.route('/')
def index():
    """Ana sayfa - Form"""
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    """CBAM hesaplama yap"""
    try:
        ets_price = float(request.form['ets_price'])
        quantity = float(request.form['quantity'])
        cn_code = request.form['cn_code']
        
        calc = CBAMCalculator(ets_price)
        summary = calc.get_summary(cn_code, quantity)
        
        if summary is None:
            return render_template('error.html', 
                                 error="CN Code bulunamadı!")
        
        return render_template('results.html', summary=summary)
        
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
        
        # === ADIM 2: ETS FİYAT TAHMİNİ ===
        predictor = ETSPricePredictor(gemini_client)
        ets_forecast, ets_stats = predictor.predict(csv_path)
        
        # === ADIM 3: CBAM MALİYET PROJEKSİYONU ===
        forecaster = CBAMCostForecaster(gemini_client)
        cbam_cost_forecast = forecaster.forecast(cbam_summary, ets_forecast)
        
        # === ADIM 4: YÖNETİCİ RAPORU ===
        generator = CBAMReportGenerator(gemini_client)
        report = generator.generate_report(cbam_summary, ets_forecast, cbam_cost_forecast)
        
        # Sonuçları render et
        return render_template('full_results.html',
                             cbam_summary=cbam_summary,
                             ets_forecast=ets_forecast.to_dict('records')[:8],
                             ets_stats=ets_stats,
                             report=report,
                             cbam_df=report['cbam_df'].to_dict('records')[:8])
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return render_template('error.html', 
                             error=f"Analiz hatası: {str(e)}<br><br><pre>{error_detail}</pre>")


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌍 CBAM WEB UYGULAMASI")
    print("="*70)
    print("\n📱 Adres: http://localhost:5000")
    print("🛑 Durdurmak için: CTRL+C\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
